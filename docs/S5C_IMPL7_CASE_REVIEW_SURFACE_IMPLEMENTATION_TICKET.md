# S5-C-IMPL-7 Case Review Surface Scoped Implementation Ticket

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S5-C-IMPL-7 Case Review Surface Scoped Implementation Ticket |
| Status | Draft governed docs-only scoped implementation ticket |
| Scope | Define a Yellow implementation ticket for internal case review guidance inside the existing case view read model |
| Snapshot | S5C-IMPL7-CASE-REVIEW-SURFACE-IMPLEMENTATION-TICKET-2026-04-20-001 |
| Stage | s5c-impl7-case-review-surface-implementation-ticket |
| Baseline commit | `46af57c3e8fd773ec7d8dc99c25169041672248a` |
| Baseline snapshot | S5C-IMPL7-CASE-REVIEW-SURFACE-TICKET-PREP-2026-04-20-001 |
| Baseline stage | s5c-impl7-case-review-surface-ticket-prep |
| Baseline manifest status | PASS |
| Baseline release sha256 | `f332304af953a2883d34c3017098eadab092b9c8b652dc4f4da249ccc4dc1282` |
| Route opened by | Human product/governance prompt `OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_IMPLEMENTATION_TICKET` |
| Lane of this document | Green docs-only scoped implementation ticket definition |
| Lane of later implementation | Yellow implementation, authorized only after this ticket closes PASS and the recorded GO applies |
| Required review before implementation | Claude Code review-only for this ticket; implementation review before closeout |

This document defines a later Yellow implementation ticket. It does not itself implement code, modify tests, create fixtures, update dependencies, change runtime/API/schema behavior, alter contracts, modify release scripts, or authorize launch, deployment, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB changes.

The `IMPL7` label is a planning/ticket sequence label only. It does not authorize implementation outside the exact scope below.

## 2. Startup And Baseline Verification

Autonomous startup checks for this stage:

- `docs\DELEGATED_APPROVER_CHARTER.md` was readable.
- `delegation_expires` is `2026-05-06 23:59 Asia/Shanghai`, which has not passed at draft time.
- The current branch is `codex/s3-a-runtime`.
- Baseline commit is `46af57c3e8fd773ec7d8dc99c25169041672248a`.
- Baseline manifest snapshot is `S5C-IMPL7-CASE-REVIEW-SURFACE-TICKET-PREP-2026-04-20-001`.
- Baseline manifest verification status is `PASS`.
- Baseline release sha256 is `f332304af953a2883d34c3017098eadab092b9c8b652dc4f4da249ccc4dc1282`.
- The only known out-of-scope untracked files are `CLAUDE.md` and `SecuPilot_阶段性总结_20260409.md`; this stage does not touch them.

## 3. Governed Inputs

This ticket is based on these governed source artifacts:

- `docs\S5C_IMPL7_CASE_REVIEW_SURFACE_TICKET_PREP.md`
- `docs\NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION.md`
- `docs\S5C1_CASE_WORKFLOW_JOURNEY_CONTRACT.md`
- `docs\S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`
- `docs\S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`
- `docs\S5C5_CASE_WORKFLOW_REVIEW_PASS.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_CLOSEOUT.md`
- `docs\S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_IMPLEMENTATION_CLOSEOUT.md`

Read-only code/test baseline checked:

- `backend\app\agents\case_view.py`
- `backend\tests\test_case_view.py`
- `backend\app\tools\persistent_case.py` for current `case_view` storage usage only
- `backend\tests\test_runtime_service.py` for current payload assertion context only

No code or test file is changed by this document.

## 4. Current Implementation Reality

Current `build_case_view()` output already includes:

- `executive_summary`
- `what_happened`
- `why_it_matters`
- `jarvis_plan`
- `recommended_action`
- `evidence_panels`
- `analysis_limits`

Current `analysis_limits` already carries degraded reasons, missing telemetry, unavailable tools, unresolved pivots, and disabled action reason. It is the safest existing internal panel for bounded review guidance because it can add review cues without creating a new top-level case view panel, changing runtime routes, or touching persistence schema.

## 5. Yellow Implementation Scope

The later Yellow implementation is allowed to touch only these files:

| File | Allowed role | Required constraints |
| --- | --- | --- |
| `backend\app\agents\case_view.py` | Add bounded internal review guidance under `analysis_limits["review_guidance"]`. | No new top-level case view panel, no runtime/API/schema behavior, no public endpoint coupling, no persistence schema change, no lifecycle/action-request status change, no real data handling. |
| `backend\tests\test_case_view.py` | Add synthetic tests for review guidance shape, safe analyst/manager cues, degraded/partial behavior, and non-execution semantics. | Must preserve existing top-level case view contract shape assertions. No endpoint, fixture, real-data, or external pilot tests. |

The implementation must not touch:

- `backend\tests\test_runtime_service.py`
- `backend\app\runtime_service.py`
- `backend\app\main.py`
- public endpoint/API/schema files
- `backend\app\tools\persistent_case.py`
- dependency files
- fixture files
- release scripts
- contract files
- `docs\AI_COLLAB_OPERATING_MODEL.md` or any AI_COLLAB file
- any file outside the listed implementation/test scope, except docs and manifest artifacts for implementation closeout

If implementation requires any excluded file, the implementation must HOLD and request a separate governed route.

