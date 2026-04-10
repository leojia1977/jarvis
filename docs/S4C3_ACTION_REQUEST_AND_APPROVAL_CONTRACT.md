# S4-C-3 Action Request And Approval Contract

## Scope
- Freeze how recommended actions become durable `action_requests[]`.
- Keep action execution out of scope. Sprint 4 stores reviewable requests only.
- Make approval history auditable through `lifecycle_audit[]`, not transient UI text.

## Source Of Truth
- Root: `D:\产品设计\New folder`
- Snapshot family: `S4-C`
- Contract owners:
  - Product semantics: `Claude`
  - Implementation and release: `Codex`

## Non-Goals
- No autonomous containment or destructive execution.
- No ticketing integration.
- No workflow-engine branching beyond the frozen request and approval states below.

## Frozen Action Request States
- `draft`
  - Created from `threat_case.suggested_action` when `case_view.recommended_action.action_state == "AVAILABLE"`.
- `pending_approval`
  - Analyst has submitted the request for approval.
- `approved`
  - Approval recorded as durable data.
- `rejected`
  - Approval denied as durable data.
- `cancelled`
  - Draft or pending request has been withdrawn.

Frozen transitions:
- `draft -> pending_approval | cancelled`
- `pending_approval -> approved | rejected | cancelled`
- `approved -> <none>`
- `rejected -> <none>`
- `cancelled -> <none>`

## Guardrails
- Action requests are non-destructive by default.
- `create_action_request` only stores a reviewable record; it never executes the action.
- Degraded cases suppress unsafe action enablement:
  - if `case_view.recommended_action.action_state != "AVAILABLE"`, action-request creation must fail
  - degraded or otherwise disabled recommendations must not become stored approval work
- Closed cases must not accept new or updated action requests.

## Durable Record Rules
- `PersistentCaseRecord.action_requests[]` remains the canonical durable request list.
- `CaseActionRequestRecord` remains first-class and immutable-in-practice:
  - callers must never append or mutate in place
  - helper functions must return a new `PersistentCaseRecord`
- `next_action_request_id()` and `next_audit_event_id()` remain the only authoritative ID generators.

## Audit Rules
The following audit events are frozen for Sprint 4:
- `action_request_created`
- `action_request_submitted`
- `action_request_approved`
- `action_request_rejected`
- `action_request_cancelled`

Approval history must be auditable by reading `lifecycle_audit[]` in order.

## Lifecycle Interaction
- `create_action_request` does not change `lifecycle_status`.
- `submit_action_request_for_approval`
  - moves `open -> in_review` when needed
  - requires `review_owner`
- `approve_action_request`
  - moves `in_review -> approved` when needed
- `reject_action_request`
  - keeps the case in its current review state
- `cancel_action_request`
  - keeps the case in its current lifecycle state

`lifecycle_status` is workflow state.  
`threat_case.investigation_status` remains analysis-quality state.  
They must not be conflated.

## Runtime API Contract
Frozen pilot endpoints:
- `POST /api/v1/cases/{case_id}/action-requests`
  - create one draft request from the stored case's recommended action
- `POST /api/v1/cases/{case_id}/action-requests/{action_request_id}/submit`
  - promote draft to `pending_approval`
- `POST /api/v1/cases/{case_id}/action-requests/{action_request_id}/approve`
  - record durable approval
- `POST /api/v1/cases/{case_id}/action-requests/{action_request_id}/reject`
  - record durable rejection
- `POST /api/v1/cases/{case_id}/action-requests/{action_request_id}/cancel`
  - record durable cancellation

## Required Payload Semantics
- create:
  - requires `rationale`
- submit:
  - requires `reason`
  - requires `review_owner`
- approve / reject / cancel:
  - require `reason`
- all endpoints may accept `actor`
  - default remains `secupilot.runtime` when omitted

## Required Error Semantics
- `case_not_found`
- `case_id_required`
- `rationale_required`
- `reason_required`
- `review_owner_required`
- `action_request_not_found`
- `action_request_unavailable`
- `invalid_action_request_transition`
- `case_store_unavailable`
- `internal_error`

## Acceptance
- action requests are durable data, not transient UI-only text
- approval history is reconstructable from `lifecycle_audit[]`
- degraded cases cannot create reviewable action requests
- helper functions return new immutable-style records
- runtime API and persistence layers preserve the frozen contract above
