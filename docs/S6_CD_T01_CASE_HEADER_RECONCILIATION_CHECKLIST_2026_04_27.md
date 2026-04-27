# S6 CD-T01 Case Header Reconciliation Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 CD-T01 Case Header Reconciliation Checklist 2026-04-27 |
| Ticket | `CD-T01` |
| Scope | Case header with `caseId / verdict / coverage / case_state` |
| Status | RECONCILIATION_HOLD_PENDING_EXACT_IMPLEMENTATION_GO |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Route | `OPEN_CD_T01_CASE_HEADER_RECONCILIATION_CHECKLIST` |
| Primary implementor | Codex for checklist only |
| Execution surface | `codex` |
| Reviewer | Not required for checklist-only reconciliation |
| Review surface | `not_required_no_implementation_diff` |
| External review | not required unless later implementation triggers Go/NoGo Section 9 |
| SWE | disabled |

This checklist evaluates whether current repo behavior is sufficient to close Backlog Tracker v0.4 row `CD-T01`.

It does not authorize code implementation, Jira Done transition, backend/runtime/API/schema changes, real data, secrets, deployment, public endpoint work, or external pilot execution.

## 2. Decision

Decision:

```text
RECONCILIATION_HOLD_PENDING_EXACT_IMPLEMENTATION_GO
```

Meaning:

- Current repo behavior partially covers the row.
- It is not sufficient to close `CD-T01` without a focused implementation or visual/semantic reconciliation decision.
- The ticket must stop before implementation GO.

## 3. Current Repo Evidence

Current coverage:

- `CaseDetail` renders a `.case-header` with `activeCase.id`, `activeCase.title`, and `case_state` pill.
- The top bar renders a global `Coverage L*` badge.
- The left Case Lifecycle rail repeats coverage and case_state.
- The narrative summary panel renders the verdict in the first-screen narrative spine.

## 4. Gap Assessment

| Required CD-T01 field | Current placement | Reconciliation result |
| --- | --- | --- |
| `caseId` | Case header | Covered |
| `case_state` | Case header pill and Case Lifecycle rail | Covered |
| `coverage` | Topbar badge and Case Lifecycle rail, not the header | Partial |
| `verdict` | Summary panel, not the header | Partial |

The tracker row asks for a case header containing `caseId / verdict / coverage / case_state`. Current repo behavior distributes verdict and coverage outside the header. That may be acceptable after product/design ratification, but it should not be silently closed as `CD-T01`.

## 5. Required Next Step

Open a separate exact implementation or reconciliation decision if Jarvis wants to close `CD-T01`.

Candidate bounded implementation, if later authorized:

- allowed files: `frontend/src/App.tsx`, `frontend/src/App.css`, `frontend/src/App.test.tsx`, route/handoff, and this checklist;
- add header-level coverage and verdict treatment without changing route, context, fixture, adapter, validator, backend/runtime/API/schema, or P2/P3 authority;
- preserve existing summary panel and Case Lifecycle rail.

## 6. HOLD Conditions

HOLD if:

- implementation requires visual-frame interpretation beyond exact text placement;
- the ticket attempts to redesign the Case Detail layout;
- implementation touches P2/P3, route handoff, backend/runtime/API/schema, real data, secrets, deployment, public endpoint, or external pilot behavior;
- allowed files or tests cannot be exact.

## 7. Jira Sync

Jira cloud mutation:

```text
NOT_SYNCED_NOT_DONE
```

Reason: `CD-T01` is not closeout-ready. Do not mark Done from current evidence.

## 8. Next Safe Action

Next safe automation action:

```text
OPEN_CD_T02_SUMMARY_LAYER_RECONCILIATION_CHECKLIST
```

