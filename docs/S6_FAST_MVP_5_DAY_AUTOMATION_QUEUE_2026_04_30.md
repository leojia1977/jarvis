# S6 Fast MVP 5-Day Automation Queue 2026-04-30

## 1. Purpose

This queue prevents full automation from idling while preserving the new fast-MVP rule:

```text
EVERY_AUTOMATED_ITEM_MUST_DELIVER_CODE_OR_ARTIFACT_OR_TEST_OUTPUT
```

No recurring loop should run unless the next queue item has exact files, commands, verification, and stop conditions.

## 2. Global Boundaries

Allowed:

```text
frontend workbench changes
local scripts
local synthetic/package artifacts
local tests
docs that define exact commands or closeout evidence
stage/commit per passing queue item if explicitly bulk-authorized
```

Not allowed:

```text
real data
masked-real data
live customer data
live Qwen API call
production connector
production write-back
customer-visible publish/deploy
backend API/schema migration unless a later explicit GO names it
secrets/tokens/auth headers in docs, commands, artifacts, or commits
push without a separate explicit push authorization
```

## 3. Stop Conditions

Automation must stop and report if any condition is true:

```text
git status shows unrelated dirty files outside the current item write scope
required input file/folder is missing
tests fail twice in the same way
command exits with unexpected code
secret/token/raw payload/customer-visible/write-back finding appears
Claude Code / external review command is unavailable or returns a tool/path error
the ordered queue is exhausted
the next item would require real data, live connector, live Qwen, deploy, or customer-visible output
```

## 4. Queue

| Order | Item | Deliverable | Main files | Verification |
| --- | --- | --- | --- | --- |
| 1 | MVP-03 | Frontend S1 artifact viewer | `frontend/src/secupilot/s1/*`, `frontend/src/App.tsx`, `frontend/src/App.css`, `frontend/src/App.test.tsx` | `npm run test -- --run App.test.tsx`; `npm run build`; fast gate |
| 2 | MVP-04 | One-shot VS Code and PowerShell command loop | `.vscode/tasks.json`, `scripts/s1_fast_mvp_loop.ps1`, focused docs update | run task commands directly; fast gate |
| 3 | MVP-05 | Playwright smoke for `/s1-run` and local visual sanity | `frontend/tests/e2e/s1-artifact-viewer.spec.ts`, optional screenshot artifact | `npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts`; frontend build |
| 4 | MVP-06 | S1 artifact validator | `scripts/s1_artifact_validate.py`, `backend/tests/test_s1_artifact_validate.py` | targeted backend test; validate current `artifacts/s1_closed_shadow_runs/2026-04-30-001` |
| 5 | MVP-07 | `external-output` provider import path | `scripts/s1_closed_shadow_run.py`, `backend/tests/test_s1_closed_shadow_run.py`, sample approved-output fixture | targeted backend test; runner command with `--provider external-output` |
| 6 | MVP-08 | Local demo package builder | `scripts/package_s1_local_demo.py`, `backend/tests/test_package_s1_local_demo.py`, `artifacts/local_demo_packages/*` | targeted backend test; package command; manifest scan |
| 7 | MVP-09 | Focused Claude Code review capture if local command is available | `artifacts/reviews/claude_code/*`, closeout doc | review command exits 0 and references current diff only |

## 5. One-Shot Commands

Baseline:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
git -c core.quotepath=false status --short --branch
py -3 scripts\git_preflight.py --mode fast
```

Frontend loop:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder\frontend'
npm run test -- --run App.test.tsx
npm run build
```

S1 runner loop:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 scripts\s1_closed_shadow_run.py --run-id S1-CLOSED-SHADOW-2026-04-30-001 --input mock_data\s0_synthetic\qwen_fact_bundle --output artifacts\s1_closed_shadow_runs\2026-04-30-001 --provider fixture --no-writeback --no-customer-visible
```

Fast closeout:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
git diff --check
py -3 scripts\git_preflight.py --mode fast
git -c core.quotepath=false status --short --branch
```

## 6. Bulk Authorization Text

If the user wants the five-day queue to run without repeated micro-authorization, use exactly:

```text
GO_FAST_MVP_5_DAY_AUTOMATION_QUEUE_2026_04_30

Authorize Codex to execute MVP-04 through MVP-09 in order after MVP-03 closeout.
Authorize local file edits, local command execution, local tests, local artifact generation, stage, and commit for each passing item.
Do not push.
Do not use real data or masked-real data.
Do not call live Qwen/API/connectors.
Do not deploy.
Do not create customer-visible output.
Stop on any Stop Condition in docs/S6_FAST_MVP_5_DAY_AUTOMATION_QUEUE_2026_04_30.md.
```

## 7. No-Idle Rule

When the queue is exhausted, automation must stop with:

```text
FAST_MVP_QUEUE_EXHAUSTED_NO_IDLE_LOOP
```

It must not invent MVP-10 or continue scanning for unrelated work.
