# S6 AP-T01 Patch-Isolation Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 AP-T01 Patch-Isolation Checklist 2026-04-27 |
| Ticket | `AP-T01` |
| Scope | `/approval route, default landing, role guard readiness only` |
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

This checklist is a readiness and isolation record only. It does not implement `/approval`, does not mark `AP-T01` Done, and does not authorize broad P2 Approval Surface work.

## 2. Checklist Decision

Decision:

```text
PATCH_ISOLATION_CHECKLIST_PASS_IMPLEMENTATION_REQUIRES_SEPARATE_GO
```

Interpretation:

- `AP-T01` is a valid isolated candidate for a later narrow route-shell / guard implementation.
- Implementation is not started by this checklist.
- A later explicit `AP-T01 implementation GO` is still required before code changes.
- Future implementation must prove that route shell / guard behavior can be added without implementing approval controls, state transitions, Manager View, backend/runtime/API/schema, or cross-surface handoff.

## 3. Authority Evidence

Claude Web architecture/governance review returned `PASS` for `AP-T01` and confirmed:

- P2 may enter `/approval` as the primary work surface.
- P0 may enter a read-only approval container.
- P1 must hard-redirect to `/inbox`.
- P3 must hard-redirect to `/manager`.
- AP shell may render a safe empty/loading state when AR context is missing, but no approval CTA or action area may render.
- `AP-T01` is route + guard + landing only.
- CTA and state migration behavior remain later AP ticket scope.
- Route guard must read role from `ResolvedSurfaceContext`, not URL, query, route params, localStorage, or sessionStorage.
- Missing AR context must render SH-08 or data-unavailable safe state, not guessed AP state.

## 4. Future Implementation Scope If Separately Authorized

A later implementation may do only:

- add a bounded `/approval` route shell and role guard;
- activate the existing `Approval Queue` navigation only where the resolved role is eligible;
- render P2 shell / landing content without approve, reject, delay, observe, close, or execute controls;
- render P0 read-only shell / landing content if the resolved context provides P0 authority;
- hard redirect P1 to `/inbox`;
- hard redirect P3 to `/manager` without implementing Manager View content in this ticket;
- render SH-08 or data-unavailable safe state when AR context is missing;
- add stable test ids and semantic attributes proving route authority comes from `ResolvedSurfaceContext`;
- add regression tests proving URL/storage/route params do not grant AP role/action authority and non-P2 cannot operate approval actions.

## 5. Exact Non-Goals

Do not implement:

- approve/reject/delay/observe CTA, confirmation modal, state mutation, observation-window countdown, stale-approve handling, approval audit, or AP acceptance suite;
- `AP-T10` badge / pill display mapping unless separately authorized;
- `ActionMode` creation, selection, mutation, inferred defaulting, or P1 action authority;
- P2 state migration, progress arrows, automatic transition language, or next-step guidance;
- Manager View page content, P0/P2 Manager variants, manager KPI cards, deep-link handoff, or approval audit summary;
- P1, P3, Search/History, Coverage & Health, cross-surface data flow, or route handoff beyond the `/approval` guard;
- new D-02 enum values, new labels, new severity categories, or parallel mapping authority;
- `ui_messages` dynamic copy semantics;
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
docs/S6_AP_T01_PATCH_ISOLATION_CHECKLIST_2026_04_27.md
docs/S6_AP_T01_APPROVAL_ROUTE_GUARD_CLOSEOUT_2026_04_27.md
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
- implementation needs approval controls, state transition behavior, confirmation modal, audit chain, observation-window countdown, stale-approve handling, or AP acceptance suite;
- implementation needs Manager View content, Manager route content, Manager KPI cards, deep-link handoff, or P0/P2 Manager variants;
- P3 hard redirect to `/manager` cannot be implemented without creating Manager View scope;
- D-02, Model Contract, PRD, visual-frame, route spec, or Go/NoGo conflict appears;
- implementation needs new enum values, labels, severity categories, `ui_messages` dynamic copy semantics, or parallel mapping authority;
- implementation needs URL/storage/route params as role, surface, AR, or action authority;
- implementation needs P1 `ActionMode` choice or any non-P2 action authority;
- implementation needs P2/P3 authority expansion beyond route shell / guard behavior;
- implementation needs fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- implementation needs backend/runtime/API/schema work;
- tests/build fail and cannot be corrected inside the exact ticket scope;
- Claude Code review raises a blocking finding;
- any mandatory external-review trigger fires.

## 9. Next Safe Action

Next safe action:

```text
WAIT_FOR_AP_T01_IMPLEMENTATION_GO_OR_OPEN_CD_T05_P2P3_READINESS_CHECKLIST
```
