# S6 IN-T01 Inbox Base Structure Reconciliation Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 IN-T01 Inbox Base Structure Reconciliation Checklist 2026-04-27 |
| Ticket | `IN-T01` |
| Scope | Inbox list base structure and minimal fields |
| Status | RECONCILIATION_HOLD_PENDING_EXACT_IMPLEMENTATION_GO |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Route | `OPEN_IN_T01_INBOX_BASE_STRUCTURE_RECONCILIATION_CHECKLIST` |
| Primary implementor | Codex for checklist only |
| Execution surface | `codex` |
| Reviewer | Not required for checklist-only reconciliation |
| Review surface | `not_required_no_implementation_diff` |
| External review | not required unless later implementation triggers Go/NoGo Section 9 |
| SWE | disabled |

This checklist evaluates whether current repo behavior is sufficient to close Backlog Tracker v0.4 row `IN-T01`.

It does not authorize code implementation, Jira Done transition, backend/runtime/API/schema changes, real data, secrets, deployment, public endpoint work, or external pilot execution.

## 2. Decision

Decision:

```text
RECONCILIATION_HOLD_PENDING_EXACT_IMPLEMENTATION_GO
```

Meaning:

- Current repo behavior includes an Inbox skeleton and case-first open path.
- It is not sufficient to close `IN-T01` because the tracker note explicitly warns against work-queue affordance, and the current copy still includes queue-oriented language.

## 3. Current Repo Evidence

Current coverage:

- `InboxView` renders a page heading and case cards.
- Each case card renders risk, coverage, title, verdict, next step, and an `Open case` button.
- Existing tests prove an Inbox case opens into `/case/CASE-2847`.

## 4. Gap Assessment

| IN-T01 requirement | Current placement | Reconciliation result |
| --- | --- | --- |
| Base Inbox list structure | `InboxView` / `.case-grid` | Covered |
| Minimal fields | risk, coverage, title, verdict, next step | Covered |
| Case-first open path | `Open case` to Case Detail | Covered by `IN-T05` / tests |
| No work-queue affordance | Current copy says `Current case queue` | Not closed |
| VF-02 visual alignment | Not ratified in this ticket | Partial |

The current implementation is close, but `IN-T01` should not be marked Done while the surface still uses queue-oriented wording that may conflict with the tracker note `不出现工作队列 affordance`.

## 5. Required Next Step

Open a separate exact implementation if Jarvis wants to close `IN-T01`.

Candidate bounded implementation, if later authorized:

- allowed files: `frontend/src/App.tsx`, `frontend/src/App.css`, `frontend/src/App.test.tsx`, route/handoff, and this checklist;
- replace queue-oriented copy with case-first Inbox wording;
- preserve existing case cards and `Open case` route behavior;
- do not add approval controls or work-queue semantics.

## 6. HOLD Conditions

HOLD if:

- implementation introduces work-queue, approval queue, P2 quick approval, or P3 management semantics;
- implementation changes route authority, fixtures, adapter, validator, backend/runtime/API/schema, real data, secrets, deployment, public endpoint, or external pilot behavior;
- allowed files or tests cannot be exact.

## 7. Jira Sync

Jira cloud mutation:

```text
NOT_SYNCED_NOT_DONE
```

Reason: `IN-T01` is not closeout-ready. Do not mark Done from current evidence.

## 8. Next Safe Action

Next safe automation action:

```text
OPEN_CD_T04_HONESTY_LAYER_LAUNCH_CHECKLIST
```

