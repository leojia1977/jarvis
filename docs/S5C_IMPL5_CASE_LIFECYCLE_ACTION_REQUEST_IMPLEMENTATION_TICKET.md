# S5-C-IMPL-5 Case Lifecycle and Action Request Implementation Ticket

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S5-C-IMPL-5 Case Lifecycle and Action Request Implementation Ticket |
| Status | Closed as governed S5-C-IMPL-5 implementation-ticket definition baseline |
| Scope | docs-only implementation-ticket definition for first allowed S5-C case lifecycle and action-request semantics implementation ticket |
| Baseline | S5C-SCOPED-IMPLEMENTATION-DECISION-2026-04-16-001 |
| Predecessor artifacts | docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md; docs/S5C_SCOPED_IMPLEMENTATION_DECISION_PREP.md; docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md; docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md; docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md |
| Route | OPEN_FIRST_ALLOWED_S5_C_IMPLEMENTATION_TICKET_FOR_CASE_LIFECYCLE_AND_ACTION_REQUEST_SEMANTICS |
| primary_implementor | VS Code |
| reviewer | Claude Code |
| reviewer_when_cc_implements | not applicable |
| requires_external_review | true |

`requires_external_review` is true because this ticket defines a future implementation scope over governed S5-C case lifecycle semantics, action-request approval/denial/cancellation semantics, audit history, and closed-case safety. Even though this draft does not implement code, it scopes future runtime/test behavior and engages AI_COLLAB triggers around case lifecycle semantics, action-request semantics, evidence/audit handling, and future runtime/test planning. External review does not authorize implementation and does not replace human go/no-go.

## 2. Goal

This document drafts a governed docs-only implementation-ticket definition for the first allowed S5-C implementation ticket.

The goal is to define the exact later implementation ticket boundary for case lifecycle and action-request semantics without modifying code or tests in this draft.

This draft must not implement anything.

This document answers:

- Which governed clauses are in scope for a later implementation ticket.
- Which candidate files may be modified later.
- Which behaviors may be implemented or tested later.
- Which tests must be added or modified later.
- Which areas remain HOLD.
- What must remain unauthorized.
- What must be true before actual implementation begins.

## 3. Baseline Summary

- Sprint 5 milestone verdict remains `SPRINT5_BASELINE_REVIEW_PASS_WITH_EXTERNAL_INPUTS_PENDING`.
- The External Input Tracker is governed and does not make any input `READY`.
- S5-C Scoped Implementation Decision Prep is governed.
- S5-C Scoped Implementation Decision is governed.
- The S5-C decision recommendation is `PRELIMINARY_RECOMMENDATION_OPEN_FIRST_ALLOWED_S5_C_IMPLEMENTATION_TICKET_FOR_CASE_LIFECYCLE_AND_ACTION_REQUEST_SEMANTICS`.
- This draft opens only the implementation-ticket definition for that recommendation.
- This draft does not implement.
- S5-A external pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- Real customer/operator sign-off remains unauthorized.
- S5-B remains `PASS_AND_PARK`.
- S5-D remains `PASS_AND_PARK`.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- AI_COLLAB operating model and contract are not changed.

## 4. S5-C-3 Status Correction

- docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md file header may still say `Status: Draft for review`.
- HANDOFF, manifest, and later S5-C / Sprint 5 governance records are the controlling evidence that S5-C-3 is a governed contract/planning artifact.
- Treat the header mismatch as documentation hygiene only, not an unmet precondition.
- This draft does not modify S5-C-3.
- S5-C-3 alone does not authorize implementation.

## 5. Implementation-Ticket Status Vocabulary

Allowed future ticket status / bucket values:

- `FUTURE_IMPLEMENTATION_CANDIDATE`
- `FUTURE_TEST_SCOPE_CANDIDATE`
- `HOLD_PUBLIC_ENDPOINT`
- `HOLD_EXTERNAL_INPUT`
- `HOLD_POLICY_OR_EXTERNAL_REVIEW`
- `HOLD_OUT_OF_SCOPE`
- `NOT_APPLICABLE`

