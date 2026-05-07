# GOAL-MVP-48_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP47

## Goal ID

```text
GOAL-MVP-48_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP47
```

## Goal type

```text
script
```

## Goal statement

```text
Close RC-014 reviewer backlog item RFB-RC014-002 using MVP-47 commit evidence, without changing product behavior or generating a new RC package.
```

## Primary executable object

```text
script=scripts/close_reviewer_backlog_items.py
artifact=artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog_closeout.json
artifact=artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
closeout=docs/S6_FAST_MVP_MVP_48_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP47_2026_05_07.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
scripts/close_reviewer_backlog_items.py
docs/S6_FAST_MVP_MVP_47_RESULT_PAGE_FIELD_DOWNSHIFT_CLOSEOUT_2026_05_07.md
```

## Output paths

```text
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.md
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog_closeout.json
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog_closeout.md
docs/goals/GOAL-MVP-48_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP47.md
docs/S6_FAST_MVP_MVP_48_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP47_2026_05_07.md
artifacts/reviews/claude_code/mvp-48-current-diff-review-20260507.txt
```

## Allowed files

```text
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.md
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog_closeout.json
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog_closeout.md
docs/goals/GOAL-MVP-48_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP47.md
docs/S6_FAST_MVP_MVP_48_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP47_2026_05_07.md
artifacts/reviews/claude_code/mvp-48-current-diff-review-20260507.txt
```

## Allowed scope

```text
local/offline only
repo-local backlog closeout
local tests
no product behavior changes
no new RC package generation
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-48_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP47.md
py -3 -m unittest backend.tests.test_close_reviewer_backlog_items
py -3 scripts/close_reviewer_backlog_items.py --backlog-json artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json --output-json artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json --output-md artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.md --closeout-json artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog_closeout.json --closeout-md artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog_closeout.md --item-id RFB-RC014-002 --closed-by-goal GOAL-MVP-47_RESULT_PAGE_FIELD_DOWNSHIFT --closed-by-commit bc67b42 --resolution "MVP-47 moved candidate, run id, data mode, and provider from first-screen emphasis into technical reconciliation while preserving traceability." --evidence docs/S6_FAST_MVP_MVP_47_RESULT_PAGE_FIELD_DOWNSHIFT_CLOSEOUT_2026_05_07.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
RFB-RC014-002 is not present in the source backlog
closeout changes any backlog item other than RFB-RC014-002
backlog grants customer-visible or deploy go
external tracker write is attempted or implied
generated closeout contains secret/token/auth/raw payload/write-back marker
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files only
preserve failure evidence
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
reviewer_backlog.json with RFB-RC014-002 closed
reviewer_backlog_closeout.json
reviewer_backlog_closeout.md
automated review artifact or REVIEW_TOOL_UNAVAILABLE_NON_BLOCKING record
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
If PASS, unlock selecting the next concrete GOAL-* from remaining RC-014 backlog items or refreshing RC package evidence when needed.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: docs(secupilot): GOAL-MVP-48 close rc014 backlog item
do not push unless separately authorized
```
