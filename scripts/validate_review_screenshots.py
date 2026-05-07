#!/usr/bin/env python3
"""Validate reviewer-clean screenshots and their captured visible-text sidecars."""

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

EXPECTED_SCREENSHOTS = (
    ("s1-run-desktop.png", "/s1-run", "1440x1100"),
    ("s1-run-mobile.png", "/s1-run", "390x1000"),
    ("s1-trial-desktop.png", "/s1-trial", "1440x1100"),
    ("s1-trial-mobile.png", "/s1-trial", "390x1000"),
)

BLOCKING_PATTERNS = (
    ("role_switch_p1_p2_p3", re.compile(r"\bP[123]\b")),
    ("mock_fixture_phase", re.compile(r"Mock Fixture|Mock Redline Fixture", re.IGNORECASE)),
    ("expert_mode", re.compile(r"Expert Mode", re.IGNORECASE)),
    ("stale_local_offline_rc_001_007", re.compile(r"LOCAL_OFFLINE_TRIAL_RC_00[1-7]", re.IGNORECASE)),
    ("stale_rc_package_path_001_007", re.compile(r"local-offline-trial-rc-00[1-7]", re.IGNORECASE)),
    ("stale_s1_closed_shadow_rc_001_007", re.compile(r"s1-closed-shadow-local-offline-trial-rc-00[1-7]", re.IGNORECASE)),
    ("legacy_rc004_package", re.compile(r"rc-004|RC-004")),
    ("secret_or_auth_text", re.compile(r"Authorization:|Bearer |refresh_token|access_token|api_key|private_key", re.IGNORECASE)),
    ("raw_or_writeback_text", re.compile(r"raw_payload|raw_evidence|writeback_action|customer_visible_message", re.IGNORECASE)),
)

WARNING_PATTERNS = (
    ("source_candidate_rc008_phrase", re.compile(r"RC-008\s+中文评审包")),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_png(path: Path) -> bool:
    return path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_one(
    screenshot_dir: Path,
    file_name: str,
    route: str,
    viewport: str,
    expected_candidate: str,
) -> dict[str, Any]:
    screenshot_path = screenshot_dir / file_name
    text_path = screenshot_dir / file_name.replace(".png", ".text.json")
    blocking: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    if not screenshot_path.exists():
        blocking.append({"label": "missing_screenshot", "detail": file_name})
    elif screenshot_path.stat().st_size <= 0:
        blocking.append({"label": "empty_screenshot", "detail": file_name})
    elif not is_png(screenshot_path):
        blocking.append({"label": "not_png", "detail": file_name})

    text_payload: dict[str, Any] = {}
    visible_text = ""
    if not text_path.exists():
        blocking.append({"label": "missing_text_sidecar", "detail": text_path.name})
    else:
        try:
            text_payload = read_json(text_path)
            visible_text = str(text_payload.get("visible_text", ""))
        except Exception as exc:  # noqa: BLE001 - convert malformed evidence to HOLD.
            blocking.append({"label": "invalid_text_sidecar", "detail": f"{text_path.name}:{exc}"})

    if text_payload:
        if text_payload.get("route") != route:
            blocking.append({"label": "route_mismatch", "detail": f"{text_path.name}:{text_payload.get('route')}"})
        if text_payload.get("viewport") != viewport:
            blocking.append({"label": "viewport_mismatch", "detail": f"{text_path.name}:{text_payload.get('viewport')}"})
        if text_payload.get("file_name") != file_name:
            blocking.append({"label": "file_name_mismatch", "detail": f"{text_path.name}:{text_payload.get('file_name')}"})

    if expected_candidate not in visible_text:
        blocking.append({"label": "expected_candidate_missing", "detail": file_name})

    for label, pattern in BLOCKING_PATTERNS:
        if pattern.search(visible_text):
            blocking.append({"label": label, "detail": file_name})
    for label, pattern in WARNING_PATTERNS:
        if pattern.search(visible_text):
            warnings.append({"label": label, "detail": file_name})

    return {
        "file_name": file_name,
        "route": route,
        "viewport": viewport,
        "screenshot_path": screenshot_path.as_posix(),
        "screenshot_sha256": file_sha256(screenshot_path) if screenshot_path.exists() else None,
        "text_sidecar_path": text_path.as_posix(),
        "visible_text_sha256": text_sha256(visible_text) if visible_text else None,
        "blocking_findings": blocking,
        "warnings": warnings,
    }


def validate_screenshots(args: argparse.Namespace) -> dict[str, Any]:
    screenshot_dir = Path(args.screenshot_dir)
    results = [
        validate_one(screenshot_dir, file_name, route, viewport, args.expected_candidate)
        for file_name, route, viewport in EXPECTED_SCREENSHOTS
    ]
    blocking_count = sum(len(item["blocking_findings"]) for item in results)
    warning_count = sum(len(item["warnings"]) for item in results)
    status = "HOLD" if blocking_count else "PASS_WITH_NOTES" if warning_count else "PASS"
    return {
        "schema_version": "secupilot.s1.review_screenshot_safety_scan.v1",
        "created_at_utc": utc_now(),
        "status": status,
        "expected_candidate": args.expected_candidate,
        "screenshot_dir": screenshot_dir.as_posix(),
        "checked": len(results),
        "blocking_finding_count": blocking_count,
        "warning_count": warning_count,
        "results": results,
    }


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshot-dir", required=True)
    parser.add_argument("--expected-candidate", required=True)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args(argv)

    payload = validate_screenshots(args)
    write_json(args.output_json, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return HOLD if payload["status"] == "HOLD" else PASS


if __name__ == "__main__":
    sys.exit(run())
