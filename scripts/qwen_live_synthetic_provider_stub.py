#!/usr/bin/env python3
"""Generate a no-network Qwen synthetic provider stub response."""

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

OUTPUT_SCHEMA_VERSION = "secupilot.qwen_provider_dry_response.v1"
REPORT_SCHEMA_VERSION = "secupilot.qwen_live_synthetic_provider_stub_report.v1"
PROVIDER_STUB_MODE = "qwen_live_synthetic_provider_stub_no_network"
DEFAULT_OUTPUT_NAME = "qwen_live_synthetic_provider_stub_output.json"
DEFAULT_REPORT_NAME = "qwen_live_synthetic_provider_stub_report.json"
DEFAULT_MD_NAME = "qwen_live_synthetic_provider_stub_report_中文.md"

FORBIDDEN_TEXT_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}",
        r"\bapi[_-]?key\s*[:=]\s*\S+",
        r"\baccess[_-]?token\s*[:=]\s*\S+",
        r"\brefresh[_-]?token\s*[:=]\s*\S+",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"\b(isolate|block|delete|disable|quarantine|execute)\b.{0,40}\b(host|account|file|command)\b",
        r"\bapprove\s+immediately\b",
        r"\bbypass\s+approval\b",
        r"\bclose\s+(the\s+)?case\b",
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


def scan_forbidden_text(payload: Any) -> list[str]:
    findings: list[str] = []
    for path, value in flatten_json(payload):
        if isinstance(value, str):
            for pattern in FORBIDDEN_TEXT_PATTERNS:
                if pattern.search(value):
                    findings.append(f"{path}: {pattern.pattern}")
    return sorted(set(findings))


def load_fact_bundles(bundle_dir: Path) -> list[dict[str, Any]]:
    bundles = []
    for path in sorted(bundle_dir.glob("*.json")):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"{path.name}: root must be object")
        payload["_source_file"] = path.name
        bundles.append(payload)
    if not bundles:
        raise ValueError(f"no fact bundle JSON files found: {bundle_dir}")
    return bundles


