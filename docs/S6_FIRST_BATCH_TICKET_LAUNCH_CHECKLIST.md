# S6 First Batch Ticket Launch Checklist

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 First Batch Ticket Launch Checklist |
| Status | READY_FOR_EXACT_TICKET after scaffold decision |
| Date | 2026-04-24 |
| Repo root | `D:\产品设计\New folder` |
| Frontend scaffold | `vite-react-typescript` |
| Execution surface | `codex` for all first-batch tickets |

This checklist converts the Jira smoke batch into exact repo-local launch scope.

It does not authorize launch, deploy, real data, credentials, public endpoint work, parked-stream reopen, backend API changes, schema/API breaking changes, or product scope beyond named first-batch tickets.

## 2. Batch Summary

| Ticket | Jira Key | Source Req | Execution Surface | Reviewer | Patch Batch | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| `GS-T01` | `SCRUM-9` | `GS-01` | `codex` | `claude-code` / `claude-cmd` | `Normal-Batch` | `READY_FOR_EXACT_TICKET` |
| `GS-T02` | `SCRUM-10` | `GS-02` | `codex` | `claude-code` / `claude-cmd` | `Normal-Batch` | `READY_FOR_EXACT_TICKET` |
| `GS-T03` | `SCRUM-11` | `GS-03` | `codex` | `claude-code` / `claude-cmd` | `Normal-Batch` | `READY_FOR_EXACT_TICKET` |
| `IN-T05` | `SCRUM-12` | `IN-04` | `codex` | `claude-code` / `claude-cmd` | `Normal-Batch` | `READY_FOR_EXACT_TICKET` |
| `CD-T03` | `SCRUM-13` | `CD-03` | `codex` | `claude-code` / `claude-cmd` | `Normal-Batch` | `READY_FOR_EXACT_TICKET` |

## 3. Exact Behaviors

### GS-T01

Implement a top global conversation/search input shell visible on all rendered workbench views.

Acceptance:

- input is visually dominant over navigation;
- placeholder communicates conversation-first query behavior;
- no permission is granted by submitting text;
- no backend request is made in this slice.

### GS-T02

Implement role-cropped first-level navigation.

Acceptance:

- `P1` sees Inbox and Search / History only;
- hidden routes are not rendered as clickable disabled links;
- Case Detail is not a first-level nav item;
- role switch in the local demo updates visible nav without creating new permissions.

### GS-T03

Implement a global coverage badge visible on all rendered workbench views.

Acceptance:

- badge includes text enum such as `Coverage L2`;
- badge is not color-only;
- badge remains visible on Inbox and Case Detail.

### IN-T05

Implement Inbox to Case Detail case-first navigation.

Acceptance:

- Inbox case card opens `/case/:caseId`;
- Case Detail route shows the case header and summary first;
- no technical panel is opened before case header/summary.

### CD-T03

Implement Case Detail follow-up input always visible when case detail is rendered.

Acceptance:

- follow-up input appears in Case Detail summary view;
- low coverage demo state does not hide the input;
- input does not authorize remediation or action execution.

## 4. Exact Non-Goals

This batch must not implement:

- backend API changes;
- real case data integration;
- auth, login, RBAC backend, or user management;
- approval queue;
- manager view;
- search/history full behavior;
- coverage-health page;
- expert-mode data expansion;
- evidence/timeline/blast-radius panel behavior;
- action execution;
- public endpoints;
- deployment scripts.

## 5. Exact Allowed Files

Allowed files:

- `.gitignore`
- `docs/S6_FRONTEND_SCAFFOLD_DECISION.md`
- `docs/S6_FIRST_BATCH_TICKET_LAUNCH_CHECKLIST.md`
- `docs/S6_FIRST_BATCH_IMPLEMENTATION_LAUNCH_PREP.md`
- `docs/PROJECT_STRUCTURE.md`
- `frontend/index.html`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.json`
- `frontend/tsconfig.node.json`
- `frontend/vite.config.ts`
- `frontend/src/main.tsx`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/test/setup.ts`
- `frontend/src/App.test.tsx`

## 6. Required Tests

Frontend:

```powershell
cd frontend
npm run test
npm run build
```

Backend guard:

```powershell
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
```

Required assertions:

- global input renders;
- `P1` nav excludes Approval Queue, Coverage & Health, and Manager View;
- coverage badge renders text enum;
- Inbox case card navigates to case detail;
- Case Detail follow-up input is visible.

## 7. Rollback

Rollback condition:

```text
Revert frontend scaffold and S6 docs if frontend tests/build fail, backend guard fails, scope expands outside allowed files, or HOLD triggers fire.
```

## 8. HOLD Conditions

HOLD if:

- implementation requires files outside the allowed list;
- implementation requires backend/API/schema changes;
- implementation requires dependency or framework beyond Vite React TypeScript, Vitest test tooling, and `lucide-react` icons;
- implementation invents routes beyond `/`, `/inbox`, and `/case/:caseId`;
- implementation adds product behavior outside the five first-batch tickets;
- tests cannot be named or run;
- Jira execution surface update cannot be reconciled after code work;
- reviewer/review surface becomes unavailable at closeout.
