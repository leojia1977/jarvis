# Sprint 5 Stream Review Checkpoint

## Document Control
- Title: Sprint 5 Stream Review Checkpoint
- Baseline: `S5-C-IMPL-2026-04-14-004`
- Source of truth: `D:\产品设计\New folder`
- Status: Draft for review
- Scope: Sprint 5 route selection / planning checkpoint only
- Owner: Human-governed Sprint 5 planning

## Goal
Review the current Sprint 5 stream state and recommend the safest next route after S5-A, S5-C, S5-C-IMPL, and S5-E/collaboration guidance work have produced governed baselines.

This checkpoint does not authorize implementation, runtime/API/schema/test changes, dependency changes, public close-case endpoint work, external pilot execution, real customer/operator sign-off, or real SIEM/EDR/source-system access. It only records route-selection evidence and a preliminary recommendation for the next separately governed ticket.

## Non-Goals
- production implementation
- runtime/API/schema/test changes
- dependency changes
- public close-case HTTP endpoint implementation
- S4-C or S5-C semantic changes
- external pilot execution
- real customer/operator sign-off
- real SIEM/EDR/source-system access
- enterprise RBAC
- ticketing integration
- workflow-engine behavior
- destructive response automation
- modifying `docs/AI_COLLAB_OPERATING_MODEL.md` directly from this checkpoint

## Current Governed Baseline
- Active baseline is `S5-C-IMPL-2026-04-14-004`.
- `docs/HANDOFF.md` and `releases/release_manifest.json` both record `S5-C-IMPL-2026-04-14-004`.
- `releases/verify_report.json` records verification for `S5-C-IMPL-2026-04-14-004`.
- S5-C planning/contract stream is `PASS`.
- S5-C implementation-preparation / test-hardening mini-stream is `PASS`.
- `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` keeps the public close-case HTTP endpoint at `KEEP_DEFERRED`.
- External pilot execution remains unauthorized.
- No real customer/operator sign-off exists in governed repo evidence.
- `S5-B` and `S5-D` remain discovery-only unless source or telemetry inputs become available and a separate product/governance decision expands their scope.

## Sprint 5 Stream Matrix

| Stream | Current governed evidence | Current status | What is authorized | What remains blocked or discovery-only | Recommended next action | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- |
| S5-A external pilot input intake / assessment | `docs/S5_EXTERNAL_PILOT_DECISION_CHECKPOINT.md`; `docs/S5_EXTERNAL_PILOT_INPUT_INTAKE.md`; `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md`; S5-A review pass in HANDOFF. | S5-A prep is closed; all seven external pilot input categories remain `UNKNOWN`; external pilot package is `NOT_READY`. | Continue collecting or explicitly accepting the seven external pilot inputs. | External pilot decision package, external pilot execution, real sign-off, real external access. | Keep intake/assessment as input collection path unless product provides all seven categories. | Any attempt to draft or start external pilot package while inputs remain `UNKNOWN`. |
| S5-B source/input discovery | `docs/SPRINT5_PRD.md`; `docs/SPRINT5_JIRA_BACKLOG.md`; Sprint 5 discovery brief. | Discovery/contract depth only. | In-repo source-mode discovery and contract sketches if scoped by separate ticket. | Real source-system connection, live refresh, external auth, multi-tenant data ownership, CMDB sync, S4-A identity bypass. | Wait for external source inputs or open a bounded discovery-only doc ticket. | Source work moves to implementation without source samples/product decision. |
| S5-C case workflow hardening | `docs/S5C_CASE_WORKFLOW_HARDENING_PLAN.md`; `docs/S5C1...S5C5` docs. | Planning/contract stream `PASS`. | Use S5-C contracts as future scoped-ticket baseline. | Runtime/API/schema/test changes, public endpoint implementation, semantic changes, RBAC/ticketing/workflow engine. | Park safely unless a new scoped implementation/test ticket is selected. | S5-C `PASS` is treated as runtime authorization. |
| S5-C-IMPL implementation-preparation / test-hardening | `docs/S5C_IMPL1_DOC_TEST_ALIGNMENT.md`; `backend/tests/test_case_action_request_contract.py`; `backend/tests/test_case_lifecycle_regression.py`; `docs/S5C_IMPL4_TEST_HARDENING_REVIEW_PASS.md`. | Mini-stream `PASS`; test-hardening baseline accepted. | Use existing hardened tests as governed protection and future ticket evidence. | Additional test edits, runtime/API/schema changes, production implementation. | Do not continue test hardening by default unless product selects another scoped test-only ticket. | New tests or behavior changes start without exact scoped ticket. |
| S5-D telemetry / external-system discovery | `docs/SPRINT5_PRD.md`; `docs/SPRINT5_JIRA_BACKLOG.md`; Sprint 5 discovery brief. | Discovery/fixture depth only. | Documentation or fixture-only discovery if external telemetry inputs or bounded questions exist. | Live EDR/SIEM access, async queue/fan-out, performance commitments, S4-A identity authority bypass. | Wait for telemetry breadth inputs or open a bounded discovery-only doc/fixture ticket. | Telemetry work moves to implementation without external inputs or identity-authority routing. |
| S5-E collaboration guidance / AI operating model | `docs/AI_COLLAB_OPERATING_MODEL.md`; `docs/S5E1...S5E3`; manifest governed key file; HANDOFF. | AI collaboration operating model is governed as collaboration guidance. | Use current guidance for source-of-truth, one-writer, role assignment, review, and snapshot discipline. | Direct AI_COLLAB edits from this checkpoint; external tool dependencies; workflow rewrite without ticket. | Open a separate docs-only amendment decision ticket for pending execution-rule clarifications. | AI_COLLAB is modified without a governed amendment ticket. |
| Release/governance hygiene | `docs/HANDOFF.md`; `releases/release_manifest.json`; `releases/verify_report.json`; release/review artifacts. | Current baseline is aligned at `S5-C-IMPL-2026-04-14-004`. | Use normal snapshot path for any governed route selected next. | Manual artifact edits outside full gate, stale review packs, chat-only governance. | Keep route decision separate from closeout; require full gate only during governance closeout. | Snapshot changes without HANDOFF/manifest/verify/review-pack alignment. |

