# GOAL-MVP-38_RC012_REVIEW_PACKAGE_AFTER_MVP36

## Goal ID

```text
GOAL-MVP-38_RC012_REVIEW_PACKAGE_AFTER_MVP36
```

## Goal type

```text
package
```

## Goal statement

```text
Build RC-012 as a Chinese local/offline reviewer package after MVP-36, proving that first-screen technical codes are hidden behind Chinese reviewer links while raw codes remain available in the closed technical reconciliation area.
```

## Primary executable object

```text
package=artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review
artifact=artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review-package-20260507.zip
validator=scripts/validate_review_screenshots.py
validator=scripts/validate_local_trial_rc_consistency.py
test=frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
closeout=docs/S6_FAST_MVP_MVP_38_RC012_REVIEW_PACKAGE_AFTER_MVP36_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-011-cn-review/
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
artifacts/review_screenshot_safety/local-offline-trial-rc-012-cn-review/screenshot_safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review-package-20260507.zip
artifacts/local_trial_rc_consistency/local-offline-trial-rc-012-cn-review/rc_consistency_check.json
docs/goals/GOAL-MVP-38_RC012_REVIEW_PACKAGE_AFTER_MVP36.md
docs/S6_FAST_MVP_MVP_38_RC012_REVIEW_PACKAGE_AFTER_MVP36_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/**
artifacts/review_screenshot_safety/local-offline-trial-rc-012-cn-review/screenshot_safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review/**
artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review-package-20260507.zip
artifacts/local_trial_rc_consistency/local-offline-trial-rc-012-cn-review/rc_consistency_check.json
docs/goals/GOAL-MVP-38_RC012_REVIEW_PACKAGE_AFTER_MVP36.md
docs/S6_FAST_MVP_MVP_38_RC012_REVIEW_PACKAGE_AFTER_MVP36_CLOSEOUT_2026_05_07.md
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-38_RC012_REVIEW_PACKAGE_AFTER_MVP36.md
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_012_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-012-cn-review/screenshot_safety_scan.json
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_012_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_011_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-011-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review-package-20260507.zip --source-commit 02fa889 --screenshot-safety-scan artifacts/review_screenshot_safety/local-offline-trial-rc-012-cn-review/screenshot_safety_scan.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_012_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_011_CN --zip-name local-offline-trial-rc-012-cn-review-package-20260507.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-012-cn-review-package-20260507.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-012-cn-review/rc_consistency_check.json
```

## HOLD conditions

```text
RC-012 screenshots do not show LOCAL_OFFLINE_TRIAL_RC_012_CN
/s1-run screenshot exposes first-screen raw technical codes instead of Chinese links
/s1-run screenshot does not expose a closed technical reconciliation entry point
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
delete generated RC-012 package directory, zip, screenshot safety scan, and consistency scan only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
RC-012 package manifest with SHA256
validation/screenshot_safety_scan.json inside package
external screenshot_safety_scan.json
external rc_consistency_check.json
RC-012 zip artifact
screenshots proving Chinese first-screen links and closed technical reconciliation
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
If PASS, unlock sending the RC-012 zip to an internal local/offline reviewer.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-38 rc012 review package
do not push unless separately authorized
```
