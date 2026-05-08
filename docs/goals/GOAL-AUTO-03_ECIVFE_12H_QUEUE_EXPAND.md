# GOAL-AUTO-03 ECIVFE 12H Queue Expand

## Goal ID

GOAL-AUTO-03_ECIVFE_12H_QUEUE_EXPAND

## Goal Type

script

## Goal Statement

Expand the active SecuPilot automation picker so the ECI/VFE lane can continue after guard work into UI and local review package goals instead of stopping after GOAL-ECIVFE-34.

## Primary Executable Object

script=scripts/pick_next_mvp_goal.py
test=backend/tests/test_pick_next_mvp_goal.py
artifact=artifacts/product_acceleration/next_goal_candidate.json
closeout=docs/S6_FAST_PRODUCT_GOAL_AUTO_03_ECIVFE_12H_QUEUE_EXPAND_CLOSEOUT_2026_05_08.md

## Inputs

- `docs/S6_ECI_VFE_V0_2_BASELINE_INTAKE_AND_GOAL_MAPPING_2026_05_08.md`
- `docs/goals/GOAL-ECIVFE-30_FIXTURE_MODEL.md`
- Current automation memory showing `GOAL-ECIVFE-33_LOCAL_RULE_ENGINE` as next candidate

## Output Paths

- `docs/goals/GOAL-AUTO-03_ECIVFE_12H_QUEUE_EXPAND.md`
- `scripts/pick_next_mvp_goal.py`
- `backend/tests/test_pick_next_mvp_goal.py`
- `artifacts/product_acceleration/next_goal_candidate.json`
- `artifacts/product_acceleration/next_goal_candidate.md`
- `docs/S6_FAST_PRODUCT_GOAL_AUTO_03_ECIVFE_12H_QUEUE_EXPAND_CLOSEOUT_2026_05_08.md`

## Allowed Files

- `docs/goals/GOAL-AUTO-03_ECIVFE_12H_QUEUE_EXPAND.md`
- `scripts/pick_next_mvp_goal.py`
- `backend/tests/test_pick_next_mvp_goal.py`
- `artifacts/product_acceleration/next_goal_candidate.json`
- `artifacts/product_acceleration/next_goal_candidate.md`
- `docs/S6_FAST_PRODUCT_GOAL_AUTO_03_ECIVFE_12H_QUEUE_EXPAND_CLOSEOUT_2026_05_08.md`

## Allowed Scope

- Add picker queue entries for `GOAL-ECIVFE-31_CHAIN_INDICATOR_UI`, `GOAL-ECIVFE-32_FORECAST_CARD_UI`, and `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE`.
- Add picker contract profiles with exact files, acceptance commands, and HOLD conditions.
- Add unit tests that prove the ECI/VFE lane advances in the required order: 30 -> 33 -> 34 -> 31 -> 32 -> 35.
- Refresh the current next-goal candidate without changing the current candidate if 33 remains next.

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
- implementing ECI/VFE UI or package logic in this Goal
- push

## Acceptance Commands

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-AUTO-03_ECIVFE_12H_QUEUE_EXPAND.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts\pick_next_mvp_goal.py --output-json artifacts/product_acceleration/next_goal_candidate.json --output-md artifacts/product_acceleration/next_goal_candidate.md
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- picker skips `GOAL-ECIVFE-33` or `GOAL-ECIVFE-34`
- picker allows `GOAL-ECIVFE-31` before output guard exists
- picker allows `GOAL-ECIVFE-32` before chain indicator UI exists
- picker allows `GOAL-ECIVFE-35` before both UI goals exist
- any new candidate omits executable object, exact files, acceptance commands, or HOLD conditions
- any new candidate authorizes real data, live model/API, connector, write-back, deploy, customer-visible output, raw evidence, PoC/exploit detail, topology disclosure, or autonomous action
- tests fail twice in the same way
- scope expands beyond listed files

## Rollback

- Revert the picker and picker-test changes.
- Re-run the picker to restore the previous next-goal candidate.
- Preserve automation memory and failure output as evidence.

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
- no `attack_path` without defensive summary guard language

## Merge Rule

May stage and commit only if the goal card validates, picker tests pass, picker output remains on the correct next executable ECI/VFE candidate, and no HOLD condition is observed. Do not push. Do not merge unrelated changes.

## Next Unlock

If PASS, unlock overnight automation continuation through ECI/VFE 33, 34, 31, 32, and 35 before falling back to product acceleration pool items. If HOLD, stop and report the exact queue ordering or safety-contract issue.

## Commit Posture

One commit for `GOAL-AUTO-03`. Stage and commit only listed files. Do not push.
