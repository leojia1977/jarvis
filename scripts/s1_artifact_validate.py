#!/usr/bin/env python3
"""Validate SecuPilot S1 closed-shadow artifacts for fast MVP checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

REQUIRED_FILES = (
    "run_record.json",
    "safety_scan.json",
    "case_summary.json",
    "final_status.json",
    "artifact_manifest.json",
)

ALLOWED_RETENTION_CLASSES = {
    "S1_CLOSED_SHADOW_EVIDENCE_METADATA",
}

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


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def flatten_json(obj: Any, prefix: str = "") -> list[tuple[str, Any]]:
    fields: list[tuple[str, Any]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            field_path = f"{prefix}.{key}" if prefix else str(key)
            fields.append((field_path, value))
            fields.extend(flatten_json(value, field_path))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            field_path = f"{prefix}[{index}]"
            fields.append((field_path, value))
            fields.extend(flatten_json(value, field_path))
    return fields


def validate_required_files(artifact_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        path = artifact_dir / name
        if not path.exists():
            errors.append(f"missing required artifact: {name}")
    return errors


def validate_manifest(manifest: dict[str, Any], artifact_dir: Path) -> list[str]:
    errors: list[str] = []
    artifact_dir_resolved = artifact_dir.resolve()
    try:
        expected_manifest_dir = artifact_dir_resolved.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        expected_manifest_dir = artifact_dir_resolved.as_posix()

    actual_artifact_dir = manifest.get("artifact_dir")
    if not isinstance(actual_artifact_dir, str) or actual_artifact_dir != expected_manifest_dir:
        errors.append("manifest artifact_dir mismatch")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("manifest artifacts list is missing or empty")
        return errors

    for index, item in enumerate(artifacts):
        if not isinstance(item, dict):
            errors.append(f"manifest artifact[{index}] is not an object")
            continue
        retention_class = item.get("retention_class")
        if retention_class not in ALLOWED_RETENTION_CLASSES:
            errors.append(f"unknown retention_class: {retention_class!r}")
        for key in ("contains_raw_payload", "contains_secret_or_token", "contains_customer_visible_artifact"):
            if item.get(key) is True:
                errors.append(f"manifest artifact[{index}] has forbidden flag {key}=true")
    return errors


def validate_final_status(final_status: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    boundaries = final_status.get("boundaries_preserved")
    if not isinstance(boundaries, dict):
        return ["final_status.boundaries_preserved is missing or invalid"]
    expected_false_flags = (
        "customer_visible_output",
        "writeback",
        "production_connectors",
        "raw_payload_retention",
        "secret_retention",
    )
    for key in expected_false_flags:
        if boundaries.get(key) is not False:
            errors.append(f"final_status.boundaries_preserved.{key} must be false")
    return errors


def validate_forbidden_keys(artifacts: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for file_name, obj in artifacts.items():
        for field_path, _ in flatten_json(obj):
            leaf = field_path.split(".")[-1].split("[")[0].strip().lower()
            if leaf in FORBIDDEN_LEAF_KEYS:
                errors.append(f"{file_name}: forbidden field key {field_path}")
    return errors


def validate_artifact_dir(artifact_dir: Path) -> tuple[int, list[str]]:
    errors = validate_required_files(artifact_dir)
    if errors:
        return HOLD, errors

    loaded: dict[str, Any] = {}
    for file_name in REQUIRED_FILES:
        try:
            loaded[file_name] = read_json(artifact_dir / file_name)
        except json.JSONDecodeError as exc:
            errors.append(f"{file_name}: invalid JSON ({exc.msg})")
        except OSError as exc:
            errors.append(f"{file_name}: read error ({exc})")

    if errors:
        return HOLD, errors

    manifest = loaded["artifact_manifest.json"]
    if not isinstance(manifest, dict):
        errors.append("artifact_manifest.json root must be an object")
    else:
        errors.extend(validate_manifest(manifest, artifact_dir))

    final_status = loaded["final_status.json"]
    if not isinstance(final_status, dict):
        errors.append("final_status.json root must be an object")
    else:
        errors.extend(validate_final_status(final_status))

    errors.extend(validate_forbidden_keys(loaded))

    if errors:
        return HOLD, errors
    return PASS, []


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate S1 closed-shadow artifact directory.")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--schema-dir", default=None, help="Reserved for MVP-10 schema checks.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    artifact_dir = Path(args.artifact_dir).resolve()
    if not artifact_dir.exists():
        print(f"HOLD: artifact directory not found: {artifact_dir}")
        return HOLD

    code, errors = validate_artifact_dir(artifact_dir)
    if code == PASS:
        print(f"PASS: artifact validation succeeded for {artifact_dir}")
        return PASS

    print(f"HOLD: artifact validation failed for {artifact_dir}")
    for error in errors:
        print(f"- {error}")
    return code


if __name__ == "__main__":
    sys.exit(main())
