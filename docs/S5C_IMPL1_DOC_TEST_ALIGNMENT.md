# S5-C-IMPL-1 Doc/Test Alignment Only

## Document Control
- Title: S5-C-IMPL-1 Doc/Test Alignment Only
- Baseline: `S5-C-DECISION-2026-04-14-001`
- Source of truth: `D:\产品设计\New folder`
- Scope: S5-C implementation preparation / doc-test alignment only
- Status: Draft for review
- Owner: Human-governed Sprint 5 planning

## Goal
Map S5-C planning/contract artifacts to future test-hardening work without changing runtime behavior, API behavior, schema, or tests.

This document does not modify tests. It does not authorize runtime/API/schema behavior changes. It only prepares alignment for a later scoped test-hardening ticket.

## Non-Goals
- implementation
- code changes
- test changes
- runtime/API/schema behavior changes
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
- adding runtime/build dependencies

## Current Baseline
- Current governed snapshot is `S5-C-DECISION-2026-04-14-001`.
- `docs/S5C_IMPLEMENTATION_DECISION_CHECKPOINT.md` selected `S5-C-IMPL-1_DOC_TEST_ALIGNMENT_ONLY`.
- S5-C-IMPL-1 does not authorize implementation.
- S5-C-4 public close-case endpoint remains `KEEP_DEFERRED`.
- Future test or implementation changes require a later governed scoped ticket.

## Alignment Inputs
- `docs/S5C_IMPLEMENTATION_DECISION_CHECKPOINT.md`
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
- `backend/tests/test_persistent_case_contract.py`
- `backend/tests/test_case_action_request_contract.py`
- `backend/tests/test_case_lifecycle_regression.py`
- `backend/tests/test_case_store.py`
- `backend/tests/test_runtime_service.py`
- `backend/tests/test_case_view.py`
- `docs/HANDOFF.md`
- `releases/release_manifest.json`
- `releases/verify_report.json`

## Existing Coverage Inventory

Inventory method: read-only search using `rg` for `PersistentCaseRecord`, `action_request`, `approve`, `reject`, `cancel`, `closed`, `lifecycle_status`, `lifecycle_audit`, and `case_view`, plus read-only review of the relevant test files listed above. No tests were edited.

| Existing file | Relevant coverage area | Current governed behavior it appears to cover | Potential future alignment need | Notes / assumptions |
| --- | --- | --- | --- | --- |
| `backend/tests/test_persistent_case_contract.py` | Persistent case schema, lifecycle transition matrix, initial audit, `case_view`, and action-request seed. | Initial `PersistentCaseRecord` starts `open`, preserves `case_view`, keeps `action_requests[]` first-class, records `case_created`, freezes status transitions, and treats action-request seeds as non-destructive. | If later S5-C tickets add doc-only close reason checks or additional status wording tests, align them without changing persisted lifecycle states. | Coverage is contract-level and currently protects S4-C schema/lifecycle basics. |
| `backend/tests/test_case_action_request_contract.py` | Action request create / submit / approve / reject / cancel behavior and closed-case safety. | Approval is auditable, rejection and cancellation follow frozen transitions, degraded cases suppress action-request creation, and closed cases block reject/cancel updates. | Later test-hardening may add explicit separation assertions for `action_request_status` versus `case.lifecycle_status` wording if scoped. | Existing tests already cover core S4-C/S5-C-3 behavior signals. |
| `backend/tests/test_case_lifecycle_regression.py` | Runtime-service lifecycle regression through create, retrieve, review, approve, close, and post-close retrieval stability. | Deterministic audit chain includes create, action request, submit, approve, and close events; retrieving closed cases preserves schema and does not mutate stored payloads. | Later scoped ticket may expand closed-case safety regression coverage without opening public close-case endpoint. | Current close path uses governed helper/storage behavior, not a public close-case HTTP endpoint. |
| `backend/tests/test_case_store.py` | SQLite case store round-trip, immutable-style helper behavior, action request IDs, transition ownership, serializer shape. | Store round-trips without mutating stored case data, helpers return new record versions, `in_review` transition requires owner, and serialized records expose stable lifecycle/case_view shape. | Later tests may align additional audit/evidence expectations if a scoped implementation ticket changes helper usage. | This is persistence and helper coverage, not S5-C role or endpoint behavior. |
| `backend/tests/test_runtime_service.py` | Runtime create/get case paths and runtime action-request round trip. | `create_case_sync()` persists/retrieves a case, action request create/submit/approve round trip records statuses and audit, degraded cases block action-request creation, and pilot smoke creates an `open` persistent case. | Later scoped ticket may add targeted runtime-service tests only if exact behavior changes are explicitly authorized. | No public close-case HTTP endpoint implementation is inferred from this coverage. |
| `backend/tests/test_case_view.py` | Analyst-facing `case_view` projection and degraded recommended-action behavior. | `case_view` shape remains stable, recommended action availability is derived, and degraded cases disable unsafe recommended actions. | Later S5-C work may reference this as analyst-review evidence, but journey roles/stages should remain doc-level unless a scoped UI/runtime ticket exists. | This is case-view projection coverage, not durable lifecycle transition coverage. |

