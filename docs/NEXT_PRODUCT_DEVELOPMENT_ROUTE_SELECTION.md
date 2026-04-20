# Next Product Development Route Selection

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Next Product Development Route Selection |
| Status | Draft governed docs-only route-selection stage |
| Scope | Select the next autonomously advanceable product-development task without authorizing implementation |
| Snapshot | S5-NEXT-PRODUCT-DEVELOPMENT-ROUTE-SELECTION-2026-04-19-001 |
| Stage | s5-next-product-development-route-selection |
| Baseline commit | `8a342825cea2cb45c45709cb32aa2e6b65320f2f` |
| Baseline snapshot | S5-CC-SWITCH-COMMAND-PATH-PROVISIONING-2026-04-19-001 |
| Baseline manifest status | PASS |
| Route opened by | Human product/governance prompt `OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE` |
| Lane | Green docs-only route selection |
| Required review | Claude Code review-only unless a reviewer or human routes to Claude Web/external review |

This stage selects the next safe product-development task from the current governed baseline. It does not implement code, modify tests, create fixtures, change dependencies, update runtime/API/schema behavior, or authorize launch, deployment, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB changes.

## 2. Startup And Baseline Verification

Autonomous startup checks for this stage:

- `docs\DELEGATED_APPROVER_CHARTER.md` was readable.
- `delegation_expires` is `2026-05-06 23:59 Asia/Shanghai`, which has not passed at draft time.
- The current branch is `codex/s3-a-runtime`.
- Baseline commit is `8a342825cea2cb45c45709cb32aa2e6b65320f2f`.
- Baseline manifest snapshot is `S5-CC-SWITCH-COMMAND-PATH-PROVISIONING-2026-04-19-001`.
- Baseline manifest verification status is `PASS`.
- The only known out-of-scope untracked files are `CLAUDE.md` and `SecuPilot_阶段性总结_20260409.md`; this stage does not touch them.

The following governed docs were loaded or checked before drafting:

