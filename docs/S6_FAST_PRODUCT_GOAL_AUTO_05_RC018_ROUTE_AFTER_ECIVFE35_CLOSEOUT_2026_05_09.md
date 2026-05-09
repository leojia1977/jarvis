# S6 Fast Product Goal AUTO-05 RC018 Route After ECIVFE35 Closeout

Date: 2026-05-09

Goal: GOAL-AUTO-05_RC018_ROUTE_AFTER_ECIVFE35

## Outcome

PASS

## Why This Exists

RC-018 has now been designed as a customer-readable local/offline review package. The automation must not finish ECI/VFE-35 and then drift back to low-value backlog or legacy package work.

This Goal adds the missing route from completed ECI/VFE work into the RC-018 package builder contract.

## Policy Implemented

- Keep the current candidate on `GOAL-ECIVFE-32_FORECAST_CARD_UI` while ECIVFE-32 is incomplete.
- After ECIVFE-32 and ECIVFE-35 are complete, select `GOAL-RC018_CUSTOMER_READABLE_PACKAGE`.
- Define RC-018 package acceptance around product route, screenshots, safety scan, manifest, screenshot index, ECI/VFE guard scan, and local/offline boundaries.

## Boundary

This change only affects picker routing. It does not implement ECIVFE-32, ECIVFE-35, or the RC-018 package builder. It does not use real data, call live Qwen/API/connectors, authorize production write-back, create customer-visible output, deploy, launch, or enable autonomous action.

## Verification

Commands run:

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-AUTO-05_RC018_ROUTE_AFTER_ECIVFE35.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts\pick_next_mvp_goal.py --repo-root . --output-json artifacts\product_acceleration\next_goal_candidate.json --output-md artifacts\product_acceleration\next_goal_candidate.md
git -c core.quotepath=false diff --check
```

Results:

- Goal-card validation: PASS
- Picker tests: PASS, 19 tests
- Picker refresh: PASS
- Current candidate remains: `GOAL-ECIVFE-32_FORECAST_CARD_UI`
- Post-ECIVFE35 routing test: PASS, next queue becomes `GOAL-RC018_CUSTOMER_READABLE_PACKAGE`
- Diff whitespace check: PASS, with line-ending warnings only on refreshed candidate files

## Next Route

1. `GOAL-ECIVFE-32_FORECAST_CARD_UI`
2. `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE`
3. `GOAL-RC018_CUSTOMER_READABLE_PACKAGE`
4. RC-018 review decision export and product polish
