# GOAL-MVP-71_CLOUD_QWEN_DRY_RUN_PROVIDER_UI

## Goal ID

```text
GOAL-MVP-71_CLOUD_QWEN_DRY_RUN_PROVIDER_UI
```

## Goal type

```text
page
```

## Goal statement

```text
Deliver a customer-readable cloud Qwen provider path preview on the incident page while keeping the experience dry-run only, local/offline safe, and free of live API calls or real data.
```

## Primary executable object

```text
page=frontend/src/App.tsx
style=frontend/src/App.css
unit_test=frontend/src/App.test.tsx
playwright=frontend/tests/e2e/incident-product-page.spec.ts
playwright=frontend/tests/e2e/s1-artifact-viewer.spec.ts
artifact=artifacts/product_experience/mvp71/incident-product-desktop.png
artifact=artifacts/product_experience/mvp71/incident-product-desktop.text.json
artifact=artifacts/product_experience/mvp71/incident-product-mobile.png
artifact=artifacts/product_experience/mvp71/incident-product-mobile.text.json
closeout=docs/S6_FAST_MVP_MVP_71_CLOUD_QWEN_DRY_RUN_PROVIDER_UI_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/secupilot/s1/s1QwenProviderContract.ts
frontend/src/secupilot/s1/s1QwenProviderDryPreview.ts
frontend/tests/e2e/incident-product-page.spec.ts
frontend/tests/e2e/s1-artifact-viewer.spec.ts
```

## Output paths

```text
docs/goals/GOAL-MVP-71_CLOUD_QWEN_DRY_RUN_PROVIDER_UI.md
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/incident-product-page.spec.ts
frontend/tests/e2e/s1-artifact-viewer.spec.ts
artifacts/product_experience/mvp71/incident-product-desktop.png
artifacts/product_experience/mvp71/incident-product-desktop.text.json
artifacts/product_experience/mvp71/incident-product-mobile.png
artifacts/product_experience/mvp71/incident-product-mobile.text.json
docs/S6_FAST_MVP_MVP_71_CLOUD_QWEN_DRY_RUN_PROVIDER_UI_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-71_CLOUD_QWEN_DRY_RUN_PROVIDER_UI.md
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/incident-product-page.spec.ts
frontend/tests/e2e/s1-artifact-viewer.spec.ts
artifacts/product_experience/mvp71/incident-product-desktop.png
artifacts/product_experience/mvp71/incident-product-desktop.text.json
artifacts/product_experience/mvp71/incident-product-mobile.png
artifacts/product_experience/mvp71/incident-product-mobile.text.json
docs/S6_FAST_MVP_MVP_71_CLOUD_QWEN_DRY_RUN_PROVIDER_UI_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
incident product page cloud Qwen dry-run provider UI
readonly provider mode selection and local preview state
desktop/mobile responsive styling for the provider path preview
unit/e2e assertions coupled to dry-run safety boundaries
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-71_CLOUD_QWEN_DRY_RUN_PROVIDER_UI.md
Set-Location -LiteralPath frontend; npm run test -- --run src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/incident-product-page.spec.ts
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
Qwen provider preview performs live API call, network request, connector call, backend write, artifact write, or production write-back
Qwen provider preview requires API key, secret, token, auth header, or real customer data
Qwen provider preview creates autonomous approval, rejection, closure, block, isolate, deploy, publish, or write-back action
provider UI exposes P1/P2/P3, Mock Fixture, Expert Mode, raw payload, auth, token, or private key text
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
incident desktop/mobile screenshot evidence files under artifacts/product_experience/mvp71
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no live_qwen_api=true
no network_request=true
no api_key_required=true
no real_data=true
no connector_call=true
no autonomous_qwen_action=true
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
If PASS, unlock GOAL-MVP-72_CLOUD_MODEL_CONTRACT_LATENCY_ERROR_HANDLING.
If HOLD, stop and report failing command plus blocker evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-71 cloud qwen dry-run provider UI
stage and commit only Goal files
do not push
```
