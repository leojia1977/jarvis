# GOAL-UX-04 AI Advice Section Collapse Decision

## Goal ID

GOAL-UX-04_AI_ADVICE_SECTION_COLLAPSE_DECISION

## Goal Type

page

## Goal Statement

Close the RC-017 ambiguity where `AI 建议来源` claimed to be folded but first-load evidence still looked like the AI advice body was visible.

## Primary Executable Object

page=frontend/src/App.tsx
test=frontend/src/App.test.tsx
test=frontend/tests/e2e/incident-product-page.spec.ts
artifact=artifacts/product_experience/ux04/
closeout=docs/S6_FAST_PRODUCT_GOAL_UX_04_AI_ADVICE_SECTION_COLLAPSE_DECISION_CLOSEOUT_2026_05_08.md

## Inputs

- `docs/S6_RC017_UX03_INCIDENT_EVIDENCE_TIMELINE_REVIEW_DECISION_2026_05_08.md`
- RC-017 reviewer note `N-A AI Advice Source Fold Ambiguity`
- Current `/incident/CASE-2847` product page

## Output Paths

- `docs/goals/GOAL-UX-04_AI_ADVICE_SECTION_COLLAPSE_DECISION.md`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/tests/e2e/incident-product-page.spec.ts`
- `artifacts/product_experience/ux04/incident-product-first-load-desktop.png`
- `artifacts/product_experience/ux04/incident-product-first-load-desktop.text.json`
- `artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.png`
- `artifacts/product_experience/ux04/incident-product-evidence-expanded-desktop.text.json`
- `artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.png`
- `artifacts/product_experience/ux04/incident-product-technical-expanded-desktop.text.json`
- `artifacts/product_experience/ux04/incident-product-mobile.png`
- `artifacts/product_experience/ux04/incident-product-mobile.text.json`
- `docs/S6_FAST_PRODUCT_GOAL_UX_04_AI_ADVICE_SECTION_COLLAPSE_DECISION_CLOSEOUT_2026_05_08.md`

## Allowed Files

- `docs/goals/GOAL-UX-04_AI_ADVICE_SECTION_COLLAPSE_DECISION.md`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/tests/e2e/incident-product-page.spec.ts`
- `artifacts/product_experience/ux04/*`
- `docs/S6_FAST_PRODUCT_GOAL_UX_04_AI_ADVICE_SECTION_COLLAPSE_DECISION_CLOSEOUT_2026_05_08.md`

## Allowed Scope

- `/incident/CASE-2847` AI advice source section information architecture
- first-load folded-state behavior
- text-sidecar screenshot evidence
- small copy polish from `本地合成摘要字段` to `认证行为摘要`
- local frontend tests, build, and Playwright screenshots

## Forbidden Scope

- real data
- masked-real data
- live Qwen/API/connectors
- production write-back
- customer-visible publish, deploy, or output
- external pilot
- production launch
- secrets, tokens, auth headers, raw logs, raw payloads, or host raw evidence
- autonomous containment, remediation, isolation, blocking, approval, rejection, or action-mode choice
- backend API/schema migration
- push

## Acceptance Commands

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-UX-04_AI_ADVICE_SECTION_COLLAPSE_DECISION.md
Set-Location -LiteralPath frontend; npm run test -- --run src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/incident-product-page.spec.ts
PowerShell text scan over artifacts\product_experience\ux04\*.text.json
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- first-load desktop or mobile text after the `AI 建议来源` section title still contains `发生了什么`, `为什么重要`, `还不能确认什么`, `SecuPilot 研判计划`, `AI 建议输出预览`, `输入如何进入建议引擎`, or `失败时怎么处理`
- `AI 建议来源` body is rendered before the user expands the section
- the section still displays ambiguous `默认收起` wording while body content is visible
- screenshots or text sidecars expose P1/P2/P3, Mock Fixture, Expert Mode, stale RC wording, raw payload, token, auth header, live API, connector, production write-back, or deploy language
- frontend unit/build/e2e fails twice in the same way
- scope expands beyond listed files

## Rollback

- Revert listed frontend and test files.
- Remove generated `artifacts/product_experience/ux04/*` artifacts if they are wrong, or preserve them as failure evidence.
- Preserve RC-017 package and unrelated untracked artifacts.

## Evidence Contract

- Goal-card validation output
- frontend App test output
- frontend build output
- Playwright e2e output
- UX-04 desktop/mobile screenshots and text sidecars
- closeout report with exact command results

## Safety Sentinels

- no `real_data=true`
- no `masked_real_data=true`
- no `live_qwen_api=true`
- no `production_writeback=true`
- no `customer_visible_output=true`
- no `Authorization`
- no `Bearer`
- no `token`
- no `raw_payload`
- no `P1`, `P2`, `P3`, `Mock Fixture`, or `Expert Mode` in reviewer-facing UX-04 sidecars

## Merge Rule

May stage and commit only if all acceptance commands pass, UX-04 first-load evidence proves the AI advice body is folded, and no HOLD condition is observed. Do not push. Do not merge unrelated changes.

## Next Unlock

If PASS, unlock RC-018 or the next incident-workbench review package using UX-04 screenshots. If HOLD, stop and report the exact first-load folded-state blocker.

## Commit Posture

One commit for `GOAL-UX-04`. Stage and commit only listed files. Do not push.
