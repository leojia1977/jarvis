# GOAL-RC021-05 Review Gates And Return Package

## Goal ID

```text
GOAL-RC021-05_REVIEW_GATES_AND_RETURN_PACKAGE
```

## Goal Type

```text
package
```

## Goal Statement

```text
Assemble RC-021 controlled-trial GO review materials and return-state package, including required reviewer docs, package evidence snapshots, Team1/Team2 raw gate outputs, and merged gate status for human GO/NO-GO review after return.
```

## Primary Executable Object

```text
package_dir=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn
gate_summary=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/MERGED_REVIEW_GATE_RESULT.json
return_state=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
consistency=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
closeout=docs/S6_CONTROLLED_TRIAL_GOAL_RC021_05_REVIEW_GATES_AND_RETURN_PACKAGE_2026_05_09.md
```

## Inputs

```text
docs/S6_CONTROLLED_TRIAL_GO_REVIEW_48H_MISSION_CHARTER_2026_05_09.md
artifacts/product_acceleration/controlled_trial_go_review_48h_mission_charter.json
docs/goals/GOAL-RC021-04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK.md
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK_2026_05_09.md
artifacts/product_acceleration/rc021_customer_path_lint_and_healthcheck.json
artifacts/private_preview/healthcheck/local-offline-go-review-rc-021-healthcheck.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/package_manifest.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/SCREENSHOT_INDEX.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/validation/screenshot_safety_scan.json
```

## Output Paths

```text
docs/goals/GOAL-RC021-05_REVIEW_GATES_AND_RETURN_PACKAGE.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/GO_REVIEW_HANDOFF_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/TRIAL_SUCCESS_CRITERIA_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/NO_GO_BOUNDARY_CHECKLIST_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/KNOWN_NOTES_NOT_BLOCKERS_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/STOP_CONDITIONS_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/PACKAGE_MANIFEST.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/SCREENSHOT_INDEX_中文.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/SCREENSHOT_SAFETY_SCAN.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/PRIVATE_PREVIEW_HEALTHCHECK.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/TEAM1_PRODUCT_PATH_REVIEW_RAW.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/TEAM2_PACKAGE_BOUNDARY_REVIEW_RAW.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/MERGED_REVIEW_GATE_RESULT.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_05_REVIEW_GATES_AND_RETURN_PACKAGE_2026_05_09.md
```

## Allowed Files

```text
docs/goals/GOAL-RC021-05_REVIEW_GATES_AND_RETURN_PACKAGE.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/GO_REVIEW_HANDOFF_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/TRIAL_SUCCESS_CRITERIA_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/NO_GO_BOUNDARY_CHECKLIST_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/KNOWN_NOTES_NOT_BLOCKERS_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/STOP_CONDITIONS_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/PACKAGE_MANIFEST.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/SCREENSHOT_INDEX_中文.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/SCREENSHOT_SAFETY_SCAN.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/PRIVATE_PREVIEW_HEALTHCHECK.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/TEAM1_PRODUCT_PATH_REVIEW_RAW.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/TEAM2_PACKAGE_BOUNDARY_REVIEW_RAW.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/MERGED_REVIEW_GATE_RESULT.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/RETURN_STATE_PACKAGE.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_05_REVIEW_GATES_AND_RETURN_PACKAGE_2026_05_09.md
```

## Allowed Scope

```text
Prepare reviewer-facing controlled-trial GO review material only.
Record Team1/Team2 review gate raw outputs and merged result with explicit pending/unavailable labels when external gate execution is unavailable in this local run.
Assemble return-state package fields required by charter Phase 5.
Do not change product code, scripts, package-builder logic, screenshot binaries, or candidate package manifest entries.
```

## Forbidden Scope

```text
real data
masked-real data
live Qwen/API (except external Team2 review-only; unavailable in this run)
live connectors
production writeback
customer-visible publish/deploy/output
external pilot
production launch
secrets/tokens/auth headers/raw customer logs/raw payloads
autonomous remediation/approval/rejection/action execution
GO/HOLD/NO-GO final human decision replacement
push
```

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-RC021-05_REVIEW_GATES_AND_RETURN_PACKAGE.md
PowerShell material assembly command -> required Phase-4 files + Team1/Team2 raw outputs + merged gate json + return-state package json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-go-review-rc-021-cn --candidate LOCAL_OFFLINE_GO_REVIEW_RC_021_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --zip-name local-offline-go-review-rc-021-cn-review-package-20260509.zip --zip-path artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip --output-json artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
PowerShell assertion command: GO_REVIEW_HANDOFF_中文.md contains "建议进入人工 GO/NO-GO 评审" and excludes "建议发布/建议试点/建议客户使用"
PowerShell assertion command: all required material files exist and merged gate records TEAM1_PRODUCT_PATH_REVIEW_PENDING + TEAM2_PACKAGE_BOUNDARY_REVIEW_PENDING
git -c core.quotepath=false diff --check
```

## HOLD Conditions

```text
Required Phase-4/Phase-5 material file missing.
GO handoff contains forbidden launch wording.
Merged review gate reports HOLD or NO_GO_SECURITY_BOUNDARY.
Any boundary/security sentinel violation appears in assembled reviewer materials.
```

## Rollback

```text
Revert only files listed in Allowed Files.
Keep generated reviewer package files for audit if HOLD is hit.
Do not modify known residue files outside this Goal.
```

## Evidence Contract

```text
Goal card validator PASS
Required review materials generated
Team1/Team2 raw outputs and merged gate result generated
Return-state package generated with required fields
Handoff phrase assertion PASS (required phrase present, forbidden phrases absent)
git diff --check PASS
Closeout note with exact command outcomes and boundary checks
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
PASS unlock: mission return state summary for human review.
HOLD behavior: report exact material/gate blocker and stop.
```

## Commit Posture

```text
one commit for this passing Goal
commit message: docs(secupilot): GOAL-RC021-05 review gates and return package
do not push
```
