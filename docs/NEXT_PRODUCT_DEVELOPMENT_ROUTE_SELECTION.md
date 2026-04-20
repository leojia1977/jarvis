# Next Product Development Route Selection

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Next Product Development Route Selection |
| Status | Draft governed docs-only route-selection stage |
| Scope | Select the next autonomously advanceable product-development task after S5-C-IMPL-7 closeout without authorizing implementation |
| Snapshot | S5-NEXT-PRODUCT-DEVELOPMENT-ROUTE-SELECTION-2026-04-20-002 |
| Stage | s5-next-product-development-route-selection |
| Baseline commit | `d753416a77099da4468d80e13d65897004a59bc1` |
| Baseline snapshot | S5C-IMPL7-CASE-REVIEW-SURFACE-IMPLEMENTATION-CLOSEOUT-2026-04-20-001 |
| Baseline stage | s5c-impl7-case-review-surface-implementation-closeout |
| Baseline manifest status | PASS |
| Baseline release sha256 | `9545c2c13cb0eaaae16b55c43b370a3891e7517531aadb3a81bd332e209e6c6b` |
| Route opened by | Human product/governance prompt `OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE` |
| Lane | Green docs-only route selection |
| Required review | Claude Code review-only or Claude Web/external review if requested before closeout |

This stage selects the next safe product-development task from the current governed baseline. It does not implement code, modify tests, create fixtures, change dependencies, update runtime/API/schema behavior, or authorize launch, deployment, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB changes.

## 2. Startup And Baseline Verification

Autonomous startup checks for this stage:

- `docs\DELEGATED_APPROVER_CHARTER.md` was readable.
- `delegation_expires` is `2026-05-06 23:59 Asia/Shanghai`, which has not passed at draft time.
- The current branch is `codex/s3-a-runtime`.
- Baseline commit is `d753416a77099da4468d80e13d65897004a59bc1`.
- Baseline manifest snapshot is `S5C-IMPL7-CASE-REVIEW-SURFACE-IMPLEMENTATION-CLOSEOUT-2026-04-20-001`.
- Baseline manifest verification status is `PASS`.
- Baseline release sha256 is `9545c2c13cb0eaaae16b55c43b370a3891e7517531aadb3a81bd332e209e6c6b`.
- The only known out-of-scope untracked files are pre-existing local files; this stage does not touch them.

The following governed docs were loaded or checked before drafting:

