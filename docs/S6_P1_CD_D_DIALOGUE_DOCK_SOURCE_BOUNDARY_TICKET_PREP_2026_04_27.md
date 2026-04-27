# S6 P1-CD-D Dialogue Dock Source Boundary Ticket Prep 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 P1-CD-D Dialogue Dock Source Boundary Ticket Prep 2026-04-27 |
| Ticket | `P1-CD-D` |
| Scope | Dialogue Dock source boundary |
| Status | READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO_WITH_BOUNDS |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `79112ac` |
| Intake record | `docs\S6_PRODUCT_SOURCE_INTAKE_2026_04_25.md` |
| Route record | `docs\S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md` |
| Predecessors | `P1-CD-A`, `P1-CD-B`, `P1-CD-C`, `E0-01` through `E0-04B` |
| Lane | Yellow bounded frontend implementation after this prep |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | conditional |
| SWE | disabled |

This record converts `P1-CD-D - Dialogue Dock source boundary` into an exact bounded implementation item.

It does not authorize live chat, LLM/runtime integration, backend/API/schema changes, recommended-question generation, P2/P3 implementation, route handoff, cross-surface propagation, real data, secrets, deploy, public endpoint, external pilot, or broad reusable chat-framework work.

## 2. Governing Product Sources

Use this authority order:

1. `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版 (2).md`
2. `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2 (1).md`
3. `SecuPilot_P1_L2_Case_Detail_Page_Model_Contract_v0.2 (1).md`
4. `SecuPilot_P1_L2_Case_Detail_Prototype_v2.1_Formal.md`
5. `SecuPilot_Web_Case_Workbench_IA_and_Flow_v0.2.md`
6. Existing implemented P1-CD-A/B/C app behavior

Binding constraints:

```text
Dialogue Dock must remain visible on Case Detail.
Recommended follow-up chips may exist only when their text comes from backend ui_messages or current runtime context output.
Prototype/example copy is placeholder only and must not become frontend hardcoded runtime suggestions.
```

## 3. Exact Behavior

Implement a source-boundary treatment for the existing Case Detail Dialogue Dock.

Required behavior:

| Area | Required behavior |
| --- | --- |
| Persistent visibility | Keep the Dialogue Dock visible on the P1 Case Detail page. |
| Source boundary | Render a small source/context strip inside the dock showing the current case and currently active evidence frame as local context. |
| Runtime placeholder | Render a non-interactive placeholder that indicates runtime follow-up suggestions are unavailable until `ui_messages` supplies them. |
| No hardcoded chips | Do not render recommended follow-up chip buttons or static business suggestion text. |
| Submit behavior | Keep submit behavior local and mock-only: submitting clears the input and does not create transcript, suggestions, case mutation, route handoff, backend call, or runtime call. |
| Existing page contract | Preserve P1-CD-A/B/C behavior, including evidence controls, Action Request modal, role-cropped navigation, coverage badge, and E0 redline behavior. |

Data mode:

```text
synthetic/local UI state only
```

## 4. Exact Non-Goals

This ticket must not implement:

- live chat;
- LLM calls or streaming responses;
- backend/runtime/API/schema work;
- real recommended-question generation;
- hardcoded business follow-up chips, unlock messages, ROI values, queue windows, CMDB business tags, remediation suggestions, or final runtime prompts;
- transcript persistence;
- route handoff;
- cross-surface propagation;
- P2 Approval Surface;
- P3 Manager View;
- Storybook changes;
- Playwright E2E changes;
- fixture registry, fixture adapter, validator, or mock fixture data changes;
- dependency changes;
- static HTML prototype copy/paste;
- broad conversation framework, service layer, registry, or generalized chat abstraction;
- real data, credentials, cookies, tokens, auth headers, browser session material, deploy, public endpoint, or external pilot.

## 5. Exact Allowed Files

Allowed files for this ticket:

- `docs/S6_P1_CD_D_DIALOGUE_DOCK_SOURCE_BOUNDARY_TICKET_PREP_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

No other file may be changed for P1-CD-D unless a HOLD is triggered and a new decision record expands scope.

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

- P1 `/case/CASE-2847` renders a persistent Dialogue Dock;
- the dock exposes current case context and current evidence frame context;
- the source-boundary placeholder is non-interactive and marked as runtime / `ui_messages` sourced;
- no recommended follow-up chip buttons are rendered from frontend hardcoded copy;
- the dock does not expose hardcoded business prompt phrases such as CMDB tags, blast radius unlocks, remediation suggestions, ROI, queue windows, approve/reject/delay/observe, or `IMMEDIATE` / `DELAYED` / `OBSERVE_ONLY`;
- submitting a follow-up clears the input and does not add transcript, suggestions, route changes, context mutation, or backend/runtime behavior;
- changing the evidence frame updates the local context strip without creating suggestions;
- P1-CD-C Action Request modal behavior remains available.

## 8. Max Change Budget

Maximum expected implementation scope:

- one source/context strip in the existing Dialogue Dock JSX;
- one runtime placeholder element;
- focused CSS for the dock strip/placeholder;
- focused component tests.

Do not introduce new modules, helpers, directories, dependencies, reducers, service layers, registries, or generalized chat abstractions.

## 9. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- implementation is small and tightly coupled to current `App.tsx`;
- source-boundary semantics are authority sensitive;
- no separate SWE exact sub-ticket has been created.

## 10. Review Path

Required review path:

```text
Claude Code focused review after implementation diff.
```

Claude Web / external product-architecture-governance review is conditional and required if implementation:

- changes product semantics beyond P1-CD-D;
- claims broad P1/P2/P3 architecture readiness;
- introduces backend/API/schema/runtime behavior;
- implements real chat/LLM behavior;
- implements hardcoded recommendation generation;
- changes E0 root context / validator semantics;
- conflicts with PRD, the P1 Model Contract, or visual/source-boundary constraints;
- touches Red/HOLD trigger categories from the Go/No-Go record.

## 11. Rollback

Rollback condition:

```text
Revert P1-CD-D frontend and ticket-prep changes if frontend tests/build fail, backend guard fails, scope expands outside allowed files, or HOLD triggers fire.
```

## 12. HOLD Conditions

HOLD if:

- any implementation requires files outside the allowed file list;
- implementation needs backend/API/schema/runtime work;
- implementation tries to copy static HTML prototype code into the app;
- implementation renders hardcoded business follow-up chips as runtime suggestions;
- implementation starts live chat, LLM calls, streaming, transcript persistence, or external network behavior;
- implementation mutates route, resolved context, case_state, ar_status, action_mode, fixture data, adapter, or validator behavior;
- implementation begins route handoff or cross-surface propagation;
- P1 gains approve/reject/delay/observe/final execution controls;
- `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` choices are exposed to P1;
- a broad abstraction, registry, platform helper, or new module appears;
- product source conflict is found between PRD, the P1 Model Contract, and the P1 prototype source-boundary rules;
- tests cannot be run;
- Claude Code review is unavailable and closeout would claim review PASS anyway.

## 13. Decision

Decision:

```text
READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO_WITH_BOUNDS
```

Authorized next technical action:

```text
Implement P1-CD-D inside the exact allowed file scope, then run required gates and Claude Code focused review.
```
