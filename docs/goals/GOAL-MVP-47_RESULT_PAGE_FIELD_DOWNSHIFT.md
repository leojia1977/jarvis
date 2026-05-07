# GOAL-MVP-47_RESULT_PAGE_FIELD_DOWNSHIFT

## Goal ID

```text
GOAL-MVP-47_RESULT_PAGE_FIELD_DOWNSHIFT
```

## Goal type

```text
page
```

## Goal statement

```text
Close RC-014 backlog item RFB-RC014-002 by moving candidate/run id/data mode/provider out of first-screen emphasis on /s1-run into the technical reconciliation section while preserving reviewer traceability.
```

## Primary executable object

```text
page=/s1-run
test=frontend/src/App.test.tsx
test=frontend/tests/e2e/s1-artifact-viewer.spec.ts
test=frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
validator=scripts/validate_review_screenshots.py
validator=scripts/validate_local_trial_rc_consistency.py
closeout=docs/S6_FAST_MVP_MVP_47_RESULT_PAGE_FIELD_DOWNSHIFT_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
```

## Output paths

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/goals/GOAL-MVP-47_RESULT_PAGE_FIELD_DOWNSHIFT.md
docs/S6_FAST_MVP_MVP_47_RESULT_PAGE_FIELD_DOWNSHIFT_CLOSEOUT_2026_05_07.md
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json
artifacts/review_screenshot_safety/local-offline-trial-rc-014-cn-review/screenshot_safety_scan.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-014-cn-review/rc_consistency_check.json
artifacts/reviews/claude_code/mvp-47-current-diff-review-20260507.txt
```

## Allowed files

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/goals/GOAL-MVP-47_RESULT_PAGE_FIELD_DOWNSHIFT.md
docs/S6_FAST_MVP_MVP_47_RESULT_PAGE_FIELD_DOWNSHIFT_CLOSEOUT_2026_05_07.md
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json
artifacts/review_screenshot_safety/local-offline-trial-rc-014-cn-review/screenshot_safety_scan.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-014-cn-review/rc_consistency_check.json
artifacts/reviews/claude_code/mvp-47-current-diff-review-20260507.txt
```

## Allowed scope

```text
local/offline only
frontend /s1-run field emphasis adjustment
matching test updates
local screenshot safety and RC consistency validation
automated engineering review capture
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
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-47_RESULT_PAGE_FIELD_DOWNSHIFT.md
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-014-cn-review/screenshot_safety_scan.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_013_CN --zip-name local-offline-trial-rc-014-cn-review-package-20260507.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review-package-20260507.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-014-cn-review/rc_consistency_check.json
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
candidate/run id/data mode/provider remain emphasized in first-screen summary area
/s1-run no longer exposes technical reconciliation entry point
technical reconciliation details open by default
customer_visible_output is not false
production_writeback is not false
screenshot safety validator reports blocking finding
RC consistency validator reports blocking finding
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files only
preserve failure evidence
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
updated Playwright screenshots and text evidence
screenshot_safety_scan.json
rc_consistency_check.json
automated review artifact or REVIEW_TOOL_UNAVAILABLE_NON_BLOCKING record
closeout note with exact commands
```

## Safety sentinels

```text
no customer_visible_output=true
no production_writeback=true
no live_qwen_api=true
no live_connectors=true
no Authorization: / Bearer / refresh_token in artifacts
technical reconciliation remains closed by default
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock a dedicated backlog-closeout Goal for RFB-RC014-002 with this commit as evidence.
If PASS_WITH_NOTES, capture notes without expanding scope.
If HOLD, stop and record the blocker.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-47 result page field downshift
do not push unless separately authorized
```
