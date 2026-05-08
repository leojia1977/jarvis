#!/usr/bin/env python3
"""Generate a dry operator runbook for a future Qwen live synthetic-only run."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

MANIFEST_SCHEMA_VERSION = "secupilot.qwen_live_synthetic_operator_runbook_manifest.v1"
RUNBOOK_NAME = "qwen_live_synthetic_operator_runbook_中文.md"
DRY_COMMAND_NAME = "qwen_live_synthetic_dry_command.ps1"
MANIFEST_NAME = "qwen_live_synthetic_operator_runbook_manifest.json"


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


def validate_inputs(request: dict[str, Any], precheck: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    authorization = request.get("authorization", {})
    runtime = request.get("runtime_controls", {})
    data_boundary = request.get("data_boundary", {})

    if request.get("status") != "PREPARED_NOT_EXECUTED":
        errors.append("GO request status must be PREPARED_NOT_EXECUTED")
    if authorization.get("live_call_authorized") is not False:
        errors.append("GO request must not authorize live call")
    if authorization.get("requires_separate_go") is not True:
        errors.append("GO request must require separate human GO")
    if request.get("data_mode") != "SYNTHETIC_ONLY":
        errors.append("GO request data_mode must be SYNTHETIC_ONLY")
    if not str(request.get("run_id", "")).startswith("QWEN-LIVE-SYNTHETIC-"):
        errors.append("run_id must start with QWEN-LIVE-SYNTHETIC-")
    if runtime.get("provider_flag_default") is not False:
        errors.append("provider flag must default to false")
    if runtime.get("secret_source") != "human_runtime_or_secret_manager_only":
        errors.append("secret_source must be human_runtime_or_secret_manager_only")
    if runtime.get("secret_value_present") is not False:
        errors.append("secret value must not be present in request package")
    if precheck.get("overall_status") != "READY_FOR_QWEN_LIVE_SYNTHETIC_GO_REVIEW_NOT_EXECUTION":
        errors.append("precheck report must be READY_FOR_QWEN_LIVE_SYNTHETIC_GO_REVIEW_NOT_EXECUTION")
    if precheck.get("execution_status") != "NOT_EXECUTED":
        errors.append("precheck execution_status must be NOT_EXECUTED")
    if precheck.get("network_call") is not False or precheck.get("live_qwen_api_call") is not False:
        errors.append("precheck must record no network or live Qwen call")
    for field in (
        "real_data",
        "masked_real_data",
        "raw_payload_allowed",
        "raw_log_allowed",
        "customer_visible_output",
        "production_writeback",
        "live_connectors",
        "autonomous_qwen_action",
    ):
        if data_boundary.get(field) is not False:
            errors.append(f"data boundary {field} must be false")
    if not isinstance(request.get("stop_conditions"), list) or len(request.get("stop_conditions", [])) < 6:
        errors.append("stop_conditions must contain at least 6 items")
    if not isinstance(request.get("rollback_plan"), list) or len(request.get("rollback_plan", [])) < 3:
        errors.append("rollback_plan must contain at least 3 items")
    return errors


def render_runbook(request: dict[str, Any], precheck: dict[str, Any], dry_command_path: str) -> str:
    runtime = request["runtime_controls"]
    budget = runtime["cost_or_token_budget"]
    secret_names = ", ".join(runtime.get("secret_env_var_names_allowed", []))
    stop_lines = "\n".join(f"- {item}" for item in request["stop_conditions"])
    rollback_lines = "\n".join(f"- {item}" for item in request["rollback_plan"])

    return f"""# SecuPilot Qwen Live Synthetic-Only Operator Runbook

Run ID: `{request['run_id']}`

Request ID: `{request['request_id']}`

Status: `OPERATOR_RUNBOOK_READY_DRY_COMMAND_ONLY`

## 一句话结论

这份手册说明操作员未来如何在本机准备一次 Qwen live synthetic-only run。当前产物只提供 dry command，不发起 live call，不读取 secret 值，不调用 Qwen/API。

## 操作员

- alias: `{request['operator']['alias']}`
- type: `{request['operator']['type']}`
- confirmation required: `{request['operator']['confirmation_required']}`

## 输入与输出

- input package: `{request['input_package']}`
- artifact root: `{request['artifact_root']}`
- precheck status: `{precheck['overall_status']}`
- dry command: `{dry_command_path}`

## Runtime Secret 提供方式

1. 打开一个新的本机 PowerShell session。
2. 从人工控制的 secret manager 或本机安全输入渠道取得 Qwen runtime secret。
3. 只在这个本机 session 里设置 `{secret_names}`。
4. 不要把 secret 写入 repo、脚本、Markdown、JSON、命令历史、日志、artifact 或聊天。
5. dry command 不会读取、保存、打印或校验 secret 值。

## 未来真实 synthetic-only run 前必须人工确认

