# S6 Fast MVP-99 Customer First Impression Home Closeout

Date: 2026-05-08

Goal ID: GOAL-MVP-99_CUSTOMER_FIRST_IMPRESSION_HOME

Decision: PASS

## Summary

MVP-99 turns `/s1-trial` from a local/offline review package entry into a customer first-impression product home.

The first screen now follows the earlier dark SecuPilot workbench visual direction, but it serves a different job from the user's reference screenshots:

- reference screenshots: event detail and approval workbench after a user is already inside the product
- MVP-99 `/s1-trial`: product entry page that explains SecuPilot, what it judges, what to do now, and why the result can be trusted

Technical package paths, candidate codes, and artifact evidence remain available below the first screen or inside technical reconciliation areas, but they are no longer the main first-impression content.

## MVP-80 to MVP-85 Handling

Created:

- `docs/S6_MVP80_85_ROUTE_RECONCILIATION_2026_05_08.md`

Decision:

- Do not reopen MVP-80 to MVP-85 just to preserve numbering.
- Treat them as covered, superseded, or optional follow-up based on current MVP-73 to MVP-94 work.
- If a missing capability becomes real later, create a new current executable Goal instead of backfilling stale numbering.

## Executable Objects Delivered

- page: `frontend/src/secupilot/s1/S1LocalTrialView.tsx`
- styles: `frontend/src/App.css`
- tests: `frontend/src/App.test.tsx`
- e2e: `frontend/tests/e2e/s1-artifact-viewer.spec.ts`
- route reconciliation: `docs/S6_MVP80_85_ROUTE_RECONCILIATION_2026_05_08.md`
- goal card: `docs/goals/GOAL-MVP-99_CUSTOMER_FIRST_IMPRESSION_HOME.md`

## Product Changes

- Added a dark customer product home shell to `/s1-trial`.
- Added a first-impression command card that says the first screen is for product judgment, not evidence directories.
- Added a product preview queue for:
  - suspicious lateral movement incident
  - Qwen synthetic provider path
  - Windows private preview delivery boundary
- Kept role paths for:
  - engineer
  - analysis lead
  - security lead
  - CTO / deployment lead
- Downshifted long technical candidate text from first-screen status cards.
- Kept local/offline boundaries visible and machine-testable.

## Verification

```powershell
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-99_CUSTOMER_FIRST_IMPRESSION_HOME.md
```

Result: PASS

```powershell
Set-Location -LiteralPath frontend; npm run test -- --run src/App.test.tsx
```

Result: PASS, 63 tests

```powershell
Set-Location -LiteralPath frontend; npm run build
```

Result: PASS

```powershell
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts
```

Result: PASS, 4 tests

```powershell
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.visual.spec.ts
```

Result: PASS, 4 tests

```powershell
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_019_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
```

Result: PASS, `blocking_finding_count=0`, `warning_count=0`

## Screenshot Check

Reviewed:

- `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png`

Observation:

- First screen now reads as a product home/control console.
- It visually aligns more closely with the earlier dark SecuPilot workbench direction.
- It is less dense than the reference workbench screenshots because a homepage must orient new users before event/approval details.

## Boundaries Preserved

- No real data.
- No masked-real data.
- No live Qwen/API calls.
- No connectors.
- No API keys, secrets, tokens, auth headers, raw customer logs, or raw customer payloads.
- No production write-back.
- No customer-visible publish/deploy/output.
- No external pilot.
- No production launch.
- No backend API/schema migration.
- No push.

## Next

The automation queue remains pointed at:

- `GOAL-MVP-95_PRIVATE_PREVIEW_LAUNCH_SHELL`

Human/product lane can continue with:

- deeper workbench-style homepage refinement
- event journey polish behind the homepage
- private preview package refresh after current page changes
