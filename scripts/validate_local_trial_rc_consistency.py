#!/usr/bin/env python3
"""Validate local/offline trial RC package naming, manifests, and handoff consistency."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

REQUIRED_JSON_FILES = (
    "package_manifest.json",
    "PACKAGE_INDEX_中文.json",
    "SCREENSHOT_INDEX.json",
)

REQUIRED_REVIEWER_FILES = (
    "REVIEWER_START_HERE_中文.md",
    "REVIEWER_CHECKLIST_中文.md",
    "FEEDBACK_TEMPLATE_中文.md",
)

REQUIRED_EVIDENCE_FILES = (
    "evidence/artifact_manifest.json",
    "evidence/case_summary.json",
    "evidence/final_status.json",
    "evidence/safety_scan.json",
)

REQUIRED_SCREENSHOTS = (
    "screenshots/s1-run-desktop.png",
    "screenshots/s1-run-mobile.png",
    "screenshots/s1-run-first-load-folded-desktop.png",
    "screenshots/s1-trial-desktop.png",
    "screenshots/s1-trial-mobile.png",
)

BOUNDARY_FALSE_KEYS = (
    "real_data",
    "masked_real_data",
    "live_qwen_api",
    "live_connectors",
    "production_writeback",
    "customer_visible_output",
    "push",
)

CANDIDATE_TOKEN_RE = re.compile(r"LOCAL_OFFLINE_TRIAL_RC_\d{3}(?:_CN)?", re.IGNORECASE)
PACKAGE_SLUG_RE = re.compile(
    r"(?:s1-closed-shadow-)?local-offline-trial-rc-\d{3}(?:-[a-z0-9]+)*",
    re.IGNORECASE,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_path(value: str | Path) -> str:
    return str(value).replace("\\", "/").strip().rstrip("/")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_png(path: Path) -> bool:
    return path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def add_finding(findings: list[dict[str, str]], label: str, detail: str) -> None:
    findings.append({"label": label, "detail": detail})


def check_equal(findings: list[dict[str, str]], label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        add_finding(findings, label, f"actual={actual!r}; expected={expected!r}")


def check_boundaries(findings: list[dict[str, str]], source_name: str, payload: dict[str, Any]) -> None:
    boundaries = payload.get("boundaries")
    if not isinstance(boundaries, dict):
        add_finding(findings, "missing_boundaries", source_name)
        return
    for key in BOUNDARY_FALSE_KEYS:
        if boundaries.get(key) is not False:
            add_finding(findings, "boundary_not_false", f"{source_name}:{key}={boundaries.get(key)!r}")


def check_manifest_files(findings: list[dict[str, str]], package_dir: Path, manifest: dict[str, Any]) -> None:
    entries = manifest.get("package_files")
    if not isinstance(entries, list):
        add_finding(findings, "manifest_package_files_missing", "package_manifest.json")
        return

    seen_paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            add_finding(findings, "manifest_entry_invalid", repr(entry))
            continue
        rel_path = normalize_path(entry.get("path", ""))
        seen_paths.add(rel_path)
        if "\\" in str(entry.get("path", "")):
            add_finding(findings, "manifest_path_not_portable", rel_path)
        if not entry.get("sha256"):
            add_finding(findings, "manifest_sha256_missing", rel_path)
        if not entry.get("retention_class"):
            add_finding(findings, "manifest_retention_class_missing", rel_path)
        if entry.get("contains_raw_payload") is not False:
            add_finding(findings, "manifest_raw_payload_flag_not_false", rel_path)
        if entry.get("contains_secret_or_token") is not False:
            add_finding(findings, "manifest_secret_flag_not_false", rel_path)
        if entry.get("contains_customer_visible_artifact") is not False:
            add_finding(findings, "manifest_customer_visible_flag_not_false", rel_path)

        file_path = package_dir / rel_path
        if not file_path.exists():
            add_finding(findings, "manifest_file_missing", rel_path)
            continue
        actual_sha = file_sha256(file_path)
        if entry.get("sha256") != actual_sha:
            add_finding(findings, "manifest_sha256_mismatch", rel_path)

    required = (
        (set(REQUIRED_JSON_FILES) - {"package_manifest.json"})
        | set(REQUIRED_REVIEWER_FILES)
        | set(REQUIRED_EVIDENCE_FILES)
        | set(REQUIRED_SCREENSHOTS)
    )
    for rel_path in sorted(required - seen_paths):
        add_finding(findings, "required_file_not_in_manifest", rel_path)


def collect_text(package_dir: Path, rel_paths: list[str]) -> dict[str, str]:
    texts: dict[str, str] = {}
    for rel_path in rel_paths:
        path = package_dir / rel_path
        if path.exists() and path.is_file():
            texts[rel_path] = path.read_text(encoding="utf-8")
    return texts


def check_text_consistency(
    findings: list[dict[str, str]],
    texts: dict[str, str],
    candidate: str,
    source_candidate: str,
    package_dir_arg: str,
    zip_name: str,
) -> None:
    allowed_candidates = {candidate.upper(), source_candidate.upper()}
    current_package_slug = Path(package_dir_arg).name.lower()
    allowed_package_slugs = {current_package_slug}
    if zip_name:
        allowed_package_slugs.add(zip_name.lower())
        allowed_package_slugs.add(Path(zip_name).stem.lower())
    required_context_files = {"REVIEWER_START_HERE_中文.md", "PACKAGE_INDEX_中文.json", "package_manifest.json"}

    for rel_path, text in texts.items():
        if rel_path in required_context_files:
            if candidate not in text:
                add_finding(findings, "candidate_missing_in_reviewer_text", rel_path)
            if source_candidate not in text:
                add_finding(findings, "source_candidate_missing_in_reviewer_text", rel_path)
            if package_dir_arg not in normalize_path(text):
                add_finding(findings, "package_dir_missing_in_reviewer_text", rel_path)
            if zip_name and zip_name not in text:
                add_finding(findings, "zip_name_missing_in_reviewer_text", rel_path)

        for token in CANDIDATE_TOKEN_RE.findall(text):
            if token.upper() not in allowed_candidates:
                add_finding(findings, "unexpected_candidate_token", f"{rel_path}:{token}")
        for slug in PACKAGE_SLUG_RE.findall(text):
            if slug.lower() not in allowed_package_slugs:
                add_finding(findings, "unexpected_package_slug", f"{rel_path}:{slug}")


def check_screenshot_index(findings: list[dict[str, str]], package_dir: Path, screenshot_index: dict[str, Any]) -> None:
    screenshots = screenshot_index.get("screenshots")
    if not isinstance(screenshots, list):
        add_finding(findings, "screenshot_index_missing_list", "SCREENSHOT_INDEX.json")
        return
    by_path = {normalize_path(item.get("path", "")): item for item in screenshots if isinstance(item, dict)}
    for rel_path in REQUIRED_SCREENSHOTS:
        item = by_path.get(rel_path)
        if not item:
            add_finding(findings, "screenshot_index_missing_path", rel_path)
            continue
        path = package_dir / rel_path
        if not path.exists():
            add_finding(findings, "screenshot_file_missing", rel_path)
        elif not is_png(path):
            add_finding(findings, "screenshot_not_png", rel_path)
        elif item.get("sha256") != file_sha256(path):
            add_finding(findings, "screenshot_sha256_mismatch", rel_path)


def validate(args: argparse.Namespace) -> dict[str, Any]:
    package_dir = Path(args.package_dir)
    package_dir_arg = normalize_path(args.package_dir)
    zip_name = args.zip_name or ""
    blocking: list[dict[str, str]] = []

    if not package_dir.exists():
        add_finding(blocking, "package_dir_missing", package_dir_arg)

    loaded: dict[str, dict[str, Any]] = {}
    for rel_path in REQUIRED_JSON_FILES:
        path = package_dir / rel_path
        if not path.exists():
            add_finding(blocking, "required_json_missing", rel_path)
            continue
        try:
            payload = read_json(path)
        except Exception as exc:  # noqa: BLE001 - malformed package evidence is a HOLD.
            add_finding(blocking, "required_json_invalid", f"{rel_path}:{exc}")
            continue
        if not isinstance(payload, dict):
            add_finding(blocking, "required_json_not_object", rel_path)
            continue
        loaded[rel_path] = payload

    manifest = loaded.get("package_manifest.json", {})
    package_index = loaded.get("PACKAGE_INDEX_中文.json", {})
    screenshot_index = loaded.get("SCREENSHOT_INDEX.json", {})

    for source_name, payload in loaded.items():
        check_equal(blocking, f"{source_name}:candidate_mismatch", payload.get("candidate"), args.candidate)
        check_equal(blocking, f"{source_name}:source_candidate_mismatch", payload.get("source_candidate"), args.source_candidate)
        check_boundaries(blocking, source_name, payload)

    if manifest:
        check_equal(blocking, "package_manifest:package_dir_mismatch", normalize_path(manifest.get("package_dir", "")), package_dir_arg)
        if zip_name:
            check_equal(blocking, "package_manifest:zip_name_mismatch", manifest.get("zip_name"), zip_name)
        check_manifest_files(blocking, package_dir, manifest)

    if package_index:
        check_equal(blocking, "package_index:package_dir_mismatch", normalize_path(package_index.get("package_dir", "")), package_dir_arg)
        if zip_name:
            check_equal(blocking, "package_index:zip_name_mismatch", package_index.get("zip_name"), zip_name)
        for rel_path in REQUIRED_EVIDENCE_FILES:
            if rel_path not in package_index.get("evidence_files", []):
                add_finding(blocking, "package_index_missing_evidence_file", rel_path)
        for rel_path in REQUIRED_SCREENSHOTS:
            if rel_path not in package_index.get("screenshot_files", []):
                add_finding(blocking, "package_index_missing_screenshot_file", rel_path)

    if screenshot_index:
        check_screenshot_index(blocking, package_dir, screenshot_index)

    reviewer_rel_paths = list(REQUIRED_REVIEWER_FILES) + ["PACKAGE_INDEX_中文.json", "SCREENSHOT_INDEX.json", "package_manifest.json"]
    texts = collect_text(package_dir, reviewer_rel_paths)
    for rel_path in REQUIRED_REVIEWER_FILES:
        if rel_path not in texts:
            add_finding(blocking, "required_reviewer_file_missing", rel_path)
    check_text_consistency(blocking, texts, args.candidate, args.source_candidate, package_dir_arg, zip_name)

    zip_path = Path(args.zip_path) if args.zip_path else None
    if zip_path:
        if not zip_path.exists():
            add_finding(blocking, "zip_path_missing", normalize_path(zip_path))
        elif zip_name and zip_path.name != zip_name:
            add_finding(blocking, "zip_path_name_mismatch", f"{zip_path.name} != {zip_name}")

    return {
        "schema_version": "secupilot.s1.local_trial_rc_consistency_check.v1",
        "created_at_utc": utc_now(),
        "status": "HOLD" if blocking else "PASS",
        "candidate": args.candidate,
        "source_candidate": args.source_candidate,
        "package_dir": package_dir_arg,
        "zip_name": zip_name,
        "checked_json_files": sorted(loaded),
        "blocking_finding_count": len(blocking),
        "blocking_findings": blocking,
    }


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--source-candidate", required=True)
    parser.add_argument("--zip-name")
    parser.add_argument("--zip-path")
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args(argv)

    payload = validate(args)
    write_json(args.output_json, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return HOLD if payload["status"] == "HOLD" else PASS


if __name__ == "__main__":
    sys.exit(run())
