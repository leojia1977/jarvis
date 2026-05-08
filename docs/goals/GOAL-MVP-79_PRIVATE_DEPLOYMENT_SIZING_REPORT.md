# GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT

## Goal ID

```text
GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT
```

## Goal type

```text
test-report
```

## Goal statement

```text
Turn the MVP-77 sizing draft and MVP-78 precheck result into a local/offline private deployment sizing report with assumptions, benchmark placeholders, and explicit non-production caveats.
```

## Primary executable object

```text
script=scripts/generate_private_deployment_sizing_report.py
test=backend/tests/test_generate_private_deployment_sizing_report.py
report=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report.json
report=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report_中文.md
closeout=docs/S6_FAST_MVP_MVP_79_PRIVATE_DEPLOYMENT_SIZING_REPORT_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_precheck_result.json
```

## Output paths

```text
docs/goals/GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT.md
scripts/generate_private_deployment_sizing_report.py
backend/tests/test_generate_private_deployment_sizing_report.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report_中文.md
docs/S6_FAST_MVP_MVP_79_PRIVATE_DEPLOYMENT_SIZING_REPORT_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT.md
scripts/generate_private_deployment_sizing_report.py
backend/tests/test_generate_private_deployment_sizing_report.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report_中文.md
docs/S6_FAST_MVP_MVP_79_PRIVATE_DEPLOYMENT_SIZING_REPORT_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline sizing report generation only
local prereq/sizing draft reads
local precheck result reads
local JSON/Markdown output
local tests
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
py -3 scripts/generate_private_deployment_sizing_report.py --package-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1 --draft-json artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft.json --precheck-json artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_precheck_result.json --output-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output --repo-root .
py -3 -m unittest -q backend.tests.test_generate_private_deployment_sizing_report
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
sizing report generator performs deployment, starts production service, calls live API, sends network request, reads API key, calls connector, writes production, or pushes
precheck result is not PRIVATE_DEPLOYMENT_PRECHECK_PASS
precheck result reports deploy_executed, network_request, live_qwen_api, live_connectors, production_writeback, customer_visible_output, real_data, or masked_real_data as true
sizing source status is not DRAFT_NOT_BENCHMARKED
generated report claims production benchmark, customer pilot sizing, deployment readiness, or live Qwen/API readiness
generated report omits assumptions, non-production caveats, sizing profiles, observed precheck, or non-authorization boundary
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete generated sizing report JSON/MD for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
goal card validator output
sizing report generator output
unit test output
private_deployment_sizing_report.json
private_deployment_sizing_report_中文.md
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
no production benchmark claim
no Authorization/Bearer/refresh_token in generated report
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-80_MODEL_PROVIDER_SETUP_FLOW_DRY_RUN.
If HOLD, stop and report failing command plus blocker evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-79 private deployment sizing report
stage and commit only Goal files
do not push
```
