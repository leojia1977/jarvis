# S6 AP-T08 Narrow Implementation Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T08` |
| Title | Approval audit chain narrow implementation checklist |
| Status | `HOLD_PENDING_EXTERNAL_AUTHORITY_REVIEW` |
| Date | 2026-04-28 |
| Jira | `SCRUM-62` remains `待办` |

## 2. Checklist Inputs

- Source proof: `docs/S6_AP_T08_SH_T08_AUTHORITY_SOURCE_PROOF_2026_04_28.md`
- AP decomposition: `docs/S6_AP_BATCH_AUTHORITY_DECOMPOSITION_2026_04_27.md`
- Current AP implementation chain: `AP-T01`, `AP-T03`, `AP-T04`, `AP-T05`, `AP-T06A`, `AP-T07`, `AP-T10`
- Existing source data: `ResolvedSurfaceContext.audit_trail`

## 3. Decision

```text
AP_T08_NARROW_IMPLEMENTATION_CHECKLIST_HOLD_PENDING_EXTERNAL_AUTHORITY_REVIEW
```

Source legality is proven, but implementation is still authority-sensitive because `AP-T08` defines the approval audit chain boundary between P2 approval events and P3/SH read paths.

## 4. Safe Future Implementation Shape

If external authority review passes, the narrow implementation may be limited to:

- display-only audit source boundary in `/approval`;
- fields derived only from existing `activeContext.audit_trail`;
- no AP state mutation;
- no ActionMode creation;
- no P3 Manager output;
- no Search/History output;
- no fixture/adapter/validator/context changes.

Likely future allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_AP_T08_APPROVAL_AUDIT_CHAIN_CLOSEOUT_2026_04_28.md
```

## 5. Required External Review Question

```text
Can AP-T08 render a display-only approval audit source boundary from existing audit_trail records without creating P2 state-transition authority, P3 manager summary authority, or Search/History source authority?
```

## 6. HOLD Conditions

HOLD remains active if:

- external authority review is unavailable or not PASS / PASS_WITH_NOTES;
- implementation needs new audit fields or fixture changes;
- implementation would create approval audit summary content for P3;
- implementation would expose host raw evidence;
- implementation would add state transitions, timers, backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot.

## 7. Non-Authorization

This checklist does not authorize implementation or Jira Done transition.