## Candidate Next Routes

| Candidate | Meaning | Required inputs | Allowed work | Not authorized | Main risk | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- |
| `CONTINUE_TEST_ONLY_HARDENING` | Add another scoped test-only ticket after IMPL-2/3/4. | Concrete test gap, exact test file, unchanged semantics, targeted test command. | Test-only changes in named files. | Production code, runtime/API/schema changes, dependency changes, public endpoint work. | Test hardening becomes semantic redesign by assertion. | Test expectations redefine S4-C/S5-C contracts or introduce endpoint/lifecycle behavior. |
| `S5_C_RUNTIME_IMPLEMENTATION_DECISION` | Decide whether any S5-C runtime/API/schema implementation should be scoped. | Explicit product need, exact files, behavior changes, acceptance criteria, test plan, rollback/hold rules. | Draft a planning/decision document only unless later implementation ticket is approved. | Immediate implementation, public endpoint opening, semantic drift, RBAC/ticketing/workflow engine. | S5-C planning `PASS` is mistaken for implementation approval. | Runtime/API/schema work starts from checkpoint text alone. |
| `RETURN_TO_S5_B_S5_D_DISCOVERY` | Revisit source or telemetry discovery while external pilot inputs remain unavailable. | Source samples, telemetry samples, or bounded fixture/discovery questions. | Discovery docs or fixture-only exploration under exact scope. | Real external access, external auth, live refresh, CMDB sync, queue/fan-out, performance commitments. | Discovery drifts into production integration. | No external inputs exist but implementation assumptions appear. |
| `AI_COLLAB_OPERATING_MODEL_AMENDMENT_DECISION` | Decide whether to amend governed collaboration guidance with execution-rule clarifications already being used in practice. | Current AI_COLLAB, HANDOFF practice, recent ticket patterns, explicit amendment scope. | Docs-only amendment decision ticket; optionally later AI_COLLAB wording patch if separately authorized. | Direct AI_COLLAB modification from this checkpoint, product/runtime changes, external tool dependencies. | Process work distracts from product route or over-constrains normal tickets. | AI_COLLAB is modified without a separate governed amendment ticket. |
| `KEEP_PLANNING_ONLY / WAIT_FOR_EXTERNAL_INPUTS` | Do not start another implementation or discovery stream now. | Product decision to pause or wait; list of missing external inputs. | Continue evidence collection and planning notes only. | Implementation, external pilot, endpoint work, source/telemetry integration. | Momentum loss or ambiguous ownership of next decision. | Teams proceed from chat-only context without structured ticket. |

