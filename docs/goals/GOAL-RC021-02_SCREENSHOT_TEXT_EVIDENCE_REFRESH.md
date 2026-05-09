# GOAL-RC021-02 Screenshot Text Evidence Refresh

## Goal ID

```text
GOAL-RC021-02_SCREENSHOT_TEXT_EVIDENCE_REFRESH
```

## Goal Type

```text
package
```

## Goal Statement

```text
Refresh or explicitly reuse-with-hash-match the current 7-path customer review screenshots and text sidecars, and produce deterministic evidence for folded-default and expanded AI-source assertions before RC-021 package build.
```

## Primary Executable Object

```text
e2e=frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
e2e=frontend/tests/e2e/incident-product-page.spec.ts
screenshots=artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/*
screenshots=artifacts/product_experience/ux04/*
scan=artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
evidence=artifacts/product_acceleration/rc021_screenshot_text_evidence_refresh.json
closeout=docs/S6_CONTROLLED_TRIAL_GOAL_RC021_02_SCREENSHOT_TEXT_EVIDENCE_REFRESH_2026_05_09.md
```

## Inputs

```text
docs/S6_CONTROLLED_TRIAL_GO_REVIEW_48H_MISSION_CHARTER_2026_05_09.md
artifacts/product_acceleration/controlled_trial_go_review_48h_mission_charter.json
docs/goals/GOAL-RC021-01_CUSTOMER_MISREAD_RISK_COPY_FIX.md
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_01_CUSTOMER_MISREAD_RISK_COPY_FIX_2026_05_09.md
```

## Output Paths

```text
docs/goals/GOAL-RC021-02_SCREENSHOT_TEXT_EVIDENCE_REFRESH.md
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-first-load-folded-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-first-load-folded-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
artifacts/product_experience/ux04/incident-product-first-load-desktop.png
artifacts/product_experience/ux04/incident-product-first-load-desktop.text.json
artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.png
artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.text.json
artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.png
artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.text.json
artifacts/product_experience/ux04/incident-product-mobile.png
artifacts/product_experience/ux04/incident-product-mobile.text.json
artifacts/product_acceleration/rc021_screenshot_text_evidence_refresh.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_02_SCREENSHOT_TEXT_EVIDENCE_REFRESH_2026_05_09.md
```

## Allowed Files

```text
docs/goals/GOAL-RC021-02_SCREENSHOT_TEXT_EVIDENCE_REFRESH.md
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
frontend/tests/e2e/incident-product-page.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-first-load-folded-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-first-load-folded-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
artifacts/product_experience/ux04/incident-product-first-load-desktop.png
artifacts/product_experience/ux04/incident-product-first-load-desktop.text.json
artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.png
artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.text.json
artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.png
artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.text.json
artifacts/product_experience/ux04/incident-product-mobile.png
artifacts/product_experience/ux04/incident-product-mobile.text.json
artifacts/product_acceleration/rc021_screenshot_text_evidence_refresh.json
docs/S6_CONTROLLED_TRIAL_GOAL_RC021_02_SCREENSHOT_TEXT_EVIDENCE_REFRESH_2026_05_09.md
```

## Allowed Scope

```text
Refresh or explicitly reuse with hash-match the 7-path evidence set:
1) /s1-trial desktop
2) /s1-trial mobile
3) /s1-run first-load folded desktop
4) /incident/CASE-2847 first-load desktop
5) /incident/CASE-2847 evidence-expanded desktop
6) /incident/CASE-2847 technical-expanded desktop
7) /incident/CASE-2847 mobile (full-page as available downscroll evidence)
Ensure matching .text.json exists for each screenshot and maintain no-boundary-violation text.
Keep AI source default-folded and expanded-path assertions validated through e2e deterministic checks.
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-RC021-02_SCREENSHOT_TEXT_EVIDENCE_REFRESH.md
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.visual.spec.ts tests/e2e/incident-product-page.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
PowerShell hash/sidecar evidence generation command -> artifacts/product_acceleration/rc021_screenshot_text_evidence_refresh.json
PowerShell assertion command: all 7 screenshot files and 7 sidecars exist; AI source folded first-load sidecar excludes "AI 建议输出预览"; text sidecars include no old misread phrases
git -c core.quotepath=false diff --check
```

## HOLD Conditions

```text
Any 7-path screenshot or matching text sidecar missing.
AI source first-load sidecar contains "AI 建议输出预览" or other expanded-only marker.
Any sidecar contains old misread-risk phrases from RC021-01.
validate_review_screenshots returns HOLD.
Any boundary or security sentinel violation appears in screenshot sidecars.
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
7-path screenshot/text sidecar hash evidence JSON generated
7-path deterministic assertion checks PASS
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
PASS unlock: GOAL-RC021-03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD.
HOLD behavior: report exact screenshot/sidecar assertion failure and stop.
```

## Commit Posture

```text
one commit for this passing Goal
commit message: feat(secupilot): GOAL-RC021-02 screenshot text evidence refresh
do not push
```
