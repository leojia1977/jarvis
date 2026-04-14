# S5-C-2 Close Reason And Lifecycle Semantics

## Document Control
- Status: `draft for review`
- Baseline: `S5-C-2026-04-13-001`
- Source of truth: `D:\产品设计\New folder`
- Purpose: close reason and lifecycle semantics contract
- Non-goals:
  - not implementation
  - not runtime/API/test change
  - not public close-case API implementation
  - not enterprise RBAC
  - not ticketing integration
  - not workflow engine
  - not destructive response automation
  - not external pilot execution
  - not real customer/operator sign-off

## Goal
Define the `S5-C-2 Close Reason And Lifecycle Semantics` contract for pilot-local case workflow hardening.

This document clarifies close reasons and lifecycle wording for the existing S4-C durable case lifecycle. It does not authorize implementation, does not add or rename persisted states, and does not open the deferred public close-case HTTP endpoint.

## S4-C Baseline Inheritance
S5-C-2 preserves the governed S4-C baseline accepted by `docs/S4C5_PRODUCT_REVIEW_PASS.md` and rooted in `docs/S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md`, `docs/S4C3_ACTION_REQUEST_AND_APPROVAL_CONTRACT.md`, and `docs/S4C4_CASE_LIFECYCLE_REGRESSION_TESTS.md`.

Inherited guarantees:
- durable case record: the persisted case remains a first-class durable record with `threat_case`, `case_view`, `action_requests[]`, and `lifecycle_audit[]`
- create/retrieve lifecycle: persisted cases can be created and retrieved through governed paths without mutating stored case data
- review/approval/close semantics: `lifecycle_status` remains explicit and separate from runtime `investigation_status`
- audit history: lifecycle and approval actions remain append-safe, ordered, durable, and replayable
- non-destructive action request semantics: approval records do not imply autonomous or destructive execution
- closed-case safety: closed cases cannot accept new or updated action requests except through existing governed safety rules
- public close-case HTTP endpoint: remains deferred unless a later governed ticket explicitly authorizes that decision

S5-C-2 may clarify close reason language and lifecycle meaning. It must not bypass, weaken, or reinterpret S4-C durable case semantics.

## Lifecycle Vocabulary
The current governed durable case lifecycle remains bounded by S4-C.

| Term | Contract meaning | Current persisted state? | Notes |
| --- | --- | --- | --- |
| `open` | Case is active and available for analyst review, action-request creation where allowed, or closure through governed helpers. | Yes | Preserved from S4-C. |
| `in_review` | Case is under human review after an action request is submitted or review ownership is assigned. | Yes | Preserved from S4-C. |
| `under_review` | Operator-facing wording for the same semantic phase as `in_review`. | No | Must not be persisted as a new state unless a later governed decision renames or expands lifecycle status. |
| `approved` | A human review decision accepted the current action direction or case disposition. | Yes | Current S4-C durable case `lifecycle_status`; must remain distinct from action-request approval semantics and destructive execution. |
| `denied` | Human-facing wording for an action request being denied or rejected. | No | Maps to action-request `rejected`; it is not a current durable case `lifecycle_status`. |
| `closed` | Analyst workflow is concluded. | Yes | Closure does not erase audit history and does not imply remediation executed. |
| `close_pending` | Potential future state for a close request that requires separate approval. | Future decision only | Not a current persisted state and must not appear in stored records without a later governed ticket. |

Any other lifecycle term must be marked as a future decision, not treated as a current persisted state.

## Close Reason Taxonomy
Close reasons describe why a case workflow is concluded. They do not replace the original case evidence, case summary, severity, action-request rationale, or lifecycle audit entries.

