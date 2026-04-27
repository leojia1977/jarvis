# S6 IN-T02 P3 Readonly Inbox Variant Skeleton Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 IN-T02 P3 Readonly Inbox Variant Skeleton Launch Checklist 2026-04-27 |
| Ticket | `IN-T02` |
| Scope | `P3 readonly inbox variant semantic skeleton` |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_WITH_NON_BLOCKING_NOTES_JIRA_DONE_SYNCED |
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

This checklist opens `IN-T02` under the staged Visual Skeleton GO lane. It does not claim final `VF-02` visual PASS.

## 2. Launch Decision

Decision:

```text
GO_FOR_VISUAL_SKELETON_IMPLEMENTATION
```

Rationale:

- `IN-T01` has already established the case-first Inbox base structure.
- `IN-T02` can be bounded to a P3 readonly skeleton without changing routes, permissions, P2/P3 authority, fixture adapters, or backend behavior.
- `VF-02` remains pending, so only semantic skeleton, test ids, accessibility landmarks, layout slots, and regression tests are allowed.

## 3. Exact Scope

Implement only:

- P3-only readonly Inbox variant using the existing Inbox route;
- stable test ids for the P3 readonly variant and card;
- semantic attributes proving `ResolvedSurfaceContext` is the authority source;
- case id, verdict, coverage, case state, and next-step summary as readonly fields;
- absence of `Open case` and approval/write CTA affordances in the P3 readonly variant;
- regression tests for P3 readonly behavior.

## 4. Exact Non-Goals

Do not implement:

- final `VF-02` visual styling or visual PASS;
- new route, Manager View page, approval page, or route handoff;
- P2 approval shortcuts, close request, approve/reject/delay/observe controls, or `ActionMode`;
- backend/runtime/API/schema changes;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- Storybook, Playwright, real data, anonymized real data, secrets, deploy, public endpoint, or external pilot.

## 5. Allowed Files

Allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_IN_T02_P3_READONLY_INBOX_VARIANT_SKELETON_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_IN_T02_P3_READONLY_INBOX_VARIANT_SKELETON_CLOSEOUT_2026_04_27.md
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
- implementation needs P3 authority expansion, Manager View, approval audit, P2 Approval Surface, or route handoff;
- implementation needs backend/runtime/API/schema work;
- implementation needs fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- tests/build fail and cannot be corrected inside this ticket scope;
- Claude Code review raises a blocking finding;
- any mandatory external-review trigger fires.

## 8. Next Safe Action

Next safe automation action if implementation PASSes:

```text
OPEN_IN_T04_P1_ESCALATION_CLOSE_REQUEST_ENTRY_SKELETON_LAUNCH
```