Forbidden values:

- `READY`
- `APPROVED`
- `IMPLEMENTABLE`
- `PILOT_READY`
- `PRODUCTION_READY`
- `AUTHORIZED_FOR_IMPLEMENTATION`
- `IMPLEMENT_NOW`
- `CODE_NOW`

The forbidden values above must not be used as status or bucket values.

## 6. Fixed Implementation-Ticket Risks

Any of the following is a HOLD trigger:

- Implementation-ticket definition being mistaken for implementation authorization.
- `FUTURE_IMPLEMENTATION_CANDIDATE` being mistaken for immediate code permission.
- Exact governed clauses being skipped or ambiguous.
- Exact files being skipped or ambiguous.
- Exact behavior changes being skipped or ambiguous.
- Exact tests/test commands being skipped or ambiguous.
- Acceptance criteria being skipped or ambiguous.
- Case lifecycle semantics changing beyond governed baselines.
- Action-request approval/denial/cancellation semantics changing beyond governed baselines.
- New persisted lifecycle/action-request statuses being introduced.
- Approval being mistaken for destructive execution.
- Approval being mistaken for real customer/operator sign-off.
- Denial/rejection deleting evidence or audit.
- Cancellation/withdrawal erasing prior request history.
- Audit/evidence behavior turning into evidence retention.
- Redaction/secret/evidence boundaries being frozen without review.
- Public close-case endpoint `KEEP_DEFERRED` being weakened.
- Pending action request close-case behavior opening endpoint work.
- Destructive response automation being introduced.
- RBAC / ticketing / workflow engine scope being introduced.
- Runtime/API/schema/test/dependency changes appearing in this draft.
- Fixture file creation or modification appearing.
- External pilot execution or readiness appearing.
- Real customer/operator sign-off appearing.
- Real SIEM/EDR/source/telemetry access appearing.
- Credentials/tokens/API keys/auth headers/cookies appearing.
- Raw logs/screenshots/exports/payloads/event bodies/customer evidence appearing.
- S5-B or S5-D reopen appearing.
- S4-A resolver order changing.
- AI_COLLAB operating model or contract changing.
- External review bypass or human go/no-go replacement.

## 7. Governed Clause Scope

