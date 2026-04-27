# S6 EP-T01 Subordinate Panel Framework Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 EP-T01 Subordinate Panel Framework Launch Checklist 2026-04-27 |
| Ticket | `EP-T01` |
| Scope | Evidence / Timeline / Blast Radius subordinate panel framework |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_COMMITTED_PUSHED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Parent triage | `docs\S6_SPRINT1_BATCH1_P1_GAP_TRIAGE_CHECKLIST_2026_04_27.md` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Route | `OPEN_EP_T01_SUBORDINATE_PANEL_FRAMEWORK_LAUNCH_CHECKLIST` |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | not required unless HOLD / trigger fires |
| SWE | disabled |

This record converts `EP-T01 - subordinate panels framework` into an exact bounded implementation item and records its closeout.

It does not itself authorize implementation, backend/runtime/API/schema changes, Storybook, Playwright, fixture registry, validator changes, real data, secrets, deployment, public endpoint work, external pilot execution, or Jira cloud mutation.

## 2. Decision

Decision:

```text
READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO_WITH_BOUNDS
```

Meaning:

- EP-T01 is ready for implementation only after Jarvis explicitly authorizes implementation GO.
- The implementation must remain P1-local, mock-only, and limited to the exact files below.
- SWE remains disabled because this ticket is small, authority-sensitive, and tightly coupled to current Case Detail UI behavior.

## 3. Governing Sources

Use this authority order:

1. `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版 (2).md`
2. `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2 (1).md`
3. `SecuPilot_P1_L2_Case_Detail_Page_Model_Contract_v0.2 (1).md`
4. Backlog Tracker v0.4 row `EP-T01`
5. Existing implemented P1 workbench behavior in `frontend/src/App.tsx`

Binding tracker row:

```text
EP-T01 - subordinate panels - implement panel=evidence/timeline/blast_radius subordinate panel framework.
Notes: do not add a new first-level page.
Design dependency: none.
Governance dependency: none.
Patch gate impact: none.
```

## 4. Exact Behavior

Implement a subordinate panel framework inside the existing P1 Case Detail surface.

Required behavior:

| Area | Required behavior |
| --- | --- |
| Panel framework | Add a subordinate panel selector or equivalent frame for `Evidence`, `Timeline`, and `Blast Radius` inside the existing Case Detail / evidence area. |
| No top-level route | Do not create a new route, nav item, page, or first-level surface. |
| Evidence panel | Preserve the existing contextual evidence panel, Auto / Manual mode, Pin / Unpin, and frame switcher behavior. |
| Timeline panel | Render a mock-only, read-only timeline subordinate panel using existing fixture/audit/narrative data already available in `App.tsx`; do not infer new product facts. |
| Blast Radius panel | Render only when coverage permits it. If `coverage_level` is `L1`, do not render blast-radius details or placeholder cards. |
| P1 authority boundary | P1 must not gain approve/reject/delay/observe controls, `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` options. |
| P3 safety | P3 host raw evidence must remain absent from the DOM. |
| Data mode | Existing mock-only fixture-derived UI state only. |

## 5. Exact Non-Goals

This ticket must not implement:

- new top-level pages or routes;
- Search/History;
- P2 Approval Surface;
- P2 decision composer, strong confirm, approve/reject/delay/observe controls, or observation-window state migration;
- P3 Manager View;
- P3 executive summary component;
- inferred-node visual weakening from `EP-T02`;
- lineage confidence degradation from `EP-T03`;
- full L1 blast-radius closeout from `EP-T04`, except the required EP-T01 guard that L1 must not render blast-radius detail/placeholder;
- P3 technical panel fallback from `EP-T05`;
- Storybook stories;
- Playwright E2E;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema changes;
- real data, secrets, deployment, public endpoint, external pilot, or Jira cloud mutation.

## 6. Exact Allowed Files

Allowed files:

- `docs/S6_EP_T01_SUBORDINATE_PANEL_FRAMEWORK_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

No other files may be changed. If additional files appear necessary, HOLD and open a new decision record.

## 7. Required Tests

Frontend:

```powershell
cd frontend
npm run test -- --run
npm run build
```

Backend guard:

```powershell
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
```

Repo hygiene:

```powershell
git diff --check
```

## 8. Required Assertions

Implementation closeout must prove:

- Case Detail exposes subordinate choices for Evidence, Timeline, and Blast Radius.
- Selecting Evidence preserves the current contextual evidence panel behavior.
- Selecting Timeline shows a read-only subordinate panel from existing mock fixture / audit / narrative data.
- Selecting Blast Radius under coverage `L2` renders only mock-safe summary content.
- Under coverage `L1`, Blast Radius detail and placeholder cards are not attached.
- The panel framework does not add a new route or top-level nav item.
- P1 does not expose approve/reject/delay/observe controls or ActionMode choices.
- P3 host raw evidence remains absent from the DOM.
- Existing Dialogue Dock and P1 Action Request modal behavior remain available.

## 9. Review Path

Required review:

```text
Claude Code focused review after implementation diff.
```

Claude Web / external architecture-governance review is not required unless implementation:

- changes E0 root context or validator semantics;
- changes product authority between P1/P2/P3;
- introduces backend/runtime/API/schema behavior;
- claims cross-surface route handoff;
- touches state-sync / observation-window material migration;
- introduces real data, secrets, deploy, public endpoint, or external pilot behavior;
- triggers any Go/No-Go Section 9 or AI_COLLAB mandatory external-review condition.

## 10. Rollback

Rollback condition:

```text
Revert EP-T01 ticket-scoped changes if frontend tests/build fail, backend guard fails, scope expands outside allowed files, P1 authority boundaries are violated, P3 raw evidence attaches, or HOLD triggers fire.
```

## 11. HOLD Conditions

HOLD if:

- implementation needs files outside the allowed list;
- implementation requires new fixture data, fixture registry changes, adapter changes, validator changes, or `ResolvedSurfaceContext` changes;
- implementation needs backend/runtime/API/schema work;
- implementation needs Storybook or Playwright changes;
- implementation adds a new route, page, or top-level navigation item;
- implementation requires visual details from `VF-10` or other unratified visual frames;
- implementation starts `EP-T02`, `EP-T03`, `EP-T04`, `EP-T05`, or `EP-T06` scope beyond the minimal EP-T01 guard;
- P1 gains approve/reject/delay/observe controls or ActionMode choices;
- P3 host raw evidence appears in the DOM;
- tests cannot be run;
- Claude Code focused review is unavailable after implementation diff;
- Jira cloud mutation is attempted without explicit Jarvis authorization.

## 12. Implementation Closeout

Closeout decision:

```text
IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_COMMITTED_PUSHED
```

Implemented files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

Implemented behavior:

- added a P1-local subordinate panel selector inside the existing Case Detail contextual evidence area;
- added `Evidence`, `Timeline`, and `Blast Radius` subordinate choices without adding a new route, top-level page, or navigation item;
- preserved the existing Evidence panel Auto / Manual / Pin / frame-switcher behavior by moving it behind the Evidence subordinate panel;
- added a read-only Timeline subordinate panel from existing mock trace/audit metadata;
- added a mock-safe Blast Radius subordinate panel only when coverage is not `L1`;
- preserved the L1 hard ceiling by not rendering the Blast Radius selector or subordinate panel under `coverage_level = L1`;
- preserved P1 authority boundaries: no approve/reject/delay/observe controls and no `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` choices;
- preserved P3 host raw evidence absence from the DOM.

Gate evidence:

```text
cd frontend
npm run test -- --run
PASS: 5 test files, 57 tests

cd frontend
npm run build
PASS

py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
PASS: 42 tests

git diff --check
PASS with Windows line-ending warnings only
```

Claude Code focused review:

```text
PASS
```

Non-blocking observations:

- `useEffect` dependency list could be simplified later if lint policy becomes stricter;
- the subordinate panel selector keeps a three-column grid under L1 even when the Blast Radius button is absent.

These observations do not reopen EP-T01.

External review:

```text
NOT_REQUIRED
```

Reason: EP-T01 did not change E0 root context or validator semantics, product authority between P1/P2/P3, backend/runtime/API/schema behavior, cross-surface route handoff, state-sync / observation-window material migration, real data, secrets, deploy, public endpoint, or external pilot behavior.

Next safe action:

```text
WAIT_FOR_NEXT_EXACT_BOUNDED_TICKET_SELECTION
```
