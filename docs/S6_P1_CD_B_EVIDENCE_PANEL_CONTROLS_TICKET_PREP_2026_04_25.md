# S6 P1-CD-B Evidence Panel Controls Ticket Prep 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 P1-CD-B Evidence Panel Controls Ticket Prep 2026-04-25 |
| Ticket | `P1-CD-B` |
| Scope | Right contextual evidence panel controls |
| Status | IMPLEMENTED_GATE_PASS_COMMITTED_PUSHED |
| Date | 2026-04-25 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `40929a2` |
| Intake record | `docs\S6_PRODUCT_SOURCE_INTAKE_2026_04_25.md` |
| Route record | `docs\S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md` |
| P1-CD-A predecessor | `docs\S6_P1_CD_A_CASE_DETAIL_LAYOUT_TICKET_PREP_2026_04_25.md` |
| Lane | Yellow bounded frontend implementation after this prep |
| Execution surface | `codex` |
| Review surface | `claude-cmd` focused review, if available at closeout |

This record converts the selected P1 evidence-panel control ticket into an exact bounded implementation item.

It does not authorize launch, deploy, public endpoint work, external pilot execution, real-data handling, credential handling, backend/API/schema changes, static HTML copy, P2 approval implementation, P3 manager implementation, cross-surface state propagation, AI_COLLAB changes, SWE execution, staging, commit, or push by itself.

## 2. Governing Product Sources

Use this authority order:

1. `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版 (2).md`
2. `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2 (1).md`
3. `SecuPilot_P1_L2_Case_Detail_Page_Model_Contract_v0.2 (1).md`
4. `SecuPilot_Core_Surface_Logic_Collision_Walkthrough_v0.2.md`
5. `SecuPilot_High_Fidelity_UI_and_Visual_Interaction_Spec_v0.1 (1).md`
6. P1 prototype Markdown and HTML as visual / interaction references only

Binding intake constraint:

```text
HTML is visual and interaction reference only. Model Contract and PRD govern implementation. Do not copy static HTML into the production frontend as final code.
```

## 3. Exact Behavior

Implement right contextual evidence panel controls inside the existing `/case/:caseId` P1 Case Detail page.

Required behavior:

| Area | Required behavior |
| --- | --- |
| Evidence mode | Add `Auto` and `Manual` controls. `Auto` allows narrative focus/click to change the active evidence frame when not pinned. `Manual` preserves user-selected frame until another manual selection or mode change. |
| Pin / Lock | Add `Pin` / `Unpin` control for the current evidence frame. When pinned, narrative hover/focus/click must not change the active frame. Unpinning allows `Auto` to resume. |
| Manual frame switcher | Add visible buttons for the available P1/L2 frames: Process / Execution Evidence, Topology / Blast Radius Preview, Event Timeline, Attack Chain / Lineage & Confidence. Manual selection sets mode to `Manual`. |
| Narrative fallback | Add keyboard/click-accessible anchors on the existing WHAT / WHY / INTENT / HONESTY / DECISION narrative sections. The interaction may be section-level for this ticket; it must not be hover-only. |
| Active frame | Display the active evidence frame clearly and keep provenance as chip/metadata, not standard-mode headline language. |
| Existing page contract | Preserve Case Rail, Narrative Spine, HONESTY visibility, follow-up input, role-cropped navigation, and text coverage badge from P1-CD-A. |

Data mode:

```text
synthetic/local view-model data only
```

Implementation may add local frontend evidence-frame ids and section-to-frame mapping to the existing sample case objects.

## 4. Exact Non-Goals

This ticket must not implement:

- P2 Approval Surface;
- P3 Manager View;
- P1 Action Request modal;
- P1 submission to P2;
- P1 post-submit `Waiting on P2` propagation;
- P2 to P3 audit propagation;
- cross-surface route handoff;
- AR status migration E2E;
- observation-window backend signaling, polling, WebSocket, or concurrency conflict handling;
- backend/API/schema changes;
- new routes beyond the existing `/case/:caseId` behavior;
- static HTML prototype copy/paste;
- final runtime business follow-up chips or hardcoded backend-sourced messages;
- approval, reject, delayed, observe-only, or final execution-mode controls for P1;
- broad component library, reusable platform layer, registry, service layer, or design-system abstraction;
- real data, credentials, cookies, tokens, auth headers, browser session material, or external network integration.

## 5. Exact Allowed Files

