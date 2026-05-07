# GOAL-MVP-30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG

## Goal ID

```text
GOAL-MVP-30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG
```

## Goal type

```text
script
```

## Goal statement

```text
Convert structured local reviewer feedback into a repo-local product backlog and action list without writing to external trackers.
```

## Primary executable object

```text
script=scripts/export_reviewer_feedback_backlog.py
test=backend/tests/test_export_reviewer_feedback_backlog.py
artifact=artifacts/product_backlog/local-offline-trial-rc-009-cn-review/reviewer_backlog.json
closeout=docs/S6_FAST_MVP_MVP_30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.json
```

## Output paths

```text
scripts/export_reviewer_feedback_backlog.py
backend/tests/test_export_reviewer_feedback_backlog.py
docs/goals/GOAL-MVP-30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG.md
artifacts/product_backlog/local-offline-trial-rc-009-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-009-cn-review/reviewer_backlog.md
docs/S6_FAST_MVP_MVP_30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
scripts/export_reviewer_feedback_backlog.py
backend/tests/test_export_reviewer_feedback_backlog.py
docs/goals/GOAL-MVP-30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG.md
artifacts/product_backlog/local-offline-trial-rc-009-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-009-cn-review/reviewer_backlog.md
docs/S6_FAST_MVP_MVP_30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
local reviewer feedback parsing
local backlog JSON/MD artifact generation
local tests
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
external tracker writes
production write-back
customer-visible publish/deploy/output
secrets/tokens/auth headers/raw customer logs
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG.md
py -3 -m unittest backend.tests.test_export_reviewer_feedback_backlog
py -3 scripts/export_reviewer_feedback_backlog.py --feedback-json artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/reviewer_feedback.json --output-json artifacts/product_backlog/local-offline-trial-rc-009-cn-review/reviewer_backlog.json --output-md artifacts/product_backlog/local-offline-trial-rc-009-cn-review/reviewer_backlog.md
```

## HOLD conditions

```text
reviewer feedback missing candidate/source_candidate/decision/reviewer/timestamp
reviewer feedback boundary field is true
reviewer feedback grants customer-visible or deploy go
generated backlog contains secret/token/auth/raw payload/write-back marker
external tracker write is attempted or implied
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated reviewer_backlog.json/md only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
reviewer_backlog.json
reviewer_backlog.md
closeout note with exact commands
```

## Safety sentinels

```text
no external tracker write
no Authorization: / Bearer / refresh_token in artifacts
no raw_payload in artifacts
no customer_visible_output=true
no customer_visible_or_deploy_go=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock backlog artifacts for the next product route selection.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-30 reviewer feedback backlog
do not push unless separately authorized
```
