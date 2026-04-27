# S6 SH-T05 Readonly Focus Scope Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 SH-T05 Readonly Focus Scope Launch Checklist 2026-04-27 |
| Ticket | `SH-T05` |
| Scope | `/search readonly focus scopes` |
| Status | READY_FOR_RECONCILIATION_OR_BOUNDED_IMPLEMENTATION_GO |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Parent queue | `docs\S6_SPRINT1_RQ04_EXACT_BOUNDED_RUNNER_QUEUE_2026_04_27.md` |
| Depends on | `SH-T03` |
| Primary implementor | Codex |
| Execution surface | codex |
| Reviewer | Claude Code focused review if implementation diff exists |
| Review surface | claude-cmd |
| External review | not required unless HOLD trigger fires |
| SWE | disabled |

This checklist opens `SH-T05` after `SH-T03` closeout.

## 2. Launch Decision

Decision:

```text
GO_FOR_RECONCILIATION_THEN_BOUNDED_IMPLEMENTATION_IF_NEEDED
```

Meaning:

- The runner must first check whether the current `/search?tab=history` route already restricts focus scope enough.
- If current repo evidence is sufficient, close out as `RECONCILED_GATE_PASS_NO_CODE`.
- If code is needed, implementation may proceed only inside the allowed files and acceptance criteria below.

## 3. Exact Scope

Implement or reconcile only:

- `/search` exposes read-only focus scopes;
- allowed focus scopes are limited to `summary`, `approval_audit`, and `history_audit`;
- focus selection is a hint/filter only, not an authorization source;
- technical deep-dive handoff remains to Case Detail, not Search/History;
- write CTAs remain absent.

## 4. Exact Non-Goals

Do not implement:

- `SH-T01` historical list-item visual treatment;
- `SH-T02` dual coverage label treatment;
- `SH-T04` available_focuses hint outside this minimal focus-scope UI;
- `SH-T06` empty/degraded state visuals;
- `SH-T07` full write-CTA disabled ticket, except preserving current absence of write CTAs;
- `SH-T08` P3 approval audit summary;
- `SH-T09` acceptance suite;
- P2 Approval Surface;
- P3 Manager View;
- route handoff beyond the existing `/search` route;
- backend/runtime/API/schema;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- Storybook, Playwright, real data, secrets, deploy, public endpoint, or external pilot.

## 5. Allowed Files

Allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_SH_T05_READONLY_FOCUS_SCOPE_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_SPRINT1_RQ04_EXACT_BOUNDED_RUNNER_QUEUE_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

No other files are authorized.

## 6. Required Tests

Minimum gate:

```powershell
cd frontend
npm run test -- --run
npm run build
cd ..
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
git diff --check
```

## 7. Acceptance Criteria

Closeout must prove:

- `/search?tab=history` renders exactly the allowed read-only focus scopes: `summary`, `approval_audit`, and `history_audit`.
- unsupported focus query values are ignored or downgraded without expanding authority.
- focus scopes do not change role, coverage, case state, ActionMode, or write authority.
- no approve/reject/delay/observe/close CTA appears on the history surface.
- URL/localStorage/sessionStorage do not become authority for role or coverage.

## 8. HOLD Conditions

HOLD if:

- implementation requires files outside the allowed list;
- implementation needs new route handoff, P2/P3 authority, approval audit semantics, or manager view behavior;
- implementation needs backend/runtime/API/schema work;
- implementation changes fixture registry, adapter, validator, or `ResolvedSurfaceContext`;
- implementation tries to treat focus query parameters as authority;
- tests/build fail;
- Claude Code review raises a blocking finding;
- any GoNoGo Section 9 mandatory external-review trigger fires.

## 9. Next Safe Action

Next safe automation action:

```text
SH_T05_RECONCILE_OR_IMPLEMENT
```
