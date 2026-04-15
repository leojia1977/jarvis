# Sprint 5 Next Route After AI_COLLAB Amendment

## Document Control
- Title: Sprint 5 Next Route After AI_COLLAB Amendment
- Baseline: `AI-COLLAB-AMEND-2026-04-14-001`
- Source of truth: `D:\产品设计\New folder`
- Status: Draft for review
- Scope: Sprint 5 product-mainline route selection only
- Owner: Human-governed Sprint 5 planning

## Goal
Return Sprint 5 routing to the product mainline now that the AI collaboration operating model amendment is governed.

This checkpoint does not authorize implementation, runtime/API/schema/test/dependency changes, public endpoint work, external pilot execution, real customer/operator sign-off, real external access, or additional `docs/AI_COLLAB_OPERATING_MODEL.md` changes. It only evaluates the current governed Sprint 5 state and recommends the next separately governed product-mainline route.

## Non-Goals
- modifying `docs/AI_COLLAB_OPERATING_MODEL.md` again
- implementation work
- runtime/API/schema/test/dependency changes
- public close-case HTTP endpoint implementation
- external pilot execution
- real customer/operator sign-off
- real SIEM/EDR/source-system access
- enterprise RBAC
- ticketing integration
- workflow-engine behavior
- destructive response automation
- changing S4-C or S5-C semantics
- moving S5-B or S5-D beyond discovery without governed inputs

## Current Governed Baseline
- Active baseline is `AI-COLLAB-AMEND-2026-04-14-001`.
- `docs/AI_COLLAB_OPERATING_MODEL.md` now codifies:
  - `primary_implementor` per ticket
  - single-writer lock by ticket and file scope
  - `reviewer_when_cc_implements`
  - human final go/no-go
  - trigger-based external review
  - integration verifier checklist role
- S5-C planning/contract stream is `PASS` and safely parked.
- S5-C implementation-preparation / test-hardening mini-stream is `PASS` and safely parked.
- `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` keeps the public close-case endpoint at `KEEP_DEFERRED`.
- `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md` records all seven external pilot input categories as `UNKNOWN`, so the external pilot decision package is `NOT_READY`.
- S5-B and S5-D remain discovery-only unless source or telemetry inputs become available and a separate product/governance decision expands scope.

## Product-Mainline State Matrix

| Stream | Current evidence | Current status | What is now governed | What remains blocked | Safe next action | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- |
| S5-A external pilot input intake / assessment | `docs/S5_EXTERNAL_PILOT_DECISION_CHECKPOINT.md`; `docs/S5_EXTERNAL_PILOT_INPUT_INTAKE.md`; `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md`; HANDOFF. | S5-A preparation is closed, but external pilot inputs remain `UNKNOWN`; package readiness is `NOT_READY`. | Intake and assessment process for seven external pilot inputs. | External pilot decision package, external pilot execution, real sign-off, real external access. | Continue collecting explicit pilot inputs; do not draft pilot package yet. | Any attempt to proceed while required categories remain `UNKNOWN`. |
| S5-B source/input discovery | `docs/SPRINT5_PRD.md`; `docs/SPRINT5_JIRA_BACKLOG.md`; S5 stream review checkpoint. | Discovery/contract depth only; no current external source input evidence. | Sprint 5 boundaries for source-mode discovery, contract sketches, and fixture-only validation. | Real external source connection, live refresh, external auth, multi-tenant data ownership, CMDB sync, S4-A identity authority bypass. | Open a bounded S5-B discovery ticket focused on docs/contracts/fixtures and missing input inventory. | Source work implies production readiness or live source integration. |
| S5-C case workflow hardening | `docs/S5C_CASE_WORKFLOW_HARDENING_PLAN.md`; `docs/S5C1...S5C5`; HANDOFF. | Planning/contract stream `PASS`; safely parked. | S5-C journey, lifecycle, action-request, endpoint decision, and stream review baseline. | Runtime/API/schema/test changes, semantic changes, RBAC, ticketing, workflow engine, destructive response. | Do not continue by inertia; reopen only with product need and scoped ticket. | S5-C `PASS` is treated as runtime authorization. |
| S5-C-IMPL test-hardening mini-stream | `docs/S5C_IMPL1_DOC_TEST_ALIGNMENT.md`; `backend/tests/test_case_action_request_contract.py`; `backend/tests/test_case_lifecycle_regression.py`; `docs/S5C_IMPL4_TEST_HARDENING_REVIEW_PASS.md`. | Test-hardening mini-stream `PASS`; safely parked. | Test-only protection around action request semantics and closed-case safety. | Additional tests, production code, runtime/API/schema changes, dependency changes. | No further test work unless a new scoped ticket names exact gap and files. | Additional test edits start without a governed ticket. |
| S5-D telemetry / external-system discovery | `docs/SPRINT5_PRD.md`; `docs/SPRINT5_JIRA_BACKLOG.md`; S5 stream review checkpoint. | Discovery/fixture depth only; no current external telemetry input evidence. | Boundaries for telemetry breadth, host-selection policy discovery, queue/fan-out discovery, and fixture-only exploration. | Live EDR/SIEM access, async queue/fan-out implementation, performance commitments, S4-A identity authority bypass. | Keep parked unless telemetry-specific inputs or questions are available. | Telemetry work drifts into implementation or performance commitment. |
| AI_COLLAB operating model | `docs/AI_COLLAB_OPERATING_MODEL.md`; `docs/AI_COLLAB_OPERATING_MODEL_AMENDMENT_DECISION.md`; HANDOFF; manifest. | Governed and amended. | Ticket ownership, single-writer lock, Claude Code implementation/review separation, trigger-based external review, integration verifier, human go/no-go. | Further AI_COLLAB edits without a separate governed ticket. | Use as workflow guidance for the next product-mainline ticket. | AI_COLLAB is modified again from this checkpoint. |
| Release/governance hygiene | `docs/HANDOFF.md`; `releases/release_manifest.json`; `releases/verify_report.json`; release/review artifacts. | Current baseline aligned at `AI-COLLAB-AMEND-2026-04-14-001`. | Normal governed snapshot path and full-gate requirements. | Chat-only governance, stale review packs, manual artifact drift. | Keep this checkpoint draft-only until review/closeout. | Snapshot changes without HANDOFF/manifest/verify/review-pack alignment. |

