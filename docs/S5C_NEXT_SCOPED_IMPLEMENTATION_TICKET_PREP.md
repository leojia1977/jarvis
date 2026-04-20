# S5-C Next Scoped Implementation Ticket Prep

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S5-C Next Scoped Implementation Ticket Prep |
| Status | Draft governed docs-only ticket-prep stage |
| Scope | Prepare the next possible S5-C scoped implementation ticket without authorizing implementation |
| Snapshot | S5C-NEXT-SCOPED-IMPLEMENTATION-TICKET-PREP-2026-04-20-001 |
| Stage | s5c-next-scoped-implementation-ticket-prep |
| Baseline commit | `e399726f612916308f398437da4e6a36d88cb89b` |
| Baseline snapshot | S5-NEXT-PRODUCT-DEVELOPMENT-ROUTE-SELECTION-2026-04-19-001 |
| Baseline stage | s5-next-product-development-route-selection |
| Baseline manifest status | PASS |
| Baseline release sha256 | `12a1b9a952e32e46b09c5a144196725c3991b89e000e1625dae853d6594027a5` |
| Route opened by | Human product/governance prompt `OPEN_S5C_NEXT_SCOPED_IMPLEMENTATION_TICKET_PREP` |
| Lane | Green docs-only ticket prep |
| Required review | Claude Code review-only; Claude Web/external review is required before any later implementation GO because lifecycle/close semantics are in scope |

This stage prepares a possible later S5-C scoped implementation ticket. It does not implement code, modify tests, create fixtures, change dependencies, update runtime/API/schema behavior, or authorize launch, deployment, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB changes.

## 2. Startup And Baseline Verification

Autonomous startup checks for this stage:

- `docs\DELEGATED_APPROVER_CHARTER.md` was readable.
- `delegation_expires` is `2026-05-06 23:59 Asia/Shanghai`, which has not passed at draft time.
- The current branch is `codex/s3-a-runtime`.
- Baseline commit is `e399726f612916308f398437da4e6a36d88cb89b`.
- Baseline manifest snapshot is `S5-NEXT-PRODUCT-DEVELOPMENT-ROUTE-SELECTION-2026-04-19-001`.
- Baseline manifest verification status is `PASS`.
- Baseline release sha256 is `12a1b9a952e32e46b09c5a144196725c3991b89e000e1625dae853d6594027a5`.
- The only known out-of-scope untracked files are `CLAUDE.md` and `SecuPilot_阶段性总结_20260409.md`; this stage does not touch them.

The governed route-selection baseline selected:

```text
OPEN_S5C_NEXT_SCOPED_IMPLEMENTATION_TICKET_PREP
```

Meaning:

- Draft a Green docs-only ticket-prep artifact for a possible later S5-C scoped implementation ticket.
- Inspect existing governed S5-C decisions and current code/test reality as baseline context.
- Name exact future files, behavior, tests, review triggers, GO requirement, and HOLD conditions if a clean future ticket exists.
- HOLD rather than invent implementation scope if exact future files, behavior, tests, and acceptance criteria cannot be named safely.

## 3. Governed Inputs Checked

This ticket-prep stage checked these governed S5-C source artifacts:

- `docs\S5C_CASE_WORKFLOW_HARDENING_PLAN.md`
- `docs\S5C1_CASE_WORKFLOW_JOURNEY_CONTRACT.md`
- `docs\S5C2_CLOSE_REASON_AND_LIFECYCLE_SEMANTICS.md`
- `docs\S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`
- `docs\S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`
- `docs\S5C5_CASE_WORKFLOW_REVIEW_PASS.md`
- `docs\S5C_SCOPED_IMPLEMENTATION_DECISION.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_TICKET.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_CODE_TEST_TICKET.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_CLOSEOUT.md`
- `docs\S5_POST_S5C_IMPL5_ROUTE_DECISION.md`
- `docs\S5_POST_S5C_IMPL5_MAINLINE_ROUTE_SELECTION.md`
- `docs\NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION.md`

This stage also checked current code/test reality as read-only baseline context:

- `backend\app\tools\persistent_case.py`
- `backend\app\tools\case_store.py`
- `backend\app\runtime_service.py`
- `backend\tests\test_case_action_request_contract.py`
- `backend\tests\test_case_lifecycle_regression.py`
- `backend\tests\test_case_store.py`
- `backend\tests\test_runtime_service.py`

No code or test file was modified by this stage.

## 4. Current S5-C Implementation Reality

S5-C-IMPL-5 is closed as governed. Current code/test baseline already covers:

