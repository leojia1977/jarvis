# S5-C Autonomous Yellow Backlog Preauthorization

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S5-C Autonomous Yellow Backlog Preauthorization |
| Status | Draft governed docs-only conditional Yellow preauthorization |
| Scope | Define exact Yellow implementation backlog items that may run autonomously after S5-C stream refresh closeout PASS |
| Snapshot | S5C-STREAM-REVIEW-REFRESH-2026-04-20-001 |
| Stage | s5c-stream-review-refresh |
| Baseline commit | `0f59584f307aaf8e4adc582cfd73f83ae43c0dcc` |
| Baseline snapshot | S5-POST-S5C-IMPL7-ROUTE-DECISION-2026-04-20-001 |
| Baseline stage | s5-post-s5c-impl7-route-decision |
| Baseline manifest status | PASS |
| Baseline release sha256 | `2f246b5c727e44401d1feb3c06d674c2ae6259d78ca9504f7ef34d64d6de7968` |
| Requested by | Human product/governance prompt asking the autonomous loop to prepare exact Yellow backlog preauthorization |
| Lane of this document | Green docs-only preauthorization package |
| Lane of listed future implementation items | Yellow implementation |

This document is the exact bounded backlog package requested for vacation-mode continuous development. It authorizes nothing until the paired `docs\S5C_STREAM_REVIEW_REFRESH.md` stage closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push. After that, it may be used only for the listed Yellow items and only under the per-item file, behavior, test, review, and HOLD rules below.

## 2. Standing Preconditions For Every Listed Yellow Item

Every listed Yellow implementation item must satisfy all standing preconditions before work starts:

1. Current repo baseline manifest is PASS.
2. `docs\DELEGATED_APPROVER_CHARTER.md` is readable and `delegation_expires` has not passed.
3. Core governance docs are loaded.
4. The selected item appears in this document.
5. Only one Yellow backlog item is implemented per autonomous run.
6. The implementation starts from the latest governed baseline and clean git status except known unrelated untracked files.
7. The implementation touches only the item-specific allowed implementation/test files plus later closeout docs/manifest.
8. Claude Code review-only is used for implementation review through the governed verdict-line path.
9. Targeted tests and `py -3 scripts\git_preflight.py --mode all` pass before closeout.
10. Release package and manifest verification PASS before any implementation closeout commit/push.
11. Exact staged files are limited to the implementation files, tests, closeout docs, rolling maps, and manifest for that item.
12. Any ambiguity, missing scope, failing test outside allowed files, or Red trigger means HOLD.

This preauthorization includes staging, commit, and push for each listed Yellow item only after that item's review PASS, targeted tests PASS, full gate PASS, release verification PASS, manifest PASS, exact staged scope, and no-HOLD checks pass. It does not authorize staging, commit, or push for any unlisted item or excluded file.

## 3. Backlog Item 01 - Internal Workflow Summary Helper

| Field | Value |
| --- | --- |
| Item ID | `S5C-YB-01` |
| Route name | `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_01` |
| Future implementation snapshot prefix | `S5C-IMPL8-INTERNAL-WORKFLOW-SUMMARY` |
| Lane | Yellow implementation |
| Purpose | Add a read-only internal summary helper for lifecycle, review owner, action-request counts, latest audit event, and close reason derived from `PersistentCaseRecord`. |

Allowed files:

- `backend\app\tools\persistent_case.py`
- `backend\tests\test_case_lifecycle_regression.py`
- `backend\tests\test_case_store.py`

Exact allowed behavior:

- Add an internal helper with a clear name such as `persistent_case_workflow_summary(record)`.
- The helper may return a plain dict derived only from the supplied `PersistentCaseRecord`.
- The helper may include:
  - `lifecycle_status`
  - `review_owner`
  - `action_request_counts`
  - `pending_action_request_count`
  - `latest_audit_event_type`
  - `latest_audit_reason`
  - `close_reason` only if present in existing lifecycle audit `details`
  - `execution_authorized: False`
- The helper must not mutate the record.
- The helper must not add persisted fields, dataclass fields, database columns, runtime routes, public API fields, or case-view top-level panels.
- The helper must not infer launch readiness, execution authority, or external sign-off.

Required targeted tests:

- `py -3 -m unittest -q backend.tests.test_case_lifecycle_regression backend.tests.test_case_store`

Required test assertions:

- summary from open case has `lifecycle_status="open"` and zero pending action requests
- summary from submitted action request has pending count 1
- summary from approved action request remains non-execution-authorizing
- summary from closed case includes close reason only from audit `details`
- store round-trip preserves the summary source data
- helper does not mutate the original record

