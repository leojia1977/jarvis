# S6 MV-T02 Authority Model Pack 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `MV-T02` |
| Title | P0/P2 degraded readonly Manager variant authority model pack |
| Status | LOW_RISK_QUEUE_OUTPUT_AUTHORITY_HOLD_REMAINS |
| Queue item | `LR-04` |
| Date | 2026-04-27 |
| Current checklist | `docs\S6_MV_T02_P0_P2_MANAGER_READONLY_VARIANT_READINESS_CHECKLIST_2026_04_27.md` |

This pack prepares the authority questions for `MV-T02`.

It does not authorize implementation, P0/P2 Manager branches, fixture changes, backend/runtime/API/schema changes, or `ResolvedSurfaceContext` changes.

## 2. Current HOLD

Decision remains:

```text
READINESS_CHECKLIST_HOLD_PENDING_MANAGER_VARIANT_AUTHORITY_MODEL
```

Why:

- `MV-T01` intentionally implemented P3-only Manager View.
- Claude Web review made "no P0/P2 placeholders or conditional branches" a hard guard for `MV-T01`.
- `MV-T02` is the correct future scope for degraded readonly P0/P2 Manager variants.
- Current repo does not define safe P0/P2 Manager data contracts or renderable authority contexts.

## 3. Authority Questions

These questions must be answered before implementation GO:

1. Are P0 and P2 allowed to enter `/manager` at all, or should they remain guarded until a later surface?
2. If allowed, which source document defines the degraded readonly Manager authority?
3. Which fields may P0 see, and which fields may P2 see?
4. Must P0/P2 use the same `manager-summary-root`, or separate readonly shells?
5. What must be absent from DOM for P0/P2 variants?
6. May the current fixture context produce P0/P2 manager renderability without changing fixture/adapter/validator or `ResolvedSurfaceContext`?
7. What is the safe fail-closed behavior when P0/P2 Manager context is missing?

## 4. Non-Negotiable Guards

| Guard | Rule |
| --- | --- |
| MV-T01 isolation | Do not retrofit or reinterpret `MV-T01`; it remains P3-only. |
| Authority source | No URL/storage/route param may create Manager authority. |
| Raw evidence | P3 host raw evidence remains absent; P0/P2 variants must not introduce raw evidence. |
| No workflow expansion | No Manager workflow action, approval action, or deep-link handoff enters `MV-T02`. |
| No placeholder leakage | P0/P2 branches must not be added before the model is approved. |

## 5. Minimum Reopen Conditions

`MV-T02` can move from HOLD to launch checklist only when all are true:

```text
P0/P2 degraded manager authority model approved: YES
P0/P2 renderable manager context exists without URL/storage authority: YES
Allowed source fields are exact: YES
Allowed files are exact: YES
Test command is exact: YES
No fixture/adapter/validator/ResolvedSurfaceContext change is needed inside MV-T02, or that change has separate governed GO: YES
No MV-T03/MV-T04/MV-T05 scope enters MV-T02: YES
```

## 6. Claude Web Review Prompt

```text
Review MV-T02 only: P0/P2 degraded readonly Manager variants.

Check:
- whether P0/P2 may enter /manager at all;
- source authority for degraded readonly manager fields;
- raw evidence DOM absence;
- no URL/storage/route-param authority;
- no retrofit of MV-T01;
- no approval audit summary, deep-link handoff, or workflow actions.

Decision needed:
- PASS
- PASS_WITH_NOTES
- HOLD

This review is not implementation, deployment, real-data, or backend/API authorization.
```

