# GOAL-MVP-26_CLIENT_TRIAL_READINESS_REPORT

## Goal ID

```text
GOAL-MVP-26_CLIENT_TRIAL_READINESS_REPORT
```

## Goal type

```text
test-report
```

## Goal statement

```text
Generate a client-trial readiness report from the accepted RC-009 local/offline package and reviewer feedback without authorizing customer-visible trial.
```

## Primary executable object

```text
script=scripts/build_client_trial_readiness_report.py
report=docs/S6_FAST_MVP_CLIENT_TRIAL_READINESS_REPORT_2026_05_07.md
test=backend/tests/test_build_client_trial_readiness_report.py
closeout=docs/S6_FAST_MVP_MVP_26_CLIENT_TRIAL_READINESS_REPORT_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/package_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/evidence/final_status.json
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/evidence/safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/SCREENSHOT_INDEX.json
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.json
```

## Output paths

```text
scripts/build_client_trial_readiness_report.py
backend/tests/test_build_client_trial_readiness_report.py
docs/goals/GOAL-MVP-26_CLIENT_TRIAL_READINESS_REPORT.md
docs/S6_FAST_MVP_CLIENT_TRIAL_READINESS_REPORT_2026_05_07.md
docs/S6_FAST_MVP_MVP_26_CLIENT_TRIAL_READINESS_REPORT_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
scripts/build_client_trial_readiness_report.py
backend/tests/test_build_client_trial_readiness_report.py
docs/goals/GOAL-MVP-26_CLIENT_TRIAL_READINESS_REPORT.md
docs/S6_FAST_MVP_CLIENT_TRIAL_READINESS_REPORT_2026_05_07.md
docs/S6_FAST_MVP_MVP_26_CLIENT_TRIAL_READINESS_REPORT_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
local report generation
local tests
local readiness synthesis
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
secrets/tokens/auth headers/raw customer logs
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-26_CLIENT_TRIAL_READINESS_REPORT.md
py -3 -m unittest backend.tests.test_build_client_trial_readiness_report
py -3 scripts/build_client_trial_readiness_report.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review --feedback-json artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.json --output-report docs/S6_FAST_MVP_CLIENT_TRIAL_READINESS_REPORT_2026_05_07.md
```

## HOLD conditions

```text
reviewer_feedback decision is not PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL
safety_scan finding_count > 0
customer_visible_output != false
production_writeback != false
screenshots missing
report claims customer-visible trial or deploy is authorized
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated readiness report only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
client trial readiness report
closeout note with exact commands
```

## Safety sentinels

```text
no Authorization: / Bearer / refresh_token in report
no raw_payload in report
no writeback_enabled=true
no customer_visible_output=true
customer_visible_or_deploy_go = false
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-25_QWEN_PROVIDER_DRY_CONTRACT as dry contract only.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: docs(secupilot): GOAL-MVP-26 client trial readiness report
do not push unless separately authorized
```
