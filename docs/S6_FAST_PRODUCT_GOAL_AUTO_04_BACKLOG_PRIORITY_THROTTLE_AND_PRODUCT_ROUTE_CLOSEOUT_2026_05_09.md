# S6 Fast Product Goal AUTO-04 Backlog Priority Throttle And Product Route Closeout

Date: 2026-05-09

Goal: GOAL-AUTO-04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE

## Outcome

PASS

## Why This Exists

The overnight automation delivered useful commits, but after `GOAL-ECIVFE-31` it spent many runs on low-priority folded-screenshot metadata backlog work. Those commits were passing and bounded, but the product acceleration value was too low for the current stage.

This Goal changes the picker itself so the automation cannot keep selecting P3 micro-tasks while a higher-value product queue item is open.

## Policy Implemented

- P0/P1 reviewer backlog items may preempt the queue.
- P2 reviewer backlog items may create at most two goal-card attempts for the same backlog item.
- P3 reviewer backlog items do not preempt an open product queue. They can only be considered after the queue is exhausted, and even then are limited to one attempt.
- The current next candidate should route back to `GOAL-ECIVFE-32_FORECAST_CARD_UI`.

## Boundary

This change only affects local automation candidate selection. It does not implement ECI/VFE UI, does not build RC-018, does not use real data, does not call live Qwen/API/connectors, and does not authorize production write-back, customer-visible output, deploy, external pilot, or production launch.

## Verification

Commands run:

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-AUTO-04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts\pick_next_mvp_goal.py --repo-root . --output-json artifacts\product_acceleration\next_goal_candidate.json --output-md artifacts\product_acceleration\next_goal_candidate.md
git -c core.quotepath=false diff --check
```

Results:

- Goal-card validation: PASS
- Picker tests: PASS, 18 tests
- Picker refresh: PASS
- Current candidate: `GOAL-ECIVFE-32_FORECAST_CARD_UI`
- Diff whitespace check: PASS, with line-ending warnings only on refreshed candidate files

## Next Route

After PASS, automation should resume on:

1. `GOAL-ECIVFE-32_FORECAST_CARD_UI`
2. `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE`
3. RC-018 package after ECI/VFE UI/package evidence exists
4. Product homepage and incident-workbench polish
