# S6 First Batch Implementation Launch Prep

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 First Batch Implementation Launch Prep |
| Status | Superseded by scaffold decision and exact ticket launch checklist |
| Date | 2026-04-24 |
| Repo root | `D:\产品设计\New folder` |
| Current repo branch | `codex/s3-a-runtime` |
| Current repo HEAD | `96d3e03eab2e278829beea1d64cc5f77de537a34` |
| Current manifest snapshot | `S5-PRD-INTAKE-AUTOMATION-TRIGGER-2026-04-22-001` |
| Current manifest verification | `PASS` |
| External product package | `D:\产品设计\secupilot0421` |

This record answers whether the first Jira-backed implementation batch can start immediately from the current repo state.

It does not authorize launch, deploy, external pilot, real-data handling, credential handling, public endpoint work, parked-stream reopen, schema/API breaking change, AI_COLLAB changes, broad frontend platforming, or implementation outside named tickets.

Resolution update on 2026-04-24:

- Human approved `vite-react-typescript` as the frontend scaffold baseline.
- Human approved temporary execution-surface change from `swe` to `codex` for `GS-T01`, `GS-T03`, and `CD-T03`.
- This launch-prep HOLD was resolved by `docs/S6_FRONTEND_SCAFFOLD_DECISION.md` and `docs/S6_FIRST_BATCH_TICKET_LAUNCH_CHECKLIST.md`.

## 2. Cloud Jira State

Jira Cloud smoke setup is PASS.

| Backlog ID | Jira Key | Jira Type | Status | Parent | Story Points | Patch Gate Batch | Planned Execution Surface |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `GS-EPIC` | `SCRUM-6` | `长篇故事` | `待办` |  |  |  |  |
| `IN-EPIC` | `SCRUM-7` | `长篇故事` | `待办` |  |  |  |  |
| `CD-EPIC` | `SCRUM-8` | `长篇故事` | `待办` |  |  |  |  |
| `GS-T01` | `SCRUM-9` | `任务` | `待办` | `SCRUM-6` | 2 | `Normal-Batch` | `codex` |
| `GS-T02` | `SCRUM-10` | `任务` | `待办` | `SCRUM-6` | 2 | `Normal-Batch` | `codex` |
| `GS-T03` | `SCRUM-11` | `任务` | `待办` | `SCRUM-6` | 1 | `Normal-Batch` | `codex` |
| `IN-T05` | `SCRUM-12` | `任务` | `待办` | `SCRUM-7` | 1 | `Normal-Batch` | `codex` |
| `CD-T03` | `SCRUM-13` | `任务` | `待办` | `SCRUM-8` | 2 | `Normal-Batch` | `codex` |

Do not import the first-batch smoke CSV again. Do not import the full CSV as-is unless the 8 existing smoke rows are excluded or the sync is idempotent.

## 3. Repo Discovery Result

At the pre-decision discovery point, the repo was backend/runtime only.

Observed implementation surfaces:

- `backend/app/main.py`
- `backend/app/runtime_service.py`
- `backend/app/agents/*`
- `backend/app/tools/*`
- `backend/tests/*`
- root compatibility wrappers

No existing frontend application directory was found at that time:

- no `frontend/`
- no `web/`
- no `ui/`
- no `client/`
- no repo-local frontend `package.json`

Targeted backend tests pass:

```text
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
```

Result:

```text
Ran 42 tests
OK
```

## 4. Product Source Import State

The latest product package exists outside the repo source-of-truth root:

- `D:\产品设计\secupilot0421\SecuPilot_Engineering_Executable_PRD_v1.0_冻结版.md`
- `D:\产品设计\secupilot0421\SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2.1.md`
- `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx`
- `D:\产品设计\secupilot0421\SecuPilot_Jira_Cloud_Smoke_Result_v0.1.md`
- `D:\产品设计\secupilot0421\SecuPilot_Visual_Kickoff_Frame_Checklist_v0.3.xlsx`

Under the current repo handoff rule, external files are input material until explicitly imported into `D:\产品设计\New folder` and governed by the repo closeout path.

Therefore the first implementation batch is not yet repo-launch-ready as code work.

