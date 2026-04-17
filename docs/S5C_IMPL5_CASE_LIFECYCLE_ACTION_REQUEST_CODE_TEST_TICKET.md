# S5-C-IMPL-5 Case Lifecycle and Action Request Code/Test Ticket

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S5-C-IMPL-5 Case Lifecycle and Action Request Code/Test Ticket |
| Status | Closed as governed S5-C-IMPL-5 code/test implementation ticket baseline |
| Scope | docs-only code/test implementation ticket definition for later S5-C-IMPL-5 implementation |
| Snapshot candidate | S5C-IMPL5-CODE-TEST-TICKET-2026-04-17-001 |
| Stage candidate | s5c-impl5-code-test-ticket |
| Baseline snapshot | S5-POST-ORDIV-L1A-ROUTE-DECISION-2026-04-16-001 |
| Baseline stage | s5-post-ordiv-l1a-route-decision |
| Baseline commit | `51543ea9834f54216def4732245d8bba62955c7e` |
| Route | OPEN_S5_C_IMPL5_CODE_AND_TEST_IMPLEMENTATION_TICKET |
| Predecessor artifacts | `docs/S5_POST_ORDIV_L1A_ROUTE_DECISION.md`; `docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md`; `docs/S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_TICKET.md`; `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` |
| Codex role | planning, boundary definition, and prompt orchestration only |
| Draft creator | VS Code / human-supervised workspace |
| Reviewer | Claude Code review-only |
| Claude Web posture | Required before any later implementation human go/no-go |
| Human posture | Final go/no-go required before any implementation can begin |
| requires_external_review | true |

`requires_external_review` is true because this draft defines the future boundary for code/test work over governed S5-C case lifecycle semantics, action-request approval/denial/cancellation semantics, audit traceability, and closed-case safety. Even though this document is docs-only and non-authorizing, a later implementation attempt would touch lifecycle/action-request behavior and must pass Claude Web external review before human go/no-go. External review does not authorize implementation and does not replace human go/no-go.

## 2. Goal

Define the exact future code/test implementation ticket boundary for S5-C-IMPL-5 case lifecycle and action-request semantics, without authorizing implementation now.

This draft answers:

- Which exact governed S5-C clauses are in scope for a later implementation attempt.
- Which candidate implementation files may be modified later.
- Which candidate test files may be modified later.
- Which exact behavior deltas are candidates.
- Which areas remain HOLD or out of scope.
- Which tests and test commands must be required later.
- Which acceptance criteria must be met.
- Which rollback / HOLD criteria apply.
- Why `requires_external_review=true`.
- What must be true before implementation begins.

## 3. Baseline Summary

- Current HEAD is `51543ea9834f54216def4732245d8bba62955c7e`.
- Current governed snapshot is `S5-POST-ORDIV-L1A-ROUTE-DECISION-2026-04-16-001`.
- Current stage is `s5-post-ordiv-l1a-route-decision`.
- Manifest verification overall status is `PASS`.
- ORDIV-L1A remains parked at `PARK_LOCAL_VALIDATION_NO_REPORT`.
- No ORDIV-L1A validation metrics, row counts, distributions, workbook details, filenames, paths, sheet names, raw values, success rates, report artifacts, or further real-data work are authorized by this draft.
- S5-B remains `PASS_AND_PARK`.
- S5-D remains `PASS_AND_PARK`.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- External pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- AI_COLLAB operating model and contract remain unchanged.
- This draft does not change any governed S5-C, S5-B, S5-D, S4-A, ORDIV-L1A, or AI_COLLAB baseline.

## 4. Role Boundary

- Codex may plan, define boundaries, and orchestrate prompts only for this draft.
- VS Code / human-supervised workspace is the draft creator.
- Claude Code is review-only for this draft.
- Claude Web is required before any later implementation human go/no-go because implementation would touch case lifecycle semantics, action-request approval/denial/cancellation semantics, audit traceability, and closed-case safety.
- Human product/governance must give explicit final go/no-go before any later implementation can begin.
- If Claude Code becomes primary implementor in any later route, the later ticket must assign `reviewer_when_cc_implements` before code/test work starts.

## 5. Governed Clause Scope