- locked case lifecycle status vocabulary: `open`, `in_review`, `approved`, `closed`
- locked action request status vocabulary: `draft`, `pending_approval`, `approved`, `rejected`, `cancelled`
- action request status remains separate from case lifecycle status
- approval is non-destructive review data only
- rejection and cancellation preserve request and audit history
- closed cases reject action-request create, submit, approve, reject, and cancel paths
- action-request and lifecycle audit remain append-safe and replayable in synthetic tests
- runtime service action-request error behavior is deterministic for the governed S5-C-IMPL-5 scope

Current code/test baseline does not yet freeze S5-C-2 close reason taxonomy in implementation. `transition_persistent_case_status()` accepts a free-form `reason` and optional `details`, but no governed internal helper currently validates the S5-C-2 close reason vocabulary or records a bounded close reason in audit details. This gap is narrow enough for future ticket preparation, provided the later ticket remains internal, synthetic-only, and non-endpoint.

## 5. Candidate Routes Considered

| Candidate route | Meaning | Current status | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| A. `OPEN_S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_TICKET` | Prepare a later scoped implementation ticket for internal close reason taxonomy validation and audit detail hardening, without public endpoint work. | Clean candidate for later Yellow implementation after review and GO. | Could be mistaken for public close-case endpoint or schema/API expansion. | Selected future ticket candidate. |
| B. `OPEN_PUBLIC_CLOSE_CASE_ENDPOINT_ROUTE` | Reopen public close-case HTTP endpoint implementation or route design. | Blocked by `KEEP_DEFERRED` and AHQ-013. | Public API/runtime/schema risk. | HOLD. |
| C. `OPEN_S5C_ACTION_REQUEST_FOLLOWUP_IMPLEMENTATION` | Continue action-request implementation beyond S5-C-IMPL-5. | No exact new product gap found beyond already closed S5-C-IMPL-5 scope. | Would duplicate closed implementation or invent scope. | HOLD. |
| D. `OPEN_S5C_RBAC_OR_WORKFLOW_ENGINE_ROUTE` | Add roles, RBAC, ticketing, or workflow-engine behavior. | Out of scope in S5-C contracts. | Authorization and integration creep. | HOLD. |
| E. `OPEN_EXTERNAL_PILOT_EVIDENCE_OR_READINESS_ROUTE` | Tie S5-C workflow to external pilot inputs or real evidence. | Blocked by AHQ-003 and external pilot `NOT_READY` / `UNKNOWN`. | Readiness and real-data risk. | HOLD. |
| F. `PARK_S5C_NEXT_IMPLEMENTATION` | Do not prepare a ticket. | Safe fallback. | Progress stalls despite a narrow internal S5-C-2 candidate. | Fallback only. |

## 6. Selected Future Ticket Candidate

Selected future candidate:

```text
OPEN_S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_TICKET
```

Proposed future ticket title:

```text
S5-C-IMPL-6 Close Reason Internal Semantics Scoped Implementation Ticket
```

Meaning:

- A later separate ticket may scope a Yellow implementation that validates S5-C-2 close reason taxonomy in internal persistent-case helpers and synthetic tests.
- The later ticket may define a non-public helper such as governed close reason vocabulary validation or an internal close-case helper that records close reason in existing audit `details`.
- The later ticket must preserve current lifecycle status vocabulary and must not add a persisted dataclass field, public endpoint, public API method/path, runtime API/schema contract, dependency, fixture, real-data behavior, evidence retention behavior, or redaction policy freeze.
- The later ticket must preserve S5-C-IMPL-5 action-request lifecycle guarantees.

Non-meaning:

- This stage does not authorize implementation.
- This stage does not authorize code/test changes.
- This stage does not authorize public close-case endpoint work.
- This stage does not authorize a public close-case HTTP route.
- This stage does not authorize runtime/API/schema expansion.
- This stage does not authorize external pilot readiness or execution.
- This stage does not authorize real data, credentials, evidence retention, evidence replay, evidence deletion/expiry, evidence-pack behavior, or redaction policy freeze.

## 7. Candidate Future File Scope

The future implementation ticket, if opened, should start from this exact candidate scope and reduce it further if possible.

