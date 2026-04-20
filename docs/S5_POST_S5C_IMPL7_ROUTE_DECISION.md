# Sprint 5 Post S5-C-IMPL-7 Route Decision

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Sprint 5 Post S5-C-IMPL-7 Route Decision |
| Status | Draft governed docs-only route decision |
| Scope | Select the next route after S5-C-IMPL-7 closeout and record autonomous vacation-mode implications |
| Snapshot | S5-POST-S5C-IMPL7-ROUTE-DECISION-2026-04-20-001 |
| Stage | s5-post-s5c-impl7-route-decision |
| Baseline commit | `7143b8b7fe3f22a68ee44a3596908925da44a7cf` |
| Baseline snapshot | S5-NEXT-PRODUCT-DEVELOPMENT-ROUTE-SELECTION-2026-04-20-002 |
| Baseline stage | s5-next-product-development-route-selection |
| Baseline manifest status | PASS |
| Baseline release sha256 | `5a0ae49d813ca2d5ea7fdf561ecf066edeb96a8d56e00a80e70463fa64157ade` |
| Route opened by | Human product/governance prompt `OPEN_POST_S5C_IMPL7_ROUTE_DECISION_STAGE` |
| Lane | Green docs-only route decision |
| Required review | Claude Code review-only unless a reviewer or human requests Claude Web/external review |

This stage reviews the governed state after S5-C-IMPL-5, S5-C-IMPL-6, and S5-C-IMPL-7 implementation closeouts. It chooses the next product-development route without authorizing implementation, runtime/API/schema changes, launch, deployment, external pilot execution, real-data handling, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB changes.

## 2. Startup And Baseline Verification

Autonomous startup checks for this stage:

- `docs\DELEGATED_APPROVER_CHARTER.md` was readable.
- `delegation_expires` is `2026-05-06 23:59 Asia/Shanghai`, which has not passed at draft time.
- The current branch is `codex/s3-a-runtime`.
- Baseline commit is `7143b8b7fe3f22a68ee44a3596908925da44a7cf`.
- Baseline manifest snapshot is `S5-NEXT-PRODUCT-DEVELOPMENT-ROUTE-SELECTION-2026-04-20-002`.
- Baseline manifest verification status is `PASS`.
- Baseline release sha256 is `5a0ae49d813ca2d5ea7fdf561ecf066edeb96a8d56e00a80e70463fa64157ade`.
- The only known out-of-scope untracked files are pre-existing local files; this stage does not touch them.

The following governed context was loaded or checked before drafting:

- `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
- `docs\DELEGATED_APPROVER_CHARTER.md`
- `docs\AUTONOMOUS_DELIVERY_PIPELINE.md`
- `docs\AUTONOMOUS_HOLD_QUEUE.md`
- `docs\PRODUCT_STATE.md`
- `docs\ROADMAP_AND_PARKED_ITEMS.md`
- `docs\GOVERNANCE_DECISION_LOG.md`
- `docs\HANDOFF.md`
- `docs\NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION.md`
- `docs\S5C5_CASE_WORKFLOW_REVIEW_PASS.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_CLOSEOUT.md`
- `docs\S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_IMPLEMENTATION_CLOSEOUT.md`
- `docs\S5C_IMPL7_CASE_REVIEW_SURFACE_IMPLEMENTATION_CLOSEOUT.md`

## 3. S5-C State After IMPL7

Accepted implementation closeouts:

| Stream | Governed outcome | Still not authorized |
| --- | --- | --- |
| S5-C-IMPL-5 | Case lifecycle and action-request hardening is implemented and closed. | Additional lifecycle/action-request changes without a new scoped ticket. |
| S5-C-IMPL-6 | Internal close reason vocabulary validation and audit `details` semantics are implemented and closed. | Public close-case endpoint, runtime/API exposure, new persisted fields, new lifecycle/action-request statuses. |
| S5-C-IMPL-7 | Internal case review guidance under `analysis_limits["review_guidance"]` is implemented and closed. | New top-level case-view panels, runtime/API/schema behavior, public endpoint work, persistence changes. |

S5-C planning artifacts remain coherent:

- S5-C-1 journey language remains descriptive and does not create RBAC.
- S5-C-2 close reason semantics remain S4-C-compatible.
- S5-C-3 action-request semantics remain non-destructive.
- S5-C-4 public close-case endpoint remains `KEEP_DEFERRED`.
- S5-C-5 planning/contract review pass remains a planning baseline, not implementation authority.

No exact S5-C-IMPL8 implementation gap is safely named from the current baseline. Creating a new Yellow implementation ticket now would risk inventing scope rather than deriving it from a governed product need.

## 4. Vacation-Mode Automation Answer

The current autonomous workflow can reduce human involvement, but it must not become unbounded autonomous implementation.

What can run without repeated human assistance now:

- Green docs-only route decisions, planning docs, ticket prep, rolling-map updates, review-pack generation, full gate/package/release verification, manifest PASS updates after gate PASS, and Green docs-only commit/push under AHQ-019 when all standing conditions pass.
- Claude Code review-only evidence through the verified `claude.cmd` verdict-line path.
- Claude Web review-prompt transfer through the verified AdsPower configured-profile path, when the prompt contains no secrets, raw customer data, credentials, unredacted evidence, or high-risk login/session material.

What can run during vacation only after a precise preauthorization or delegated GO:

- Yellow implementation with exact files, exact behavior, exact tests, review path, rollback/HOLD criteria, and no Red trigger.
- Red-1 or allowed Red-2 preparation work only with complete `DELEGATED_APPROVER_GO` where policy requires it.
- Any product route that needs a human product choice before scope can be named.

What cannot be made fully unattended under the current governed baseline:

- launch execution
- production deployment
- external pilot execution
- real customer/operator sign-off
- raw credential or secret handling by AI
- real-data handling or unredacted evidence retention
- public endpoint activation
- S5-B/S5-D reopen without a separate governed reopen decision
- ORDIV report/CSV/L1B or real-data validation reopen without a separate governed route
- Red-3 actions
- AI_COLLAB changes outside a separate AI_COLLAB route

Practical vacation setup:

1. Keep the 2-hour autonomous ops loop active.
2. Let the loop automatically handle Green docs-only route/ticket/review/gate/closeout stages under AHQ-019.
3. Create a small preauthorized Yellow backlog only after each item has exact files, tests, acceptance criteria, review path, and HOLD rules.
4. Use jarvis as delegated approver only for policy-allowed Red-1/selected Red-2 preparation, never Red-3.
5. Accept that any missing product decision, high-risk route, real-data/credential issue, or ambiguous lane will HOLD rather than silently proceed.

This setup preserves development cadence while preventing accidental launch, data, credential, or irreversible production actions.

## 5. Candidate Routes

| Candidate route | Meaning | Lane | Current status | Risk | Decision |
| --- | --- | --- | --- | --- | --- |
| A. `OPEN_S5C_STREAM_REVIEW_REFRESH_STAGE` | Refresh the S5-C stream review after IMPL5/6/7 and decide whether S5-C is implementation-complete for now or has a named next gap. | Green docs-only | Allowed. | Low if it stays review/route only. | Selected. |
| B. `OPEN_S5C_IMPL8_SCOPED_IMPLEMENTATION_TICKET_PREP` | Prepare a new S5-C-IMPL8 ticket. | Green docs-only ticket prep | Not selected because no exact gap is named yet. | Medium: could invent scope. | HOLD until stream refresh identifies a precise need. |
| C. `OPEN_EXTERNAL_INPUT_TRACKER_REFRESH_DOCS_ONLY` | Refresh external pilot input status and blockers. | Green docs-only | Allowed later. | Could be mistaken for readiness if not bounded. | Not selected because S5-C state should be refreshed first. |
| D. `OPEN_AUTONOMOUS_YELLOW_BACKLOG_PREAUTH_STAGE` | Prepare a package of exact Yellow tasks that could run during human vacation without per-task human intervention. | Green docs-only preparation | Useful later after a stream refresh names candidate tasks. | Could become too broad if created without exact scopes. | Candidate after S5-C stream refresh. |
| E. `OPEN_S5C_YELLOW_IMPLEMENTATION_NOW` | Start another code/test implementation immediately. | Yellow implementation | Not allowed. | Missing exact ticket and GO. | HOLD. |
| F. `OPEN_PUBLIC_CLOSE_CASE_ENDPOINT_ROUTE` | Reopen deferred public close-case endpoint work. | Red/high-risk route | Blocked by `KEEP_DEFERRED` and AHQ-013. | Runtime/API/schema risk. | HOLD. |
| G. `OPEN_EXTERNAL_PILOT_DECISION_PACKAGE` | Draft or finalize L3/customer-trial decision package. | Red-1/Red-2 preparation | Blocked by AHQ-003/AHQ-011 unless inputs are governed. | Readiness/launch confusion. | HOLD. |
| H. `REOPEN_S5B_OR_S5D` | Reopen parked source/input or telemetry streams. | Conditional Red / Red-2 depending scope | Blocked by `PASS_AND_PARK` and AHQ-012. | Source/telemetry/real evidence risk. | HOLD. |
| I. `OPEN_ORDIV_REPORT_CSV_L1B_ROUTE` | Reopen ORDIV report, CSV, L1B, or real-data validation route. | Red-2 / Red-3-adjacent depending evidence | Blocked by ORDIV parked state and AHQ-014. | Real-data/evidence/report risk. | HOLD. |

## 6. Selected Next Route

Selected route:

```text
OPEN_S5C_STREAM_REVIEW_REFRESH_STAGE
```

Meaning:

- The next stage should be a Green docs-only S5-C stream review refresh.
- It should review S5-C planning plus IMPL5/6/7 implementation closeouts together.
- It should decide whether S5-C is complete/parked for now, whether a precise IMPL8 ticket-prep candidate exists, or whether an autonomous Yellow backlog preauthorization package is warranted.
- It should not implement code or tests.
- It should not open public close-case endpoint work.
- It should not claim external pilot readiness or execution.

Non-meaning:

- This does not authorize implementation.
- This does not authorize Yellow work by itself.
- This does not authorize any new code/test/dependency/fixture/runtime/API/schema/release-script/contract/AI_COLLAB changes.
- This does not authorize launch, deployment, external pilot execution, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, S4-A resolver changes, or Red-3 action.

## 7. Required Shape Of Follow-Up Stage

The follow-up stage should be opened as:

```text
OPEN_S5C_STREAM_REVIEW_REFRESH_STAGE
```

It must include:

- current baseline commit, snapshot, manifest PASS, and release sha256
- S5-C planning/contract baseline review
- S5-C-IMPL-5/6/7 implementation closeout summary
- gap matrix comparing S5-C planning candidates against implemented reality
- decision among `S5_C_STREAM_COMPLETE_AND_PARK`, `OPEN_S5C_IMPL8_SCOPED_IMPLEMENTATION_TICKET_PREP`, `OPEN_AUTONOMOUS_YELLOW_BACKLOG_PREAUTH_STAGE`, or `OPEN_EXTERNAL_INPUT_TRACKER_REFRESH_DOCS_ONLY`
- exact reasons for rejecting immediate implementation
- inherited boundary preservation
- automation/vacation implications
- review path
- HOLD conditions

It must route to Claude Web/external review if it claims S5-C stream readiness, freezes a new implementation scope, or changes high-risk lifecycle/action-request/evidence/public-endpoint boundaries.

## 8. HOLD Conditions

This stage must HOLD if any action attempts to:

- implement code or tests
- modify dependencies, fixtures, runtime/API/schema, release scripts, contracts, or AI_COLLAB
- infer Yellow implementation authority from this route decision
- create broad autonomous implementation authority without exact files/tests/HOLD rules
- claim external pilot readiness
- execute launch, deployment, or external pilot work
- access or handle credentials, tokens, API keys, auth headers, cookies, sessions, or secrets
- access, parse, summarize, retain, or validate real customer/operator data
- open public close-case endpoint work
- reopen S5-B or S5-D without a separate governed reopen decision
- reopen ORDIV work without a separate governed route
- change S4-A resolver order or authority
- perform Red-3 action
- use Claude Code for file edits, command execution, tests, staging, commit, or push
- use AdsPower for login automation, profile creation/switching, session inspection, or browser-storage/profile-file inspection

## 9. Non-Authorization

This route-decision stage does not authorize:

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

## 10. Acceptance Criteria

This docs-only route-decision stage is acceptable when:

- this document records the current governed baseline
- selected route is `OPEN_S5C_STREAM_REVIEW_REFRESH_STAGE`
- candidate routes and HOLD reasons are explicit
- vacation-mode automation boundaries are explicit
- immediate implementation is rejected without a separate scoped ticket and GO
- all inherited boundaries remain preserved
- rolling maps are updated as passive context
- `docs\HANDOFF.md` records the route-decision stage
- `releases\release_manifest.json` records the new snapshot/stage in draft state
- manifest `current_release_sha256` remains `null`
- manifest verification fields remain `PENDING_FULL_GATE_AFTER_REVIEW` until full gate PASS
- no code/test/dependency/fixture/runtime/API/schema/release-script/contract/AI_COLLAB files are modified
- known out-of-scope untracked files remain untouched and unstaged

## 11. Final Route Decision

Final selected next task:

```text
OPEN_S5C_STREAM_REVIEW_REFRESH_STAGE
```

This is the next autonomously advanceable product-development task because it reduces the risk of scope invention while keeping the automated development cycle moving. It is Green docs-only and can be closed by the standing Green closeout rule if review, full gate, release verification, manifest PASS, exact staged scope, and no-HOLD conditions pass.
