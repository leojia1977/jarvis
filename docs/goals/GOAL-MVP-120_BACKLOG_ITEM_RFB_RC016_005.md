# GOAL-MVP-120 Backlog Close RFB-RC016-005

## Goal ID

```text
GOAL-MVP-120_BACKLOG_ITEM_RFB_RC016_005
```

## Goal type

```text
script
```

## Goal statement

```text
Close reviewer backlog item RFB-RC016-005 by confirming Chinese-first customer copy remains in place and formal capitalization review is intentionally deferred to a later branding pass.
```

## Primary executable object

```text
artifact=artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json
artifact=artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.md
artifact=artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog_closeout_rfb_rc016_005.json
artifact=artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog_closeout_rfb_rc016_005.md
closeout=docs/S6_FAST_MVP_GOAL_MVP_120_BACKLOG_ITEM_RFB_RC016_005_2026_05_08.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json
scripts/close_reviewer_backlog_items.py
backend/tests/test_close_reviewer_backlog_items.py
frontend/src/App.tsx
commit 02783ca (GOAL-MVP-118 implementation)
```

## Output paths

```text
docs/goals/GOAL-MVP-120_BACKLOG_ITEM_RFB_RC016_005.md
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.md
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog_closeout_rfb_rc016_005.json
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog_closeout_rfb_rc016_005.md
docs/S6_FAST_MVP_GOAL_MVP_120_BACKLOG_ITEM_RFB_RC016_005_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-120_BACKLOG_ITEM_RFB_RC016_005.md
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.md
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog_closeout_rfb_rc016_005.json
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog_closeout_rfb_rc016_005.md
docs/S6_FAST_MVP_GOAL_MVP_120_BACKLOG_ITEM_RFB_RC016_005_2026_05_08.md
```

## Allowed scope

```text
single-item backlog status transition from BACKLOG_OPEN to BACKLOG_CLOSED
documented governance decision to keep current Chinese-first copy and defer capitalization to branding pass
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-120_BACKLOG_ITEM_RFB_RC016_005.md
py -3 -m unittest backend.tests.test_close_reviewer_backlog_items
py -3 scripts/close_reviewer_backlog_items.py --backlog-json artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json --output-json artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json --output-md artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.md --closeout-json artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog_closeout_rfb_rc016_005.json --closeout-md artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog_closeout_rfb_rc016_005.md --item-id RFB-RC016-005 --closed-by-goal GOAL-MVP-118_BACKLOG_ITEM_RFB_RC016_004 --closed-by-commit 02783ca --resolution "Confirmed incident-page copy remains Chinese-first for current local/internal trial; formal customer-view capitalization is deferred to a later branding pass." --evidence frontend/src/App.tsx --repo-root .
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
target backlog item id not found
closeout script returns HOLD
closed item evidence references are missing or malformed
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
keep historical residue untouched
```

## Evidence contract

```text
goal card validator PASS output
close backlog script unittest PASS output
close backlog command PASS output with closed_item_count=1
diff --check PASS output
closeout report linking item id and deferred branding decision
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no production_writeback=true
no customer_visible_output=true
no Authorization header
no Bearer token
no raw_payload
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock next picker-selected backlog item or queue fallback candidate.
If HOLD, stop and report exact failing command and artifact.
```

## Commit posture

```text
one commit per passing Goal
commit message: docs(secupilot): GOAL-MVP-120 close backlog item rc016-005
stage and commit only Goal files
do not push
```
