# GOAL-MVP-28_RC_DIFF_CHECKER

## Goal ID

```text
GOAL-MVP-28_RC_DIFF_CHECKER
```

## Goal type

```text
validator
```

## Goal statement

```text
Validate that a local/offline RC package is internally consistent across candidate, source_candidate, package_dir, zip_name, reviewer docs, package indexes, screenshots, and manifest SHA256 values.
```

## Primary executable object

```text
script=scripts/validate_local_trial_rc_consistency.py
test=backend/tests/test_validate_local_trial_rc_consistency.py
artifact=artifacts/local_trial_rc_consistency/local-offline-trial-rc-009-cn-review/rc_consistency_check.json
closeout=docs/S6_FAST_MVP_MVP_28_RC_DIFF_CHECKER_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review-package-20260507.zip
```

## Output paths

```text
scripts/validate_local_trial_rc_consistency.py
backend/tests/test_validate_local_trial_rc_consistency.py
docs/goals/GOAL-MVP-28_RC_DIFF_CHECKER.md
artifacts/local_trial_rc_consistency/local-offline-trial-rc-009-cn-review/rc_consistency_check.json
docs/S6_FAST_MVP_MVP_28_RC_DIFF_CHECKER_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
scripts/validate_local_trial_rc_consistency.py
backend/tests/test_validate_local_trial_rc_consistency.py
docs/goals/GOAL-MVP-28_RC_DIFF_CHECKER.md
artifacts/local_trial_rc_consistency/local-offline-trial-rc-009-cn-review/rc_consistency_check.json
docs/S6_FAST_MVP_MVP_28_RC_DIFF_CHECKER_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
local RC package consistency validation
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-28_RC_DIFF_CHECKER.md
py -3 -m unittest backend.tests.test_validate_local_trial_rc_consistency
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_009_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_008_CN --zip-name local-offline-trial-rc-009-cn-review-package-20260507.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review-package-20260507.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-009-cn-review/rc_consistency_check.json
```

## HOLD conditions

```text
candidate/source_candidate mismatch across package_manifest, PACKAGE_INDEX, or SCREENSHOT_INDEX
package_dir mismatch across package_manifest or PACKAGE_INDEX
zip_name mismatch across package_manifest, PACKAGE_INDEX, or zip path
required evidence, reviewer doc, screenshot, or manifest entry missing
manifest SHA256 mismatch
stale unexpected RC candidate token appears
stale unexpected package slug appears
boundary field is not false
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated rc_consistency_check.json only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
rc_consistency_check.json
closeout note with exact commands
```

## Safety sentinels

```text
no unexpected LOCAL_OFFLINE_TRIAL_RC token in reviewer docs or package indexes
no unexpected local-offline-trial-rc package slug in reviewer docs or package indexes
no missing package manifest SHA256
no boundary field true
no Authorization: / Bearer / refresh_token in artifacts
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
If PASS, unlock the next exact GOAL-* selected by product route.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-28 local trial rc diff checker
do not push unless separately authorized
```
