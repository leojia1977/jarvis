# S5-C Case Workflow Hardening Plan

## Document Control
- Status: `draft for review`
- Baseline: `S5-PILOT-INPUT-2026-04-13-002`
- Source of truth: `D:\产品设计\New folder`
- Purpose: S5-C case workflow hardening plan
- Non-goals:
  - not implementation
  - not external pilot execution
  - not real customer/operator sign-off
  - not enterprise RBAC
  - not ticketing integration
  - not workflow engine
  - not destructive response automation

## Goal
Define the planning scope and boundaries for `S5-C Case Workflow Hardening` before any implementation begins.

This document is a planning record only. It does not start S5-C implementation, does not authorize external pilot execution, and does not change runtime behavior, tests, case APIs, or governed S4-C semantics.

## Trigger Rationale
- `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md` records all seven external pilot input categories as `UNKNOWN`.
- Therefore, an external pilot decision package is not ready.
- `S5-C` may proceed only by explicit product decision to harden case workflow while pilot inputs are collected.
- This plan records that product-planning path, not an implementation start.
- If product does not explicitly choose case workflow hardening now, the default path remains collecting or confirming the seven external pilot inputs.
- `S5-B` and `S5-D` remain discovery-only unless source/telemetry inputs become available and a separate product/governance decision expands their scope; this S5-C plan does not change S5-B/S5-D scope.

## S4-C Baseline
The governed S4-C baseline is accepted under `docs/S4C5_PRODUCT_REVIEW_PASS.md` and rooted in the schema freeze from `docs/S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md`.

Accepted S4-C guarantees:
- durable case record: one `PersistentCaseRecord` stores the governed `threat_case`, `case_view`, `action_requests[]`, and `lifecycle_audit[]`
- create/retrieve lifecycle: persisted cases can be created and retrieved through governed paths without mutating stored case data
- review/approval/close semantics: lifecycle status remains explicit and separate from runtime `investigation_status`
- audit history: analyst and manager actions remain append-only, ordered, durable, and replayable through `lifecycle_audit`
- non-destructive action request semantics: approval records do not imply autonomous or destructive execution
- closed-case safety: closed cases cannot accept new or updated action requests under the accepted S4-C guarantees
- public close-case HTTP endpoint: still deferred in the S4-C closeout unless a later governed ticket explicitly opens that decision

S5-C must preserve these guarantees. It may clarify analyst/manager workflow language, but it must not bypass, weaken, or reinterpret the S4-C durable case lifecycle.

## S5-C Scope Candidates
Candidate planning areas:
- analyst/manager journey clarification
- case close reason taxonomy
- action request denial / approval wording
- review status transition clarity
- public close-case API decision
- case workflow evidence / audit wording
- docs/tests planning only

These candidates are planning and contract targets. They do not authorize code, runtime, API, or test changes without a later explicit implementation ticket.

## Hold Triggers
Pause S5-C planning or implementation and require independent product/governance decision if any work moves toward:
- enterprise RBAC
- ticketing system integration
- workflow engine
- destructive response automation
- multi-tenant authorization model
- real customer/operator sign-off
- external pilot execution
- bypassing existing S4-C durable case semantics
- treating S5-C planning as approval to change runtime behavior without a scoped implementation ticket
- changing action-request semantics so approval implies destructive execution

## Candidate Ticket Breakdown

| Ticket | Type | Goal | Planning-first boundary | Later implementation requirement |
| --- | --- | --- | --- | --- |
| `S5-C-1 Case Workflow Journey Contract` | `DOC/INT` | Define the minimum analyst and manager journey for pilot-local case review. | Keep journey language within pilot-local analyst/manager semantics and S4-C lifecycle guarantees. | Any runtime or UI behavior change needs a separate implementation ticket and targeted tests. |
| `S5-C-2 Close Reason And Lifecycle Semantics` | `DOC` | Decide whether close reasons or lifecycle wording need a governed contract refinement. | Preserve the S4-C lifecycle status model and keep public close-case API as a decision item, not an assumed implementation. | Any new endpoint, helper, or persistence mutation requires a later scoped ticket. |
| `S5-C-3 Action Request Approval / Denial Contract` | `DOC` | Clarify approval and denial wording, rationale expectations, actor identity, and non-destructive semantics. | Keep action requests non-destructive and avoid RBAC, ticketing, workflow-engine, or external approval-system dependencies. | Any schema, API, or test change requires a later implementation ticket. |
| `S5-C-4 Public Close-Case API Decision` | `INT/DOC` | Decide whether Sprint 5 should open the deferred public close-case HTTP endpoint. | Record product need, safety criteria, and S4-C alignment before implementation is considered. | Endpoint implementation requires a separate runtime/API ticket and regression coverage. |
| `S5-C-5 Case Workflow Review Pass` | `INT` | Close the S5-C stream only after accepted planning and any separately authorized implementation are reviewed. | Verify no unresolved `P1/P2` ambiguity and no boundary drift into RBAC, ticketing, workflow engine, destructive response, or external pilot execution. | Review pass follows completed scoped tickets; it is not a substitute for implementation acceptance. |

## Acceptance Criteria For This Plan
This plan is acceptable when it:
- explains why S5-C is considered while external pilot inputs remain `UNKNOWN`
- preserves all S4-C accepted guarantees
- defines boundaries against RBAC, ticketing, workflow-engine, destructive response, real sign-off, and external pilot execution
- provides candidate tickets without starting implementation
- states that implementation requires a separate governed ticket
- keeps public close-case API work as a decision candidate unless separately approved
- keeps docs/tests planning separate from actual runtime or test changes

## Preliminary Recommendation
Recommend S5-C planning as the next product stream only if product explicitly chooses case workflow hardening while pilot inputs are collected.

If product does not make that explicit choice, continue collecting or confirming the seven external pilot inputs using `docs/S5_EXTERNAL_PILOT_INPUT_INTAKE.md` and `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md`.

S5-C implementation should not begin from this document alone. A later governed ticket must define exact files, behavior changes, acceptance criteria, and test plan before any code, runtime, API, or test changes are made.

## Acceptance
`S5C_CASE_WORKFLOW_HARDENING_PLAN` is complete when:
- it records the S5-C trigger rationale from the external pilot input assessment
- it anchors S5-C to the accepted S4-C case lifecycle baseline
- it defines candidate scope without starting implementation
- it lists hold triggers for governance and product-scope drift
- it provides planning-first candidate tickets
- it preserves external pilot execution as unauthorized
