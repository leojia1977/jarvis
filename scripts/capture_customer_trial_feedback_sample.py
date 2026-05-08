#!/usr/bin/env python3
"""Create and validate local/offline SecuPilot customer trial feedback samples."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

SCHEMA_VERSION = "secupilot.customer_trial_feedback_sample.v1"
DEFAULT_OUTPUT_NAME = "customer_trial_feedback.sample.json"

ALLOWED_REVIEWER_ROLES = {
    "security_engineer",
    "security_manager",
    "cto",
    "internal_reviewer",
}

ALLOWED_DECISIONS = {
    "continue_local_trial",
    "needs_more_context",
    "hold_for_fix",
}

FORBIDDEN_BOUNDARY_TRUE_FIELDS = (
    "real_data",
    "masked_real_data",
    "live_qwen_api",
    "live_connectors",
    "network_request",
    "api_key_required",
    "production_writeback",
    "customer_visible_output",
    "deploy_executed",
    "production_launch",
    "push",
    "autonomous_qwen_action",
)

FORBIDDEN_LITERAL_FRAGMENTS = (
    "Authorization:",
    "Bearer ",
    "refresh_token",
    "access_token",
    "api_key:",
    "api_key=",
    "private_key",
    "raw_payload",
    "raw_evidence",
    "cookie:",
    "set-cookie",
    "writeback_action",
    "production_connector_output",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def portable_path(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def assert_inside_repo(path: Path, repo_root: Path) -> None:
    try:
        path.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"path is outside repo: {path}") from exc


def scan_value(value: Any, *, label: str) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            scan_value(nested, label=f"{label}.{key}")
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            scan_value(nested, label=f"{label}[{index}]")
        return
    if not isinstance(value, str):
        return

    lowered = value.lower()
    for fragment in FORBIDDEN_LITERAL_FRAGMENTS:
        if fragment.lower() in lowered:
            raise ValueError(f"{label}: forbidden literal fragment {fragment}")


def default_sample_records() -> list[dict[str, Any]]:
    return [
        {
            "response_id": "FB-SAMPLE-001",
            "reviewer_role": "security_engineer",
            "understood": True,
            "useful": True,
            "missing_information": "",
            "blocker": "",
            "decision": "continue_local_trial",
            "notes": "入口清楚，能确认本地 dry-run 已启动，边界说明可理解。",
        },
        {
            "response_id": "FB-SAMPLE-002",
            "reviewer_role": "security_manager",
            "understood": True,
            "useful": True,
            "missing_information": "希望下一版补充 Windows 前置依赖检查。",
            "blocker": "",
            "decision": "continue_local_trial",
            "notes": "可以继续内部本地试用。",
        },
        {
            "response_id": "FB-SAMPLE-003",
            "reviewer_role": "cto",
            "understood": True,
            "useful": False,
            "missing_information": "希望看到私有化部署资源需求和模型接入路径。",
            "blocker": "",
            "decision": "needs_more_context",
            "notes": "作为产品方向可继续，但上线测试前需要补充部署 sizing。",
        },
    ]


def validate_feedback_payload(payload: dict[str, Any], *, expected_package_id: str | None = None) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if expected_package_id is not None and payload.get("package_id") != expected_package_id:
        errors.append("package_id mismatch")
    if payload.get("data_mode") != "local_offline_feedback_sample":
        errors.append("data_mode must be local_offline_feedback_sample")

    feedback = payload.get("feedback")
    if not isinstance(feedback, list) or not feedback:
        errors.append("feedback must be a non-empty list")
        return errors

    seen_ids: set[str] = set()
    for index, item in enumerate(feedback, start=1):
        if not isinstance(item, dict):
            errors.append(f"feedback[{index}] must be an object")
            continue
        response_id = item.get("response_id")
        if not isinstance(response_id, str) or not response_id.strip():
            errors.append(f"feedback[{index}].response_id is required")
        elif response_id in seen_ids:
            errors.append(f"feedback[{index}].response_id duplicates {response_id}")
        else:
            seen_ids.add(response_id)
        if item.get("reviewer_role") not in ALLOWED_REVIEWER_ROLES:
            errors.append(f"feedback[{index}].reviewer_role is invalid")
        if not isinstance(item.get("understood"), bool):
            errors.append(f"feedback[{index}].understood must be boolean")
        if not isinstance(item.get("useful"), bool):
            errors.append(f"feedback[{index}].useful must be boolean")
        if item.get("decision") not in ALLOWED_DECISIONS:
            errors.append(f"feedback[{index}].decision is invalid")
        for field in ("missing_information", "blocker", "notes"):
            if not isinstance(item.get(field, ""), str):
                errors.append(f"feedback[{index}].{field} must be string")

    return errors


def build_feedback_sample(
    *,
    package_dir: Path,
    output_path: Path,
    repo_root: Path,
    records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    assert_inside_repo(package_dir, repo_root)
    assert_inside_repo(output_path, repo_root)
    manifest_path = package_dir / "package_manifest.json"
    status_path = package_dir / "trial_output" / "customer_trial_status.json"
    if not manifest_path.exists():
        raise ValueError(f"package manifest not found: {manifest_path}")
    if not status_path.exists():
        raise ValueError(f"trial status not found: {status_path}")

    manifest = read_json(manifest_path)
    trial_status = read_json(status_path)
    package_id = str(manifest.get("package_id", ""))
    if not package_id or package_id != trial_status.get("package_id"):
        raise ValueError("package_id mismatch between manifest and trial status")

    boundaries = trial_status.get("boundaries") or manifest.get("boundaries") or {}
    for field in FORBIDDEN_BOUNDARY_TRUE_FIELDS:
        if boundaries.get(field) is not False:
            raise ValueError(f"{field} is not false")

    feedback_records = records or default_sample_records()
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": utc_now(),
        "package_id": package_id,
        "package_dir": portable_path(package_dir, repo_root),
        "data_mode": "local_offline_feedback_sample",
        "source_status": portable_path(status_path, repo_root),
        "feedback": feedback_records,
        "summary": {
            "feedback_count": len(feedback_records),
            "understanding_sample_count": sum(1 for item in feedback_records if "understood" in item),
            "usefulness_sample_count": sum(1 for item in feedback_records if "useful" in item),
            "missing_information_count": sum(1 for item in feedback_records if item.get("missing_information")),
            "blocker_count": sum(1 for item in feedback_records if item.get("blocker")),
        },
        "non_authorization": [
            "No real data",
            "No masked-real data",
            "No live Qwen/API/connectors",
            "No production write-back",
            "No customer-visible publish/deploy",
            "No external pilot",
            "No production launch",
        ],
    }
    scan_value(payload, label="feedback_payload")
    errors = validate_feedback_payload(payload, expected_package_id=package_id)
    if errors:
        raise ValueError("; ".join(errors))
    write_json(output_path, payload)
    return payload


def validate_feedback_file(*, feedback_path: Path, package_dir: Path | None, repo_root: Path) -> dict[str, Any]:
    assert_inside_repo(feedback_path, repo_root)
    expected_package_id = None
    if package_dir is not None:
        assert_inside_repo(package_dir, repo_root)
        manifest_path = package_dir / "package_manifest.json"
        if not manifest_path.exists():
            raise ValueError(f"package manifest not found: {manifest_path}")
        expected_package_id = str(read_json(manifest_path).get("package_id", ""))
    payload = read_json(feedback_path)
    scan_value(payload, label="feedback_payload")
    errors = validate_feedback_payload(payload, expected_package_id=expected_package_id)
    return {
        "schema_version": "secupilot.customer_trial_feedback_validation.v1",
        "status": "HOLD" if errors else "PASS",
        "feedback_path": portable_path(feedback_path, repo_root),
        "feedback_count": len(payload.get("feedback", [])) if isinstance(payload.get("feedback"), list) else 0,
        "errors": errors,
    }


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", type=Path)
    parser.add_argument("--output-path", type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--feedback-json", type=Path)
    args = parser.parse_args(argv)

    try:
        if args.validate_only:
            if args.feedback_json is None:
                raise ValueError("--feedback-json is required with --validate-only")
            result = validate_feedback_file(
                feedback_path=args.feedback_json,
                package_dir=args.package_dir,
                repo_root=args.repo_root,
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return HOLD if result["status"] == "HOLD" else PASS

        if args.package_dir is None:
            raise ValueError("--package-dir is required")
        output_path = args.output_path or args.package_dir / "trial_output" / DEFAULT_OUTPUT_NAME
        payload = build_feedback_sample(
            package_dir=args.package_dir,
            output_path=output_path,
            repo_root=args.repo_root,
        )
    except Exception as exc:  # noqa: BLE001 - CLI converts sample violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    print(
        json.dumps(
            {
                "status": "PASS",
                "feedback_path": portable_path(output_path, args.repo_root),
                "feedback_count": payload["summary"]["feedback_count"],
                "missing_information_count": payload["summary"]["missing_information_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return PASS


if __name__ == "__main__":
    sys.exit(run())
