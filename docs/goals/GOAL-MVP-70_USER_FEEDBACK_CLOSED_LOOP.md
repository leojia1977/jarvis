# GOAL-MVP-70_USER_FEEDBACK_CLOSED_LOOP

## Goal ID

```text
GOAL-MVP-70_USER_FEEDBACK_CLOSED_LOOP
```

## Goal type

```text
page
```

## Goal statement

```text
Deliver a product-grade local feedback loop on the incident recommendation page so reviewers can mark whether the recommendation is accurate, useful, and missing required information.
```

## Primary executable object

```text
page=frontend/src/App.tsx
style=frontend/src/App.css
unit_test=frontend/src/App.test.tsx
playwright=frontend/tests/e2e/incident-product-page.spec.ts
playwright=frontend/tests/e2e/s1-artifact-viewer.spec.ts
artifact=artifacts/product_experience/mvp70/incident-product-desktop.png
artifact=artifacts/product_experience/mvp70/incident-product-desktop.text.json
artifact=artifacts/product_experience/mvp70/incident-product-mobile.png
artifact=artifacts/product_experience/mvp70/incident-product-mobile.text.json
closeout=docs/S6_FAST_MVP_MVP_70_USER_FEEDBACK_CLOSED_LOOP_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/tests/e2e/incident-product-page.spec.ts
frontend/tests/e2e/s1-artifact-viewer.spec.ts
```

## Output paths

```text
docs/goals/GOAL-MVP-70_USER_FEEDBACK_CLOSED_LOOP.md
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/incident-product-page.spec.ts
frontend/tests/e2e/s1-artifact-viewer.spec.ts
artifacts/product_experience/mvp70/incident-product-desktop.png
artifacts/product_experience/mvp70/incident-product-desktop.text.json
artifacts/product_experience/mvp70/incident-product-mobile.png
artifacts/product_experience/mvp70/incident-product-mobile.text.json
docs/S6_FAST_MVP_MVP_70_USER_FEEDBACK_CLOSED_LOOP_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-70_USER_FEEDBACK_CLOSED_LOOP.md
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/incident-product-page.spec.ts
frontend/tests/e2e/s1-artifact-viewer.spec.ts
artifacts/product_experience/mvp70/incident-product-desktop.png
artifacts/product_experience/mvp70/incident-product-desktop.text.json
artifacts/product_experience/mvp70/incident-product-mobile.png
artifacts/product_experience/mvp70/incident-product-mobile.text.json
docs/S6_FAST_MVP_MVP_70_USER_FEEDBACK_CLOSED_LOOP_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
incident product page local feedback controls
readonly local preview generation for recommendation feedback
desktop/mobile responsive styling for the feedback loop
unit/e2e assertions coupled to the feedback loop
docs-only closeout evidence for this Goal
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
API keys
secrets/tokens/auth headers/raw customer logs
live connectors
production write-back
customer-visible publish/deploy/output
external pilot
production launch
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-70_USER_FEEDBACK_CLOSED_LOOP.md
Set-Location -LiteralPath frontend; npm run test -- --run src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/incident-product-page.spec.ts
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
feedback loop performs backend write, artifact write, connector call, or Qwen API call
feedback loop exposes P1/P2/P3, Mock Fixture, Expert Mode, raw payload, auth, token, or private key text
feedback loop creates an approve, deploy, publish, isolate, block, close, or write-back action
incident page tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
keep failed test outputs for audit
```

## Evidence contract

```text
goal card validator output
frontend App.test output
frontend build output
playwright smoke output for /incident and /s1 routes
incident desktop/mobile screenshot evidence files under artifacts/product_experience/mvp70
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no backend_write=true
no artifact_write=true
no qwen_api_call=true
no connector_call=true
no customer_visible_output=true
no production_writeback=true
no Authorization/Bearer/refresh_token in changed files
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-71_CLOUD_QWEN_DRY_RUN_PROVIDER_UI.
If HOLD, stop and report failing command plus blocker evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-70 user feedback closed loop
stage and commit only Goal files
do not push
```
