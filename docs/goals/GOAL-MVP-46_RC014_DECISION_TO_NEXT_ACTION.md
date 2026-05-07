# GOAL-MVP-46_RC014_DECISION_TO_NEXT_ACTION

## Goal ID

```text
GOAL-MVP-46_RC014_DECISION_TO_NEXT_ACTION
```

## Goal type

```text
script
```

## Goal statement

```text
Convert the RC-014 local/offline reviewer PASS decision and non-blocking notes into structured feedback plus a repo-local next-action backlog.
```

## Primary executable object

```text
script=scripts/export_local_reviewer_feedback.py
script=scripts/export_reviewer_feedback_backlog.py
artifact=artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/reviewer_feedback.json
artifact=artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
closeout=docs/S6_FAST_MVP_MVP_46_RC014_DECISION_TO_NEXT_ACTION_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
docs/S6_RC_014_CHINESE_LOCAL_OFFLINE_REVIEW_DECISION_2026_05_07.md
artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/
scripts/export_local_reviewer_feedback.py
scripts/export_reviewer_feedback_backlog.py
```

## Output paths

```text
docs/S6_RC_014_CHINESE_LOCAL_OFFLINE_REVIEW_DECISION_2026_05_07.md
docs/goals/GOAL-MVP-46_RC014_DECISION_TO_NEXT_ACTION.md
artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/reviewer_feedback.json
artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/reviewer_feedback.md
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.md
docs/S6_FAST_MVP_MVP_46_RC014_DECISION_TO_NEXT_ACTION_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
docs/S6_RC_014_CHINESE_LOCAL_OFFLINE_REVIEW_DECISION_2026_05_07.md
docs/goals/GOAL-MVP-46_RC014_DECISION_TO_NEXT_ACTION.md
artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/reviewer_feedback.json
artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/reviewer_feedback.md
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.md
docs/S6_FAST_MVP_MVP_46_RC014_DECISION_TO_NEXT_ACTION_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
local reviewer decision parsing
local feedback JSON/MD generation
local next-action backlog JSON/MD generation
local tests
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
API keys
secrets/tokens/auth headers/raw customer logs
live connectors
external tracker writes
production write-back
customer-visible publish/deploy/output
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-46_RC014_DECISION_TO_NEXT_ACTION.md
py -3 -m unittest backend.tests.test_export_local_reviewer_feedback backend.tests.test_export_reviewer_feedback_backlog
py -3 scripts/export_local_reviewer_feedback.py --decision-doc docs/S6_RC_014_CHINESE_LOCAL_OFFLINE_REVIEW_DECISION_2026_05_07.md --package-dir artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review --output-json artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/reviewer_feedback.json --output-md artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/reviewer_feedback.md --reviewer "Jarvis / TL / Product-governance reviewer"
py -3 scripts/export_reviewer_feedback_backlog.py --feedback-json artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/reviewer_feedback.json --output-json artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json --output-md artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
RC-014 decision doc cannot be parsed
reviewer feedback missing candidate/source_candidate/decision/reviewer/timestamp
reviewer feedback boundary field is true
generated backlog contains secret/token/auth/raw payload/write-back marker
generated backlog grants customer-visible or deploy go
external tracker write is attempted or implied
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated reviewer_feedback.json/md and reviewer_backlog.json/md only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
reviewer_feedback.json
reviewer_feedback.md
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
no production_writeback=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock a focused UI copy Goal for the RC-014 N01 note.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: docs(secupilot): GOAL-MVP-46 rc014 decision next actions
do not push unless separately authorized
```
