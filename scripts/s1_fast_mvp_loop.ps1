[CmdletBinding()]
param(
    [ValidateSet("verify", "baseline", "mvp-03", "mvp-05", "mvp-06", "mvp-07", "mvp-08", "mvp-09", "queue")]
    [string]$Mode = "verify",

    [string]$RepoRoot = "",

    [switch]$WriteStatus
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $scriptRoot = $PSScriptRoot
    if ([string]::IsNullOrWhiteSpace($scriptRoot)) {
        $scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    }
    $RepoRoot = (Resolve-Path -LiteralPath (Join-Path $scriptRoot "..")).Path
}
else {
    $RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
}

$StatusRoot = Join-Path $RepoRoot "artifacts\automation\fast_mvp_queue"
$S1RunArtifactDir = "artifacts\s1_closed_shadow_runs\2026-04-30-001"
$ExternalOutputArtifactDir = "artifacts\s1_closed_shadow_runs\2026-04-30-001-external-output"
$LocalDemoPackageDir = "artifacts\local_demo_packages\s1-closed-shadow-2026-04-30-001"

function Convert-ToJsonText {
    param([Parameter(Mandatory = $true)] [object]$Value)
    return ($Value | ConvertTo-Json -Depth 8)
}

function Write-QueueStatus {
    param(
        [Parameter(Mandatory = $true)] [string]$Status,
        [Parameter(Mandatory = $true)] [string]$Item,
        [Parameter(Mandatory = $true)] [string]$Detail
    )

    $payload = [ordered]@{
        schema_version = "secupilot.fast_mvp_queue.status.v1"
        generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        status = $Status
        item = $Item
        detail = $Detail
        mode = $Mode
    }

    Write-Output ("[{0}] {1}: {2}" -f $Status, $Item, $Detail)

    if ($WriteStatus) {
        New-Item -ItemType Directory -Force -Path $StatusRoot | Out-Null
        Convert-ToJsonText -Value $payload | Set-Content -LiteralPath (Join-Path $StatusRoot "last_status.json") -Encoding UTF8
    }
}

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory = $true)] [string]$Label,
        [Parameter(Mandatory = $true)] [string]$FilePath,
        [string[]]$Arguments = @(),
        [string]$WorkingDirectory = $RepoRoot,
        [int[]]$AllowedExitCodes = @(0)
    )

    Write-Output ("[RUN] {0}" -f $Label)
    Write-Output ("[CWD] {0}" -f $WorkingDirectory)
    Push-Location -LiteralPath $WorkingDirectory
    try {
        $global:LASTEXITCODE = 0
        & $FilePath @Arguments
        $exitCode = $LASTEXITCODE
        if ($null -eq $exitCode) {
            $exitCode = 0
        }
    }
    finally {
        Pop-Location
    }

    if ($AllowedExitCodes -notcontains $exitCode) {
        throw ("{0} exited with {1}; allowed exit codes: {2}" -f $Label, $exitCode, ($AllowedExitCodes -join ","))
    }
}

function Require-RepoPath {
    param(
        [Parameter(Mandatory = $true)] [string]$RelativePath,
        [Parameter(Mandatory = $true)] [string]$HoldCode
    )

    $path = Join-Path $RepoRoot $RelativePath
    if (-not (Test-Path -LiteralPath $path)) {
        throw ("{0}: missing {1}" -f $HoldCode, $RelativePath)
    }
}

function Invoke-Baseline {
    Invoke-CheckedCommand -Label "git status" -FilePath "git" -Arguments @("-c", "core.quotepath=false", "status", "--short", "--branch")
    Invoke-CheckedCommand -Label "fast preflight" -FilePath "py" -Arguments @("-3", "scripts\git_preflight.py", "--mode", "fast")
}

function Invoke-Mvp03 {
    $frontendRoot = Join-Path $RepoRoot "frontend"
    Invoke-CheckedCommand -Label "frontend App test" -FilePath "npm.cmd" -Arguments @("run", "test", "--", "--run", "App.test.tsx") -WorkingDirectory $frontendRoot
    Invoke-CheckedCommand -Label "frontend build" -FilePath "npm.cmd" -Arguments @("run", "build") -WorkingDirectory $frontendRoot
    Invoke-Baseline
}

function Invoke-Mvp05 {
    Require-RepoPath -RelativePath "frontend\tests\e2e\s1-artifact-viewer.spec.ts" -HoldCode "HOLD_MVP_05_PLAYWRIGHT_SPEC_MISSING"
    $frontendRoot = Join-Path $RepoRoot "frontend"
    Invoke-CheckedCommand -Label "S1 Playwright smoke" -FilePath "npm.cmd" -Arguments @("run", "test:e2e", "--", "tests/e2e/s1-artifact-viewer.spec.ts") -WorkingDirectory $frontendRoot
    Invoke-CheckedCommand -Label "frontend build" -FilePath "npm.cmd" -Arguments @("run", "build") -WorkingDirectory $frontendRoot
}

