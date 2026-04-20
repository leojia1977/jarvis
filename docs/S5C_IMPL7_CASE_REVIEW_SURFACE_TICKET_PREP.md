# S5-C-IMPL-7 Case Review Surface Ticket Prep

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S5-C-IMPL-7 Case Review Surface Ticket Prep |
| Status | Draft governed docs-only ticket-prep stage |
| Scope | Prepare a possible later Yellow implementation ticket for internal case review surface/read-model hardening |
| Snapshot | S5C-IMPL7-CASE-REVIEW-SURFACE-TICKET-PREP-2026-04-20-001 |
| Stage | s5c-impl7-case-review-surface-ticket-prep |
| Baseline commit | `7af8841a10685c0420fdea8c3a6bddef2c207f51` |
| Baseline snapshot | S5-NEXT-PRODUCT-DEVELOPMENT-ROUTE-SELECTION-2026-04-20-001 |
| Baseline stage | s5-next-product-development-route-selection |
| Baseline manifest status | PASS |
| Baseline release sha256 | `bddecafb75f0dfde2aa46a37e407afbdbcc69ae1499728f267bcb93101f2513b` |
| Route opened by | Human product/governance prompt `OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_TICKET_PREP` |
| Lane of this document | Green docs-only ticket prep |
| Lane of later implementation | Yellow implementation, HOLD until scoped ticket review and explicit GO |
| Required review before implementation | Claude Code review-only plus Claude Web or human-supervised external review if case view contract shape changes |

This document prepares a possible later implementation ticket. It does not implement code, modify tests, create fixtures, update dependencies, change runtime/API/schema behavior, alter contracts, modify release scripts, or authorize launch, deployment, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB changes.

The `IMPL7` label is a planning/ticket sequence label only. It does not constitute an implementation GO. A separate Yellow implementation review gate and explicit GO are required before any code or test changes.

## 2. Startup And Baseline Verification

Autonomous startup checks for this stage:

- `docs\DELEGATED_APPROVER_CHARTER.md` was readable.
- `delegation_expires` is `2026-05-06 23:59 Asia/Shanghai`, which has not passed at draft time.
- The current branch is `codex/s3-a-runtime`.
- Baseline commit is `7af8841a10685c0420fdea8c3a6bddef2c207f51`.
- Baseline manifest snapshot is `S5-NEXT-PRODUCT-DEVELOPMENT-ROUTE-SELECTION-2026-04-20-001`.
- Baseline manifest verification status is `PASS`.
- Baseline release sha256 is `bddecafb75f0dfde2aa46a37e407afbdbcc69ae1499728f267bcb93101f2513b`.
- The only known out-of-scope untracked files are `CLAUDE.md` and `SecuPilot_阶段性总结_20260409.md`; this stage does not touch them.

The governed route-selection baseline selected:

```text
OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_TICKET_PREP
```

The `IMPL7` sequence label in this route name is non-authorizing. It is not a Yellow implementation GO and must not be used to infer permission for code or test changes.

Meaning:

- Prepare a future scoped implementation ticket for case review surface/read-model hardening.
- Decide whether a later Yellow implementation can be bounded to existing internal case view shaping.
- Preserve public close-case endpoint `KEEP_DEFERRED`.
- HOLD rather than broaden scope if implementation requires runtime/API/schema, persistence schema, real data, credentials, evidence retention, or external-system behavior.

## 3. Governed Inputs

This ticket-prep stage is based on these governed source artifacts:

- `docs\NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION.md`
- `docs\S5C_CASE_WORKFLOW_HARDENING_PLAN.md`
- `docs\S5C1_CASE_WORKFLOW_JOURNEY_CONTRACT.md`
- `docs\S5C2_CLOSE_REASON_AND_LIFECYCLE_SEMANTICS.md`
- `docs\S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`
- `docs\S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`
- `docs\S5C5_CASE_WORKFLOW_REVIEW_PASS.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_CLOSEOUT.md`
- `docs\S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_IMPLEMENTATION_CLOSEOUT.md`

