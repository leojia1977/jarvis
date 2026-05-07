# GOAL-MVP-44_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP43

## Goal ID

```text
GOAL-MVP-44_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP43
```

## Goal type

```text
script
```

## Goal statement

```text
Close the RC-013 reviewer backlog item RFB-RC013-004 using the MVP-43 commit evidence, without changing product behavior or generating a new RC package.
```

## Primary executable object

```text
script=scripts/close_reviewer_backlog_items.py
artifact=artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog_closeout.json
artifact=artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog.json
closeout=docs/S6_FAST_MVP_MVP_44_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP43_2026_05_07.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog.json
scripts/close_reviewer_backlog_items.py
docs/S6_FAST_MVP_MVP_43_TECH_RECONCILIATION_COPY_CLARITY_CLOSEOUT_2026_05_07.md
```

## Output paths

```text
artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog.md
artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog_closeout.json
artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog_closeout.md
docs/goals/GOAL-MVP-44_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP43.md
docs/S6_FAST_MVP_MVP_44_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP43_2026_05_07.md
```

## Allowed files

```text
artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog.md
artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog_closeout.json
artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog_closeout.md
docs/goals/GOAL-MVP-44_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP43.md
docs/S6_FAST_MVP_MVP_44_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP43_2026_05_07.md
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-44_REVIEWER_BACKLOG_CLOSEOUT_FOR_MVP43.md
py -3 -m unittest backend.tests.test_close_reviewer_backlog_items
py -3 scripts/close_reviewer_backlog_items.py --backlog-json artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog.json --output-json artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog.json --output-md artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog.md --closeout-json artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog_closeout.json --closeout-md artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog_closeout.md --item-id RFB-RC013-004 --closed-by-goal GOAL-MVP-43_TECH_RECONCILIATION_COPY_CLARITY --closed-by-commit 5a526e8 --resolution "MVP-43 clarified the /s1-run technical reconciliation copy to say it is used to check candidate version, run id, evidence hash, and status code only." --evidence docs/S6_FAST_MVP_MVP_43_TECH_RECONCILIATION_COPY_CLARITY_CLOSEOUT_2026_05_07.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
RFB-RC013-004 is not present in the source backlog
closeout changes any backlog item other than RFB-RC013-004
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
reviewer_backlog.json with RFB-RC013-004 closed
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
If PASS, unlock selecting the next concrete GOAL-* from the remaining RC-013 notes or generating a fresh local/offline RC package if reviewer evidence needs refreshed screenshots.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: docs(secupilot): GOAL-MVP-44 close rc013 backlog item
do not push unless separately authorized
```
