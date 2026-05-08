#!/usr/bin/env python3
"""Validate customer trial success criteria and Qwen live-entry gate."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

SCHEMA_VERSION = "secupilot.customer_trial_success_qwen_live_gate.v1"
DEFAULT_JSON_NAME = "customer_trial_success_qwen_live_gate_report.json"
DEFAULT_MD_NAME = "customer_trial_success_qwen_live_gate_report_中文.md"

REQUIRED_ROLES = {"security_engineer", "security_manager", "cto"}
MIN_UNDERSTANDING_RATE = 80.0
MIN_USEFULNESS_RATE = 60.0

BOUNDARY_FALSE_FIELDS = (
    "real_data",
    "masked_real_data",
    "live_qwen_api",
    "live_connectors",
    "network_request",
    "production_writeback",
    "customer_visible_output",
    "deploy_executed",
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


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


def check_boundaries(boundaries: dict[str, Any], checks: list[dict[str, Any]], prefix: str) -> None:
    for field in BOUNDARY_FALSE_FIELDS:
        if field in boundaries:
            add_check(
                checks,
                f"{prefix}-{field}",
                f"{field} remains false",
                boundaries.get(field) is False,
                boundaries.get(field),
                False,
            )


def feedback_roles(feedback_payload: dict[str, Any]) -> set[str]:
    feedback = feedback_payload.get("feedback")
    if not isinstance(feedback, list):
        return set()
    return {str(item.get("reviewer_role", "")) for item in feedback if isinstance(item, dict)}


def validate_qwen_spec(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    required_markers = {
        "synthetic_only": "synthetic" in lowered and "real data" in lowered,
        "explicit_go": "explicit go" in lowered or "explicit qwen" in lowered,
        "no_live_authorization": "not authorize live" in lowered
        or "does not authorize live" in lowered
        or "no, needs later explicit go" in lowered,
        "forbidden_fields": "raw_payload" in lowered and "auth_header" in lowered and "writeback_action" in lowered,
        "timeout_retry_guard": "timeout" in lowered and "retry" in lowered,
    }
    return {
        "path": path.as_posix(),
        "required_markers": required_markers,
        "passed": all(required_markers.values()),
    }


def build_customer_trial_checks(
    *,
    trial_status: dict[str, Any],
    feedback_sample: dict[str, Any],
    kpi_report: dict[str, Any],
    precheck_result: dict[str, Any],
    sizing_report: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "CTS-01",
        "local trial entry ready",
        trial_status.get("status") == "LOCAL_TRIAL_ENTRY_READY",
        trial_status.get("status"),
        "LOCAL_TRIAL_ENTRY_READY",
    )
    add_check(
        checks,
        "CTS-02",
        "role coverage includes engineer manager CTO",
        REQUIRED_ROLES.issubset(feedback_roles(feedback_sample)),
        sorted(feedback_roles(feedback_sample)),
        sorted(REQUIRED_ROLES),
    )
    feedback = kpi_report.get("feedback", {})
    add_check(
        checks,
        "CTS-03",
        "understanding rate threshold",
        float(feedback.get("understanding_rate_percent") or 0) >= MIN_UNDERSTANDING_RATE,
        feedback.get("understanding_rate_percent"),
        f">= {MIN_UNDERSTANDING_RATE}",
    )
    add_check(
        checks,
        "CTS-04",
        "usefulness rate threshold",
        float(feedback.get("usefulness_rate_percent") or 0) >= MIN_USEFULNESS_RATE,
        feedback.get("usefulness_rate_percent"),
        f">= {MIN_USEFULNESS_RATE}",
    )
    add_check(
        checks,
        "CTS-05",
        "no KPI blockers",
        not kpi_report.get("blockers"),
        len(kpi_report.get("blockers", [])),
        0,
    )
    add_check(
        checks,
        "CTS-06",
        "private deployment precheck pass",
        precheck_result.get("status") == "PRIVATE_DEPLOYMENT_PRECHECK_PASS",
        precheck_result.get("status"),
        "PRIVATE_DEPLOYMENT_PRECHECK_PASS",
    )
    add_check(
        checks,
        "CTS-07",
        "sizing report remains draft not benchmarked",
        sizing_report.get("status") == "SIZING_DRAFT_READY_NOT_BENCHMARKED",
        sizing_report.get("status"),
        "SIZING_DRAFT_READY_NOT_BENCHMARKED",
    )
    add_check(
        checks,
        "CTS-08",
        "no production or customer pilot sizing claims",
        all(
            item.get("production_claim") is False and item.get("customer_pilot_claim") is False
            for item in sizing_report.get("sizing_profiles", [])
        ),
        "all sizing profile claims false",
        "production_claim=false and customer_pilot_claim=false",
    )
    check_boundaries(trial_status.get("boundaries", {}), checks, "CTS-TRIAL")
    check_boundaries(precheck_result.get("boundaries", {}), checks, "CTS-PRECHECK")
    return checks


def qwen_live_gate(qwen_spec: dict[str, Any]) -> dict[str, Any]:
    controls = [
        {
            "id": "QWEN-GATE-01",
            "name": "synthetic-only live sandbox scope",
            "status": "DEFINED" if qwen_spec["required_markers"]["synthetic_only"] else "MISSING",
        },
        {
            "id": "QWEN-GATE-02",
            "name": "explicit GO required",
            "status": "DEFINED" if qwen_spec["required_markers"]["explicit_go"] else "MISSING",
        },
        {
            "id": "QWEN-GATE-03",
            "name": "live Qwen not currently authorized",
            "status": "DEFINED" if qwen_spec["required_markers"]["no_live_authorization"] else "MISSING",
        },
        {
            "id": "QWEN-GATE-04",
            "name": "request/response forbidden fields",
            "status": "DEFINED" if qwen_spec["required_markers"]["forbidden_fields"] else "MISSING",
        },
        {
            "id": "QWEN-GATE-05",
            "name": "timeout and retry guard",
            "status": "DEFINED" if qwen_spec["required_markers"]["timeout_retry_guard"] else "MISSING",
        },
        {
            "id": "QWEN-GATE-06",
            "name": "secret runtime provisioning outside repo",
            "status": "REQUIRES_SEPARATE_OPERATOR_CONFIRMATION",
        },
        {
            "id": "QWEN-GATE-07",
            "name": "run id, operator, artifact root, rollback and stop plan",
            "status": "REQUIRES_SEPARATE_GO_RECORD",
        },
    ]
    return {
        "status": "HOLD_PENDING_EXPLICIT_QWEN_LIVE_SYNTHETIC_ONLY_GO",
        "first_allowed_live_scope": "QWEN_LIVE_SYNTHETIC_ONLY_SANDBOX",
        "customer_data_allowed": False,
        "masked_real_data_allowed": False,
        "customer_visible_output_allowed": False,
        "production_writeback_allowed": False,
        "autonomous_action_allowed": False,
        "controls": controls,
        "required_go_fields": [
            "run_id",
            "operator",
            "artifact_root",
            "data_mode=SYNTHETIC_ONLY",
            "provider_flag_default=false",
            "secret_source=human_runtime_or_secret_manager_only",
            "timeout_seconds",
            "max_retries",
            "cost_or_token_budget",
            "stop_conditions",
            "rollback_plan",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    cts_lines = "\n".join(
        f"- {item['id']}: {item['name']} = {'PASS' if item['passed'] else 'HOLD'} "
        f"(observed: {item['observed']})"
        for item in report["customer_trial_success"]["checks"]
    )
    qwen_lines = "\n".join(
        f"- {item['id']}: {item['name']} = {item['status']}"
        for item in report["qwen_live_gate"]["controls"]
    )
    go_lines = "\n".join(f"- {item}" for item in report["qwen_live_gate"]["required_go_fields"])

    return f"""# SecuPilot 客户试用成功标准与 Qwen Live 接入 Gate

