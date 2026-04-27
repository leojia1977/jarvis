# S6 SH-T03 Patch-Gate Isolated Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 SH-T03 Patch-Gate Isolated Launch Checklist 2026-04-27 |
| Ticket | `SH-T03` |
| Scope | `history route resolve -> clamp -> guard -> render` |
| Status | PATCH_GATE_ISOLATED_CHECKLIST_CREATED_IMPLEMENTATION_NOT_AUTHORIZED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Parent queue | `docs\S6_SPRINT1_RQ01_REMAINING_STATUS_RECONCILIATION_2026_04_27.md` |
| Visual unblock queue | `docs\S6_SPRINT1_RQ02_VISUAL_DEPENDENCY_UNBLOCK_QUEUE_2026_04_27.md` |
| Route | `OPEN_SH_T03_PATCH_GATE_ISOLATED_LAUNCH_CHECKLIST` |
| Primary implementor | TBD for implementation |
| Execution surface | TBD for implementation |
| Reviewer | Claude Code focused review required after implementation diff |
| Review surface | `claude-cmd` |
| External review | conditional |
| SWE | disabled unless a later exact bounded sub-ticket says otherwise |

This checklist creates a patch-gate isolated launch record for `SH-T03`.

It does not authorize implementation, Jira mutation, backend/runtime/API/schema changes, real data, secrets, deployment, public endpoint work, external pilot execution, or route-handoff expansion.

## 2. Decision

Decision:

```text
PATCH_GATE_ISOLATED_CHECKLIST_CREATED_IMPLEMENTATION_NOT_AUTHORIZED
```

Meaning:

- `SH-T03` is a viable acceleration candidate only if Jarvis explicitly relaxes the patch-gate filter for this one ticket.
- It must not be mixed into normal Sprint 1 burn-down.
- Implementation remains HOLD until a separate explicit `SH-T03 implementation GO` is granted.

## 3. Why SH-T03 Is Special

Backlog Tracker v0.4 row:

```text
SH-T03 - history route resolve -> clamp -> guard -> render
Patch Gate Impact = possible
External Review Required = conditional
Design Dependency = none
```

Why it can accelerate:

- it has no direct visual-frame dependency;
- it is a root prerequisite for later Search/History tasks;
- it can potentially be bounded to frontend route/guard/render behavior;
- it can create leverage for later `SH-T04`, `SH-T05`, `SH-T07`, and acceptance tests.

Why it is risky:

- it touches route resolution and coverage clamp semantics;
- it may intersect with hard constraints around coverage ceiling and no URL/storage authority;
- it can conflict with Search/History source rules if implemented too broadly;
- it is marked patch-gate possible and must be isolated.

## 4. Candidate Future Allowed Files

Future implementation, if later authorized, should start from this minimal candidate file scope:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_SH_T03_PATCH_GATE_ISOLATED_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

No other files are authorized by this checklist.

If implementation discovers a need to touch any of these areas, HOLD immediately:

```text
ResolvedSurfaceContext / ContextValidator
fixture registry / fixture adapter
backend/runtime/API/schema
Playwright config
Storybook
real data / secrets / deploy / public endpoint / external pilot
```

## 5. Candidate Future Test Command

Future implementation, if later authorized, must run at minimum:

```powershell
cd frontend
npm run test -- --run
npm run build
cd ..
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
git diff --check
```

Claude Code focused review is required after the implementation diff.

## 6. Candidate Future Acceptance Criteria

Future implementation may only proceed if it can satisfy these acceptance criteria without scope expansion:

- `/search` or `/search?tab=history` resolves through an explicit frontend route path rather than URL/storage-derived authority.
- The route resolves first, then clamps effective visibility before rendering.
- A current request must not upgrade visibility beyond the recorded/allowed coverage ceiling.
- History rendering must fail closed or render a safe unavailable state when required route/context fields are missing.
- No approve/reject/close or other write CTA is attached on the history surface.
- P3 host raw evidence remains absent from the DOM.
- The implementation must not create `SH-T01` visual list-item styling, `SH-T02` dual-label styling, `SH-T06` empty-state visuals, or `SH-T08` P3 approval-audit summary behavior.

## 7. Explicit Non-Goals

Do not implement:

- `SH-T01` HistoricalCaseListItem visual treatment;
- `SH-T02` Recorded coverage / Current visible dual labels;
- `SH-T04` available_focuses hint;
- `SH-T05` readonly focus scopes;
- `SH-T06` structural vs degraded empty states;
- `SH-T07` write-CTA disabling outside the minimum guard needed for SH-T03;
- `SH-T08` P3 approval audit source/data availability;
- `SH-T09` full history acceptance suite;
- P2 approval routes or state migration;
- P3 Manager View;
- backend/runtime/API/schema;
- new fixture semantics;
- real data, secrets, deploy, public endpoint, or external pilot.

## 8. Patch-Gate Triggers

External review or HOLD is required if any of these conditions appear:

- PRD / Model Contract / D-02 / Visual frame conflict;
- hard-constraint conflict around `coverage_level` ceiling;
- attempt to treat URL, localStorage, or sessionStorage as authority;
- missing exact reviewer / review surface / test command / rollback condition;
- need to touch root context, validator, fixture adapter, backend/runtime/API/schema, or route handoff beyond this surface;
- any implementation uncertainty that would require product interpretation.

## 9. Rollback Condition

If later implementation is authorized and then fails, rollback must be local and bounded:

```text
Revert only SH-T03 files changed by that implementation ticket.
Do not revert unrelated user or prior automation changes.
Return route to prior safe P1 workbench behavior.
```

## 10. Current Outcome

Current outcome:

```text
IMPLEMENTATION_HOLD_PENDING_EXPLICIT_SH_T03_GO
```

Next safe automation action:

```text
WAIT_FOR_JARVIS_SH_T03_IMPLEMENTATION_GO_OR_OPEN_PATCH_GATE_BATCH_ISOLATION_CHECKLIST
```
