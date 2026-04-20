# S5-C-IMPL-6 Close Reason Internal Semantics Scoped Implementation Ticket

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S5-C-IMPL-6 Close Reason Internal Semantics Scoped Implementation Ticket |
| Status | Draft governed docs-only scoped implementation ticket |
| Scope | Define a later Yellow implementation ticket for internal close reason taxonomy semantics only |
| Snapshot | S5C-IMPL6-CLOSE-REASON-INTERNAL-SEMANTICS-TICKET-2026-04-20-001 |
| Stage | s5c-impl6-close-reason-internal-semantics-ticket |
| Baseline commit | `b177f5eee17048601264668460cc26ae18618ef5` |
| Baseline snapshot | S5C-NEXT-SCOPED-IMPLEMENTATION-TICKET-PREP-2026-04-20-001 |
| Baseline stage | s5c-next-scoped-implementation-ticket-prep |
| Baseline manifest status | PASS |
| Baseline release sha256 | `bb9415c6bcee966099ec00f93fa0686df575fef7578478a16eb5a4ed61c5fc1c` |
| Route opened by | Human product/governance prompt `OPEN_S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_TICKET` |
| Lane of this document | Green docs-only scoped implementation ticket definition |
| Lane of later implementation | Yellow implementation, HOLD until required review and explicit human GO |
| Required review before implementation | Claude Code review-only plus Claude Web or human-supervised external review |

This document defines a possible later implementation ticket. It does not implement code, modify tests, create fixtures, update dependencies, change runtime/API/schema behavior, alter contracts, modify release scripts, or authorize launch, deployment, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB changes.

Allowed future file scope is a boundary, not approval to begin work. No file listed in this document may be edited until a later implementation prompt or governed decision records required review evidence, exact file scope, explicit human GO, and rollback/HOLD criteria.

## 2. Startup And Baseline Verification

Autonomous startup checks for this stage:

- `docs\DELEGATED_APPROVER_CHARTER.md` was readable.
- `delegation_expires` is `2026-05-06 23:59 Asia/Shanghai`, which has not passed at draft time.
- The current branch is `codex/s3-a-runtime`.
- Baseline commit is `b177f5eee17048601264668460cc26ae18618ef5`.
- Baseline manifest snapshot is `S5C-NEXT-SCOPED-IMPLEMENTATION-TICKET-PREP-2026-04-20-001`.
- Baseline manifest verification status is `PASS`.
- Baseline release sha256 is `bb9415c6bcee966099ec00f93fa0686df575fef7578478a16eb5a4ed61c5fc1c`.
- The only known out-of-scope untracked files are `CLAUDE.md` and `SecuPilot_阶段性总结_20260409.md`; this stage does not touch them.

The governed ticket-prep baseline selected:

```text
OPEN_S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_TICKET
```

Meaning:

- Define exact future implementation scope for internal S5-C close reason taxonomy validation.
- Keep public close-case endpoint work deferred.
- Preserve S5-C-IMPL-5 action-request and lifecycle guarantees.
- HOLD rather than broaden scope if implementation requires runtime/API/schema, public endpoint, evidence, real-data, or external-system behavior.

## 3. Governed Inputs

This ticket is based on these governed source artifacts:

- `docs\S5C2_CLOSE_REASON_AND_LIFECYCLE_SEMANTICS.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_TICKET.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_CODE_TEST_TICKET.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_CLOSEOUT.md`
- `docs\S5C_NEXT_SCOPED_IMPLEMENTATION_TICKET_PREP.md`

Read-only code/test baseline checked:

- `backend\app\tools\persistent_case.py`
- `backend\tests\test_case_lifecycle_regression.py`
- `backend\tests\test_case_store.py`
- `backend\tests\test_case_action_request_contract.py`

No code or test file is changed by this document.

## 4. Current Implementation Reality

Current S5-C baseline already includes:

- governed case lifecycle status vocabulary: `open`, `in_review`, `approved`, `closed`
- governed action request status vocabulary: `draft`, `pending_approval`, `approved`, `rejected`, `cancelled`
- `case_closed` lifecycle audit event support
- `transition_persistent_case_status()` with free-form `reason` and optional audit `details`
- closed-case protections that reject action-request create, submit, approve, reject, and cancel mutations
- synthetic regression tests for lifecycle, store round-trip, and action-request contract behavior

