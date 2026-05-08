#!/usr/bin/env python3
"""Generate a Windows/local-first private deployment precheck script."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

SCHEMA_VERSION = "secupilot.private_deployment_precheck_contract.v1"
DEFAULT_SCRIPT_NAME = "RUN_PRIVATE_DEPLOYMENT_PRECHECK.ps1"
DEFAULT_CONTRACT_NAME = "private_deployment_precheck_contract.json"

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


def scan_text(text: str, *, label: str) -> None:
    lowered = text.lower()
    for fragment in FORBIDDEN_LITERAL_FRAGMENTS:
        if fragment.lower() in lowered:
            raise ValueError(f"{label}: forbidden literal fragment {fragment}")


def validate_draft(draft: dict[str, Any], manifest: dict[str, Any]) -> None:
    if draft.get("status") != "DRAFT_READY_FOR_INTERNAL_PRODUCT_REVIEW":
        raise ValueError("draft status is not ready for precheck generation")
    if draft.get("blockers"):
        raise ValueError("draft blockers must be empty")
    if draft.get("package_id") != manifest.get("package_id"):
        raise ValueError("package_id mismatch between draft and manifest")
    checks = draft.get("windows_prerequisites", {}).get("checks_to_turn_into_precheck_script")
    if not isinstance(checks, list) or len(checks) < 4:
        raise ValueError("draft must include at least four Windows prerequisite checks")
    required_ids = {"WIN-PREQ-01", "WIN-PREQ-02", "WIN-PREQ-03", "WIN-PREQ-04"}
    found_ids = {str(item.get("id")) for item in checks if isinstance(item, dict)}
    if not required_ids.issubset(found_ids):
        raise ValueError("draft missing required Windows prerequisite check ids")


def precheck_script_template() -> str:
    return r"""param(
  [string]$PackageRoot = ''
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($PackageRoot)) {
  $PackageRoot = Split-Path -Parent $PSScriptRoot
}

$PackageRoot = [System.IO.Path]::GetFullPath($PackageRoot)
$TrialOutputDir = Join-Path $PackageRoot 'trial_output'
$ResultPath = Join-Path $TrialOutputDir 'private_deployment_precheck_result.json'
New-Item -ItemType Directory -Force -Path $TrialOutputDir | Out-Null

$Checks = New-Object System.Collections.Generic.List[object]

function Add-Check {
  param(
    [string]$Id,
    [string]$Name,
    [bool]$Passed,
    [string]$Observed,
    [string]$Remediation
  )
  $Checks.Add([ordered]@{
    id = $Id
    name = $Name
    passed = $Passed
    observed = $Observed
    remediation = $Remediation
  }) | Out-Null
}

$Platform = [System.Environment]::OSVersion.Platform.ToString()
$IsWindowsHost = $Platform -like 'Win*'
Add-Check `
  -Id 'WIN-PREQ-01' `
  -Name 'Windows 本地执行环境' `
  -Passed $IsWindowsHost `
  -Observed ('platform=' + $Platform) `
  -Remediation '请在 Windows 工作站或 Windows Server 上运行本地试用包。'

$PowerShellVersion = $PSVersionTable.PSVersion.ToString()
$PowerShellOk = [version]$PSVersionTable.PSVersion -ge [version]'5.1'
Add-Check `
  -Id 'WIN-PREQ-02' `
  -Name 'PowerShell 执行能力' `
  -Passed $PowerShellOk `
  -Observed ('powershell_version=' + $PowerShellVersion) `
  -Remediation '请使用 PowerShell 5.1 或更新版本运行本地 dry-run 脚本。'

$PythonObserved = ''
$PythonOk = $false
try {
  $PythonOutput = & py -3 --version 2>&1
  $PythonObserved = ($PythonOutput | ForEach-Object { $_.ToString() }) -join ' '
  $PythonOk = $LASTEXITCODE -eq 0
} catch {
  $PythonObserved = $_.Exception.Message
  $PythonOk = $false
}
Add-Check `
  -Id 'WIN-PREQ-03' `
  -Name 'Python 启动器' `
  -Passed $PythonOk `
  -Observed $PythonObserved `
  -Remediation '请安装 Python launcher，并确保 py -3 --version 可以在本机执行。'

$WriteObserved = ''
$WriteOk = $false
$ProbePath = Join-Path $TrialOutputDir ('precheck_write_probe_' + [System.Guid]::NewGuid().ToString('N') + '.tmp')
try {
  Set-Content -LiteralPath $ProbePath -Value 'secupilot-precheck' -Encoding UTF8
  Remove-Item -LiteralPath $ProbePath -Force
  $WriteObserved = 'trial_output writable'
  $WriteOk = $true
} catch {
  $WriteObserved = $_.Exception.Message
  $WriteOk = $false
}
Add-Check `
  -Id 'WIN-PREQ-04' `
  -Name '本地文件权限' `
  -Passed $WriteOk `
  -Observed $WriteObserved `
  -Remediation '请确认当前用户可以读取包目录并写入 trial_output 目录。'

