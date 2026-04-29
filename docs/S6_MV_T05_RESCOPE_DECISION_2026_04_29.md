# S6 MV-T05 Rescope Decision 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `MV-T05` |
| Jira issue | `SCRUM-75` |
| Scope | Manager acceptance rescope decision |
| Status | `MV_T05_RESCOPE_DECISION_OPTION_A_P3_ONLY_ACCEPTANCE_CANDIDATE` |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |

## 2. Decision

```text
MV_T05_RESCOPE_DECISION_OPTION_A_P3_ONLY_ACCEPTANCE_CANDIDATE
```

`MV-T05` may be rescoped to P3-only Manager acceptance over existing P3 Manager
evidence, explicitly excluding P0/P2 Manager variants.

This decision does not close `MV-T05`; it only opens a future exact
reconciliation checklist.

## 3. Rationale

`MV-T02 = OPTION_A` is now implemented as hard redirect / no Manager entry for
non-P3 Manager access. Therefore full cross-role Manager acceptance would be
misleading unless Product creates a new governed P0/P2 Manager field map and
implementation route.

Current completed P3 evidence:

| Dependency | State |
| --- | --- |
| `MV-T01` | P3 Manager structure done. |
| `MV-T03` | Manager deep-link handoff done. |
| `MV-T04` | P3 approval audit summary done. |
| `AP-T08` / `SH-T08` | Source-bound audit evidence done. |
| `MV-T02` | Non-P3 hard redirect / no Manager entry done. |

## 4. Rescoped Acceptance Candidate

Future `MV-T05A` checklist may evaluate:

- P3 Manager structure exists;
- P3 deep-link handoff is source-bound;
- P3 approval audit summary is read-only;
- host raw evidence is not attached;
- P2 evidence drawer is not mounted;
- P0/P2 Manager access redirects rather than rendering placeholders;
- URL/storage do not create Manager authority.

## 5. Explicit Exclusion

The rescoped `MV-T05` must not claim:

- P0/P2 Manager degraded readonly variant;
- P0/P2 Manager field mapping;
- P0/P2 Manager placeholder slots;
- cross-role Manager acceptance.

## 6. Jira

`SCRUM-75` was created and intentionally left `待办`.

No Jira Done transition is allowed until a future exact `MV-T05A` or equivalent
reconciliation checklist returns PASS.

## 7. Next Route

```text
OPEN_MV_T05A_P3_ONLY_MANAGER_ACCEPTANCE_RECONCILIATION_CHECKLIST
```

