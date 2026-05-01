#!/usr/bin/env python3
"""Build an offline/local S1 demo package from closed-shadow artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
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


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


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

    if errors:
        return None, errors

    for file_name, payload in loaded.items():
        for field_path, _ in flatten_json(payload):
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


def package_artifacts(artifact_dir: Path, output_dir: Path) -> tuple[int, list[str]]:
    loaded, errors = validate_artifact_dir(artifact_dir)
    if errors:
        return HOLD, errors

    assert loaded is not None
    output_dir.mkdir(parents=True, exist_ok=True)

    source_manifest = loaded["artifact_manifest.json"]
    retention_map = (
        build_retention_map(source_manifest) if isinstance(source_manifest, dict) else {}
    )

    package_entries: list[dict[str, Any]] = []
    for name in REQUIRED_ARTIFACT_FILES:
        src = artifact_dir / name
        dst = output_dir / name
        shutil.copy2(src, dst)
        package_entries.append(
            {
                "file_name": name,
                "path": str(dst.as_posix()),
                "sha256": file_sha256(dst),
                "bytes": dst.stat().st_size,
                "retention_class": retention_map.get(name, DEFAULT_RETENTION_CLASS),
                "contains_raw_payload": False,
                "contains_secret_or_token": False,
                "contains_customer_visible_artifact": False,
            }
        )

    package_manifest_path = output_dir / "package_manifest.json"
    package_manifest = {
        "schema_version": "secupilot.s1.local_demo_package_manifest.v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_artifact_dir": str(artifact_dir.as_posix()),
        "package_dir": str(output_dir.as_posix()),
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
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    artifact_dir = Path(args.artifact_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    code, errors = package_artifacts(artifact_dir, output_dir)
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
