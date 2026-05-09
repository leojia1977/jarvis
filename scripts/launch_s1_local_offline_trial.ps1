[CmdletBinding()]
param(
    [string]$PackageDir = "artifacts\local_demo_packages\local-offline-trial-rc-019-cn-review",
    [string]$DeliveryDir = "artifacts\local_trial_packages\local-offline-trial-rc-006",
    [string]$Route = "/s1-trial",
    [int]$Port = 4174,
    [switch]$SkipBuild,
    [switch]$NoServer,
    [switch]$OpenBrowser,
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

function Resolve-RepoPath {
    param([string]$PathValue)

    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return (Resolve-Path -LiteralPath $PathValue).Path
    }

    return (Resolve-Path -LiteralPath (Join-Path -Path $RepoRoot -ChildPath $PathValue)).Path
}

$RepoRoot = (Resolve-Path -LiteralPath (Join-Path -Path $PSScriptRoot -ChildPath "..")).Path
$PackageRoot = Resolve-RepoPath -PathValue $PackageDir
$DeliveryRoot = Resolve-RepoPath -PathValue $DeliveryDir
$FrontendRoot = Resolve-RepoPath -PathValue "frontend"
$LaunchRoot = Join-Path -Path $RepoRoot -ChildPath "artifacts\local_trial_launches\local-offline-trial-rc-019"
$LaunchInfoPath = Join-Path -Path $LaunchRoot -ChildPath "launch_info.json"
$LocalUrl = "http://127.0.0.1:$Port$Route"

$RequiredFiles = @(
    "REVIEWER_START_HERE_中文.md",
    "REVIEWER_CHECKLIST_中文.md",
    "FEEDBACK_TEMPLATE_中文.md",
    "PACKAGE_INDEX_中文.json",
    "SCREENSHOT_INDEX.json",
    "package_manifest.json",
    "evidence\final_status.json",
    "evidence\case_summary.json",
    "evidence\artifact_manifest.json",
    "evidence\safety_scan.json",
    "screenshots\s1-run-desktop.png",
    "screenshots\s1-run-mobile.png",
    "screenshots\s1-trial-desktop.png",
    "screenshots\s1-trial-mobile.png"
)

$RequiredDeliveryFiles = @(
    "START_HERE.md",
    "REVIEWER_CHECKLIST.md",
    "FEEDBACK_TEMPLATE.md",
    "PACKAGE_INDEX.json"
)

$MissingFiles = @()
foreach ($RelativePath in $RequiredFiles) {
    $Candidate = Join-Path -Path $PackageRoot -ChildPath $RelativePath
    if (-not (Test-Path -LiteralPath $Candidate -PathType Leaf)) {
        $MissingFiles += $RelativePath
    }
}

if ($MissingFiles.Count -gt 0) {
    throw "S1 local offline trial package is incomplete. Missing: $($MissingFiles -join ', ')"
}

$MissingDeliveryFiles = @()
foreach ($RelativePath in $RequiredDeliveryFiles) {
    $Candidate = Join-Path -Path $DeliveryRoot -ChildPath $RelativePath
    if (-not (Test-Path -LiteralPath $Candidate -PathType Leaf)) {
        $MissingDeliveryFiles += $RelativePath
    }
}

if ($MissingDeliveryFiles.Count -gt 0) {
    throw "S1 local offline delivery package is incomplete. Missing: $($MissingDeliveryFiles -join ', ')"
}

$FinalStatusPath = Join-Path -Path $PackageRoot -ChildPath "evidence\final_status.json"
$SafetyScanPath = Join-Path -Path $PackageRoot -ChildPath "evidence\safety_scan.json"
$FinalStatus = Get-Content -LiteralPath $FinalStatusPath -Raw | ConvertFrom-Json
$SafetyScan = Get-Content -LiteralPath $SafetyScanPath -Raw | ConvertFrom-Json

