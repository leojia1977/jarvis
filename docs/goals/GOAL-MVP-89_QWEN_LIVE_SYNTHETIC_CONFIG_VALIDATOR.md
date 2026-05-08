# GOAL-MVP-89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR

## Goal ID

```text
GOAL-MVP-89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR
```

## Goal type

```text
validator
run-artifact
```

## Goal statement

```text
Validate the local runtime configuration contract for a future Qwen live synthetic-only run, including provider flag, timeout, retry, model name, base URL, and runtime secret env names, without retaining env values or executing any live call.
```

## Primary executable object

```text
script=scripts/validate_qwen_live_synthetic_runtime_config.py
test=backend/tests/test_validate_qwen_live_synthetic_runtime_config.py
report=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json
report=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report_中文.md
closeout=docs/S6_FAST_MVP_MVP_89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_request.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_operator_runbook_manifest.json
docs/S6_FAST_MVP_MVP_88_QWEN_LIVE_SYNTHETIC_OPERATOR_RUNBOOK_CLOSEOUT_2026_05_08.md
```

## Output paths

```text
docs/goals/GOAL-MVP-89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR.md
scripts/validate_qwen_live_synthetic_runtime_config.py
backend/tests/test_validate_qwen_live_synthetic_runtime_config.py
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report_中文.md
docs/S6_FAST_MVP_MVP_89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR.md
scripts/validate_qwen_live_synthetic_runtime_config.py
backend/tests/test_validate_qwen_live_synthetic_runtime_config.py
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report_中文.md
docs/S6_FAST_MVP_MVP_89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline runtime config validation only
policy-mode validation for repo artifacts
process-mode validation for future operator local env checks
local unit tests
docs-only closeout evidence for this Goal
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
API keys
secrets/tokens/auth headers/raw customer logs
live connectors
production write-back
customer-visible publish/deploy/output
external pilot
production launch
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/validate_qwen_live_synthetic_runtime_config.py --request artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_request.json --output-dir artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001 --repo-root . --mode policy
py -3 -m unittest -q backend.tests.test_validate_qwen_live_synthetic_runtime_config
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
GO request authorizes live call or does not require separate human GO
GO request data_mode is not SYNTHETIC_ONLY
GO request contains secret value or enables provider by default
runtime policy omits provider enabled, synthetic-only, API base, model, timeout, retry, or API key env name
process mode records actual API base, model, or secret value in generated report
process mode reads, prints, stores, validates, or transmits secret value
process mode accepts non-HTTPS base URL or URL with credentials
process mode accepts provider enabled value other than true
process mode accepts timeout or retry values above the GO request bounds
script performs network request, live Qwen/API call, connector call, production write-back, or customer-visible output
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete generated runtime config report files for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
goal card validator output
runtime config policy report JSON
runtime config policy report Markdown
unit test output covering process-mode env validation without value retention
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no live_qwen_api_call=true
no network_call=true
no env_values_retained=true
no secret_values_read=true
no secret_values_retained=true
no actual API base or model value retained in process-mode reports
no Authorization/Bearer/access_token/refresh_token/private_key/raw_payload/raw_evidence in generated artifacts
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB or a customer-trial product Goal.
If HOLD, stop and report the failing runtime config item.
This Goal does not unlock live execution by itself.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-89 qwen live synthetic config validator
stage and commit only Goal files
do not push
```
