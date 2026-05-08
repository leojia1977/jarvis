param()
$ErrorActionPreference = 'Stop'

$PackageRoot = Split-Path -Parent $PSScriptRoot
$ManifestPath = Join-Path $PackageRoot 'package_manifest.json'
$BoundaryScript = Join-Path $PackageRoot 'scripts\VERIFY_BOUNDARIES.ps1'
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
