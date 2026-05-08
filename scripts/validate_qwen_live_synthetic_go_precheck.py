#!/usr/bin/env python3
"""Validate a Qwen live synthetic-only GO request without making live calls."""

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

SCHEMA_VERSION = "secupilot.qwen_live_synthetic_go_request.v1"
REPORT_SCHEMA_VERSION = "secupilot.qwen_live_synthetic_go_precheck_report.v1"
DEFAULT_JSON_NAME = "qwen_live_synthetic_go_precheck_report.json"
DEFAULT_MD_NAME = "qwen_live_synthetic_go_precheck_report_中文.md"

REQUIRED_DATA_BOUNDARY_FALSE_FIELDS = (
    "real_data",
    "masked_real_data",
    "raw_payload_allowed",
    "raw_log_allowed",
    "customer_visible_output",
    "production_writeback",
    "live_connectors",
    "autonomous_qwen_action",
)

FORBIDDEN_KEYS = {
    "api_key",
    "access_token",
    "refresh_token",
    "auth_header",
    "authorization_header",
    "private_key",
    "raw_payload",
    "raw_evidence",
    "raw_log",
    "customer_record",
    "cookie",
    "writeback_action",
    "action_command",
    "production_connector_output",
}

FORBIDDEN_TEXT_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}",
        r"\bapi[_-]?key\s*[:=]\s*\S+",
        r"\baccess[_-]?token\s*[:=]\s*\S+",
        r"\brefresh[_-]?token\s*[:=]\s*\S+",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"\bAKIA[0-9A-Z]{16}\b",
        r"\bsig=[A-Za-z0-9%]{16,}",
    )
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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


def scan_forbidden_content(payload: Any) -> list[str]:
    errors: list[str] = []
    for field_path, value in flatten_json(payload):
        leaf = field_path.split(".")[-1].split("[")[0].lower()
        if leaf in FORBIDDEN_KEYS:
            errors.append(f"forbidden key: {field_path}")
        if isinstance(value, str):
            for pattern in FORBIDDEN_TEXT_PATTERNS:
                if pattern.search(value):
                    errors.append(f"forbidden text pattern at {field_path}: {pattern.pattern}")
    return sorted(set(errors))


def add_check(checks: list[dict[str, Any]], check_id: str, name: str, passed: bool, observed: Any, required: Any) -> None:
    checks.append(
        {
            "id": check_id,
            "name": name,
            "passed": bool(passed),
            "observed": observed,
            "required": required,
        }
    )


