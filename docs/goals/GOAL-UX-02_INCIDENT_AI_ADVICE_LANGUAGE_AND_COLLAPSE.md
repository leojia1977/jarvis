# GOAL-UX-02 Incident AI Advice Language And Collapse

## Goal ID

GOAL-UX-02_INCIDENT_AI_ADVICE_LANGUAGE_AND_COLLAPSE

## Goal Type

page

## Goal Statement

Close the RC-015 UX01 review notes by replacing visible model/provider/dry-run/HOLD engineering terms with operator-readable AI advice language and making the AI advice source section collapsed by default.

## Primary Executable Object

page=/incident/CASE-2847
test=frontend focused test + Playwright screenshot smoke
artifact=artifacts/product_experience/ux02/
closeout=docs/S6_FAST_PRODUCT_GOAL_UX_02_INCIDENT_AI_ADVICE_LANGUAGE_AND_COLLAPSE_CLOSEOUT_2026_05_08.md

## Inputs

- `docs/S6_RC015_UX01_INCIDENT_WORKBENCH_REVIEW_DECISION_2026_05_08.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/tests/e2e/incident-product-page.spec.ts`
- `frontend/src/App.test.tsx`

## Output Paths

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/tests/e2e/incident-product-page.spec.ts`
- `artifacts/product_experience/ux02/incident-product-desktop.png`
- `artifacts/product_experience/ux02/incident-product-desktop.text.json`
- `artifacts/product_experience/ux02/incident-product-mobile.png`
- `artifacts/product_experience/ux02/incident-product-mobile.text.json`
- `docs/S6_RC015_UX01_INCIDENT_WORKBENCH_REVIEW_DECISION_2026_05_08.md`
- `docs/S6_FAST_PRODUCT_GOAL_UX_02_INCIDENT_AI_ADVICE_LANGUAGE_AND_COLLAPSE_CLOSEOUT_2026_05_08.md`

## Allowed Files

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/tests/e2e/incident-product-page.spec.ts`
- `artifacts/product_experience/ux02/**`
- `docs/goals/GOAL-UX-02_INCIDENT_AI_ADVICE_LANGUAGE_AND_COLLAPSE.md`
- `docs/S6_RC015_UX01_INCIDENT_WORKBENCH_REVIEW_DECISION_2026_05_08.md`
- `docs/S6_FAST_PRODUCT_GOAL_UX_02_INCIDENT_AI_ADVICE_LANGUAGE_AND_COLLAPSE_CLOSEOUT_2026_05_08.md`

## Allowed Scope

- Local/offline frontend page copy and layout changes for `/incident/CASE-2847`.
- Default collapse behavior for the AI advice source section.
- Reviewer-facing visible text cleanup for model/provider/dry-run/HOLD terminology.
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
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-UX-02_INCIDENT_AI_ADVICE_LANGUAGE_AND_COLLAPSE.md
npm run test -- --run src/App.test.tsx
npm run build
npm run test:e2e -- tests/e2e/incident-product-page.spec.ts
Select-String -LiteralPath artifacts\product_experience\ux02\incident-product-desktop.text.json,artifacts\product_experience\ux02\incident-product-mobile.text.json -Pattern 'Qwen dry-run|provider stub|HOLD 输入包|模拟延迟|stub 案例数|Dry-run 输出预览|模型接入预览|\bP1\b|\bP2\b|\bP3\b|Mock Fixture|Expert Mode|raw_payload|authorization\s*[:=]|token\s*[:=]|private_key' -AllMatches
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- Reviewer-facing screenshot text still contains `Qwen dry-run`, `provider stub`, `HOLD 输入包`, `模拟延迟`, `stub 案例数`, `Dry-run 输出预览`, or `模型接入预览`.
- The AI advice source section is open by default on desktop or mobile.
- The route shows `P1`, `P2`, `P3`, `Mock Fixture`, `Expert Mode`, raw payload, token, auth header, private key, or stale RC wording.
- Any `data-real-data`, `data-live-qwen-api`, `data-live-connectors`, `data-production-writeback`, or `data-customer-visible-output` sentinel becomes true.
- Tests fail twice in the same way.
- Scope expands beyond listed files.

## Rollback

- Revert the listed frontend and test files.
- Delete generated `artifacts/product_experience/ux02/` evidence if the Goal is abandoned before commit.
- Preserve failed command output in closeout if a HOLD is reached.
- Do not hide failed evidence.

## Evidence Contract

- Command transcript or test output for all acceptance commands.
- Playwright desktop and mobile screenshots.
- Screenshot text JSON for visible text inspection.
- RC-015 decision doc linked to this Goal.
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

If PASS, unlock RC-016 screenshot/package review for the cleaned incident workbench route. If HOLD, stop and record the blocker before any further product-depth polish.

## Commit Posture

Commit this Goal as one focused product UI commit after verification. Do not push.
