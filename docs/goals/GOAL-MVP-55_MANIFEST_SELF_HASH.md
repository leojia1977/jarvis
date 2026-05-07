# GOAL-MVP-55_MANIFEST_SELF_HASH

## Goal ID

```text
GOAL-MVP-55_MANIFEST_SELF_HASH
```

## Goal type

```text
script
```

## Goal statement

```text
Add manifest_self_sha256 support to the local/offline RC package builder so package manifests can self-attest deterministic integrity metadata without changing product UI behavior.
```

## Primary executable object

```text
script=scripts/build_local_offline_trial_rc.py
test=backend/tests/test_build_local_offline_trial_rc.py
closeout=docs/S6_FAST_MVP_MVP_55_MANIFEST_SELF_HASH_2026_05_08.md
```

## Inputs

```text
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review
artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan.json
```

## Output paths

```text
docs/goals/GOAL-MVP-55_MANIFEST_SELF_HASH.md
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
docs/S6_FAST_MVP_MVP_55_MANIFEST_SELF_HASH_2026_05_08.md
artifacts/reviews/claude_code/mvp-55-current-diff-review-20260508.txt
artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review-mvp55/rc_consistency_check_mvp55.json
artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review-mvp55/screenshot_safety_scan_mvp55.json
```

## Allowed files

```text
docs/goals/GOAL-MVP-55_MANIFEST_SELF_HASH.md
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
docs/S6_FAST_MVP_MVP_55_MANIFEST_SELF_HASH_2026_05_08.md
artifacts/reviews/claude_code/mvp-55-current-diff-review-20260508.txt
artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review-mvp55/rc_consistency_check_mvp55.json
artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review-mvp55/screenshot_safety_scan_mvp55.json
```

## Allowed scope

```text
local/offline only
package-builder script and unit tests only
local command verification only
no product UI text or route changes
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-55_MANIFEST_SELF_HASH.md
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review --screenshot-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review/screenshots --output-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp55 --zip-path artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp55-package-20260508.zip --source-commit 137da34 --screenshot-safety-scan artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp55 --candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --zip-name local-offline-trial-rc-015-cn-review-mvp55-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp55-package-20260508.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review-mvp55/rc_consistency_check_mvp55.json
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review-mvp55/screenshot_safety_scan_mvp55.json
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
manifest_self_sha256 missing in generated package_manifest.json
manifest_self_sha256 format is not 64-char lowercase hex
builder mutation changes package boundaries or reviewer-facing route semantics
unit test fails twice in the same way
consistency or screenshot safety validators report blocking findings
```

## Rollback

```text
revert changed files listed in Allowed files only
preserve failure evidence and command output
do not hide failed evidence
```

## Evidence contract

```text
goal card validator output
unit test output
real builder invocation output including manifest_self_sha256
rc consistency validation json
screenshot safety validation json
automated review artifact or REVIEW_TOOL_UNAVAILABLE_NON_BLOCKING record
closeout note with exact commands and results
```

## Safety sentinels

```text
no external network dependency required for acceptance
no Authorization: / Bearer / refresh_token markers in new artifacts
no raw_payload markers in generated package docs
all local/offline boundaries remain false
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not stage unrelated historical RC zip files.
```

## Next unlock

```text
If PASS, unlock either reviewer-driven package refresh or GOAL-MVP-NEXT_GOAL_PICKER for the next queue run.
If HOLD, stop and report exact blocker with evidence artifact paths.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-55 add manifest self hash
do not push unless separately authorized
```
