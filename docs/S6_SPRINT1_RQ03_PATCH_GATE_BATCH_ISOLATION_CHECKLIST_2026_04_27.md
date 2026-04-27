# S6 Sprint 1 RQ-03 Patch-Gate Batch Isolation Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Sprint 1 RQ-03 Patch-Gate Batch Isolation Checklist 2026-04-27 |
| Queue item | `RQ-03` |
| Status | PATCH_GATE_BATCH_ISOLATION_SH_T03_IMPLEMENTED_GATE_PASS |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Parent records | `docs\S6_SPRINT1_RQ01_REMAINING_STATUS_RECONCILIATION_2026_04_27.md`; `docs\S6_SH_T03_PATCH_GATE_ISOLATED_LAUNCH_CHECKLIST_2026_04_27.md` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Route | `OPEN_PATCH_GATE_BATCH_ISOLATION_CHECKLIST` |

This record isolates patch-gate possible work from normal Sprint 1 burn-down.

It does not authorize broad patch-gate batch implementation, backend/runtime/API/schema changes, real data, secrets, deployment, public endpoint work, or external pilot execution.

## 2. Decision

Decision:

```text
PATCH_GATE_BATCH_ISOLATION_SH_T03_IMPLEMENTED_GATE_PASS
```

Meaning:

- Patch-gate filtering was relaxed only for `SH-T03`.
- `SH-T03` was isolated from normal Sprint 1 burn-down.
- No other patch-gate possible row is authorized by this checklist.
- `SH-T03` implementation is complete, gated, Claude Code reviewed, and Jira-synced.

## 3. Isolated Ticket

| Ticket | Scope | Isolation decision |
| --- | --- | --- |
| `SH-T03` | `history route resolve -> clamp -> guard -> render` | May proceed only under its own checklist and explicit Jarvis implementation GO. |

Jarvis implementation GO is recorded in chat for:

```text
SH-T03 implementation GO under patch-gate isolation
```

## 4. Excluded Patch-Gate Rows

The following patch-gate possible rows remain HOLD:

| Ticket | Reason |
| --- | --- |
| `CD-T06` | State-header semantics require D-02/state-label isolation and visual frames. |
| `CH-T03` | Depends on `CH-T01` and hard-constraint copy semantics. |
| `MV-T04` | P3 approval audit summary plus visual/P3 boundary risk. |
| `AP-T01`, `AP-T03`, `AP-T05`, `AP-T06`, `AP-T07`, `AP-T10`, `AP-T11`, `AP-T12` | P2 approval and D-02/state-machine sensitive; belong to a later AP-governed batch. |
| `SH-T08` | P3 approval-audit source/data availability plus visual frames. |

## 5. SH-T03 Implementation Bounds

Allowed implementation must stay within:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_SH_T03_PATCH_GATE_ISOLATED_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_SPRINT1_RQ03_PATCH_GATE_BATCH_ISOLATION_CHECKLIST_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

Implementation may:

- add a minimal `/search` or `/search?tab=history` route;
- resolve route input into a bounded local history context;
- clamp requested coverage to a safe effective coverage before render;
- render a safe history guard surface;
- prove no write CTA is attached;
- prove URL/localStorage/sessionStorage do not act as authority for role or coverage.

Implementation must not:

- add `SH-T01` visual list styling;
- add `SH-T02` dual coverage label treatment;
- add `SH-T04` / `SH-T05` focus behavior;
- add `SH-T06` empty-state visuals;
- add `SH-T08` P3 approval audit summary;
- touch `ResolvedSurfaceContext`, `ContextValidator`, fixture registry, or mock adapter;
- add backend/runtime/API/schema changes;
- add Storybook/Playwright/dependency changes;
- use real data, secrets, deploy, public endpoint, or external pilot behavior.

## 6. Required Gate

Minimum required gate:

```powershell
cd frontend
npm run test -- --run
npm run build
cd ..
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
git diff --check
```

Claude Code focused review is required after implementation diff.

Jira sync is allowed only if implementation closes with PASS and exact issue handling is safe.

Gate evidence recorded for the implemented ticket:

```text
frontend tests: PASS, 60 tests
frontend build: PASS
backend guard: PASS, 42 tests
git diff --check: PASS with Windows line-ending warnings only
Claude Code focused review: PASS
```

Jira sync:

```text
SCRUM-31 [SH] Search / History - epic open
SCRUM-32 [SH-T03] history route resolve -> clamp -> guard -> render - 已完成
```

## 7. HOLD Conditions

HOLD immediately if:

- implementation needs any file outside the allowed file list;
- route guard requires backend/runtime/API/schema work;
- implementation changes root context, validator, fixture registry, or adapter;
- implementation needs product interpretation beyond clamp-first route guard;
- implementation touches P2/P3 authority, P2 approval, P3 manager, or approval audit summary;
- tests/build fail and cannot be corrected inside scope;
- Claude Code review raises a blocking issue;
- any GoNoGo Section 9 mandatory external-review trigger fires.

## 8. Next Safe Action

Next safe automation action:

```text
WAIT_FOR_NEXT_EXACT_BOUNDED_TICKET_OR_PATCH_GATE_BATCH_ITEM
```