| Governed S5-C clause | Source artifact(s) | Later implementation may include | Later implementation must not include | Required confirmation before implementation | HOLD triggers |
| --- | --- | --- | --- | --- | --- |
| Durable case lifecycle baseline | `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; `docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md`; `docs/S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_TICKET.md` | Internal model/store guards that preserve governed lifecycle behavior. | New persisted lifecycle statuses, broad lifecycle rewrite, public endpoint behavior, or external pilot behavior. | Exact lifecycle clause, exact file paths, exact tests, rollback/HOLD criteria, Claude Web review, and human go/no-go. | New lifecycle vocabulary, weakened closed-case safety, or ambiguous behavior delta. |
| Case close reason / lifecycle semantics | `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; `docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md` | Validation or persistence behavior within already governed close reason/lifecycle vocabulary. | Public close-case endpoint work, new close reason vocabulary, API/schema freeze, or semantic expansion. | Exact close reason/lifecycle clause, exact behavior delta, endpoint deferral assertion, tests, Claude Web review, and human go/no-go. | `KEEP_DEFERRED` weakened, endpoint scope appears, or new close semantics appear. |
| Action request approval semantics | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; `docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md` | Non-destructive approval decision recording and append-safe audit trace if exact scope names it. | Destructive execution, response automation, real customer/operator sign-off, RBAC/ticketing/workflow integration, or external-system action. | Exact approval clause, exact files/tests, non-execution assertion, Claude Web review, and human go/no-go. | Approval triggers execution, approval implies real sign-off, or external action appears. |
| Action request denial / rejection semantics | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; `docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md` | Non-destructive denial/rejection decision recording and history preservation if exact scope names it. | Evidence deletion, request history deletion, audit history deletion, new status vocabulary, or destructive behavior. | Exact denial/rejection clause, preservation assertions, tests, Claude Web review, and human go/no-go. | Deletion, audit erasure, new status vocabulary, or ambiguous rejection semantics. |
| Action request cancellation / withdrawal semantics | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; `docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md` | Cancellation/withdrawal trace that preserves the original request and prior history if exact scope names it. | Erasing original request, erasing prior history, broader workflow engine behavior, or response execution. | Exact cancellation/withdrawal clause, prior-history assertions, tests, Claude Web review, and human go/no-go. | Request/history erasure, workflow expansion, or automation. |
| Audit history / decision traceability | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; `docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md` | Append-safe, replayable lifecycle/action-request decision traceability using non-sensitive governance data. | Evidence retention, raw evidence handling, customer/operator evidence, mutable audit, or evidence-pack behavior. | Exact audit clause, append-safety expectations, non-retention boundary, tests, Claude Web review, and human go/no-go. | Raw evidence appears, audit mutability appears, or retention/storage/replay/deletion/expiry is implied. |
| Closed-case safety / immutability boundary | `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; `docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md` | Guards preventing new or updated action requests on closed cases if exact scope names relevant seams. | Unsafe post-close mutation, weakened closed-case protections, endpoint implementation, or new lifecycle states. | Exact closed-case safety clause, exact failure behavior, tests, rollback/HOLD criteria, Claude Web review, and human go/no-go. | Post-close mutation, endpoint coupling, lifecycle state expansion, or ambiguous failure behavior. |

## 6. Candidate File Scope

This draft must not modify the files below. It only defines the narrow file set that a later separate implementation ticket may evaluate.

| File | Candidate role | Later change may include | Later change must not include | Required test relationship | HOLD triggers |
| --- | --- | --- | --- | --- | --- |
| `backend/app/tools/persistent_case.py` | Candidate implementation file for case/action-request model fields, validation helpers, and append-safe audit structures. | Preservation of separate `action_request_status` and case `lifecycle_status`, governed action-request decision state handling, and closed-case safety helpers if exact scope names them. | New persisted lifecycle statuses, new persisted action-request statuses unless already governed and exact, evidence retention, public endpoint behavior, secrets handling, or broad model rewrite. | Must be covered by `backend/tests/test_case_action_request_contract.py`, `backend/tests/test_case_lifecycle_regression.py`, and `backend/tests/test_case_store.py` if changed. | New status vocabulary, evidence behavior, ambiguous persistence shape, skipped round-trip tests, or unreviewed semantic freeze. |
| `backend/app/tools/case_store.py` | Candidate implementation file for store-level transition and round-trip behavior. | Round-trip preservation of action requests, lifecycle/action-request audit entries, and closed-case mutation guards if exact scope names store behavior. | Fixture creation, real evidence retention, customer/operator evidence, endpoint coupling, dependency changes, or broad store backend changes. | Must be covered by `backend/tests/test_case_store.py` plus lifecycle/action-request tests if changed. | Fixture changes, raw evidence handling, skipped persistence assertions, endpoint coupling, or backend expansion. |
| `backend/app/runtime_service.py` | Candidate implementation file for runtime validation seam and deterministic invalid-transition behavior only if exact scope names runtime behavior. | Deterministic invalid action-request transition payloads and closed-case safety checks if exact scope names the runtime seam. | New public API endpoints, public close-case endpoint work, runtime API/schema contract expansion, response automation, live external-system access, or config integration. | Must be covered by `backend/tests/test_runtime_service.py` plus action-request/lifecycle tests if changed. | API/schema expansion, endpoint work, external access, response automation, ambiguous error payloads, or runtime integration creep. |
| `backend/tests/test_case_action_request_contract.py` | Candidate test file for action-request approval, denial/rejection, cancellation/withdrawal, and non-destructive decision semantics. | Synthetic-only assertions for governed action-request transitions, history preservation, non-execution, and audit traceability. | Real external-system access, raw evidence, fixtures, destructive execution tests, or real sign-off assertions. | Must map every new assertion to exact S5-C governed clauses. | Missing clause mapping, real data/evidence, fixture creation, or implementation authorization wording. |
| `backend/tests/test_case_lifecycle_regression.py` | Candidate test file for lifecycle regression and closed-case safety. | Synthetic-only tests for lifecycle/action-request separation, closed-case immutability, and `KEEP_DEFERRED` preservation. | Public close-case endpoint tests, new lifecycle statuses, external pilot behavior, or runtime integration beyond exact scope. | Must assert endpoint remains out of scope if lifecycle/close behavior is touched. | Endpoint coupling, new lifecycle vocabulary, weakened closed-case safety, or skipped regression coverage. |
| `backend/tests/test_case_store.py` | Candidate test file for store-level persistence and round-trip behavior. | Synthetic-only round-trip preservation tests for action requests, lifecycle audit, and append-safe traces. | Fixture file creation, raw customer/operator evidence, evidence retention behavior, or broad backend store changes. | Must cover store behavior if `case_store.py` changes. | Fixture changes, raw evidence, skipped round-trip assertions, or backend expansion. |
| `backend/tests/test_runtime_service.py` | Candidate test file for runtime service invalid-transition and closed-case safety behavior if runtime seam is named. | Synthetic-only deterministic invalid-transition payload assertions and runtime guard assertions if exact scope names `runtime_service.py`. | Public close-case endpoint work, new runtime API/schema contracts, live access, response automation, or config changes. | Must cover runtime behavior if `runtime_service.py` changes. | Endpoint work, API/schema expansion, live access, automation, or ambiguous error contract. |

## 7. Candidate Behavior Scope

| Behavior candidate | Governed source | Later implementation may include | Later implementation must not include | Required tests/assertions | HOLD triggers |
| --- | --- | --- | --- | --- | --- |
| Preserve `action_request_status` separate from case `lifecycle_status` | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Separate synthetic model/store/runtime checks if exact scope names the relevant files. | Merging action request state into case lifecycle state or creating new lifecycle vocabulary. | Assertions that action-request transitions do not mutate case lifecycle status except where already governed and exact. | State merge, new lifecycle status, or ambiguous persistence. |
| Approval records a non-destructive review decision only | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md` | Approval status/trace recording and non-execution guard if exact scope names it. | Destructive execution, response automation, real customer/operator sign-off, or external action. | Assertions that approval does not execute, call external systems, or imply real sign-off. | Execution, external action, sign-off implication, or automation. |
| Denial/rejection preserves request and audit history | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Denial/rejection decision state and append-safe trace if exact scope names it. | Deleting evidence, request history, or audit history; adding new status vocabulary. | Assertions that denial/rejection preserves original request and prior audit entries. | Deletion, history loss, or new persisted status. |
| Cancellation/withdrawal preserves original request and prior history | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md` | Cancellation/withdrawal decision trace if exact scope names it. | Erasing original request, erasing prior history, or inventing broader workflow engine behavior. | Assertions that original request and previous decisions remain inspectable after cancellation/withdrawal. | Request erasure, history loss, workflow expansion, or automation. |
| Closed cases cannot accept new or updated action requests | `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; `docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md` | Store/runtime guards against post-close action-request creation or update if exact scope names the seam. | Weakening closed-case safety, public close-case endpoint behavior, or unsafe post-close mutation. | Assertions for rejection of new and updated action requests on closed cases. | Post-close mutation, endpoint work, or ambiguous closed-case state. |
| Lifecycle/action-request audit remains append-safe and replayable | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Append-only synthetic decision traces and deterministic replay/round-trip checks if exact scope names it. | Evidence retention, raw evidence storage, mutable audit, or evidence-pack behavior. | Assertions that prior audit entries remain and replay/round-trip keeps decision trace order. | Audit deletion, raw evidence retention, mutable trace, or retention policy freeze. |
| Close reason / lifecycle semantics remain within governed vocabulary | `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Existing governed vocabulary checks if exact scope names it. | New close reason values, new lifecycle states, public endpoint behavior, or API/schema freeze. | Assertions that no new vocabulary is introduced and `KEEP_DEFERRED` remains intact. | New vocabulary, endpoint scope, or weakened `KEEP_DEFERRED`. |
| Runtime service invalid-transition behavior may be deterministic only if exact scope names `runtime_service.py` | `docs/S5C_SCOPED_IMPLEMENTATION_DECISION.md`; `docs/S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_TICKET.md` | Stable synthetic invalid-transition response shape if the later ticket explicitly includes `backend/app/runtime_service.py`. | New runtime API/schema contract, public endpoint work, live system access, or config integration. | Assertions in `backend/tests/test_runtime_service.py` only if runtime file is in scope. | Runtime file omitted but behavior changed, API/schema expansion, or endpoint creep. |

## 8. Required Future Tests And Commands

A later implementation ticket must name exact tests before code/test work begins. Candidate commands are:

- `py -3 -m unittest -q backend.tests.test_case_action_request_contract`
- `py -3 -m unittest -q backend.tests.test_case_lifecycle_regression`
- `py -3 -m unittest -q backend.tests.test_case_store`
- `py -3 -m unittest -q backend.tests.test_runtime_service`
- `py -3 scripts\git_preflight.py --mode all`

The later ticket must state which commands are required for its exact file scope. The full gate command remains required before staging, committing, or pushing any later implementation.

## 9. Non-Authorization

This docs-only draft does not authorize:

- implementation now
- code changes now
- test changes now
- HANDOFF changes during draft
- release_manifest changes during draft
- full gate during draft
- staging, commit, or push during draft
- public close-case endpoint work
- weakening `KEEP_DEFERRED`
- new public API endpoints
- new runtime API/schema contracts
- dependency changes
- fixture file creation or modification
- new persisted lifecycle statuses
- new persisted action-request statuses unless already governed and exact
- approval triggering destructive execution
- approval being treated as real customer/operator sign-off
- denial/rejection deleting evidence, request history, or audit history
- cancellation/withdrawal erasing original request or prior history
- audit traceability becoming evidence retention
- redaction policy freeze
- secrets handling implementation
- evidence retention, storage, replay, deletion, expiry, or evidence-pack behavior
- real SIEM/EDR/source/telemetry access
- credentials, tokens, API keys, auth headers, cookies, or secret material
- raw logs, screenshots, exports, payloads, event bodies, or customer/operator evidence
- external pilot execution
- external pilot readiness
- real customer/operator sign-off
- S5-B reopen
- S5-D reopen
- S4-A resolver authority or priority changes
- AI_COLLAB operating model or contract changes
- external review bypass
- human go/no-go replacement
- automatic implementation
- ORDIV-L1A validation report creation, metric recording, or further real-data work
- CSV processing
- L1B syslog/log parsing

## 10. HOLD Conditions

This route must HOLD if any of the following appears:

- Any implementation instruction appears in this draft.
- Code changes, test changes, runtime/API/schema changes, dependency changes, config changes, or fixture changes appear during this draft.
- HANDOFF or release_manifest changes appear during this draft.
- Full gate, staging, commit, or push is attempted during this draft.
- Claude Web external review is skipped before any later implementation human go/no-go.
- Human go/no-go is absent before any later implementation attempt.
- Exact governed clauses are not named in the later implementation ticket.
- Exact files are not named in the later implementation ticket.
- Exact behavior deltas are not named in the later implementation ticket.
- Exact tests and test commands are not named in the later implementation ticket.
- Rollback / HOLD plan is missing in the later implementation ticket.
- `reviewer_when_cc_implements` is missing if Claude Code becomes primary implementor later.
- Public close-case endpoint work appears or `KEEP_DEFERRED` is weakened.
- New public API endpoints or runtime API/schema contracts appear.
- New persisted lifecycle statuses appear.
- New persisted action-request statuses appear unless already governed and exact.
- Approval triggers destructive execution or is treated as real customer/operator sign-off.
- Denial/rejection deletes evidence, request history, or audit history.
- Cancellation/withdrawal erases original request or prior history.
- Audit traceability becomes evidence retention.
- Evidence retention, storage, replay, deletion, expiry, evidence-pack behavior, redaction policy freeze, or secrets handling implementation appears.
- Real SIEM/EDR/source/telemetry access appears.
- Credentials, tokens, API keys, auth headers, cookies, or secret material appear.
- Raw logs, screenshots, exports, payloads, event bodies, or customer/operator evidence appear.
- External pilot execution, readiness, or real sign-off appears.
- S5-B or S5-D reopen appears without explicit reopen decision.
- S4-A resolver authority or priority changes appear.
- AI_COLLAB operating model or contract changes appear.
- ORDIV-L1A report creation, metric recording, workbook access, CSV processing, L1B/syslog work, or further real-data work appears.

## 11. Future Implementation Preconditions

Implementation may begin only after a later implementation ticket satisfies all of the following:

- Claude Web external review gate is completed.
- Explicit human go/no-go is recorded after Claude Web review.
- Exact governed S5-C clauses are confirmed.
- Exact files are confirmed.
- Exact behavior deltas are confirmed.
- Exact tests are confirmed.
- Targeted test commands are named.
- Full gate command `py -3 scripts\git_preflight.py --mode all` is named.
- No HOLD triggers are active.
- Rollback plan is stated.
- `reviewer_when_cc_implements` assignment is stated if Claude Code becomes primary implementor in any later route.
- Public close-case endpoint status remains `KEEP_DEFERRED`.
- S5-B and S5-D remain `PASS_AND_PARK`.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- External pilot execution/readiness/sign-off remain unauthorized.
- Real external-system access, credentials, raw evidence, and evidence retention remain prohibited.
- ORDIV-L1A remains parked unless a separate governed route explicitly changes that posture.

## 12. Rollback / HOLD Plan For Later Implementation

A later implementation ticket must include a rollback / HOLD plan before code/test work begins:

- If any HOLD trigger appears, stop implementation immediately.
- Revert or remove only the later implementation changes created by that later ticket; do not revert unrelated user or governance changes.
- Preserve existing S5-C governed baselines and `KEEP_DEFERRED`.
- Preserve action-request and lifecycle audit data in any synthetic test scenario.
- Do not delete evidence, request history, audit history, fixtures, or external data as a rollback behavior.
- Rerun named targeted tests and the full gate before any later commit.

## 13. Acceptance Criteria For This Draft

- Exactly one new docs file is created.
- Baseline and predecessor artifacts are accurate.
- `requires_external_review=true` is documented with rationale.
- Role model is explicit.
- Candidate implementation file scope is exact and bounded.
- Candidate test file scope is exact and bounded.
- Behavior deltas are governed and bounded.
- Non-authorization section is comprehensive.
- HOLD conditions are explicit.
- Implementation preconditions include Claude Web external review and human go/no-go.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- S5-B and S5-D remain `PASS_AND_PARK`.
- S4-A resolver order remains unchanged.
- External pilot remains unauthorized.
- ORDIV-L1A remains parked with no report, metrics, or further real-data work.
- No code/test/dependency/runtime/config/fixture/governed contract changes are made or authorized.
- No HANDOFF or manifest changes are made.
- No full gate is run.
- Nothing is staged, committed, or pushed.

## 14. Preliminary Recommendation

`PRELIMINARY_RECOMMENDATION_READY_FOR_CLAUDE_CODE_REVIEW_ONLY`

Meaning:

- This docs-only draft may be reviewed by Claude Code.
- If accepted and later closed as governed, it may permit a separate future S5-C-IMPL-5 code/test implementation ticket to be prepared for human consideration.
- Any later implementation attempt still requires Claude Web external review and explicit human go/no-go.
- Any later implementation ticket may still HOLD if exact clauses, files, behavior deltas, tests, rollback criteria, or boundaries are not clean enough.

Non-meaning:

- This does not authorize implementation now.
- This does not authorize code or test changes now.
- This does not authorize public close-case endpoint work.
- This does not authorize external pilot execution or readiness.
- This does not authorize S5-B/S5-D reopen, S4-A resolver changes, AI_COLLAB changes, ORDIV-L1A real-data work, or automatic implementation.
