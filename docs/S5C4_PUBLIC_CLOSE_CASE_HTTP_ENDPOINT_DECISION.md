# S5-C-4 Public Close-Case HTTP Endpoint Decision

## Document Control
- Title: S5-C-4 Public Close-Case HTTP Endpoint Decision
- Baseline: `S5-C-2026-04-14-003`
- Source of truth: `D:\产品设计\New folder`
- Scope: S5-C case workflow planning / endpoint decision
- Status: Draft for review
- Owner: Human-governed Sprint 5 planning

## Goal
Decide whether the previously deferred public close-case HTTP endpoint should remain deferred or become eligible for a later scoped implementation ticket.

S5-C-4 does not implement the endpoint. It does not authorize endpoint implementation by itself. Any future implementation requires a separate governed ticket with exact files, behavior changes, acceptance criteria, and test plan.

## Non-Goals
- endpoint implementation
- runtime/API/test changes
- schema changes
- new persisted lifecycle states
- changing S5-C-2 close reason/lifecycle semantics
- changing S5-C-3 action request approval/denial semantics
- enterprise RBAC
- ticketing integration
- workflow-engine behavior
- destructive response automation
- external pilot execution
- real customer/operator sign-off
- real SIEM/EDR/source-system access

## Current Baseline
- `S5-C` planning is governed by `docs/S5C_CASE_WORKFLOW_HARDENING_PLAN.md`.
- `S5-C-1` defines descriptive journey roles and stages in `docs/S5C1_CASE_WORKFLOW_JOURNEY_CONTRACT.md`.
- `S5-C-2` defines close reason and lifecycle semantics in `docs/S5C2_CLOSE_REASON_AND_LIFECYCLE_SEMANTICS.md`.
- `S5-C-3` defines action request approval / denial semantics in `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`.
- `S5-C-4` owns the public close-case HTTP endpoint decision.
- `S5-C-5` owns the case workflow review pass.
- `S4-C` deferred the public close-case HTTP endpoint.
- No implementation may start from S5-C-4 alone.

## S4-C / S5-C Guarantees Inherited
S5-C-4 inherits and must preserve the accepted S4-C and S5-C contract guarantees.

Inherited guarantees:
- durable case record: `PersistentCaseRecord` remains the durable record for `threat_case`, `case_view`, `action_requests[]`, and `lifecycle_audit[]`
- create/retrieve lifecycle: persisted cases remain retrievable without mutating stored case data
- review/approval/close semantics: durable `lifecycle_status` remains explicit and separate from runtime `investigation_status`
- audit history: lifecycle and action-request decisions remain ordered, durable, append-safe, and replayable
- non-destructive action request semantics: approval records do not imply autonomous or destructive execution
- closed-case safety: closed cases remain protected by existing governed safety rules
- public close-case HTTP endpoint was deferred until a later governed decision
- close reasons remain governed by S5-C-2
- action request approval/denial remains governed by S5-C-3

## Decision Options

| Option | Meaning | When to use | Non-meaning |
| --- | --- | --- | --- |
| `KEEP_DEFERRED` | The public close-case HTTP endpoint remains deferred. | Safe default if product need, actor authority, lifecycle behavior, pending action request handling, evidence/audit behavior, or test scope is not clear. | Does not block internal governed helpers or existing S4-C lifecycle evidence. |
| `READY_FOR_SCOPED_IMPLEMENTATION_TICKET` | A later implementation ticket may be drafted because all decision boundaries are clear. | Use only when eligibility criteria are satisfied and no S4-C/S5-C boundary ambiguity remains. | Does not implement the endpoint and does not authorize implementation by itself. |
| `HOLD` | Endpoint decision cannot safely proceed even as planning. | Use if the decision would weaken S4-C/S5-C guarantees, imply external pilot authorization, require real external access, introduce RBAC/ticketing/workflow-engine/destructive automation, or bypass action-request semantics. | Does not mean the endpoint is rejected forever; it means the current decision needs product/governance repair first. |

## Endpoint Eligibility Criteria

Before any later implementation ticket may be drafted, all criteria below must be satisfied.

| Criterion | Required condition | HOLD trigger |
| --- | --- | --- |
| Product need | Product need for a public close-case endpoint is explicit. | Endpoint is opened because it is convenient rather than governed by product need. |
| Actor model | Actor is descriptive and pilot-local, not enterprise RBAC. | Actor wording creates permission infrastructure or multi-tenant authorization assumptions. |
| Close reason alignment | Close reason handling aligns with S5-C-2. | Endpoint invents new close reasons, changes lifecycle vocabulary, or treats oral-only reasons as sufficient. |
| Action-request alignment | Action-request approval/denial handling aligns with S5-C-3. | Endpoint bypasses approval, denial, cancellation, or non-destructive action-request semantics. |
| Pending action requests | Pending action request behavior is explicitly decided or deferred. | Endpoint proceeds while pending action request behavior remains ambiguous. |
| Audit behavior | Audit entry behavior is append-safe and replayable. | Close mutates or erases audit history, evidence, or prior request records. |
| Closed-case safety | Closed-case safety is preserved. | Endpoint weakens closed-case protections or permits unsafe post-close mutation. |
| Implementation shape | Exact method, path, request, response, error model, and test plan are deferred to a later implementation ticket. | S5-C-4 freezes runtime/API behavior or test expectations directly. |
| External access | No real external system access is required. | Endpoint requires SIEM, EDR, source-system, ticketing, or workflow-engine connectivity. |
| Pilot/sign-off boundary | No external pilot or real sign-off is implied. | Endpoint decision is treated as external pilot authorization or real customer/operator sign-off. |

