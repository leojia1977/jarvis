# GOAL-MVP-87_QWEN_LIVE_SYNTHETIC_GO_PRECHECK

## Goal ID

```text
GOAL-MVP-87_QWEN_LIVE_SYNTHETIC_GO_PRECHECK
```

## Goal type

```text
validator
run-artifact
```

## Goal statement

```text
Create a runnable precheck package for a future Qwen live synthetic-only GO, including run ID, operator, artifact root, timeout, retry, runtime secret source, stop conditions, and rollback plan, without executing any live call.
```

## Primary executable object

```text
script=scripts/validate_qwen_live_synthetic_go_precheck.py
test=backend/tests/test_validate_qwen_live_synthetic_go_precheck.py
artifact=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_request.json
report=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report.json
report=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report_中文.md
closeout=docs/S6_FAST_MVP_MVP_87_QWEN_LIVE_SYNTHETIC_GO_PRECHECK_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
docs/S6_FAST_MVP_QWEN_CLOUD_ADAPTER_SPEC_2026_05_06.md
docs/S6_FAST_MVP_MVP_86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE_CLOSEOUT_2026_05_08.md
artifacts/product_readiness/customer_trial_success_qwen_live_gate/customer_trial_success_qwen_live_gate_report.json
mock_data/s0_synthetic/qwen_fact_bundle
```

## Output paths

```text
docs/goals/GOAL-MVP-87_QWEN_LIVE_SYNTHETIC_GO_PRECHECK.md
scripts/validate_qwen_live_synthetic_go_precheck.py
backend/tests/test_validate_qwen_live_synthetic_go_precheck.py
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_request.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report_中文.md
docs/S6_FAST_MVP_MVP_87_QWEN_LIVE_SYNTHETIC_GO_PRECHECK_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-87_QWEN_LIVE_SYNTHETIC_GO_PRECHECK.md
scripts/validate_qwen_live_synthetic_go_precheck.py
backend/tests/test_validate_qwen_live_synthetic_go_precheck.py
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_request.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report_中文.md
docs/S6_FAST_MVP_MVP_87_QWEN_LIVE_SYNTHETIC_GO_PRECHECK_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline GO precheck only
synthetic-only Qwen live preparation artifact
local JSON/Markdown report generation
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
py -3 scripts/validate_qwen_live_synthetic_go_precheck.py --request artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_request.json --output-dir artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001 --repo-root .
py -3 -m unittest -q backend.tests.test_validate_qwen_live_synthetic_go_precheck
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-87_QWEN_LIVE_SYNTHETIC_GO_PRECHECK.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
GO request authorizes live call inside the precheck package
GO request does not require separate human GO
data_mode is not SYNTHETIC_ONLY
run_id is missing or not scoped to QWEN-LIVE-SYNTHETIC
operator alias is missing or human confirmation is not required
artifact_root is absolute, outside repo, contains parent traversal, or is not under artifacts/qwen_live_synthetic_runs
provider flag defaults to enabled
secret source is not human_runtime_or_secret_manager_only
secret value is present in repo, command, log, artifact, or chat
timeout is missing or greater than 60 seconds
retry count is missing or greater than 2
cost/token budget is missing
real data, masked-real data, raw payload, raw log, customer-visible output, production write-back, live connector, or autonomous Qwen action is allowed
stop conditions or rollback plan are incomplete
script performs a network call, reads API keys, calls live Qwen/API/connectors, writes production, or pushes
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete generated Qwen live GO precheck report files for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
goal card validator output
Qwen live synthetic-only GO request JSON
Qwen live synthetic-only GO precheck report JSON
Qwen live synthetic-only GO precheck report Markdown
unit test output
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no live_call_authorized=true
no real_data=true
no masked_real_data=true
no raw_payload_allowed=true
no raw_log_allowed=true
no live_connectors=true
no production_writeback=true
no customer_visible_output=true
no autonomous_qwen_action=true
no network_call=true
no live_qwen_api_call=true
no Authorization/Bearer/access_token/refresh_token/private_key/raw_payload/raw_evidence in generated reports
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-88_QWEN_LIVE_SYNTHETIC_OPERATOR_RUNBOOK or the next model-provider setup Goal.
If HOLD, stop and report the failing precheck item.
This Goal does not unlock live execution by itself.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-87 qwen live synthetic go precheck
stage and commit only Goal files
do not push
```