- exact run ID: `{request['run_id']}`
- data mode: `{request['data_mode']}`
- provider flag default: `{runtime['provider_flag_default']}`
- secret source: `{runtime['secret_source']}`
- timeout seconds: `{runtime['timeout_seconds']}`
- max retries: `{runtime['max_retries']}`
- max requests: `{budget['max_requests']}`
- max tokens per case: `{budget['max_tokens_per_case']}`
- stop on budget exceeded: `{budget['stop_on_budget_exceeded']}`

## Dry Command 使用方式

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File {dry_command_path}
```

该命令只打印运行计划和人工确认项；它不会执行 live runner。

## Stop Conditions

{stop_lines}

## Rollback Plan

{rollback_lines}

## 当前不授权

- 不授权 live Qwen/API call。
- 不授权真实数据或脱敏真实数据。
- 不授权 live connector。
- 不授权生产写回。
- 不授权客户可见输出。
- 不授权 autonomous Qwen action。
"""


def render_dry_command(request: dict[str, Any]) -> str:
    runtime = request["runtime_controls"]
    budget = runtime["cost_or_token_budget"]
    secret_names = ", ".join(runtime.get("secret_env_var_names_allowed", []))
    return f"""# SecuPilot Qwen live synthetic-only dry command.
# This script is intentionally non-executing. It prints a future run plan only.

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$plan = [ordered]@{{
  mode = 'DRY_COMMAND_ONLY_NO_LIVE_CALL'
  run_id = '{request['run_id']}'
  request_id = '{request['request_id']}'
  operator_alias = '{request['operator']['alias']}'
  data_mode = '{request['data_mode']}'
  input_package = '{request['input_package']}'
  artifact_root = '{request['artifact_root']}'
  provider_flag_default = $false
  timeout_seconds = {runtime['timeout_seconds']}
  max_retries = {runtime['max_retries']}
  max_requests = {budget['max_requests']}
  max_tokens_per_case = {budget['max_tokens_per_case']}
  runtime_secret_env_var_names = '{secret_names}'
  execution_status = 'NOT_EXECUTED'
  network_call = $false
  live_qwen_api_call = $false
  live_connectors = $false
  production_writeback = $false
  customer_visible_output = $false
  autonomous_qwen_action = $false
  next_manual_steps = @(
    'Open a fresh local PowerShell session.',
    'Provide the runtime secret only in that local session from a human-controlled source.',
    'Confirm this exact run_id and artifact_root.',
    'Run a future live runner only after a separate synthetic-only GO.',
    'Do not paste secrets into repo files, logs, artifacts, command history, or chat.'
  )
}}

$plan | ConvertTo-Json -Depth 5
exit 0
"""


def build_outputs(*, request_path: Path, precheck_path: Path, output_dir: Path, repo_root: Path) -> dict[str, Any]:
    assert_inside_repo(request_path, repo_root)
    assert_inside_repo(precheck_path, repo_root)
    assert_inside_repo(output_dir, repo_root)
    if not request_path.exists():
        raise ValueError(f"GO request not found: {request_path}")
    if not precheck_path.exists():
        raise ValueError(f"precheck report not found: {precheck_path}")

    request = read_json(request_path)
    precheck = read_json(precheck_path)
    errors = validate_inputs(request, precheck)
    if errors:
        raise ValueError("; ".join(errors))

    runbook_path = output_dir / RUNBOOK_NAME
    dry_command_path = output_dir / DRY_COMMAND_NAME
    manifest_path = output_dir / MANIFEST_NAME
    write_text(runbook_path, render_runbook(request, precheck, portable_path(dry_command_path, repo_root)))
    write_text(dry_command_path, render_dry_command(request))
    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "created_at_utc": utc_now(),
        "status": "OPERATOR_RUNBOOK_READY_DRY_COMMAND_ONLY",
        "execution_status": "NOT_EXECUTED",
        "network_call": False,
        "live_qwen_api_call": False,
        "request": portable_path(request_path, repo_root),
        "precheck_report": portable_path(precheck_path, repo_root),
        "outputs": {
            "runbook": portable_path(runbook_path, repo_root),
            "dry_command": portable_path(dry_command_path, repo_root),
            "manifest": portable_path(manifest_path, repo_root),
        },
        "run_id": request["run_id"],
        "operator_alias": request["operator"]["alias"],
        "runtime_secret_source": request["runtime_controls"]["secret_source"],
        "non_authorization": [
            "No live Qwen/API call",
            "No network request",
            "No real data",
            "No masked-real data",
            "No secret value read or stored",
            "No live connectors",
            "No production write-back",
            "No customer-visible output",
            "No autonomous Qwen action",
        ],
    }
    write_json(manifest_path, manifest)
    return manifest


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--precheck-report", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    args = parser.parse_args(argv)

    try:
        manifest = build_outputs(
            request_path=args.request,
            precheck_path=args.precheck_report,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
        )
    except Exception as exc:  # noqa: BLE001 - CLI converts generation violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    print(json.dumps({"status": "PASS", "manifest": manifest}, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