Read-only code/test baseline checked:

- `backend\app\agents\case_view.py`
- `backend\tests\test_case_view.py`

Read-only usage baseline checked:

- `backend\app\agents\graph.py` uses `build_case_view()` to attach `case_view` to generated case payloads.
- `backend\app\tools\persistent_case.py` stores `case_view` in durable case records with `CASE_VIEW_SCHEMA_VERSION = "3.1"`.
- Existing tests assert `case_view` shape in `backend\tests\test_case_view.py`, persistent case tests, lifecycle tests, runtime tests, and draft regression tests.

No code or test file is changed by this document.

## 4. Current Implementation Reality

Current case view baseline already includes:

- top-level panels `executive_summary`, `what_happened`, `why_it_matters`, `jarvis_plan`, `recommended_action`, `evidence_panels`, and `analysis_limits`
- `executive_summary.status_banner` for degraded and partial investigations
- `jarvis_plan.scope`, `stop_conditions`, and `next_suggested`
- `recommended_action.action_state`, approval requirement, targets, and disabled reason
- evidence reference panels for top chains, IOC table, persistence, and evidence gaps
- analysis limits for degraded reasons, missing telemetry, unavailable tools, unresolved pivots, and disabled action reason
- synthetic unit tests freezing current panel shape and degraded/partial/no-action behavior

Current baseline does not yet define an explicit internal analyst/manager review surface that groups review readiness, human decision context, lifecycle/action-request references, and safe next-review prompts without changing runtime/API/public endpoint behavior. That is the only future candidate this ticket-prep stage may prepare.

## 5. Candidate Future Implementation Scope

The later implementation ticket may be proposed only if it can be bounded to these files:

| File | Candidate role | Required constraints |
| --- | --- | --- |
| `backend\app\agents\case_view.py` | Add internal review-surface/read-model helper semantics inside the existing `build_case_view()` output. | No runtime/API/schema behavior, no public endpoint coupling, no persistence schema change, no new lifecycle or action-request status, no real data handling. |
| `backend\tests\test_case_view.py` | Add synthetic tests for the bounded review surface shape, safe manager/analyst cues, degraded/partial behavior, and existing panel compatibility. | Must preserve existing contract shape assertions or explicitly update them only within the future ticket scope. |
| `backend\tests\test_runtime_service.py` | Optional only if the later ticket explicitly decides existing runtime payload assertions must be protected. | The later ticket must restate this condition exactly before including this file. If the condition cannot be stated, this file remains excluded. |

The later implementation ticket must not touch:

- `backend\app\runtime_service.py`
- `backend\app\main.py`
- public endpoint/API/schema files
- `backend\app\tools\persistent_case.py` unless a later route separately governs case view schema-version or persistence behavior
- dependency files
- fixture files
- release scripts
- contract files
- `docs\AI_COLLAB_OPERATING_MODEL.md` or any AI_COLLAB file
- any file outside the listed candidate implementation/test scope, except docs and manifest artifacts for that later stage closeout

If implementation requires any excluded file, the later ticket must HOLD and request a separate governed route.

## 6. Candidate Future Behavior

The later implementation ticket may propose a bounded internal case review surface only if it:

- reuses existing case input data already available to `build_case_view()`
- preserves existing top-level case view panels unless the later ticket explicitly scopes and reviews a contract-shape change
- adds no public HTTP endpoint, request model, response model, or schema artifact
- adds no runtime service method or route
- adds no persisted dataclass field, lifecycle status, action-request status, or database schema
- treats analyst, manager, operator, and reviewer as descriptive workflow roles only, not RBAC or authorization infrastructure
- presents approval/denial context as review data only, never destructive execution authority
- preserves closed-case safety and S5-C-IMPL-6 close reason semantics
- uses synthetic test cases only
- stores no real customer/operator evidence, secrets, credentials, cookies, sessions, tokens, auth headers, browser storage, or profile-file material