def validate_fact_bundle(bundle: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    fixture_meta = bundle.get("fixture_meta", {})
    if bundle.get("uat_id") is None:
        errors.append("uat_id missing")
    if bundle.get("scenario_title") is None:
        errors.append("scenario_title missing")
    if not isinstance(bundle.get("facts"), list) or not bundle.get("facts"):
        errors.append("facts missing")
    expected_false = {
        "real_data_derived": False,
        "masked_real_data": False,
        "secrets_present": False,
        "raw_layer0_payload_present": False,
    }
    if fixture_meta.get("synthetic_only") is not True:
        errors.append("fixture_meta.synthetic_only must be true")
    for key, expected in expected_false.items():
        if fixture_meta.get(key) is not expected:
            errors.append(f"fixture_meta.{key} must be {expected}")
    return errors


def build_case(bundle: dict[str, Any]) -> dict[str, Any]:
    unsupported = [
        {"claim": str(claim), "status": "unsupported", "reason": "Not asserted by synthetic metadata."}
        for claim in bundle.get("unsupported_claims", [])
    ]
    return {
        "case_id": str(bundle["uat_id"]),
        "title": str(bundle["scenario_title"]),
        "severity": "review_required",
        "risk_level": "medium",
        "evidence_metadata_refs": [str(bundle.get("source_payload_id") or bundle.get("fact_bundle_id"))],
        "model_summary": (
            f"本地 stub 仅基于 synthetic metadata 生成摘要：{bundle['scenario_title']}。"
            "结论需要人工复核，不产生处置命令。"
        ),
        "reviewer_action": "REVIEW_AND_SIGNOFF_REQUIRED",
        "confidence": 0.7,
        "limitation_note": (
            "No live Qwen/API call. Synthetic metadata only; no raw customer evidence, "
            "connector action, production write-back, or autonomous action."
        ),
        "unsupported_claims_kept_unsupported": unsupported,
    }


def validate_runtime_policy_report(path: Path) -> None:
    report = read_json(path)
    if not isinstance(report, dict):
        raise ValueError("runtime config report root must be object")
    if report.get("overall_status") != "RUNTIME_CONFIG_POLICY_READY_PROCESS_ENV_NOT_CHECKED":
        raise ValueError("runtime config policy report is not ready")
    if report.get("network_call") is not False or report.get("live_qwen_api_call") is not False:
        raise ValueError("runtime config report must record no network/live Qwen call")
    if report.get("secret_values_read") is not False or report.get("secret_values_retained") is not False:
        raise ValueError("runtime config report must not read or retain secret values")


def render_markdown(report: dict[str, Any]) -> str:
    return f"""# SecuPilot Qwen Live Synthetic Provider Stub

Report ID: `{report['report_id']}`

Overall: `{report['overall_status']}`

Execution status: `{report['execution_status']}`

## 一句话结论

{report['summary']}

## 输出

- provider output: `{report['outputs']['provider_output']}`
- report JSON: `{report['outputs']['report_json']}`

## 关键事实

- case_count: `{report['case_count']}`
- provider_stub_mode: `{report['provider_stub_mode']}`
- network_call: `{report['network_call']}`
- live_qwen_api_call: `{report['live_qwen_api_call']}`
- secret_values_read: `{report['secret_values_read']}`
- customer_visible_output: `{report['customer_visible_output']}`
- production_writeback: `{report['production_writeback']}`
- autonomous_qwen_action: `{report['autonomous_qwen_action']}`

## 当前不授权

- 不发起 live Qwen/API call。
- 不发起 network request。
- 不读取 secret 值。
- 不使用真实数据或脱敏真实数据。
- 不调用 connector，不生产写回，不发布客户可见输出。
"""


def build_provider_stub(*, bundle_dir: Path, runtime_config_report: Path, output_dir: Path, repo_root: Path) -> dict[str, Any]:
    assert_inside_repo(bundle_dir, repo_root)
    assert_inside_repo(runtime_config_report, repo_root)
    assert_inside_repo(output_dir, repo_root)
    if not bundle_dir.exists():
        raise ValueError(f"bundle dir not found: {bundle_dir}")
    if not runtime_config_report.exists():
        raise ValueError(f"runtime config report not found: {runtime_config_report}")
    validate_runtime_policy_report(runtime_config_report)
    bundles = load_fact_bundles(bundle_dir)
    bundle_errors = []
    for bundle in bundles:
        for error in validate_fact_bundle(bundle):
            bundle_errors.append(f"{bundle.get('_source_file', '<unknown>')}: {error}")
    if bundle_errors:
        raise ValueError("; ".join(bundle_errors))

    cases = [build_case(bundle) for bundle in bundles]
    output = {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "provider_mode": "dry_contract_only",
        "provider_stub_mode": PROVIDER_STUB_MODE,
        "data_mode": "SYNTHETIC_ONLY",
        "qwen_used": False,
        "live_qwen_api": False,
        "live_connectors": False,
        "customer_visible_output": False,
        "production_writeback": False,
        "autonomous_qwen_action": False,
        "qwen_action_mode": "HITL_SUMMARY_ONLY",
        "network_call": False,
        "secret_values_read": False,
        "secret_values_retained": False,
        "source_bundle_dir": portable_path(bundle_dir, repo_root),
        "runtime_config_report": portable_path(runtime_config_report, repo_root),
        "cases": cases,
    }
    findings = scan_forbidden_text(output)
    if findings:
        raise ValueError("forbidden text in provider output: " + "; ".join(findings))

    output_path = output_dir / DEFAULT_OUTPUT_NAME
    report_path = output_dir / DEFAULT_REPORT_NAME
    md_path = output_dir / DEFAULT_MD_NAME
    write_json(output_path, output)
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_id": "secupilot-qwen-live-synthetic-provider-stub",
        "created_at_utc": utc_now(),
        "overall_status": "QWEN_SYNTHETIC_PROVIDER_STUB_READY_NO_NETWORK",
        "execution_status": "NOT_EXECUTED",
        "provider_stub_mode": PROVIDER_STUB_MODE,
        "case_count": len(cases),
        "network_call": False,
        "live_qwen_api_call": False,
        "secret_values_read": False,
        "secret_values_retained": False,
        "customer_visible_output": False,
        "production_writeback": False,
        "autonomous_qwen_action": False,
        "summary": (
            "Qwen synthetic provider stub generated metadata-only model output from local synthetic bundles; "
            "no network or live Qwen/API call was executed."
        ),
        "outputs": {
            "provider_output": portable_path(output_path, repo_root),
            "report_json": portable_path(report_path, repo_root),
            "report_markdown": portable_path(md_path, repo_root),
        },
    }
    write_json(report_path, report)
    write_text(md_path, render_markdown(report))
    return report


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-dir", required=True, type=Path)
    parser.add_argument("--runtime-config-report", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    args = parser.parse_args(argv)
    try:
        report = build_provider_stub(
            bundle_dir=args.bundle_dir,
            runtime_config_report=args.runtime_config_report,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
        )
    except Exception as exc:  # noqa: BLE001 - CLI converts stub violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD
    print(json.dumps({"status": "PASS", "report": report}, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