## S5-C Contract To Test Mapping

| Contract artifact | Contract guarantee | Existing coverage signal | Future test-hardening candidate | Boundary |
| --- | --- | --- | --- | --- |
| S5-C-1 journey roles/stages | Pilot-local roles are descriptive only; journey stages preserve S4-C durable lifecycle, audit, and non-destructive action-request semantics. | Indirect signals in `test_case_view.py`, `test_runtime_service.py`, and lifecycle/action-request tests show readable case detail, persistent case creation, action-request review flow, and audit evidence. | Doc/test-plan alignment may define which existing tests support each journey stage before any new test is proposed. | Do not create RBAC, authorization infrastructure, ticketing, workflow engine, UI behavior, or runtime role behavior from this mapping. |
| S5-C-2 close reason/lifecycle semantics | Close reason taxonomy is bounded; lifecycle vocabulary remains S4-C-compatible; no new persisted lifecycle states are introduced. | `test_persistent_case_contract.py`, `test_case_lifecycle_regression.py`, and `test_case_store.py` cover existing lifecycle statuses, transitions, close audit behavior, and post-close retrieval stability. | Future scoped tests may assert no new persisted lifecycle states or validate close reason documentation-to-test expectations if a later ticket defines exact tests. | Close reason taxonomy remains planning/contract language until a governed implementation ticket changes schema, API, or tests. |
| S5-C-3 action request approval/denial/cancellation semantics | Approval is non-destructive; denial/rejection preserves evidence; cancellation/withdrawal preserves history; `action_request_status` remains separate from `case.lifecycle_status`. | `test_case_action_request_contract.py` covers create/submit/approve/reject/cancel, audit entries, degraded-case suppression, and closed-case reject/cancel blocking; `test_runtime_service.py` covers runtime action-request round trip. | Later scoped tests may add explicit separation checks for action-request status versus case lifecycle status, and harden rejection/cancellation audit assertions. | Do not redefine statuses, destructive execution, or lifecycle meaning through tests. |
| S5-C-4 public close-case endpoint `KEEP_DEFERRED` | Public close-case HTTP endpoint remains deferred and is not implemented or authorized. | `test_case_lifecycle_regression.py` closes through governed helper/storage behavior; no public endpoint expectation is required by current S5-C docs. | Future scoped tests may assert no endpoint expectations are introduced only if a later ticket explicitly chooses that style of guard. | Do not open endpoint, freeze method/path/payload/error model, or infer endpoint behavior from this doc. |
| S5-C-5 `PASS` and future implementation gate | S5-C is accepted as a planning/contract baseline only; later implementation requires exact files, behavior changes, acceptance criteria, test plan, audit/evidence behavior, redaction checks, hold/rollback criteria, and review ownership. | Current manifest and verify report include governed S5-C documents and passing canonical tests. | Future ticket checklist can require test-command naming and owner/reviewer fields before any code or test change starts. | PASS does not authorize implementation, external pilot, real sign-off, real external access, or public endpoint work. |

## Future Test-Hardening Candidates

