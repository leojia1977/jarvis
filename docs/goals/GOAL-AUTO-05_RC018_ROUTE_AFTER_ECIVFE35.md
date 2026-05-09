# GOAL-AUTO-05 RC018 Route After ECIVFE35

## Goal ID

GOAL-AUTO-05_RC018_ROUTE_AFTER_ECIVFE35

## Goal Type

script

## Goal Statement

Ensure the automation routes from completed ECI/VFE fixture, guard, UI, and local review package work directly into the RC-018 customer-readable review package instead of falling back to low-value backlog or legacy package work.

## Primary Executable Object

script=scripts/pick_next_mvp_goal.py
test=backend/tests/test_pick_next_mvp_goal.py
artifact=artifacts/product_acceleration/next_goal_candidate.json
closeout=docs/S6_FAST_PRODUCT_GOAL_AUTO_05_RC018_ROUTE_AFTER_ECIVFE35_CLOSEOUT_2026_05_09.md

## Inputs

- `docs/S6_RC018_CUSTOMER_READABLE_REVIEW_PACKAGE_DESIGN_2026_05_09.md`
- Current ECI/VFE queue design: 30 -> 33 -> 34 -> 31 -> 32 -> 35
- Current backlog-throttle behavior from `GOAL-AUTO-04`

## Output Paths

- `docs/goals/GOAL-AUTO-05_RC018_ROUTE_AFTER_ECIVFE35.md`
- `scripts/pick_next_mvp_goal.py`
- `backend/tests/test_pick_next_mvp_goal.py`
- `artifacts/product_acceleration/next_goal_candidate.json`
- `artifacts/product_acceleration/next_goal_candidate.md`
- `docs/S6_FAST_PRODUCT_GOAL_AUTO_05_RC018_ROUTE_AFTER_ECIVFE35_CLOSEOUT_2026_05_09.md`

## Allowed Files

- `docs/goals/GOAL-AUTO-05_RC018_ROUTE_AFTER_ECIVFE35.md`
- `scripts/pick_next_mvp_goal.py`
- `backend/tests/test_pick_next_mvp_goal.py`
- `artifacts/product_acceleration/next_goal_candidate.json`
- `artifacts/product_acceleration/next_goal_candidate.md`
- `docs/S6_FAST_PRODUCT_GOAL_AUTO_05_RC018_ROUTE_AFTER_ECIVFE35_CLOSEOUT_2026_05_09.md`

## Allowed Scope

- Add a picker queue entry for `GOAL-RC018_CUSTOMER_READABLE_PACKAGE`.
- Add a package contract for the future RC-018 builder script.
- Add a test proving the picker selects RC-018 after `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE` exists.
- Refresh the current candidate without changing it while `GOAL-ECIVFE-32_FORECAST_CARD_UI` remains incomplete.

## Forbidden Scope

- real data
- masked-real data
- live Qwen/API/connectors
- production write-back
- customer-visible publish, deploy, or output
- external pilot
- production launch
- secrets, tokens, auth headers, raw logs, raw payloads, PoC, exploit steps, or attacker-readable topology
- autonomous containment, remediation, isolation, blocking, approval, rejection, or action-mode choice
- implementing RC-018 package builder logic in this Goal
- touching ECIVFE-32 or ECIVFE-35 implementation files
- push

## Acceptance Commands

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-AUTO-05_RC018_ROUTE_AFTER_ECIVFE35.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts\pick_next_mvp_goal.py --repo-root . --output-json artifacts\product_acceleration\next_goal_candidate.json --output-md artifacts\product_acceleration\next_goal_candidate.md
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- picker does not select `GOAL-RC018_CUSTOMER_READABLE_PACKAGE` after `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE` exists
- picker selects RC-018 before `GOAL-ECIVFE-32` and `GOAL-ECIVFE-35` exist
- current refreshed candidate changes away from `GOAL-ECIVFE-32_FORECAST_CARD_UI` before ECIVFE-32 is complete
- RC-018 package contract starts from artifact tables rather than product route map
- RC-018 contract authorizes real data, live model/API, connector, write-back, deploy, customer-visible output, raw evidence, PoC/exploit detail, topology disclosure, or autonomous action
- tests fail twice in the same way
- scope expands beyond listed files

## Rollback

- Revert the picker and picker-test changes.
- Re-run the picker to restore the previous next-goal candidate.
- Preserve automation memory and previous product-route docs as evidence.

## Evidence Contract

- Goal-card validation output
- picker unit-test output
- refreshed `next_goal_candidate.json` and `next_goal_candidate.md`
- closeout report with exact command results

## Safety Sentinels

- no `real_data=true`
- no `masked_real_data=true`
- no `live_qwen_api=true`
- no `production_writeback=true`
- no `customer_visible_output=true`
- no `Authorization`
- no `Bearer`
- no `token`
- no `raw_payload`
- no `action_command`
- no attacker-readable `attack_path`

## Merge Rule

May stage and commit only if the goal card validates, picker tests pass, the refreshed current candidate remains `GOAL-ECIVFE-32_FORECAST_CARD_UI`, and the post-ECIVFE35 test proves RC-018 is next. Do not push. Do not merge unrelated changes.

## Next Unlock

If PASS, unlock automation continuation from ECIVFE-32 to ECIVFE-35 to RC-018 customer-readable package. If HOLD, stop and report the exact routing or safety-contract failure.

## Commit Posture

One commit for `GOAL-AUTO-05`. Stage and commit only listed files. Do not push.