## 6. Required Implementation Behavior

The Yellow implementation may add `analysis_limits["review_guidance"]` with these exact internal fields:

- `review_context`
- `manager_decision_context`
- `analyst_questions`
- `audit_focus`

Required semantics:

- `review_context` must summarize investigation status, whether analyst review is recommended, whether manager review is relevant, and `execution_authorized: False`.
- `manager_decision_context` must summarize action type, targets, approval requirement, disabled reason, and `execution_authorized: False` from existing `recommended_action` only.
- `analyst_questions` must be a bounded synthetic list derived from existing missing telemetry, degraded/partial state, action availability, and primary-chain presence. It must not include raw event bodies or real evidence.
- `audit_focus` must be a bounded list of references such as `persistent_case.lifecycle_status`, `persistent_case.action_requests`, and `persistent_case.lifecycle_audit`; it must not change audit storage or reconstruct audit data.
- The implementation must not add new top-level case view panels.
- The implementation must not alter `CASE_VIEW_SCHEMA_VERSION`.
- The implementation must not add persisted dataclass fields, lifecycle statuses, action-request statuses, database schema, runtime service routes, public endpoints, or request/response models.
- Approval or manager decision context remains review data only and never destructive response execution authority.

## 7. Required Tests

The Yellow implementation must include or preserve tests that prove:

- the existing top-level case view panel set remains unchanged
- `analysis_limits["review_guidance"]` exists for complete cases
- manager decision context identifies recommended action review without authorizing execution
- degraded cases produce safe review guidance and keep action execution unauthorized
- partial cases include missing-telemetry review questions
- no-action cases remain unavailable rather than disabled unless degraded
- audit focus entries are references only and do not duplicate audit/evidence payloads
- no runtime/API/schema/public endpoint behavior changes are introduced

Required commands after implementation:

- `py -3 -m unittest -q backend.tests.test_case_view`
- `py -3 scripts\git_preflight.py --mode all`

`backend.tests.test_runtime_service` is covered by full gate but must not be edited by this implementation.

## 8. Yellow Implementation GO Record

Human product/governance prompt supplied:

```text
打开并授权：OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_IMPLEMENTATION_TICKET，然后给 Yellow implementation GO。
```

This GO is accepted only under these constraints:

- it applies only after this scoped implementation ticket closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push
- it applies only to `backend\app\agents\case_view.py` and `backend\tests\test_case_view.py`
- it authorizes only the behavior in Section 6
- it requires the tests in Section 7
- it expires if any HOLD condition in Section 9 occurs

This GO does not authorize launch, deployment, external pilot, public endpoint work, runtime/API/schema changes, real data, credentials, S5-B/S5-D reopen, ORDIV work, Red-3 action, AI_COLLAB changes, staging, commit, or push outside the normal implementation closeout rules.

Yellow GO blocking checklist:

- HOLD if this ticket does not close with review PASS, full gate PASS, release verification PASS, closeout commit, and push.
- HOLD if any implementation file outside `backend\app\agents\case_view.py` or `backend\tests\test_case_view.py` is needed.
- HOLD if implementation needs `backend\tests\test_runtime_service.py`, `backend\app\runtime_service.py`, `backend\app\main.py`, public endpoint/API/schema files, or `backend\app\tools\persistent_case.py`.
- HOLD if the patch needs a new top-level case view panel or `CASE_VIEW_SCHEMA_VERSION` change.
- HOLD if runtime/API/schema behavior, persistence schema, lifecycle status, action-request status, or case store behavior must change.
- HOLD if review/manager guidance could be interpreted as destructive response execution authority.
- HOLD if targeted tests or full gate fail without a bounded in-scope fix.
- HOLD if real data, credentials, evidence retention, public endpoint work, S5-B/S5-D, ORDIV, Red-3, or AI_COLLAB becomes necessary.

## 9. HOLD Conditions

HOLD if any implementation action attempts to:

- touch files outside `backend\app\agents\case_view.py` and `backend\tests\test_case_view.py`
- edit `backend\tests\test_runtime_service.py`
- edit `backend\app\runtime_service.py`, `backend\app\main.py`, public endpoint/API/schema files, or `backend\app\tools\persistent_case.py`
- add a new top-level case view panel
- alter `CASE_VIEW_SCHEMA_VERSION`
- change runtime/API/schema behavior
- add public method/path/request/response/error model
- change persistence schema, durable case dataclass fields, lifecycle status vocabulary, action-request status vocabulary, or case store behavior
- treat workflow roles as RBAC or authorization infrastructure
- treat approval/denial context as destructive execution
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

- implementation before this ticket closes PASS and the recorded GO applies
- files outside `backend\app\agents\case_view.py` and `backend\tests\test_case_view.py`
- dependency changes
- fixture creation or modification
- runtime/API/schema changes
- release script changes
- contract changes
- AI_COLLAB changes
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
- Yellow implementation scope is limited to `backend\app\agents\case_view.py` and `backend\tests\test_case_view.py`
- exact excluded files are listed
- exact `analysis_limits["review_guidance"]` behavior is defined
- no new top-level case view panel is authorized
- no runtime/API/schema/public endpoint behavior is authorized
- required tests are listed
- the human Yellow GO is recorded with constraints
- inherited boundaries remain preserved
- rolling maps are updated as passive context