HOLD if:

- implementation needs `backend\app\runtime_service.py`, `backend\app\main.py`, public endpoint/API/schema files, fixture files, dependency files, release scripts, contracts, AI_COLLAB, or real data
- a new persisted field, lifecycle status, action-request status, audit event type, database column, API response field, or case-view top-level panel is needed
- close reason must be promoted out of audit `details`
- execution authority, launch readiness, or external sign-off is implied

## 4. Backlog Item 02 - Audit Event Vocabulary Guard

| Field | Value |
| --- | --- |
| Item ID | `S5C-YB-02` |
| Route name | `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_02` |
| Future implementation snapshot prefix | `S5C-IMPL9-AUDIT-EVENT-VOCABULARY-GUARD` |
| Lane | Yellow implementation |
| Purpose | Add runtime validation for the existing audit event vocabulary during serialization/deserialization without adding new event types. |

Allowed files:

- `backend\app\tools\persistent_case.py`
- `backend\tests\test_case_action_request_contract.py`
- `backend\tests\test_case_store.py`

Exact allowed behavior:

- Add `GOVERNED_AUDIT_EVENT_TYPES` derived from the existing `AuditEventType` literal.
- Add `governed_audit_event_types()` returning the sorted vocabulary.
- Add `_require_audit_event_type()` that rejects unknown values with `invalid_audit_event_type:<value>`.
- Validate audit event type in `_audit_entry_from_dict()` and `_validate_persistent_case_record()`.
- Do not add, rename, remove, or reinterpret any audit event type.
- Do not change lifecycle/action-request transition semantics.

Required targeted tests:

- `py -3 -m unittest -q backend.tests.test_case_action_request_contract backend.tests.test_case_store`

Required test assertions:

- governed audit event vocabulary equals the existing literal set
- deserialization rejects unknown audit event type
- serializer validation rejects mutated in-memory record with unknown audit event type
- existing action-request and close-reason round trips still pass

HOLD if:

- a new audit event type is needed
- a migration/backfill is needed
- runtime/API/schema behavior is needed
- existing persisted lifecycle/action-request statuses must change
- evidence retention, redaction policy, real data, credentials, or public endpoint behavior appears

## 5. Backlog Item 03 - Pending Action Request Boundary Helpers

| Field | Value |
| --- | --- |
| Item ID | `S5C-YB-03` |
| Route name | `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_03` |
| Future implementation snapshot prefix | `S5C-IMPL10-PENDING-ACTION-REQUEST-BOUNDARY-HELPERS` |
| Lane | Yellow implementation |
| Purpose | Add internal read-only helpers for pending action-request detection so future endpoint decisions cannot bypass pending-request boundaries. |

Allowed files:

- `backend\app\tools\persistent_case.py`
- `backend\tests\test_case_action_request_contract.py`
- `backend\tests\test_case_lifecycle_regression.py`

Exact allowed behavior:

- Add internal helper(s) such as `pending_action_request_ids(record)` and `has_pending_action_requests(record)`.
- Pending means action request status exactly `pending_approval`.
- Helpers must be read-only and must not mutate action requests or lifecycle audit.
- Helpers must not approve, reject, cancel, submit, close, reopen, or execute anything.
- Helpers must not expose runtime/API behavior or public endpoint behavior.

Required targeted tests:

- `py -3 -m unittest -q backend.tests.test_case_action_request_contract backend.tests.test_case_lifecycle_regression`

Required test assertions:

- draft action request is not pending
- submitted action request is pending
- approved/rejected/cancelled action requests are not pending
- closed case with pending request remains detectable as pending but not mutable
- helper output is deterministic after serialization round trip

HOLD if:

- implementation needs endpoint behavior, runtime service changes, public API/schema changes, or `backend\app\main.py`
- pending action request handling requires policy decisions beyond read-only detection
- helper starts closing cases, rejecting requests, cancelling requests, or modifying audit
- RBAC, ticketing, workflow engine, external system, or destructive response semantics appear

## 6. Backlog Item 04 - Case View Review Guidance Regression Hardening

| Field | Value |
| --- | --- |
| Item ID | `S5C-YB-04` |
| Route name | `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_04` |
| Future implementation snapshot prefix | `S5C-IMPL11-CASE-VIEW-REVIEW-GUIDANCE-REGRESSION-HARDENING` |
| Lane | Yellow implementation |
| Purpose | Strengthen synthetic regression coverage for internal case-view review guidance edge cases without changing runtime/API/schema behavior. |