| Candidate | Possible future scope | Required later ticket |
| --- | --- | --- |
| Action request approval/rejection/cancellation regression hardening | Add or refine targeted tests around existing action-request decision states and audit evidence. | Later scoped test-hardening ticket must name exact tests, expected current behavior, and semantic non-change boundary. |
| Closed-case safety regression expansion | Expand coverage that closed cases do not accept unsafe action-request updates or endpoint-like mutation. | Later scoped ticket must name exact closed-case safety behavior and confirm no public close-case endpoint opening. |
| `lifecycle_status` vs `action_request_status` separation checks | Add explicit assertions that action-request status does not redefine durable case lifecycle status. | Later scoped ticket must preserve S4-C/S5-C-2/S5-C-3 semantics and avoid new persisted states. |
| Audit append/replay checks | Harden audit chain checks for action request and close flows where current behavior already exists. | Later scoped ticket must define audit/evidence behavior and redaction/secret handling expectations. |
| Public close-case endpoint remains deferred / no endpoint expectations | Record or test that no public endpoint behavior is assumed unless later authorized. | Later scoped ticket must avoid freezing method/path/payload/error model unless endpoint work is separately governed. |
| Doc-only acceptance checklist for future implementation tickets | Create a checklist mapping S5-C future ticket requirements to exact files, tests, and review ownership. | Later doc/test ticket must remain no-runtime-change unless explicitly expanded by governance. |

These candidates are observations, not accepted work items. Each requires a later scoped ticket before any test or implementation change.

## No-Runtime-Change Boundary
- This document does not change runtime behavior.
- This document does not change API behavior.
- This document does not change schema.
- This document does not change tests.
- Existing test gaps are observations only, not failures unless a later ticket accepts them.
- Future scoped tickets must explicitly decide whether tests are changed.

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This document modifies code or tests. | S5-C-IMPL-1 is documentation/test-plan alignment only. |
| Runtime/API/schema behavior changes. | Behavior changes require a later governed scoped ticket. |
| Public close-case endpoint implementation is implied. | S5-C-4 remains `KEEP_DEFERRED`. |
| Action request semantics are redefined. | S5-C-3 owns action-request semantics. |
| Lifecycle semantics are redefined. | S5-C-2 and S4-C own lifecycle semantics. |
| S4-C guarantees are weakened. | Durable case record, audit, non-destructive action requests, and closed-case safety remain inherited guarantees. |
| External pilot execution is implied. | External pilot remains unauthorized. |
| Real customer/operator sign-off is required. | S5-C docs do not create real sign-off. |
| Real SIEM/EDR/source-system access is required. | S5-C alignment remains repo-local and does not require real external access. |
| RBAC, ticketing integration, workflow-engine behavior, or destructive response scope appears. | These remain out of scope for S5-C alignment. |
| New runtime/build dependency is introduced. | Dependency changes are outside this doc/test alignment scope. |

## Future Ticket Requirements

Any later test-hardening or implementation ticket must define:

| Requirement | Required detail |
| --- | --- |
| `primary_implementor` | Name who performs the work. |
| `reviewer` | Name who reviews the delta. |
| `reviewer_when_cc_implements` | Required if Claude Code is primary implementor. |
| Exact files | Name every doc, test, code, API, or schema file in scope. |
| Exact behavior changes | State whether behavior changes are absent, test-only, or implementation-impacting. |
| Exact tests to add or modify | Name each test file and intended assertion before edits begin. |
| Acceptance criteria | Define verifiable pass conditions. |
| Test command | Name the exact command required for validation. |
| Audit/evidence behavior | Required if lifecycle or action-request audit behavior is relevant. |
| Redaction/secret handling check | Confirm no secret values, auth material, raw credentials, or unredacted customer/operator payloads are required. |
| Hold/rollback criteria | Define when to stop, hold, or revert scope. |
| External review requirement | State whether external review is required before governance closeout. |

## Preliminary Decision
Decision: `READY_FOR_SCOPED_TEST_HARDENING_TICKET`.

Meaning:
- S5-C-IMPL-1 is acceptable as a doc/test alignment baseline.
- It may be followed by a later scoped test-hardening ticket.

Non-meaning:
- It does not authorize test changes.
- It does not authorize code changes.
- It does not authorize runtime/API/schema changes.
- It does not authorize public endpoint implementation.
- It does not authorize external pilot execution.
- It does not authorize real customer/operator sign-off.

## Acceptance Criteria
S5-C-IMPL-1 is acceptable when:
- baseline is `S5-C-DECISION-2026-04-14-001`
- existing relevant coverage is inventoried read-only
- S5-C contracts are mapped to future test-hardening areas
- no code/test/runtime/API/schema changes are made or authorized
- public close-case endpoint remains `KEEP_DEFERRED`
- future scoped test-hardening ticket requirements are explicit
- external pilot and real sign-off remain unauthorized
