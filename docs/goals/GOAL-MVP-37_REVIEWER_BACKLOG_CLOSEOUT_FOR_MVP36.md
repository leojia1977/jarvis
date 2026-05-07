# GOAL-MVP-37_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP36

## Goal ID

```text
GOAL-MVP-37_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP36
```

## Goal type

```text
script
```

## Goal statement

```text
Close the RC-011 reviewer backlog actions that were resolved by MVP-36, leaving a repo-local closeout record and no external tracker writes.
```

## Primary executable object

```text
script=scripts/close_reviewer_backlog_items.py
test=backend/tests/test_close_reviewer_backlog_items.py
artifact=artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog.json
artifact=artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog_closeout.json
closeout=docs/S6_FAST_MVP_MVP_37_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP36_2026_05_07.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog.json
docs/S6_FAST_MVP_MVP_36_RESULT_TECH_CODE_DISCLOSURE_CLOSEOUT_2026_05_07.md
scripts/close_reviewer_backlog_items.py
```

## Output paths

```text
scripts/close_reviewer_backlog_items.py
backend/tests/test_close_reviewer_backlog_items.py
docs/goals/GOAL-MVP-37_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP36.md
artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog.md
artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog_closeout.json
artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog_closeout.md
docs/S6_FAST_MVP_MVP_37_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP36_2026_05_07.md
```

## Allowed files

```text
scripts/close_reviewer_backlog_items.py
backend/tests/test_close_reviewer_backlog_items.py
docs/goals/GOAL-MVP-37_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP36.md
artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog.md
artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog_closeout.json
artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog_closeout.md
docs/S6_FAST_MVP_MVP_37_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP36_2026_05_07.md
```

## Allowed scope

```text
local/offline only
local reviewer backlog closeout
local closeout JSON/MD generation
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-37_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP36.md
py -3 -m unittest backend.tests.test_close_reviewer_backlog_items
py -3 scripts/close_reviewer_backlog_items.py --backlog-json artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog.json --output-json artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog.json --output-md artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog.md --closeout-json artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog_closeout.json --closeout-md artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog_closeout.md --item-id RFB-RC011-001 --item-id RFB-RC011-002 --closed-by-goal GOAL-MVP-36_RESULT_TECH_CODE_DISCLOSURE --closed-by-commit 02fa889 --resolution "MVP-36 added Chinese tooltips and moved raw technical codes into technical reconciliation." --evidence docs/S6_FAST_MVP_MVP_36_RESULT_TECH_CODE_DISCLOSURE_CLOSEOUT_2026_05_07.md
```

## HOLD conditions

```text
requested backlog item id is missing
closed item does not become BACKLOG_CLOSED
closeout record grants customer-visible or deploy go
external tracker write is attempted or implied
generated artifacts contain secret/token/auth/raw payload/write-back marker
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
restore reviewer_backlog.json/md to previous committed state
delete generated reviewer_backlog_closeout.json/md only
preserve failure evidence
```

## Evidence contract

```text
command transcript or test output
updated reviewer_backlog.json
updated reviewer_backlog.md
reviewer_backlog_closeout.json
reviewer_backlog_closeout.md
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
If PASS, unlock GOAL-MVP-38_RC012_REVIEW_PACKAGE_AFTER_MVP36.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-37 reviewer backlog closeout
do not push unless separately authorized
```