Allowed files:

- `backend\tests\test_case_view.py`

Exact allowed behavior:

- Add synthetic tests for no-chain complete cases, low-confidence cases, degraded cases with a suggested action, and partial cases with evidence gaps.
- Preserve the existing top-level case view panel set.
- Preserve `CASE_VIEW_SCHEMA_VERSION`.
- Preserve `analysis_limits["review_guidance"]` as the only review-guidance location.
- Preserve `execution_authorized: False`.
- This item is test-only. If the new tests reveal a need to edit `backend\app\agents\case_view.py`, this item must HOLD and open a later separate scoped route for that exact code change.

Required targeted tests:

- `py -3 -m unittest -q backend.tests.test_case_view`

Required test assertions:

- no-chain complete case keeps review guidance safe and non-execution-authorizing
- low-confidence case surfaces analyst review need without manager execution authority
- degraded case with suggested action still disables execution
- partial case with evidence gaps includes bounded analyst questions
- top-level case view panel set remains unchanged

HOLD if:

- any code file needs to change
- implementation needs runtime/API/schema behavior
- implementation needs `backend\app\runtime_service.py`, `backend\app\main.py`, public endpoint/API/schema files, persistent case files, fixture files, dependencies, release scripts, contracts, AI_COLLAB, real data, or credentials
- a new top-level case view panel or schema version bump is needed
- review guidance implies destructive response execution, launch readiness, external pilot readiness, or real customer/operator sign-off

## 7. Execution Order

Default autonomous order:

1. `S5C-YB-01`
2. `S5C-YB-02`
3. `S5C-YB-03`
4. `S5C-YB-04`

Automation may skip an item only if a later route records a reason such as "already satisfied" or "HOLD." Automation must not reorder items if reordering would create dependency ambiguity.

## 8. Review And Closeout Rules For Each Yellow Item

Each item must produce its own implementation closeout artifact and update rolling maps and manifest. Each item must:

- record current baseline commit, snapshot, manifest PASS, and release sha256
- record item ID and exact allowed file set
- record implementation summary
- record Claude Code review-only verdict
- route to Claude Web/external review if the item unexpectedly touches high-risk semantics, broadens scope, or claims readiness
- run item-targeted tests
- run `py -3 scripts\git_preflight.py --mode all`
- update `releases\release_manifest.json` from PENDING to PASS only after full gate PASS
- stage only exact allowed implementation/test files plus governed closeout docs/rolling maps/manifest
- commit and push only after PASS, exact scope, and no-HOLD checks

## 9. Standing Exclusions

This preauthorization does not authorize:

- unlisted implementation
- files outside the selected item scope
- dependency changes
- fixture creation or modification
- runtime/API/schema changes
- release script changes
- contract changes
- AI_COLLAB changes
- public endpoint work
- launch execution
- production deployment
- external pilot execution or readiness
- real customer/operator sign-off
- credential handling by AI
- real-data handling
- evidence retention, replay, deletion, expiry, or evidence-pack behavior
- redaction policy freeze
- S5-B reopen
- S5-D reopen
- ORDIV reopen/report/CSV/L1B work
- S4-A resolver order or authority changes
- Red-3 action
- AdsPower profile creation/switching or Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection
- Claude Code file edits, command execution, tests, staging, commit, or push

## 10. Global HOLD Conditions

HOLD any listed Yellow item if:

- exact scope is unclear
- an allowed file list is insufficient
- a required test fails and the fix needs an excluded file
- any Red trigger appears
- any public endpoint, runtime/API/schema, real-data, credential, launch, deployment, external pilot, S5-B/S5-D, ORDIV, Red-3, S4-A resolver, or AI_COLLAB path is needed
- Claude Code review-only returns FAIL, HOLD, malformed verdict, file mutation, web request, permission surprise, or ambiguity
- full gate fails without a bounded in-scope fix
- network ambiguity affects review, package, git push, or any non-idempotent action

## 11. Acceptance Criteria

This preauthorization package is acceptable when:

- every item has exact allowed files
- every item has exact allowed behavior
- every item has exact required tests
- every item has item-specific HOLD conditions
- the package defines one-item-at-a-time execution
- the package defines review, full gate, release, manifest, stage, commit, and push constraints
- the package excludes public endpoint, runtime/API/schema, real data, credentials, launch, deployment, external pilot, S5-B/S5-D, ORDIV, Red-3, S4-A resolver, and AI_COLLAB work
- the paired stream review refresh closes with PASS before this preauthorization is used
