# S6 Fast Product Goal AUTO-03 ECI/VFE 12H Queue Expand Closeout

Date: 2026-05-08

Goal: GOAL-AUTO-03_ECIVFE_12H_QUEUE_EXPAND

## Outcome

PASS

## What Changed

- Added ECI/VFE automation picker entries for:
  - `GOAL-ECIVFE-31_CHAIN_INDICATOR_UI`
  - `GOAL-ECIVFE-32_FORECAST_CARD_UI`
  - `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE`
- Locked the required ECI/VFE automation order:
  - 30 fixture model
  - 33 local rule engine
  - 34 output guard
  - 31 chain indicator UI
  - 32 forecast card UI
  - 35 local review package
- Added picker tests for the post-guard UI and package progression.
- Kept the current next candidate on `GOAL-ECIVFE-33_LOCAL_RULE_ENGINE` because only GOAL-ECIVFE-30 is complete right now.

## Boundary

This change only expands local/offline automation candidate selection. It does not implement ECI/VFE UI, does not build the review package, does not call live Qwen/API/connectors, and does not authorize real data, masked-real data, production write-back, customer-visible output, deploy, external pilot, or production launch.

## Verification

Commands run:

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-AUTO-03_ECIVFE_12H_QUEUE_EXPAND.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts\pick_next_mvp_goal.py --output-json artifacts/product_acceleration/next_goal_candidate.json --output-md artifacts/product_acceleration/next_goal_candidate.md
git -c core.quotepath=false diff --check
```

Results:

- Goal-card validation: PASS
- Picker tests: PASS, 15 tests
- Picker refresh: PASS
- Current candidate remains: `GOAL-ECIVFE-33_LOCAL_RULE_ENGINE`
- Diff whitespace check: PASS

## Next Automation Behavior

After this closeout passes, the active automation can keep working through the ECI/VFE lane after the next run:

1. `GOAL-ECIVFE-33_LOCAL_RULE_ENGINE`
2. `GOAL-ECIVFE-34_OUTPUT_GUARD`
3. `GOAL-ECIVFE-31_CHAIN_INDICATOR_UI`
4. `GOAL-ECIVFE-32_FORECAST_CARD_UI`
5. `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE`

The existing automation recurrence is hourly, but its prompt allows up to three sequential clean Goals per run. So the next 12 hours should have enough executable work, provided the worktree remains clean except for known ignored historical residue.
