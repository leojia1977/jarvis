#!/usr/bin/env python3
"""Validate local runtime config for a future Qwen live synthetic-only run."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


PASS = 0
HOLD = 20

REPORT_SCHEMA_VERSION = "secupilot.qwen_live_synthetic_runtime_config_validation.v1"
DEFAULT_JSON_NAME = "qwen_live_synthetic_runtime_config_report.json"
DEFAULT_MD_NAME = "qwen_live_synthetic_runtime_config_report_中文.md"

NON_SECRET_ENV_RULES = {
    "SECUPILOT_QWEN_PROVIDER_ENABLED": {"kind": "bool_true"},
    "SECUPILOT_QWEN_SYNTHETIC_ONLY": {"kind": "bool_true"},
    "SECUPILOT_QWEN_API_BASE": {"kind": "https_url"},
    "SECUPILOT_QWEN_MODEL": {"kind": "model_name"},
    "SECUPILOT_QWEN_TIMEOUT_SECONDS": {"kind": "int_range_from_request", "request_key": "timeout_seconds"},
    "SECUPILOT_QWEN_MAX_RETRIES": {"kind": "int_range_from_request", "request_key": "max_retries"},
}

MODEL_NAME_PATTERN = re.compile(r"^[A-Za-z0-9._:/-]{1,128}$")
SECRET_NAME_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]{2,128}$")
FORBIDDEN_VALUE_PATTERNS = tuple(
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


def safe_env_presence(env: dict[str, str], name: str) -> bool:
    return name in env


def safe_env_value(env: dict[str, str], name: str) -> str | None:
    # Non-secret env values are read only for validation and are never written to reports.
    return env.get(name)


def validate_bool_true(value: str | None) -> tuple[bool, str]:
    if value is None:
        return False, "missing"
    return value.strip().lower() == "true", "present_bool_true" if value.strip().lower() == "true" else "present_not_true"


def validate_https_url(value: str | None) -> tuple[bool, str]:
    if value is None:
        return False, "missing"
    parsed = urlparse(value)
    if parsed.scheme != "https":
        return False, "present_invalid_scheme"
    if parsed.username or parsed.password:
        return False, "present_contains_userinfo"
    if not parsed.netloc:
        return False, "present_missing_host"
    if any(pattern.search(value) for pattern in FORBIDDEN_VALUE_PATTERNS):
        return False, "present_contains_forbidden_secret_like_fragment"
    return True, "present_https_url_valid"


def validate_model_name(value: str | None) -> tuple[bool, str]:
    if value is None:
        return False, "missing"
    if any(pattern.search(value) for pattern in FORBIDDEN_VALUE_PATTERNS):
        return False, "present_contains_forbidden_secret_like_fragment"
    if not MODEL_NAME_PATTERN.match(value):
        return False, "present_invalid_model_name"
    return True, "present_model_name_valid"


def validate_int_range(value: str | None, *, minimum: int, maximum: int) -> tuple[bool, str]:
    if value is None:
        return False, "missing"
    try:
        parsed = int(value)
    except ValueError:
        return False, "present_not_integer"
    if minimum <= parsed <= maximum:
        return True, "present_integer_in_range"
    return False, "present_integer_out_of_range"


def request_runtime_limits(request: dict[str, Any]) -> dict[str, int]:
    runtime = request.get("runtime_controls", {})
    return {
        "timeout_seconds": int(runtime.get("timeout_seconds") or 0),
        "max_retries": int(runtime.get("max_retries") or 0),
    }


def validate_request_for_config(request: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    authorization = request.get("authorization", {})
    runtime = request.get("runtime_controls", {})
    add_check(
        checks,
        "RUNTIME-REQ-01",
        "request is prepared not executed",
        request.get("status") == "PREPARED_NOT_EXECUTED",
        request.get("status"),
        "PREPARED_NOT_EXECUTED",
    )
    add_check(
        checks,
        "RUNTIME-REQ-02",
        "request does not authorize live call",
        authorization.get("live_call_authorized") is False,
        authorization.get("live_call_authorized"),
        False,
    )
    add_check(
        checks,
        "RUNTIME-REQ-03",
        "request still requires separate human GO",
        authorization.get("requires_separate_go") is True,
        authorization.get("requires_separate_go"),
        True,
    )
    add_check(
        checks,
        "RUNTIME-REQ-04",
        "request data mode is synthetic only",
        request.get("data_mode") == "SYNTHETIC_ONLY",
        request.get("data_mode"),
        "SYNTHETIC_ONLY",
    )
    add_check(
        checks,
        "RUNTIME-REQ-05",
        "provider disabled by default in request",
        runtime.get("provider_flag_default") is False,
        runtime.get("provider_flag_default"),
        False,
    )
    add_check(
        checks,
        "RUNTIME-REQ-06",
        "secret source remains local runtime or secret manager only",
        runtime.get("secret_source") == "human_runtime_or_secret_manager_only",
        runtime.get("secret_source"),
        "human_runtime_or_secret_manager_only",
    )
    add_check(
        checks,
        "RUNTIME-REQ-07",
        "secret value absent from request package",
        runtime.get("secret_value_present") is False,
        runtime.get("secret_value_present"),
        False,
    )
    return checks


def validate_policy(request: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    runtime = request.get("runtime_controls", {})
    secret_names = runtime.get("secret_env_var_names_allowed", [])
    add_check(
        checks,
        "RUNTIME-POLICY-01",
        "non-secret env names are declared without values",
        set(NON_SECRET_ENV_RULES) == {
            "SECUPILOT_QWEN_PROVIDER_ENABLED",
            "SECUPILOT_QWEN_SYNTHETIC_ONLY",
            "SECUPILOT_QWEN_API_BASE",
            "SECUPILOT_QWEN_MODEL",
            "SECUPILOT_QWEN_TIMEOUT_SECONDS",
            "SECUPILOT_QWEN_MAX_RETRIES",
        },
        sorted(NON_SECRET_ENV_RULES),
        "required env name set",
    )
    add_check(
        checks,
        "RUNTIME-POLICY-02",
        "secret env names are declared as names only",
        isinstance(secret_names, list)
        and bool(secret_names)
        and all(isinstance(name, str) and SECRET_NAME_PATTERN.match(name) for name in secret_names),
        secret_names,
        "one or more uppercase env var names",
    )
    add_check(
        checks,
        "RUNTIME-POLICY-03",
        "request timeout/retry bounds are usable",
        isinstance(runtime.get("timeout_seconds"), int)
        and 1 <= runtime.get("timeout_seconds") <= 60
        and isinstance(runtime.get("max_retries"), int)
        and 0 <= runtime.get("max_retries") <= 2,
        {"timeout_seconds": runtime.get("timeout_seconds"), "max_retries": runtime.get("max_retries")},
        "timeout 1..60 and retries 0..2",
    )
    return checks


def validate_process_env(request: dict[str, Any], env: dict[str, str]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    limits = request_runtime_limits(request)
    for name, rule in NON_SECRET_ENV_RULES.items():
        value = safe_env_value(env, name)
        if rule["kind"] == "bool_true":
            passed, observed = validate_bool_true(value)
            required = "present and true"
        elif rule["kind"] == "https_url":
            passed, observed = validate_https_url(value)
            required = "present https URL without credentials"
        elif rule["kind"] == "model_name":
            passed, observed = validate_model_name(value)
            required = "present safe model name"
        elif rule["kind"] == "int_range_from_request":
            max_value = limits[rule["request_key"]]
            passed, observed = validate_int_range(value, minimum=0 if rule["request_key"] == "max_retries" else 1, maximum=max_value)
            required = f"present integer within request bound <= {max_value}"
        else:
            passed, observed = False, "unknown_rule"
            required = "known rule"
        add_check(checks, f"RUNTIME-ENV-{name}", f"{name} local env config", passed, observed, required)

    for name in request.get("runtime_controls", {}).get("secret_env_var_names_allowed", []):
        add_check(
            checks,
            f"RUNTIME-SECRET-{name}",
            f"{name} secret presence without value retention",
            safe_env_presence(env, name),
            "present_without_value_retention" if safe_env_presence(env, name) else "missing",
            "present in local process env; value is never read into report",
        )
    return checks


def render_markdown(report: dict[str, Any]) -> str:
    check_lines = "\n".join(
        f"- {item['id']}: {item['name']} = {'PASS' if item['passed'] else 'HOLD'} "
        f"(observed: {item['observed']})"
        for item in report["checks"]
    )
    env_lines = "\n".join(f"- {item}" for item in report["required_local_env_names"])
    secret_lines = "\n".join(f"- {item}" for item in report["secret_env_names"])
    return f"""# SecuPilot Qwen Live Synthetic Runtime Config Validator

