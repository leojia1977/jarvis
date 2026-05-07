# GOAL-MVP-41_RC013_REVIEW_PACKAGE_AFTER_MVP39

## Goal ID

```text
GOAL-MVP-41_RC013_REVIEW_PACKAGE_AFTER_MVP39
```

## Goal type

```text
package
```

## Goal statement

```text
Build RC-013 as a Chinese local/offline reviewer package after MVP-39, proving that the /s1-run technical reconciliation entry has Chinese explanatory copy and remains closed by default.
```

## Primary executable object

```text
package=artifacts/local_demo_packages/local-offline-trial-rc-013-cn-review
artifact=artifacts/local_demo_packages/local-offline-trial-rc-013-cn-review-package-20260507.zip
validator=scripts/validate_review_screenshots.py
validator=scripts/validate_local_trial_rc_consistency.py
test=frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
closeout=docs/S6_FAST_MVP_MVP_41_RC013_REVIEW_PACKAGE_AFTER_MVP39_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review/
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/secupilot/s1/S1ArtifactView.tsx
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/
scripts/build_local_offline_trial_rc.py
scripts/validate_review_screenshots.py
scripts/validate_local_trial_rc_consistency.py
```

## Output paths

```text
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/**
artifacts/review_screenshot_safety/local-offline-trial-rc-013-cn-review/screenshot_safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-013-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-013-cn-review-package-20260507.zip
artifacts/local_trial_rc_consistency/local-offline-trial-rc-013-cn-review/rc_consistency_check.json
docs/goals/GOAL-MVP-41_RC013_REVIEW_PACKAGE_AFTER_MVP39.md
docs/S6_FAST_MVP_MVP_41_RC013_REVIEW_PACKAGE_AFTER_MVP39_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/**
artifacts/review_screenshot_safety/local-offline-trial-rc-013-cn-review/screenshot_safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-013-cn-review/**
artifacts/local_demo_packages/local-offline-trial-rc-013-cn-review-package-20260507.zip
artifacts/local_trial_rc_consistency/local-offline-trial-rc-013-cn-review/rc_consistency_check.json
docs/goals/GOAL-MVP-41_RC013_REVIEW_PACKAGE_AFTER_MVP39.md
docs/S6_FAST_MVP_MVP_41_RC013_REVIEW_PACKAGE_AFTER_MVP39_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
local package generation
local screenshot capture
local screenshot safety validation
local RC consistency validation
local tests
local reviewer handoff artifacts
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-41_RC013_REVIEW_PACKAGE_AFTER_MVP39.md
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_013_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-013-cn-review/screenshot_safety_scan.json
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_013_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_012_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-013-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-013-cn-review-package-20260507.zip --source-commit 448e995 --screenshot-safety-scan artifacts/review_screenshot_safety/local-offline-trial-rc-013-cn-review/screenshot_safety_scan.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-013-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_013_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_012_CN --zip-name local-offline-trial-rc-013-cn-review-package-20260507.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-013-cn-review-package-20260507.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-013-cn-review/rc_consistency_check.json
```

## HOLD conditions

```text
RC-013 screenshots do not show LOCAL_OFFLINE_TRIAL_RC_013_CN
/s1-run screenshot does not show the technical reconciliation explanatory copy
/s1-run screenshot opens technical reconciliation by default
screenshot safety scan has blocking findings
package manifest missing SHA256
package manifest omits validation/screenshot_safety_scan.json
candidate/source_candidate/package_dir/zip_name inconsistent
stale unexpected RC candidate or package slug appears
safety_scan finding_count > 0
customer_visible_output != false
production_writeback != false
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated RC-013 package directory, zip, screenshot safety scan, and consistency scan only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
RC-013 package manifest with SHA256
validation/screenshot_safety_scan.json inside package
external screenshot_safety_scan.json
external rc_consistency_check.json
RC-013 zip artifact
screenshots proving the technical reconciliation explainer and closed details
closeout note with exact commands
```

## Safety sentinels

```text
no P1/P2/P3 in reviewer-clean screenshots
no Mock Fixture in reviewer-clean screenshots
no Expert Mode in reviewer-clean screenshots
no unexpected LOCAL_OFFLINE_TRIAL_RC token in reviewer docs or package indexes
no Authorization: / Bearer / refresh_token in artifacts
no writeback_enabled=true
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
If PASS, unlock sending the RC-013 zip to an internal local/offline reviewer.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-41 rc013 review package
do not push unless separately authorized
```
