# GOAL-MVP-69_RECOMMENDED_ACTION_CARDS

## Goal ID

```text
GOAL-MVP-69_RECOMMENDED_ACTION_CARDS
```

## Goal type

```text
page
```

## Goal statement

```text
Deliver incident-page recommended action card content that is explicitly human-review only, local/offline safe, and verifiable by unit/e2e smoke tests.
```

## Primary executable object

```text
page=frontend/src/App.tsx
style=frontend/src/App.css
unit_test=frontend/src/App.test.tsx
playwright=frontend/tests/e2e/s1-artifact-viewer.spec.ts
playwright=frontend/tests/e2e/incident-product-page.spec.ts
artifact=artifacts/product_experience/mvp69/incident-product-desktop.png
artifact=artifacts/product_experience/mvp69/incident-product-desktop.text.json
artifact=artifacts/product_experience/mvp69/incident-product-mobile.png
artifact=artifacts/product_experience/mvp69/incident-product-mobile.text.json
closeout=docs/S6_FAST_MVP_MVP_69_RECOMMENDED_ACTION_CARD_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
frontend/src/App.tsx
frontend/src/App.css
artifacts/product_acceleration/next_goal_candidate.json
```

## Output paths

```text
docs/goals/GOAL-MVP-69_RECOMMENDED_ACTION_CARDS.md
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/incident-product-page.spec.ts
artifacts/product_experience/mvp69/incident-product-desktop.png
artifacts/product_experience/mvp69/incident-product-desktop.text.json
artifacts/product_experience/mvp69/incident-product-mobile.png
artifacts/product_experience/mvp69/incident-product-mobile.text.json
docs/S6_FAST_MVP_MVP_69_RECOMMENDED_ACTION_CARD_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-69_RECOMMENDED_ACTION_CARDS.md
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/incident-product-page.spec.ts
artifacts/product_experience/mvp69/incident-product-desktop.png
artifacts/product_experience/mvp69/incident-product-desktop.text.json
artifacts/product_experience/mvp69/incident-product-mobile.png
artifacts/product_experience/mvp69/incident-product-mobile.text.json
docs/S6_FAST_MVP_MVP_69_RECOMMENDED_ACTION_CARD_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
incident product page recommended action card copy and readonly safety attributes
incident card visual styling for desktop/mobile responsive layout
unit/e2e assertions coupled to the new card
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-69_RECOMMENDED_ACTION_CARDS.md
Set-Location -LiteralPath frontend; npm run test -- --run src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/incident-product-page.spec.ts
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
recommended action card shows autonomous execution intent
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
incident desktop/mobile screenshot evidence files under artifacts/product_experience/mvp69
git diff --check output
automated review result or REVIEW_TOOL_UNAVAILABLE_NON_BLOCKING note
```

## Safety sentinels

```text
no external tracker write
no Authorization/Bearer/refresh_token in changed files
no customer_visible_output=true
no production_writeback=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock picker-driven MVP-62 zip tamper negative test or next queued candidate.
If HOLD, stop and report failing command plus blocker evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-69 recommended action cards
stage and commit only Goal files
do not push
```
