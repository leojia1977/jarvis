# S6 Fast MVP Goal Closeout - GOAL-MVP-127 Backlog Item RFB-RC016-001

Date: 2026-05-08
Goal: GOAL-MVP-127_BACKLOG_ITEM_RFB_RC016_001
Decision: PASS

## Scope

- Keep work inside package-builder + unittest boundary for `RFB-RC016-001`.
- Add deterministic sha256 binding for folded-state primary screenshot evidence in package contracts.

## Files Changed

- docs/goals/GOAL-MVP-127_BACKLOG_ITEM_RFB_RC016_001.md
- scripts/build_local_offline_trial_rc.py
- backend/tests/test_build_local_offline_trial_rc.py
- docs/S6_FAST_MVP_GOAL_MVP_127_BACKLOG_ITEM_RFB_RC016_001_2026_05_08.md

## Implementation Summary

- Extended `required_archive_evidence_payload` to include `folded_state_primary_sha256` when the folded-state screenshot is present.
- Wired package build flow to compute sha256 from copied archive screenshot and reuse the same payload for both `PACKAGE_INDEX_中文.json` and `package_manifest.json`.
- Added unittest assertions proving screenshot hash binding is present and consistent between package index and package manifest.

## Acceptance Commands

1. `py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-127_BACKLOG_ITEM_RFB_RC016_001.md`
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

- Run picker for follow-up backlog closeout Goal for `RFB-RC016-001`.
