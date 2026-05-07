# S6 Fast MVP MVP-27 Screenshot Safety Validator Closeout

Date: 2026-05-07

Goal ID: GOAL-MVP-27_SCREENSHOT_SAFETY_VALIDATOR

Decision: PASS_WITH_NOTES

## Scope

MVP-27 turns the RC-007 UI/package failure mode into a machine check.

The validator checks local/offline reviewer screenshots and their visible-text sidecars for:

- P1 / P2 / P3 debug role labels
- Mock Fixture / Mock Redline Fixture text
- Expert Mode text
- stale RC-001 through RC-007 candidate/package wording
- rc-004 stale package references
- obvious secret/token/auth markers
- raw payload / write-back marker text

This closeout does not authorize real data, masked-real data, live Qwen/API calls, live connectors, customer-visible publish/deploy, production write-back, backend API/schema migration, or autonomous Qwen action.

## Executable Objects

- Goal card: `docs/goals/GOAL-MVP-27_SCREENSHOT_SAFETY_VALIDATOR.md`
- Validator: `scripts/validate_review_screenshots.py`
- Unit tests: `backend/tests/test_validate_review_screenshots.py`
- Screenshot text evidence sidecars:
  - `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.text.json`
  - `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.text.json`
  - `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json`
  - `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json`
- Scan artifact: `artifacts/review_screenshot_safety/local-offline-trial-rc-009-cn-review/screenshot_safety_scan.json`

## Verification

Command:

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-MVP-27_SCREENSHOT_SAFETY_VALIDATOR.md
```

Result: PASS

Command:

```powershell
py -3 -m unittest backend.tests.test_validate_review_screenshots
```

Result: PASS, 4 tests

Command:

```powershell
npx playwright test tests/e2e/s1-artifact-viewer.visual.spec.ts
```

Workdir: `frontend`

Result: PASS, 4 tests

Command:

```powershell
py -3 scripts\validate_review_screenshots.py --screenshot-dir artifacts\s1_closed_shadow_runs\2026-04-30-001\playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_009_CN --output-json artifacts\review_screenshot_safety\local-offline-trial-rc-009-cn-review\screenshot_safety_scan.json
```

Result: PASS_WITH_NOTES

## Scan Result

Checked screenshots: 4

Blocking finding count: 0

Warning count: 2

Warnings:

- `s1-trial-desktop.png` includes the known non-blocking source-candidate phrase `RC-008 中文评审包`
- `s1-trial-mobile.png` includes the known non-blocking source-candidate phrase `RC-008 中文评审包`

This matches the RC-009 reviewer note: the phrase is a source-candidate reference, not stale current-candidate or package-path drift.

## HOLD Behavior

The validator returns HOLD if any screenshot visible text includes blocked debug, stale-RC, secret/auth, raw-payload, or write-back markers.

The validator returns PASS_WITH_NOTES for the RC-008 source-candidate phrase only, so the current package can proceed while leaving the cleanup visible for the next RC.

## Next Unlock

MVP-27 unlocks use of screenshot safety validation in future local/offline RC package checks.

Recommended next item:

- GOAL-MVP-28_RC_DIFF_CHECKER

