# S6 AP-T02 P0 Readonly Approval Readiness Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T02` |
| Title | P0 readonly approval container |
| Decision | `READINESS_CHECKLIST_HOLD_PENDING_P0_RENDERABLE_APPROVAL_CONTEXT` |
| Primary implementor | Codex for checklist only |
| Execution surface | codex |
| Reviewer | Claude Code required if later implementation diff exists |
| Review surface | claude-cmd |
| Workspace | VS Code / local repo |
| Implementation status | `NOT_STARTED` |
| Jira issue | `SCRUM-54` |
| Jira status | `To Do / HOLD comment synced` |

This checklist is readiness-only. It does not implement `AP-T02`, does not mark `AP-T02` Done, and does not authorize P0 approval implementation.

## 2. Checklist Decision

Decision:

```text
READINESS_CHECKLIST_HOLD_PENDING_P0_RENDERABLE_APPROVAL_CONTEXT
```

Meaning:

- `AP-T01` already implemented `/approval` as route shell / guard only.
- The code path already contains a P0 readonly approval-container branch if a P0 resolved context is ever supplied.
- Current mock fixture phases do not supply a renderable P0 approval context.
- The nav currently exposes `Approval Queue` only to P2, so AP-T02 cannot be completed from current user-visible fixture flow.
- Proving P0 readonly approval behavior end-to-end would require either a P0 approval fixture/context or a separate approved test harness path.

Therefore `AP-T02` remains HOLD. No implementation GO activates from this checklist.

## 3. Current Repo Evidence

Existing repo evidence:

- `/approval` route exists.
- P2 enters a shell-only approval container.
- P1 hard-redirects to `/inbox`.
- P3 hard-redirects URL to `/manager` while rendering only a route guard.
- P0 branch is represented in code as readonly if a P0 context is supplied, but it is not currently reachable from the fixture phase selector.
- No approval controls, confirmation modal, state transition, observation-window countdown, stale-approve behavior, or approval audit summary is implemented by AP-T01.

## 4. Required Before Implementation GO

A later `AP-T02` implementation may proceed only after a new checklist proves all of:

```text
P0 renderable approval context exists: YES
P0 readonly route entry is testable without URL/storage authority: YES
Allowed files are exact: YES
Test command is exact: YES
No fixture/adapter/validator/ResolvedSurfaceContext change required: YES
No P2 approval-control scope enters AP-T02: YES
```

Likely allowed implementation files if the HOLD clears:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

## 5. Non-Authorization

This checklist does not authorize:

- implementing AP-T02;
- exposing P0 approval nav by URL/storage inference;
- approve/reject/delay/observe controls;
- confirmation modal;
- state transition;
- observation-window countdown;
- stale-approve behavior;
- approval audit summary;
- backend/runtime/API/schema changes;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- real data, secrets, deploy, public endpoint, or external pilot.

## 6. Next Route

```text
OPEN_MV_T02_P0_P2_MANAGER_READONLY_VARIANT_READINESS_CHECKLIST
```
