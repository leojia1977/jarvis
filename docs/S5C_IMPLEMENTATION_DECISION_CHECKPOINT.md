# S5-C Implementation Decision Checkpoint

## Document Control
- Title: S5-C Implementation Decision Checkpoint
- Baseline: `S5-C-2026-04-14-005`
- Source of truth: `D:\产品设计\New folder`
- Scope: S5-C post-review implementation decision routing
- Status: Draft for review
- Owner: Human-governed Sprint 5 planning

## Goal
Decide whether S5-C should proceed from planning/contract `PASS` into a later scoped implementation ticket, and if so which implementation path should be prepared first.

S5-C planning/contract stream is `PASS`. This checkpoint does not authorize implementation. It only selects or recommends the next route. Any implementation requires a later governed implementation ticket.

## Non-Goals
- implementation
- runtime/API/test/schema changes
- public close-case HTTP endpoint implementation
- changing S5-C-1 through S5-C-5 semantics
- changing S4-C guarantees
- external pilot execution
- real customer/operator sign-off
- real SIEM/EDR/source-system access
- enterprise RBAC
- ticketing integration
- workflow-engine behavior
- destructive response automation

## Current Baseline
- Current governed snapshot is `S5-C-2026-04-14-005`.
- `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` accepted S5-C as a governed planning/contract baseline.
- S5-C `PASS` does not authorize implementation.
- `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` selected `KEEP_DEFERRED` for the public close-case HTTP endpoint.
- Future implementation requires a separate governed implementation ticket.

## Decision Inputs
- `docs/S5C_CASE_WORKFLOW_HARDENING_PLAN.md`
- `docs/S5C1_CASE_WORKFLOW_JOURNEY_CONTRACT.md`
- `docs/S5C2_CLOSE_REASON_AND_LIFECYCLE_SEMANTICS.md`
- `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`
- `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`
- `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`
- `docs/S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md`
- `docs/S4C3_ACTION_REQUEST_AND_APPROVAL_CONTRACT.md`
- `docs/S4C4_CASE_LIFECYCLE_REGRESSION_TESTS.md`
- `docs/S4C5_PRODUCT_REVIEW_PASS.md`
- `docs/SPRINT5_PRD.md`
- `docs/SPRINT5_JIRA_BACKLOG.md`
- `docs/HANDOFF.md`
- `releases/release_manifest.json`
- `releases/verify_report.json`

## Candidate Path Matrix

| Candidate | Scope | Allowed in this checkpoint? | Required next step | Main risk | HOLD trigger |
| --- | --- | --- | --- | --- | --- |
| `S5-C-IMPL-1_DOC_TEST_ALIGNMENT_ONLY` | Documentation/test-plan alignment only; no runtime behavior change. | Allowed as a low-risk next route if product wants a bridge from planning to implementation. | A later scoped ticket defining exact docs/tests, acceptance criteria, and no-runtime-change boundary. | Test/document alignment is mistaken for runtime implementation authorization. | Any code/runtime/API/schema behavior change appears. |
| `S5-C-IMPL-2_ACTION_REQUEST_TEST_HARDENING` | Targeted test hardening around existing action request approval/denial/rejection/cancellation behavior. | Allowed only through a later scoped implementation/test ticket. | Ticket must name exact tests, existing behavior under test, acceptance criteria, and confirm no semantic change unless explicitly governed. | Tests accidentally redefine approval/denial/cancellation semantics. | Test expectations change S4-C/S5-C-3 semantics or imply destructive execution. |
| `S5-C-IMPL-3_CLOSED_CASE_SAFETY_REGRESSION_EXPANSION` | Targeted closed-case safety regression expansion. | Allowed only through a later scoped implementation/test ticket. | Ticket must name exact tests, closed-case safety behavior, acceptance criteria, and no public endpoint opening. | Regression expansion drifts into endpoint implementation or lifecycle transition change. | Public close-case HTTP endpoint opens, lifecycle states change, or closed-case safety is weakened. |
| `KEEP_PLANNING_ONLY` | No implementation now; retain S5-C as planning baseline. | Allowed if product need or implementation priority is unclear. | Record no implementation selected; choose another Sprint 5 stream or wait for product decision. | Planning `PASS` is later misread as hidden implementation approval. | Teams proceed to implementation without a scoped ticket. |
| `NEEDS_PRODUCT_DECISION` | Product/governance must choose before any implementation ticket is drafted. | Required if path choice affects product behavior, public API, external pilot assumptions, or Sprint 5 priorities. | Collect explicit product/governance decision. | Ambiguous priority causes implicit or convenience-driven implementation. | Implementation starts without explicit path selection. |

## Candidate Path Details

`S5-C-IMPL-1_DOC_TEST_ALIGNMENT_ONLY` permits a later scoped ticket to align documentation and test plans with the accepted S5-C planning contracts. It does not permit runtime behavior changes, API changes, schema changes, public endpoint implementation, or new test expectations that redefine S4-C/S5-C semantics.