Report ID: `{report['report_id']}`

Mode: `{report['mode']}`

Overall: `{report['overall_status']}`

Execution status: `{report['execution_status']}`

## 一句话结论

{report['summary']}

## Required Local Runtime Env Names

{env_lines}

## Secret Env Names

{secret_lines}

Secret values are not read into this report.

## Checks

{check_lines}

## 当前不授权

- 不发起 live Qwen/API call。
- 不发起 network request。
- 不读取、不保存、不打印 secret 值。
- 不使用真实数据或脱敏真实数据。
- 不调用 connector，不生产写回，不发布客户可见输出。
"""


def build_report(*, request_path: Path, output_dir: Path, repo_root: Path, mode: str, env: dict[str, str]) -> dict[str, Any]:
    assert_inside_repo(request_path, repo_root)
    assert_inside_repo(output_dir, repo_root)
    if not request_path.exists():
        raise ValueError(f"GO request not found: {request_path}")
    request = read_json(request_path)
    if not isinstance(request, dict):
        raise ValueError("GO request root must be a JSON object")

    checks = validate_request_for_config(request) + validate_policy(request)
    process_env_checked = mode == "process"
    if process_env_checked:
        checks.extend(validate_process_env(request, env))

    passed = all(item["passed"] for item in checks)
    report_id = "secupilot-qwen-live-synthetic-runtime-config-validator"
    json_path = output_dir / DEFAULT_JSON_NAME
    md_path = output_dir / DEFAULT_MD_NAME
    secret_names = request.get("runtime_controls", {}).get("secret_env_var_names_allowed", [])
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_id": report_id,
        "created_at_utc": utc_now(),
        "mode": mode,
        "overall_status": (
            "RUNTIME_CONFIG_POLICY_READY_PROCESS_ENV_NOT_CHECKED"
            if mode == "policy" and passed
            else "RUNTIME_CONFIG_READY_FOR_SYNTHETIC_LIVE_GO_REVIEW_NOT_EXECUTION"
            if mode == "process" and passed
            else "HOLD"
        ),
        "execution_status": "NOT_EXECUTED",
        "network_call": False,
        "live_qwen_api_call": False,
        "process_env_checked": process_env_checked,
        "env_values_retained": False,
        "secret_values_read": False,
        "secret_values_retained": False,
        "request": portable_path(request_path, repo_root),
        "required_local_env_names": sorted(NON_SECRET_ENV_RULES),
        "secret_env_names": secret_names,
        "summary": (
            "Runtime config policy is ready; process env values were intentionally not checked in repo artifact mode."
            if mode == "policy" and passed
            else "Local process runtime config is complete for synthetic-only GO review; no live call was executed."
            if mode == "process" and passed
            else "Runtime config validation failed; do not execute Qwen live synthetic run."
        ),
        "checks": checks,
        "outputs": {
            "json": portable_path(json_path, repo_root),
            "markdown": portable_path(md_path, repo_root),
        },
    }
    write_json(json_path, report)
    write_text(md_path, render_markdown(report))
    return report


def run(argv: list[str] | None = None, *, env: dict[str, str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    parser.add_argument("--mode", choices=("policy", "process"), default="policy")
    args = parser.parse_args(argv)

    try:
        report = build_report(
            request_path=args.request,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
            mode=args.mode,
            env=os.environ if env is None else env,
        )
    except Exception as exc:  # noqa: BLE001 - CLI converts config violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    cli_status = "PASS" if report["overall_status"] != "HOLD" else "HOLD"
    print(json.dumps({"status": cli_status, "report": report}, ensure_ascii=False, indent=2))
    return PASS if cli_status == "PASS" else HOLD


if __name__ == "__main__":
    sys.exit(run())