function Invoke-Mvp06 {
    Require-RepoPath -RelativePath "scripts\s1_artifact_validate.py" -HoldCode "HOLD_MVP_06_VALIDATOR_SCRIPT_MISSING"
    Require-RepoPath -RelativePath "backend\tests\test_s1_artifact_validate.py" -HoldCode "HOLD_MVP_06_VALIDATOR_TEST_MISSING"
    Invoke-CheckedCommand -Label "S1 artifact validator tests" -FilePath "py" -Arguments @("-3", "-m", "unittest", "-q", "backend.tests.test_s1_artifact_validate")
    Invoke-CheckedCommand -Label "S1 artifact validator" -FilePath "py" -Arguments @("-3", "scripts\s1_artifact_validate.py", "--artifact-dir", $S1RunArtifactDir)
}

function Invoke-Mvp07 {
    Require-RepoPath -RelativePath "mock_data\s1_closed_shadow_fixture\external_provider_output.example.json" -HoldCode "HOLD_MVP_07_EXTERNAL_OUTPUT_FIXTURE_MISSING"
    Invoke-CheckedCommand -Label "S1 external-output provider run" -FilePath "py" -Arguments @(
        "-3",
        "scripts\s1_closed_shadow_run.py",
        "--run-id",
        "S1-CLOSED-SHADOW-2026-04-30-001-EXTERNAL-OUTPUT",
        "--input",
        "mock_data\s0_synthetic\qwen_fact_bundle",
        "--output",
        $ExternalOutputArtifactDir,
        "--provider",
        "external-output",
        "--provider-output-file",
        "mock_data\s1_closed_shadow_fixture\external_provider_output.example.json",
        "--no-writeback",
        "--no-customer-visible"
    ) -AllowedExitCodes @(0, 10)
    Invoke-CheckedCommand -Label "S1 runner tests" -FilePath "py" -Arguments @("-3", "-m", "unittest", "-q", "backend.tests.test_s1_closed_shadow_run")
}

function Invoke-Mvp08 {
    Require-RepoPath -RelativePath "scripts\package_s1_local_demo.py" -HoldCode "HOLD_MVP_08_PACKAGE_SCRIPT_MISSING"
    Require-RepoPath -RelativePath "backend\tests\test_package_s1_local_demo.py" -HoldCode "HOLD_MVP_08_PACKAGE_TEST_MISSING"
    Invoke-CheckedCommand -Label "S1 local demo package tests" -FilePath "py" -Arguments @("-3", "-m", "unittest", "-q", "backend.tests.test_package_s1_local_demo")
    Invoke-CheckedCommand -Label "S1 local demo package" -FilePath "py" -Arguments @(
        "-3",
        "scripts\package_s1_local_demo.py",
        "--artifact-dir",
        $S1RunArtifactDir,
        "--output-dir",
        $LocalDemoPackageDir
    )
}

function Invoke-Mvp09 {
    $claude = Get-Command "claude" -ErrorAction SilentlyContinue
    if (-not $claude) {
        $claude = Get-Command "claude.cmd" -ErrorAction SilentlyContinue
    }
    if (-not $claude) {
        throw "HOLD_EXTERNAL_REVIEW_COMMAND_UNAVAILABLE: claude command not found"
    }

    $reviewRoot = Join-Path $RepoRoot "artifacts\reviews\claude_code"
    New-Item -ItemType Directory -Force -Path $reviewRoot | Out-Null
    $reviewPath = Join-Path $reviewRoot ("mvp-09-current-diff-review-{0}.txt" -f (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ"))
    $prompt = "Review only the current git diff for the SecuPilot Fast MVP queue item. Check correctness, unsafe data handling, secret/token/raw payload retention, production write-back, customer-visible output, tests, and overengineering. Do not edit files. Return findings ordered by severity, or say no findings."

    Push-Location -LiteralPath $RepoRoot
    try {
        & $claude.Source --print $prompt | Tee-Object -FilePath $reviewPath
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    if ($exitCode -ne 0) {
        throw ("Claude review exited with {0}" -f $exitCode)
    }
}

function Invoke-Mode {
    switch ($Mode) {
        "verify" {
            Require-RepoPath -RelativePath ".vscode\tasks.json" -HoldCode "HOLD_MVP_04_TASKS_JSON_MISSING"
            Require-RepoPath -RelativePath "scripts\s1_fast_mvp_loop.ps1" -HoldCode "HOLD_MVP_04_LOOP_SCRIPT_MISSING"
            Require-RepoPath -RelativePath "docs\S6_FAST_MVP_5_DAY_AUTOMATION_QUEUE_2026_04_30.md" -HoldCode "HOLD_MVP_04_QUEUE_DOC_MISSING"
            Get-Content -LiteralPath (Join-Path $RepoRoot ".vscode\tasks.json") -Raw | ConvertFrom-Json | Out-Null
            Invoke-Mvp03
        }
        "baseline" { Invoke-Baseline }
        "mvp-03" { Invoke-Mvp03 }
        "mvp-05" { Invoke-Mvp05 }
        "mvp-06" { Invoke-Mvp06 }
        "mvp-07" { Invoke-Mvp07 }
        "mvp-08" { Invoke-Mvp08 }
        "mvp-09" { Invoke-Mvp09 }
        "queue" {
            Invoke-Mvp05
            Invoke-Mvp06
            Invoke-Mvp07
            Invoke-Mvp08
            Invoke-Mvp09
        }
    }
}

try {
    Invoke-Mode
    Write-QueueStatus -Status "PASS" -Item $Mode -Detail "Completed requested Fast MVP queue command."
}
catch {
    Write-QueueStatus -Status "HOLD" -Item $Mode -Detail $_.Exception.Message
    exit 20
}
