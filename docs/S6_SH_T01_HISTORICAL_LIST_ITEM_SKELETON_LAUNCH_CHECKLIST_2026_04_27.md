# S6 SH-T01 Historical List Item Skeleton Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 SH-T01 Historical List Item Skeleton Launch Checklist 2026-04-27 |
| Ticket | `SH-T01` |
| Scope | `Historical list item semantic skeleton and test ids only` |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Acceleration matrix | `docs\S6_SPRINT1_4_AUTOMATION_ACCELERATION_MATRIX_2026_04_27.md` |
| Staged authorization | `docs\S6_STAGED_ACCELERATION_AUTHORIZATION_2026_04_27.md` |
| Frame dependency | `HF-SH-01` / `VF-08` final visual frames pending |
| Primary implementor | Codex |
| Execution surface | codex |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review if implementation diff exists |
| Review surface | claude-cmd |
| External review | not required unless HOLD trigger fires |
| SWE | disabled |

This checklist opens `SH-T01` under the staged Visual Skeleton GO lane. It does not claim final `HF-SH-01` / `VF-08` visual PASS.

## 2. Launch Decision

Decision:

```text
GO_FOR_VISUAL_SKELETON_IMPLEMENTATION
```

Rationale:

- `SH-T03` has already established the clamp-first Search / History route guard.
- `SH-T05` has already established the read-only focus scopes and write-authority boundary.
- `SH-T01` can be bounded to a lightweight historical list item skeleton without implementing detail handoff, final list styling, Search / History visual frames, or new permission authority.

## 3. Exact Scope

Implement only:

- a historical case list item semantic skeleton inside the existing Search / History surface;
- stable test ids and semantic attributes proving the list item is `summary-only`, route-handoff is not implemented, and detail visibility remains owned by the case-detail route;
- lightweight list fields for case id, verdict, summary snippet, timestamp availability, recorded coverage, and current visible coverage;
- regression tests proving the list item does not attach write controls, approval controls, host raw evidence, detail visibility decisions, or route handoff.

## 4. Exact Non-Goals

Do not implement:

- final `HF-SH-01` / `VF-08` visual styling or visual PASS;
- `SH-T02` dual coverage visual treatment, `SH-T04`, `SH-T06`, `SH-T07`, `SH-T08`, or `SH-T09`;
- case-detail route handoff, focus-route handoff, deep links, or detail permission decisions;
- evidence timeline, blast radius, host raw evidence, approval controls, close controls, or ActionMode;
- fixture registry changes, fixture adapter changes, validator changes, or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema changes;
- Storybook, Playwright, real data, anonymized real data, secrets, deploy, public endpoint, or external pilot.

## 5. Allowed Files

Allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_SH_T01_HISTORICAL_LIST_ITEM_SKELETON_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_SH_T01_HISTORICAL_LIST_ITEM_SKELETON_CLOSEOUT_2026_04_27.md
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
- implementation needs route handoff, detail permission authority, write controls, approval controls, or ActionMode;
- implementation needs new fixture data, fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- implementation needs backend/runtime/API/schema work;
- tests/build fail and cannot be corrected inside this ticket scope;
- Claude Code review raises a blocking finding;
- any mandatory external-review trigger fires.

## 8. Next Safe Action

Next safe automation action if implementation PASSes:

```text
OPEN_CH_T01_COVERAGE_HEALTH_PAGE_SKELETON_LAUNCH
```
