# GOAL-MVP-49_CASE_TITLE_CLEANUP

## Goal ID

```text
GOAL-MVP-49_CASE_TITLE_CLEANUP
```

## Goal type

```text
package
```

## Goal statement

```text
Close RC-014 backlog item RFB-RC014-001 by downshifting the UAT-19 synthetic P3 case title/summary wording in package-facing evidence only, while preserving local/offline boundaries.
```

## Primary executable object

```text
script=scripts/build_local_offline_trial_rc.py
test=backend/tests/test_build_local_offline_trial_rc.py
artifact=artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review/evidence/case_summary.json
artifact=artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-package-20260507.zip
closeout=docs/S6_FAST_MVP_MVP_49_CASE_TITLE_CLEANUP_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/evidence/case_summary.json
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
```

## Output paths

```text
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
docs/goals/GOAL-MVP-49_CASE_TITLE_CLEANUP.md
docs/S6_FAST_MVP_MVP_49_CASE_TITLE_CLEANUP_CLOSEOUT_2026_05_07.md
artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review/**
artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-package-20260507.zip
artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review/rc_consistency_check.json
artifacts/reviews/claude_code/mvp-49-current-diff-review-20260507.txt
```

## Allowed files

```text
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
docs/goals/GOAL-MVP-49_CASE_TITLE_CLEANUP.md
docs/S6_FAST_MVP_MVP_49_CASE_TITLE_CLEANUP_CLOSEOUT_2026_05_07.md
artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review/**
artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-package-20260507.zip
artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review/rc_consistency_check.json
artifacts/reviews/claude_code/mvp-49-current-diff-review-20260507.txt
```

## Allowed scope

```text
local/offline only
package-facing evidence copy cleanup for UAT-19 wording
targeted package-builder tests
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-49_CASE_TITLE_CLEANUP.md
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan.json
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-package-20260507.zip --source-commit 90909f6 --repo-root . --screenshot-safety-scan artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --zip-name local-offline-trial-rc-015-cn-review-package-20260507.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-package-20260507.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review/rc_consistency_check.json
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
package-facing case_summary still contains "P3 manager summary without host raw evidence"
wording cleanup changes non-UAT-19 case semantics
build_local_offline_trial_rc.py fails twice in the same way
screenshot safety validator reports blocking findings
RC consistency validator reports blocking findings
any boundary flips to true
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
updated rc-015 package and zip
updated screenshot_safety_scan.json and rc_consistency_check.json
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
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock a follow-up backlog closeout Goal for RFB-RC014-001 with this commit evidence.
If PASS_WITH_NOTES, capture notes without expanding scope.
If HOLD, stop and report blocker.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-49 case title cleanup
do not push unless separately authorized
```
