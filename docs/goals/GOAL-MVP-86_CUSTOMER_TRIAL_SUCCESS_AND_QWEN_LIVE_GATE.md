# GOAL-MVP-86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE

## Goal ID

```text
GOAL-MVP-86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE
```

## Goal type

```text
validator
test-report
```

## Goal statement

```text
Turn customer trial success criteria and the Qwen live integration gate into a runnable local validator and readiness report, so SecuPilot can decide whether it is ready for local private trial and what still blocks live Qwen.
```

## Primary executable object

```text
script=scripts/validate_customer_trial_success_and_qwen_live_gate.py
test=backend/tests/test_validate_customer_trial_success_and_qwen_live_gate.py
report=artifacts/product_readiness/customer_trial_success_qwen_live_gate/customer_trial_success_qwen_live_gate_report.json
report=artifacts/product_readiness/customer_trial_success_qwen_live_gate/customer_trial_success_qwen_live_gate_report_中文.md
closeout=docs/S6_FAST_MVP_MVP_86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_status.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_feedback.sample.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_precheck_result.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report.json
docs/S6_FAST_MVP_QWEN_CLOUD_ADAPTER_SPEC_2026_05_06.md
```

## Output paths

```text
docs/goals/GOAL-MVP-86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE.md
scripts/validate_customer_trial_success_and_qwen_live_gate.py
backend/tests/test_validate_customer_trial_success_and_qwen_live_gate.py
artifacts/product_readiness/customer_trial_success_qwen_live_gate/customer_trial_success_qwen_live_gate_report.json
artifacts/product_readiness/customer_trial_success_qwen_live_gate/customer_trial_success_qwen_live_gate_report_中文.md
docs/S6_FAST_MVP_MVP_86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE.md
scripts/validate_customer_trial_success_and_qwen_live_gate.py
backend/tests/test_validate_customer_trial_success_and_qwen_live_gate.py
artifacts/product_readiness/customer_trial_success_qwen_live_gate/customer_trial_success_qwen_live_gate_report.json
artifacts/product_readiness/customer_trial_success_qwen_live_gate/customer_trial_success_qwen_live_gate_report_中文.md
docs/S6_FAST_MVP_MVP_86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline readiness validation only
local private deployment package artifact reads
Qwen dry/live contract document reads
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
py -3 scripts/validate_customer_trial_success_and_qwen_live_gate.py --package-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1 --qwen-spec docs/S6_FAST_MVP_QWEN_CLOUD_ADAPTER_SPEC_2026_05_06.md --output-dir artifacts/product_readiness/customer_trial_success_qwen_live_gate --repo-root .
py -3 -m unittest -q backend.tests.test_validate_customer_trial_success_and_qwen_live_gate
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
customer trial status is not LOCAL_TRIAL_ENTRY_READY
customer trial feedback does not cover security engineer, security manager, and CTO roles
understanding rate is below 80 percent
usefulness rate is below 60 percent
KPI report contains blockers
private deployment precheck is not PRIVATE_DEPLOYMENT_PRECHECK_PASS
sizing report claims production benchmark, customer pilot sizing, or deployment readiness
real_data, masked_real_data, live_qwen_api, live_connectors, network_request, production_writeback, customer_visible_output, or deploy_executed is true
Qwen spec does not define synthetic-only scope, explicit GO, no-current-live authorization, forbidden fields, timeout, and retry guard
script performs a network call, reads API keys, calls live Qwen/API/connectors, writes production, or pushes
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete generated product_readiness reports for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
goal card validator output
customer trial success and Qwen live gate report JSON
customer trial success and Qwen live gate report Markdown
unit test output
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no network_request=true
no live_connectors=true
no production_writeback=true
no customer_visible_output=true
no deploy_executed=true
no Authorization/Bearer/refresh_token/access_token/api_key/private_key/cookie/raw_payload/raw_evidence in generated reports
Qwen live status must remain HOLD unless a separate synthetic-only live GO record exists
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-80_MODEL_PROVIDER_SETUP_FLOW_DRY_RUN or the next active model-provider setup Goal.
If HOLD_FOR_CUSTOMER_TRIAL_CRITERIA, fix local private trial artifacts before live model work.
If HOLD_PENDING_EXPLICIT_QWEN_LIVE_SYNTHETIC_ONLY_GO, continue dry-run setup and prepare a separate Qwen live synthetic-only GO record.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-86 customer trial qwen live gate
stage and commit only Goal files
do not push
```