| Governed clause | Governed source artifact(s) | Future ticket bucket | Clause scope | Later implementation may include | Later implementation must not include | Required tests / assertions | requires_external_review implication | HOLD triggers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Durable case lifecycle baseline | docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md; docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md | `FUTURE_IMPLEMENTATION_CANDIDATE` | Preserve already governed lifecycle baseline in a later exact ticket. | Case lifecycle persistence and transition guards within governed vocabulary. | New lifecycle states, public endpoint work, or lifecycle semantics beyond governed baselines. | Lifecycle transition regression tests and closed-case guard assertions. | Later ticket must set its own decision/rationale and likely requires external review. | New state, ambiguous transition, or direct implementation in this draft. |
| Case close reason / lifecycle semantics | docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md; docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md; docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md | `FUTURE_IMPLEMENTATION_CANDIDATE` | Keep close reason behavior within governed planning boundaries. | Internal close reason validation or persistence if later exact scope names it. | Public close-case endpoint implementation or new close semantics. | Close reason validation tests and endpoint deferral assertions. | Later ticket must preserve `KEEP_DEFERRED` and re-evaluate external review. | Endpoint work, broadened close semantics, or weakened `KEEP_DEFERRED`. |
| Action request approval semantics | docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md; docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md | `FUTURE_IMPLEMENTATION_CANDIDATE` | Approval is a governed non-destructive review decision. | Recording approval status, actor-neutral metadata, and audit entry if later scoped. | Destructive execution, response automation, or real customer/operator sign-off. | Approval transition tests and non-execution assertions. | Later ticket must re-evaluate external review because action semantics are in scope. | Approval treated as execution or sign-off. |
| Action request denial / rejection semantics | docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md; docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md | `FUTURE_IMPLEMENTATION_CANDIDATE` | Denial/rejection preserves request and decision history. | Recording denial/rejection state and append-safe audit trace if later scoped. | Evidence deletion, audit erasure, or new status vocabulary. | Denial/rejection persistence and audit-preservation assertions. | Later ticket must re-evaluate external review because action semantics are in scope. | Deletion, history loss, or new persisted status. |
| Action request cancellation / withdrawal semantics | docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md; docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md | `FUTURE_IMPLEMENTATION_CANDIDATE` | Cancellation/withdrawal preserves original request and prior history. | Recording cancellation/withdrawal as non-destructive lifecycle of the request if later scoped. | Erasing prior request data, inventing broader workflow, or response execution. | Cancellation/withdrawal audit and prior-history preservation tests. | Later ticket must re-evaluate external review because action semantics are in scope. | History erasure, broader workflow introduction, or automation. |
| Audit history / decision traceability | docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md; docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md; docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md | `FUTURE_IMPLEMENTATION_CANDIDATE` | Audit traceability is limited to governed lifecycle/action-request decisions. | Append-safe audit entries and deterministic replay checks if later scoped. | Raw evidence retention, customer/operator evidence handling, or evidence-pack behavior. | Audit append-only and replay/round-trip assertions. | Later ticket must re-evaluate external review because evidence/audit handling is adjacent. | Raw evidence retention, deletion of audit, or unclear evidence boundary. |
| Closed-case safety / immutability boundary | docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md; docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md | `FUTURE_IMPLEMENTATION_CANDIDATE` | Closed cases remain protected from unsafe mutation. | Guards preventing new or updated action requests on closed cases if later scoped. | Weakening closed-case protections or allowing unsafe post-close mutation. | Closed-case mutation rejection tests across store and runtime seams if later scoped. | Later ticket must re-evaluate external review because lifecycle safety is in scope. | Post-close mutation, ambiguous safety behavior, or endpoint coupling. |

## 8. Candidate Future File Scope

This draft must not modify the files below. It only lists candidate future scope for a later separate ticket.

| Candidate future file | Candidate role | Future ticket bucket | Later changes may include | Later changes must not include | Required test relationship | HOLD triggers |
| --- | --- | --- | --- | --- | --- | --- |
| `backend/app/tools/persistent_case.py` | Case/action-request model and persistence helpers if later exact scope requires it. | `FUTURE_IMPLEMENTATION_CANDIDATE` | Persist governed action-request status and append-safe lifecycle audit. | New public endpoint behavior, raw evidence storage, or new persisted status vocabulary. | Covered by action-request contract and case store round-trip tests. | New status, evidence retention, or implementation outside later ticket. |
| `backend/app/tools/case_store.py` | Case store transition and round-trip behavior if later exact scope requires it. | `FUTURE_IMPLEMENTATION_CANDIDATE` | Round-trip preservation of action requests and lifecycle audit. | Fixture creation, customer evidence retention, or endpoint coupling. | Covered by `backend/tests/test_case_store.py`. | Fixture changes, evidence retention, or skipped round-trip assertions. |
| `backend/app/runtime_service.py` | Runtime service validation seam if later exact scope requires it. | `FUTURE_IMPLEMENTATION_CANDIDATE` | Deterministic invalid-transition errors and closed-case safety guards. | Public close-case endpoint work or response automation. | Covered by runtime service tests for invalid transitions. | Endpoint work, automation, or ambiguous error behavior. |
| `backend/tests/test_case_action_request_contract.py` | Primary action-request semantics test file. | `FUTURE_TEST_SCOPE_CANDIDATE` | Approval, denial/rejection, cancellation/withdrawal, and non-destructive decision assertions. | Real external-system access, evidence retention, or fixture file creation. | Must map to governed S5-C clauses named by later ticket. | Missing clause mapping or forbidden evidence. |
| `backend/tests/test_case_lifecycle_regression.py` | Lifecycle regression and closed-case safety tests. | `FUTURE_TEST_SCOPE_CANDIDATE` | Lifecycle status separation and closed-case immutability assertions. | Public endpoint implementation tests unless later endpoint ticket opens it. | Must assert `KEEP_DEFERRED` remains outside scope. | Endpoint coupling or new lifecycle status. |
| `backend/tests/test_case_store.py` | Store-level round-trip and persistence tests. | `FUTURE_TEST_SCOPE_CANDIDATE` | Action request and lifecycle audit round-trip assertions. | Fixture file creation or raw evidence retention tests. | Must cover case store behavior if store files change. | Fixture changes or skipped persistence assertions. |
| `backend/tests/test_runtime_service.py` | Runtime service behavior tests. | `FUTURE_TEST_SCOPE_CANDIDATE` | Deterministic invalid action-request transition payload assertions if later scoped. | Public close-case endpoint work, live access, or response automation. | Must cover runtime seam if `runtime_service.py` changes. | Endpoint work, live access, or automation. |

