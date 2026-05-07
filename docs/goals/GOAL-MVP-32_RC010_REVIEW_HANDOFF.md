# GOAL-MVP-32_RC010_REVIEW_HANDOFF

## Goal ID

```text
GOAL-MVP-32_RC010_REVIEW_HANDOFF
```

## Goal type

```text
package
```

## Goal statement

```text
Build a self-contained RC-010 local/offline reviewer handoff package containing the RC package, validator results, Qwen dry UI preview evidence, and reviewer checklist.
```

## Primary executable object

```text
script=scripts/build_rc_review_handoff.py
package=artifacts/reviewer_handoffs/local-offline-trial-rc-010-cn-review-handoff
artifact=artifacts/reviewer_handoffs/local-offline-trial-rc-010-cn-review-handoff-20260507.zip
test=backend/tests/test_build_rc_review_handoff.py
closeout=docs/S6_FAST_MVP_MVP_32_RC010_REVIEW_HANDOFF_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review-package-20260507.zip
artifacts/review_screenshot_safety/local-offline-trial-rc-010-cn-review/screenshot_safety_scan.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-010-cn-review/rc_consistency_check.json
artifacts/qwen_provider_contract/mvp-31-ui-preview-validation.json
artifacts/qwen_provider_dry_ui_preview/2026-05-07/s1-qwen-dry-provider-preview.png
artifacts/qwen_provider_dry_ui_preview/2026-05-07/s1-qwen-dry-provider-preview.text.json
```

## Output paths

```text
scripts/build_rc_review_handoff.py
backend/tests/test_build_rc_review_handoff.py
docs/goals/GOAL-MVP-32_RC010_REVIEW_HANDOFF.md
artifacts/reviewer_handoffs/local-offline-trial-rc-010-cn-review-handoff/
artifacts/reviewer_handoffs/local-offline-trial-rc-010-cn-review-handoff-20260507.zip
docs/S6_FAST_MVP_MVP_32_RC010_REVIEW_HANDOFF_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
scripts/build_rc_review_handoff.py
backend/tests/test_build_rc_review_handoff.py
docs/goals/GOAL-MVP-32_RC010_REVIEW_HANDOFF.md
artifacts/reviewer_handoffs/local-offline-trial-rc-010-cn-review-handoff/**
artifacts/reviewer_handoffs/local-offline-trial-rc-010-cn-review-handoff-20260507.zip
docs/S6_FAST_MVP_MVP_32_RC010_REVIEW_HANDOFF_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
local reviewer handoff package generation
local validation artifact copying
local tests
local zip artifact
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
API keys
secrets/tokens/auth headers
live connectors
external tracker writes
production write-back
customer-visible publish/deploy/output
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-32_RC010_REVIEW_HANDOFF.md
py -3 -m unittest backend.tests.test_build_rc_review_handoff
py -3 scripts/build_rc_review_handoff.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review --package-zip artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review-package-20260507.zip --screenshot-safety-scan artifacts/review_screenshot_safety/local-offline-trial-rc-010-cn-review/screenshot_safety_scan.json --rc-consistency-check artifacts/local_trial_rc_consistency/local-offline-trial-rc-010-cn-review/rc_consistency_check.json --qwen-preview-validation artifacts/qwen_provider_contract/mvp-31-ui-preview-validation.json --qwen-preview-screenshot artifacts/qwen_provider_dry_ui_preview/2026-05-07/s1-qwen-dry-provider-preview.png --qwen-preview-text artifacts/qwen_provider_dry_ui_preview/2026-05-07/s1-qwen-dry-provider-preview.text.json --output-dir artifacts/reviewer_handoffs/local-offline-trial-rc-010-cn-review-handoff --zip-path artifacts/reviewer_handoffs/local-offline-trial-rc-010-cn-review-handoff-20260507.zip
```

## HOLD conditions

```text
RC package zip missing
RC package manifest candidate/source_candidate mismatch
screenshot safety scan status is not PASS
RC consistency check status is not PASS
Qwen dry UI preview validation status is not PASS
Qwen validation has network_call or live_qwen_api true
handoff text contains secret/token/auth/raw payload/write-back marker
handoff implies customer-visible/deploy/pilot/production authorization
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated reviewer handoff directory and zip only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
HANDOFF_MANIFEST.json
reviewer handoff zip
closeout note with exact commands
```

## Safety sentinels

```text
no live_qwen_api=true
no live_connectors=true
no production_writeback=true
no customer_visible_output=true
no Authorization: / Bearer / refresh_token in artifacts
no raw_payload in artifacts
no customer_visible_or_deploy_go=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock sending the generated local/offline handoff zip to an internal reviewer.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-32 rc010 review handoff
do not push unless separately authorized
```
