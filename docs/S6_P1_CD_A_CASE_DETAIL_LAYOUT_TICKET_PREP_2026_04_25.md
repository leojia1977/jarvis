# S6 P1-CD-A Case Detail Layout Ticket Prep 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 P1-CD-A Case Detail Layout Ticket Prep 2026-04-25 |
| Ticket | `P1-CD-A` |
| Scope | Case Detail layout regions and narrative spine |
| Status | IMPLEMENTED_GATE_PASS_PENDING_STAGE_COMMIT_PUSH |
| Date | 2026-04-25 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `4d6b380` |
| Intake record | `docs\S6_PRODUCT_SOURCE_INTAKE_2026_04_25.md` |
| Route record | `docs\S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md` |
| Lane | Yellow bounded frontend implementation after this prep |
| Execution surface | `codex` |
| Review surface | `claude-cmd` focused review, if available at closeout |

This record converts the selected first core-surface ticket into an exact bounded implementation item.

It does not authorize launch, deploy, public endpoint work, external pilot execution, real-data handling, credential handling, backend/API/schema changes, static HTML copy, P2 approval implementation, P3 manager implementation, AI_COLLAB changes, SWE execution, staging, commit, or push by itself.

## 2. Governing Product Sources

Use this authority order:

1. `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版 (2).md`
2. `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2 (1).md`
3. `SecuPilot_P1_L2_Case_Detail_Page_Model_Contract_v0.2 (1).md`
4. `SecuPilot_High_Fidelity_UI_and_Visual_Interaction_Spec_v0.1 (1).md`
5. P1 prototype Markdown and HTML as visual / interaction references only

Binding intake constraint:

```text
HTML is visual and interaction reference only. Model Contract and PRD govern implementation. Do not copy static HTML into the production frontend as final code.
```

## 3. Exact Behavior

Implement a P1/L2 Case Detail layout skeleton on the existing `/case/:caseId` route.

Required visible regions:

| Region | Required behavior |
| --- | --- |
| App Shell | Preserve existing SecuPilot shell, role selector, role-cropped navigation, global conversation input, and text coverage badge. |
| Case Header | Preserve the current case as the absolute page object with case id, title, lifecycle state, and coverage context. |
| Left Case Rail | Add persistent rail sections for `Case Lifecycle`, `Processing Trace`, and `Action Request`. Treat processing trace as provenance, not case lifecycle. |
| Center Narrative Spine | Add fixed ordered sections: `WHAT`, `WHY`, `INTENT`, `HONESTY`, `DECISION`. `HONESTY` must be default visible. |
| Right Evidence Region | Reserve a contextual evidence region with non-interactive, read-only frame summaries only. Do not implement Auto / Manual / Pin behavior in this ticket. |
| Dialogue Dock | Keep the case follow-up input visible at the bottom of Case Detail. |

Data mode:

```text
synthetic/local view-model data only
```

Implementation may add local frontend fields to the existing sample case objects when needed to render the exact P1-CD-A regions.

## 4. Exact Non-Goals

This ticket must not implement:

- P2 Approval Surface;
- P3 Manager View;
- P1 Action Request modal;
- P1 approval, reject, delayed, observe-only, or final execution-mode controls;
- `ActionMode`, `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` choices for P1;
- right-panel Auto / Manual / Pin controls;
- narrative-to-evidence hover/focus/click switching;
- backend/API/schema changes;
- new routes beyond the existing `/case/:caseId` behavior;
- static HTML prototype copy/paste;
- hardcoded final business follow-up chips, unlock messages, queue windows, ROI values, CMDB business tags, or remediation suggestions;
- broad component library, reusable platform layer, registry, service layer, or design-system abstraction;
- real data, credentials, cookies, tokens, auth headers, browser session material, or external network integration.

## 5. Exact Allowed Files

Allowed files for this ticket:

- `docs/S6_P1_CD_A_CASE_DETAIL_LAYOUT_TICKET_PREP_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

No other file may be changed for P1-CD-A unless a HOLD is triggered and a new decision record expands scope.

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

## 7. Required Assertions

Automated or closeout-visible assertions must cover:

- `/case/CASE-001` renders `Case Lifecycle`, `Processing Trace`, and `Action Request`;
- `/case/CASE-001` renders `WHAT`, `WHY`, `INTENT`, `HONESTY`, and `DECISION` in the Case Detail page;
- `HONESTY` is visible by default and includes unsupported or confidence-limiting language;
- the right evidence region renders as read-only frame summaries;
- the Case Detail follow-up input remains visible;
- P1 navigation still excludes `Approval Queue`;
- no P1 approval-mode terms such as `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` are rendered.

## 8. Max Change Budget

Maximum expected implementation scope:

- one local Case Detail view-model extension;
- one Case Detail JSX restructure;
- focused CSS for a responsive three-region detail layout plus persistent dialogue dock;
- focused test assertions for the new layout regions.

Do not introduce new modules, helpers, directories, dependencies, or generalized component registries.

## 9. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- execution surface is currently `codex`;
- the ticket is small and tightly coupled to the current frontend scaffold;
- no separate SWE command path is required for this bounded implementation.

## 10. Review Path

Required review path:

```text
Focused code review after implementation diff, preferably via claude-cmd / Claude Code if available.
```

Claude Web / external product-architecture-governance review is not required for this ticket unless implementation:

- changes product semantics beyond P1-CD-A;
- claims broad P1/P2/P3 architecture readiness;
- introduces backend/API/schema behavior;
- conflicts with PRD or Model Contract wording;
- touches Red/HOLD trigger categories from the Go/No-Go record.

## 11. Rollback

Rollback condition:

```text
Revert P1-CD-A frontend and ticket-prep changes if frontend tests/build fail, backend guard fails, scope expands outside allowed files, or HOLD triggers fire.
```

## 12. HOLD Conditions

HOLD if:

- any implementation requires files outside the allowed file list;
- implementation needs backend/API/schema work;
- implementation tries to copy static HTML prototype code into the app;
- the Case Detail page starts implementing P2 approval authority or P3 manager behavior;
- P1 gains approve/reject/final execution-mode controls;
- `ActionMode`, `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` are exposed to P1;
- right-panel Auto / Manual / Pin behavior becomes necessary to pass tests;
- hardcoded final business chips, unlock messages, ROI values, queue windows, or CMDB tags are introduced;
- a broad abstraction, registry, platform helper, or new module appears;
- product source conflict is found between PRD and the P1 Model Contract;
- tests cannot be run;
- review surface is unavailable and closeout would claim review PASS anyway.

## 13. Decision

Decision:

```text
READY_FOR_EXACT_TICKET
```

Authorized next technical action:

```text
Implement P1-CD-A inside the exact allowed file scope, then run the required gates.
```

## 14. Implementation Closeout 2026-04-25

Implementation status:

```text
P1-CD-A IMPLEMENTED_GATE_PASS
```

Files changed:

- `docs/S6_P1_CD_A_CASE_DETAIL_LAYOUT_TICKET_PREP_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

Implemented behavior:

- added local synthetic P1/L2 Case Detail view-model fields;
- added left Case Rail with `Case Lifecycle`, `Processing Trace`, and `Action Request`;
- added center Narrative Spine with `WHAT`, `WHY`, `INTENT`, `HONESTY`, and `DECISION`;
- kept `HONESTY` visible by default;
- added right `Contextual Evidence` region as read-only frame summaries only;
- preserved the persistent Case Detail follow-up input;
- avoided P2/P3 implementation, backend/API/schema changes, static HTML copy, approval controls, and final execution-mode controls.

Focused review:

```text
claude.cmd --print focused review: NO BLOCKING FINDINGS
```

Review notes accepted:

- replaced text-content React keys with section/index keys;
- added test assertions that the evidence panel contains no button or textbox controls.

Gate results:

```text
npm run test -- --run
Result: PASS, 6 tests passed

npm run build
Result: PASS

py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
Result: PASS, 42 tests passed
```

Local preview:

```text
http://127.0.0.1:5173/case/CASE-001
```

Commit state:

```text
Not staged, not committed, not pushed in this closeout.
```