## Close-Case Semantics If Later Implemented
Any future endpoint must:
- close an existing governed case non-destructively
- preserve original investigation evidence
- preserve action requests
- preserve lifecycle audit history
- record close reason using the S5-C-2 taxonomy if close reason is included
- avoid secret values and unredacted customer/operator payloads
- not execute destructive response
- not call external SIEM/EDR/source systems
- not create external tickets
- not route through a workflow engine
- not change action-request approval/denial semantics

This document does not freeze exact HTTP method, path, payload, response body, or error model. Those belong to a later governed implementation ticket if `READY_FOR_SCOPED_IMPLEMENTATION_TICKET` is selected.

## Pending Action Request Boundary
S5-C-4 must not bypass S5-C-3.

If a case has pending action requests, the endpoint decision must either:
- require the later implementation ticket to define safe behavior for pending action requests, or
- keep the endpoint deferred until pending action request behavior is decided.

S5-C-4 does not invent runtime behavior for pending requests. It only records that pending action request handling must be explicit before endpoint implementation can be scoped.

## Audit / Evidence Requirements

Allowed evidence may include:
- case identifier if non-sensitive
- `lifecycle_status`
- close reason name from S5-C-2 taxonomy
- actor identity if non-sensitive
- timestamp or run context if available
- audit entry reference if available
- implementation-ticket reference if later created

Prohibited evidence:
- secret values
- raw credentials
- auth headers
- cookies
- bearer tokens
- API keys
- unredacted customer/operator payloads
- raw external SIEM/EDR/source payloads

Any later close-case endpoint evidence must remain redacted, append-safe, and replayable without depending on oral knowledge.

## Authorization And External Boundary
- S5-C-4 does not authorize external pilot execution.
- S5-C-4 does not create real customer/operator sign-off.
- S5-C-4 does not authorize real SIEM/EDR/source-system access.
- Descriptive actors do not create enterprise RBAC.
- Any future endpoint auth/authz design is a separate implementation/product decision.

## HOLD Conditions
HOLD if any condition below appears.

| Condition | Why it holds |
| --- | --- |
| S5-C-4 is treated as endpoint implementation authorization. | S5-C-4 is a decision document only. |
| Public close-case API is opened directly. | Runtime/API behavior requires a later governed implementation ticket. |
| Durable lifecycle states are changed. | S5-C-4 must preserve S4-C and S5-C-2 lifecycle semantics. |
| Close deletes evidence or audit history. | Violates durable case and append-safe audit guarantees. |
| Close implies destructive response execution. | Violates non-destructive action semantics. |
| Action-request approval/denial semantics are bypassed. | S5-C-3 owns action-request decision semantics. |
| Pending action request behavior is ambiguous but endpoint proceeds. | Endpoint behavior would be unsafe without explicit pending-request handling. |
| Closed-case safety is weakened. | Reopens accepted S4-C closed-case protections. |
| RBAC, ticketing integration, workflow-engine behavior, or destructive automation appears. | Expands beyond S5-C-4 decision scope. |
| Real SIEM/EDR/source-system access is required. | Violates external-system boundary. |
| Real customer/operator sign-off is required. | Violates no real sign-off boundary. |
| External pilot execution is implied. | External pilot remains unauthorized. |
| Runtime/API/test/schema behavior is changed without later governed implementation ticket. | Bypasses required implementation governance. |

## Handoff To Later Tickets
- `S5-C-5` owns case workflow review pass.
- If `READY_FOR_SCOPED_IMPLEMENTATION_TICKET` is selected, the later implementation ticket must name exact files, behavior changes, acceptance criteria, and test plan.
- A later implementation ticket must explicitly define method, path, request body, response body, error model, audit behavior, pending action request behavior, and tests.
- S5-C-4 alone does not authorize implementation.

## Preliminary Decision
Decision: `KEEP_DEFERRED`.

Rationale:
- The public close-case HTTP endpoint remains deferred in the accepted S4-C baseline.
- S5-C-2 and S5-C-3 now clarify close reason, lifecycle, and action-request semantics, but S5-C-4 does not yet have an explicit product need, endpoint actor authority, pending action request behavior, or implementation test scope.
- Planning can continue safely because the endpoint remains deferred and no `HOLD` condition blocks documenting the decision.

If a later product/governance decision provides all eligibility criteria, S5-C-4 may be revisited or followed by a scoped implementation ticket. No implementation starts from this document alone.

## Acceptance Criteria
S5-C-4 is acceptable when:
- decision options are explicit and non-overlapping
- S4-C guarantees are preserved
- S5-C-2 close reason/lifecycle semantics are preserved
- S5-C-3 action request approval/denial semantics are preserved
- no endpoint is implemented or authorized directly
- public endpoint implementation requires a later governed ticket
- external pilot and real sign-off remain unauthorized
- runtime/API/test/schema changes remain out of scope
