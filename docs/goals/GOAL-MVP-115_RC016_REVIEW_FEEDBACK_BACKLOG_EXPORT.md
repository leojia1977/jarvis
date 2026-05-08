# GOAL-MVP-115 RC016 Review Feedback Backlog Export

## Goal ID

```text
GOAL-MVP-115_RC016_REVIEW_FEEDBACK_BACKLOG_EXPORT
```

## Goal type

```text
script
```

## Goal statement

```text
Export the latest RC016 local/offline review decision into structured reviewer feedback and reviewer backlog artifacts so product acceleration can consume actionable items without parsing narrative review text.
```

## Primary executable object

```text
artifact=artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/reviewer_feedback.json
artifact=artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/reviewer_feedback.md
artifact=artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json
artifact=artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.md
closeout=docs/S6_FAST_MVP_GOAL_MVP_115_RC016_REVIEW_FEEDBACK_BACKLOG_EXPORT_2026_05_08.md
```

## Inputs

```text
docs/S6_RC016_UX02_INCIDENT_AI_ADVICE_REVIEW_DECISION_2026_05_08.md
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/package_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/evidence/final_status.json
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/evidence/safety_scan.json
scripts/export_local_reviewer_feedback.py
scripts/export_reviewer_feedback_backlog.py
```

## Output paths

```text
docs/goals/GOAL-MVP-115_RC016_REVIEW_FEEDBACK_BACKLOG_EXPORT.md
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_decision_normalized.md
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/reviewer_feedback.json
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/reviewer_feedback.md
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.md
docs/S6_FAST_MVP_GOAL_MVP_115_RC016_REVIEW_FEEDBACK_BACKLOG_EXPORT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-115_RC016_REVIEW_FEEDBACK_BACKLOG_EXPORT.md
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_decision_normalized.md
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/reviewer_feedback.json
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/reviewer_feedback.md
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.md
docs/S6_FAST_MVP_GOAL_MVP_115_RC016_REVIEW_FEEDBACK_BACKLOG_EXPORT_2026_05_08.md
```

## Allowed scope

```text
RC016 decision normalization for script-readable export only
local feedback/backlog artifact generation only
focused export script unit tests and direct script invocations
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
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-115_RC016_REVIEW_FEEDBACK_BACKLOG_EXPORT.md
py -3 -m unittest backend.tests.test_export_local_reviewer_feedback backend.tests.test_export_reviewer_feedback_backlog
py -3 scripts/export_local_reviewer_feedback.py --decision-doc artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_decision_normalized.md --package-dir artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review --output-json artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/reviewer_feedback.json --output-md artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/reviewer_feedback.md --reviewer "Jarvis / TL / Product-governance reviewer" --repo-root .
py -3 scripts/export_reviewer_feedback_backlog.py --feedback-json artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/reviewer_feedback.json --output-json artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json --output-md artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.md --repo-root .
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
normalized decision artifact drifts from RC016 decision meaning or boundaries
feedback/backlog export scripts return HOLD
exported artifacts include forbidden boundary text or customer-visible/deploy authorization
backlog export drops source references or creates malformed items
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
keep prior historical residue untouched
```

## Evidence contract

```text
goal card validator PASS output
focused unittest PASS output for two export scripts
export_local_reviewer_feedback PASS json output
export_reviewer_feedback_backlog PASS json output
diff --check PASS output
closeout report mapping outputs and boundaries
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no production_writeback=true
no customer_visible_output=true
no Authorization header
no Bearer token
no raw_payload
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock picker-driven next candidate execution (expected ECI/VFE or private-preview queue fallback) after committing this export closeout.
If HOLD, stop and report exact failing command and artifact.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-115 export rc016 feedback backlog
stage and commit only Goal files
do not push
```