- `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
- `docs\DELEGATED_APPROVER_CHARTER.md`
- `docs\AUTONOMOUS_DELIVERY_PIPELINE.md`
- `docs\AUTONOMOUS_HOLD_QUEUE.md`
- `docs\L3_CUSTOMER_TRIAL_LAUNCH_CRITICAL_PATH.md`
- `docs\PRODUCT_STATE.md`
- `docs\ROADMAP_AND_PARKED_ITEMS.md`
- `docs\GOVERNANCE_DECISION_LOG.md`
- `docs\AUTONOMOUS_TOOLCHAIN_INTEGRATION.md`
- `docs\AUTONOMOUS_TOOL_CAPABILITY_MATRIX.md`
- `docs\AUTONOMOUS_TOOL_RUNBOOK.md`
- `docs\VSCODE_ROLE_AND_TOOLCHAIN_ORCHESTRATION.md`
- `docs\ADSPOWER_CLAUDE_WEB_AUTOMATION_VERIFICATION.md`
- `docs\ADSPOWER_CLAUDE_WEB_RUNBOOK.md`
- `docs\ADSPOWER_PROFILE_LAUNCH_VERIFICATION.md`
- `docs\ADSPOWER_PROFILE_LAUNCH_RUNBOOK.md`
- `docs\CC_SWITCH_COMMAND_PATH_PROVISIONING.md`
- `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md`

## 3. Current Governed Capability

The current governed automation capability allows:

- Green docs-only route judgment and planning artifacts.
- Green docs-only closeout under the standing rule when exact scope, review, full gate, release verification, manifest PASS, no-HOLD, exact staged files, and reporting conditions are satisfied.
- Limited four-tool Green/docs-only review evidence using Codex orchestration, VS Code local workspace surface, Claude Web in AdsPower review-prompt path, and Claude Code verdict-line review capture through `claude.cmd`.

The current governed automation capability does not allow:

- autonomous implementation without a separate scoped ticket and required approvals
- Yellow implementation by implication from this route selection
- Red execution without exact `DELEGATED_APPROVER_GO`
- any Red-3 action
- launch execution, production deployment, or external pilot execution
- credential handling by AI or real-data handling
- public endpoint work
- S5-B/S5-D reopen
- ORDIV reopen/report/CSV/L1B work
- AI_COLLAB changes

## 4. Product-Development Candidate Routes

| Candidate route | Meaning | Lane | Current status | Risk | Recommendation |
| --- | --- | --- | --- | --- | --- |
| A. `OPEN_S5C_NEXT_SCOPED_IMPLEMENTATION_TICKET_PREP` | Draft a docs-only scoped-ticket preparation artifact for the next possible S5-C implementation ticket. The prep must inspect existing governed S5-C decisions and current code/test baseline, then name exact future files, behavior, tests, review triggers, human GO requirement, and HOLD conditions. | Green docs-only | Allowed as route selection and ticket-prep drafting only. | Could be mistaken for immediate implementation if not tightly bounded. | Selected next product-development task. |
| B. `OPEN_EXTERNAL_INPUT_TRACKER_REFRESH_DOCS_ONLY` | Refresh the external input tracker with owners, channels, missing inputs, restart criteria, and HOLD rules without accepting real evidence or marking inputs ready. | Green docs-only | Allowed as a later blocker-reduction route. | Could be mistaken for readiness or evidence acceptance. | Useful later, not selected as the immediate product-development task. |
| C. `OPEN_S5C_YELLOW_IMPLEMENTATION_NOW` | Start code/test work for another S5-C implementation. | Yellow implementation | Not allowed from this stage. Requires a separate scoped implementation ticket, required review, human GO, exact files/tests, and no HOLD. | Would bypass ticket and review gates. | HOLD. |
| D. `OPEN_EXTERNAL_PILOT_DECISION_PACKAGE` | Draft a customer-trial decision package. | Red-1/Red-2 preparation | Blocked by AHQ-003 and AHQ-011 because external pilot inputs remain `NOT_READY` / `UNKNOWN`. | Could imply readiness or launch. | HOLD. |
| E. `OPEN_PUBLIC_CLOSE_CASE_ENDPOINT_ROUTE` | Reopen public close-case endpoint work. | Red/high-risk route | Blocked by `KEEP_DEFERRED` and AHQ-013. | Public API/runtime/schema behavior risk. | HOLD. |
| F. `REOPEN_S5B_OR_S5D` | Reopen parked source/input or telemetry streams. | Conditional Red / Red-2 depending scope | Blocked by `PASS_AND_PARK` and AHQ-012 without explicit governed reopen decision. | Could reopen source/telemetry contracts or real evidence handling. | HOLD. |
| G. `OPEN_ORDIV_REPORT_CSV_L1B_ROUTE` | Reopen ORDIV report, CSV, or L1B work. | Red-2 / Red-3-adjacent depending evidence | Blocked by ORDIV parked state and AHQ-014. | Real-data/report/evidence risk. | HOLD. |
| H. `PARK_AND_WAIT_FOR_PRODUCT_INPUT` | Do not select a next task. | Green docs-only | Safe fallback. | Progress stalls despite available safe route. | Fallback only. |

## 5. Selected Next Task

Selected route:

```text
OPEN_S5C_NEXT_SCOPED_IMPLEMENTATION_TICKET_PREP
```

Meaning:

- The next product-development task may be a Green docs-only ticket-prep stage.
- That stage should prepare a later possible S5-C scoped implementation ticket.
- It must decide whether a clean next implementation ticket exists after S5-C-IMPL-5, and may HOLD if no exact scope is safe.
- It must use current code/test reality only as local baseline context and must not modify code or tests.
- It must preserve public close-case endpoint `KEEP_DEFERRED`.
- It must preserve external pilot inputs as `NOT_READY` / `UNKNOWN`.
- It must keep S5-B and S5-D parked unless a later explicit reopen decision is made.
- It must keep ORDIV parked unless a later explicit ORDIV route is opened.
- It must keep AI_COLLAB unchanged.

Non-meaning:

- This does not authorize implementation.
- This does not authorize code/test/runtime/API/schema/dependency/fixture changes.
- This does not create a Yellow implementation GO.
- This does not authorize public endpoint work.
- This does not authorize external pilot readiness or execution.
- This does not authorize real data, credentials, evidence retention, or redaction policy freeze.

## 6. Required Shape Of The Follow-Up Ticket-Prep Stage

The follow-up stage should be opened as:

```text
OPEN_S5C_NEXT_SCOPED_IMPLEMENTATION_TICKET_PREP
```

It must include:

- baseline commit, snapshot, manifest PASS, and release sha256
- exact inherited boundaries
- current S5-C implementation history, especially S5-C-IMPL-5 closeout
- candidate next S5-C implementation objectives
- exact candidate future files, if any
- exact candidate future tests, if any
- whether the future implementation would be Yellow or HOLD
- `requires_external_review` decision and rationale
- human GO requirement before implementation
- GO approval specification naming approver role, approval channel, artifact evidence, and HOLD criteria if GO is absent, incomplete, ambiguous, expired, or outside policy
- public close-case endpoint preservation
- evidence/redaction/secret non-retention boundary
- rollback/HOLD criteria
- explicit statement that the ticket-prep stage does not implement

If exact future files, behavior, tests, and acceptance criteria cannot be named safely, the follow-up stage must select HOLD rather than invent implementation scope.

The GO approval specification must state that reviewer PASS is evidence only, not implementation authority. It must name the human product/governance approver role or a delegated approver only where the activated policy explicitly permits that lane. It must define the approval channel as an explicit prompt or governed decision artifact naming the stage/ticket, lane, approved action, file scope, required review, rollback/HOLD criteria, and expiration where applicable. Silence, inferred consent, incomplete approval text, expired approval, lane ambiguity, missing file scope, or unresolved HOLD means implementation remains HOLD.

## 7. Review Routing

This route-selection stage is Green docs-only and does not itself freeze implementation scope. Claude Code review-only is sufficient unless a reviewer or human requests Claude Web/external review.

The follow-up S5-C ticket-prep stage must re-evaluate review needs. It should use Claude Code review-only as baseline review and should route to Claude Web/external review if it freezes or changes case lifecycle semantics, action-request semantics, evidence/audit behavior, runtime/API behavior planning, public endpoint boundary, or any other high-risk trigger.

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
- stage, commit, or push without the applicable governed closeout authority

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
- the selected route is `OPEN_S5C_NEXT_SCOPED_IMPLEMENTATION_TICKET_PREP`
- candidate routes and HOLD reasons are explicit
- the selected route is defined as Green docs-only ticket prep, not implementation
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
OPEN_S5C_NEXT_SCOPED_IMPLEMENTATION_TICKET_PREP
```

This is the next autonomously advanceable product-development task because it moves the product toward a future scoped implementation ticket while staying in Green docs-only territory.

The next task is not implementation. It may only draft the next ticket-prep artifact. Any later code/test implementation still requires a separate scoped implementation ticket, required review, explicit human GO where required, full gate, release verification, and governed closeout.