Current baseline does not yet implement the S5-C-2 close reason taxonomy as a locked internal helper vocabulary. That is the only implementation gap this ticket may later address.

## 5. Future Implementation Scope

The later implementation ticket is allowed to touch only these files:

| File | Allowed role | Required constraints |
| --- | --- | --- |
| `backend\app\tools\persistent_case.py` | Add internal close reason type, vocabulary, validator, and optional close helper that records close reason in existing audit `details`. | No new lifecycle status, no new action-request status, no public endpoint coupling, no runtime/API/schema behavior, no persisted dataclass field unless separately reviewed. |
| `backend\tests\test_case_lifecycle_regression.py` | Add synthetic lifecycle tests for allowed and rejected close reasons. | Must preserve existing lifecycle and audit assertions. No endpoint, fixture, real-data, or external pilot tests. |
| `backend\tests\test_case_store.py` | Add synthetic serialization round-trip tests for close reason audit details if the helper records them. | Must not create fixtures or new persisted model fields. |
| `backend\tests\test_case_action_request_contract.py` | Optional only if the future patch touches closure behavior where unresolved action requests exist. | Must preserve S5-C-IMPL-5 non-destructive action-request guarantees and closed-case mutation blocks. |

The later implementation ticket must not touch:

- `backend\app\runtime_service.py`
- `backend\app\main.py`
- dependency files
- fixture files
- release scripts
- contract files
- `docs\AI_COLLAB_OPERATING_MODEL.md` or any AI_COLLAB file
- any file outside the listed allowed implementation/test scope, except docs and manifest artifacts for that later stage closeout

If implementation requires any excluded file, the later ticket must HOLD and request a separate governed route.

Importing, wiring, or exposing the new helper through `backend\app\runtime_service.py`, `backend\app\main.py`, or any other runtime/API path is out of scope for S5-C-IMPL-6. The later Yellow implementation may test internal helper behavior directly, but any runtime import, public route, API method/path, request/response/error model, or schema exposure requires a separate governed route and explicit human GO.

The optional `backend\tests\test_case_action_request_contract.py` inclusion decision must be made and recorded by the later implementation ticket or the explicit human GO. If that record does not say whether unresolved action-request closure interactions are touched, the optional file remains out of scope and implementation must HOLD before editing it.

## 6. Required Future Behavior

The later implementation may add a bounded internal close reason helper path:

- Add `CaseCloseReason` or equivalent internal type bounded to S5-C-2 taxonomy.
- Add a frozen internal vocabulary and read-only accessor such as `governed_case_close_reasons()`.
- Add a validator such as `_require_case_close_reason(value)` that raises deterministic `ValueError("invalid_case_close_reason:<value>")` for unknown values.
- Add or route through an internal helper such as `close_persistent_case(...)` only if that helper:
  - validates `close_reason`
  - transitions to existing lifecycle status `closed`
  - records `case_closed` in existing lifecycle audit behavior
  - stores the close reason only in existing audit `details`, for example `{"close_reason": close_reason}`
  - preserves caller-provided non-sensitive details only when explicitly scoped
  - does not rewrite prior audit entries
  - does not add a persisted dataclass field
  - does not expose public endpoint, runtime, API, or schema behavior

The governed S5-C-2 close reason vocabulary is:

- `resolved_false_positive`
- `resolved_expected_activity`
- `resolved_contained`
- `duplicate_case`
- `insufficient_evidence`
- `out_of_scope`
- `deferred_to_external_process`

The later implementation must preserve:

- lifecycle vocabulary `open`, `in_review`, `approved`, `closed`
- action-request vocabulary `draft`, `pending_approval`, `approved`, `rejected`, `cancelled`
- action-request approval as review data only, not execution
- rejection and cancellation as history-preserving decisions
- closed-case safety
- public close-case endpoint `KEEP_DEFERRED`
- S4-A resolver order `asset_id -> hostname -> fqdn -> ip_address -> aliases`

## 7. Required Future Tests

The later implementation must include or preserve tests that prove:

- `governed_case_close_reasons()` or equivalent returns exactly the seven S5-C-2 close reasons and no additional values.
- Unknown close reason values are rejected by the new internal helper path with deterministic error text.
- Valid close reasons close the case with `lifecycle_status == "closed"`.
- The final audit event remains `case_closed`.
- Audit `details`, if used, contain only bounded non-sensitive close reason metadata.
- Serialization round-trip preserves the close reason audit metadata without adding a new persisted field.
- Existing lifecycle status and action-request status vocabularies remain unchanged.
- Existing closed-case action-request mutation blocks remain intact.
- No runtime/API/schema/public endpoint behavior changes are introduced.