Report ID: `{report['report_id']}`

Overall: `{report['overall_status']}`

## 一句话结论

{report['summary']}

## 客户试用成功标准

{cts_lines}

## Qwen Live 接入 Gate

当前状态：`{report['qwen_live_gate']['status']}`

{qwen_lines}

## Qwen Live GO 必须包含

{go_lines}

## 当前允许推进

- 可以继续本地/离线/私有化试用包打磨。
- 可以继续 Qwen dry-run setup flow、config contract、validator、UI preview。
- 可以准备 synthetic-only live sandbox GO 记录。

## 当前不允许

- 不允许真实数据或脱敏真实数据。
- 不允许 live Qwen/API 实际调用。
- 不允许 API key、token、auth header 或 secret 写入 repo、命令、日志、artifact 或聊天。
- 不允许 live connector、生产写回、客户可见发布、外部试点或生产上线。
"""


def build_report(
    *,
    package_dir: Path,
    qwen_spec_path: Path,
    output_dir: Path,
    repo_root: Path,
) -> dict[str, Any]:
    assert_inside_repo(package_dir, repo_root)
    assert_inside_repo(qwen_spec_path, repo_root)
    assert_inside_repo(output_dir, repo_root)
    paths = {
        "trial_status": package_dir / "trial_output" / "customer_trial_status.json",
        "feedback_sample": package_dir / "trial_output" / "customer_trial_feedback.sample.json",
        "kpi_report": package_dir / "trial_output" / "internal_trial_kpi_report.json",
        "precheck_result": package_dir / "trial_output" / "private_deployment_precheck_result.json",
        "sizing_report": package_dir / "trial_output" / "private_deployment_sizing_report.json",
    }
    for name, path in paths.items():
        if not path.exists():
            raise ValueError(f"{name} not found: {path}")
    if not qwen_spec_path.exists():
        raise ValueError(f"Qwen spec not found: {qwen_spec_path}")

    payloads = {name: read_json(path) for name, path in paths.items()}
    for name, payload in payloads.items():
        scan_value(payload, label=name)
    qwen_spec = validate_qwen_spec(qwen_spec_path)
    checks = build_customer_trial_checks(
        trial_status=payloads["trial_status"],
        feedback_sample=payloads["feedback_sample"],
        kpi_report=payloads["kpi_report"],
        precheck_result=payloads["precheck_result"],
        sizing_report=payloads["sizing_report"],
    )
    customer_trial_pass = all(item["passed"] for item in checks)
    qwen_gate = qwen_live_gate(qwen_spec)
    report_id = "secupilot-customer-trial-success-qwen-live-gate"
    json_path = output_dir / DEFAULT_JSON_NAME
    md_path = output_dir / DEFAULT_MD_NAME
    report = {
        "schema_version": SCHEMA_VERSION,
        "report_id": report_id,
        "generated_at_utc": utc_now(),
        "overall_status": "READY_FOR_LOCAL_PRIVATE_TRIAL_AND_HOLD_FOR_QWEN_LIVE",
        "summary": (
            "客户试用成功标准在当前本地/私有化包证据上通过；Qwen live 接入仍保持 HOLD，"
            "必须等待单独的 synthetic-only live GO 和运行时 secret 方案。"
        ),
        "inputs": {name: portable_path(path, repo_root) for name, path in paths.items()}
        | {"qwen_spec": portable_path(qwen_spec_path, repo_root)},
        "customer_trial_success": {
            "status": "PASS_FOR_LOCAL_PRIVATE_TRIAL" if customer_trial_pass else "HOLD",
            "thresholds": {
                "required_roles": sorted(REQUIRED_ROLES),
                "min_understanding_rate_percent": MIN_UNDERSTANDING_RATE,
                "min_usefulness_rate_percent": MIN_USEFULNESS_RATE,
            },
            "checks": checks,
        },
        "qwen_live_gate": qwen_gate,
        "non_authorization": [
            "No real data",
            "No masked-real data",
            "No live Qwen/API call",
            "No API keys/secrets/tokens/auth headers/raw customer logs",
            "No live connectors",
            "No production write-back",
            "No customer-visible publish/deploy/output",
            "No external pilot",
            "No production launch",
        ],
        "next_unlock": "GOAL-MVP-80_MODEL_PROVIDER_SETUP_FLOW_DRY_RUN",
    }
    report["outputs"] = {
        "json": portable_path(json_path, repo_root),
        "markdown": portable_path(md_path, repo_root),
    }
    scan_value(report, label="gate_report")
    md_text = render_markdown(report)
    scan_value(md_text, label=DEFAULT_MD_NAME)
    write_json(json_path, report)
    write_text(md_path, md_text)
    return report


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", required=True, type=Path)
    parser.add_argument("--qwen-spec", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    args = parser.parse_args(argv)

    try:
        report = build_report(
            package_dir=args.package_dir,
            qwen_spec_path=args.qwen_spec,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
        )
    except Exception as exc:  # noqa: BLE001 - CLI converts gate violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    cli_status = "PASS" if report["customer_trial_success"]["status"].startswith("PASS") else "HOLD"
    print(json.dumps({"status": cli_status, "report": report}, ensure_ascii=False, indent=2))
    return PASS if cli_status == "PASS" else HOLD


if __name__ == "__main__":
    sys.exit(run())
