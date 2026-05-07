# GOAL-MVP-29_RC010_PACKAGE_WITH_VALIDATORS

## Goal ID

```text
GOAL-MVP-29_RC010_PACKAGE_WITH_VALIDATORS
```

## Goal type

```text
package
```

## Goal statement

```text
Build RC-010 as a Chinese local/offline reviewer package that includes screenshot safety validation and passes RC package consistency validation before handoff.
```

## Primary executable object

```text
package=artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review
artifact=artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review-package-20260507.zip
script=scripts/build_local_offline_trial_rc.py
validator=scripts/validate_review_screenshots.py
validator=scripts/validate_local_trial_rc_consistency.py
test=backend/tests/test_build_local_offline_trial_rc.py
closeout=docs/S6_FAST_MVP_MVP_29_RC010_PACKAGE_WITH_VALIDATORS_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
scripts/validate_review_screenshots.py
scripts/validate_local_trial_rc_consistency.py
```

## Output paths

```text
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/**
artifacts/review_screenshot_safety/local-offline-trial-rc-010-cn-review/screenshot_safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review-package-20260507.zip
artifacts/local_trial_rc_consistency/local-offline-trial-rc-010-cn-review/rc_consistency_check.json
docs/goals/GOAL-MVP-29_RC010_PACKAGE_WITH_VALIDATORS.md
docs/S6_FAST_MVP_MVP_29_RC010_PACKAGE_WITH_VALIDATORS_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/**
artifacts/review_screenshot_safety/local-offline-trial-rc-010-cn-review/screenshot_safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review/**
artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review-package-20260507.zip
artifacts/local_trial_rc_consistency/local-offline-trial-rc-010-cn-review/rc_consistency_check.json
docs/goals/GOAL-MVP-29_RC010_PACKAGE_WITH_VALIDATORS.md
docs/S6_FAST_MVP_MVP_29_RC010_PACKAGE_WITH_VALIDATORS_CLOSEOUT_2026_05_07.md
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
live connectors
production write-back
customer-visible publish/deploy/output
secrets/tokens/auth headers/raw customer logs
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-29_RC010_PACKAGE_WITH_VALIDATORS.md
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
npm run test -- src/App.test.tsx
npm run build
npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_010_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-010-cn-review/screenshot_safety_scan.json
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_010_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_009_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review-package-20260507.zip --source-commit 069afd0 --screenshot-safety-scan artifacts/review_screenshot_safety/local-offline-trial-rc-010-cn-review/screenshot_safety_scan.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_010_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_009_CN --zip-name local-offline-trial-rc-010-cn-review-package-20260507.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review-package-20260507.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-010-cn-review/rc_consistency_check.json
```

## HOLD conditions

```text
RC-010 screenshots do not show LOCAL_OFFLINE_TRIAL_RC_010_CN
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
delete generated RC-010 package directory, zip, screenshot safety scan, and consistency scan only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
RC-010 package manifest with SHA256
validation/screenshot_safety_scan.json inside package
external screenshot_safety_scan.json
external rc_consistency_check.json
RC-010 zip artifact
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
If PASS, unlock GOAL-MVP-30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG and GOAL-MVP-31_QWEN_DRY_PROVIDER_UI_PREVIEW.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-29 rc010 package validators
do not push unless separately authorized
```