Candidate future commands:

- `py -3 -m unittest -q backend.tests.test_case_lifecycle_regression`
- `py -3 -m unittest -q backend.tests.test_case_store`
- `py -3 -m unittest -q backend.tests.test_case_action_request_contract`
- `py -3 scripts\git_preflight.py --mode all`

The later implementation ticket must decide whether `backend.tests.test_case_action_request_contract` is mandatory based on whether unresolved action-request closure interactions are touched. Full gate remains mandatory before any implementation closeout commit.

## 8. Review And GO Required Before Implementation

This ticket does not grant implementation authority.

Before code/test work begins, the later implementation requires:

1. Claude Code review-only verdict for the exact scoped implementation plan.
2. Claude Web or human-supervised external review for lifecycle/close semantics.
3. Explicit human product/governance GO for Yellow implementation.
4. Exact file scope and test command list in the GO or governed ticket.
5. Clear rollback/HOLD criteria.
6. Full gate and release verification before any closeout commit.

Reviewer PASS is evidence only. It is not implementation authority.

Silence, inferred consent, ambiguous lane, missing file scope, missing review evidence, expired approval, unresolved HOLD, or a request to touch excluded files means implementation remains HOLD.

## 9. HOLD Conditions

HOLD if any future action attempts to:

- implement code or tests before explicit human GO
- touch files outside the allowed future implementation/test scope
- add public close-case endpoint work or weaken `KEEP_DEFERRED`
- change `backend\app\runtime_service.py` or `backend\app\main.py`
- add runtime/API/schema behavior
- add public method/path/request/response/error model
- add new persisted lifecycle status or action-request status
- add close reason as real customer/operator sign-off
- add evidence retention, replay, deletion, expiry, evidence-pack behavior, or redaction policy freeze
- introduce raw customer/operator data or unredacted evidence
- handle credentials, tokens, API keys, auth headers, cookies, sessions, or secrets
- imply external pilot readiness or execution
- reopen S5-B or S5-D without separate governed reopen decision
- reopen ORDIV work without separate governed route
- change S4-A resolver order or authority
- perform Red-3 action
- modify AI_COLLAB
- use Claude Code for file edits, command execution, tests, staging, commit, or push
- use AdsPower for login automation, profile creation/switching, session inspection, or browser-storage/profile-file inspection

## 10. Non-Authorization

This docs-only scoped implementation ticket does not authorize:

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

## 11. Acceptance Criteria

This docs-only ticket is acceptable when:

- the current governed PASS baseline is recorded
- future implementation lane is Yellow and HOLD until review plus explicit human GO
- exact allowed future implementation/test files are listed
- exact excluded files are listed, including `backend\app\runtime_service.py` and `backend\app\main.py`
- exact S5-C-2 close reason vocabulary is listed
- future behavior is restricted to internal helper semantics and existing audit `details`
- public close-case endpoint remains `KEEP_DEFERRED`
- S5-C-IMPL-5 action-request guarantees are preserved
- inherited boundaries remain preserved
- rolling maps are updated as passive context
- `docs\HANDOFF.md` records this stage
- `releases\release_manifest.json` records the new snapshot/stage in draft state
- manifest `current_release_sha256` remains `null`
- manifest verification fields remain `PENDING_FULL_GATE_AFTER_REVIEW` until full gate PASS
- for this S5-C-IMPL-6 manifest draft, `releases\release_manifest.json` path fields follow the existing Windows source-of-truth manifest convention for this repository and do not authorize changing release tooling semantics
- no code/test/dependency/fixture/runtime/API/schema/release-script/contract/AI_COLLAB files are modified
- known out-of-scope untracked files remain untouched and unstaged

## 12. Preliminary Recommendation

```text
PRELIMINARY_RECOMMENDATION_READY_FOR_SEPARATE_S5C_IMPL6_YELLOW_IMPLEMENTATION_GO
```

Meaning:

- The implementation scope is narrow enough for a later Yellow implementation GO.
- The later implementation must be limited to internal close reason taxonomy validation, bounded audit details, and synthetic tests.
- Public close-case endpoint remains deferred.
- Implementation remains HOLD until required review, explicit human GO, full gate, release verification, and governed closeout.
