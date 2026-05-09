# GOAL-RC021-05 Team2 Package Boundary Review Execute

## Goal ID

```text
GOAL-RC021-05_TEAM2_PACKAGE_BOUNDARY_REVIEW_EXECUTE
```

## Goal Type

```text
package
```

## Goal Statement

```text
Execute ChatGPT Team2 package-boundary review on sanitized RC-021 material, update Team2 raw gate output, and reconcile merged gate/return-state while preserving mission boundary and Team1 pending semantics.
```

## Primary Executable Object

```text
team2_raw=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/TEAM2_PACKAGE_BOUNDARY_REVIEW_RAW.json
merged_gate=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/MERGED_REVIEW_GATE_RESULT.json
return_state=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
consistency=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
closeout=docs/S6_CONTROLLED_TRIAL_GOAL_RC021_05_TEAM2_PACKAGE_BOUNDARY_REVIEW_EXECUTE_2026_05_09.md
```

## Inputs

```text
docs/S6_CONTROLLED_TRIAL_GO_REVIEW_48H_MISSION_CHARTER_2026_05_09.md
artifacts/product_acceleration/controlled_trial_go_review_48h_mission_charter.json
docs/goals/GOAL-RC021-05_REVIEW_GATES_AND_RETURN_PACKAGE.md
artifacts/product_acceleration/rc021_customer_path_lint_and_healthcheck.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/PACKAGE_MANIFEST.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/SCREENSHOT_INDEX_中文.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/SCREENSHOT_SAFETY_SCAN.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/PRIVATE_PREVIEW_HEALTHCHECK.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/TEAM2_PACKAGE_BOUNDARY_REVIEW_RAW.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/MERGED_REVIEW_GATE_RESULT.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
```

## Output Paths

```text
docs/goals/GOAL-RC021-05_TEAM2_PACKAGE_BOUNDARY_REVIEW_EXECUTE.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/TEAM2_PACKAGE_BOUNDARY_REVIEW_RAW.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/MERGED_REVIEW_GATE_RESULT.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_05_TEAM2_PACKAGE_BOUNDARY_REVIEW_EXECUTE_2026_05_09.md
```

## Allowed Files

```text
docs/goals/GOAL-RC021-05_TEAM2_PACKAGE_BOUNDARY_REVIEW_EXECUTE.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/TEAM2_PACKAGE_BOUNDARY_REVIEW_RAW.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/MERGED_REVIEW_GATE_RESULT.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_05_TEAM2_PACKAGE_BOUNDARY_REVIEW_EXECUTE_2026_05_09.md
```

## Allowed Scope

```text
Team2 review-only boundary/governance assessment using sanitized package artifacts.
Update Team2 raw output, merged gate, and return-state fields to reflect actual Team2 result.
Keep Team1 gate independent and pending when Team1 review is unavailable.
Do not modify product code, scripts, screenshots, or package file payloads.
```

## Forbidden Scope

```text
real data
masked-real data
secrets/tokens/auth headers/raw customer logs/raw payloads
live connectors
live Qwen/API execution beyond sanitized Team2 review
production writeback
customer-visible publish/deploy/output
external pilot
production launch
autonomous remediation/approval/rejection/push
```

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-RC021-05_TEAM2_PACKAGE_BOUNDARY_REVIEW_EXECUTE.md
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-go-review-rc-021-cn --candidate LOCAL_OFFLINE_GO_REVIEW_RC_021_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --zip-name local-offline-go-review-rc-021-cn-review-package-20260509.zip --zip-path artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip --output-json artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
PowerShell assertion command: TEAM2_PACKAGE_BOUNDARY_REVIEW_RAW.json status=PASS or PASS_WITH_NOTES and blocking=false
PowerShell assertion command: MERGED_REVIEW_GATE_RESULT.json keeps merged_decision=HOLD_FOR_SPECIFIC_PRODUCT_OR_PACKAGE_FIXES while Team1 is pending
PowerShell assertion command: RETURN_STATE_PACKAGE team2_package_boundary_status synced with Team2 raw and no forbidden readiness outcome appears
git -c core.quotepath=false diff --check
```

## HOLD Conditions

```text
Team2 sanitized review detects boundary/security blocker requiring HOLD or NO_GO_SECURITY_BOUNDARY.
Any required Team2/merged/return-state field cannot be updated deterministically.
Consistency check fails.
```

## Rollback

```text
Revert only files listed in Allowed Files.
Do not touch known residue files.
```

## Evidence Contract

```text
Goal card validator PASS
Consistency check PASS
Team2 raw review status written with sanitized input set
Merged gate and return-state synchronized to Team2 result
git diff --check PASS
Closeout records exact commands and outputs
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
Stage and commit only this Goal files after all acceptance commands PASS and no HOLD condition is triggered.
Reject unrelated changes.
Do not push.
```

## Next Unlock

```text
PASS unlock: reduce external gate blockers to Team1 pending only; keep human final decision pending.
HOLD behavior: preserve HOLD/NO_GO and record exact blocker.
```

## Commit Posture

```text
one commit for this passing Goal
commit message: docs(secupilot): GOAL-RC021-05 team2 package boundary review execute
do not push
```
