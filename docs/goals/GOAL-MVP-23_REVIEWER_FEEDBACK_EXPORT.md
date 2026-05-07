# GOAL-MVP-23_REVIEWER_FEEDBACK_EXPORT

## Goal ID

```text
GOAL-MVP-23_REVIEWER_FEEDBACK_EXPORT
```

## Goal type

```text
run-artifact
```

## Goal statement

```text
Export the RC-009 local/offline reviewer PASS decision into structured reviewer_feedback.json and reviewer_feedback.md artifacts.
```

## Primary executable object

```text
script=scripts/export_local_reviewer_feedback.py
artifact=artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.json
artifact=artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.md
test=backend/tests/test_export_local_reviewer_feedback.py
closeout=docs/S6_FAST_MVP_MVP_23_REVIEWER_FEEDBACK_EXPORT_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
docs/S6_RC_009_CHINESE_LOCAL_OFFLINE_REVIEW_DECISION_2026_05_07.md
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/package_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/evidence/final_status.json
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/evidence/safety_scan.json
```

## Output paths

```text
scripts/export_local_reviewer_feedback.py
backend/tests/test_export_local_reviewer_feedback.py
docs/goals/GOAL-MVP-23_REVIEWER_FEEDBACK_EXPORT.md
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.json
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.md
docs/S6_FAST_MVP_MVP_23_REVIEWER_FEEDBACK_EXPORT_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
scripts/export_local_reviewer_feedback.py
backend/tests/test_export_local_reviewer_feedback.py
docs/goals/GOAL-MVP-23_REVIEWER_FEEDBACK_EXPORT.md
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.json
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.md
docs/S6_FAST_MVP_MVP_23_REVIEWER_FEEDBACK_EXPORT_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
local reviewer decision parsing
local artifact generation
local tests
local closeout note
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-23_REVIEWER_FEEDBACK_EXPORT.md
py -3 -m unittest backend.tests.test_export_local_reviewer_feedback
py -3 scripts/export_local_reviewer_feedback.py --decision-doc docs/S6_RC_009_CHINESE_LOCAL_OFFLINE_REVIEW_DECISION_2026_05_07.md --package-dir artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review --output-json artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.json --output-md artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.md
```

## HOLD conditions

```text
decision doc candidate does not match package manifest
safety_scan finding_count > 0
customer_visible_output != false
production_writeback != false
reviewer decision is missing
exported artifact contains secret/token/auth/raw payload markers
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated reviewer_feedback.json and reviewer_feedback.md only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
reviewer_feedback.json
reviewer_feedback.md
closeout note with exact commands
```

## Safety sentinels

```text
no Authorization: / Bearer / refresh_token in artifacts
no raw_payload in artifacts
no writeback_action in artifacts
no writeback_enabled=true
no customer_visible_output=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-26_CLIENT_TRIAL_READINESS_REPORT.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-23 reviewer feedback export
do not push unless separately authorized
```
