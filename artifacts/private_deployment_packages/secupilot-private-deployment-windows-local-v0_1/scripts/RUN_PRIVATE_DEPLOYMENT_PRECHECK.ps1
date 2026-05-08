param(
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