## Candidate Next Routes

| Candidate | Meaning | Required inputs | Allowed work | Not authorized | Main risk | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- |
| `RETURN_TO_S5_B_S5_D_DISCOVERY` | Resume the deferred source/telemetry discovery lane without choosing a specific first ticket. | Product/governance choice of source-first or telemetry-first; bounded discovery questions. | Route decision or discovery planning. | Real source/telemetry access, implementation, source/telemetry production readiness. | Ambiguity lets work sprawl across both streams. | No exact first ticket or file scope is named. |
| `KEEP_PLANNING_ONLY_WAIT_FOR_EXTERNAL_INPUTS` | Pause product-mainline work and only collect external pilot/source/telemetry inputs. | Human decision to wait; owner for input collection. | Intake updates and planning notes. | Implementation, external pilot, source/telemetry integration. | Momentum stalls while no owner collects inputs. | Teams proceed from chat-only context despite wait decision. |
| `OPEN_BOUNDED_S5_B_DISCOVERY_TICKET` | Open a docs/contract/fixture-only S5-B source/input discovery ticket. | Sprint 5 PRD/backlog boundaries; S4-A identity authority; explicit no-real-access scope. | New S5-B discovery document, input inventory, source-mode questions, contract sketches, fixture-only acceptance planning. | Real external source connection, live refresh, external auth, tenancy ownership, CMDB sync, S4-A identity bypass. | Discovery language accidentally implies production source readiness. | Ticket tries to implement source mode or connect external systems. |
| `OPEN_BOUNDED_S5_D_DISCOVERY_TICKET` | Open a docs/fixture-only S5-D telemetry breadth and host-selection discovery ticket. | Telemetry-specific samples or concrete questions; S4-A identity authority and S4-B telemetry boundaries. | Telemetry breadth questions, host-selection policy discovery, fixture-only exploration plan. | Live telemetry access, async queue/fan-out implementation, performance commitments, identity authority bypass. | Discovery drifts into scale/runtime design without inputs. | Ticket includes queue/fan-out implementation or performance targets. |
| `S5_C_RUNTIME_IMPLEMENTATION_DECISION` | Decide whether S5-C should move from parked planning/test baseline into runtime/API/schema/test implementation. | Explicit product need, exact behavior, exact files, acceptance criteria, test plan, rollback/hold criteria. | Decision document only unless a later implementation ticket is approved. | Immediate implementation, public close-case endpoint opening, semantic drift, RBAC/ticketing/workflow engine. | S5-C `PASS` is mistaken for implementation approval. | Runtime/API/schema work starts from planning pass alone. |
| `SPRINT5_MILESTONE_REVIEW` | Review Sprint 5 progress across S5-A, S5-C, S5-E, and remaining S5-B/S5-D gaps. | Product/governance choice to pause for milestone review; all current governed artifacts. | Review-pass or checkpoint document. | Implementation, external pilot, source/telemetry expansion. | Milestone review becomes a substitute for choosing a concrete next stream. | Review is used to authorize implementation without next-ticket scope. |

## Recommended Route
Recommended route: `OPEN_BOUNDED_S5_B_DISCOVERY_TICKET`.

Rationale:
- AI_COLLAB governance is complete, so collaboration rules are no longer the blocker.
- S5-C is safely parked and should not continue by inertia.
- S5-A external pilot package remains `NOT_READY` because all seven external pilot input categories remain `UNKNOWN`.
- S5-B and S5-D both need input discovery before runtime implementation.
- S5-B source/input discovery can be bounded to docs, fixtures, and contracts only, producing useful missing-input evidence without real external access.
- S5-D may follow after S5-B or start earlier only if telemetry-specific inputs or questions are available.
- S5-C runtime implementation should not start until product need, exact behavior, exact files, and tests are separately decided.

