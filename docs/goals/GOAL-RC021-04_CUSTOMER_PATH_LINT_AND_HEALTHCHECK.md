# GOAL-RC021-04 Customer Path Lint And Healthcheck

## Goal ID

```text
GOAL-RC021-04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK
```

## Goal Type

```text
package
```

## Goal Statement

```text
Run deterministic customer-path lint (comprehension, boundary/misleading capability, and security exposure) against RC-021 reviewer-facing materials and screenshot text sidecars, then re-run RC-021 private-preview healthcheck for blocking readiness evidence.
```

## Primary Executable Object

```text
lint_json=artifacts/product_acceleration/rc021_customer_path_lint_and_healthcheck.json
healthcheck=artifacts/private_preview/healthcheck/local-offline-go-review-rc-021-healthcheck.json
closeout=docs/S6_CONTROLLED_TRIAL_GOAL_RC021_04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK_2026_05_09.md
```

## Inputs

```text
docs/S6_CONTROLLED_TRIAL_GO_REVIEW_48H_MISSION_CHARTER_2026_05_09.md
artifacts/product_acceleration/controlled_trial_go_review_48h_mission_charter.json
docs/goals/GOAL-RC021-03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD.md
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD_2026_05_09.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/REVIEWER_START_HERE_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/REVIEWER_CHECKLIST_中文.md
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/PACKAGE_INDEX_中文.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/SCREENSHOT_INDEX.json
artifacts/local_demo_packages/local-offline-go-review-rc-021-cn/package_manifest.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-first-load-folded-desktop.text.json
artifacts/product_experience/ux04/incident-product-first-load-desktop.text.json
artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.text.json
artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.text.json
artifacts/product_experience/ux04/incident-product-mobile.text.json
```

## Output Paths

```text
docs/goals/GOAL-RC021-04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK.md
artifacts/product_acceleration/rc021_customer_path_lint_and_healthcheck.json
artifacts/private_preview/healthcheck/local-offline-go-review-rc-021-healthcheck.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK_2026_05_09.md
```

## Allowed Files

```text
docs/goals/GOAL-RC021-04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK.md
artifacts/product_acceleration/rc021_customer_path_lint_and_healthcheck.json
artifacts/private_preview/healthcheck/local-offline-go-review-rc-021-healthcheck.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK_2026_05_09.md
```

## Allowed Scope

```text
Deterministically lint RC-021 customer path materials and screenshot text sidecars for comprehension and boundary language.
Block on any attacker-readable attack path/PoC/payload/topology reachability, real or masked-real data, secrets/tokens/auth headers/raw payload claims, backend write/production write-back/live connector/live API claims, or autonomous containment/remediation claims.
Re-run private-preview healthcheck to ensure RC-021 package readiness evidence remains PASS.
No product code, script logic, screenshot binaries, or package-builder logic changes in this Goal.
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
package rebuild or zip overwrite
push
```

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-RC021-04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK.md
PowerShell customer-path lint command -> artifacts/product_acceleration/rc021_customer_path_lint_and_healthcheck.json
py -3 scripts/check_private_preview_health.py --package-dir artifacts/local_demo_packages/local-offline-go-review-rc-021-cn --route-map artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json --launch-info artifacts/local_trial_launches/local-offline-trial-rc-020/launch_info.json --output-json artifacts/private_preview/healthcheck/local-offline-go-review-rc-021-healthcheck.json --repo-root .
PowerShell assertion command: lint_json.status=PASS and lint_json.blocking_finding_count=0 and healthcheck.status=PASS
git -c core.quotepath=false diff --check
```

## HOLD Conditions

```text
customer-path lint reports any blocking finding for exploit/PoC/payload/attacker-readable path/topology, live/production authorization intent, backend write claim, or data/secret exposure.
Any required customer-path text sidecar is missing.
private-preview healthcheck is not PASS.
Any NO_GO_SECURITY_BOUNDARY finding appears in lint or healthcheck outputs.
```

## Rollback

```text
Revert only files listed in Allowed Files.
Keep generated lint/healthcheck evidence for audit if HOLD is hit.
Do not modify known residue files outside this Goal.
```

## Evidence Contract

```text
Goal card validator PASS
Customer-path lint json generated with blocking_finding_count=0
Private-preview healthcheck PASS with blocking_finding_count=0
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
PASS unlock: GOAL-RC021-05_REVIEW_GATES_AND_RETURN_PACKAGE.
HOLD behavior: report exact lint/healthcheck blocker and stop.
```

## Commit Posture

```text
one commit for this passing Goal
commit message: feat(secupilot): GOAL-RC021-04 customer path lint and healthcheck
do not push
```
