# S6 AP-T05 Delay / Observe Config Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T05` |
| Title | Delay / observe configuration semantic shell |
| Status | `GO_BOUNDED_IMPLEMENTATION` |
| Date | 2026-04-28 |

## 2. Scope

Implement bounded configuration shells for Delay and Observe decisions. The shells may preview governed fields, but they must not submit, schedule, or migrate state.

## 3. Required Semantics

- Only `P2_APPROVAL` with `PENDING_APPROVAL` may expose Delay / Observe config entries.
- Delay / Observe configuration is shell-only.
- Observation window behavior is not timer-authoritative here.
- `OBSERVATION_WINDOW` state migration remains out of scope.
- No backend/API, clock, runtime service, or external source is used.

## 4. Allowed Files

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- closeout / route / handoff docs

## 5. Tests Required

- Delay opens a config shell with no submit-side effect.
- Observe opens a config shell with no frontend timer authority.
- Config shells declare `data-state-mutation="none"`.
- Closing returns to the approval boundary.

## 6. HOLD

HOLD if implementation needs timers, state sync, backend/API, fixture contract edits, or any real state transition.

## 7. Decision

```text
AP_T05_GO_BOUNDED_IMPLEMENTATION
```

