# GOAL-AUTO-02 Product Acceleration Pool Expand

## Goal ID

GOAL-AUTO-02_PRODUCT_ACCELERATION_POOL_EXPAND

## Goal Type

script

## Goal Statement

Expand the picker-backed automation queue so SecuPilot product acceleration can keep selecting executable private-preview Goals after the current MVP-95 through MVP-98 lane is exhausted.

## Primary Executable Object

script=scripts/pick_next_mvp_goal.py
test=backend/tests/test_pick_next_mvp_goal.py
artifact=artifacts/product_acceleration/next_goal_candidate.json
closeout=docs/S6_FAST_PRODUCT_GOAL_AUTO_02_PRODUCT_ACCELERATION_POOL_EXPAND_CLOSEOUT_2026_05_08.md

## Inputs

- `scripts/pick_next_mvp_goal.py`
- `backend/tests/test_pick_next_mvp_goal.py`
- `artifacts/product_acceleration/next_goal_candidate.json`
- `artifacts/product_acceleration/next_goal_candidate.md`

## Output Paths

- `scripts/pick_next_mvp_goal.py`
- `backend/tests/test_pick_next_mvp_goal.py`
- `docs/goals/GOAL-AUTO-02_PRODUCT_ACCELERATION_POOL_EXPAND.md`
- `docs/S6_FAST_PRODUCT_GOAL_AUTO_02_PRODUCT_ACCELERATION_POOL_EXPAND_CLOSEOUT_2026_05_08.md`
- `artifacts/product_acceleration/next_goal_candidate.json`
- `artifacts/product_acceleration/next_goal_candidate.md`

## Allowed Files

- `scripts/pick_next_mvp_goal.py`
- `backend/tests/test_pick_next_mvp_goal.py`
- `docs/goals/GOAL-AUTO-02_PRODUCT_ACCELERATION_POOL_EXPAND.md`
- `docs/S6_FAST_PRODUCT_GOAL_AUTO_02_PRODUCT_ACCELERATION_POOL_EXPAND_CLOSEOUT_2026_05_08.md`
- `artifacts/product_acceleration/next_goal_candidate.json`
- `artifacts/product_acceleration/next_goal_candidate.md`

## Allowed Scope

- Add bounded product-acceleration queue templates after the private-preview RC package refresh lane.
- Add picker contracts with exact files, commands, and HOLD conditions for new executable Goals.
- Add unit tests proving the lane continues after MVP-95 through MVP-98.
- Refresh the current next-goal candidate artifact.
- Stage and commit this automation/picker change.

## Forbidden Scope

- No real data.
- No masked-real data.
- No live Qwen/API calls.
- No live connectors.
- No production write-back or production writeback.
- No customer-visible publish/deploy/output.
- No secrets, tokens, auth headers, or raw customer logs.
- No backend API/schema migration outside the picker/test files listed here.
- No autonomous approval, isolation, blocking, account closure, or state mutation.
- No push.

## Acceptance Commands

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-AUTO-02_PRODUCT_ACCELERATION_POOL_EXPAND.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts\pick_next_mvp_goal.py --repo-root . --output-json artifacts\product_acceleration\next_goal_candidate.json --output-md artifacts\product_acceleration\next_goal_candidate.md
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- Picker still falls to `QUEUE_EXHAUSTED_REQUIRE_NEW_PRODUCT_GOAL` immediately after MVP-95 through MVP-98 exist.
- New queue templates lack exact files, acceptance commands, or HOLD conditions.
- New queue templates authorize real data, masked-real data, live Qwen/API, connectors, production write-back, deploy, or customer-visible output.
- Unit tests fail twice in the same way.
- Scope expands beyond listed files.

## Rollback

- Revert `scripts/pick_next_mvp_goal.py`.
- Revert `backend/tests/test_pick_next_mvp_goal.py`.
- Revert generated `artifacts/product_acceleration/next_goal_candidate.json` and `.md` if they were refreshed only for this Goal.
- Preserve failure output in the closeout if the Goal reaches HOLD.
- Do not hide failed evidence.

## Evidence Contract

- Command transcript or test output for all acceptance commands.
- Refreshed next-goal candidate JSON and Markdown artifacts.
- Closeout report listing the new queue depth and next selected candidate.
- Git diff check result.

## Safety Sentinels

- no `live Qwen/API calls`
- no `production write-back`
- no `customer-visible publish/deploy/output`
- no `secret` / `token` / `auth header`
- `QUEUE_EXHAUSTED_REQUIRE_NEW_PRODUCT_GOAL` must not appear until the expanded private-preview pool is exhausted

## Merge Rule

May stage/commit only if all acceptance commands PASS and no HOLD condition is observed. Do not push. Do not include unrelated changes or historical untracked residue.

## Next Unlock

If PASS, unlock overnight automation continuation through the expanded private-preview product pool while manual UX03 work continues separately. If HOLD, stop and report the picker/queue blocker before more manual product work is mixed into the automation lane.

## Commit Posture

Commit this Goal as one focused automation queue commit after verification. Do not push.