| Close reason | Meaning | Allowed actor type | Required evidence note | Audit requirement | Action request approval required? | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- |
| `resolved_false_positive` | The reviewed evidence supports closing the case because the alert or hypothesis is not security-relevant in context. | `analyst` or `manager` as later governed ticket defines | Note the governed evidence reviewed and why it does not support security action. | Append or preserve a close audit entry with actor and reason. | No, unless an existing pending action request must be resolved by governed action-request rules first. | Reason is oral-only, rewrites evidence, or hides unresolved action requests. |
| `resolved_expected_activity` | The activity is expected or approved operational behavior based on reviewed evidence. | `analyst` or `manager` as later governed ticket defines | Record the expected-activity basis without storing sensitive external approval artifacts. | Append or preserve a close audit entry with actor and reason. | No, unless an existing pending action request must be resolved by governed action-request rules first. | Reason depends on ungoverned external sign-off, ticketing integration, or private customer data. |
| `resolved_contained` | The case can close because containment or mitigation is recorded outside SecuPilot's non-destructive action semantics. | `manager` preferred, or `analyst` if later governed scope allows | Record only a redacted operational note that containment is outside SecuPilot execution. | Append or preserve a close audit entry with actor and reason. | Yes if a governed action request remains pending and needs approval/rejection before closure; otherwise no. | Close reason implies SecuPilot executed destructive response or autonomous remediation. |
| `duplicate_case` | The case is a duplicate of another case already being tracked. | `analyst` or `manager` as later governed ticket defines | Reference the duplicate relationship using non-sensitive case identifiers where allowed. | Append or preserve a close audit entry with actor, reason, and duplicate reference. | No, unless an existing pending action request must be resolved first. | Duplicate target is unavailable, sensitive, oral-only, or requires ticketing/workflow-engine integration. |
| `insufficient_evidence` | Available evidence is not enough to justify further governed workflow action. | `analyst` or `manager` as later governed ticket defines | State what evidence was reviewed and what remains insufficient. | Append or preserve a close audit entry with actor and reason. | No, unless an existing pending action request must be rejected or cancelled first. | Closure deletes evidence, suppresses audit, or masks unresolved severity/action ambiguity. |
| `out_of_scope` | The case falls outside the pilot-local case workflow scope or accepted product boundary. | `manager` preferred, or `analyst` if later governed scope allows | Record the boundary that makes the case out of scope without introducing external workflow dependency. | Append or preserve a close audit entry with actor and reason. | No, unless an existing pending action request must be resolved first. | Reason expands scope into external pilot execution, RBAC, ticketing, workflow engine, or real customer/operator sign-off. |
| `deferred_to_external_process` | Follow-up is intentionally outside SecuPilot and must be handled by a separate external process. | `manager` preferred | Record a redacted note that responsibility is outside SecuPilot, without storing external ticket details or sensitive payloads. | Append or preserve a close audit entry with actor and reason. | Yes if a governed action request remains pending and must be approved/rejected/cancelled before closure; otherwise no. | Reason requires ticketing integration, workflow-engine routing, or real external-system connectivity. |

Close reasons are contract-level taxonomy candidates for S5-C planning. Persisting them as a new field, endpoint payload, or API response requires a later governed implementation ticket.

## Transition Semantics
- Close does not erase audit history.
- Denial does not delete evidence.
- Approval does not execute destructive response.
- Close reason does not change original investigation evidence.
- Close reason does not replace case summary or case severity.
- Close reason does not replace action-request rationale, approval reason, rejection reason, or cancellation reason.
- Closed-case modification must follow existing S4-C safety rules.
- Public close-case HTTP endpoint remains a separate decision under `S5-C-4`.
- `lifecycle_status` remains separate from runtime `investigation_status`.
- New persisted lifecycle states require a separate governed decision before runtime, API, test, or manifest changes occur.

## Ambiguity / HOLD Conditions
HOLD if:
- close reason is unclear or oral-only
- close reason implies destructive action
- close removes or rewrites audit history
- denial deletes evidence
- approval is interpreted as response execution
- close reason requires external ticketing or workflow engine
- close reason requires enterprise RBAC
- public close-case API is treated as already authorized
- new persisted lifecycle states are introduced without separate decision
- close reason changes original investigation evidence, case summary, case severity, or action-request rationale
- close reason depends on real customer/operator sign-off
- close reason authorizes external pilot execution

## Handoff To Later S5-C Tickets
- `S5-C-3` owns action request approval / denial contract.
- `S5-C-4` owns public close-case API decision.
- `S5-C-5` owns case workflow review pass.
- No implementation may start from S5-C-2 alone.

Any later implementation ticket must name exact files, behavior changes, acceptance criteria, and test plan before modifying runtime, API, persistence schema, or tests.

## Acceptance Criteria
S5-C-2 is acceptable when:
- close reason taxonomy is defined
- lifecycle vocabulary is bounded to S4-C semantics or marked future decision
- approval, denial, and close boundaries are clear
- S4-C guarantees are preserved
- public close-case API remains deferred
- implementation requires a later governed ticket
- no enterprise RBAC, ticketing integration, workflow engine, destructive response automation, external pilot execution, or real customer/operator sign-off is implied

## Preliminary Decision
This contract draft defines bounded close reason and lifecycle semantics for pilot-local case workflow hardening.

It does not start implementation. The next step should be review-only validation of this contract, followed by a separate governance closeout if accepted.
