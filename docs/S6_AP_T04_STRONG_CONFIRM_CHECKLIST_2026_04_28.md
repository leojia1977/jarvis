# S6 AP-T04 Strong Confirm Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T04` |
| Title | Strong Confirm modal semantic shell |
| Status | `GO_BOUNDED_IMPLEMENTATION` |
| Date | 2026-04-28 |

## 2. Scope

Implement a bounded strong-confirm modal shell for P2 approval decisions. The modal may be opened from the P2 approval CTA boundary and must remain mock-only.

## 3. Required Semantics

- Only `P2_APPROVAL` with `PENDING_APPROVAL` may expose the strong-confirm entry.
- Modal content must show explicit decision facts before any future confirm action can exist.
- Confirm action must be disabled / unavailable in this ticket.
- No ActionMode is selected, created, persisted, or submitted.
- No state transition occurs.
- URL, localStorage, sessionStorage, and route params are not authority.

## 4. Allowed Files

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- closeout / route / handoff docs

## 5. Tests Required

- P2 pending approval can open the strong-confirm shell.
- The shell states that action wiring is unavailable.
- Confirm is disabled or otherwise non-submitting.
- Closing the modal returns focus to the originating CTA.
- No `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` text appears.

## 6. HOLD

HOLD if implementation needs state mutation, backend/API, real data, fixture contract edits, or product copy not already implied by the approval boundary.

## 7. Decision

```text
AP_T04_GO_BOUNDED_IMPLEMENTATION
```