- `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
- `docs\DELEGATED_APPROVER_CHARTER.md`
- `docs\AUTONOMOUS_DELIVERY_PIPELINE.md`
- `docs\AUTONOMOUS_HOLD_QUEUE.md`
- `docs\L3_CUSTOMER_TRIAL_LAUNCH_CRITICAL_PATH.md`
- `docs\PRODUCT_STATE.md`
- `docs\ROADMAP_AND_PARKED_ITEMS.md`
- `docs\GOVERNANCE_DECISION_LOG.md`
- `docs\HANDOFF.md`
- `docs\SPRINT5_PRD.md`
- `docs\SPRINT5_JIRA_BACKLOG.md`
- `docs\S5C_CASE_WORKFLOW_HARDENING_PLAN.md`
- `docs\S5C1_CASE_WORKFLOW_JOURNEY_CONTRACT.md`
- `docs\S5C2_CLOSE_REASON_AND_LIFECYCLE_SEMANTICS.md`
- `docs\S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`
- `docs\S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`
- `docs\S5C5_CASE_WORKFLOW_REVIEW_PASS.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_CLOSEOUT.md`
- `docs\S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_IMPLEMENTATION_CLOSEOUT.md`
- `docs\S5C_IMPL7_CASE_REVIEW_SURFACE_IMPLEMENTATION_CLOSEOUT.md`

The route-selection manifest `current_release_sha256` remains `null` until this new docs-only stage passes full gate and release verification.

## 3. New Conversation Window Decision

A new conversation window is not required for this route-selection stage.

Current-thread continuation is acceptable because:

- the current governed baseline was re-read from `releases\release_manifest.json`
- core governance docs were reloaded from the repo
- current `docs\HANDOFF.md`, `docs\PRODUCT_STATE.md`, `docs\ROADMAP_AND_PARKED_ITEMS.md`, and `docs\GOVERNANCE_DECISION_LOG.md` were used as repo-backed context
- the working tree was clean except for the two known out-of-scope untracked local files

If a later new window is opened, the new session must start by loading `releases\release_manifest.json`, `docs\HANDOFF.md`, `docs\PRODUCT_STATE.md`, `docs\ROADMAP_AND_PARKED_ITEMS.md`, `docs\GOVERNANCE_DECISION_LOG.md`, `docs\DELEGATED_APPROVER_CHARTER.md`, and the eight core governance docs before action. New-window memory is execution context only; repo-governed artifacts remain the authority.

## 4. Automation Capability Impact

The current toolchain supports governed autonomous progress for:

- Green docs-only route judgment, ticket prep, review prompt transfer, gate/package/release verification, manifest updates, and closeout when all standing closeout conditions are met
- Yellow implementation only after a separate scoped implementation ticket and explicit GO define exact files, behavior, tests, review, and HOLD criteria
- limited four-tool Green/docs-only review evidence using Codex orchestration, VS Code local workspace surface, Claude Web in AdsPower review-prompt path, and Claude Code verdict-line review capture through `claude.cmd`

The remaining non-automated or never-automated areas do not block governed product development. They define mandatory HOLD boundaries:

- launch execution, production deployment, and external pilot execution
- real data, credentials, secrets, cookies, sessions, tokens, auth headers, browser storage, or profile-file inspection
- public endpoint activation or public close-case endpoint implementation
- S5-B/S5-D reopen, ORDIV reopen/report/CSV/L1B work, S4-A resolver changes, and AI_COLLAB changes
- Red-3 actions
- AdsPower profile creation/switching and Claude Web login automation
- Claude Code file edits, command execution, tests, staging, commit, or push

This means autonomous product development can proceed, but only as governed Green docs-only work or explicitly authorized Yellow implementation. It is intentionally not an unguarded autonomous implementation loop.

## 5. Product-Development Candidate Routes

| Candidate route | Meaning | Lane | Current status | Risk | Recommendation |
| --- | --- | --- | --- | --- | --- |
| A. `OPEN_POST_S5C_IMPL7_ROUTE_DECISION_STAGE` | Review the post-IMPL7 S5-C state and decide whether the next safe route is S5-C stream review/refresh, another scoped implementation ticket prep, external input tracker refresh, or park/wait. | Green docs-only route decision | Allowed. | Low; must avoid implying implementation readiness. | Selected next product-development task. |
| B. `OPEN_S5C_STREAM_REVIEW_REFRESH_STAGE` | Refresh S5-C planning/implementation acceptance after IMPL5/6/7 and record remaining gaps. | Green docs-only | Probably allowed after a post-IMPL7 route decision confirms scope. | Could be premature if it implies stream completion without reviewing implementation deltas. | Candidate follow-up, not selected directly. |
| C. `OPEN_S5C_IMPL8_SCOPED_IMPLEMENTATION_TICKET_PREP` | Prepare another S5-C implementation ticket. | Green docs-only ticket prep | Not selected yet because no exact unimplemented safe gap is named from the current baseline. | Could invent implementation scope. | HOLD until post-IMPL7 route decision identifies a precise gap. |
| D. `OPEN_S5C_YELLOW_IMPLEMENTATION_NOW` | Start another code/test implementation immediately. | Yellow implementation | Not allowed from this stage. Requires separate ticket, review, explicit GO, exact files/tests, full gate, release verification, and closeout. | Would bypass scoped-ticket and GO gates. | HOLD. |
| E. `OPEN_PUBLIC_CLOSE_CASE_ENDPOINT_ROUTE` | Reopen public close-case HTTP endpoint work. | Red/high-risk route | Blocked by `KEEP_DEFERRED` and AHQ-013. | Public API/runtime/schema behavior risk. | HOLD. |
| F. `OPEN_EXTERNAL_PILOT_DECISION_PACKAGE` | Draft a customer-trial decision package. | Red-1/Red-2 preparation | Blocked by AHQ-003 and AHQ-011 because external pilot inputs remain `NOT_READY` / `UNKNOWN`. | Could imply readiness or launch. | HOLD. |
| G. `REOPEN_S5B_OR_S5D` | Reopen parked source/input or telemetry streams. | Conditional Red / Red-2 depending scope | Blocked by `PASS_AND_PARK` and AHQ-012 without explicit governed reopen decision. | Could reopen source/telemetry contracts or real evidence handling. | HOLD. |
| H. `OPEN_ORDIV_REPORT_CSV_L1B_ROUTE` | Reopen ORDIV report, CSV, or L1B work. | Red-2 / Red-3-adjacent depending evidence | Blocked by ORDIV parked state and AHQ-014. | Real-data/report/evidence risk. | HOLD. |
| I. `PARK_AND_WAIT_FOR_PRODUCT_INPUT` | Do not select a next task. | Green docs-only | Safe fallback. | Progress stalls despite a bounded route-decision candidate. | Fallback only. |

## 6. Selected Next Task

Selected route:

```text
OPEN_POST_S5C_IMPL7_ROUTE_DECISION_STAGE
```

Meaning:

- The next product-development task is a Green docs-only route-decision stage.
- It should evaluate the governed S5-C state after IMPL5, IMPL6, and IMPL7.
- It should decide whether to open a stream review/refresh, prepare a precise S5-C-IMPL8 ticket, refresh external input tracking, or park/wait.
- It may inspect governed docs and current code/test reality as read-only baseline context.
- It must not implement code or tests.
- It must not open public close-case endpoint work.
- It must HOLD if it cannot name a safe next route without crossing current HOLD boundaries.

Non-meaning:

- This does not authorize implementation.
- This does not authorize code/test/runtime/API/schema/dependency/fixture changes.
- This does not create a Yellow implementation GO.
- This does not authorize public close-case endpoint work.
- This does not authorize external pilot readiness or execution.
- This does not authorize real data, credentials, evidence retention, or redaction policy freeze.
- This does not reopen S5-B, S5-D, ORDIV, AI_COLLAB, or S4-A resolver work.

## 7. Required Shape Of The Follow-Up Route-Decision Stage

The follow-up stage should be opened as:

```text
OPEN_POST_S5C_IMPL7_ROUTE_DECISION_STAGE
```

It must include:

- current baseline commit, snapshot, manifest PASS, and release sha256
- exact inherited boundaries
- current S5-C implementation history, especially S5-C-IMPL-5, S5-C-IMPL-6, and S5-C-IMPL-7 closeouts
- candidate next routes and rejection reasons
- whether an S5-C stream review/refresh is safe now
- whether any S5-C-IMPL8 ticket-prep candidate can be safely named
- whether external input tracker refresh is a better next Green docs-only task
- whether the route should park/wait for product input
- required review path
- rollback/HOLD criteria
- explicit public close-case endpoint preservation
- evidence/redaction/secret non-retention boundary
- explicit statement that route decision does not implement

Candidate future routes for that stage:

- `OPEN_S5C_STREAM_REVIEW_REFRESH_STAGE`
- `OPEN_S5C_IMPL8_SCOPED_IMPLEMENTATION_TICKET_PREP`
- `OPEN_EXTERNAL_INPUT_TRACKER_REFRESH_DOCS_ONLY`
- `PARK_AND_WAIT_FOR_PRODUCT_INPUT`

The follow-up must reject immediate implementation unless a separate exact scoped ticket and explicit Yellow GO exist.

## 8. Review Routing

This route-selection stage is Green docs-only and does not itself freeze implementation scope. Claude Code review-only is sufficient unless a reviewer or human requests Claude Web/external review.

The follow-up post-IMPL7 route-decision stage must re-evaluate review needs. It should route to Claude Web/external review if it claims stream readiness, freezes a new implementation-ticket scope, touches high-risk launch/public endpoint language, or changes inherited S5-C lifecycle/action-request/evidence boundaries.

Claude Code review evidence is not authority. Human or delegated authority remains required where the policy requires GO.

## 9. HOLD Conditions

This stage must HOLD if any action attempts to:

- implement code or tests
- modify dependencies, fixtures, runtime/API/schema, release scripts, contracts, or AI_COLLAB
- infer Yellow implementation authority from this route selection
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

## 10. Non-Authorization

This route-selection stage does not authorize:

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

This docs-only route-selection stage is acceptable when:

- this document records the current governed baseline
- the selected route is `OPEN_POST_S5C_IMPL7_ROUTE_DECISION_STAGE`
- candidate routes and HOLD reasons are explicit
- the selected route is defined as Green docs-only route decision, not implementation
- automation capability limitations are recorded as HOLD boundaries rather than blockers to governed development
- all inherited boundaries remain preserved
- rolling maps are updated as passive context
- `docs\HANDOFF.md` records the route-selection stage
- `releases\release_manifest.json` records the new snapshot/stage in draft state
- manifest `current_release_sha256` remains `null`
- manifest verification fields remain `PENDING_FULL_GATE_AFTER_REVIEW` until full gate PASS
- no code/test/dependency/fixture/runtime/API/schema/release-script/contract/AI_COLLAB files are modified
- known out-of-scope untracked files remain untouched and unstaged

## 12. Final Route Decision

Final selected next task:

```text
OPEN_POST_S5C_IMPL7_ROUTE_DECISION_STAGE
```

This is the next autonomously advanceable product-development task because it keeps momentum after S5-C-IMPL-7 while preventing automation from inventing a new implementation task without exact product need, file scope, tests, and GO.

The next task is not implementation. It may only draft the next route-decision artifact. Any later code/test implementation still requires a separate scoped implementation ticket, required review, explicit human GO where required, full gate, release verification, and governed closeout.
