# S6 Controlled Trial GOAL-RC021-01 Customer Misread Risk Copy Fix

Date: 2026-05-09

Goal: GOAL-RC021-01_CUSTOMER_MISREAD_RISK_COPY_FIX

Decision: PASS

## Scope

在当前客户路径 UI 中替换两处易误解文案，并刷新截图与文本侧车证据：

- `查看部署准备` -> `查看本地接入准备`
- `隔离 finance-042 并锁定凭据` -> `待复核：finance-042 隔离与凭据锁定建议`

## Commands Run

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-RC021-01_CUSTOMER_MISREAD_RISK_COPY_FIX.md
```

Result: PASS.

```text
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.visual.spec.ts tests/e2e/incident-product-page.spec.ts
```

Result: PASS, 6 tests passed.

```text
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
```

Result: PASS, checked=5, blocking_finding_count=0, warning_count=0.

```text
keyword checks on refreshed *.text.json sidecars
```

Result: PASS.

- old phrases not found in refreshed sidecars:
  - `查看部署准备`
  - `隔离 finance-042 并锁定凭据`
- new phrases found in refreshed sidecars:
  - `查看本地接入准备`
  - `待复核：finance-042 隔离与凭据锁定建议`

```text
git -c core.quotepath=false diff --check
```

Result: PASS (line-ending warnings only, no blocking whitespace errors).

## Files Changed In Goal Scope

- `frontend/src/secupilot/s1/S1LocalTrialView.tsx`
- `frontend/src/App.tsx`
- `frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts`
- `frontend/tests/e2e/incident-product-page.spec.ts`
- `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png`
- `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json`
- `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png`
- `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json`
- `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json`
- `artifacts/product_experience/ux04/incident-product-first-load-desktop.png`
- `artifacts/product_experience/ux04/incident-product-first-load-desktop.text.json`
- `artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.png`
- `artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.text.json`
- `artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.png`
- `artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.text.json`
- `artifacts/product_experience/ux04/incident-product-mobile.png`
- `artifacts/product_experience/ux04/incident-product-mobile.text.json`
- `docs/goals/GOAL-RC021-01_CUSTOMER_MISREAD_RISK_COPY_FIX.md`
- `docs/S6_CONTROLLED_TRIAL_GOAL_RC021_01_CUSTOMER_MISREAD_RISK_COPY_FIX_2026_05_09.md`

## Boundary Check

- real_data: false
- masked_real_data: false
- live_qwen_api: false
- live_connectors: false
- production_writeback: false
- customer_visible_output: false
- external_pilot: false
- production_launch: false
- push: false

## Next Unlock

Proceed to `GOAL-RC021-02_SCREENSHOT_TEXT_EVIDENCE_REFRESH`.
