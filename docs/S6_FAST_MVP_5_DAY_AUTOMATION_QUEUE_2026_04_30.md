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
runner CLI arguments in queue do not match `scripts/s1_closed_shadow_run.py`
artifact manifest contains unknown `retention_class`
`external-output` provider sees any non-whitelisted field
review command references files outside the current diff / current MVP item scope
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
| 8 | MVP-10 | Formal S1 artifact JSON schemas plus validator schema coverage | `schemas/s1/*.schema.json`, `scripts/s1_artifact_validate.py`, `backend/tests/test_s1_artifact_validate.py` | schema-aware validator test and current artifact validation |
| 9 | MVP-11 | Desktop/mobile visual smoke for `/s1-run` | `frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts`, `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/*` | Playwright visual smoke; frontend build |
| 10 | MVP-12 | Golden synthetic artifact snapshot refresh command | `scripts/refresh_s1_synthetic_snapshot.py`, `backend/tests/test_refresh_s1_synthetic_snapshot.py`, `artifacts/s1_closed_shadow_runs/2026-04-30-001-snapshot/*` | targeted backend test; snapshot refresh command |
| 11 | MVP-13 | Offline reviewer README bundled into local demo package | `scripts/package_s1_local_demo.py`, `backend/tests/test_package_s1_local_demo.py`, `artifacts/local_demo_packages/s1-closed-shadow-2026-04-30-001/*` | package test; README-bearing package command |

## 5. MVP-04 Command Entrypoints

MVP-04 adds deterministic local command entrypoints:

```text
.vscode/tasks.json
scripts/s1_fast_mvp_loop.ps1
```

The PowerShell loop is a command runner and verifier. It does not write product code by itself and does not push. Codex automation owns implementation, test execution, stage, and commit per passing item.

VS Code task labels:

```text
SecuPilot: Fast MVP Baseline
SecuPilot: MVP-03 S1 Artifact View
SecuPilot: MVP-05 Playwright Smoke
SecuPilot: MVP-06 Artifact Validator
SecuPilot: MVP-07 External Output Provider
SecuPilot: MVP-08 Local Demo Package
SecuPilot: MVP-09 Claude Review Capture
SecuPilot: MVP-10 S1 Artifact Schemas
SecuPilot: MVP-11 Visual Smoke
SecuPilot: MVP-12 Snapshot Refresh
SecuPilot: MVP-13 Offline Reviewer README
SecuPilot: Fast MVP Queue Verify
```

PowerShell modes:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode verify
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode baseline
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-05 -WriteStatus
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-06 -WriteStatus
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-07 -WriteStatus
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-08 -WriteStatus
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-09 -WriteStatus
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-10 -WriteStatus
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-11 -WriteStatus
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-12 -WriteStatus
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-13 -WriteStatus
```

## 6. One-Shot Commands

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

Runner CLI note:

```text
`--input` / `--output` are supported short aliases.
`--input-package` / `--artifact-dir` are supported long aliases.
Queue canonical commands use `--input`, `--output`, `--no-writeback`, and `--no-customer-visible`.
The explicit `--no-writeback` and `--no-customer-visible` assertions must stay present.
```

MVP-05 Playwright smoke:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder\frontend'
npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts
npm run build
```

MVP-06 artifact validator:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 -m unittest -q backend.tests.test_s1_artifact_validate
py -3 scripts\s1_artifact_validate.py --artifact-dir artifacts\s1_closed_shadow_runs\2026-04-30-001
```

MVP-07 external-output provider import:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 scripts\s1_closed_shadow_run.py --run-id S1-CLOSED-SHADOW-2026-04-30-001-EXTERNAL-OUTPUT --input mock_data\s0_synthetic\qwen_fact_bundle --output artifacts\s1_closed_shadow_runs\2026-04-30-001-external-output --provider external-output --provider-output-file mock_data\s1_closed_shadow_fixture\external_provider_output.example.json --no-writeback --no-customer-visible
py -3 -m unittest -q backend.tests.test_s1_closed_shadow_run
```

MVP-07 provider whitelist:

```text
allowed fields:
case_id
title
summary
severity
risk_level
evidence_metadata_refs
model_summary
reviewer_action
confidence
score
limitation_note

forbidden fields:
raw_payload
raw_evidence
host_raw_evidence
secret
token
auth_header
cookie
private_key
customer_visible_message
writeback_action
action_command
production_connector_output
```

MVP-08 local demo package builder:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 -m unittest -q backend.tests.test_package_s1_local_demo
py -3 scripts\package_s1_local_demo.py --artifact-dir artifacts\s1_closed_shadow_runs\2026-04-30-001 --output-dir artifacts\local_demo_packages\s1-closed-shadow-2026-04-30-001
```

MVP-09 optional Claude Code review capture:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
claude --print "Review only the current git diff for the SecuPilot Fast MVP queue item. Check correctness, unsafe data handling, secret/token/raw payload retention, production write-back, customer-visible output, tests, and overengineering. Do not edit files. Return findings ordered by severity, or say no findings."
```

