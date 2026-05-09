# GOAL-RC021-03 Local Offline GO Review Package Build

## Goal ID

```text
GOAL-RC021-03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD
```

## Goal Type

```text
package
```

## Goal Statement

```text
Generate a unique LOCAL_OFFLINE_GO_REVIEW_RC_021_CN local/offline GO review package and zip from the RC-020 package baseline, then pass package consistency and private-preview healthcheck without overwriting RC-020 artifacts.
```

## Primary Executable Object

```text
package_dir=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn
zip=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip
outer_zip_manifest=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip.outer_zip_manifest.json
consistency=artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
healthcheck=artifacts/private_preview/healthcheck/local-offline-go-review-rc-021-healthcheck.json
closeout=docs/S6_CONTROLLED_TRIAL_GOAL_RC021_03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD_2026_05_09.md
```

## Inputs

```text
docs/S6_CONTROLLED_TRIAL_GO_REVIEW_48H_MISSION_CHARTER_2026_05_09.md
artifacts/product_acceleration/controlled_trial_go_review_48h_mission_charter.json
docs/goals/GOAL-RC021-02_SCREENSHOT_TEXT_EVIDENCE_REFRESH.md
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_02_SCREENSHOT_TEXT_EVIDENCE_REFRESH_2026_05_09.md
artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review/**
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json
artifacts/local_trial_launches/local-offline-trial-rc-020/launch_info.json
```

## Output Paths

```text
docs/goals/GOAL-RC021-03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip.outer_zip_manifest.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
artifacts/private_preview/healthcheck/local-offline-go-review-rc-021-healthcheck.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD_2026_05_09.md
```

## Allowed Files

```text
docs/goals/GOAL-RC021-03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/**
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip.outer_zip_manifest.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
artifacts/private_preview/healthcheck/local-offline-go-review-rc-021-healthcheck.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD_2026_05_09.md
```

## Allowed Scope

```text
Build RC-021 GO review package using candidate LOCAL_OFFLINE_GO_REVIEW_RC_021_CN and source candidate LOCAL_OFFLINE_TRIAL_RC_020_CN.
Keep RC-020 package and zip untouched.
Validate manifest/hash/zip consistency and private-preview healthcheck readiness evidence.
Do not change product code, screenshots, or scripts in this Goal.
```

## Forbidden Scope

```text
real data
masked-real data
live Qwen/API
live connectors
production writeback
customer-visible publish/deploy/output
external pilot
production launch
secrets/tokens/auth headers/raw customer logs/raw payloads
autonomous remediation/approval/rejection/action execution
RC-020 overwrite
push
```

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-RC021-03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD.md
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_GO_REVIEW_RC_021_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-go-review-rc-021-cn --zip-path artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip --source-commit 3545b95 --repo-root . --screenshot-safety-scan artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json --outer-zip-manifest artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip.outer_zip_manifest.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-go-review-rc-021-cn --candidate LOCAL_OFFLINE_GO_REVIEW_RC_021_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --zip-name local-offline-go-review-rc-021-cn-review-package-20260509.zip --zip-path artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-review-package-20260509.zip --output-json artifacts/local_demo_packages/local-offline-go-review-rc-021-cn-consistency-check.json
py -3 scripts/check_private_preview_health.py --package-dir artifacts/local_demo_packages/local-offline-go-review-rc-021-cn --route-map artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json --launch-info artifacts/local_trial_launches/local-offline-trial-rc-020/launch_info.json --output-json artifacts/private_preview/healthcheck/local-offline-go-review-rc-021-healthcheck.json --repo-root .
git -c core.quotepath=false diff --check
```

## HOLD Conditions

```text
RC-021 package/zip generation fails or collides with existing RC-020 artifacts.
Consistency check returns HOLD or any blocking finding.
Private preview healthcheck returns HOLD.
Any current-candidate field stays RC-020 in package manifest/package index/screenshot index.
Any boundary or security sentinel violation appears in package outputs.
```

## Rollback

```text
Revert only files listed in Allowed Files.
Keep generated artifacts for audit if HOLD is hit.
Do not modify known residue files outside this Goal.
```

## Evidence Contract

```text
Goal card validator PASS
RC-021 package build PASS with zip + outer zip manifest
RC-021 consistency check PASS
RC-021 private preview healthcheck PASS
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
PASS unlock: GOAL-RC021-04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK.
HOLD behavior: report exact package/consistency/healthcheck failure and stop.
```

## Commit Posture

```text
one commit for this passing Goal
commit message: feat(secupilot): GOAL-RC021-03 local offline go review package build
do not push
```
