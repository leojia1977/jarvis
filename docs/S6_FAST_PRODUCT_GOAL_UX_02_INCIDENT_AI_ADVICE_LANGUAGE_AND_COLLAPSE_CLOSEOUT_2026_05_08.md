# S6 Fast Product Goal UX-02 Incident AI Advice Language And Collapse Closeout

Date: 2026-05-08

Goal: `GOAL-UX-02_INCIDENT_AI_ADVICE_LANGUAGE_AND_COLLAPSE`

Status: PASS

## Review Intake

This Goal closes the main RC-015 note:

```text
Replace model/provider/dry-run/HOLD engineering terms with operator-readable AI advice language and make the AI advice source section collapsed by default.
```

RC-015 decision was recorded in:

```text
docs/S6_RC015_UX01_INCIDENT_WORKBENCH_REVIEW_DECISION_2026_05_08.md
```

## Product Changes

- Changed the visible route copy from engineering/model terms to operator-facing language:
  - `云端模型接入预览` -> `AI 建议来源`
  - `Qwen 接入路径` -> `了解 AI 建议的工作方式`
  - `provider stub` -> `建议引擎`
  - `HOLD 输入包` -> `建议暂停，等待人工清理`
  - `Live API` -> `实时模型连接`
  - `网络请求` -> `外部网络`
- Made the AI advice source section collapsed by default on desktop and mobile.
- Removed the visible `stub 案例数` and `模拟延迟` rows from the operator-facing summary.
- Changed the English-heavy subtitle to `SecuPilot · 事件研判报告`.
- Added explicit expand affordances for folded evidence, technical reconciliation, local feedback preview, and technical AI advice preview.
- Raised feedback missing-info touch targets to 44px.

## Evidence

- `artifacts/product_experience/ux02/incident-product-desktop.png`
- `artifacts/product_experience/ux02/incident-product-desktop.text.json`
- `artifacts/product_experience/ux02/incident-product-mobile.png`
- `artifacts/product_experience/ux02/incident-product-mobile.text.json`

The visible-text scan found no:

- `Qwen dry-run`
- `provider stub`
- `HOLD 输入包`
- `模拟延迟`
- `stub 案例数`
- `Dry-run 输出预览`
- `模型接入预览`
- `P1`, `P2`, `P3`
- `Mock Fixture`
- `Expert Mode`
- `raw_payload`
- `authorization`
- `token`
- `private_key`

## Verification

Commands run:

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-UX-02_INCIDENT_AI_ADVICE_LANGUAGE_AND_COLLAPSE.md
npm run test -- --run src/App.test.tsx
npm run build
npm run test:e2e -- tests/e2e/incident-product-page.spec.ts
Select-String -LiteralPath artifacts\product_experience\ux02\incident-product-desktop.text.json,artifacts\product_experience\ux02\incident-product-mobile.text.json -Pattern 'Qwen dry-run|provider stub|HOLD 输入包|模拟延迟|stub 案例数|Dry-run 输出预览|模型接入预览|\bP1\b|\bP2\b|\bP3\b|Mock Fixture|Expert Mode|raw_payload|authorization\s*[:=]|token\s*[:=]|private_key' -AllMatches
git -c core.quotepath=false diff --check
```

Results:

- Goal card validator: PASS
- Vitest `src/App.test.tsx`: 63 passed
- Frontend build: PASS
- Playwright `incident-product-page.spec.ts`: 2 passed
- Visible text scan: PASS, no matches
- Diff check: PASS

## Boundary

This closeout does not authorize:

- real data
- masked-real data
- live Qwen/API/connectors
- secrets, tokens, auth headers, or raw customer logs
- production write-back
- customer-visible publish/deploy/output
- external pilot
- production launch
- backend/runtime/API/schema changes
- autonomous approval, isolation, blocking, account closure, or action

## Next Unlock

Recommended next step:

```text
RC-016 incident workbench local review package
```

Purpose:

```text
Send the UX-02 screenshots and visible-text evidence back to reviewer to confirm RC-015 F1/F2/F3 and N01/N04/N05 are closed or downgraded.
```
