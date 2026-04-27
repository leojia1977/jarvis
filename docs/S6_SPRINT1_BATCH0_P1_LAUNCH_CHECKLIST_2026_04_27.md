# S6 Sprint 1 Batch-0 P1 Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Sprint 1 Batch-0 P1 Launch Checklist 2026-04-27 |
| Status | READY_FOR_BATCH0_RECONCILIATION_CLOSEOUT_NO_NEW_CODE |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Parent gate | `docs\S6_SPRINT0_EXIT_REVIEW_AND_SPRINT1_ENTRY_GATE_2026_04_27.md` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Route | `OPEN_SPRINT1_BATCH0_P1_LAUNCH_CHECKLIST` |

This record launches Sprint 1 Batch-0 P1 review at the ticket-readiness level.

It does not authorize new code implementation, backend/runtime/API/schema changes, real data, secrets, deployment, public endpoint work, external pilot execution, or Jira cloud mutation.

## 2. Decision

Decision:

```text
READY_FOR_BATCH0_RECONCILIATION_CLOSEOUT_NO_NEW_CODE
```

Meaning:

- The five candidate Sprint 1 Batch-0 tracker tickets are valid first-batch P1 tickets.
- Current repo implementation and tests already cover the baseline behavior for all five tickets.
- The next safe action is a docs/Jira reconciliation closeout, not duplicate UI implementation.
- Jira cloud updates require separate explicit authorization before mutation.

## 3. Candidate Batch

Batch-0 candidate tickets from Backlog Tracker v0.4:

| Ticket | Tracker summary | Tracker implementor | Tracker execution surface | Current launch result |
| --- | --- | --- | --- | --- |
| `GS-T01` | Global conversation input shell | `swe` | `swe` | Already covered by current global query shell and tests. |
| `GS-T02` | Role-cropped primary navigation | `codex` | `codex` | Already covered by role-filtered nav and tests. |
| `GS-T03` | Global coverage badge and text placeholder | `swe` | `swe` | Already covered by coverage badge and tests. |
| `IN-T05` | Inbox to Case Detail case-first route | `codex` | `codex` | Already covered by `/case/:caseId` navigation and tests. |
| `CD-T03` | Persistent in-case follow-up input | `swe` | `swe` | Already covered by Dialogue Dock / follow-up input behavior and tests. |

Tracker note:

```text
Backlog Tracker v0.4 still records allowed files and test commands as TBD for these tickets.
This checklist resolves them for reconciliation purposes only.
```

## 4. Repo Evidence

Current implementation evidence:

| Ticket | Evidence in `frontend/src/App.tsx` | Evidence in `frontend/src/App.test.tsx` |
| --- | --- | --- |
| `GS-T01` | `global-query` topbar form and `Global conversation input` label. | `renders the global conversation input and coverage badge`. |
| `GS-T02` | `NAV_ITEMS` role filtering through `item.roles.includes(role)`. | `crops P1 navigation without disabled forbidden links`; `updates visible navigation when role changes`. |
| `GS-T03` | `coverage-badge` renders `Coverage {activeCase.coverage}`. | `renders the global conversation input and coverage badge`; fixture authority test rejects URL/storage coverage injection. |
| `IN-T05` | `navigate("case", nextCaseId)` normalizes opened cases to `/case/:caseId`. | `opens a case from Inbox into the case-first detail route`. |
| `CD-T03` | `Case dialogue dock` form remains visible on Case Detail. | `renders the P1 Case Detail layout regions and narrative spine`; `keeps the Dialogue Dock source-boundary local without hardcoded recommendation chips`. |

Latest closeout evidence:

- P1-CD-C closed as `IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_COMMITTED_PUSHED`.
- P1-CD-D closed as `IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_COMMITTED_PUSHED`.
- Latest P1-CD-D gate passed frontend tests, frontend build, backend guard, `git diff --check`, and Claude Code focused review.

## 5. AI_COLLAB Field Resolution

For reconciliation closeout, actual implementation authority is:

| Field | Resolution |
| --- | --- |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review from the underlying P1-CD-A/B/C/D implementation chain |
| Review surface | `claude-cmd` |
| External review | Not required unless Go/No-Go Section 9 or AI_COLLAB external-review triggers fire |
| SWE | Not used for realized implementation; tracker `swe` suggestions for `GS-T01`, `GS-T03`, and `CD-T03` must be reconciled to actual closeout evidence |

Reason:

The realized implementation predates this Batch-0 tracker reconciliation and was executed by Codex under exact bounded P1-CD tickets. Reopening the same UI behavior under SWE would duplicate scope and create drift risk.

## 6. Resolved Allowed Files

For reconciliation closeout only:

- `docs/S6_SPRINT1_BATCH0_P1_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`

Already implemented code evidence lives in:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

No new code file is authorized by this launch checklist.

If a later hardening ticket discovers a real gap, it must create a new exact bounded ticket with a new allowed-file list.

## 7. Resolved Test Command

For reconciliation evidence:

```powershell
cd frontend
npm run test -- --run
npm run build
```

Backend guard:

```powershell
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
```

Repo hygiene:

```powershell
git diff --check
```

For this docs-only launch checklist, `git diff --check` is sufficient before commit. Full frontend/backend gates are required only if a follow-up code or closeout claim refreshes implementation evidence.

## 8. Batch-0 Reconciliation Criteria

The reconciliation closeout may mark the five tickets as covered only if it records:

- `GS-T01` global conversation input shell exists and is tested;
- `GS-T02` P1/P2 role navigation cropping exists and is tested;
- `GS-T03` coverage badge exists, uses resolved context coverage, and is tested against URL/storage injection;
- `IN-T05` Inbox opens a case through `/case/:caseId` and is tested;
- `CD-T03` in-case follow-up input / Dialogue Dock remains visible and is tested;
- no P1 approval authority, `IMMEDIATE`, `DELAYED`, `OBSERVE_ONLY`, P2 decision composer, backend/runtime/API/schema, real-data, secrets, deploy, or external pilot behavior is introduced;
- tracker/Jira field reconciliation does not claim SWE implementation where actual implementation evidence is Codex.

## 9. HOLD Conditions

HOLD if:

- any of the five tickets requires new code to satisfy its acceptance criteria;
- implementation files are changed under this checklist;
- tracker reconciliation attempts to mark unrelated Sprint 1 tickets complete;
- Jira cloud mutation is attempted without explicit Jarvis authorization;
- a discrepancy is found between Backlog Tracker v0.4, current repo behavior, and P1 product source;
- a ticket requires P2/P3 ratification, route handoff, cross-surface propagation, E0-04D state-sync harness, backend/runtime/API/schema changes, real data, secrets, deploy, public endpoint, or external pilot;
- Claude Code review evidence is claimed beyond the underlying implemented P1-CD ticket chain.

## 10. Next Safe Action

Next safe automation action:

```text
OPEN_SPRINT1_BATCH0_P1_RECONCILIATION_CLOSEOUT
```

Recommended closeout scope:

- docs-only route/handoff update;
- optional local Jira delta notes;
- Jira cloud sync only after explicit Jarvis authorization;
- no code changes unless a new exact gap ticket is created.
