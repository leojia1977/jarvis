# S5-C-1 Case Workflow Journey Contract

## Document Control
- Status: `draft for review`
- Baseline: `S5-C-PLAN-2026-04-13-001`
- Source of truth: `D:\产品设计\New folder`
- Purpose: case workflow journey contract
- Non-goals:
  - not implementation
  - not runtime/API/test change
  - not enterprise RBAC
  - not ticketing integration
  - not workflow engine
  - not destructive response automation
  - not external pilot execution
  - not real customer/operator sign-off

## Goal
Define the `S5-C-1 Case Workflow Journey Contract` for `pilot_local` analyst, manager, operator, and optional reviewer usage of the existing S4-C durable case lifecycle.

This is a contract and planning document only. It does not authorize implementation, runtime/API/test changes, public close-case endpoint work, external pilot execution, or real customer/operator sign-off.

## S4-C Baseline Inheritance
S5-C-1 must preserve the governed S4-C baseline accepted by `docs/S4C5_PRODUCT_REVIEW_PASS.md` and rooted in `docs/S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md`.

Inherited guarantees:
- durable case record: the persisted case remains a first-class durable record with `threat_case`, `case_view`, `action_requests[]`, and `lifecycle_audit[]`
- create/retrieve lifecycle: persisted cases can be created and retrieved through governed paths without mutating stored case data
- review/approval/close semantics: `lifecycle_status` remains explicit and separate from runtime `investigation_status`
- audit history: lifecycle and approval actions remain append-safe, ordered, durable, and replayable
- non-destructive action request semantics: approval records do not imply autonomous or destructive execution
- closed-case safety: closed cases cannot accept new or updated action requests except through existing governed safety rules
- public close-case HTTP endpoint: remains deferred unless a later governed ticket explicitly authorizes that decision

S5-C-1 may clarify journey expectations and wording. It must not add persisted states, reinterpret S4-C lifecycle transitions, or weaken non-destructive action request semantics.

## Roles
These `pilot_local` workflow roles are descriptive roles only:
- `operator`: runs governed pilot-prep, smoke, and evidence flow and may hand off created case evidence for review
- `analyst`: reviews case detail, evidence, recommendations, lifecycle context, and action request context
- `manager`: approves or denies an action request where the governed lifecycle allows a human review decision
- `reviewer`: optional governance/product reviewer for closeout evidence and workflow-contract review evidence

Role boundaries:
- these are not enterprise RBAC roles
- no authorization infrastructure is created
- role naming does not create a multi-tenant permission model
- role naming does not authorize ticketing integration, workflow-engine routing, or external pilot execution
- any future authorization, assignment, or access-control behavior requires a separate product/governance decision and implementation ticket

## Journey Stages

