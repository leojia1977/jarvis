# GOAL-UX-03 Incident Evidence And Timeline Depth

## Goal ID

GOAL-UX-03_INCIDENT_EVIDENCE_AND_TIMELINE_DEPTH

## Goal Type

page

## Goal Statement

Polish the `/incident/CASE-2847` second-level evidence, timeline, and technical reconciliation states so the deeper view remains conclusion-first, operator-readable, folded by default where appropriate, and usable on mobile.

## Primary Executable Object

page=/incident/CASE-2847
test=frontend focused test + Playwright screenshot smoke
artifact=artifacts/product_experience/ux03/
closeout=docs/S6_FAST_PRODUCT_GOAL_UX_03_INCIDENT_EVIDENCE_AND_TIMELINE_DEPTH_CLOSEOUT_2026_05_08.md

## Inputs

- `docs/S6_RC016_UX02_INCIDENT_AI_ADVICE_REVIEW_DECISION_2026_05_08.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/tests/e2e/incident-product-page.spec.ts`

## Output Paths

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/tests/e2e/incident-product-page.spec.ts`
- `artifacts/product_experience/ux03/incident-product-first-load-desktop.png`
- `artifacts/product_experience/ux03/incident-product-first-load-desktop.text.json`
- `artifacts/product_experience/ux03/incident-product-evidence-expanded-desktop.png`
- `artifacts/product_experience/ux03/incident-product-evidence-expanded-desktop.text.json`
- `artifacts/product_experience/ux03/incident-product-technical-expanded-desktop.png`
- `artifacts/product_experience/ux03/incident-product-technical-expanded-desktop.text.json`
- `artifacts/product_experience/ux03/incident-product-mobile.png`
- `artifacts/product_experience/ux03/incident-product-mobile.text.json`
- `docs/S6_FAST_PRODUCT_GOAL_UX_03_INCIDENT_EVIDENCE_AND_TIMELINE_DEPTH_CLOSEOUT_2026_05_08.md`

## Allowed Files

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/tests/e2e/incident-product-page.spec.ts`
- `artifacts/product_experience/ux03/**`
- `docs/goals/GOAL-UX-03_INCIDENT_EVIDENCE_AND_TIMELINE_DEPTH.md`
- `docs/S6_RC016_UX02_INCIDENT_AI_ADVICE_REVIEW_DECISION_2026_05_08.md`
- `docs/S6_FAST_PRODUCT_GOAL_UX_03_INCIDENT_EVIDENCE_AND_TIMELINE_DEPTH_CLOSEOUT_2026_05_08.md`

## Allowed Scope

- Local/offline frontend page changes for `/incident/CASE-2847`.
- Evidence summary, event timeline, technical reconciliation, and folded-state UX polish.
- One first-load no-interaction screenshot proving the AI advice source section is folded by default.
- Reviewer-facing visible text cleanup and mobile readability fixes.
- Frontend tests, Playwright screenshots, visible-text evidence, diff review, stage, and commit.

## Forbidden Scope

- No real data.
- No masked-real data.
- No live Qwen/API calls.
- No live connectors.
- No production write-back or production writeback.
- No customer-visible publish/deploy/output.
- No secrets, tokens, auth headers, or raw customer logs.
- No backend API/schema migration.
- No autonomous approval, isolation, blocking, account closure, or state mutation.
- No push.

## Acceptance Commands

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-UX-03_INCIDENT_EVIDENCE_AND_TIMELINE_DEPTH.md
npm run test -- --run src/App.test.tsx
npm run build
npm run test:e2e -- tests/e2e/incident-product-page.spec.ts
Get-ChildItem -LiteralPath artifacts\product_experience\ux03 -Filter '*.text.json' | Select-String -Pattern 'Qwen dry-run|provider stub|HOLD 输入包|模拟延迟|stub 案例数|Dry-run 输出预览|模型接入预览|\bP1\b|\bP2\b|\bP3\b|Mock Fixture|Expert Mode|raw_payload|authorization\s*[:=]|token\s*[:=]|private_key' -AllMatches
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- First-load screenshots show the AI advice source section expanded by default.
- Evidence summary or technical reconciliation presents raw logs or engineering tables as the primary experience.
- Reviewer-facing screenshot text contains `Qwen dry-run`, `provider stub`, `HOLD 输入包`, `模拟延迟`, `stub 案例数`, `Dry-run 输出预览`, or `模型接入预览`.
- Reviewer-facing screenshot text shows `P1`, `P2`, `P3`, `Mock Fixture`, `Expert Mode`, raw payload, token, auth header, private key, or stale RC wording.
- Any `data-real-data`, `data-live-qwen-api`, `data-live-connectors`, `data-production-writeback`, or `data-customer-visible-output` sentinel becomes true.
- Mobile evidence or feedback controls are materially hard to read or tap.
- Tests fail twice in the same way.
- Scope expands beyond listed files.

## Rollback

- Revert the listed frontend and test files.
- Delete generated `artifacts/product_experience/ux03/` evidence if the Goal is abandoned before commit.
- Preserve failed command output in closeout if a HOLD is reached.
- Do not hide failed evidence.

## Evidence Contract

- Command transcript or test output for all acceptance commands.
- First-load no-interaction screenshot showing folded AI advice state.
- Expanded evidence summary screenshot.
- Expanded technical reconciliation screenshot.
- Mobile screenshot and visible-text JSON.
- Closeout report with exact commands and PASS/HOLD result.

## Safety Sentinels

- `data-real-data="false"`
- `data-live-qwen-api="false"`
- `data-live-connectors="false"`
- `data-production-writeback="false"`
- `data-customer-visible-output="false"`
- no `Qwen dry-run` / `provider stub` / `HOLD 输入包` / `模拟延迟` in visible screenshot text
- no `authorization:` / `bearer` / `token` / `private_key` in visible screenshot text

## Merge Rule

May stage/commit only if all acceptance commands PASS and no HOLD condition is observed. Do not push. Do not include unrelated changes or historical untracked residue.

## Next Unlock

If PASS, unlock RC-017 evidence/timeline depth review for the incident workbench route. If HOLD, stop and record the blocker before any further product-depth polish.

## Commit Posture

Commit this Goal as one focused product UI commit after verification. Do not push.
