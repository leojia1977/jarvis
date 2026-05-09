# GOAL-RC021-05 Return Package Metadata Reconcile

## Goal ID

```text
GOAL-RC021-05_RETURN_PACKAGE_METADATA_RECONCILE
```

## Goal Type

```text
package
```

## Goal Statement

```text
Reconcile RC-021 return-state metadata so the human-return package contains deterministic commit and zip hash evidence while preserving HOLD status for pending Team1/Team2 gates.
```

## Primary Executable Object

```text
return_state=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
goal_card=docs/goals/GOAL-RC021-05_RETURN_PACKAGE_METADATA_RECONCILE.md
closeout=docs/S6_CONTROLLED_TRIAL_GOAL_RC021_05_RETURN_PACKAGE_METADATA_RECONCILE_2026_05_09.md
```

## Inputs

```text
docs/S6_CONTROLLED_TRIAL_GO_REVIEW_48H_MISSION_CHARTER_2026_05_09.md
artifacts/product_acceleration/controlled_trial_go_review_48h_mission_charter.json
docs/goals/GOAL-RC021-05_REVIEW_GATES_AND_RETURN_PACKAGE.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/MERGED_REVIEW_GATE_RESULT.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
```

## Output Paths

```text
docs/goals/GOAL-RC021-05_RETURN_PACKAGE_METADATA_RECONCILE.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_05_RETURN_PACKAGE_METADATA_RECONCILE_2026_05_09.md
```

## Allowed Files

```text
docs/goals/GOAL-RC021-05_RETURN_PACKAGE_METADATA_RECONCILE.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_05_RETURN_PACKAGE_METADATA_RECONCILE_2026_05_09.md
```

## Allowed Scope

```text
Only reconcile deterministic metadata completeness in RC021 return-state package.
Do not change gate decisions, do not change package contents, and do not change product code or script logic.
```

## Forbidden Scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production writeback
customer-visible publish/deploy/output
external pilot
production launch
secret/token/auth header
autonomous approval/rejection
push
```

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-RC021-05_RETURN_PACKAGE_METADATA_RECONCILE.md
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-go-review-rc-021-cn --candidate LOCAL_OFFLINE_GO_REVIEW_RC_021_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --zip-name local-offline-go-review-rc-021-cn-review-package-20260509.zip --zip-path artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip --output-json artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
PowerShell assertion command: RETURN_STATE_PACKAGE executed_goal_results includes GOAL-RC021-05 commit=547cbbd and zip_sha256 equals zip file SHA256
git -c core.quotepath=false diff --check
```

## HOLD Conditions

```text
Zip file missing or hash cannot be computed.
RETURN_STATE_PACKAGE schema fields cannot be reconciled without changing gate decision semantics.
Consistency check fails after metadata update.
```

## Rollback

```text
Revert only Allowed Files in this goal.
Do not touch known residue files.
```

## Evidence Contract

```text
Goal card validator PASS
Consistency check PASS
RETURN_STATE_PACKAGE metadata assertions PASS
git diff --check PASS
Closeout notes with exact command outcomes
```

## Safety Sentinels

```text
real_data=false
masked_real_data=false
live_qwen_api=false
live_connectors=false
production_writeback=false
customer_visible_output=false
external_pilot=false
production_launch=false
push=false
```

## Merge Rule

```text
Stage and commit only this goal files after all acceptance commands PASS and no HOLD condition is triggered.
Reject unrelated changes.
Do not push.
```

## Next Unlock

```text
PASS unlock: use reconciled return-state package for human-return GO review material consumption.
HOLD behavior: keep current HOLD outcome and report exact metadata blocker.
```

## Commit Posture

```text
one commit for this passing Goal
commit message: docs(secupilot): GOAL-RC021-05 reconcile return package metadata
do not push
```

