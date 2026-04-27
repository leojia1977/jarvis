# S6 AP-T02 Unblock Pack 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T02` |
| Title | P0 readonly approval container unblock pack |
| Status | LOW_RISK_QUEUE_OUTPUT_HOLD_REMAINS |
| Queue item | `LR-03` |
| Date | 2026-04-27 |
| Current checklist | `docs\S6_AP_T02_P0_READONLY_APPROVAL_READINESS_CHECKLIST_2026_04_27.md` |

This pack records what must be true before P0 readonly approval can be implemented safely.

It does not authorize implementation, approval controls, state transition, fixture changes, backend/runtime/API/schema changes, or `ResolvedSurfaceContext` changes.

## 2. Current HOLD

Decision remains:

```text
READINESS_CHECKLIST_HOLD_PENDING_P0_RENDERABLE_APPROVAL_CONTEXT
```

Why:

- `AP-T01` implemented `/approval` as shell/guard only.
- The code path can represent P0 readonly behavior only if a P0 resolved context is supplied.
- Current fixture phases do not provide a renderable P0 approval context.
- P0 readonly behavior cannot be proven through URL/query/storage injection, because those are not authority sources.

## 3. Required Authority Boundary

| Boundary | Rule |
| --- | --- |
| Role authority | Must come from `ResolvedSurfaceContext`, not URL/storage/route params. |
| P0 behavior | Read-only container only, no approve/reject/delay/observe controls. |
| AP route authority | AP-T01 shell/guard remains separate from AP action implementation. |
| Missing context | Must render safe unavailable or guarded state, never guessed defaults. |

## 4. Minimum Reopen Conditions

`AP-T02` can move from HOLD to launch checklist only when all are true:

```text
P0 renderable approval context exists: YES
P0 readonly context is reachable without URL/storage authority: YES
Allowed files are exact: YES
Test command is exact: YES
No fixture/adapter/validator/ResolvedSurfaceContext change is needed inside AP-T02: YES
No approve/reject/delay/observe controls enter AP-T02: YES
No AP state transition enters AP-T02: YES
```

## 5. Safe Future Scope If Reopened

Likely allowed implementation scope after inputs exist:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

Likely test assertions:

- P0 context renders read-only approval container;
- P0 context does not attach approval action controls;
- P0 context does not expose `ActionMode`;
- URL/storage cannot upgrade role or action authority;
- P1/P3 guard behavior remains unchanged.

## 6. Explicit Non-Authorization

This pack does not authorize:

- creating or modifying P0 fixture/context;
- exposing P0 approval by URL or storage;
- approve/reject/delay/observe controls;
- confirmation modal;
- state transition;
- observation-window countdown;
- approval audit summary;
- backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot.

## 7. Recommended Authority Question

```text
What is the governed source for a P0 readonly approval context, and may that context be made renderable without changing fixture/adapter/validator or ResolvedSurfaceContext in this ticket?
```

