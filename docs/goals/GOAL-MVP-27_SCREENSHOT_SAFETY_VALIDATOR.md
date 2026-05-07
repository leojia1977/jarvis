# GOAL-MVP-27_SCREENSHOT_SAFETY_VALIDATOR

## Goal ID

```text
GOAL-MVP-27_SCREENSHOT_SAFETY_VALIDATOR
```

## Goal type

```text
validator
```

## Goal statement

```text
Validate reviewer-clean screenshots using PNG presence plus captured visible-text sidecars so P1/P2/P3, Mock Fixture, Expert Mode, stale RC package paths, secrets, raw payloads, and write-back text cannot pass unnoticed.
```

## Primary executable object

```text
script=scripts/validate_review_screenshots.py
test=backend/tests/test_validate_review_screenshots.py
artifact=artifacts/review_screenshot_safety/local-offline-trial-rc-009-cn-review/screenshot_safety_scan.json
closeout=docs/S6_FAST_MVP_MVP_27_SCREENSHOT_SAFETY_VALIDATOR_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/*.text.json
```

## Output paths

```text
scripts/validate_review_screenshots.py
backend/tests/test_validate_review_screenshots.py
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/goals/GOAL-MVP-27_SCREENSHOT_SAFETY_VALIDATOR.md
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/*.text.json
artifacts/review_screenshot_safety/local-offline-trial-rc-009-cn-review/screenshot_safety_scan.json
docs/S6_FAST_MVP_MVP_27_SCREENSHOT_SAFETY_VALIDATOR_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
scripts/validate_review_screenshots.py
backend/tests/test_validate_review_screenshots.py
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/goals/GOAL-MVP-27_SCREENSHOT_SAFETY_VALIDATOR.md
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/*.text.json
artifacts/review_screenshot_safety/local-offline-trial-rc-009-cn-review/screenshot_safety_scan.json
docs/S6_FAST_MVP_MVP_27_SCREENSHOT_SAFETY_VALIDATOR_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
local screenshot evidence validation
local Playwright text sidecar capture
local tests
local validation artifact
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
secrets/tokens/auth headers/raw customer logs
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-27_SCREENSHOT_SAFETY_VALIDATOR.md
py -3 -m unittest backend.tests.test_validate_review_screenshots
npx playwright test tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_009_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-009-cn-review/screenshot_safety_scan.json
```

## HOLD conditions

```text
screenshots missing or not valid PNG
text sidecar missing or route/viewport/file mismatch
expected candidate missing
P1/P2/P3 appears in reviewer-clean screenshot text
Mock Fixture or Mock Redline Fixture appears in reviewer-clean screenshot text
Expert Mode appears in reviewer-clean screenshot text
stale RC-001 through RC-007 package path appears
secret/token/auth/raw payload/write-back marker appears
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated screenshot safety scan and text sidecars only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
screenshot text sidecars
screenshot_safety_scan.json
closeout note with exact commands
```

## Safety sentinels

```text
no P1/P2/P3 in reviewer-clean screenshots
no Mock Fixture in reviewer-clean screenshots
no Expert Mode in reviewer-clean screenshots
no Authorization: / Bearer / refresh_token in artifacts
no raw_payload in artifacts
no customer_visible_output=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-28_RC_DIFF_CHECKER.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-27 screenshot safety validator
do not push unless separately authorized
```
