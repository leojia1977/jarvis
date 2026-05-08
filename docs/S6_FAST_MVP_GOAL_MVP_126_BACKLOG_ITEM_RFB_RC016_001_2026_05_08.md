# S6 Fast MVP Goal Closeout - GOAL-MVP-126 Backlog Item RFB-RC016-001

Date: 2026-05-08
Goal: GOAL-MVP-126_BACKLOG_ITEM_RFB_RC016_001
Decision: PASS

## Scope

- Keep work inside package-builder + unittest boundary for `RFB-RC016-001`.
- Add canonical folded-state screenshot path key into required archive evidence payload.

## Files Changed

- docs/goals/GOAL-MVP-126_BACKLOG_ITEM_RFB_RC016_001.md
- scripts/build_local_offline_trial_rc.py
- backend/tests/test_build_local_offline_trial_rc.py
- docs/S6_FAST_MVP_GOAL_MVP_126_BACKLOG_ITEM_RFB_RC016_001_2026_05_08.md

## Implementation Summary

- Extended required archive evidence payload with `folded_state_primary_screenshot=screenshots/s1-run-first-load-folded-desktop.png`.
- Kept all prior folded-state contract keys and exposed the canonical path through the shared payload helper in package index and package manifest outputs.
- Added unit assertions validating canonical screenshot path in package index and manifest contract payload.

## Acceptance Commands

1. `py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-126_BACKLOG_ITEM_RFB_RC016_001.md`
- PASS

2. `py -3 -m unittest backend.tests.test_build_local_offline_trial_rc`
- PASS (`Ran 7 tests`)

3. `py -3 scripts/build_local_offline_trial_rc.py --help`
- PASS

4. `git -c core.quotepath=false diff --check`
- PASS

## Safety and Boundary Check

- Local/offline package script and unittest scope only.
- No real data, no live API/connectors, no production write-back, no customer-visible deploy/output.
- No backend API/schema migration and no push.

## HOLD Check

- No HOLD condition triggered.

## Automated Review Status

- NOT_RUN in-goal (deterministic script/test evidence used).

## Next Unlock

- Run picker for follow-up backlog closeout Goal for `RFB-RC016-001`.