def is_relative_artifact_root(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts and value.startswith("artifacts/qwen_live_synthetic_runs/")


def validate_go_request(payload: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    authorization = payload.get("authorization", {})
    runtime = payload.get("runtime_controls", {})
    data_boundary = payload.get("data_boundary", {})
    operator = payload.get("operator", {})
    stop_conditions = payload.get("stop_conditions")
    rollback_plan = payload.get("rollback_plan")

    add_check(
        checks,
        "QWEN-GO-01",
        "schema version",
        payload.get("schema_version") == SCHEMA_VERSION,
        payload.get("schema_version"),
        SCHEMA_VERSION,
    )
    add_check(
        checks,
        "QWEN-GO-02",
        "request status is prepared not executed",
        payload.get("status") == "PREPARED_NOT_EXECUTED",
        payload.get("status"),
        "PREPARED_NOT_EXECUTED",
    )
    add_check(
        checks,
        "QWEN-GO-03",
        "live call remains not authorized in precheck",
        authorization.get("live_call_authorized") is False,
        authorization.get("live_call_authorized"),
        False,
    )
    add_check(
        checks,
        "QWEN-GO-04",
        "separate human GO remains required",
        authorization.get("requires_separate_go") is True,
        authorization.get("requires_separate_go"),
        True,
    )
    add_check(
        checks,
        "QWEN-GO-05",
        "data mode is synthetic only",
        payload.get("data_mode") == "SYNTHETIC_ONLY",
        payload.get("data_mode"),
        "SYNTHETIC_ONLY",
    )
    add_check(
        checks,
        "QWEN-GO-06",
        "run id present",
        isinstance(payload.get("run_id"), str) and payload.get("run_id", "").startswith("QWEN-LIVE-SYNTHETIC-"),
        payload.get("run_id"),
        "QWEN-LIVE-SYNTHETIC-*",
    )
    add_check(
        checks,
        "QWEN-GO-07",
        "operator alias present and human confirmation required",
        isinstance(operator, dict)
        and bool(operator.get("alias"))
        and operator.get("confirmation_required") is True
        and operator.get("type") == "human_runtime_operator",
        operator,
        "human_runtime_operator with alias and confirmation_required=true",
    )
    add_check(
        checks,
        "QWEN-GO-08",
        "artifact root is governed relative path",
        is_relative_artifact_root(payload.get("artifact_root")),
        payload.get("artifact_root"),
        "artifacts/qwen_live_synthetic_runs/<run>/",
    )
    add_check(
        checks,
        "QWEN-GO-09",
        "provider disabled by default",
        runtime.get("provider_flag_default") is False,
        runtime.get("provider_flag_default"),
        False,
    )
    add_check(
        checks,
        "QWEN-GO-10",
        "secret source is runtime or secret manager only",
        runtime.get("secret_source") == "human_runtime_or_secret_manager_only",
        runtime.get("secret_source"),
        "human_runtime_or_secret_manager_only",
    )
    add_check(
        checks,
        "QWEN-GO-11",
        "secret value absent from repo package",
        runtime.get("secret_value_present") is False,
        runtime.get("secret_value_present"),
        False,
    )
    add_check(
        checks,
        "QWEN-GO-12",
        "timeout is bounded",
        isinstance(runtime.get("timeout_seconds"), int) and 1 <= runtime.get("timeout_seconds") <= 60,
        runtime.get("timeout_seconds"),
        "integer 1..60",
    )
    add_check(
        checks,
        "QWEN-GO-13",
        "retry count is bounded",
        isinstance(runtime.get("max_retries"), int) and 0 <= runtime.get("max_retries") <= 2,
        runtime.get("max_retries"),
        "integer 0..2",
    )
    add_check(
        checks,
        "QWEN-GO-14",
        "cost and token budget present",
        isinstance(runtime.get("cost_or_token_budget"), dict)
        and isinstance(runtime.get("cost_or_token_budget", {}).get("max_requests"), int)
        and isinstance(runtime.get("cost_or_token_budget", {}).get("max_tokens_per_case"), int)
        and runtime.get("cost_or_token_budget", {}).get("stop_on_budget_exceeded") is True,
        runtime.get("cost_or_token_budget"),
        "max_requests, max_tokens_per_case, stop_on_budget_exceeded=true",
    )
    for field in REQUIRED_DATA_BOUNDARY_FALSE_FIELDS:
        add_check(
            checks,
            f"QWEN-BOUNDARY-{field}",
            f"{field} remains false",
            data_boundary.get(field) is False,
            data_boundary.get(field),
            False,
        )
    add_check(
        checks,
        "QWEN-GO-15",
        "stop conditions are explicit",
        isinstance(stop_conditions, list) and len(stop_conditions) >= 6 and all(isinstance(item, str) and item for item in stop_conditions),
        len(stop_conditions) if isinstance(stop_conditions, list) else type(stop_conditions).__name__,
        "at least 6 non-empty stop conditions",
    )
    add_check(
        checks,
        "QWEN-GO-16",
        "rollback plan is explicit",
        isinstance(rollback_plan, list) and len(rollback_plan) >= 3 and all(isinstance(item, str) and item for item in rollback_plan),
        len(rollback_plan) if isinstance(rollback_plan, list) else type(rollback_plan).__name__,
        "at least 3 rollback steps",
    )
    return checks


def render_markdown(report: dict[str, Any]) -> str:
    check_lines = "\n".join(
        f"- {item['id']}: {item['name']} = {'PASS' if item['passed'] else 'HOLD'} "
        f"(observed: {item['observed']})"
        for item in report["checks"]
    )
    required_lines = "\n".join(f"- {item}" for item in report["required_before_execution"])
    stop_lines = "\n".join(f"- {item}" for item in report["stop_conditions"])
    rollback_lines = "\n".join(f"- {item}" for item in report["rollback_plan"])

    return f"""# SecuPilot Qwen Live Synthetic-Only GO Precheck

Report ID: `{report['report_id']}`

Overall: `{report['overall_status']}`

Execution status: `{report['execution_status']}`

## 一句话结论

{report['summary']}

## Precheck Checks

{check_lines}

## 真正执行前还需要人工确认

{required_lines}

## Stop Conditions

{stop_lines}

## Rollback Plan

{rollback_lines}

## 当前不授权

- 不发起 live Qwen/API call。
- 不使用真实数据或脱敏真实数据。
- 不读取、不保存、不打印 API key、token、auth header 或 secret 值。
- 不调用 connector，不生产写回，不发布客户可见输出。
"""


def build_report(*, request_path: Path, output_dir: Path, repo_root: Path) -> dict[str, Any]:
    assert_inside_repo(request_path, repo_root)
    assert_inside_repo(output_dir, repo_root)
    if not request_path.exists():
        raise ValueError(f"GO request not found: {request_path}")
    payload = read_json(request_path)
    if not isinstance(payload, dict):
        raise ValueError("GO request root must be a JSON object")

    checks = validate_go_request(payload)
    for error in scan_forbidden_content(payload):
        add_check(checks, "QWEN-GO-FORBIDDEN-CONTENT", "forbidden credential or raw-data content scan", False, error, "no findings")

    precheck_pass = all(item["passed"] for item in checks)
    report_id = "secupilot-qwen-live-synthetic-go-precheck"
    json_path = output_dir / DEFAULT_JSON_NAME
    md_path = output_dir / DEFAULT_MD_NAME
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_id": report_id,
        "generated_at_utc": utc_now(),
        "overall_status": "READY_FOR_QWEN_LIVE_SYNTHETIC_GO_REVIEW_NOT_EXECUTION" if precheck_pass else "HOLD",
        "execution_status": "NOT_EXECUTED",
        "network_call": False,
        "live_qwen_api_call": False,
        "summary": (
            "Qwen live synthetic-only GO 参数已具备可审核形态；当前仅完成前置检查，"
            "没有发起 live call，真正执行仍需要单独人工 GO。"
            if precheck_pass
            else "Qwen live synthetic-only GO 前置检查未通过；不得进入 live call。"
        ),
        "request": portable_path(request_path, repo_root),
        "checks": checks,
        "required_before_execution": [
            "human confirms this exact run_id",
            "human supplies runtime secret outside repo and outside chat",
            "operator confirms artifact root is empty or dedicated to this run",
            "operator starts provider flag manually for this run only",
            "operator confirms cost/token budget and timeout/retry values",
            "operator confirms stop conditions and rollback plan",
        ],
        "stop_conditions": payload.get("stop_conditions", []),
        "rollback_plan": payload.get("rollback_plan", []),
        "outputs": {
            "json": portable_path(json_path, repo_root),
            "markdown": portable_path(md_path, repo_root),
        },
    }
    write_json(json_path, report)
    write_text(md_path, render_markdown(report))
    return report


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    args = parser.parse_args(argv)

    try:
        report = build_report(request_path=args.request, output_dir=args.output_dir, repo_root=args.repo_root)
    except Exception as exc:  # noqa: BLE001 - CLI converts gate violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    cli_status = "PASS" if report["overall_status"].startswith("READY_") else "HOLD"
    print(json.dumps({"status": cli_status, "report": report}, ensure_ascii=False, indent=2))
    return PASS if cli_status == "PASS" else HOLD


if __name__ == "__main__":
    sys.exit(run())