| Stage | Actor | Expected input | Allowed action | Expected output | Governed evidence | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- |
| Case created | `operator` or existing governed runtime path | governed case creation output from S4-C/S5-A evidence; `case_id`; initial `threat_case` and `case_view` | create or observe a persisted case only through existing governed creation paths | durable case record exists with `lifecycle_status=open`, stable `case_id`, and initial audit entry | `docs/S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md`; `docs/S4C5_PRODUCT_REVIEW_PASS.md`; `docs/S5A_REVIEW_PASS.md` | case is created through an ungoverned path, lacks `case_id`, lacks audit evidence, or implies real external pilot execution |
| Case retrieved | `analyst` | existing `case_id` and governed retrieval path | retrieve the persisted case for review | fresh reconstructed case view and persisted lifecycle data are available without mutating stored case data | S4-C create/retrieve lifecycle guarantee; S4-C product review pass | retrieval mutates stored case data, hides lifecycle status, or depends on oral/local-only knowledge |
| Analyst review | `analyst` | retrieved `case_view`, `threat_case`, evidence refs, lifecycle status, recommendations, and action request context | review details, identify questions, and decide whether manager review is needed where action request context exists | analyst review intent and rationale are ready for governed lifecycle or action-request handling | S4-C audit and action-request baseline; Sprint 5 S5-C plan | analyst language implies destructive response, bypasses manager decision, or requires enterprise RBAC/ticketing/workflow-engine scope |
| Action request review | `analyst` and optionally `manager` | `action_requests[]`, action type, targets, rationale, approval requirement, and source case status | inspect action request context and prepare approval/denial decision where allowed | action request remains non-destructive and ready for human manager decision if required | S4-C action-request schema and S4-C product review pass | action request is treated as executable containment, lacks rationale/actor context, or is reconstructed from narrative text instead of durable record fields |
| Manager approval or denial | `manager` | pending action request, rationale, target context, analyst review context, and lifecycle state | approve or deny the action request where governed lifecycle permits | approval or denial decision is recorded with actor, reason, and audit evidence; no destructive execution occurs | S4-C review/approval semantics; S4-C audit guarantee | approval is interpreted as destructive execution, denial deletes evidence, actor identity is unclear, or decision bypasses lifecycle/audit rules |
| Close decision | `analyst` or `manager` as later governed ticket defines | case lifecycle context, review outcome, action request state, and close rationale | decide whether case closure should be requested or recorded through existing governed helpers only | case is closed only through governed lifecycle rules; audit history remains intact | S4-C lifecycle status model; S4-C product review pass | workflow assumes a public close-case HTTP endpoint exists, close erases audit history, or closed-case safety is bypassed |
| Audit review | `analyst`, `manager`, or `reviewer` | `lifecycle_audit[]`, action request decisions, status changes, actors, reasons, and timestamps | review audit history for completeness and replayability | ordered audit evidence supports workflow understanding and closeout review | S4-C append-safe audit schema and product review pass | audit entries are missing, unordered, mutable, or insufficient to explain status/approval changes |
| Closeout evidence review | `reviewer` with optional `operator` / `analyst` / `manager` input | redacted workflow evidence, case identifiers where allowed, lifecycle state, audit summary, and unresolved decisions | determine whether journey evidence is clear enough for S5-C contract closeout | documented review outcome or follow-up list for later S5-C tickets | S5-C plan; S4-C product review pass; current manifest and verify report | closeout relies on oral knowledge, real customer/operator sign-off, external pilot execution, or ungoverned evidence collection |

## State / Transition Rules
- Reuse existing S4-C lifecycle semantics.
- Do not invent new persisted states unless they are marked as a future decision and governed by a later ticket.
- Approval does not mean destructive execution.
- Denial does not delete evidence.
- Close does not erase audit history.
- Closed-case modification must follow existing safety rules.
- `lifecycle_status` remains separate from runtime `investigation_status`.
- Any future lifecycle expansion must update the governed lifecycle contract before runtime/API/test changes occur.

## Ambiguity / HOLD Conditions
HOLD if:
- actor responsibility is unclear
- approval is interpreted as destructive execution
- denial or close would remove audit evidence
- workflow requires enterprise RBAC
- workflow requires ticketing integration
- workflow requires workflow engine
- workflow requires external pilot execution
- workflow changes public close-case API without separate decision
- workflow bypasses S4-C durable case lifecycle
- workflow creates new persisted states without a later governed decision
- workflow treats descriptive roles as authorization infrastructure
- workflow requires real customer/operator sign-off

## Handoff To Later S5-C Tickets
- `S5-C-2` owns close reason and lifecycle semantics.
- `S5-C-3` owns action request approval / denial contract.
- `S5-C-4` owns public close-case API decision.
- `S5-C-5` owns case workflow review pass.
- No implementation may start from S5-C-1 alone.

Any later implementation ticket must name exact files, behavior changes, acceptance criteria, and test plan before modifying runtime, API, or tests.

## Acceptance Criteria
S5-C-1 is acceptable when:
- journey stages are defined
- roles are descriptive, not RBAC
- S4-C guarantees are preserved
- destructive response automation remains out of scope
- public close-case API remains deferred
- implementation requires a later governed ticket
- no external pilot execution or real customer/operator sign-off is implied

## Preliminary Decision
This contract draft defines the pilot-local case workflow journey language needed before S5-C implementation planning can proceed.

It does not start implementation. The next step should be review-only validation of this journey contract, followed by a separate governance closeout if accepted.
