# S6 MV/SH Audit Authority Map 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 MV/SH Audit Authority Map 2026-04-27 |
| Status | LOW_RISK_QUEUE_OUTPUT_AUTHORITY_MAP |
| Queue item | `LR-06` |
| Date | 2026-04-27 |
| Tickets mapped | `MV-T03`, `MV-T04`, `MV-T05`, `SH-T08` |

This map identifies approval-audit and Search/History authority dependencies before any Manager or audit follow-up implementation.

It does not authorize route handoff, approval audit implementation, host raw evidence rendering, backend/runtime/API/schema changes, fixture changes, real data, secrets, deploy, public endpoint, or external pilot.

## 2. Current Baseline

Closed:

| Ticket | Relevant evidence |
| --- | --- |
| `MV-T01` | P3-only Manager structure implemented; no P0/P2 variants; no approval audit summary. |
| `SH-T05` | Readonly focus scopes implemented. |
| `SH-T07` | Write CTA absence reconciled. |
| `CD-T05` | P3 executive summary implemented without raw host evidence. |

Not closed:

```text
AP-T08 approval audit chain
MV-T03 manager deep-link handoff
MV-T04 P3 approval audit summary
MV-T05 manager acceptance
SH-T08 P3 approval-audit source/data availability
```

## 3. Authority Rules

| Rule | Consequence |
| --- | --- |
| P3 host raw evidence must remain absent from DOM | Use `not.toBeAttached()` style assertions when implemented. |
| Approval audit source path must be explicit | No audit summary can infer from UI strings or route params. |
| URL/storage cannot create Manager or audit authority | Handoff must use governed context/data source only. |
| Deep-link handoff is its own scope | `MV-T03` must not be smuggled into `MV-T01` or `MV-T04`. |
| Acceptance tickets close last | `MV-T05` cannot close until chain evidence exists. |

## 4. Ticket Map

| Ticket | Primary authority question | Dependencies | Current state |
| --- | --- | --- | --- |
| `MV-T03` | What source may deep-link Search/History to Manager without URL/storage authority? | `MV-T01`, SH source rules | Needs authority checklist |
| `MV-T04` | What exact approval-audit fields may P3 summarize without raw host evidence? | `AP-T08`, P3 raw-evidence guard | Needs authority checklist |
| `MV-T05` | What evidence proves Manager acceptance? | `MV-T01`, `MV-T03`, `MV-T04` | Not safe to start |
| `SH-T08` | What Search/History source may expose P3 approval-audit availability? | `SH-T05`, `AP-T08` | Needs authority checklist |

## 5. Recommended Checklist Order

```text
AP-T08 authority checklist
SH-T08 authority checklist
MV-T03 authority checklist
MV-T04 authority checklist
MV-T05 acceptance checklist
```

Reason:

- AP audit source legality should be known before SH or MV reads it.
- SH-T08 can then define Search/History source availability.
- MV-T03 and MV-T04 can consume defined sources without inventing route or audit authority.
- MV-T05 should remain acceptance-only at the end.

## 6. Claude Web Review Prompt

```text
Review MV/SH audit authority only.

Scope:
- AP-T08 source legality as prerequisite;
- SH-T08 P3 approval-audit source availability;
- MV-T03 deep-link handoff boundary;
- MV-T04 P3 approval audit summary;
- MV-T05 acceptance dependency.

Check:
- no host raw evidence DOM attachment;
- no URL/storage/route-param authority;
- no backend/runtime/API/schema changes;
- no raw evidence or technical panel leakage;
- no acceptance closeout before dependencies exist.

Decision needed:
- PASS
- PASS_WITH_NOTES
- HOLD
```

