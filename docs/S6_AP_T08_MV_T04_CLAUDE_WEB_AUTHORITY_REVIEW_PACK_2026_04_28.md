# S6 AP-T08 / MV-T04 Claude Web Authority Review Pack 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 AP-T08 / MV-T04 Claude Web Authority Review Pack 2026-04-28 |
| Status | `EXTERNAL_AUTHORITY_REVIEW_PASS_WITH_NOTES_RECORDED` |
| Date | 2026-04-28 |
| Scope | AP-T08 approval audit source boundary + MV-T04 P3 approval audit summary authority review |
| Review surface | Claude Web architecture/governance review |
| Implementation authorization | AP-T08 may proceed to narrow implementation checklist only; MV-T04 remains order-gated |
| Jira | `SCRUM-62` / `SCRUM-68` remain `待办` |

Verdict record:

```text
docs\S6_AP_T08_MV_T04_CLAUDE_WEB_AUTHORITY_VERDICT_2026_04_28.md
```

Verdict summary:

```text
AP-T08: PASS_WITH_NOTES; narrow implementation checklist allowed.
MV-T04: PASS_WITH_NOTES; implementation remains gated by AP-T08 and SH-T08 source/order confirmation.
```

## 2. Why This Review Exists

The continuous burn pool found no safe immediate implementation ticket in the audit lane because:

- `AP-T08` defines the approval audit chain source boundary between P2 approval events and downstream P3/SH readers.
- `MV-T04` consumes approval audit information inside P3 Manager View, which is authority-sensitive and must preserve P3 raw-evidence DOM absence.
- Both tickets can probably move faster if Claude Web confirms the read-only authority boundary and allowed source fields.

This review is intended to turn a HOLD into either:

```text
PASS_READY_FOR_NARROW_IMPLEMENTATION_CHECKLIST
```

or:

```text
HOLD_WITH_EXACT_BLOCKER
```

It does not itself authorize implementation, merge, deploy, real data, secrets, backend/runtime/API/schema, fixture/adapter/validator, or `ResolvedSurfaceContext` changes.

## 3. Current Repo Facts

Closed / implemented evidence:

- `AP-T01`: `/approval` route shell/guard exists; no approval controls or transitions.
- `AP-T03`: inert P2-only CTA boundary exists; state mutation is disabled.
- `AP-T04`: shell-only Strong Confirm modal exists; confirm remains disabled.
- `AP-T05`: delay/observe configuration shell exists; frontend timer authority is none.
- `AP-T06A`: static read-only observation-window skeleton exists; material state sync remains HOLD.
- `AP-T07`: approved-pending locked-state semantic skeleton exists.
- `AP-T10`: D-02 display-only AR badge/pill mapping exists.
- `SH-T05`: Search/History focus scopes exist for `summary`, `approval_audit`, and `history_audit`.
- `SH-T07`: Search/History write CTA absence is reconciled.
- `MV-T01`: P3 Manager View structure exists; no approval audit summary.
- `MV-T03`: P3 Search/History audit-focus route-only handoff to `/manager` exists; no URL/storage/payload authority.
- `CD-T05`: P3 executive summary exists but explicitly keeps approval audit summary `not-implemented`.

Source evidence:

- `ResolvedSurfaceContext.audit_trail` exists and validates as an array of records.
- The fixture contains `AUD-001` through `AUD-005`, including:
  - `AUD-003` / `OBSERVE_ONLY_SELECTED`;
  - `AUD-004` / `OBSERVATION_WINDOW_EXPIRED` / `RETURN_TO_PENDING_APPROVAL`;
  - `AUD-005` / `APPROVED_AFTER_WINDOW`.
- `docs/S6_AP_T08_SH_T08_AUTHORITY_SOURCE_PROOF_2026_04_28.md` records source legality for AP-T08 and SH-T08, but not implementation authorization.

## 4. Review Questions

### Q1 - AP-T08 Source Boundary

Can `AP-T08` render a display-only approval audit source boundary in `/approval` using only existing `activeContext.audit_trail` records?

Constraints:

- no AP state mutation;
- no ActionMode creation;
- no backend/runtime/API/schema;
- no fixture/adapter/validator/ResolvedSurfaceContext changes;
- no P3 Manager summary output;
- no Search/History output;
- no approval audit source invention.

### Q2 - AP-T08 Allowed Fields

If Q1 is PASS, which fields may AP-T08 display?

Candidate field categories:

- latest audit event id;
- latest decision status derived from audit event;
- timestamp if already present;
- actor role badge;
- observation-window presence;
- terminal / locked status;
- unavailable state if the source is missing.

Claude Web should reject any field that would require inference from UI copy, route params, browser storage, host raw evidence, backend calls, or new fixture schema.

### Q3 - MV-T04 Consumption Boundary

Can `MV-T04` render a P3-only read-only approval audit summary inside existing Manager View from the same existing `audit_trail` records?

Constraints:

- no host raw evidence DOM attachment;
- no approval controls;
- no technical panels;
- no P2 confirmation modal content;
- no AP state-transition behavior;
- no URL/storage/route-param authority;
- no serialized handoff payload;
- no backend/runtime/API/schema;
- no fixture/adapter/validator/ResolvedSurfaceContext changes.

### Q4 - Dependency Order

Should the implementation order be:

```text
AP-T08 first -> SH-T08 second -> MV-T04 third
```

