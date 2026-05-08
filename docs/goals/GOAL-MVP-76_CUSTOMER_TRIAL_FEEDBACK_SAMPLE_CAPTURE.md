# GOAL-MVP-76_CUSTOMER_TRIAL_FEEDBACK_SAMPLE_CAPTURE

## Goal ID

```text
GOAL-MVP-76_CUSTOMER_TRIAL_FEEDBACK_SAMPLE_CAPTURE
```

## Goal type

```text
run-artifact
```

## Goal statement

```text
Create a local/offline customer trial feedback sample format and capture command so the internal trial KPI report can calculate understanding rate, usefulness rate, missing information, and blockers from verifiable feedback JSON.
```

## Primary executable object

```text
script=scripts/capture_customer_trial_feedback_sample.py
script=scripts/generate_internal_trial_kpi_report.py
test=backend/tests/test_capture_customer_trial_feedback_sample.py
artifact=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_feedback.sample.json
report=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report.json
report=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report_中文.md
closeout=docs/S6_FAST_MVP_MVP_76_CUSTOMER_TRIAL_FEEDBACK_SAMPLE_CAPTURE_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/package_manifest.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_status.json
scripts/generate_internal_trial_kpi_report.py
```

## Output paths

```text
docs/goals/GOAL-MVP-76_CUSTOMER_TRIAL_FEEDBACK_SAMPLE_CAPTURE.md
scripts/capture_customer_trial_feedback_sample.py
scripts/generate_internal_trial_kpi_report.py
backend/tests/test_capture_customer_trial_feedback_sample.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_feedback.sample.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report_中文.md
docs/S6_FAST_MVP_MVP_76_CUSTOMER_TRIAL_FEEDBACK_SAMPLE_CAPTURE_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-76_CUSTOMER_TRIAL_FEEDBACK_SAMPLE_CAPTURE.md
scripts/capture_customer_trial_feedback_sample.py
scripts/generate_internal_trial_kpi_report.py
backend/tests/test_capture_customer_trial_feedback_sample.py
backend/tests/test_generate_internal_trial_kpi_report.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_feedback.sample.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/internal_trial_kpi_report_中文.md
docs/S6_FAST_MVP_MVP_76_CUSTOMER_TRIAL_FEEDBACK_SAMPLE_CAPTURE_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline feedback sample capture only
local package and trial status artifact reads
local JSON validation
local KPI report regeneration from the feedback sample
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
py -3 scripts/capture_customer_trial_feedback_sample.py --package-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1 --output-path artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_feedback.sample.json --repo-root .
py -3 scripts/capture_customer_trial_feedback_sample.py --validate-only --feedback-json artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_feedback.sample.json --package-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1 --repo-root .
py -3 scripts/generate_internal_trial_kpi_report.py --package-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1 --output-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output --feedback-json artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_feedback.sample.json --repo-root .
py -3 -m unittest -q backend.tests.test_capture_customer_trial_feedback_sample backend.tests.test_generate_internal_trial_kpi_report
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-76_CUSTOMER_TRIAL_FEEDBACK_SAMPLE_CAPTURE.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
feedback capture script performs deployment, starts production service, calls live API, sends network request, reads API key, calls connector, writes production, or pushes
feedback sample contains real data, masked-real data, raw payload, auth header, token, secret, customer log, or production connector output
feedback sample lacks response_id, reviewer_role, understood, useful, missing_information, blocker, decision, or notes
feedback sample uses invalid reviewer_role or decision
trial status reports any forbidden boundary as true
KPI report does not calculate measured understanding rate, usefulness rate, missing information count, and next unlock
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete generated customer trial feedback sample and regenerated KPI report artifacts for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
goal card validator output
feedback sample capture output
feedback sample validation output
KPI report generation output with feedback-json
unit test output
customer_trial_feedback.sample.json
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
no Authorization/Bearer/refresh_token in feedback samples or reports
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT.
If HOLD, stop and report failing command plus blocker evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-76 customer trial feedback sample capture
stage and commit only Goal files
do not push
```
