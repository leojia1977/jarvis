# S6 AP-T10 Patch-Isolation Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 AP-T10 Patch-Isolation Checklist 2026-04-27 |
| Ticket | `AP-T10` |
| Scope | `ARInteractiveStatus / ActionMode badge-pill display mapping readiness only` |
| Status | PATCH_ISOLATION_CHECKLIST_PASS_IMPLEMENTATION_REQUIRES_SEPARATE_GO |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Authority pack | `docs\S6_P2_P3_AUTHORITY_REVIEW_PACK_2026_04_27.md` |
| Claude Web review | `docs\S6_P2_P3_AUTHORITY_CLAUDE_WEB_REVIEW_2026_04_27.md` |
| Staged authorization | `docs\S6_STAGED_ACCELERATION_AUTHORIZATION_2026_04_27.md` |
| Primary implementor | Codex if later implementation GO is granted |
| Execution surface | codex |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review if implementation diff exists |
| Review surface | claude-cmd |
| External review | satisfied for readiness by Claude Web `PASS`; re-trigger if HOLD condition fires |
| SWE | disabled |

This checklist is a readiness and isolation record only. It does not implement `AP-T10` and does not authorize broad P2 Approval Surface work.

## 2. Checklist Decision

Decision:

```text
PATCH_ISOLATION_CHECKLIST_PASS_IMPLEMENTATION_REQUIRES_SEPARATE_GO
```

Interpretation:

- `AP-T10` is a valid isolated candidate for a later narrow implementation.
- Implementation is not started by this checklist.
- A later explicit `AP-T10 implementation GO` is still required before code changes.

## 3. Authority Evidence

Claude Web architecture/governance review returned `PASS` for `AP-T10` and confirmed:

- D-02 is the only authority for AR status / ActionMode enum meaning.
- Model Contract and UI mapping tables are derivative and must not create parallel authority.
- `ARInteractiveStatus` display must not create or change `ActionMode`.
- `PENDING_APPROVAL` is the only actionable state and only for P2.
- `APPROVED_PENDING_EXECUTION`, `OBSERVATION_WINDOW`, `REJECTED`, `WITHDRAWN`, and `CANCELLED` are display-only for this ticket.
- Badge/pill UI must not imply automatic state migration through arrows, progress bars, or next-step language.
- Visual severity is allowed only when derived from the governed D-02 frontend interaction classification.
- Frozen enum labels are governed labels, not `ui_messages` dynamic copy.

## 4. Future Implementation Scope If Separately Authorized

A later implementation may do only:

- a display-only AR status badge / pill mapping for existing `ARStatus` values;
- a clear distinction between `PENDING_APPROVAL` as actionable only for P2 and all other AR statuses as display-only;
- stable test ids and semantic attributes proving display-only behavior;
- regression tests proving P1 cannot select `ActionMode`, URL/storage cannot set AR status, and badge/pill rendering does not attach approve / reject / delay / observe controls.

## 5. Exact Non-Goals

Do not implement:

- AP route, `/approval` shell, landing page, role guard, or default routing (`AP-T01`);
- approve/reject/delay/observe CTA, confirmation modal, state mutation, observation-window countdown, stale-approve handling, approval audit, or AP acceptance suite;
- `ActionMode` creation, selection, mutation, or inferred defaulting;
- state migration, progress arrows, automatic transition language, or next-step guidance;
- new D-02 enum values, new labels, new severity categories, or parallel mapping authority;
- `ui_messages` dynamic copy semantics;
- P1, P3, Manager View, Search/History, Coverage & Health, route handoff, or cross-surface data flow;
- fixture registry changes, fixture adapter changes, validator changes, or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema changes;
- Storybook, Playwright, real data, anonymized real data, secrets, deploy, public endpoint, or external pilot.

## 6. Exact Files For Later Narrow Implementation

If separately authorized, implementation must stay inside:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

No other implementation files are currently justified by this checklist.

Governance files for a later implementation closeout may include:

```text
docs/S6_AP_T10_PATCH_ISOLATION_CHECKLIST_2026_04_27.md
docs/S6_AP_T10_DISPLAY_MAPPING_CLOSEOUT_2026_04_27.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

## 7. Required Gate For Later Implementation

Minimum gate:

```powershell
cd frontend
npm run test -- --run
npm run build
cd ..
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
git diff --check
```

Claude Code focused review is required for any implementation diff.

## 8. HOLD Conditions

HOLD immediately if:

- implementation needs files outside the exact list;
- implementation needs AP route, approval controls, state transition behavior, confirmation modal, audit chain, observation-window countdown, or stale-approve handling;
- D-02, Model Contract, PRD, visual-frame, or Go/NoGo conflict appears;
- implementation needs new enum values, labels, severity categories, `ui_messages` dynamic copy semantics, or parallel mapping authority;
- implementation needs URL/storage/route params as authority;
- implementation needs P1 `ActionMode` choice or any non-P2 action authority;
- implementation needs P2/P3 authority expansion beyond the display mapping;
- implementation needs fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- implementation needs backend/runtime/API/schema work;
- tests/build fail and cannot be corrected inside the exact ticket scope;
- Claude Code review raises a blocking finding;
- any mandatory external-review trigger fires.

## 9. Next Safe Action

Next safe action:

```text
WAIT_FOR_AP_T10_IMPLEMENTATION_GO_OR_OPEN_AP_T01_PATCH_ISOLATION_CHECKLIST
```
