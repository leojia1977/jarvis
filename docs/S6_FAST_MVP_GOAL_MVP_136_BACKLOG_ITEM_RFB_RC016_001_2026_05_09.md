# S6 Fast MVP Goal Closeout - GOAL-MVP-136 Backlog Item RFB-RC016-001

Date: 2026-05-09
Goal: GOAL-MVP-136_BACKLOG_ITEM_RFB_RC016_001
Decision: PASS

## Scope

- Keep work inside package-builder + unittest boundary for `RFB-RC016-001`.
- Tighten folded-state screenshot archive evidence in `SCREENSHOT_INDEX.json`.

## Files Changed

- docs/goals/GOAL-MVP-136_BACKLOG_ITEM_RFB_RC016_001.md
- scripts/build_local_offline_trial_rc.py
- backend/tests/test_build_local_offline_trial_rc.py
- docs/S6_FAST_MVP_GOAL_MVP_136_BACKLOG_ITEM_RFB_RC016_001_2026_05_09.md

## Implementation Summary

- Added `capture_policy=FIRST_LOAD_NO_INTERACTION` to folded screenshot `archive_evidence` in screenshot index output.
- Added canonical `expected_route=/s1-run` and `expected_viewport=1440x1100` fields to the same folded screenshot archive evidence object.
- Updated unittest expectations to enforce the new screenshot-index evidence contract.

## Acceptance Commands

1. `py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-136_BACKLOG_ITEM_RFB_RC016_001.md`
- PASS

2. `py -3 -m unittest backend.tests.test_build_local_offline_trial_rc`
- PASS (`Ran 7 tests`)

3. `py -3 scripts/build_local_offline_trial_rc.py --help`
- PASS

4. `git -c core.quotepath=false diff --check`
- PASS (line-ending warnings only on pre-existing picker files)

## Safety and Boundary Check

- Local/offline package script and unittest scope only.
- No real data, no live API/connectors, no production write-back, no customer-visible deploy/output.
- No backend API/schema migration and no push.

## HOLD Check

- No HOLD condition triggered.

## Automated Review Status

- NOT_RUN in-goal (deterministic script/test evidence used).

## Next Unlock

- Run follow-up backlog closeout Goal for `RFB-RC016-001`.
