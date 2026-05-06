#!/usr/bin/env python3
"""Build an offline/local S1 demo package from closed-shadow artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

REQUIRED_ARTIFACT_FILES = (
    "run_record.json",
    "safety_scan.json",
    "case_summary.json",
    "final_status.json",
    "artifact_manifest.json",
    "RUN_RECORD.md",
)

FORBIDDEN_LEAF_KEYS = {
    "raw_payload",
    "raw_evidence",
    "host_raw_evidence",
    "secret",
    "token",
    "auth_header",
    "authorization",
    "cookie",
    "private_key",
    "customer_visible_message",
    "writeback_action",
    "production_connector_output",
}

DEFAULT_RETENTION_CLASS = "S1_CLOSED_SHADOW_EVIDENCE_METADATA"
REVIEWER_README_FILE = "REVIEWER_README.md"
SCREENSHOT_SOURCE_DIR = "playwright"
SCREENSHOT_EXTENSIONS = {".png", ".jpg", ".jpeg"}

FORBIDDEN_TEXT_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"authorization\s*[:=]\s*\S+",
        r"bearer\s+[A-Za-z0-9._~+/=-]{12,}",
        r"api[_-]?key\s*[:=]\s*\S+",
        r"secret\s*[:=]\s*\S+",
        r"token\s*[:=]\s*\S+",
        r"private[_-]?key\s*[:=]\s*\S+",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"raw_payload\s*[:=]",
        r"raw_evidence\s*[:=]",
        r"host_raw_evidence\s*[:=]",
        r"customer_visible_message\s*[:=]",
        r"writeback_action\s*[:=]",
        r"production_connector_output\s*[:=]",
    )
)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def portable_path(path: Path, base: Path | None = None) -> str:
    resolved = path.resolve()
    base = (base or Path.cwd()).resolve()
    try:
        return resolved.relative_to(base).as_posix()
    except ValueError:
        return path.name


def flatten_json(obj: Any, prefix: str = "", depth: int = 0, max_depth: int = 32) -> list[tuple[str, Any]]:
    fields: list[tuple[str, Any]] = []
    if depth > max_depth:
        raise ValueError(f"JSON nesting exceeds max depth {max_depth} at {prefix or '<root>'}")
    if isinstance(obj, dict):
        for key, value in obj.items():
            field_path = f"{prefix}.{key}" if prefix else str(key)
            fields.append((field_path, value))
            fields.extend(flatten_json(value, field_path, depth + 1, max_depth))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            field_path = f"{prefix}[{index}]"
            fields.append((field_path, value))
            fields.extend(flatten_json(value, field_path, depth + 1, max_depth))
    return fields


def validate_artifact_dir(artifact_dir: Path) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    if not artifact_dir.exists():
        return None, [f"artifact directory not found: {artifact_dir}"]

    loaded: dict[str, Any] = {}
    for name in REQUIRED_ARTIFACT_FILES:
        path = artifact_dir / name
        if not path.exists():
            errors.append(f"missing required artifact: {name}")
            continue
        if path.suffix.lower() == ".json":
            try:
                loaded[name] = read_json(path)
            except json.JSONDecodeError as exc:
                errors.append(f"{name}: invalid JSON ({exc.msg})")
            except OSError as exc:
                errors.append(f"{name}: read error ({exc})")
        elif path.suffix.lower() in {".md", ".txt"}:
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                errors.append(f"{name}: read error ({exc})")
                continue
            for pattern in FORBIDDEN_TEXT_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{name}: forbidden text pattern {pattern.pattern}")

    if errors:
        return None, errors

    for file_name, payload in loaded.items():
        try:
            fields = flatten_json(payload)
        except ValueError as exc:
            errors.append(f"{file_name}: {exc}")
            continue
        for field_path, _ in fields:
            leaf = field_path.split(".")[-1].split("[")[0].strip().lower()
            if leaf in FORBIDDEN_LEAF_KEYS:
                errors.append(f"{file_name}: forbidden field key {field_path}")

    manifest = loaded.get("artifact_manifest.json")
    if not isinstance(manifest, dict):
        errors.append("artifact_manifest.json root must be an object")
    else:
        for index, item in enumerate(manifest.get("artifacts", [])):
            if not isinstance(item, dict):
                errors.append(f"artifact_manifest.json artifacts[{index}] must be an object")
                continue
            for flag_key in (
                "contains_raw_payload",
                "contains_secret_or_token",
                "contains_customer_visible_artifact",
            ):
                if item.get(flag_key) is True:
                    errors.append(f"artifact_manifest.json artifacts[{index}] has {flag_key}=true")

    if errors:
        return None, errors
    return loaded, []


def build_retention_map(manifest: dict[str, Any]) -> dict[str, str]:
    retention_map: dict[str, str] = {}
    for item in manifest.get("artifacts", []):
        if not isinstance(item, dict):
            continue
        file_name = item.get("file_name")
        retention_class = item.get("retention_class")
        if isinstance(file_name, str) and isinstance(retention_class, str) and retention_class:
            retention_map[file_name] = retention_class
    return retention_map


def build_reviewer_readme(artifact_dir: Path, output_dir: Path, include_screenshots: bool = False) -> str:
    screenshot_note = (
        "\nVisual screenshots are packaged under `playwright/`.\n"
        if include_screenshots
        else "\nVisual screenshots may be reviewed from the source artifact `playwright/` directory when present.\n"
    )
    return (
        "# SecuPilot S1 Local Demo Package\n\n"
        "## Scope\n\n"
        "This package is for local/offline reviewer inspection only.\n\n"
        "Allowed review:\n\n"
        "```text\n"
        "synthetic S1 run status\n"
        "metadata-only case summary\n"
        "artifact manifest and SHA256 values\n"
        "safety scan summary\n"
        "reviewer notes and follow-up decisions\n"
        "```\n\n"
        "Not allowed from this package:\n\n"
        "```text\n"
        "real data\n"
        "masked-real data\n"
        "live Qwen/API calls\n"
        "live connector setup\n"
        "production credentials\n"
        "production write-back\n"
        "customer-visible publish/deploy\n"
        "external pilot execution\n"
        "```\n\n"
        "## Files\n\n"
        "Start with `package_manifest.json`, then inspect `final_status.json`, "
        "`case_summary.json`, `artifact_manifest.json`, and `safety_scan.json`.\n"
        f"{screenshot_note}\n"
        "Source artifact root:\n\n"
        "```text\n"
        f"{portable_path(artifact_dir)}\n"
        "```\n\n"
        "Package root:\n\n"
        "```text\n"
        f"{portable_path(output_dir)}\n"
        "```\n\n"
        "## Reviewer Checks\n\n"
        "```text\n"
        "run status is understandable\n"
        "case count matches expected synthetic bundle\n"
        "evidence references are metadata-only\n"
        "no raw payloads, credentials, tokens, auth headers, or customer logs appear\n"
        "no write-back or deployment path appears\n"
        "reviewer action is clear\n"
        "```\n\n"
        "Record feedback in the repo feedback form or a governed review note without pasting raw customer data or secrets.\n"
    )


def collect_screenshots(artifact_dir: Path) -> list[Path]:
    screenshot_dir = artifact_dir / SCREENSHOT_SOURCE_DIR
    if not screenshot_dir.exists():
        return []
    return [
        path
        for path in sorted(screenshot_dir.iterdir())
        if path.is_file() and path.suffix.lower() in SCREENSHOT_EXTENSIONS
    ]


def package_artifacts(
    artifact_dir: Path,
    output_dir: Path,
    include_reviewer_readme: bool = False,
    include_screenshots: bool = False,
) -> tuple[int, list[str]]:
    loaded, errors = validate_artifact_dir(artifact_dir)
    if errors:
        return HOLD, errors

    if loaded is None:
        return HOLD, ["artifact validation produced no loaded metadata"]

    output_dir.mkdir(parents=True, exist_ok=True)

    source_manifest = loaded["artifact_manifest.json"]
    retention_map = (
        build_retention_map(source_manifest) if isinstance(source_manifest, dict) else {}
    )

    package_entries: list[dict[str, Any]] = []
    for name in REQUIRED_ARTIFACT_FILES:
        src = artifact_dir / name
        dst = output_dir / name
        source_sha256 = file_sha256(src)
        shutil.copy2(src, dst)
        copy_sha256 = file_sha256(dst)
        if copy_sha256 != source_sha256:
            return HOLD, [f"copy hash mismatch for {name}"]
        package_entries.append(
            {
                "file_name": name,
                "path": name,
                "sha256": source_sha256,
                "bytes": dst.stat().st_size,
                "retention_class": retention_map.get(name, DEFAULT_RETENTION_CLASS),
                "contains_raw_payload": False,
                "contains_secret_or_token": False,
                "contains_customer_visible_artifact": False,
            }
        )

    if include_screenshots:
        screenshots = collect_screenshots(artifact_dir)
        if not screenshots:
            return HOLD, [f"no screenshots found under {SCREENSHOT_SOURCE_DIR}/"]
        screenshot_output_dir = output_dir / SCREENSHOT_SOURCE_DIR
        screenshot_output_dir.mkdir(parents=True, exist_ok=True)
        for src in screenshots:
            dst = screenshot_output_dir / src.name
            source_sha256 = file_sha256(src)
            shutil.copy2(src, dst)
            copy_sha256 = file_sha256(dst)
            if copy_sha256 != source_sha256:
                return HOLD, [f"copy hash mismatch for {SCREENSHOT_SOURCE_DIR}/{src.name}"]
            package_entries.append(
                {
                    "file_name": src.name,
                    "path": f"{SCREENSHOT_SOURCE_DIR}/{src.name}",
                    "sha256": source_sha256,
                    "bytes": dst.stat().st_size,
                    "retention_class": DEFAULT_RETENTION_CLASS,
                    "contains_raw_payload": False,
                    "contains_secret_or_token": False,
                    "contains_customer_visible_artifact": False,
                }
            )

    if include_reviewer_readme:
        readme_path = output_dir / REVIEWER_README_FILE
        readme_path.write_text(
            build_reviewer_readme(artifact_dir, output_dir, include_screenshots=include_screenshots),
            encoding="utf-8",
        )
        text = readme_path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            if pattern.search(text):
                return HOLD, [f"{REVIEWER_README_FILE}: forbidden text pattern {pattern.pattern}"]
        package_entries.append(
            {
                "file_name": REVIEWER_README_FILE,
                "path": REVIEWER_README_FILE,
                "sha256": file_sha256(readme_path),
                "bytes": readme_path.stat().st_size,
                "retention_class": DEFAULT_RETENTION_CLASS,
                "contains_raw_payload": False,
                "contains_secret_or_token": False,
                "contains_customer_visible_artifact": False,
            }
        )

    package_manifest_path = output_dir / "package_manifest.json"
    package_manifest = {
        "schema_version": "secupilot.s1.local_demo_package_manifest.v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_artifact_dir": portable_path(artifact_dir),
        "package_dir": portable_path(output_dir),
        "package_artifacts": package_entries,
    }
    package_manifest_path.write_text(
        json.dumps(package_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return PASS, []


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build local S1 demo package from artifact directory.")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--include-reviewer-readme", action="store_true")
    parser.add_argument("--include-screenshots", action="store_true")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    artifact_dir = Path(args.artifact_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    code, errors = package_artifacts(
        artifact_dir,
        output_dir,
        include_reviewer_readme=args.include_reviewer_readme,
        include_screenshots=args.include_screenshots,
    )
    if code == PASS:
        print(f"PASS: local demo package created at {output_dir}")
        return PASS

    print(f"HOLD: local demo package build failed for {artifact_dir}")
    for error in errors:
        print(f"- {error}")
    return HOLD


def main(argv: list[str] | None = None) -> int:
    return run(argv)


if __name__ == "__main__":
    sys.exit(main())