## 5. First-Batch Readiness Decision

| Ticket | Readiness | Reason |
| --- | --- | --- |
| `GS-T01` | `NEEDS_GREEN_DOCS_ONLY_TICKET_PREP` | Requires a repo-local frontend surface or approved scaffold file scope before implementation. Planned `swe` execution surface is not currently available locally. |
| `GS-T02` | `NEEDS_GREEN_DOCS_ONLY_TICKET_PREP` | Role-based nav needs a frontend route/nav model in repo. |
| `GS-T03` | `NEEDS_GREEN_DOCS_ONLY_TICKET_PREP` | Coverage badge needs frontend state/source and UI placement. Planned `swe` execution surface is not currently available locally. |
| `IN-T05` | `NEEDS_GREEN_DOCS_ONLY_TICKET_PREP` | Inbox to case-detail navigation needs frontend route surface in repo. |
| `CD-T03` | `NEEDS_GREEN_DOCS_ONLY_TICKET_PREP` | Case-detail follow-up input needs frontend case-detail surface in repo. Planned `swe` execution surface is not currently available locally. |

Original pre-scaffold batch decision:

```text
NOT_READY_FOR_CODE_START
```

The correct next step is not broad coding. The correct next step is a small repo-local launch-prep stage that imports governed product source references, chooses or confirms the frontend scaffold strategy, and writes exact allowed files / test commands for the first batch.

Current resolved batch decision:

```text
READY_FOR_EXACT_TICKET under docs/S6_FIRST_BATCH_TICKET_LAUNCH_CHECKLIST.md
```

## 6. Required Decisions Before Code

The decisions below are preserved as the original launch-prep blockers. They are resolved by the 2026-04-24 human approvals recorded above.

### 6.1 Frontend Scaffold Strategy

Because no frontend exists in the repo, code work needs one explicit scaffold decision.

Allowed choices for next review:

1. `static-no-dependency`:
   - fastest and lowest dependency risk;
   - can render a bounded HTML/CSS/JS workbench shell;
   - weaker long-term fit for a rich case workbench.
2. `vite-react-typescript`:
   - stronger fit for the PRD's routed Web workbench;
   - introduces Node dependency, package files, build scripts, and frontend test/lint commands;
   - should be explicitly authorized as the frontend scaffold baseline before code.

Do not silently pick a framework inside `GS-T01`.

### 6.2 Execution Surface

Local SWE command discovery found no usable `mini`, `mini-extra`, `mini-swe-agent`, or `swe` command.

Until SWE is unblocked, first-batch implementation can proceed only if one of the following is explicitly accepted:

1. Change first-batch execution surface from `swe` to `codex` for the three planned SWE tickets; or
2. Pause implementation and complete SWE tool unblock first.

### 6.3 Repo-Local Product Intake

Before code begins, create a repo-local intake/launch artifact that names:

- imported PRD / GoNoGo / tracker sources;
- exact first-batch tickets;
- exact file scope;
- exact test command;
- exact rollback condition;
- exact HOLD conditions;
- review path;
- closeout path.

## 7. Recommended Next Route

Recommended route:

```text
OPEN_S6_FRONTEND_SCAFFOLD_AND_FIRST_BATCH_LAUNCH_PREP_STAGE
```

Recommended lane:

```text
Green docs-only launch prep
```

Recommended outputs:

1. Repo-local product-source intake record.
2. Frontend scaffold decision record.
3. First-batch exact ticket launch checklist.
4. Updated Jira issue comments or metadata if execution surface changes.

Implementation should start only after those records produce:

```text
READY_FOR_EXACT_TICKET
```

or, if SWE remains planned:

```text
READY_FOR_SWE_ACCELERATION
```

## 8. HOLD Conditions

Implementation remains HOLD if any of these stay true:

- product source remains external-only and not repo-local governed context;
- frontend scaffold strategy is not explicit;
- allowed files are not exact;
- test command is missing;
- rollback condition is missing;
- planned `swe` execution surface is unavailable but not formally changed;
- implementation would create broad frontend platforming beyond first-batch tickets;
- implementation would add routes, roles, panels, API changes, schema changes, or product behavior not named by the first-batch tickets.
