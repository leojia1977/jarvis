# GOAL-AUTO-04 Backlog Priority Throttle And Product Route

## Goal ID

GOAL-AUTO-04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE

## Goal Type

script

## Goal Statement

Stop low-priority reviewer backlog micro-tasks from monopolizing automation, and route the next executable candidate back to high-value product work: ECI/VFE forecast UI, ECI/VFE local review package, RC-018 package, then product-home and incident-workbench polish.

## Primary Executable Object

script=scripts/pick_next_mvp_goal.py
test=backend/tests/test_pick_next_mvp_goal.py
artifact=artifacts/product_acceleration/next_goal_candidate.json
closeout=docs/S6_FAST_PRODUCT_GOAL_AUTO_04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE_CLOSEOUT_2026_05_09.md

## Inputs

- Current automation memory showing repeated P3 folded-screenshot backlog commits.
- Current `artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json`.
- Existing ECI/VFE lane state where 30, 33, 34, and 31 are complete, while 32 and 35 remain open.

## Output Paths

- `docs/goals/GOAL-AUTO-04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE.md`
- `scripts/pick_next_mvp_goal.py`
- `backend/tests/test_pick_next_mvp_goal.py`
- `artifacts/product_acceleration/next_goal_candidate.json`
- `artifacts/product_acceleration/next_goal_candidate.md`
- `docs/S6_FAST_PRODUCT_GOAL_AUTO_04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE_CLOSEOUT_2026_05_09.md`

## Allowed Files

- `docs/goals/GOAL-AUTO-04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE.md`
- `scripts/pick_next_mvp_goal.py`
- `backend/tests/test_pick_next_mvp_goal.py`
- `artifacts/product_acceleration/next_goal_candidate.json`
- `artifacts/product_acceleration/next_goal_candidate.md`
- `docs/S6_FAST_PRODUCT_GOAL_AUTO_04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE_CLOSEOUT_2026_05_09.md`

## Allowed Scope

- Change backlog selection policy in the next-goal picker.
- Add tests proving P3 backlog items do not preempt an open high-value queue item.
- Add tests proving P2 backlog items are limited to two goal-card attempts.
- Preserve P0/P1 backlog preemption for true blockers.
- Refresh the next-goal candidate so it points to `GOAL-ECIVFE-32_FORECAST_CARD_UI`.

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
- implementing ECI/VFE UI or RC-018 package logic in this Goal
- rewriting old automation history or reverting prior commits
- push

## Acceptance Commands

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-AUTO-04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts\pick_next_mvp_goal.py --repo-root . --output-json artifacts\product_acceleration\next_goal_candidate.json --output-md artifacts\product_acceleration\next_goal_candidate.md
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- P3 backlog item preempts `GOAL-ECIVFE-32_FORECAST_CARD_UI` while the ECI/VFE queue is still open.
- P2 backlog item can create more than two goal-card attempts for the same backlog item.
- P0/P1 backlog blockers can no longer preempt the queue.
- Next candidate is not `GOAL-ECIVFE-32_FORECAST_CARD_UI` after the picker refresh.
- Any candidate authorizes real data, live model/API, connector, write-back, deploy, customer-visible output, raw evidence, PoC/exploit detail, topology disclosure, or autonomous action.
- Tests fail twice in the same way.
- Scope expands beyond listed files.

## Rollback

- Revert the picker and picker-test changes.
- Re-run the picker to restore the previous next-goal candidate.
- Preserve automation memory and previous P3 backlog commits as audit evidence; do not rewrite history.

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

May stage and commit only if the goal card validates, picker tests pass, the refreshed candidate is `GOAL-ECIVFE-32_FORECAST_CARD_UI`, and no HOLD condition is observed. Do not push. Do not merge unrelated changes.

## Next Unlock

If PASS, unlock automation continuation on `GOAL-ECIVFE-32_FORECAST_CARD_UI`, followed by `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE`, RC-018 package work, and product-home/incident-workbench polish. If HOLD, stop and report the exact priority-throttle or routing failure.

## Commit Posture

One commit for `GOAL-AUTO-04`. Stage and commit only listed files. Do not push.