## Operating Model Pending Amendment Note
`docs/AI_COLLAB_OPERATING_MODEL.md` is governed as collaboration workflow guidance. The following items remain amendment candidates and should not be treated as newly governed rules until a separate ticket accepts and governs them:
- `primary_implementor` must be named per ticket
- single-writer lock should be explicit by ticket and file scope
- Claude Code remains review-only by default unless explicitly assigned as implementor
- `reviewer_when_cc_implements` is required if Claude Code implements
- Claude Code cannot be sole reviewer of its own implementation
- AI provides governance recommendations; the human makes go/no-go decisions
- Claude Web is high-value external review, not a default blocker for routine tickets
- `requires_external_review` should have mandatory trigger categories
- integration verifier may be defined as a checklist role at stream or milestone closeout

Any AI collaboration operating model amendment requires a separate governed docs-only ticket. This checkpoint does not modify `docs/AI_COLLAB_OPERATING_MODEL.md`.

## Recommended Route
Recommended route: `AI_COLLAB_OPERATING_MODEL_AMENDMENT_DECISION`.

Rationale:
- S5-C is safely parked: planning/contract stream is `PASS`, test-hardening mini-stream is `PASS`, and public close-case endpoint remains `KEEP_DEFERRED`.
- S5-A external pilot inputs remain `UNKNOWN`, so external pilot package work remains premature.
- S5-B and S5-D remain discovery-only because no current governed evidence supplies source or telemetry inputs.
- The operating-model rules listed above are already being used in ticket practice but are not yet codified as explicit governed amendment language.
- A docs-only amendment decision is low-risk, repo-local, and can improve future ticket clarity before another implementation stream begins.

This recommendation does not modify `docs/AI_COLLAB_OPERATING_MODEL.md` directly. It does not authorize implementation, does not reopen S5-C semantics, does not authorize external pilot execution, and does not authorize public endpoint work.

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This checkpoint is treated as implementation authorization. | It is route selection only. |
| Runtime/API/schema/test/dependency changes are introduced. | This checkpoint allows no code, test, runtime, schema, or dependency changes. |
| Public close-case endpoint is treated as opened. | S5-C-4 remains `KEEP_DEFERRED`. |
| External pilot or real sign-off is implied. | External pilot inputs remain `UNKNOWN`; real sign-off is absent. |
| S5-B/S5-D move from discovery to implementation without source/telemetry inputs. | Sprint 5 PRD/backlog keep them discovery-only until inputs exist. |
| S5-C `PASS` is treated as runtime authorization. | S5-C PASS is planning/contract and test-hardening baseline only. |
| AI_COLLAB is modified without a separate governed amendment ticket. | This checkpoint only recommends an amendment decision route. |
| Single-writer or reviewer rules are bypassed. | Collaboration governance depends on explicit role and file-scope discipline. |

## Future Ticket Requirements

Any next ticket must include:
- `primary_implementor`
- `reviewer`
- `reviewer_when_cc_implements` if relevant
- exact files
- exact behavior, doc, or test changes
- acceptance criteria
- validation command if relevant
- redaction/secret handling check if relevant
- hold/rollback criteria
- external review requirement decision

For the recommended AI_COLLAB amendment decision route, the next ticket should be docs-only and must state whether it only drafts an amendment decision or also authorizes a later bounded edit to `docs/AI_COLLAB_OPERATING_MODEL.md`.

## Preliminary Verdict
Verdict: `RECOMMEND_AI_COLLAB_AMENDMENT_DECISION`.

Meaning:
- The safest next route is a separate governed docs-only decision ticket about whether to amend `docs/AI_COLLAB_OPERATING_MODEL.md` with execution-rule clarifications.
- Product/runtime streams should remain parked unless product/governance selects a new scoped ticket with required inputs.

Non-meaning:
- This does not authorize implementation.
- This does not authorize AI_COLLAB edits.
- This does not authorize test edits.
- This does not authorize public close-case endpoint work.
- This does not authorize external pilot execution or real sign-off.

## Acceptance Criteria
This checkpoint is acceptable when:
- all Sprint 5 streams are reviewed
- S5-C remains parked safely
- S5-C implementation-preparation / test-hardening `PASS` is treated as baseline acceptance only
- S5-B and S5-D discovery-only boundaries are preserved
- public close-case endpoint remains `KEEP_DEFERRED`
- external pilot execution and real customer/operator sign-off remain unauthorized
- `docs/AI_COLLAB_OPERATING_MODEL.md` is not modified by this checkpoint
- recommended next route requires a separate governed ticket
- future ticket requirements include implementor, reviewer, exact files, exact changes, acceptance, validation, redaction when relevant, hold/rollback, and external review decision
