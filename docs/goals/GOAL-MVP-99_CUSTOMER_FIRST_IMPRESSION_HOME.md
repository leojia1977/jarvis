# GOAL-MVP-99 Customer First Impression Home

## Goal ID

GOAL-MVP-99_CUSTOMER_FIRST_IMPRESSION_HOME

## Goal Type

page

## Goal Statement

Make `/s1-trial` feel like the first customer-facing SecuPilot product home instead of an offline evidence package, using the earlier dark workbench direction as the visual reference while keeping the first screen understandable for engineers, security leaders, and CTOs.

## Primary Executable Object

page=frontend/src/secupilot/s1/S1LocalTrialView.tsx
test=frontend/src/App.test.tsx
test=frontend/tests/e2e/s1-artifact-viewer.spec.ts
closeout=docs/S6_FAST_MVP_MVP_99_CUSTOMER_FIRST_IMPRESSION_HOME_CLOSEOUT_2026_05_08.md

## Inputs

- Current `/s1-trial` private preview page.
- Current `/incident/CASE-2847` product route.
- Previous dark SecuPilot workbench visual references supplied by the user.
- Current RC-019 local/offline package metadata.
- Current MVP-80 to MVP-85 route gap concern.

## Output Paths

- docs/goals/GOAL-MVP-99_CUSTOMER_FIRST_IMPRESSION_HOME.md
- docs/S6_MVP80_85_ROUTE_RECONCILIATION_2026_05_08.md
- docs/S6_FAST_MVP_MVP_99_CUSTOMER_FIRST_IMPRESSION_HOME_CLOSEOUT_2026_05_08.md
- frontend/src/secupilot/s1/S1LocalTrialView.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx
- frontend/tests/e2e/s1-artifact-viewer.spec.ts
- artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/

## Allowed Files

- docs/goals/GOAL-MVP-99_CUSTOMER_FIRST_IMPRESSION_HOME.md
- docs/S6_MVP80_85_ROUTE_RECONCILIATION_2026_05_08.md
- docs/S6_FAST_MVP_MVP_99_CUSTOMER_FIRST_IMPRESSION_HOME_CLOSEOUT_2026_05_08.md
- frontend/src/secupilot/s1/S1LocalTrialView.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx
- frontend/tests/e2e/s1-artifact-viewer.spec.ts
- artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/

## Allowed Scope

- `/s1-trial` first-screen information architecture and visual treatment.
- Customer-readable role paths and product journey copy.
- MVP-80 to MVP-85 reconciliation note so skipped/covered items are not forgotten.
- Local frontend tests and local screenshot-capable smoke tests.

## Forbidden Scope

- No real data.
- No masked-real data.
- No live Qwen/API calls.
- No live connector or connector mutation.
- No production write-back or production writeback.
- No customer-visible publish, deploy, output, external pilot, staging, or production launch.
- No secret, token, auth header, API key, raw customer log, or raw customer payload.
- No backend API/schema migration.
- No push.

## Acceptance Commands

```powershell
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-99_CUSTOMER_FIRST_IMPRESSION_HOME.md
Set-Location -LiteralPath frontend; npm run test -- --run src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_019_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- `/s1-trial` first screen still reads mainly as an evidence package, manifest table, or technical audit desk.
- The page exposes P1/P2/P3, Mock Fixture, Expert Mode, stale RC wording, or debug controls in reviewer-facing UI.
- The first screen omits who SecuPilot is, what it judges, what the user should do now, or why the result is credible.
- UI claims customer-visible deploy, production launch, live Qwen/API, connector usage, or write-back is enabled.
- MVP-80 to MVP-85 are left ambiguous without reconciliation.
- Frontend unit/build/e2e fails twice in the same way.
- Scope expands beyond listed files.

## Rollback

- Revert the listed frontend files and MVP-99 docs.
- Preserve failing screenshots or test output if failure occurs.
- Leave existing RC packages and unrelated untracked artifacts untouched.

## Evidence Contract

- Goal-card validation output.
- Frontend unit test output.
- Frontend build output.
- Playwright smoke output for `/s1-trial`.
- Closeout report with exact command results.
- MVP-80 to MVP-85 reconciliation record.

## Safety Sentinels

- no real_data=true
- no masked_real_data=true
- no live_qwen_api=true
- no production_writeback=true
- no customer_visible_output=true
- no Authorization header
- no Bearer token
- no P1/P2/P3, Mock Fixture, Expert Mode, or stale RC wording in customer-facing first screen

## Merge Rule

May stage and commit only if all acceptance commands pass, the customer first screen is product-led, and no HOLD condition is observed. Do not push. Do not merge unrelated changes.

## Next Unlock

If PASS, unlock product work on customer-facing route depth: the workbench-style event flow can be promoted behind the new home as the main trial journey. If HOLD, stop and report the exact UI or route reconciliation blocker.

## Commit Posture

One commit for MVP-99. Stage and commit only listed files. Do not push.
