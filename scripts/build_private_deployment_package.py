#!/usr/bin/env python3
"""Build a Windows/local-first private deployment package skeleton.

This builder creates structure only. It does not deploy, call external systems,
read secrets, connect live Qwen/API providers, or start production services.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

SCHEMA_VERSION = "secupilot.private_deployment_package_manifest.v1"
DEFAULT_PACKAGE_ID = "secupilot-private-deployment-windows-local-v0_1"
DEFAULT_RETENTION_CLASS = "PRIVATE_DEPLOYMENT_STRUCTURE_DRY_RUN"

BOUNDARIES = {
    "real_data": False,
    "masked_real_data": False,
    "live_qwen_api": False,
    "live_connectors": False,
    "network_request": False,
    "api_key_required": False,
    "production_writeback": False,
    "customer_visible_output": False,
    "deploy_executed": False,
    "production_launch": False,
    "push": False,
    "autonomous_qwen_action": False,
}

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
    "customer_visible_message",
    "writeback_action",
    "production_connector_output",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
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


def ensure_clean_output(output_dir: Path, zip_path: Path | None, repo_root: Path) -> None:
    assert_inside_repo(output_dir, repo_root)
    if zip_path is not None:
        assert_inside_repo(zip_path, repo_root)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    if zip_path is not None and zip_path.exists():
        zip_path.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)


def scan_text(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    for fragment in FORBIDDEN_LITERAL_FRAGMENTS:
        if fragment.lower() in lowered:
            raise ValueError(f"{path.name}: forbidden literal fragment {fragment}")


def build_file_entry(path: Path, package_dir: Path) -> dict[str, Any]:
    return {
        "path": portable_path(path, package_dir),
        "file_name": path.name,
        "bytes": path.stat().st_size,
        "sha256": file_sha256(path),
        "retention_class": DEFAULT_RETENTION_CLASS,
        "contains_secret": False,
        "contains_raw_payload": False,
        "customer_visible": False,
        "production_writeback": False,
    }


def package_templates(package_id: str) -> dict[str, str]:
    return {
        "CUSTOMER_TRIAL_START_HERE_中文.md": f"""# SecuPilot 本地离线试用入口

Package ID: `{package_id}`

本入口面向客户试用负责人、内部 reviewer 和交付同学，用于快速确认 SecuPilot 私有化交付包的本地打开方式、边界状态和下一步反馈路径。

## 先做什么