Allowed files for this ticket:

- `docs/S6_P1_CD_B_EVIDENCE_PANEL_CONTROLS_TICKET_PREP_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

No other file may be changed for P1-CD-B unless a HOLD is triggered and a new decision record expands scope.

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

- the evidence panel renders `Auto`, `Manual`, and `Pin` / `Unpin` controls;
- manual frame selection sets the active evidence frame;
- pinned evidence frame does not change when a narrative anchor is clicked;
- unpinned auto mode allows a narrative anchor click to change the active evidence frame;
- evidence-panel controls are keyboard/click accessible through buttons, not hover-only;
- the follow-up input remains visible;
- P1 navigation still excludes `Approval Queue`;
- no P1 approval-mode terms such as `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` are rendered.

## 8. Max Change Budget

Maximum expected implementation scope:

- one local evidence-frame id extension;
- one local narrative-section-to-evidence mapping;
- one focused state block for evidence mode, active frame, and pin state;
- focused CSS for evidence panel controls and active frame display;
- focused test assertions for control behavior.

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

- changes product semantics beyond P1-CD-B;
- claims broad P1/P2/P3 architecture readiness;
- introduces backend/API/schema behavior;
- implements cross-surface state propagation;
- conflicts with PRD, the P1 Model Contract, or the logic-collision walkthrough;
- touches Red/HOLD trigger categories from the Go/No-Go record.

## 11. Rollback

Rollback condition:

```text
Revert P1-CD-B frontend and ticket-prep changes if frontend tests/build fail, backend guard fails, scope expands outside allowed files, or HOLD triggers fire.
```

## 12. HOLD Conditions

HOLD if:

- any implementation requires files outside the allowed file list;
- implementation needs backend/API/schema work;
- implementation tries to copy static HTML prototype code into the app;
- the Case Detail page starts implementing P2 approval authority or P3 manager behavior;
- implementation begins P1 to P2 AR propagation or P2 to P3 audit propagation;
- P1 gains approve/reject/final execution-mode controls;
- `ActionMode`, `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` are exposed to P1;
- evidence behavior becomes hover-only without click/focus fallback;
- hardcoded final business chips, unlock messages, ROI values, queue windows, or CMDB tags are introduced;
- a broad abstraction, registry, platform helper, or new module appears;
- product source conflict is found between PRD, the P1 Model Contract, and the logic-collision walkthrough;
- tests cannot be run;
- review surface is unavailable and closeout would claim review PASS anyway.

## 13. Decision

Decision:

```text
READY_FOR_EXACT_TICKET
```

Authorized next technical action:

```text
Implement P1-CD-B inside the exact allowed file scope, then run the required gates.
```

## 14. Implementation Closeout 2026-04-25

Implementation status:

```text
P1-CD-B IMPLEMENTED_GATE_PASS
```

Files changed:

- `docs/S6_P1_CD_B_EVIDENCE_PANEL_CONTROLS_TICKET_PREP_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

Implemented behavior:

- added local evidence-frame ids for the existing synthetic P1/L2 frame summaries;
- added `Auto` and `Manual` evidence-panel mode controls;
- added `Pin` / `Unpin` for the active evidence frame;
- added manual evidence-frame switcher buttons;
- added click/focus/hover narrative evidence anchors for WHAT / WHY / INTENT / HONESTY / DECISION;
- preserved keyboard/click fallback so evidence access is not hover-only;
- kept pinned/manual state from changing through narrative anchors;
- reset evidence-panel state when the active case changes;
- preserved P1-CD-A rail, narrative spine, HONESTY visibility, and follow-up input behavior;
- avoided backend/API/schema changes, P2/P3 implementation, AR propagation, route handoff, and approval-mode controls.

Focused review:

```text
claude.cmd --print focused review: P1 issues found and fixed
claude.cmd --print re-review: NO BLOCKING FINDINGS
```

Review notes accepted:

- renamed local handler so it does not look like a React hook;
- added `key={activeCase.id}` to reset local evidence state on case change;
- added `role="group"` to the Evidence mode segmented control;
- added `aria-disabled` for narrative evidence anchors when manual or pinned state blocks auto switching.

Gate results:

```text
npm run test -- --run
Result: PASS, 7 tests passed

npm run build
Result: PASS

py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
Result: PASS, 42 tests passed
```

Commit state:

```text
Committed and pushed in 66b45c8 Implement P1 evidence panel controls.
```
