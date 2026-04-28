# S6 SH-T08 Narrow Implementation Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `SH-T08` |
| Title | Search/History P3 approval-audit source boundary narrow checklist |
| Status | `HOLD_PENDING_AP_T08_AND_VISUAL_SOURCE_FRAME` |
| Date | 2026-04-28 |
| Jira | `SCRUM-63` remains `待办` |

## 2. Decision

```text
SH_T08_NARROW_IMPLEMENTATION_CHECKLIST_HOLD_PENDING_AP_T08_AND_VISUAL_SOURCE_FRAME
```

`SH-T08` source legality is proven, but implementation should not proceed before AP-T08 defines the audit source boundary and the Search/History approval-audit visual/source frame is available or explicitly replaced by an approved semantic skeleton.

## 3. Current Safe Evidence

- `SH-T05` has read-only focus scopes for `summary`, `approval_audit`, and `history_audit`.
- `SH-T07` proves no write CTA is attached.
- `MV-T03` now provides route-only handoff to Manager without payload.
- `ResolvedSurfaceContext.audit_trail` exists and validates as an array.

## 4. Missing Before Implementation

- `AP-T08` implementation or authority-reviewed source boundary;
- exact visual/source frame for approval-audit availability in Search/History, previously tracked as `HF-SH-04` / audit source frame;
- exact allowed fields for P3 approval-audit source display;
- exact unavailable-state behavior that does not invent audit content.

## 5. Future Narrow Scope If HOLD Clears

Potential future implementation may only:

- render P3-only read-only approval-audit source availability inside `/search?tab=history&focus=approval_audit`;
- show honest unavailable state when audit source is not renderable;
- keep P1/P2/P0 on existing downgrade/no-authority paths;
- avoid host raw evidence, approval controls, state changes, Manager summary output, backend/runtime/API/schema, and fixture/context changes.

## 6. Non-Authorization

This checklist does not authorize implementation or Jira Done transition.