| File | Candidate role | Later change may include | Later change must not include | Required test relationship | HOLD triggers |
| --- | --- | --- | --- | --- | --- |
| `backend\app\tools\persistent_case.py` | Candidate implementation file for internal close reason vocabulary validation and audit detail helper behavior. | Governed close reason constants, a read-only vocabulary accessor, and an internal close helper or validator that keeps `lifecycle_status=closed` within existing vocabulary and records close reason only in existing audit metadata if exact ticket scope names it. | New lifecycle states, new action-request statuses, public endpoint behavior, public API/schema behavior, persisted dataclass field additions unless separately reviewed, evidence retention, real-data handling, secrets handling, broad model rewrite. | Must be covered by lifecycle regression and store round-trip tests if changed. | New persisted status, endpoint coupling, schema/API expansion, evidence behavior, or ambiguous close semantics. |
| `backend\tests\test_case_lifecycle_regression.py` | Candidate test file for internal close reason lifecycle behavior. | Synthetic-only tests that allowed close reasons are accepted, unknown close reasons are rejected where the new helper is used, `lifecycle_status` remains `closed`, audit order remains deterministic, and public endpoint remains out of scope. | Public endpoint tests, real evidence, fixture files, new lifecycle status, external pilot behavior. | Required if `persistent_case.py` close helper or validator changes. | Endpoint scope, real data, new lifecycle vocabulary, or skipped closed-case safety assertions. |
| `backend\tests\test_case_store.py` | Candidate test file for persistence round-trip of existing audit metadata. | Synthetic-only round-trip checks that close reason audit details, if added by the helper, survive serialization without creating new persisted status fields. | Fixture creation, raw customer/operator evidence, evidence retention, broad backend changes. | Required if audit details are added or close helper output must round-trip. | Fixture changes, evidence handling, dataclass schema creep, or skipped round-trip assertions. |
| `backend\tests\test_case_action_request_contract.py` | Candidate test file only if the later ticket touches close behavior with unresolved action requests. | Synthetic-only preservation checks that S5-C-IMPL-5 action-request history and non-destructive decision semantics are not weakened. | New action-request status, endpoint-coupled pending-close behavior, destructive execution, sign-off semantics. | Optional; required only if later behavior touches action request closure interactions. | S5-C-IMPL-5 regression, endpoint coupling, or action-request status expansion. |

Files intentionally excluded from the first future candidate:

- `backend\app\runtime_service.py` is excluded unless a later ticket proves an internal runtime seam is needed without public endpoint/API/schema expansion.
- `backend\app\main.py` is excluded because public endpoint work remains `KEEP_DEFERRED`.
- fixture files are excluded.
- dependency files are excluded.
- release scripts are excluded.
- AI_COLLAB files are excluded.

## 8. Candidate Future Behavior Scope

| Future behavior candidate | Later implementation may include | Later implementation must not include | Required assertions | HOLD triggers |
| --- | --- | --- | --- | --- |
| Governed close reason vocabulary accessor | Return the S5-C-2 close reason vocabulary as internal helper data. | New lifecycle status, public API exposure, persisted field freeze. | Vocabulary includes only governed S5-C-2 close reasons and excludes future/unknown values. | Vocabulary expansion beyond S5-C-2 or public API coupling. |
| Close reason validation for internal helper use | Reject unknown close reasons when the new helper is used. | Retrofitting all lifecycle transitions without exact review, changing `transition_persistent_case_status()` broad semantics without review, endpoint behavior. | Unknown close reason raises deterministic error in helper path; existing lifecycle transitions remain governed. | Broad behavior change or ambiguous error contract. |
| Audit detail recording for close reason | Store close reason in existing audit `details` only if the exact future ticket chooses that path. | New dataclass field, evidence retention, raw external data, customer/operator evidence, redaction policy freeze. | Audit details round-trip and contain only non-sensitive close reason metadata. | Raw evidence, new schema field, retention behavior, or secrets. |
| Preserve lifecycle vocabulary | Keep `lifecycle_status` bounded to `open`, `in_review`, `approved`, `closed`. | `close_pending`, `archived`, `resolved`, or other new persisted lifecycle states. | Existing vocabulary tests remain passing and add no new statuses. | Any new persisted lifecycle state. |
| Preserve public endpoint deferral | Keep public close-case HTTP endpoint out of scope. | Method/path/request/response/error model, public endpoint route, API/schema contract. | Tests and docs state endpoint remains `KEEP_DEFERRED`. | Endpoint work or public API freeze. |
| Preserve S5-C-IMPL-5 action-request guarantees | Keep action request decisions non-destructive and history-preserving. | Approval execution, evidence deletion, action-request status expansion, real sign-off. | Existing S5-C-IMPL-5 tests remain in targeted and full gate. | Regression in action-request lifecycle. |

## 9. Required Future Review And GO

The later implementation ticket must set:

- lane: Yellow implementation
- required review: Claude Code review-only plus Claude Web/external review before implementation GO
- implementor: Codex or VS Code only as explicitly assigned by the later ticket
- reviewer_when_cc_implements: required if Codex/Claude Code performs implementation
- human GO: required before code/test implementation begins

