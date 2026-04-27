# S6 P1-CD-C Action Request Modal Ticket Prep 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 P1-CD-C Action Request Modal Ticket Prep 2026-04-27 |
| Ticket | `P1-CD-C` |
| Scope | P1 Action Request modal semantics |
| Status | READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO_WITH_BOUNDS |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `5270a5c` |
| Intake record | `docs\S6_PRODUCT_SOURCE_INTAKE_2026_04_25.md` |
| Route record | `docs\S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md` |
| Predecessors | `P1-CD-A`, `P1-CD-B`, `E0-01` through `E0-04B` |
| Lane | Yellow bounded frontend implementation after this prep |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | conditional |
| SWE | disabled |

This record converts the selected P1 action-request modal ticket into an exact bounded implementation item.

It does not authorize launch, deploy, public endpoint work, external pilot execution, real-data handling, credential handling, backend/API/schema changes, P2 approval implementation, P3 manager implementation, cross-surface state propagation, route handoff, AI_COLLAB changes, SWE execution, or broad reusable platform work.

## 2. Governing Product Sources

Use this authority order:

1. `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版 (2).md`
2. `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2 (1).md`
3. `SecuPilot_P1_L2_Case_Detail_Page_Model_Contract_v0.2 (1).md`
4. `SecuPilot_Approval_Interaction_and_State_Semantics_Spec_v0.2.md`
5. `SecuPilot_PR_Brief_E0-02_Mock_Fixture_Adapter_Phase_States_v0.1 (1).md`
6. P1 prototype Markdown and HTML as visual / interaction references only

Binding constraints:

```text
HTML is visual and interaction reference only. Model Contract and PRD govern implementation.
P1 may submit/escalate an Action Request to P2, but P1 must not choose ActionMode or execute approval authority.
```

## 3. Exact Behavior

Implement P1 Action Request modal semantics inside the existing `/case/:caseId` P1 Case Detail page.

Required behavior:

| Area | Required behavior |
| --- | --- |
| P1 Action Request panel CTA | Add a P1-only CTA that opens an Action Request modal when the current resolved surface is `P1_CASE_DETAIL` and no AR is submitted in the current mock phase. |
| Modal copy | State that the request is submitted to P2 for review and that P1 does not choose execution mode. |
| Modal controls | Provide only `Submit to P2` and `Cancel` controls. |
| Local submission result | On submit, close the modal and render a local mock-only submitted state such as `Submitted to P2 review` / `Waiting on P2`, without changing resolved context, case state, route, backend state, or fixture data. |
| Existing AR state | When the fixture already has an AR or phase implies waiting on P2, keep the panel read-only and do not show a second submit CTA. |
| Accessibility | Modal must use dialog semantics and be keyboard/click accessible. |
| Existing page contract | Preserve P1-CD-A layout, P1-CD-B evidence controls, follow-up input, role-cropped navigation, coverage badge, and E0 redline selector behavior. |

Data mode:

```text
synthetic/local UI state only
```

## 4. Exact Non-Goals

This ticket must not implement:

- P2 Approval Surface;
- P2 decision composer;
- P2 approve/reject/delay/observe operations;
- P2 strong confirm;
- P3 Manager View;
- cross-surface route handoff;
- AR propagation from P1 to P2 beyond local mock-only submitted text;
- material case_state, ar_status, or action_mode mutation;
- observation-window timer, `emitStateSync`, backend `STATE_SYNC`, polling, WebSocket, runtime, API, or schema behavior;
- backend/API/schema changes;
- fixture registry, fixture adapter, validator, or mock fixture data changes;
- Storybook changes;
- Playwright E2E changes;
- static HTML prototype copy/paste;
- hardcoded final business follow-up chips, unlock messages, ROI values, queue windows, CMDB business tags, or remediation suggestions;
- broad component library, reusable platform layer, registry, service layer, or design-system abstraction;
- real data, credentials, cookies, tokens, auth headers, browser session material, or external network integration.

## 5. Exact Allowed Files

Allowed files for this ticket:

- `docs/S6_P1_CD_C_ACTION_REQUEST_MODAL_TICKET_PREP_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

No other file may be changed for P1-CD-C unless a HOLD is triggered and a new decision record expands scope.

## 6. Required Tests

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

## 7. Required Assertions

Automated or closeout-visible assertions must cover:

- P1 `/case/CASE-2847` renders an Action Request CTA in the Action Request panel when no AR is submitted;
- clicking the CTA opens a dialog with `Submit to P2` and `Cancel`;
- the dialog does not expose `IMMEDIATE`, `DELAYED`, `OBSERVE_ONLY`, approve, reject, delay, observe, or execution-mode choices;
- submitting closes the dialog and renders a local mock-only `Waiting on P2` / submitted-to-P2 state;
- submission does not mutate the resolved context, case state, route, or fixture phase;
- selecting an existing AR phase keeps the panel read-only and does not render a duplicate submit CTA;
- P1 navigation still excludes `Approval Queue`;
- existing evidence Auto / Manual / Pin controls and follow-up input remain visible.

## 8. Max Change Budget

Maximum expected implementation scope:

- one local UI state for the modal open/closed state;
- one local UI state for mock-only P1 submitted result;
- one focused modal/dialog JSX block inside the existing P1 Case Detail surface;
- focused CSS for the modal and Action Request panel controls;
- focused component tests.

Do not introduce new modules, helpers, directories, dependencies, or generalized component registries.

## 9. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- implementation is small and tightly coupled to current `App.tsx`;
- the ticket is security/authority sensitive because it distinguishes P1 submission from P2 approval;
- no separate SWE exact sub-ticket has been created.

## 10. Review Path

Required review path:

```text
Claude Code focused review after implementation diff.
```

Claude Web / external product-architecture-governance review is conditional and required if implementation:

- changes product semantics beyond P1-CD-C;
- claims broad P1/P2/P3 architecture readiness;
- introduces backend/API/schema behavior;
- implements P2 approval authority or cross-surface propagation;
- changes E0 root context / validator semantics;
- conflicts with PRD, the P1 Model Contract, or the approval interaction spec;
- touches Red/HOLD trigger categories from the Go/No-Go record.

## 11. Rollback

Rollback condition:

```text
Revert P1-CD-C frontend and ticket-prep changes if frontend tests/build fail, backend guard fails, scope expands outside allowed files, or HOLD triggers fire.
```

## 12. HOLD Conditions

HOLD if:

- any implementation requires files outside the allowed file list;
- implementation needs backend/API/schema work;
- implementation tries to copy static HTML prototype code into the app;
- the Case Detail page starts implementing P2 approval authority or P3 manager behavior;
- implementation begins route handoff, cross-surface AR propagation, or backend state sync;
- P1 gains approve/reject/delay/observe/final execution controls;
- `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` choices are exposed to P1;
- case_state, ar_status, action_mode, fixture data, or validator behavior must be mutated to pass the ticket;
- hardcoded final business chips, unlock messages, ROI values, queue windows, or CMDB tags are introduced;
- a broad abstraction, registry, platform helper, or new module appears;
- product source conflict is found between PRD, the P1 Model Contract, and approval interaction spec;
- tests cannot be run;
- Claude Code review is unavailable and closeout would claim review PASS anyway.

## 13. Decision

Decision:

```text
READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO_WITH_BOUNDS
```

Authorized next technical action:

```text
Implement P1-CD-C inside the exact allowed file scope, then run required gates and Claude Code focused review.
```