Candidate review surface fields may include, if later reviewed and approved:

- `review_context` summarizing descriptive actor, lifecycle status, and whether manager review is relevant
- `manager_decision_context` summarizing action-request review cues without authorizing execution
- `analyst_questions` or equivalent safe prompts derived from existing evidence gaps and action availability
- `audit_focus` or equivalent references to existing lifecycle/action-request audit concepts without changing audit storage

These names are illustrative planning candidates only. They are not locked, pre-approved, or authorized by this ticket-prep stage. The later scoped ticket must independently review each proposed name, shape, current behavior, proposed behavior, and boundary impact before any name is treated as a commitment or implementation target.

## 7. Required Future Tests

The later implementation ticket must include or preserve tests that prove:

- existing top-level case view panel shape remains stable unless the later ticket explicitly scopes a reviewed shape change
- the new review surface is populated from existing synthetic case data only
- degraded and partial cases produce safe review guidance without enabling action execution
- no-action cases remain unavailable rather than disabled unless degraded
- manager decision context does not imply destructive response execution
- evidence panel references remain references and do not duplicate raw evidence
- optional runtime payload assertions are protected only if `backend\tests\test_runtime_service.py` is explicitly included by the later ticket
- no runtime/API/schema/public endpoint behavior changes are introduced

Candidate future commands:

- `py -3 -m unittest -q backend.tests.test_case_view`
- `py -3 -m unittest -q backend.tests.test_runtime_service` only if `backend\tests\test_runtime_service.py` is explicitly included by the later ticket
- `py -3 scripts\git_preflight.py --mode all`

## 8. Review And GO Required Before Implementation

This ticket-prep stage does not grant implementation authority.

Before any code/test work begins, the later implementation requires:

1. A scoped implementation ticket that freezes exact behavior, exact files, test plan, and HOLD criteria.
2. Claude Code review-only verdict for the exact scoped implementation plan.
3. Claude Web or human-supervised external review if the case view contract shape changes, analyst/manager workflow semantics are frozen, or runtime payload assertions are affected.
4. Explicit human product/governance GO for Yellow implementation.
5. Full gate and release verification before any implementation closeout commit.

Reviewer PASS is evidence only. It is not implementation authority.

Silence, inferred consent, ambiguous lane, missing file scope, missing review evidence, expired approval, unresolved HOLD, or a request to touch excluded files means implementation remains HOLD.

## 9. HOLD Conditions

HOLD if any future action attempts to:

- implement code or tests before explicit human GO
- touch files outside the allowed future implementation/test scope
- change `backend\app\runtime_service.py` or `backend\app\main.py`
- add public close-case endpoint work or weaken `KEEP_DEFERRED`
- add runtime/API/schema behavior
- add public method/path/request/response/error model
- change persistence schema, durable case dataclass fields, lifecycle status vocabulary, action-request status vocabulary, or case store behavior
- alter `CASE_VIEW_SCHEMA_VERSION` without a separate governed schema-version decision
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

This docs-only ticket-prep stage does not authorize:

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

This docs-only ticket-prep stage is acceptable when:

- the current governed PASS baseline is recorded
- future implementation lane is Yellow and HOLD until scoped ticket review plus explicit human GO
- exact candidate future files are listed
- exact excluded files are listed, including `backend\app\runtime_service.py` and `backend\app\main.py`
- `backend\tests\test_runtime_service.py` is optional only under the explicit carry-forward condition
- current case view reality is summarized from read-only code/test inspection
- candidate future behavior is restricted to internal review-surface/read-model semantics
- public close-case endpoint remains `KEEP_DEFERRED`
- S5-C-IMPL-5 and S5-C-IMPL-6 guarantees are preserved
- inherited boundaries remain preserved
- rolling maps are updated as passive context