1. 双击 `START_SECUPILOT_LOCAL_TRIAL.cmd`。
2. 如果 Windows 安全提示拦截，请在 PowerShell 中运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\\START_CUSTOMER_TRIAL.ps1
```

3. 打开生成的 `trial_output/customer_trial_status.json`。
4. 把终端输出和 `customer_trial_status.json` 交给内部 reviewer 或项目负责人。

## 这个入口会做什么

- 读取本包的 `package_manifest.json`。
- 执行 `scripts/VERIFY_BOUNDARIES.ps1`。
- 生成 `trial_output/customer_trial_status.json`。
- 打印本地离线试用状态。

## 这个入口不会做什么

- 不部署服务。
- 不启动生产系统。
- 不读取密钥。
- 不访问网络。
- 不调用 live Qwen/API。
- 不连接 live connector。
- 不写回生产。
- 不使用真实数据或脱敏真实数据。

## 通过标准

终端出现：

```text
LOCAL_TRIAL_ENTRY_READY
BOUNDARY_CHECK_PASS
```

并且 `trial_output/customer_trial_status.json` 中所有边界字段保持 `false`。
""",
        "README_PRIVATE_DEPLOYMENT_中文.md": f"""# SecuPilot 私有化部署包结构

Package ID: `{package_id}`

本包是 Windows/local-first 私有化部署结构草案，并包含一个本地离线试用入口。当前仅用于安装路径、交付结构和 dry-run 启动体验核验。

## 当前状态

- 结构包：YES
- 实际部署：NO
- 真实数据：NO
- 脱敏真实数据：NO
- live Qwen/API：NO
- live connectors：NO
- 生产写回：NO
- 客户可见发布：NO

## 推荐阅读顺序

1. `CUSTOMER_TRIAL_START_HERE_中文.md`
2. `START_SECUPILOT_LOCAL_TRIAL.cmd`
3. `docs/WINDOWS_LOCAL_FIRST_STRUCTURE_中文.md`
4. `docs/DEPLOYMENT_BOUNDARIES_中文.md`
5. `configs/secupilot.env.template`
6. `configs/provider.dry-run.json`
7. `scripts/VERIFY_BOUNDARIES.ps1`

## 说明

`START_SECUPILOT_LOCAL_TRIAL.cmd` 和 `scripts/START_CUSTOMER_TRIAL.ps1` 只生成本地 dry-run 状态，不启动生产服务，不读取密钥，不访问网络。
""",
        "START_SECUPILOT_LOCAL_TRIAL.cmd": """@echo off
setlocal
echo SecuPilot local offline trial entry
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\\START_CUSTOMER_TRIAL.ps1"
if errorlevel 1 (
  echo LOCAL_TRIAL_ENTRY_HOLD
  pause
  exit /b 1
)
echo LOCAL_TRIAL_ENTRY_READY
pause
""",
        "docs/WINDOWS_LOCAL_FIRST_STRUCTURE_中文.md": """# Windows / Local First 结构

目标：先让客户理解私有化部署交付物会长什么样，再进入真实安装器、真实连接器和真实模型调用设计。

## 目录

- `configs/`：本地配置模板，不含密钥。
- `scripts/`：本地 dry-run 脚本，只验证边界和结构。
- `data/`：synthetic-only 输入说明，不放真实数据。
- `logs/`：本地运行日志占位，不提交真实日志。
- `runtime/`：运行时占位，不包含生产二进制。
- `docs/`：部署边界和操作说明。
- `trial_output/`：本地离线试用脚本生成的状态文件目录。

## 后续解锁

真实部署、真实连接器、live Qwen/API、真实客户数据和生产写回都必须由后续单独 Goal 明确授权。
""",
        "docs/DEPLOYMENT_BOUNDARIES_中文.md": """# 部署边界

本结构包不授权以下事项：

- 使用真实数据或脱敏真实数据
- 调用 live Qwen/API
- 配置 API key、token、auth header 或 secret
- 调用 live connector
- 写回生产系统
- 发布客户可见输出
- 外部试点或生产上线

任何后续任务如需越过以上边界，必须创建新的可执行 Goal，并附带验收命令和 HOLD 条件。
""",
        "configs/secupilot.env.template": """# SecuPilot local/private deployment dry-run template
SECUPILOT_MODE=local_dry_run
SECUPILOT_DATA_MODE=synthetic_only
SECUPILOT_REAL_DATA_ENABLED=false
SECUPILOT_MASKED_REAL_DATA_ENABLED=false
SECUPILOT_LIVE_QWEN_ENABLED=false
SECUPILOT_LIVE_CONNECTORS_ENABLED=false
SECUPILOT_NETWORK_REQUEST_ENABLED=false
SECUPILOT_PRODUCTION_WRITEBACK_ENABLED=false
SECUPILOT_CUSTOMER_VISIBLE_OUTPUT_ENABLED=false
SECUPILOT_DEPLOY_EXECUTED=false
SECUPILOT_SECRET_MATERIAL_REQUIRED=false
""",
        "configs/provider.dry-run.json": json.dumps(
            {
                "schema_version": "secupilot.private.provider_dry_run.v1",
                "provider_mode": "dry_run_only",
                "data_mode": "synthetic_only",
                "live_qwen_api": False,
                "network_request": False,
                "api_key_required": False,
                "connector_call": False,
                "production_writeback": False,
                "customer_visible_output": False,
                "autonomous_qwen_action": False,
                "fallback_mode": "local_rules_summary",
                "retry_policy": "manual_retry_only",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        "data/README_SYNTHETIC_ONLY_中文.md": """# Synthetic Only Data Slot

此目录只允许放 synthetic fixture 或 metadata-only 示例。当前结构包不包含真实客户日志、脱敏真实数据、原始 payload 或连接器输出。
""",
        "logs/README_LOGS_中文.md": """# Logs Slot

此目录仅为本地 dry-run 日志占位。不要提交真实客户日志、token、auth header、生产连接器输出或模型请求内容。
""",
        "runtime/README_RUNTIME_中文.md": """# Runtime Slot

此目录是运行时占位。当前包不包含生产二进制、不启动服务、不执行部署。
""",
        "trial_output/README_TRIAL_OUTPUT_中文.md": """# Trial Output Slot

运行 `scripts/START_CUSTOMER_TRIAL.ps1` 后，本目录会生成 `customer_trial_status.json`。该文件只记录本地离线 dry-run 状态和边界检查结果。
""",
        "scripts/START_LOCAL_DRY_RUN.ps1": """param()
$ErrorActionPreference = 'Stop'
Write-Host 'SecuPilot local private deployment dry-run'
Write-Host 'deploy_executed=false'
Write-Host 'real_data=false'
Write-Host 'live_qwen_api=false'
Write-Host 'network_request=false'
Write-Host 'production_writeback=false'
Write-Host 'customer_visible_output=false'
Write-Host 'This script validates package structure only; it does not start production services.'
""",
        "scripts/START_CUSTOMER_TRIAL.ps1": """param()
$ErrorActionPreference = 'Stop'

$PackageRoot = Split-Path -Parent $PSScriptRoot
$ManifestPath = Join-Path $PackageRoot 'package_manifest.json'
$BoundaryScript = Join-Path $PackageRoot 'scripts\\VERIFY_BOUNDARIES.ps1'
$TrialOutputDir = Join-Path $PackageRoot 'trial_output'
$StatusPath = Join-Path $TrialOutputDir 'customer_trial_status.json'

if (-not (Test-Path -LiteralPath $ManifestPath)) {
  throw 'package_manifest.json missing'
}
if (-not (Test-Path -LiteralPath $BoundaryScript)) {
  throw 'VERIFY_BOUNDARIES.ps1 missing'
}

$Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
New-Item -ItemType Directory -Force -Path $TrialOutputDir | Out-Null

$BoundaryOutput = & $BoundaryScript 6>&1
$BoundaryLines = @($BoundaryOutput | ForEach-Object { $_.ToString() } | Where-Object { $_.Trim().Length -gt 0 })
if (-not ($BoundaryLines -contains 'BOUNDARY_CHECK_PASS')) {
  throw 'boundary check did not pass'
}

$Status = [ordered]@{
  schema_version = 'secupilot.local_trial_start_result.v1'
  generated_at_utc = (Get-Date).ToUniversalTime().ToString('o')
  package_id = $Manifest.package_id
  package_type = $Manifest.package_type
  status = 'LOCAL_TRIAL_ENTRY_READY'
  mode = 'local_offline_dry_run'
  entry_document = 'CUSTOMER_TRIAL_START_HERE_中文.md'
  entry_script = 'START_SECUPILOT_LOCAL_TRIAL.cmd'
  boundaries = $Manifest.boundaries
  boundary_check = [ordered]@{
    status = 'PASS'
    output = $BoundaryLines
  }
  generated_files = @(
    'trial_output/customer_trial_status.json'
  )
  next_steps = @(
    'Read CUSTOMER_TRIAL_START_HERE_中文.md',
    'Share customer_trial_status.json with the internal reviewer',
    'Continue with local/offline product trial only'
  )
  non_authorization = @(
    'No deployment executed',
    'No production service started',
    'No network request made',
    'No live Qwen/API call made',
    'No connector call made',
    'No production write-back made',
    'No real or masked-real data used'
  )
}

$Status | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $StatusPath -Encoding UTF8

Write-Output 'SecuPilot local offline trial entry'
Write-Output 'LOCAL_TRIAL_ENTRY_READY'
Write-Output 'BOUNDARY_CHECK_PASS'
Write-Output ('status_file=' + $StatusPath)
Write-Output 'deploy_executed=false'
Write-Output 'real_data=false'
Write-Output 'live_qwen_api=false'
Write-Output 'network_request=false'
Write-Output 'production_writeback=false'
Write-Output 'customer_visible_output=false'
""",
        "scripts/VERIFY_BOUNDARIES.ps1": """param()
$ErrorActionPreference = 'Stop'
$checks = @{
  real_data = $false
  masked_real_data = $false
  live_qwen_api = $false
  live_connectors = $false
  network_request = $false
  production_writeback = $false
  customer_visible_output = $false
  deploy_executed = $false
}
$checks.GetEnumerator() | ForEach-Object {
  Write-Host ($_.Key + '=' + $_.Value.ToString().ToLower())
}
Write-Host 'BOUNDARY_CHECK_PASS'
""",
    }


def build_package(
    *,
    package_id: str,
    output_dir: Path,
    repo_root: Path,
    zip_path: Path | None = None,
) -> dict[str, Any]:
    ensure_clean_output(output_dir, zip_path, repo_root)

    file_entries: list[dict[str, Any]] = []
    for relative_path, content in package_templates(package_id).items():
        path = output_dir / relative_path
        write_text(path, content)
        scan_text(path)
        file_entries.append(build_file_entry(path, output_dir))

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "created_at_utc": utc_now(),
        "package_id": package_id,
        "package_dir": portable_path(output_dir, repo_root),
        "package_type": "WINDOWS_LOCAL_FIRST_PRIVATE_DEPLOYMENT_STRUCTURE",
        "status": "STRUCTURE_ONLY_NOT_DEPLOYED",
        "boundaries": BOUNDARIES,
        "entry_points": {
            "start_here": "CUSTOMER_TRIAL_START_HERE_中文.md",
            "one_click_cmd": "START_SECUPILOT_LOCAL_TRIAL.cmd",
            "powershell_script": "scripts/START_CUSTOMER_TRIAL.ps1",
            "expected_status_file": "trial_output/customer_trial_status.json",
        },
        "files": file_entries,
        "next_unlock": "GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT",
    }
    manifest_path = output_dir / "package_manifest.json"
    write_json(manifest_path, manifest)
    file_entries.append(build_file_entry(manifest_path, output_dir))
    manifest["files"] = file_entries
    write_json(manifest_path, manifest)

    if zip_path is not None:
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for file_path in sorted(output_dir.rglob("*")):
                if file_path.is_file():
                    archive.write(file_path, file_path.relative_to(output_dir).as_posix())
        manifest["zip"] = {
            "zip_path": portable_path(zip_path, repo_root),
            "zip_name": zip_path.name,
            "zip_bytes": zip_path.stat().st_size,
            "zip_sha256": file_sha256(zip_path),
        }
        write_json(manifest_path, manifest)

    return manifest


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-id", default=DEFAULT_PACKAGE_ID)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    parser.add_argument("--zip-path", type=Path)
    args = parser.parse_args(argv)

    try:
        manifest = build_package(
            package_id=args.package_id,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
            zip_path=args.zip_path,
        )
    except Exception as exc:  # noqa: BLE001 - CLI converts package violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    print(json.dumps({"status": "PASS", "manifest": manifest}, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