MVP-10 artifact schema validation:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 -m unittest -q backend.tests.test_s1_artifact_validate
py -3 scripts\s1_artifact_validate.py --artifact-dir artifacts\s1_closed_shadow_runs\2026-04-30-001 --schema-dir schemas\s1
```

MVP-10 required schema files:

```text
schemas/s1/run_record.schema.json
schemas/s1/artifact_manifest.schema.json
schemas/s1/safety_scan.schema.json
schemas/s1/case_summary.schema.json
schemas/s1/final_status.schema.json
```

MVP-11 desktop/mobile visual smoke:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder\frontend'
npm run test:e2e -- tests/e2e/s1-artifact-viewer.visual.spec.ts
npm run build
```

MVP-11 screenshot boundary:

```text
Allowed screenshot root: artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/
Screenshots must be local test artifacts only.
Screenshots must not contain real data, masked-real data, secrets, tokens, auth headers, customer-visible publish UI, or production connector output.
```

MVP-12 golden synthetic artifact snapshot refresh:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 -m unittest -q backend.tests.test_refresh_s1_synthetic_snapshot
py -3 scripts\refresh_s1_synthetic_snapshot.py --input mock_data\s0_synthetic\qwen_fact_bundle --output artifacts\s1_closed_shadow_runs\2026-04-30-001-snapshot --provider fixture --no-writeback --no-customer-visible
```

MVP-12 snapshot boundary:

```text
Input must remain mock_data/s0_synthetic/qwen_fact_bundle.
Output must remain metadata-only synthetic/package artifact.
No real data, masked-real data, live Qwen, connector, write-back, deploy, or customer-visible output.
```

MVP-13 offline reviewer README package:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 -m unittest -q backend.tests.test_package_s1_local_demo
py -3 scripts\package_s1_local_demo.py --artifact-dir artifacts\s1_closed_shadow_runs\2026-04-30-001 --output-dir artifacts\local_demo_packages\s1-closed-shadow-2026-04-30-001 --include-reviewer-readme
```

MVP-13 reviewer README boundary:

```text
README must describe local/offline review only.
README must not include customer deployment instructions, production credentials, live connector setup, live Qwen/API setup, or approval language.
Package manifest must include SHA256 and retention class for README and packaged artifacts.
```

Fast closeout:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
git diff --check
py -3 scripts\git_preflight.py --mode fast
git -c core.quotepath=false status --short --branch
```

## 7. Five-Day Unattended Execution Model

This queue should not run as a busy 120-hour process. The correct unattended model is finite scheduled automation:

```text
schedule = every 4 hours for 30 runs
duration = approximately 5 days
work per run = select exactly one pending MVP item, implement it, run its exact verification, stage/commit if passing
idle behavior = if no pending item exists, report FAST_MVP_QUEUE_EXHAUSTED_NO_IDLE_LOOP and do not invent work
```

Recommended Codex cron automation:

```text
name = SecuPilot Fast MVP 5-Day Queue
workspace = D:\产品设计\New folder
schedule = FREQ=HOURLY;INTERVAL=4;COUNT=30
model = coding model
reasoning = high
```

Each automation run must:

```text
read this queue document first
inspect git status
preserve unrelated dirty files
choose the first pending MVP item in order
edit only the item write scope
run item verification and fast closeout
stage and commit passing item only
never push
stop on any HOLD condition
```

If MVP-04 through MVP-13 finish before the five-day window ends, remaining scheduled runs must not create MVP-14. They should report:

```text
FAST_MVP_QUEUE_EXHAUSTED_NO_IDLE_LOOP
```

## 8. Later Extension Candidates

These are not active queue items unless the user separately upgrades the authorization beyond MVP-13:

| Candidate | Deliverable | Boundary |
| --- | --- | --- |
| MVP-14 | Static local HTML report generated from S1 local demo package | local/offline artifact only |
| MVP-15 | Reviewer checklist renderer for local package contents | local/offline artifact only |
| MVP-16 | Manual import UX sketch for external-output files | frontend/local mock only |
| MVP-17 | Local cleanup command for generated Fast MVP artifacts | local artifact cleanup only, no repo source deletion |

## 9. Bulk Authorization Text

If the user wants the five-day queue to run without repeated micro-authorization, use exactly:

```text
GO_FAST_MVP_5_DAY_AUTOMATION_QUEUE_2026_04_30

Authorize Codex to execute MVP-04 through MVP-13 in order after MVP-03 closeout.
Authorize local file edits, local command execution, local tests, local artifact generation, stage, and commit for each passing item.
Do not push.
Do not use real data or masked-real data.
Do not call live Qwen/API/connectors.
Do not deploy.
Do not create customer-visible output.
Stop on any Stop Condition in docs/S6_FAST_MVP_5_DAY_AUTOMATION_QUEUE_2026_04_30.md.
```

## 10. No-Idle Rule

When the queue is exhausted, automation must stop with:

```text
FAST_MVP_QUEUE_EXHAUSTED_NO_IDLE_LOOP
```

It must not invent MVP-14 or continue scanning for unrelated work.
