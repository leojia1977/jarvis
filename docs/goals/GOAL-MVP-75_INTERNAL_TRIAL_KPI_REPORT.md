# GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT

## Goal ID

```text
GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT
```

## Goal type

```text
test-report
```

## Goal statement

```text
Generate a local/offline internal trial KPI report from the private deployment package and one-click trial status artifact, covering completion status, understanding rate, feedback count, and blockers without using real data or live services.
```

## Primary executable object

```text
script=scripts/generate_internal_trial_kpi_report.py
test=backend/tests/test_generate_internal_trial_kpi_report.py
report=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report.json
report=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report_中文.md
closeout=docs/S6_FAST_MVP_MVP_75_INTERNAL_TRIAL_KPI_REPORT_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/package_manifest.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_status.json
optional local feedback JSON in the same private deployment package scope
```

## Output paths

```text
docs/goals/GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT.md
scripts/generate_internal_trial_kpi_report.py
backend/tests/test_generate_internal_trial_kpi_report.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report_中文.md
docs/S6_FAST_MVP_MVP_75_INTERNAL_TRIAL_KPI_REPORT_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT.md
scripts/generate_internal_trial_kpi_report.py
backend/tests/test_generate_internal_trial_kpi_report.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report_中文.md
docs/S6_FAST_MVP_MVP_75_INTERNAL_TRIAL_KPI_REPORT_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline report generation only
local package and trial status artifact reads
optional local feedback JSON reads
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
py -3 scripts/generate_internal_trial_kpi_report.py --package-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1 --output-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output --repo-root .
py -3 -m unittest -q backend.tests.test_generate_internal_trial_kpi_report
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
report generator performs deployment, starts production service, calls live API, sends network request, reads API key, calls connector, writes production, or pushes
trial status reports any forbidden boundary as true
package_id mismatches between manifest and trial status
generated report omits completion status, understanding rate field, feedback count, blocker count, or non-authorization boundary
generated report contains real data, masked-real data, raw payload, auth header, token, secret, customer log, or production connector output
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete generated KPI report JSON/MD for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
goal card validator output
KPI report generator output
unit test output
internal_trial_kpi_report.json
internal_trial_kpi_report_中文.md
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no network_request=true
no api_key_required=true
no live_connectors=true
no production_writeback=true
no customer_visible_output=true
no deploy_executed=true
no Authorization/Bearer/refresh_token in generated reports
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-76_CUSTOMER_TRIAL_FEEDBACK_SAMPLE_CAPTURE.
If HOLD, stop and report failing command plus blocker evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-75 internal trial KPI report
stage and commit only Goal files
do not push
```