## 9. Candidate Behavior Scope

| Future behavior candidate | Future ticket bucket | Later behavior may include | Later behavior must not include | Required tests/assertions | HOLD triggers |
| --- | --- | --- | --- | --- | --- |
| Preserve `action_request_status` separate from `case.lifecycle_status` | `FUTURE_IMPLEMENTATION_CANDIDATE` | Separate persisted fields and transition validation if later exact scope names it. | Merging action state into case lifecycle state or creating new lifecycle vocabulary. | Separation and transition regression assertions. | State merge or new persisted status. |
| Approval records non-destructive review decision only | `FUTURE_IMPLEMENTATION_CANDIDATE` | Approval status and audit trace. | Destructive execution, response automation, or real sign-off. | Approval is non-executing and auditable. | Execution or sign-off implication. |
| Denial/rejection preserves action request and audit history | `FUTURE_IMPLEMENTATION_CANDIDATE` | Denial/rejection status plus append-safe audit. | Evidence deletion or audit removal. | Denial/rejection preservation assertions. | Deletion or history loss. |
| Cancellation/withdrawal preserves original request and prior history | `FUTURE_IMPLEMENTATION_CANDIDATE` | Non-destructive cancellation/withdrawal trace. | Erasing original request or broader workflow engine behavior. | Prior-history preservation assertions. | Request erasure or workflow expansion. |
| Closed cases cannot accept new or updated action requests | `FUTURE_IMPLEMENTATION_CANDIDATE` | Store/runtime guards if later exact scope names both seams. | Weakening closed-case safety or opening public endpoint behavior. | Closed-case rejection assertions. | Post-close mutation or endpoint work. |
| Lifecycle audit remains append-safe and replayable | `FUTURE_IMPLEMENTATION_CANDIDATE` | Append-only audit entries and deterministic replay checks. | Raw evidence retention or evidence-pack behavior. | Append-safety and replay/round-trip assertions. | Evidence retention or audit deletion. |
| Case close reason / lifecycle semantics remain within governed vocabulary | `FUTURE_IMPLEMENTATION_CANDIDATE` | Existing governed close reason validation if later exact scope names it. | New close reason vocabulary or public endpoint implementation. | Close reason vocabulary and endpoint deferral assertions. | New semantics or weakened `KEEP_DEFERRED`. |
| Runtime service error payloads for invalid action request transitions remain deterministic if later scoped | `FUTURE_TEST_SCOPE_CANDIDATE` | Stable error code/message shape if exact future ticket names runtime seam. | API schema freeze beyond the scoped ticket or external access behavior. | Invalid-transition payload assertions. | Schema expansion or live access. |
| Case store round-trip preserves action requests and lifecycle audit | `FUTURE_TEST_SCOPE_CANDIDATE` | Round-trip tests for governed action request and audit data. | Fixture file creation or raw customer evidence. | Store round-trip assertions. | Fixture creation or evidence handling. |

