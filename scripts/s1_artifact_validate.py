#!/usr/bin/env python3
"""Validate SecuPilot S1 closed-shadow artifacts for fast MVP checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - exercised only in minimal Python envs.
    Draft202012Validator = None


PASS = 0
HOLD = 20

REQUIRED_FILES = (
    "run_record.json",
    "safety_scan.json",
    "case_summary.json",
    "final_status.json",
    "artifact_manifest.json",
)

SCHEMA_FILE_BY_ARTIFACT = {
    "run_record.json": "run_record.schema.json",
    "safety_scan.json": "safety_scan.schema.json",
    "case_summary.json": "case_summary.schema.json",
    "final_status.json": "final_status.schema.json",
    "artifact_manifest.json": "artifact_manifest.schema.json",
}

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


def format_schema_path(path_parts: Any) -> str:
    rendered = "$"
    for part in path_parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}"
    return rendered


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


def resolve_local_schema_ref(schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported schema ref: {ref}")
    current: Any = schema
    for raw_part in ref[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"unresolvable schema ref: {ref}")
        current = current[part]
    if not isinstance(current, dict):
        raise ValueError(f"schema ref does not resolve to object: {ref}")
    return current


def json_type_matches(expected_type: str, value: Any) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "null":
        return value is None
    return True


def validate_schema_subset(instance: Any, schema: dict[str, Any], path: str = "$", root: dict[str, Any] | None = None) -> list[str]:
    root_schema = root if root is not None else schema
    errors: list[str] = []
    if "$ref" in schema:
        try:
            return validate_schema_subset(instance, resolve_local_schema_ref(root_schema, schema["$ref"]), path, root_schema)
        except ValueError as exc:
            return [f"{path}: invalid schema ({exc})"]

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value is not in enum")

    expected_types = schema.get("type")
    if isinstance(expected_types, str):
        expected_type_list = [expected_types]
    elif isinstance(expected_types, list):
        expected_type_list = [item for item in expected_types if isinstance(item, str)]
    else:
        expected_type_list = []

    if expected_type_list and not any(json_type_matches(expected_type, instance) for expected_type in expected_type_list):
        errors.append(f"{path}: expected type {'/'.join(expected_type_list)}")
        return errors

    if isinstance(instance, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if isinstance(key, str) and key not in instance:
                    errors.append(f"{path}: missing required property {key}")

        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, value in instance.items():
                if key in properties and isinstance(properties[key], dict):
                    errors.extend(validate_schema_subset(value, properties[key], f"{path}.{key}", root_schema))
                elif schema.get("additionalProperties") is False:
                    errors.append(f"{path}: unexpected property {key}")

    if isinstance(instance, list):
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(instance) < min_items:
            errors.append(f"{path}: expected at least {min_items} items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, value in enumerate(instance):
                errors.extend(validate_schema_subset(value, item_schema, f"{path}[{index}]", root_schema))

    if isinstance(instance, str):
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(instance) < min_length:
            errors.append(f"{path}: expected string length >= {min_length}")

    if isinstance(instance, int) and not isinstance(instance, bool):
        minimum = schema.get("minimum")
        if isinstance(minimum, (int, float)) and instance < minimum:
            errors.append(f"{path}: expected value >= {minimum}")

    return errors


def validate_instance_against_schema(file_name: str, instance: Any, schema: dict[str, Any]) -> list[str]:
    if Draft202012Validator is not None:
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            return [f"{file_name}: invalid schema ({exc})"]
        validator = Draft202012Validator(schema)
        schema_errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
        return [
            f"{file_name}: schema violation at {format_schema_path(error.absolute_path)}: {error.message}"
            for error in schema_errors
        ]

    return [
        f"{file_name}: schema violation at {error}"
        for error in validate_schema_subset(instance, schema)
    ]


def validate_schema_dir(schema_dir: Path, artifacts: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not schema_dir.exists():
        return [f"schema directory not found: {schema_dir}"]
    if not schema_dir.is_dir():
        return [f"schema path is not a directory: {schema_dir}"]

    for artifact_name, schema_name in SCHEMA_FILE_BY_ARTIFACT.items():
        schema_path = schema_dir / schema_name
        if not schema_path.exists():
            errors.append(f"missing schema: {schema_name}")
            continue
        try:
            schema = read_json(schema_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{schema_name}: invalid JSON ({exc.msg})")
            continue
        except OSError as exc:
            errors.append(f"{schema_name}: read error ({exc})")
            continue
        if not isinstance(schema, dict):
            errors.append(f"{schema_name}: schema root must be an object")
            continue
        errors.extend(validate_instance_against_schema(artifact_name, artifacts[artifact_name], schema))
    return errors


def validate_artifact_dir(artifact_dir: Path, schema_dir: Path | None = None) -> tuple[int, list[str]]:
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

    if schema_dir is not None:
        errors.extend(validate_schema_dir(schema_dir, loaded))

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

    schema_dir = Path(args.schema_dir).resolve() if args.schema_dir else None
    code, errors = validate_artifact_dir(artifact_dir, schema_dir=schema_dir)
    if code == PASS:
        print(f"PASS: artifact validation succeeded for {artifact_dir}")
        return PASS

    print(f"HOLD: artifact validation failed for {artifact_dir}")
    for error in errors:
        print(f"- {error}")
    return code


if __name__ == "__main__":
    sys.exit(main())