or may `MV-T04` proceed after AP-T08 authority review but before SH-T08 implementation?

The current proposed safe order is:

```text
AP-T08 external review PASS
AP-T08 narrow implementation checklist
AP-T08 implementation, if checklist GO
SH-T08 narrow implementation checklist
MV-T04 authority re-check or implementation checklist
```

Claude Web should either accept this order or give a stricter dependency order.

### Q5 - Review Trigger

Does this work require Claude Web review again at implementation closeout?

Default recommendation:

```text
AP-T08 implementation closeout: Claude Code focused review required; Claude Web re-review conditional on scope staying inside approved source-boundary wording.
MV-T04 implementation closeout: Claude Code focused review required; Claude Web re-review required if any summary field, copy, or raw-evidence boundary differs from this pack.
```

## 5. Requested Claude Web Decision Format

Please return one of:

```text
PASS
PASS_WITH_NOTES
HOLD
```

And fill this table:

| Ticket | Decision | Required notes / blockers |
| --- | --- | --- |
| AP-T08 | PASS / PASS_WITH_NOTES / HOLD | ... |
| MV-T04 | PASS / PASS_WITH_NOTES / HOLD | ... |

Also answer:

```text
AP-T08 allowed source fields:
MV-T04 allowed source fields:
Implementation order:
Does AP-T08 need Claude Web closeout re-review:
Does MV-T04 need Claude Web closeout re-review:
```

## 6. Copy-To-Claude-Web Prompt

```text
Claude Web Architecture/Governance Review
S6 AP-T08 / MV-T04 Authority Review Pack 2026-04-28

Review mode:
Architecture/governance boundary check only.
This is not implementation authorization.

Review scope:
AP-T08 approval audit source boundary
MV-T04 P3 approval audit summary authority

Current repo facts:
- AP-T01 route shell/guard exists; no approval controls or transitions.
- AP-T03 inert P2-only CTA boundary exists; state mutation disabled.
- AP-T04 shell-only Strong Confirm modal exists; confirm disabled.
- AP-T05 delay/observe configuration shell exists; frontend timer authority none.
- AP-T06A static read-only observation-window skeleton exists; material state sync remains HOLD.
- AP-T07 approved-pending locked-state semantic skeleton exists.
- AP-T10 D-02 display-only AR badge/pill mapping exists.
- SH-T05 Search/History focus scopes exist for summary, approval_audit, and history_audit.
- SH-T07 Search/History write CTA absence is reconciled.
- MV-T01 P3 Manager View structure exists; no approval audit summary.
- MV-T03 P3 Search/History audit-focus route-only handoff to /manager exists; no URL/storage/payload authority.
- CD-T05 P3 executive summary exists but explicitly keeps approval audit summary not-implemented.
- ResolvedSurfaceContext.audit_trail exists and validates as an array.
- Fixture audit records include AUD-003 OBSERVE_ONLY_SELECTED, AUD-004 OBSERVATION_WINDOW_EXPIRED / RETURN_TO_PENDING_APPROVAL, and AUD-005 APPROVED_AFTER_WINDOW.

Review questions:
1. Can AP-T08 render a display-only approval audit source boundary in /approval using only existing activeContext.audit_trail records, without AP state mutation, ActionMode creation, backend/runtime/API/schema, fixture/adapter/validator/ResolvedSurfaceContext changes, P3 Manager output, Search/History output, or audit source invention?
2. If yes, what exact source fields may AP-T08 display?
3. Can MV-T04 render a P3-only read-only approval audit summary inside existing Manager View from the same existing audit_trail records, without host raw evidence DOM attachment, approval controls, technical panels, P2 confirmation modal content, AP state-transition behavior, URL/storage/route-param authority, serialized handoff payload, backend/runtime/API/schema, or fixture/adapter/validator/ResolvedSurfaceContext changes?
4. Should implementation order be AP-T08 first -> SH-T08 second -> MV-T04 third, or may MV-T04 proceed after AP-T08 authority review but before SH-T08 implementation?
5. Does AP-T08 or MV-T04 need Claude Web closeout re-review if implementation stays within this approved boundary?

Decision needed:
- PASS
- PASS_WITH_NOTES
- HOLD

Please return:
| Ticket | Decision | Required notes / blockers |
| AP-T08 | ... | ... |
| MV-T04 | ... | ... |

Also answer:
AP-T08 allowed source fields:
MV-T04 allowed source fields:
Implementation order:
Does AP-T08 need Claude Web closeout re-review:
Does MV-T04 need Claude Web closeout re-review:

This review does not authorize launch, deploy, real data, secrets, backend/runtime/API/schema, fixture/adapter/validator/ResolvedSurfaceContext changes, or external pilot.
```

## 7. Post-Review Actions

If Claude Web returns `PASS` or `PASS_WITH_NOTES` for AP-T08:

```text
OPEN_AP_T08_APPROVAL_AUDIT_SOURCE_BOUNDARY_IMPLEMENTATION_CHECKLIST
```

If Claude Web returns `PASS` or `PASS_WITH_NOTES` for MV-T04:

```text
KEEP_MV_T04_PENDING_UNTIL_AP_T08_AND_SH_T08_ORDER_IS_CONFIRMED
```

If Claude Web returns `HOLD`:

```text
KEEP_AP_T08_MV_T04_HOLD_AND_RECORD_BLOCKERS_IN_ROUTE_HANDOFF_JIRA
```