Reviewer PASS is evidence only. It is not implementation authority.

The implementation GO must name:

- approver role: human product/governance approver, or delegated approver only where the activated policy explicitly permits the lane
- approval channel: explicit prompt or governed decision artifact
- stage/ticket
- lane
- approved action
- exact file scope
- required review evidence
- rollback/HOLD criteria
- expiration where applicable

Silence, inferred consent, incomplete approval text, expired approval, lane ambiguity, missing file scope, missing review evidence, or unresolved HOLD means implementation remains HOLD.

## 10. Required Future Tests And Commands

The later implementation ticket must name exact tests before code/test work begins. Candidate commands:

- `py -3 -m unittest -q backend.tests.test_case_lifecycle_regression`
- `py -3 -m unittest -q backend.tests.test_case_store`
- `py -3 -m unittest -q backend.tests.test_case_action_request_contract`
- `py -3 scripts\git_preflight.py --mode all`

The future ticket must decide whether `backend.tests.test_case_action_request_contract` is required based on whether action-request closure interactions are touched.

Full gate remains required before staging, committing, or pushing any later implementation.

## 11. HOLD Conditions

This ticket-prep stage must HOLD if any action attempts to:

- implement code or tests now
- modify dependencies, fixtures, runtime/API/schema, release scripts, contracts, or AI_COLLAB
- infer Yellow implementation authority from this prep
- open public close-case endpoint work or weaken `KEEP_DEFERRED`
- add public API method/path/request/response/error model
- add new persisted lifecycle statuses or action-request statuses
- add close reason behavior as real customer/operator sign-off
- add evidence retention, storage, replay, deletion, expiry, evidence-pack behavior, or redaction policy freeze
- access or handle credentials, tokens, API keys, auth headers, cookies, sessions, or secrets
- access, parse, summarize, retain, or validate real customer/operator data
- claim external pilot readiness or execute external pilot work
- reopen S5-B or S5-D without a separate governed reopen decision
- reopen ORDIV work without a separate governed route
- change S4-A resolver order or authority
- perform Red-3 action
- use Claude Code for file edits, command execution, tests, staging, commit, or push
- use AdsPower for login automation, profile creation/switching, session inspection, or browser-storage/profile-file inspection
- stage, commit, or push without applicable governed closeout authority

## 12. Non-Authorization

This ticket-prep stage does not authorize:

- implementation
- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime/API/schema changes
- release script changes
- contract changes
- AI_COLLAB changes
- Yellow implementation
- Red execution
- launch execution
- production deployment
- external pilot execution
- external pilot readiness
- real customer/operator sign-off
- credential handling by AI
- real-data handling
- evidence retention, evidence replay, evidence deletion/expiry, or evidence-pack behavior
- redaction policy freeze
- public endpoint work
- S5-B reopen
- S5-D reopen
- ORDIV reopen/report/CSV/L1B work
- S4-A resolver order or authority changes
- Red-3 action
- AdsPower profile creation/switching or Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection
- Claude Code file edits, command execution, tests, staging, commit, or push

## 13. Acceptance Criteria

This docs-only ticket-prep stage is acceptable when:

- this document records the current governed baseline
- the selected future candidate is `OPEN_S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_TICKET`
- exact candidate future files are named
- exact candidate future behavior is bounded
- exact candidate future tests are named
- `backend\app\runtime_service.py` and public endpoint files are excluded unless separately governed
- `requires_external_review` and human GO requirements are explicit
- inherited boundaries remain preserved
- rolling maps are updated as passive context
- `docs\HANDOFF.md` records the ticket-prep stage
- `releases\release_manifest.json` records the new snapshot/stage in draft state
- manifest `current_release_sha256` remains `null`
- manifest verification fields remain `PENDING_FULL_GATE_AFTER_REVIEW` until full gate PASS
- release zip path in the manifest is a draft placeholder only; no release artifact is expected before full closeout gate/package/release verification
- no code/test/dependency/fixture/runtime/API/schema/release-script/contract/AI_COLLAB files are modified
- known out-of-scope untracked files remain untouched and unstaged

## 14. Preliminary Recommendation

```text
PRELIMINARY_RECOMMENDATION_OPEN_S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_TICKET
```

Meaning:

- A clean next S5-C implementation candidate exists, but only as a future separate Yellow implementation ticket.
- The future ticket should be limited to internal close reason taxonomy validation and synthetic tests.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- Implementation remains HOLD until a separate scoped ticket, required review, explicit GO, full gate, release verification, and governed closeout are completed.
