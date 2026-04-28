# S6 AP-T03 Authority Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T03` |
| Title | Approval CTA/action boundary authority checklist |
| Status | CHECKLIST_ONLY_IMPLEMENTATION_NOT_AUTHORIZED |
| Date | 2026-04-28 |
| Primary implementor | Codex for checklist only |
| Execution surface | codex |
| Reviewer | Not required for docs-only checklist |
| Review surface | n/a |
| Workspace | VS Code / local repo |
| Source inputs | `docs\S6_AP_BATCH_AUTHORITY_DECOMPOSITION_2026_04_27.md`, `docs\S6_P2_P3_AUTHORITY_REVIEW_PACK_2026_04_27.md` |

This checklist determines whether `AP-T03` can later become a bounded implementation ticket.

It does not authorize implementation, approval controls, state transition, confirmation modal, observation-window behavior, approval audit, backend/runtime/API/schema changes, fixture/adapter/validator changes, `ResolvedSurfaceContext` changes, real data, secrets, deploy, public endpoint, or external pilot.

## 2. Current Preconditions

Closed predecessors:

| Ticket | Evidence |
| --- | --- |
| `AP-T01` | `/approval` route shell/guard implemented; no approval controls or transitions. |
| `AP-T10` | Display-only AR status badge/pill mapping implemented. |

Still unresolved:

- exact CTA attach rules;
- exact P2-only action authority;
- whether Claude Web architecture/governance review is mandatory before implementation;
- exact allowed files and test command for any later implementation.

## 3. Authority Questions

Before implementation GO, answer all:

1. Which AR states may render approval CTAs?
2. Are CTAs allowed only when `role=P2`, `surface=approval`, and `ARInteractiveStatus=PENDING_APPROVAL`?
3. Must P0 readonly approval render no CTA at all?
4. Must P1 and P3 be prevented from attaching CTA DOM, not merely hiding it?
5. Which CTAs are in scope for AP-T03: approve/reject/delay/observe labels only, or action wiring?
6. Can CTA rendering exist without creating `ActionMode` or state transition?
7. What is the fail-closed behavior when AR context is missing or not actionable?

## 4. Tentative GO Conditions For A Later Implementation

`AP-T03` may move to implementation GO only if a later launch checklist proves:

```text
CTA attach rules are exact: YES
P2-only action authority is exact: YES
P0/P1/P3 non-attachment is testable: YES
Action wiring/state mutation is out of scope or separately authorized: YES
Allowed files are exact: YES
Test command is exact: YES
Claude Web review requirement resolved: YES
No backend/runtime/API/schema change required: YES
No fixture/adapter/validator/ResolvedSurfaceContext change required: YES
```

## 5. Required Tests For A Later Implementation

Future implementation tests should prove:

- P2 + approval surface + `PENDING_APPROVAL` can attach bounded CTA region;
- P0 readonly approval attaches no approval CTA;
- P1 and P3 attach no approval CTA;
- URL/storage/query cannot create CTA authority;
- missing AR context renders safe unavailable or guarded state;
- CTA display does not mutate state.

## 6. External Review

External architecture/governance review is recommended before implementation because `AP-T03` is the first real AP action-control boundary.

Review focus:

- P2-only action authority;
- P1/P3/P0 CTA non-attachment;
- no `ActionMode` or state transition creation;
- URL/storage non-authority;
- no backend/runtime/API/schema.

## 7. Decision

Decision:

```text
CHECKLIST_PASS_IMPLEMENTATION_REQUIRES_CLAUDE_WEB_OR_HUMAN_AUTHORITY_REVIEW_AND_SEPARATE_GO
```

Implementation status:

```text
NOT_AUTHORIZED
```

## 8. Next Safe Action

```text
REQUEST_AP_T03_AUTHORITY_REVIEW_OR_AUTHORIZE_AP_T03_IMPLEMENTATION_ONLY_AFTER_REVIEW_PASS
```

