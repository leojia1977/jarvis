# Next Product Development Route Selection

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Next Product Development Route Selection |
| Status | Draft governed docs-only route-selection stage |
| Scope | Select the next autonomously advanceable product-development task after S5-C-IMPL-6 closeout without authorizing implementation |
| Snapshot | S5-NEXT-PRODUCT-DEVELOPMENT-ROUTE-SELECTION-2026-04-20-001 |
| Stage | s5-next-product-development-route-selection |
| Baseline commit | `1deae49` |
| Baseline snapshot | S5C-IMPL6-CLOSE-REASON-INTERNAL-SEMANTICS-IMPLEMENTATION-CLOSEOUT-2026-04-20-001 |
| Baseline stage | s5c-impl6-close-reason-internal-semantics-implementation-closeout |
| Baseline manifest status | PASS |
| Baseline release sha256 | `6568e236b2dc098ec4f52b8965db9f7090b8049d050db4d5edbdddc3bf7ad379` |
| Route opened by | Human product/governance prompt `OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE` |
| Lane | Green docs-only route selection |
| Required review | Claude Code review-only or Claude Web/external review if requested before closeout |

This stage selects the next safe product-development task from the current governed baseline. It does not implement code, modify tests, create fixtures, change dependencies, update runtime/API/schema behavior, or authorize launch, deployment, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB changes.

## 2. Startup And Baseline Verification

Autonomous startup checks for this stage:

- `docs\DELEGATED_APPROVER_CHARTER.md` was readable.
- `delegation_expires` is `2026-05-06 23:59 Asia/Shanghai`, which has not passed at draft time.
- The current branch is `codex/s3-a-runtime`.
- Baseline commit is `1deae49`.
- Baseline manifest snapshot is `S5C-IMPL6-CLOSE-REASON-INTERNAL-SEMANTICS-IMPLEMENTATION-CLOSEOUT-2026-04-20-001`.
- Baseline manifest verification status is `PASS`.
- Baseline release sha256 is `6568e236b2dc098ec4f52b8965db9f7090b8049d050db4d5edbdddc3bf7ad379`.
- The only known out-of-scope untracked files are pre-existing local files; this stage does not touch them.

Baseline sha256 traceability is carried by this document control record and the rolling governance maps. The route-selection manifest `current_release_sha256` remains `null` until this new docs-only stage passes full gate and release verification.

The following governed docs were loaded or checked before drafting:

- `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
- `docs\DELEGATED_APPROVER_CHARTER.md`
- `docs\AUTONOMOUS_HOLD_QUEUE.md`
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
- `docs\S5C_SCOPED_IMPLEMENTATION_DECISION.md`
- `docs\S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_CLOSEOUT.md`
- `docs\S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_IMPLEMENTATION_CLOSEOUT.md`

## 3. Automation Capability Impact

The current toolchain supports a governed automation loop for:

- Green docs-only route judgment, ticket prep, review prompt transfer, gate/package/release verification, manifest updates, and closeout when all standing closeout conditions are met.
- Yellow implementation only after a separate scoped implementation ticket and explicit GO define exact files, behavior, tests, review, and HOLD criteria.
- Limited four-tool Green/docs-only review evidence using Codex orchestration, VS Code local workspace surface, Claude Web in AdsPower review-prompt path, and Claude Code verdict-line review capture through `claude.cmd`.

The remaining non-automated or never-automated areas do not block governed product development. They define mandatory HOLD boundaries. Product development can proceed inside Green docs-only and explicitly approved Yellow implementation lanes, but the following remain outside autonomous execution:

- launch execution, production deployment, and external pilot execution
- real data, credentials, secrets, cookies, sessions, tokens, auth headers, browser storage, or profile-file inspection
- public endpoint activation or public close-case endpoint implementation
- S5-B/S5-D reopen, ORDIV reopen/report/CSV/L1B work, S4-A resolver changes, and AI_COLLAB changes
- Red-3 actions
- AdsPower profile creation/switching and Claude Web login automation
- Claude Code file edits, command execution, tests, staging, commit, or push

## 4. Product-Development Candidate Routes

| Candidate route | Meaning | Lane | Current status | Risk | Recommendation |
| --- | --- | --- | --- | --- | --- |
| A. `OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_TICKET_PREP` | Prepare a docs-only scoped implementation ticket for a possible later S5-C case review surface/read-model hardening task. The prep would evaluate whether `case_view` can expose analyst/manager workflow context from existing data without changing public endpoint, runtime service, or persistence semantics. | Green docs-only ticket prep | Allowed as ticket prep only. | Could be mistaken for immediate runtime/API payload change if not tightly bounded. | Selected next product-development task. |
| B. `OPEN_EXTERNAL_INPUT_TRACKER_REFRESH_DOCS_ONLY` | Refresh external pilot input tracker and owners without accepting real evidence or claiming readiness. | Green docs-only | Allowed as a later blocker-reduction route. | Could be mistaken for external pilot readiness. | Useful later, not selected because it does not advance the next in-repo product implementation candidate. |
| C. `OPEN_S5C_YELLOW_IMPLEMENTATION_NOW` | Start another code/test implementation immediately. | Yellow implementation | Not allowed from this stage. Requires separate ticket, review, explicit GO, exact files/tests, full gate, release verification, and closeout. | Would bypass scoped-ticket and GO gates. | HOLD. |
| D. `OPEN_PUBLIC_CLOSE_CASE_ENDPOINT_ROUTE` | Reopen public close-case HTTP endpoint work. | Red/high-risk route | Blocked by `KEEP_DEFERRED` and AHQ-013. | Public API/runtime/schema behavior risk. | HOLD. |
| E. `OPEN_EXTERNAL_PILOT_DECISION_PACKAGE` | Draft a customer-trial decision package. | Red-1/Red-2 preparation | Blocked by AHQ-003 and AHQ-011 because external pilot inputs remain `NOT_READY` / `UNKNOWN`. | Could imply readiness or launch. | HOLD. |
| F. `REOPEN_S5B_OR_S5D` | Reopen parked source/input or telemetry streams. | Conditional Red / Red-2 depending scope | Blocked by `PASS_AND_PARK` and AHQ-012 without explicit governed reopen decision. | Could reopen source/telemetry contracts or real evidence handling. | HOLD. |
| G. `OPEN_ORDIV_REPORT_CSV_L1B_ROUTE` | Reopen ORDIV report, CSV, or L1B work. | Red-2 / Red-3-adjacent depending evidence | Blocked by ORDIV parked state and AHQ-014. | Real-data/report/evidence risk. | HOLD. |
| H. `PARK_AND_WAIT_FOR_PRODUCT_INPUT` | Do not select a next task. | Green docs-only | Safe fallback. | Progress stalls despite a bounded ticket-prep candidate. | Fallback only. |

## 5. Selected Next Task

Selected route:

```text
OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_TICKET_PREP
```

Meaning:

- The next product-development task may be a Green docs-only ticket-prep stage.
- That stage should prepare a possible later S5-C-IMPL-7 scoped implementation ticket.
- The candidate theme is analyst/manager case review surface/read-model hardening using existing governed data.
- The ticket-prep stage may inspect `backend\app\agents\case_view.py`, `backend\tests\test_case_view.py`, and related governed docs as read-only baseline context.
- The ticket-prep stage must decide whether any later implementation can be bounded without public endpoint work, runtime service changes, persistence schema changes, real data, credentials, or evidence retention.
- If exact future files, behavior, tests, and acceptance criteria cannot be safely named, the ticket-prep stage must HOLD.
- The `IMPL7` label is a planning/ticket sequence label only. It does not constitute an implementation GO. A separate Yellow implementation review gate and explicit GO are required before any code or test changes.

Non-meaning:

- This does not authorize implementation.
- This does not authorize code/test/runtime/API/schema/dependency/fixture changes.
- This does not create a Yellow implementation GO.
- This does not allow any future stage to infer Yellow implementation authority from the `IMPL7` label.
- This does not authorize public close-case endpoint work.
- This does not authorize external pilot readiness or execution.
- This does not authorize real data, credentials, evidence retention, or redaction policy freeze.

## 6. Required Shape Of The Follow-Up Ticket-Prep Stage

The follow-up stage should be opened as:

```text
OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_TICKET_PREP
```

It must include:

- current baseline commit, snapshot, manifest PASS, and release sha256
- exact inherited boundaries
- current S5-C implementation history, especially S5-C-IMPL-5 and S5-C-IMPL-6 closeouts
- candidate future implementation objective
- exact candidate future files, if any
- exact candidate future tests, if any
- whether the future implementation would be Yellow or HOLD
- whether external review is required before implementation GO
- human GO requirement before implementation
- rollback/HOLD criteria
- explicit public close-case endpoint preservation
- evidence/redaction/secret non-retention boundary
- explicit statement that ticket prep does not implement
- explicit statement that the `IMPL7` label is not implementation authorization and that a separate Yellow implementation review gate plus explicit GO are required before code/test changes

Candidate future file scope for analysis only:

- `backend\app\agents\case_view.py`
- `backend\tests\test_case_view.py`
- `backend\tests\test_runtime_service.py` only if the later ticket explicitly decides existing runtime payload assertions must be protected

The follow-up ticket-prep document must restate the `backend\tests\test_runtime_service.py` condition explicitly if it includes that file in any candidate future scope. If the condition cannot be stated exactly, the file must remain excluded.

Candidate exclusions that should remain excluded unless a later ticket explicitly governs otherwise:

- `backend\app\runtime_service.py`
- `backend\app\main.py`
- public endpoint/API/schema files
- fixture files
- dependency files
- release scripts
- contract files
- AI_COLLAB files

## 7. Review Routing

This route-selection stage is Green docs-only and does not itself freeze implementation scope. Claude Code review-only is sufficient unless a reviewer or human requests Claude Web/external review.

The follow-up S5-C-IMPL-7 ticket-prep stage must re-evaluate review needs. It should route to Claude Web/external review before implementation GO if it freezes or changes case view contract shape, analyst/manager workflow semantics, lifecycle/action-request semantics, evidence/audit behavior, runtime/API behavior planning, public endpoint boundary, or any other high-risk trigger.

Claude Code review evidence is not authority. Human or delegated authority remains required where the policy requires GO.

## 8. HOLD Conditions

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

## 9. Non-Authorization

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

## 10. Acceptance Criteria

This docs-only route-selection stage is acceptable when:

- this document records the current governed baseline
- the selected route is `OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_TICKET_PREP`
- candidate routes and HOLD reasons are explicit
- the selected route is defined as Green docs-only ticket prep, not implementation
- automation capability limitations are recorded as HOLD boundaries rather than blockers to governed development
- all inherited boundaries remain preserved
- rolling maps are updated as passive context
- `docs\HANDOFF.md` records the route-selection stage
- `releases\release_manifest.json` records the new snapshot/stage in draft state
- manifest `current_release_sha256` remains `null`
- manifest verification fields remain `PENDING_FULL_GATE_AFTER_REVIEW` until full gate PASS
- no code/test/dependency/fixture/runtime/API/schema/release-script/contract/AI_COLLAB files are modified
- known out-of-scope untracked files remain untouched and unstaged

## 11. Final Route Decision

Final selected next task:

```text
OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_TICKET_PREP
```

This is the next autonomously advanceable product-development task because it moves the product toward a future scoped S5-C implementation ticket while staying in Green docs-only territory.

The next task is not implementation. It may only draft the next ticket-prep artifact. Any later code/test implementation still requires a separate scoped implementation ticket, required review, explicit human GO where required, full gate, release verification, and governed closeout.
