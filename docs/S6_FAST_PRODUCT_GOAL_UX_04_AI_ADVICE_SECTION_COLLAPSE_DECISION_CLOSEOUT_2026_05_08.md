# S6 Fast Product GOAL-UX-04 AI Advice Section Collapse Decision Closeout

Date: 2026-05-08

Goal:

```text
GOAL-UX-04_AI_ADVICE_SECTION_COLLAPSE_DECISION
```

Status:

```text
PASS
```

## Decision

Selected Option A from RC-017:

```text
AI 建议来源 is truly collapsed on first load.
```

The section now shows only the header, short explanation, and `展开查看` affordance before interaction. The detailed AI advice source body is rendered only after expansion.

## Changes

- Added explicit open state for `AI 建议来源`.
- Removed ambiguous `默认收起` wording from the first-load UI.
- Conditional-rendered the AI advice source body so first-load sidecars cannot capture hidden body content.
- Moved the AI advice source section after the incident explanation and action-plan blocks so text order no longer suggests the following product sections are AI-source body content.
- Changed the evidence card source label from `本地合成摘要字段` to `认证行为摘要`.
- Updated App tests and Playwright e2e assertions.
- Generated UX-04 screenshot/text evidence under `artifacts/product_experience/ux04/`.

## Verification

Commands run:

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-UX-04_AI_ADVICE_SECTION_COLLAPSE_DECISION.md
Set-Location -LiteralPath frontend; npm run test -- --run src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/incident-product-page.spec.ts
PowerShell first-load AI-source folded text scan
PowerShell UX-04 forbidden/debug text scan
git -c core.quotepath=false diff --check
```

Results:

- Goal card validator: PASS.
- App tests: PASS, 63 passed.
- Frontend build: PASS.
- Playwright incident product page: PASS, 2 passed.
- First-load AI-source folded text scan: PASS for desktop and mobile.
- UX-04 forbidden/debug text scan: PASS.
- Diff check: PASS.

## Evidence

Generated files:

- `artifacts/product_experience/ux04/incident-product-first-load-desktop.png`
- `artifacts/product_experience/ux04/incident-product-first-load-desktop.text.json`
- `artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.png`
- `artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.text.json`
- `artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.png`
- `artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.text.json`
- `artifacts/product_experience/ux04/incident-product-mobile.png`
- `artifacts/product_experience/ux04/incident-product-mobile.text.json`

## Boundary

This closeout does not authorize:

- real data
- masked-real data
- live Qwen/API/connectors
- production write-back
- customer-visible publish, deploy, or output
- external pilot
- production launch
- secrets, tokens, auth headers, raw logs, raw payloads, or host raw evidence
- autonomous containment, remediation, isolation, blocking, approval, rejection, or action-mode choice

## Next Unlock

Use the UX-04 evidence in the next incident-workbench RC package or review handoff. The ECI/VFE automation lane can continue independently with `GOAL-ECIVFE-33_LOCAL_RULE_ENGINE`.
