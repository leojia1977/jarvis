#!/usr/bin/env python3
"""Validate SecuPilot Qwen provider dry-contract JSON without network calls."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

REQUIRED_FALSE_FIELDS = (
    "qwen_used",
    "live_qwen_api",
    "live_connectors",
    "customer_visible_output",
    "production_writeback",
    "autonomous_qwen_action",
)

ALLOWED_CASE_FIELDS = {
    "case_id",
    "title",
    "summary",
    "severity",
    "risk_level",
    "evidence_metadata_refs",
    "model_summary",
    "reviewer_action",
    "confidence",
    "score",
    "limitation_note",
    "unsupported_claims_kept_unsupported",
}

FORBIDDEN_KEYS = {
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
    "action_command",
    "production_connector_output",
    "autonomous_approval",
    "autonomous_rejection",
    "autonomous_block",
    "autonomous_closure",
}

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
        r"\b(isolate|block|disable|delete|quarantine|execute)\b.{0,60}\b(host|ip|account|file|command)\b",
        r"\bapprove\s+immediately\b",
        r"\bbypass\s+approval\b",
        r"\bclose\s+(the\s+)?case\b",
    )
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


def validate_payload(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["root must be a JSON object"]

    if payload.get("schema_version") != "secupilot.qwen_provider_dry_response.v1":
        errors.append("schema_version must be secupilot.qwen_provider_dry_response.v1")
    if payload.get("provider_mode") != "dry_contract_only":
        errors.append("provider_mode must be dry_contract_only")
    if payload.get("data_mode") != "SYNTHETIC_ONLY":
        errors.append("data_mode must be SYNTHETIC_ONLY")
    if payload.get("qwen_action_mode") != "HITL_SUMMARY_ONLY":
        errors.append("qwen_action_mode must be HITL_SUMMARY_ONLY")

    for key in REQUIRED_FALSE_FIELDS:
        if payload.get(key) is not False:
            errors.append(f"{key} must be false")

    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty list")
    else:
        for index, case in enumerate(cases):
            if not isinstance(case, dict):
                errors.append(f"cases[{index}] must be an object")
                continue
            unknown = sorted(set(case) - ALLOWED_CASE_FIELDS)
            for key in unknown:
                errors.append(f"cases[{index}] has non-whitelisted field: {key}")
            if not isinstance(case.get("case_id"), str) or not case.get("case_id"):
                errors.append(f"cases[{index}].case_id is required")
            if case.get("reviewer_action") != "REVIEW_AND_SIGNOFF_REQUIRED":
                errors.append(f"cases[{index}].reviewer_action must be REVIEW_AND_SIGNOFF_REQUIRED")

    for field_path, value in flatten_json(payload):
        leaf = field_path.split(".")[-1].split("[")[0].lower()
        if leaf in FORBIDDEN_KEYS:
            errors.append(f"forbidden field key: {field_path}")
        if isinstance(value, str):
            for pattern in FORBIDDEN_TEXT_PATTERNS:
                if pattern.search(value):
                    errors.append(f"forbidden text pattern at {field_path}: {pattern.pattern}")
    return sorted(set(errors))


def validate_file(path: Path) -> dict[str, Any]:
    try:
        payload = read_json(path)
    except json.JSONDecodeError as exc:
        return {"path": path.as_posix(), "status": "HOLD", "errors": [f"invalid JSON: {exc.msg}"]}
    except OSError as exc:
        return {"path": path.as_posix(), "status": "HOLD", "errors": [f"read error: {exc}"]}
    errors = validate_payload(payload)
    return {"path": path.as_posix(), "status": "HOLD" if errors else "PASS", "errors": errors}


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract_files", nargs="+", type=Path)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args(argv)

    results = [validate_file(path) for path in args.contract_files]
    payload = {
        "schema_version": "secupilot.qwen_provider_contract_validation.v1",
        "created_at_utc": utc_now(),
        "status": "HOLD" if any(result["errors"] for result in results) else "PASS",
        "network_call": False,
        "live_qwen_api": False,
        "checked": len(results),
        "results": results,
    }
    if args.output_json:
        write_json(args.output_json, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return HOLD if payload["status"] == "HOLD" else PASS


if __name__ == "__main__":
    sys.exit(run())