`S5-C-IMPL-2_ACTION_REQUEST_TEST_HARDENING` permits a later scoped test ticket to harden coverage around existing action request approval, rejection, and cancellation behavior. It does not permit changing action-request status vocabulary, case lifecycle semantics, destructive execution boundaries, or external system behavior.

`S5-C-IMPL-3_CLOSED_CASE_SAFETY_REGRESSION_EXPANSION` permits a later scoped test ticket to expand closed-case safety regression coverage. It does not permit opening the public close-case HTTP endpoint, adding lifecycle states, weakening closed-case protections, or changing close semantics.

`KEEP_PLANNING_ONLY` permits retaining S5-C as a governed planning/contract baseline without selecting implementation. It does not permit teams to treat S5-C `PASS` as hidden authorization for code, runtime, API, test, or schema work.

`NEEDS_PRODUCT_DECISION` permits pausing until product/governance explicitly selects a route. It does not permit convenience-driven implementation while priority, product behavior, public API, external pilot assumptions, or Sprint 5 stream sequencing remain unclear.

## Recommendation
Recommended preliminary route: `S5-C-IMPL-1_DOC_TEST_ALIGNMENT_ONLY`.

This is the safest bridge from S5-C planning/contract `PASS` toward later scoped implementation because it can prepare exact docs/tests, acceptance criteria, and no-runtime-change boundaries before any behavior work starts.

Do not recommend public close-case HTTP endpoint implementation. `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` selected `KEEP_DEFERRED`, and any future endpoint work requires a separate governed implementation ticket.

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This checkpoint is treated as implementation authorization. | The checkpoint only selects a route. |
| Public close-case HTTP endpoint implementation is selected directly. | S5-C-4 selected `KEEP_DEFERRED`. |
| S5-C-1 through S5-C-5 semantics are changed. | Existing planning contracts must remain stable unless reopened by separate governance. |
| S4-C guarantees are weakened. | Durable lifecycle, audit, non-destructive action requests, and closed-case safety are inherited guarantees. |
| Runtime/API/test/schema behavior changes from this document alone. | Behavior changes require a later governed implementation ticket. |
| External pilot execution is implied. | External pilot remains unauthorized. |
| Real customer/operator sign-off is required. | S5-C does not create real sign-off. |
| Real SIEM/EDR/source-system access is required. | S5-C remains repo-governed and does not require real external access. |
| RBAC, ticketing integration, workflow-engine behavior, or destructive response automation appears. | These remain out of scope. |
| Future implementation ticket omits required scope controls. | Exact files, behavior changes, acceptance criteria, test plan, audit/evidence behavior, redaction/secret handling, hold/rollback criteria, and `reviewer_when_cc_implements` when needed must be explicit. |

## Future Ticket Requirements

Any later implementation ticket must define:

| Requirement | Required detail |
| --- | --- |
| `primary_implementor` | Name who performs the implementation work. |
| `reviewer` | Name who reviews the implementation delta. |
| `reviewer_when_cc_implements` | Required if Claude Code is primary implementor. |
| Exact files | Name every doc, code, API, test, or schema file in scope. |
| Exact behavior changes | State current behavior, proposed behavior, and non-goals. |
| Acceptance criteria | Define verifiable pass conditions. |
| Test plan | Define targeted tests or explain why none are required. |
| Audit/evidence behavior | Define audit entries, evidence retention, and replay expectations when relevant. |
| Redaction/secret handling check | Confirm no secret values or unredacted customer/operator payloads are required. |
| Pending action request behavior | Required if close-case endpoint or close workflow behavior is involved. |
| Hold/rollback criteria | Define when to stop, hold, or revert scope. |
| External review requirement | State whether external review is required before governance closeout. |

## Preliminary Decision
Decision: `S5-C-IMPL-1_DOC_TEST_ALIGNMENT_ONLY`.

This decision selects the next route only. It does not authorize implementation, runtime/API/test/schema changes, public close-case endpoint implementation, external pilot execution, real customer/operator sign-off, or real external system access.

The next step, if accepted, should be a later scoped ticket that names exact docs/tests, acceptance criteria, no-runtime-change boundaries, and review responsibilities.

## Acceptance Criteria
This checkpoint is acceptable when:
- current baseline is `S5-C-2026-04-14-005`
- S5-C `PASS` is correctly treated as a planning/contract baseline only
- all five candidate paths are evaluated
- public close-case endpoint remains `KEEP_DEFERRED`
- no implementation is authorized by this checkpoint
- external pilot and real sign-off remain unauthorized
- future implementation ticket requirements are explicit
- preliminary decision is one of `S5-C-IMPL-1_DOC_TEST_ALIGNMENT_ONLY`, `KEEP_PLANNING_ONLY`, or `NEEDS_PRODUCT_DECISION`
