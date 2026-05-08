# GOAL-UX-01 Incident Workbench Main Path Polish

## Goal ID

GOAL-UX-01_INCIDENT_WORKBENCH_MAIN_PATH_POLISH

## Goal Type

page

## Goal Statement

把 `/incident/CASE-2847` 从轻量结果页推进成首页后的事件工作台主路径：客户第一眼看到事件队列、结论报告、建议动作、时间线和只读边界，而不是证据包目录或调试台。

## Primary Executable Object

page=/incident/CASE-2847
test=frontend focused test + Playwright screenshot smoke
artifact=artifacts/product_experience/ux01/
closeout=docs/S6_FAST_PRODUCT_GOAL_UX_01_INCIDENT_WORKBENCH_MAIN_PATH_POLISH_CLOSEOUT_2026_05_08.md

## Inputs

- `docs/S3B_CASE_EXPERIENCE_PRD.md`
- `docs/S6_MVP67_PRD_ROLE_MAPPING_AND_PRODUCT_HOME_IA_2026_05_08.md`
- `docs/S6_FAST_MVP_MVP_68_INCIDENT_DETAIL_PRODUCT_PAGE_CLOSEOUT_2026_05_08.md`
- `D:\产品设计\Sprint2_T3_JARVIS_完整产品设计.md`
- `D:\产品设计\SecuPilot_HMI.jsx`
- `D:\产品设计\SecuPilot_Live.jsx`
- Existing `/incident/CASE-2847` product route and synthetic workbench case fixture.

## Output Paths

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/tests/e2e/incident-product-page.spec.ts`
- `artifacts/product_experience/ux01/incident-product-desktop.png`
- `artifacts/product_experience/ux01/incident-product-desktop.text.json`
- `artifacts/product_experience/ux01/incident-product-mobile.png`
- `artifacts/product_experience/ux01/incident-product-mobile.text.json`
- `artifacts/reviews/claude_web/ux01_incident_workbench_review_prompt_20260508.md`
- `docs/S6_FAST_PRODUCT_GOAL_UX_01_INCIDENT_WORKBENCH_MAIN_PATH_POLISH_CLOSEOUT_2026_05_08.md`

## Allowed Files

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/tests/e2e/incident-product-page.spec.ts`
- `artifacts/product_experience/ux01/**`
- `artifacts/reviews/claude_web/ux01_incident_workbench_review_prompt_20260508.md`
- `docs/goals/GOAL-UX-01_INCIDENT_WORKBENCH_MAIN_PATH_POLISH.md`
- `docs/S6_FAST_PRODUCT_GOAL_UX_01_INCIDENT_WORKBENCH_MAIN_PATH_POLISH_CLOSEOUT_2026_05_08.md`

## Allowed Scope

- Local/offline frontend page changes for `/incident/CASE-2847`.
- Synthetic case copy and visual layout derived from existing product design references.
- Playwright screenshots and text evidence under `artifacts/product_experience/ux01/`.
- Claude Web review prompt preparation only; no external upload from Codex.
- Local tests, build, diff review, stage, and commit.

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
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-UX-01_INCIDENT_WORKBENCH_MAIN_PATH_POLISH.md
npm run test -- --run src/App.test.tsx
npm run build
npm run test:e2e -- tests/e2e/incident-product-page.spec.ts
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- `/incident/CASE-2847` shows `P1`, `P2`, `P3`, `Mock Fixture`, `Expert Mode`, or stale RC wording in reviewer-facing visible text.
- The page exposes raw payload, raw evidence, token, auth header, private key, or secret-like text.
- The UI presents destructive action as executable instead of human-reviewed recommendation.
- Any `data-real-data`, `data-live-qwen-api`, `data-live-connectors`, `data-production-writeback`, or `data-customer-visible-output` sentinel becomes true.
- Playwright screenshots fail to render desktop or mobile workbench content.
- Tests fail twice in the same way.
- Scope expands beyond listed files.

## Rollback

- Revert the listed frontend files and test file.
- Delete generated `artifacts/product_experience/ux01/` evidence if the Goal is abandoned before commit.
- Preserve failed command output in the closeout or review artifact if a HOLD is reached.
- Do not hide failed evidence.

## Evidence Contract

- Command transcript or test output for all acceptance commands.
- Playwright desktop and mobile screenshots.
- Screenshot text JSON for visible-text inspection.
- Claude Web review prompt referencing the generated screenshots.
- Closeout report with exact commands and PASS/HOLD result.

## Safety Sentinels

- `data-real-data="false"`
- `data-live-qwen-api="false"`
- `data-live-connectors="false"`
- `data-production-writeback="false"`
- `data-customer-visible-output="false"`
- no `P1` / `P2` / `P3` / `Mock Fixture` / `Expert Mode` in visible reviewer text
- no `authorization:` / `bearer` / `token` / `private_key` in visible reviewer text

## Merge Rule

May stage/commit only if all acceptance commands PASS and no HOLD condition is observed. Do not push. Do not include unrelated changes or historical untracked residue.

## Next Unlock

If PASS, unlock Claude Web product/design review of the generated incident workbench screenshots and then continue the next product-depth page Goal. If HOLD, stop and record the blocker before any further page work.

## Commit Posture

Commit this Goal as one focused product UI commit after verification. Do not push.
