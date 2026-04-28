# S6 AP-T08 Narrow Implementation Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T08` |
| Title | Approval audit chain narrow implementation checklist |
| Status | `READY_FOR_BOUNDED_IMPLEMENTATION_GO_WITH_NOTES` |
| Date | 2026-04-28 |
| Jira | `SCRUM-62` remains `待办` |

## 2. Checklist Inputs

- Source proof: `docs/S6_AP_T08_SH_T08_AUTHORITY_SOURCE_PROOF_2026_04_28.md`
- External authority verdict: `docs/S6_AP_T08_MV_T04_CLAUDE_WEB_AUTHORITY_VERDICT_2026_04_28.md`
- AP decomposition: `docs/S6_AP_BATCH_AUTHORITY_DECOMPOSITION_2026_04_27.md`
- Current AP implementation chain: `AP-T01`, `AP-T03`, `AP-T04`, `AP-T05`, `AP-T06A`, `AP-T07`, `AP-T10`
- Existing source data: `ResolvedSurfaceContext.audit_trail`

## 3. Decision

```text
AP_T08_NARROW_IMPLEMENTATION_CHECKLIST_GO
```

Source legality is proven and Claude Web returned `PASS_WITH_NOTES`.

Implementation may proceed only as a display-only `activeContext.audit_trail` source boundary in `/approval`. Any derived status must use fixed enum mapping.

## 4. Safe Future Implementation Shape

The narrow implementation is limited to:

- display-only audit source boundary in `/approval`;
- fields derived only from existing `activeContext.audit_trail`;
- fixed enum mapping for derived display status;
- no AP state mutation;
- no ActionMode creation;
- no P3 Manager output;
- no Search/History output;
- no fixture/adapter/validator/context changes.

Allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_AP_T08_APPROVAL_AUDIT_CHAIN_CLOSEOUT_2026_04_28.md
```

## 5. Fixed Derived Status Mapping

```text
AR_SUBMITTED -> SUBMITTED
P2_OPENED_AR -> OPENED
OBSERVE_ONLY_SELECTED -> OBSERVING
OBSERVATION_WINDOW_EXPIRED -> WINDOW_EXPIRED
APPROVED_AFTER_WINDOW -> APPROVED
missing event -> UNAVAILABLE
unknown event -> UNSUPPORTED
```

## 6. HOLD Conditions

HOLD if:

- implementation needs new audit fields or fixture changes;
- implementation would create approval audit summary content for P3;
- implementation would expose host raw evidence;
- implementation would add state transitions, timers, backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot.

## 7. Non-Authorization

This checklist does not authorize Jira Done transition by itself. Jira may move only after implementation closeout and gates pass.
