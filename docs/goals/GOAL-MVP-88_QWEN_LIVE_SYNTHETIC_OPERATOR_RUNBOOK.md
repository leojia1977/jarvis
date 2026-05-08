# GOAL-MVP-88_QWEN_LIVE_SYNTHETIC_OPERATOR_RUNBOOK

## Goal ID

```text
GOAL-MVP-88_QWEN_LIVE_SYNTHETIC_OPERATOR_RUNBOOK
```

## Goal type

```text
script
run-artifact
```

## Goal statement

```text
Generate an operator-facing runbook and dry command for how a human would provide runtime secret material and prepare a future Qwen live synthetic-only run, without executing any live call.
```

## Primary executable object

```text
script=scripts/generate_qwen_live_synthetic_operator_runbook.py
test=backend/tests/test_generate_qwen_live_synthetic_operator_runbook.py
artifact=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_operator_runbook_中文.md
artifact=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_dry_command.ps1
artifact=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_operator_runbook_manifest.json
closeout=docs/S6_FAST_MVP_MVP_88_QWEN_LIVE_SYNTHETIC_OPERATOR_RUNBOOK_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_request.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report.json
docs/S6_FAST_MVP_MVP_87_QWEN_LIVE_SYNTHETIC_GO_PRECHECK_CLOSEOUT_2026_05_08.md
```

## Output paths

```text
docs/goals/GOAL-MVP-88_QWEN_LIVE_SYNTHETIC_OPERATOR_RUNBOOK.md
scripts/generate_qwen_live_synthetic_operator_runbook.py
backend/tests/test_generate_qwen_live_synthetic_operator_runbook.py
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_operator_runbook_中文.md
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_dry_command.ps1
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_operator_runbook_manifest.json
docs/S6_FAST_MVP_MVP_88_QWEN_LIVE_SYNTHETIC_OPERATOR_RUNBOOK_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-88_QWEN_LIVE_SYNTHETIC_OPERATOR_RUNBOOK.md
scripts/generate_qwen_live_synthetic_operator_runbook.py
backend/tests/test_generate_qwen_live_synthetic_operator_runbook.py
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_operator_runbook_中文.md
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_dry_command.ps1
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_operator_runbook_manifest.json
docs/S6_FAST_MVP_MVP_88_QWEN_LIVE_SYNTHETIC_OPERATOR_RUNBOOK_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline operator runbook generation only
dry command generation only
MVP-87 request and precheck report reads
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
py -3 scripts/generate_qwen_live_synthetic_operator_runbook.py --request artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_request.json --precheck-report artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report.json --output-dir artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001 --repo-root .
py -3 -m unittest -q backend.tests.test_generate_qwen_live_synthetic_operator_runbook
powershell.exe -NoProfile -ExecutionPolicy Bypass -File artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_dry_command.ps1
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-88_QWEN_LIVE_SYNTHETIC_OPERATOR_RUNBOOK.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
MVP-87 precheck report is not READY_FOR_QWEN_LIVE_SYNTHETIC_GO_REVIEW_NOT_EXECUTION
GO request authorizes live call or does not require separate human GO
GO request data_mode is not SYNTHETIC_ONLY
GO request contains secret value or enables provider by default
runbook asks operator to write secret into repo, scripts, Markdown, JSON, logs, artifacts, command history, or chat
dry command reads, prints, stores, validates, or transmits secret value
dry command invokes network, Qwen/API, connector, live runner, production write-back, or customer-visible output
dry command output is not DRY_COMMAND_ONLY_NO_LIVE_CALL and NOT_EXECUTED
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete generated operator runbook, dry command, and manifest for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
goal card validator output
operator runbook Markdown
dry PowerShell command artifact and output
operator runbook manifest JSON
unit test output
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no live_qwen_api_call=true
no network_call=true
no live_connectors=true
no production_writeback=true
no customer_visible_output=true
no autonomous_qwen_action=true
no Invoke-RestMethod
no curl
no live runner execution
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
If PASS, unlock GOAL-MVP-89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR or a customer-trial product Goal.
If HOLD, stop and report the failing runbook or dry command item.
This Goal does not unlock live execution by itself.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-88 qwen live synthetic operator runbook
stage and commit only Goal files
do not push
```
