# S6 EP-T02 Inferred Node Weakening Slot Skeleton Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 EP-T02 Inferred Node Weakening Slot Skeleton Launch Checklist 2026-04-27 |
| Ticket | `EP-T02` |
| Scope | `Inferred-node weakening semantic slot and test ids only` |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Acceleration matrix | `docs\S6_SPRINT1_4_AUTOMATION_ACCELERATION_MATRIX_2026_04_27.md` |
| Staged authorization | `docs\S6_STAGED_ACCELERATION_AUTHORIZATION_2026_04_27.md` |
| Frame dependency | `VF-10` final visual frame pending |
| Primary implementor | Codex |
| Execution surface | codex |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review if implementation diff exists |
| Review surface | claude-cmd |
| External review | not required unless HOLD trigger fires |
| SWE | disabled |

This checklist opens `EP-T02` under the staged Visual Skeleton GO lane. It does not claim final `VF-10` visual PASS.

## 2. Launch Decision

Decision:

```text
GO_FOR_VISUAL_SKELETON_IMPLEMENTATION
```

Rationale:

- `EP-T01` has already established the subordinate Timeline panel inside Case Detail.
- `EP-T02` can be bounded to an inferred-node weakening semantic slot inside that existing Timeline panel.
- `VF-10` remains pending, so only semantic skeleton, test ids, accessibility landmarks, layout slots, and regression tests are allowed.

## 3. Exact Scope

Implement only:

- an inferred-node weakening slot inside the existing Timeline subordinate panel;
- stable test ids and semantic attributes proving inferred nodes are lower weight than direct evidence;
- explicit `VF-10` pending / skeleton-only anchors;
- regression tests proving the slot is not a direct-evidence node and does not unlock write controls, `ActionMode`, blast radius, routes, or backend behavior.

## 4. Exact Non-Goals

Do not implement:

- final `VF-10` visual styling or visual PASS;
- real inferred-node data generation, graph/tool/node details, or new business facts;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- `EP-T03` lineage-confidence `L1 = DEGRADED` behavior beyond preserving existing anchors;
- `EP-T04`, `EP-T05`, `EP-T06`, Search/History, P2 Approval Surface, P3 Manager View, or route handoff;
- backend/runtime/API/schema changes;
- Storybook, Playwright, real data, anonymized real data, secrets, deploy, public endpoint, or external pilot.

## 5. Allowed Files

Allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_EP_T02_INFERRED_NODE_WEAKENING_SLOT_SKELETON_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_EP_T02_INFERRED_NODE_WEAKENING_SLOT_SKELETON_CLOSEOUT_2026_04_27.md
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
- final visual interpretation is required instead of semantic skeleton anchors;
- implementation needs new fixture data, inferred graph data, graph/tool/node surfacing, or product facts;
- implementation needs `EP-T03`, `EP-T04`, `EP-T05`, `EP-T06`, route handoff, Search/History, P2/P3 authority expansion, or approval audit work;
- implementation needs backend/runtime/API/schema work;
- implementation needs fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- tests/build fail and cannot be corrected inside this ticket scope;
- Claude Code review raises a blocking finding;
- any mandatory external-review trigger fires.

## 8. Next Safe Action

Next safe automation action if implementation PASSes:

```text
OPEN_EP_T03_L1_LINEAGE_DEGRADATION_SEMANTIC_SKELETON_LAUNCH
```