This recommendation does not authorize implementation, runtime/API/schema/test/dependency changes, real source-system access, live refresh, external authentication, CMDB sync, external pilot execution, public endpoint work, or real sign-off.

## Proposed Next Ticket Shape
If product/governance accepts `OPEN_BOUNDED_S5_B_DISCOVERY_TICKET`, the next ticket should be shaped as follows.

| Field | Proposed content |
| --- | --- |
| `primary_implementor` | Human-supervised repo writer, or another explicitly named implementor. |
| `reviewer` | Claude Code review-only by default. |
| `reviewer_when_cc_implements` | Required if Claude Code is assigned as `primary_implementor`; otherwise not applicable. |
| `requires_external_review` decision | Default `false` for a docs-only discovery draft; switch to `true` if the ticket freezes or modifies a contract, changes S4-A identity authority, introduces dependency scope, changes source semantics, or closes a stream/milestone. |
| Exact files likely in scope | New `docs/S5B_SOURCE_INPUT_DISCOVERY.md`; existing `docs/SPRINT5_PRD.md`, `docs/SPRINT5_JIRA_BACKLOG.md`, S4-A source/identity docs, HANDOFF, manifest, and verify report as read-only inputs. |
| Discovery questions | What source modes need external inputs; what `api`, `hybrid`, and `bundle` mean at contract depth; what external source samples are missing; how S4-A identity authority remains authoritative; what future hold triggers require product decision. |
| Allowed evidence sources | Governed repo docs, existing synthetic/governed fixtures, read-only manifest/verify evidence, product-provided source-mode examples if explicitly supplied later. |
| Non-goals | No real external source connection, no live refresh, no external auth, no multi-tenant data ownership, no CMDB sync, no S4-A identity bypass, no runtime/API/schema/test/dependency change unless separately scoped. |
| Acceptance criteria | Discovery doc lists source modes, required external inputs, contract questions, fixture-only options, S4-A identity authority boundary, hold triggers, and next decision options. |
| Validation command if relevant | Docs-only draft may use `git status --short`; governance closeout later requires normal full gate. |
| HOLD triggers | Any implementation, real source connection, live refresh, external auth, tenancy ownership, CMDB sync, identity authority bypass, or product-semantics change. |

This is only a proposed ticket shape, not the actual S5-B ticket.

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This checkpoint is treated as implementation authorization. | It is route selection only. |
| S5-B or S5-D moves beyond discovery without governed inputs. | Sprint 5 PRD/backlog keep both discovery-limited. |
| Real external source or telemetry access is required. | Current baseline has no governed external access approval. |
| External pilot or real sign-off is implied. | S5-A input assessment remains `NOT_READY`. |
| S5-C `PASS` is treated as runtime authorization. | S5-C is parked as planning/contract and test-hardening baseline only. |
| Public close-case endpoint is opened. | S5-C-4 remains `KEEP_DEFERRED`. |
| AI_COLLAB is modified again without a separate ticket. | AI_COLLAB amendment is complete; further changes need their own governed path. |
| Single-writer, `primary_implementor`, or reviewer rules are bypassed. | The amended operating model now governs ticket execution discipline. |
| Runtime/API/schema/test/dependency changes appear. | This checkpoint and the recommended S5-B discovery route are docs/contract/fixture planning only. |

## Preliminary Verdict
Verdict: `RECOMMEND_OPEN_BOUNDED_S5_B_DISCOVERY_TICKET`.

Meaning:
- The next safest product-mainline route is a separate bounded S5-B source/input discovery ticket.
- That ticket should produce source-mode discovery and missing-input evidence without real external access.
- AI_COLLAB governed fields should shape the ticket before work starts.

Non-meaning:
- This does not authorize S5-B implementation.
- This does not authorize real source-system access.
- This does not authorize live refresh, external auth, multi-tenant ownership, CMDB sync, or identity authority changes.
- This does not authorize S5-D implementation, S5-C runtime work, public endpoint work, external pilot execution, or AI_COLLAB edits.

Allowed verdict values for this checkpoint are:
- `RECOMMEND_OPEN_BOUNDED_S5_B_DISCOVERY_TICKET`
- `RECOMMEND_OPEN_BOUNDED_S5_D_DISCOVERY_TICKET`
- `RECOMMEND_WAIT_FOR_EXTERNAL_INPUTS`
- `RECOMMEND_SPRINT5_MILESTONE_REVIEW`
- `NEEDS_PRODUCT_DECISION`
- `HOLD`

## Acceptance Criteria
This checkpoint is acceptable when:
- AI_COLLAB amendment status is reviewed
- S5-C parked status is reviewed
- S5-A `UNKNOWN` / `NOT_READY` status is reviewed
- S5-B and S5-D discovery-only boundaries are preserved
- recommended route does not authorize implementation
- next ticket shape includes AI_COLLAB governed fields
- external pilot execution and real sign-off remain unauthorized
- public close-case endpoint remains `KEEP_DEFERRED`
- preliminary verdict is one of the allowed values
