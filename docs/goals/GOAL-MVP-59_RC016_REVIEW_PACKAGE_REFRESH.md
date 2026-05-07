# GOAL-MVP-59_RC016_REVIEW_PACKAGE_REFRESH

## Goal ID

```text
GOAL-MVP-59_RC016_REVIEW_PACKAGE_REFRESH
```

## Goal type

```text
package
```

## Goal statement

```text
Build the next local/offline RC-016 review package after recent UI/product changes, with refreshed Playwright visual evidence, screenshot safety scan, and RC consistency validation.
```

## Primary executable object

```text
package=artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review
artifact=artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review-package-20260508.zip
validator=scripts/validate_review_screenshots.py
validator=scripts/validate_local_trial_rc_consistency.py
test=backend/tests/test_build_local_offline_trial_rc.py
test=frontend/tests/e2e/s1-artifact-viewer.spec.ts
test=frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
closeout=docs/S6_FAST_MVP_MVP_59_RC016_REVIEW_PACKAGE_REFRESH_2026_05_08.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright
scripts/build_local_offline_trial_rc.py
scripts/validate_review_screenshots.py
scripts/validate_local_trial_rc_consistency.py
backend/tests/test_build_local_offline_trial_rc.py
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
```

## Output paths

```text
docs/goals/GOAL-MVP-59_RC016_REVIEW_PACKAGE_REFRESH.md
docs/S6_FAST_MVP_MVP_59_RC016_REVIEW_PACKAGE_REFRESH_2026_05_08.md
artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/**
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review-package-20260508.zip
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review-package-20260508.zip.outer_zip_manifest.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-016-cn-review/rc_consistency_check.json
artifacts/reviews/claude_code/mvp-59-current-diff-review-20260508.txt
```

## Allowed files

```text
docs/goals/GOAL-MVP-59_RC016_REVIEW_PACKAGE_REFRESH.md
docs/S6_FAST_MVP_MVP_59_RC016_REVIEW_PACKAGE_REFRESH_2026_05_08.md
artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/**
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review-package-20260508.zip
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review-package-20260508.zip.outer_zip_manifest.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-016-cn-review/rc_consistency_check.json
artifacts/reviews/claude_code/mvp-59-current-diff-review-20260508.txt
```

## Allowed scope

```text
local/offline only
local package generation
local Playwright screenshot refresh
local screenshot safety validation
local RC consistency validation
local automated review evidence capture
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
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-59_RC016_REVIEW_PACKAGE_REFRESH.md
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan.json
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_016_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review-package-20260508.zip --source-commit 15f3f14 --repo-root . --screenshot-safety-scan artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_016_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --zip-name local-offline-trial-rc-016-cn-review-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review-package-20260508.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-016-cn-review/rc_consistency_check.json
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
Playwright screenshot refresh fails twice with the same error
screenshot safety scan reports blocking findings
build_local_offline_trial_rc.py fails to produce RC-016 package or zip
outer zip manifest missing or hash fields invalid
RC consistency validator reports blocking findings
candidate/source_candidate/zip metadata mismatch
local/offline boundary fields flip to true
automated review tool invocation fails and local validations are not complete
```

## Rollback

```text
revert only files listed in Allowed files
delete only RC-016 artifacts created by this goal
preserve failure logs and command output references in closeout
```

## Evidence contract

```text
goal card validator output
backend package-builder unit test output
Playwright screenshot refresh output
screenshot safety scan JSON
RC-016 package directory and zip
outer zip manifest JSON
RC consistency JSON
automated review artifact or REVIEW_TOOL_UNAVAILABLE_NON_BLOCKING record
closeout note with exact commands and PASS/HOLD status
```

## Safety sentinels

```text
no Authorization: / Bearer / refresh_token markers in generated artifacts
no raw_payload markers in reviewer-facing docs
customer_visible_output remains false in package manifest
production_writeback remains false in package manifest
no push
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not stage unrelated historical RC zip files.
```

## Next unlock

```text
If PASS, unlock RC-016 decision recording and reviewer_backlog export when reviewer feedback arrives.
If HOLD, stop and report exact blocker with artifact paths.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-59 build rc016 review package
do not push unless separately authorized
```
