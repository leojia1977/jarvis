# S5-C-3 Action Request Approval / Denial Contract

## Document Control
- Title: S5-C-3 Action Request Approval / Denial Contract
- Baseline: `S5-C-2026-04-14-002`
- Source of truth: `D:\产品设计\New folder`
- Scope: S5-C case workflow planning / contract semantics
- Status: Draft for review
- Owner: Human-governed Sprint 5 planning

## Goal
Define pilot-local action request approval, denial/rejection, cancellation/withdrawal, and review-state semantics without changing runtime behavior.

This contract preserves S4-C durable case guarantees and clarifies that `action_request_status` is distinct from `case.lifecycle_status`.

## Non-Goals
- implementation
- runtime/API/test changes
- schema changes
- new persisted case lifecycle states
- public close-case HTTP endpoint implementation
- enterprise RBAC
- ticketing integration
- workflow-engine behavior
- destructive response automation
- external pilot execution
- real customer/operator sign-off

## Current Baseline
- `S5-C` planning is governed by `docs/S5C_CASE_WORKFLOW_HARDENING_PLAN.md`.
- `S5-C-1` defines descriptive journey roles and stages in `docs/S5C1_CASE_WORKFLOW_JOURNEY_CONTRACT.md`.
- `S5-C-2` defines close reason and lifecycle semantics in `docs/S5C2_CLOSE_REASON_AND_LIFECYCLE_SEMANTICS.md`.
- `S5-C-3` owns action request approval / denial contract semantics.
- `S5-C-4` owns any public close-case HTTP endpoint decision.
- No implementation may start from S5-C-3 alone.

## S4-C Guarantees Inherited
S5-C-3 inherits and preserves the S4-C baseline accepted by `docs/S4C5_PRODUCT_REVIEW_PASS.md` and rooted in `docs/S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md`, `docs/S4C3_ACTION_REQUEST_AND_APPROVAL_CONTRACT.md`, and `docs/S4C4_CASE_LIFECYCLE_REGRESSION_TESTS.md`.

Inherited guarantees:
- durable case record: `PersistentCaseRecord` remains the durable record for `threat_case`, `case_view`, `action_requests[]`, and `lifecycle_audit[]`
- create/retrieve lifecycle: persisted cases remain retrievable without mutating stored case data
- review/approval/close semantics: durable `lifecycle_status` remains explicit and separate from runtime `investigation_status`
- audit history: lifecycle and action-request decisions remain ordered, durable, append-safe, and replayable
- non-destructive action request semantics: approval records do not imply autonomous or destructive execution
- closed-case safety: closed cases cannot accept new or updated action requests under existing governed safety rules
- public close-case HTTP endpoint: remains deferred unless a later governed ticket explicitly authorizes that decision

## Action Request Vocabulary
These terms are contract vocabulary for pilot-local workflow clarity. They are descriptive workflow terms, not RBAC infrastructure, and they do not create enterprise authorization models.

| Term | Meaning | Boundary |
| --- | --- | --- |
| `action_request` | A durable `CaseActionRequestRecord` stored inside `PersistentCaseRecord.action_requests[]`. | It is reviewable data, not executable response automation. |
| requested action | The recommended or proposed action captured in an action request. | It does not execute external SIEM, EDR, source-system, or containment behavior. |
| reviewer | A descriptive actor who reviews case or action-request context. | Not an enterprise role, permission grant, or product sign-off authority. |
| approver | A descriptive actor who may approve or deny an action request where governed workflow allows. | Not RBAC infrastructure or external authorization. |
| approval | A durable decision accepting the action request as reviewed workflow data. | Not destructive execution, external action, or pilot authorization. |
| denial / rejection | A durable decision that the action request is not accepted. | Does not delete evidence or erase audit history. |
| cancellation / withdrawal | A durable withdrawal of a draft or pending action request where existing S4-C rules allow. | Does not erase prior request history. |
| `action_request_status` | The status on one action request, currently `draft`, `pending_approval`, `approved`, `rejected`, or `cancelled`. | Must remain separate from `case.lifecycle_status`. |
| `case.lifecycle_status` | The durable case workflow status, currently bounded to S4-C lifecycle semantics. | Must not be inferred from, renamed by, or conflated with `action_request_status`. |

## Approval Semantics
Approval means the action request has been reviewed and accepted as a governed recommendation or accepted next workflow step inside the case workflow.

Approval may record:
- the accepted action-request decision
- the reviewing actor if non-sensitive
- the decision reason after redaction
- the relationship between the decision and the existing case workflow context
- the audit evidence needed to replay the decision later

Approval must not mean:
- destructive response execution
- external EDR/SIEM/source-system action
- ticket creation
- workflow-engine routing
- real customer/operator approval
- external pilot authorization

Approval also does not collapse `action_request_status=approved` into `case.lifecycle_status=approved`. Both can exist in the S4-C model, but they remain different fields with different meanings.

