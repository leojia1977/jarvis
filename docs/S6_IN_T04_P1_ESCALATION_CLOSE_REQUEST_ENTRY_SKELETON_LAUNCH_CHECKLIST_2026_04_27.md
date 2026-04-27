# S6 IN-T04 P1 Escalation Close-Request Entry Skeleton Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 IN-T04 P1 Escalation Close-Request Entry Skeleton Launch Checklist 2026-04-27 |
| Ticket | `IN-T04` |
| Scope | `P1 escalation / close-request entry semantic skeleton` |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Acceleration matrix | `docs\S6_SPRINT1_4_AUTOMATION_ACCELERATION_MATRIX_2026_04_27.md` |
| Staged authorization | `docs\S6_STAGED_ACCELERATION_AUTHORIZATION_2026_04_27.md` |
| Frame dependency | `VF-02` final visual frame pending |
| Primary implementor | Codex |
| Execution surface | codex |
| Reviewer | Claude Code focused review if implementation diff exists |
| Review surface | claude-cmd |
| External review | not required unless HOLD trigger fires |
| SWE | disabled |

This checklist opens `IN-T04` under the staged Visual Skeleton GO lane. It does not claim final `VF-02` visual PASS.

## 2. Launch Decision

Decision:

```text
GO_FOR_VISUAL_SKELETON_IMPLEMENTATION
```

Rationale:

- Product semantics already permit P1 to escalate or submit a close request from Case Detail.
- Current code already has a bounded P1 Action Request panel; `IN-T04` can extend that surface with semantic skeleton anchors without creating a new route.
- `VF-02` remains pending, so only semantic skeleton, test ids, accessibility landmarks, layout slots, and regression tests are allowed.

## 3. Exact Scope

Implement only:

- P1-only escalation / close-request entry skeleton inside the existing Case Detail Action Request region;
- stable test ids and semantic attributes proving `ResolvedSurfaceContext` remains the authority source;
- controlled skeleton slots for escalation reason, recommended action, urgency text, and close-request entry;
- explicit evidence that recommended action is P2 reference-only and urgency text is not `ActionMode`;
- absence of approve / reject / delay / observe / close execution CTA affordances;
- regression tests for P1 skeleton presence and non-P1 / existing AR phase absence.

## 4. Exact Non-Goals

Do not implement:

- final `VF-02` visual styling or visual PASS;
- real close-request submission, close execution, approval execution, or persisted status mutation;
- P2 approval controls, `ActionMode`, `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY`;
- new route, route handoff, approval page, Manager View page, or P2/P3 authority change;
- backend/runtime/API/schema changes;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- Storybook, Playwright, real data, anonymized real data, secrets, deploy, public endpoint, or external pilot.

## 5. Allowed Files

Allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_IN_T04_P1_ESCALATION_CLOSE_REQUEST_ENTRY_SKELETON_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_IN_T04_P1_ESCALATION_CLOSE_REQUEST_ENTRY_SKELETON_CLOSEOUT_2026_04_27.md
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
- implementation needs real close execution, P2 approval execution, `ActionMode`, or status migration;
- implementation needs P2/P3 authority expansion, approval route work, Manager View, approval audit, or route handoff;
- implementation needs backend/runtime/API/schema work;
- implementation needs fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- tests/build fail and cannot be corrected inside this ticket scope;
- Claude Code review raises a blocking finding;
- any mandatory external-review trigger fires.

## 8. Next Safe Action

Next safe automation action if implementation PASSes:

```text
OPEN_EP_T02_INFERRED_NODE_WEAKENING_SLOT_SKELETON_LAUNCH
```