$BoundaryFailures = @()
if ($FinalStatus.can_deploy_to_customer_production -ne $false) {
    $BoundaryFailures += "can_deploy_to_customer_production"
}
if ($FinalStatus.boundaries_preserved.customer_visible_output -ne $false) {
    $BoundaryFailures += "customer_visible_output"
}
if ($FinalStatus.boundaries_preserved.production_connectors -ne $false) {
    $BoundaryFailures += "production_connectors"
}
if ($FinalStatus.boundaries_preserved.qwen_autonomous_action -ne $false) {
    $BoundaryFailures += "qwen_autonomous_action"
}
if ($FinalStatus.boundaries_preserved.raw_payload_retention -ne $false) {
    $BoundaryFailures += "raw_payload_retention"
}
if ($FinalStatus.boundaries_preserved.secret_retention -ne $false) {
    $BoundaryFailures += "secret_retention"
}
if ($FinalStatus.boundaries_preserved.writeback -ne $false) {
    $BoundaryFailures += "writeback"
}
if ($SafetyScan.summary.finding_count -ne 0) {
    $BoundaryFailures += "safety_scan_finding_count"
}
if ($SafetyScan.summary.no_go_count -ne 0) {
    $BoundaryFailures += "safety_scan_no_go_count"
}

if ($BoundaryFailures.Count -gt 0) {
    throw "S1 local offline trial boundary check failed: $($BoundaryFailures -join ', ')"
}

if ((-not $SkipBuild) -and (-not $CheckOnly)) {
    Push-Location -LiteralPath $FrontendRoot
    try {
        npm run build
    } finally {
        Pop-Location
    }
}

$ServerStarted = $false
if ((-not $NoServer) -and (-not $CheckOnly)) {
    $EscapedFrontend = $FrontendRoot.Replace("'", "''")
    $PreviewCommand = "Set-Location -LiteralPath '$EscapedFrontend'; npm exec -- vite preview --host 127.0.0.1 --port $Port"
    Start-Process -FilePath "powershell.exe" -ArgumentList @(
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        $PreviewCommand
    ) -WindowStyle Hidden
    $ServerStarted = $true
}

if ($OpenBrowser -and (-not $CheckOnly)) {
    Start-Process $LocalUrl
}

$LaunchInfo = [ordered]@{
    schema_version = "secupilot.s1.local_offline_trial_launcher.v1"
    generated_at_utc = (Get-Date).ToUniversalTime().ToString("o")
    candidate = "LOCAL_OFFLINE_TRIAL_RC_019_CN"
    route = $Route
    local_url = $LocalUrl
    package_dir = $PackageDir
    delivery_package_dir = $DeliveryDir
    reviewer_start_here = (Join-Path -Path $PackageDir -ChildPath "REVIEWER_START_HERE_中文.md")
    reviewer_checklist_cn = (Join-Path -Path $PackageDir -ChildPath "REVIEWER_CHECKLIST_中文.md")
    reviewer_feedback_cn = (Join-Path -Path $PackageDir -ChildPath "FEEDBACK_TEMPLATE_中文.md")
    start_here = (Join-Path -Path $DeliveryDir -ChildPath "START_HERE.md")
    reviewer_checklist = (Join-Path -Path $DeliveryDir -ChildPath "REVIEWER_CHECKLIST.md")
    feedback_template = (Join-Path -Path $DeliveryDir -ChildPath "FEEDBACK_TEMPLATE.md")
    launcher_output_path = "artifacts\local_trial_launches\local-offline-trial-rc-019\launch_info.json"
    server_started = $ServerStarted
    build_skipped = [bool]$SkipBuild
    check_only = [bool]$CheckOnly
    operator_notice = "Local/offline private-preview shell only. Do not publish, deploy, or write back."
    stop_instructions = @(
        "STOP if any boundary flag is true.",
        "STOP if package evidence files are missing.",
        "STOP if any command attempts live API/connectors."
    )
    boundaries = [ordered]@{
        real_data = $false
        masked_real_data = $false
        live_qwen_api = $false
        live_connectors = $false
        production_writeback = $false
        customer_visible_output = $false
        push = $false
    }
    required_files = $RequiredFiles
    required_delivery_files = $RequiredDeliveryFiles
}

if (-not $CheckOnly) {
    New-Item -ItemType Directory -Path $LaunchRoot -Force | Out-Null
    $LaunchInfo | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $LaunchInfoPath -Encoding UTF8
}

$LaunchInfo | ConvertTo-Json -Depth 8