$AllPassed = -not ($Checks | Where-Object { -not $_.passed })
$Status = if ($AllPassed) { 'PRIVATE_DEPLOYMENT_PRECHECK_PASS' } else { 'PRIVATE_DEPLOYMENT_PRECHECK_HOLD' }
$ExitCode = if ($AllPassed) { 0 } else { 20 }

$Result = [ordered]@{
  schema_version = 'secupilot.private_deployment_precheck_result.v1'
  generated_at_utc = (Get-Date).ToUniversalTime().ToString('o')
  package_root = (Split-Path -Leaf $PackageRoot)
  status = $Status
  checks = $Checks
  boundaries = [ordered]@{
    deploy_executed = $false
    network_request = $false
    live_qwen_api = $false
    live_connectors = $false
    production_writeback = $false
    customer_visible_output = $false
    real_data = $false
    masked_real_data = $false
  }
  non_authorization = @(
    'No deployment executed',
    'No network request made',
    'No live Qwen/API call made',
    'No connector call made',
    'No production write-back made',
    'No customer-visible output produced',
    'No real or masked-real data used'
  )
}

$Result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ResultPath -Encoding UTF8

Write-Output 'SecuPilot private deployment local precheck'
Write-Output $Status
Write-Output ('status_file=' + $ResultPath)
foreach ($Check in $Checks) {
  Write-Output ($Check.id + '=' + $Check.passed.ToString().ToLower() + ' ' + $Check.observed)
}
Write-Output 'deploy_executed=false'
Write-Output 'network_request=false'
Write-Output 'live_qwen_api=false'
Write-Output 'production_writeback=false'
Write-Output 'customer_visible_output=false'

exit $ExitCode
"""


def build_precheck(
    *,
    package_dir: Path,
    draft_json: Path,
    output_script: Path,
    contract_path: Path,
    repo_root: Path,
) -> dict[str, Any]:
    assert_inside_repo(package_dir, repo_root)
    assert_inside_repo(draft_json, repo_root)
    assert_inside_repo(output_script, repo_root)
    assert_inside_repo(contract_path, repo_root)
    manifest_path = package_dir / "package_manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"package manifest not found: {manifest_path}")
    if not draft_json.exists():
        raise ValueError(f"prereq/sizing draft not found: {draft_json}")

    manifest = read_json(manifest_path)
    draft = read_json(draft_json)
    validate_draft(draft, manifest)

    script_text = precheck_script_template()
    scan_text(script_text, label=DEFAULT_SCRIPT_NAME)
    write_text(output_script, script_text)

    contract = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": utc_now(),
        "package_id": manifest["package_id"],
        "package_dir": portable_path(package_dir, repo_root),
        "source_draft": portable_path(draft_json, repo_root),
        "precheck_script": portable_path(output_script, repo_root),
        "expected_result": portable_path(package_dir / "trial_output" / "private_deployment_precheck_result.json", repo_root),
        "checks": [
            "WIN-PREQ-01 Windows local execution environment",
            "WIN-PREQ-02 PowerShell execution",
            "WIN-PREQ-03 Python launcher",
            "WIN-PREQ-04 Local file permissions",
        ],
        "boundaries": {
            "deploy_executed": False,
            "network_request": False,
            "live_qwen_api": False,
            "live_connectors": False,
            "production_writeback": False,
            "customer_visible_output": False,
            "real_data": False,
            "masked_real_data": False,
        },
        "next_unlock": "GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT",
    }
    scan_text(json.dumps(contract, ensure_ascii=False), label=DEFAULT_CONTRACT_NAME)
    write_json(contract_path, contract)
    return contract


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", required=True, type=Path)
    parser.add_argument("--draft-json", required=True, type=Path)
    parser.add_argument("--output-script", type=Path)
    parser.add_argument("--contract-path", type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    args = parser.parse_args(argv)

    output_script = args.output_script or args.package_dir / "scripts" / DEFAULT_SCRIPT_NAME
    contract_path = args.contract_path or args.package_dir / "trial_output" / DEFAULT_CONTRACT_NAME
    try:
        contract = build_precheck(
            package_dir=args.package_dir,
            draft_json=args.draft_json,
            output_script=output_script,
            contract_path=contract_path,
            repo_root=args.repo_root,
        )
    except Exception as exc:  # noqa: BLE001 - CLI converts precheck generation violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    print(json.dumps({"status": "PASS", "contract": contract}, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
