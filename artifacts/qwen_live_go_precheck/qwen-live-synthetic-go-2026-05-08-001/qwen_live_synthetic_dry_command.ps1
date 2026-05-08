# SecuPilot Qwen live synthetic-only dry command.
# This script is intentionally non-executing. It prints a future run plan only.

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$plan = [ordered]@{
  mode = 'DRY_COMMAND_ONLY_NO_LIVE_CALL'
  run_id = 'QWEN-LIVE-SYNTHETIC-2026-05-08-001'
  request_id = 'QWEN-LIVE-SYNTHETIC-GO-2026-05-08-001'
  operator_alias = 'SecuPilot-QWEN-RUNNER-01'
  data_mode = 'SYNTHETIC_ONLY'
  input_package = 'mock_data/s0_synthetic/qwen_fact_bundle'
  artifact_root = 'artifacts/qwen_live_synthetic_runs/2026-05-08-001'
  provider_flag_default = $false
  timeout_seconds = 30
  max_retries = 1
  max_requests = 20
  max_tokens_per_case = 1200
  runtime_secret_env_var_names = 'SECUPILOT_QWEN_API_KEY'
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
}

$plan | ConvertTo-Json -Depth 5
exit 0
