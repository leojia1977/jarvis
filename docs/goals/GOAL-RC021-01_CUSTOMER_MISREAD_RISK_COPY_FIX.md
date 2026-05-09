# GOAL-RC021-01 Customer Misread Risk Copy Fix

## Goal ID

```text
GOAL-RC021-01_CUSTOMER_MISREAD_RISK_COPY_FIX
```

## Goal Type

```text
package
```

## Goal Statement

```text
Remove two customer-misread-risk phrases from current customer-path UI and regenerate screenshot text sidecars proving old text is gone and new text is present.
```

## Primary Executable Object

```text
ui=frontend/src/secupilot/s1/S1LocalTrialView.tsx
ui=frontend/src/App.tsx
e2e=frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
e2e=frontend/tests/e2e/incident-product-page.spec.ts
screenshots=artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/*
screenshots=artifacts/product_experience/ux04/*
scan=artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
closeout=docs/S6_CONTROLLED_TRIAL_GOAL_RC021_01_CUSTOMER_MISREAD_RISK_COPY_FIX_2026_05_09.md
```

## Inputs

```text
docs/S6_CONTROLLED_TRIAL_GO_REVIEW_48H_MISSION_CHARTER_2026_05_09.md
artifacts/product_acceleration/controlled_trial_go_review_48h_mission_charter.json
```

## Output Paths

```text
docs/goals/GOAL-RC021-01_CUSTOMER_MISREAD_RISK_COPY_FIX.md
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/App.tsx
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
frontend/tests/e2e/incident-product-page.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
artifacts/product_experience/ux04/incident-product-first-load-desktop.png
artifacts/product_experience/ux04/incident-product-first-load-desktop.text.json
artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.png
artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.text.json
artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.png
artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.text.json
artifacts/product_experience/ux04/incident-product-mobile.png
artifacts/product_experience/ux04/incident-product-mobile.text.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_01_CUSTOMER_MISREAD_RISK_COPY_FIX_2026_05_09.md
```

## Allowed Files

```text
docs/goals/GOAL-RC021-01_CUSTOMER_MISREAD_RISK_COPY_FIX.md
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/App.tsx
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
frontend/tests/e2e/incident-product-page.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
artifacts/product_experience/ux04/*
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_01_CUSTOMER_MISREAD_RISK_COPY_FIX_2026_05_09.md
```

## Allowed Scope

```text
Replace 查看部署准备 -> 查看本地接入准备 in current customer path UI.
Replace 隔离 finance-042 并锁定凭据 -> 待复核：finance-042 隔离与凭据锁定建议 in current incident queue UI.
Refresh screenshot text sidecars for /s1-trial and /incident/CASE-2847 evidence.
Keep screenshot safety scan PASS for RC-020 expected candidate while preparing RC-021 phase input evidence.
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
RC-021 package build or zip generation in this Goal
push
```

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-RC021-01_CUSTOMER_MISREAD_RISK_COPY_FIX.md
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.visual.spec.ts tests/e2e/incident-product-page.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
Get-ChildItem -LiteralPath artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright -Filter *.text.json | Select-String -SimpleMatch '查看部署准备','隔离 finance-042 并锁定凭据'
Get-ChildItem -LiteralPath artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright -Filter *.text.json | Select-String -SimpleMatch '查看本地接入准备','待复核：finance-042 隔离与凭据锁定建议'
Get-ChildItem -LiteralPath artifacts/product_experience/ux04 -Filter *.text.json | Select-String -SimpleMatch '隔离 finance-042 并锁定凭据'
Get-ChildItem -LiteralPath artifacts/product_experience/ux04 -Filter *.text.json | Select-String -SimpleMatch '待复核：finance-042 隔离与凭据锁定建议'
git -c core.quotepath=false diff --check
```

## HOLD Conditions

```text
Any refreshed screenshot text sidecar still contains 查看部署准备.
Any refreshed screenshot text sidecar still contains 隔离 finance-042 并锁定凭据.
Refreshed screenshot text sidecars do not contain 查看本地接入准备 or 待复核：finance-042 隔离与凭据锁定建议.
validate_review_screenshots returns HOLD.
Any boundary or security sentinel violation appears in refreshed sidecars.
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
Playwright visual/spec run PASS
Screenshot safety scan PASS
Text-sidecar checks proving old phrases removed and new phrases present
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
PASS unlock: GOAL-RC021-02_SCREENSHOT_TEXT_EVIDENCE_REFRESH.
HOLD behavior: report exact sidecar/screenshot assertion failure and stop.
```

## Commit Posture

```text
one commit for this passing Goal
commit message: feat(secupilot): GOAL-RC021-01 customer misread risk copy fix
do not push
```