## 10. HOLD / Out-Of-Scope Matrix

| Area | Bucket | Why it remains HOLD | Non-authorization note |
| --- | --- | --- | --- |
| Public close-case HTTP endpoint | `HOLD_PUBLIC_ENDPOINT` | The endpoint remains `KEEP_DEFERRED`. | No endpoint implementation is authorized. |
| Pending action request behavior around close-case endpoint | `HOLD_PUBLIC_ENDPOINT` | Endpoint-dependent behavior must not proceed while the endpoint is deferred. | No pending-close endpoint behavior is authorized. |
| Evidence/audit note retention | `HOLD_POLICY_OR_EXTERNAL_REVIEW` | Evidence retention and audit note retention need separate policy/external review. | No evidence retention, storage, replay, deletion, expiry, or evidence-pack behavior is authorized. |
| Redaction / secret handling boundary | `HOLD_POLICY_OR_EXTERNAL_REVIEW` | Redaction and secret handling must not be frozen here. | No redaction policy freeze or secrets implementation is authorized. |
| Destructive response automation | `HOLD_OUT_OF_SCOPE` | S5-C implementation scope is non-destructive case/action semantics only. | No response execution is authorized. |
| RBAC / ticketing / workflow engine integration | `HOLD_OUT_OF_SCOPE` | Integration scope requires a separate governed route. | No RBAC, ticketing, or workflow engine integration is authorized. |
| External pilot / customer evidence behavior | `HOLD_EXTERNAL_INPUT` | External pilot inputs remain `NOT_READY` / `UNKNOWN`. | No real customer/operator evidence is accepted. |
| S5-B reopen | `HOLD_OUT_OF_SCOPE` | S5-B remains `PASS_AND_PARK` unless explicitly reopened. | No source/input discovery reopen is authorized. |
| S5-D reopen | `HOLD_OUT_OF_SCOPE` | S5-D remains `PASS_AND_PARK` unless explicitly reopened. | No telemetry discovery reopen is authorized. |
| S4-A resolver behavior | `HOLD_OUT_OF_SCOPE` | S4-A authority and resolver order remain unchanged. | No resolver priority or authority change is authorized. |
| AI_COLLAB operating model or contract changes | `HOLD_OUT_OF_SCOPE` | AI_COLLAB files are not part of this route. | No operating model or contract change is authorized. |

## 11. Future Implementation Preconditions

Actual code/test implementation may begin only after a later ticket:

- Is separately drafted, reviewed, and closed.
- Names exact governed clauses.
- Names exact files.
- Names exact behavior changes.
- Names exact tests and test commands.
- Includes acceptance criteria.
- Preserves `KEEP_DEFERRED`.
- Prohibits external pilot execution/readiness/sign-off.
- Prohibits real external-system access, credentials, raw evidence, and evidence retention.
- Includes `requires_external_review` decision and rationale.
- Records human go/no-go.
- Assigns implementor/reviewer/reviewer_when_cc_implements.
- States rollback/HOLD criteria.

## 12. Non-Authorization

This draft does not authorize:

- Implementation now.
- Code changes.
- Test changes.
- Runtime/API/schema/dependency changes.
- Fixture file creation or modification.
- S5-C runtime work by itself.
- Public close-case endpoint work.
- Weakening `KEEP_DEFERRED`.
- Destructive response automation.
- RBAC / ticketing / workflow engine integration.
- New persisted lifecycle or action-request statuses.
- Case lifecycle semantic freeze beyond already governed baselines.
- Action request semantic freeze beyond already governed baselines.
- Evidence retention, storage, replay, deletion, expiry, or evidence-pack behavior.
- Redaction policy freeze.
- Secrets handling implementation.
- External pilot execution.
- External pilot readiness.
- Real customer/operator sign-off.
- Real SIEM/EDR/source/telemetry access.
- Credentials/tokens/API keys/auth headers/cookies/secret material.
- Raw logs/screenshots/exports/payloads/event bodies/customer/operator evidence.
- S5-B reopen.
- S5-D reopen.
- S4-A resolver priority or authority changes.
- AI_COLLAB operating model or contract changes.
- External review bypass.
- Human go/no-go replacement.
- Automatic implementation.

