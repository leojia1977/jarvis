# S6 GS-T04 Expert Mode Entry Skeleton Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 GS-T04 Expert Mode Entry Skeleton Launch Checklist 2026-04-27 |
| Ticket | `GS-T04` |
| Scope | `Expert mode entry semantic skeleton` |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Parent authorization | `docs\S6_STAGED_ACCELERATION_AUTHORIZATION_2026_04_27.md` |
| Design dependency | `VF-03` final visual frame remains pending |
| Primary implementor | Codex |
| Execution surface | codex |
| Reviewer | Claude Code focused review if implementation diff exists |
| Review surface | claude-cmd |
| External review | not required unless HOLD trigger fires |
| SWE | disabled |

This checklist converts `GS-T04` into a semantic skeleton ticket only. It does not claim final visual PASS.

## 2. Launch Decision

Decision:

```text
GO_FOR_VISUAL_SKELETON_IMPLEMENTATION
```

Meaning:

- Implementation may add an expert-mode entry layout slot, test ids, accessibility semantics, and regression tests.
- Implementation must not invent final VF-03 styling or interaction behavior.
- Implementation must not turn expert mode into a permission, coverage, or field-unlock control.

## 3. Exact Scope

Implement only:

- an expert-mode entry semantic slot in the Global Shell;
- role-derived state using `ResolvedSurfaceContext` role and coverage only;
- `P1` restricted state that preserves the current field set and coverage ceiling;
- `P0/P2` entry skeleton semantics without action behavior;
- test ids and regression assertions proving the slot is inert and does not expand authority.

## 4. Exact Non-Goals

Do not implement:

- final VF-03 visual styling or visual PASS;
- expert-mode toggle, switch, route, modal, drawer, or settings flow;
- additional fields, hidden technical panels, or OFF-field reveal;
- P2 Approval Surface;
- P3 Manager View;
- backend/runtime/API/schema changes;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- Storybook, Playwright, real data, secrets, deploy, public endpoint, or external pilot.

## 5. Allowed Files

Allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_GS_T04_EXPERT_MODE_ENTRY_SKELETON_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
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

- `P1` sees an expert-mode entry skeleton in restricted state;
- `P2` sees an expert-mode entry skeleton without any route, toggle, or action behavior;
- `P3` does not receive a Global Shell expert-mode entry;
- expert mode does not change role, coverage, case state, ActionMode, visible field set, route, fixture, or backend behavior;
- no control is labeled or implemented as a permission unlock switch.

## 8. HOLD Conditions

HOLD if:

- implementation requires files outside the allowed list;
- implementation needs final visual interpretation from `VF-03`;
- implementation needs new route, modal, drawer, toggle, or settings behavior;
- implementation needs P2/P3 authority changes;
- implementation needs backend/runtime/API/schema work;
- implementation changes fixture registry, adapter, validator, or `ResolvedSurfaceContext`;
- tests/build fail;
- Claude Code review raises a blocking finding;
- any GoNoGo Section 9 mandatory external-review trigger fires.

## 9. Next Safe Action

Next safe automation action:

```text
OPEN_IN_T02_P3_READONLY_INBOX_VARIANT_SKELETON_LAUNCH
```

Closeout record:

```text
docs\S6_GS_T04_EXPERT_MODE_ENTRY_SKELETON_CLOSEOUT_2026_04_27.md
```