## Denial / Rejection Semantics
Denial or rejection means the action request is not accepted.

Denial/rejection may record:
- that the requested action should not proceed as a governed recommendation
- the reviewing actor if non-sensitive
- the decision reason after redaction
- the action request reference
- audit evidence for later replay

Denial/rejection must not:
- delete the action request
- delete evidence
- erase audit history
- change original investigation evidence
- close the case by itself unless a later governed workflow explicitly defines that behavior

Denial is human-facing wording. The current S4-C persisted action-request status is `rejected`; `denied` must not be introduced as a new persisted case lifecycle status from this document.

## Cancellation / Withdrawal Semantics
Cancellation or withdrawal is descriptive and non-destructive.

Current S4-C semantics already define `action_request_status=cancelled` for a draft or pending request that has been withdrawn. S5-C-3 does not add a new persisted status.

Cancellation/withdrawal must:
- preserve the original action request record
- preserve prior audit history
- record the actor if non-sensitive
- record the reason after redaction
- keep evidence retrievable for later review

Cancellation/withdrawal must not:
- erase prior request history
- remove evidence
- imply destructive response execution
- close the case by itself unless a later governed workflow explicitly defines that behavior

Any broader withdrawal workflow is a future decision, not current persisted behavior.

## Relationship To Case Lifecycle
S5-C-3 preserves S4-C and S5-C-2 lifecycle vocabulary.

Rules:
- do not add persisted lifecycle states
- do not rename existing lifecycle states
- do not reinterpret `under_review` as a durable case `lifecycle_status`
- do not reinterpret `denied` as a durable case `lifecycle_status`
- keep `action_request_status` separate from `case.lifecycle_status`
- keep `case.lifecycle_status` separate from runtime `threat_case.investigation_status`
- public close-case HTTP endpoint remains deferred to `S5-C-4`

Any future persisted status, endpoint payload, API response, schema field, or test expectation requires a later governed implementation ticket.

## Audit / Evidence Requirements
Approval, denial/rejection, and cancellation/withdrawal decisions must preserve reviewable evidence without exposing sensitive material.

Required or allowed evidence:
- actor identity if non-sensitive
- timestamp or run context if available
- reason / rationale after redaction
- reference to the action request, such as `action_request_id`
- current `action_request_status`
- relevant `case.lifecycle_status`
- audit entry reference where available

Prohibited evidence:
- secret values
- raw credentials
- auth headers
- cookies
- bearer tokens
- API keys
- unredacted customer/operator payloads
- raw external SIEM/EDR/source payloads

Audit entries must remain append-safe and replayable. They must not be reconstructed from transient UI text or oral knowledge.

## HOLD Conditions
HOLD if any condition below appears.

| Condition | Why it holds |
| --- | --- |
| Approval is interpreted as destructive execution. | Violates S4-C non-destructive action request semantics. |
| Approval triggers external system action. | Introduces external SIEM/EDR/source behavior outside scope. |
| Denial deletes evidence. | Weakens durable evidence and audit guarantees. |
| Action-request status is confused with case lifecycle status. | Breaks S4-C separation between request state and case workflow state. |
| New persisted lifecycle states are introduced. | Requires a separate governed decision and implementation ticket. |
| Public close-case API is treated as authorized. | S5-C-4 owns that decision. |
| RBAC, ticketing, workflow engine, or destructive response scope appears. | Expands beyond S5-C-3 planning and contract semantics. |
| Real SIEM/EDR/source-system access is required. | Violates the no external-system access boundary. |
| Real customer/operator sign-off is required. | Violates the no real sign-off boundary. |
| External pilot execution is implied. | External pilot remains unauthorized. |
| S4-C durable lifecycle, audit history, or closed-case safety is weakened. | Reopens accepted S4-C guarantees. |
| Implementation is started from this document alone. | S5-C-3 is not an implementation authorization. |

## Handoff To Later Tickets
- `S5-C-4` owns public close-case HTTP endpoint decision.
- `S5-C-5` owns case workflow review pass.
- Any implementation ticket must name exact files, behavior changes, acceptance criteria, and test plan.
- S5-C-3 alone does not authorize implementation.

## Preliminary Decision
S5-C-3 can proceed as a contract baseline if review confirms no `P1/P2` ambiguity remains around approval, denial/rejection, cancellation/withdrawal, action-request status, case lifecycle status, and non-destructive boundaries.

Implementation remains deferred.

## Acceptance Criteria
S5-C-3 is acceptable when:
- approval semantics are non-destructive
- denial/rejection semantics preserve evidence
- cancellation/withdrawal semantics preserve prior request history
- `action_request_status` remains separate from `case.lifecycle_status`
- S4-C durable case, audit, closed-case safety, and non-destructive action request guarantees are preserved
- no runtime/API/test/schema change is authorized
- public close-case API remains deferred
- external pilot and real sign-off remain unauthorized
- later implementation requires a separate governed ticket