## 13. HOLD Conditions

This draft must HOLD if any of the following appears:

- Any code/test/runtime/API/schema/dependency edit appears.
- Fixture file creation or modification appears.
- Forbidden bucket/status vocabulary appears.
- Future implementation candidate is treated as immediate authorization.
- Exact clauses/files/behavior/tests are skipped.
- Public close-case endpoint `KEEP_DEFERRED` is weakened.
- Pending action request close-case behavior opens endpoint work.
- Destructive response automation appears.
- RBAC / ticketing / workflow engine integration appears.
- New persisted lifecycle/action-request statuses appear.
- External pilot execution/readiness/sign-off appears.
- Real external-system access appears.
- Credentials/tokens/API keys/auth headers/cookies/secret material appear.
- Raw evidence, logs, screenshots, exports, payloads, event bodies, or customer/operator evidence appear.
- Evidence retention/redaction/secrets boundary is frozen without external review.
- S5-B or S5-D reopen appears without explicit reopen decision.
- S4-A resolver priority changes.
- AI_COLLAB operating model or contract changes appear.
- External review is skipped or treated as replacing human go/no-go.
- HANDOFF or manifest is modified during draft-only stage.
- Protected untracked files are touched.

## 14. Preliminary Recommendation

`PRELIMINARY_RECOMMENDATION_READY_FOR_SEPARATE_S5_C_IMPL5_CODE_AND_TEST_TICKET`

Meaning:

- This document may be reviewed and, if accepted, closed as a governed implementation-ticket definition baseline.
- It permits a later separate S5-C-IMPL-5 code/test ticket to be drafted.
- That later ticket must be tightly scoped to case lifecycle and action-request semantics.
- That later ticket must still define exact clauses, files, behavior changes, tests, test commands, acceptance criteria, evidence/redaction/secret boundaries, rollback/HOLD criteria, external review decision, and human go/no-go.
- That later ticket may still HOLD if exact scope is not clean enough.

Non-meaning:

- It does not authorize implementation now.
- It does not authorize code/test/runtime/API/schema/dependency changes in this draft.
- It does not authorize public close-case endpoint work.
- It does not authorize external pilot execution or readiness.
- It does not authorize real customer/operator sign-off or real external-system access.
- It does not authorize evidence retention or redaction policy freeze.
- It does not reopen S5-B or S5-D.
- It does not change S4-A resolver order.
- It does not change AI_COLLAB.
- It does not create an automatic implementation ticket.

## 15. Acceptance Criteria

- Exactly one new docs-only file is created.
- `requires_external_review` is true with rationale.
- Baseline summary is accurate.
- S5-C-3 status correction is included and does not modify S5-C-3.
- Governed clause scope includes all required rows.
- Candidate future file scope includes all required rows.
- Candidate behavior scope includes all required rows.
- HOLD / out-of-scope matrix includes all required HOLD rows.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- No forbidden bucket/status vocabulary is used as a status or bucket value.
- Future implementation candidate means later ticket only, not immediate implementation.
- Future implementation preconditions are listed.
- No code/test/runtime/API/schema/dependency/fixture changes are made or authorized in this draft.
- No external pilot execution, sign-off, real access, credentials, raw evidence, or evidence retention is authorized.
- S5-B and S5-D remain `PASS_AND_PARK` unless later explicit reopen decision.
- S4-A resolver order remains unchanged.
- AI_COLLAB files are not modified.
- HANDOFF and manifest are not modified in this draft stage.
- Full gate is not run.
- No staging, commit, or push is performed.
