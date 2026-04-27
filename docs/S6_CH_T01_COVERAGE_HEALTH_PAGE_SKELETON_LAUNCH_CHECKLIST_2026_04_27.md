# S6 CH-T01 Coverage & Health Page Skeleton Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 CH-T01 Coverage & Health Page Skeleton Launch Checklist 2026-04-27 |
| Ticket | `CH-T01` |
| Scope | `Coverage & Health page semantic skeleton and test ids only` |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Acceleration matrix | `docs\S6_SPRINT1_4_AUTOMATION_ACCELERATION_MATRIX_2026_04_27.md` |
| Staged authorization | `docs\S6_STAGED_ACCELERATION_AUTHORIZATION_2026_04_27.md` |
| Frame dependency | `VF-01` final visual frame pending |
| Primary implementor | Codex |
| Execution surface | codex |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review if implementation diff exists |
| Review surface | claude-cmd |
| External review | not required unless HOLD trigger fires |
| SWE | disabled |

This checklist opens `CH-T01` under the staged Visual Skeleton GO lane. It does not claim final `VF-01` visual PASS.

## 2. Launch Decision

Decision:

```text
GO_FOR_VISUAL_SKELETON_IMPLEMENTATION
```

Rationale:

- `CH-T01` is explicitly authorized as a visual skeleton candidate after `SH-T01`.
- The current front-end already has role-filtered navigation for Coverage & Health (`P0` / `P2` only), but the slice is inactive.
- A bounded skeleton can add a route, landmarks, test ids, and existing-context fields without implementing `CH-T02`, `CH-T03`, real health endpoints, backend readiness, or final `VF-01` styling.

## 3. Exact Scope

Implement only:

- a `/coverage-health` page skeleton reachable from the existing `Coverage & Health` nav item for eligible roles;
- stable test ids and semantic attributes proving `VF-01` is pending, the page is skeleton-only, and `ResolvedSurfaceContext` remains authority;
- lightweight slots for coverage ceiling, case state, fixture freshness, and deferred signal-health / ui-message areas;
- regression tests proving `P1` and `P3` do not expose the Coverage & Health navigation entry, while `P2` can enter the skeleton route.

## 4. Exact Non-Goals

Do not implement:

- final `VF-01` visual styling or visual PASS;
- `CH-T02`, `CH-T03`, `CH-T04`, cross-surface hardening, or acceptance-suite behavior;
- `ui_messages` hard-constraint rendering, unlock copy, or patch-gate copy semantics;
- real `/health`, `/ready`, runtime readiness, backend telemetry, sensor health, external source health, or live data;
- coverage escalation, expert-mode field expansion, route handoff, write controls, approval controls, or ActionMode;
- fixture registry changes, fixture adapter changes, validator changes, or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema changes;
- Storybook, Playwright, real data, anonymized real data, secrets, deploy, public endpoint, or external pilot.

## 5. Allowed Files

Allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_CH_T01_COVERAGE_HEALTH_PAGE_SKELETON_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_CH_T01_COVERAGE_HEALTH_PAGE_SKELETON_CLOSEOUT_2026_04_27.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

No other files are authorized.

## 6. Required Gate

Minimum gate:

```powershell
cd frontend
npm run test -- --run
npm run build
cd ..
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
git diff --check
```

## 7. HOLD Conditions

HOLD if:

- implementation requires files outside the allowed list;
- implementation needs final visual interpretation instead of semantic skeleton anchors;
- implementation needs `ui_messages` hard-constraint copy or patch-gate semantics;
- implementation needs real health/readiness endpoints, telemetry, backend/runtime/API/schema work, external-source health, or live data;
- implementation needs coverage escalation, expert-mode expansion, route handoff, P2/P3 authority expansion, write controls, approval controls, or ActionMode;
- implementation needs fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- tests/build fail and cannot be corrected inside this ticket scope;
- Claude Code review raises a blocking finding;
- any mandatory external-review trigger fires.

## 8. Next Safe Action

Next safe automation action if implementation PASSes:

```text
OPEN_AP_T10_PATCH_ISOLATION_CHECKLIST
```
