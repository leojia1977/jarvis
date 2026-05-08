# GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE

## Goal ID

```text
GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE
```

## Goal type

```text
package
```

## Goal statement

```text
Align RC-016 screenshot visible candidate text, visual assertions, and screenshot safety expected candidate so package validation no longer relies on RC-014 text.
```

## Primary executable object

```text
fixture=frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
unit_test=frontend/src/App.test.tsx
playwright=frontend/tests/e2e/s1-artifact-viewer.spec.ts
playwright=frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
screenshot_safety=artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan_mvp61.json
closeout=docs/S6_FAST_MVP_GOAL_MVP_61_RC016_SCREENSHOT_EXPECTED_CANDIDATE_2026_05_08.md
```

## Inputs

```text
artifacts/product_acceleration/next_goal_candidate.json
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
```

## Output paths

```text
docs/goals/GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE.md
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan_mvp61.json
docs/S6_FAST_MVP_GOAL_MVP_61_RC016_SCREENSHOT_EXPECTED_CANDIDATE_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE.md
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan_mvp61.json
docs/S6_FAST_MVP_GOAL_MVP_61_RC016_SCREENSHOT_EXPECTED_CANDIDATE_2026_05_08.md
```

## Allowed scope

```text
local/offline fixture metadata and candidate reconciliation only
S1 /s1-run and /s1-trial test assertions coupled to fixture updates
screenshot safety expected candidate alignment for RC-016
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE.md
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_016_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan_mvp61.json
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
screenshot visible text still contains LOCAL_OFFLINE_TRIAL_RC_014_CN as current candidate
screenshot safety expected_candidate_missing finding appears
frontend unit/build/playwright fails twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
keep generated validator artifacts for audit
do not delete failure evidence
```

## Evidence contract

```text
goal card validation output
frontend unit test output
frontend build output
playwright smoke output and refreshed screenshot text artifacts
screenshot safety validator json with expected candidate LOCAL_OFFLINE_TRIAL_RC_016_CN
automated review result captured in closeout
git diff --check output
```

## Safety sentinels

```text
no external tracker write
no Authorization/Bearer/refresh_token in generated artifacts
no raw_payload in generated artifacts
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
If PASS, unlock RC-016 package or self-review report Goal with refreshed screenshot evidence.
If HOLD, stop and record the exact failing acceptance command and blocker.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): align rc016 screenshot candidate evidence
stage and commit only Goal files
do not push
```
