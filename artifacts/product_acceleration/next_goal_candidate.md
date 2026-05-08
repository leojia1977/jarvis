# SecuPilot Next MVP Goal Candidate

Generated at: 2026-05-08T08:28:16

Selection mode: QUEUE_FALLBACK

## Candidate Goal

- queue_key: GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE
- goal_id: GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE
- goal_type: package
- statement: Align RC-016 screenshot visible candidate text, visual assertions, and screenshot safety expected candidate so package validation no longer relies on RC-014 text.

## Exact Files

- docs/goals/GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE.md
- frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
- frontend/src/App.test.tsx
- frontend/tests/e2e/s1-artifact-viewer.spec.ts
- frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
- artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan_mvp61.json
- docs/S6_FAST_MVP_GOAL_MVP_61_RC016_SCREENSHOT_EXPECTED_CANDIDATE_2026_05_08.md

## Acceptance Commands

- py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE.md
- Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
- Set-Location -LiteralPath frontend; npm run build
- Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
- py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_016_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan_mvp61.json
- git -c core.quotepath=false diff --check

## HOLD Conditions

- screenshot visible text still contains LOCAL_OFFLINE_TRIAL_RC_014_CN as current candidate
- screenshot safety expected_candidate_missing finding appears
- frontend unit/build/playwright fails twice in the same way
- scope expands beyond listed files
