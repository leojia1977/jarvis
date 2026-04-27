# S6 IN-T01 Inbox Base Structure Reconciliation Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 IN-T01 Inbox Base Structure Reconciliation Checklist 2026-04-27 |
| Ticket | `IN-T01` |
| Scope | Inbox list base structure and minimal fields |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED |
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

This checklist evaluates and records closeout for Backlog Tracker v0.4 row `IN-T01`.

Implementation was authorized by Jarvis as part of the bounded Sprint 1 burn-down queue.

## 2. Decision

Decision:

```text
IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED
```

Meaning:

- Current repo behavior includes an Inbox skeleton and case-first open path.
- Queue-oriented copy has been removed.
- `IN-T01` is closed as implemented and Jira Done synced.

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
| No work-queue affordance | `Case-first intake`; test rejects queue language | Covered |
| VF-02 visual alignment | Not ratified in this ticket | Partial |

The current implementation is sufficient for IN-T01 bounded closeout. Full VF-02 polish remains outside this ticket.

## 5. Required Next Step

Authorized implementation:

- changed Inbox heading from `Current case queue` to `Case-first intake`;
- added a stable `case-first-inbox-list` test target;
- preserved existing case cards and `Open case` route behavior;
- added regression assertions that queue/work-queue/approval-queue affordance does not appear.

## 6. HOLD Conditions

HOLD if:

- implementation introduces work-queue, approval queue, P2 quick approval, or P3 management semantics;
- implementation changes route authority, fixtures, adapter, validator, backend/runtime/API/schema, real data, secrets, deployment, public endpoint, or external pilot behavior;
- allowed files or tests cannot be exact.

## 7. Jira Sync

Jira cloud sync:

```text
SCRUM-28 [IN-T01] Inbox base structure and minimal fields
Parent: SCRUM-7
Status: 已完成
```

## 8. Implementation Closeout

Implemented files:

```text
frontend/src/App.tsx
frontend/src/App.test.tsx
```

Gate evidence:

```text
frontend tests: PASS, 58 tests
frontend build: PASS
backend guard: PASS, 42 tests
git diff --check: PASS with Windows line-ending warnings only
Claude Code focused review: PASS
```

External review:

```text
NOT_REQUIRED
```

Reason: IN-T01 did not change architecture/governance authority, P1/P2/P3 authority, route authority, fixture/adapter/validator behavior, backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot behavior.

## 9. Next Safe Action

Next safe automation action:

```text
OPEN_CD_T01_CASE_HEADER_IMPLEMENTATION
```
