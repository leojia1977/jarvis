# Roadmap And Parked Items

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Roadmap And Parked Items |
| Status | Rolling governed roadmap and parked-items map |
| Snapshot | S5-MINI-SWE-AGENT-NONINTERACTIVE-DRY-RUN-VERIFICATION-2026-04-21-001 |
| Stage | s5-mini-swe-agent-noninteractive-dry-run-verification |
| Baseline commit | `262dc49081ff4d41b0ae425536b098e53a218136` |

This file summarizes parked, deferred, and possible future routes. It is a passive governed context and planning aid only. It does not authorize implementation, reopen parked streams, create pilot readiness, or override source governed docs.

## 2. Current Mainline Posture

The current governed mainline outcome is the fourth preauthorized S5-C Yellow backlog item closeout, the autonomous Yellow backlog template anti-overengineering refresh, the governed current phase summary, the next product-development route selection, the next Yellow backlog preauthorization package, and the SWE agent install/capability verification. The current in-flight Green docs-only stage verifies whether WSL2 or a PTY-capable runner can support a no-write mini-swe-agent dry run.

The YB-04 closeout completed under exact test-only file scope. The template refresh added future anti-overengineering rules. The phase summary records current posture, route selection chose `OPEN_NEXT_YELLOW_BACKLOG_PREAUTHORIZATION_STAGE`, and the package prepared YB-05 through YB-07. SWE agent / mini-swe-agent is partially verified for user-package presence and help visibility, but main agent execution remains HOLD because no WSL/PTTY no-write dry run is available. This stage does not authorize launch execution, deployment, real-data handling, public endpoint work, login route, AdsPower profile switching/creation, parked-stream reopen, runtime/API/schema behavior, production code changes, test changes, SWE agent execution/integration, WSL distro installation, PTY runner installation, or unlisted implementation.

## 3. Parked And Deferred Items

| Item | Current state | Why parked/deferred | What could reopen it | Prohibited now |
| --- | --- | --- | --- | --- |
| ORDIV-L1A | `PARK_LOCAL_VALIDATION_NO_REPORT` | Local validation lineage is parked with no report, no metrics, and no further real-data work. | Separate governed route with Claude Web if report governance, real-data validation, CSV, L1B, evidence retention, or redaction policy is implicated. | ORDIV report creation, metrics, further real-data validation, workbook access/listing/opening/parsing/copying/inspection/summarization/upload/retention, CSV processing, L1B syslog/log parsing. |
| S5-B source/input | `PASS_AND_PARK` | Discovery is accepted and parked; no new source/input gap has been provided. | Explicit S5-B reopen decision with scoped source/input question and review. | Source adapter implementation, source contract freeze, identity/source mapping freeze, real source access, fixture creation/modification. |
| S5-D telemetry | `PASS_AND_PARK` | Discovery is accepted and parked; no new telemetry gap has been provided. | Explicit S5-D reopen decision with scoped telemetry question and review. | Telemetry adapter implementation, telemetry schema/normalization/freshness/provenance freeze, real telemetry handling, evidence retention. |
| Public close-case endpoint | `KEEP_DEFERRED` | Endpoint work remains high risk and was deferred by governed S5-C decisions. | Separate public close-case endpoint route with required review and exact API/runtime scope. | Public endpoint work, new public API endpoints, runtime API/schema contract changes, weakening `KEEP_DEFERRED`. |
| External pilot inputs | `NOT_READY` / `UNKNOWN` | Required input categories remain incomplete in governed repo evidence. | Product/governance supplies governed inputs and evidence-handling rules. | Marking any input `READY`, creating a pilot package, claiming readiness, storing raw customer/operator evidence. |
| External pilot execution | Unauthorized | No governed external pilot decision package or sign-off exists. | Later external pilot decision package, required review, and explicit human GO. | External pilot execution, readiness claims, real customer/operator sign-off, real external-system access. |
| AI_COLLAB | Unchanged | Current stage is not an AI_COLLAB governance route. | Separate AI_COLLAB governance route. | Any AI_COLLAB file modification or behavior change from this stage. |

## 4. Possible Future Routes

Possible future routes require separate human product/governance decision:

- Continue waiting for product input.
- Open a scoped S5-C docs-only ticket if a concrete product need is supplied.
- Revisit external input tracking if product/governance supplies channels or owners.
- Reopen S5-B or S5-D only through explicit governed reopen decisions.
- Open public close-case endpoint route only through a high-risk governed route.
- Open ORDIV report/CSV/L1B route only through required review and explicit authorization.
- Open stream/milestone closeout only when readiness criteria and review triggers are satisfied.
- Open autonomous L3 launch acceleration path only through the governed authorization policy, delegated approver charter, delivery pipeline, L3 critical path, and HOLD queue.

## 5. Autonomous L3 Launch Acceleration Path

The autonomous L3 launch acceleration path is a candidate governed path for controlled customer-trial launch / private launch candidate preparation.

Green/Yellow/Conditional Red authorization can accelerate future stages only within the ACTIVE authorization window and under all policy limits:

- delegated approver `jarvis, technical lead` is confirmed as an accountable human approver
- authorization window is active: 2026-04-18 00:00 Asia/Shanghai to 2026-05-06 23:59 Asia/Shanghai
- policy state is `ACTIVE` only during that window after human product/governance `FINAL_HUMAN_GO`
- every autonomous session starts by reading `docs\DELEGATED_APPROVER_CHARTER.md` and verifying `delegation_expires`
- lane and allowed actions are explicit
- required external review conditions are incorporated
- `DELEGATED_APPROVER_GO` is complete where Red approval is required
- required review is satisfied
- full gate and release rules are followed where applicable
- no HOLD remains

The final activation path records `FINAL_HUMAN_GO`, closes AHQ-018 as `CLOSED_BY_FINAL_HUMAN_GO`, and adds an `AUTONOMOUS_PERIOD_START` marker. It does not itself authorize launch execution, external pilot execution, production deployment, real-data handling, credential handling, public endpoint activation, S5-B/S5-D reopen, ORDIV report/CSV/L1B work, Red-3 action, S4-A resolver changes, or AI_COLLAB changes.

The autonomous operation startup path added a default operating cadence for safe Green/Yellow docs-only drafting and closeout-gate preparation. The later anti-overengineering template refresh aligns the active cadence to every 1 hour. Startup does not close AHQ-003 through AHQ-014, does not remove AHQ-017 ambiguity handling, and does not authorize Red execution beyond exact per-action policy requirements.

The autonomous toolchain integration path defines a four-tool collaboration model and capability matrix. It reduced planning risk by clarifying Codex, VS Code, Claude Code through the user-configured `cc switch` API tool, Claude Web running in the user's AdsPower browser/profile, Git, and release/gate boundaries, but it did not claim full four-tool automation at that baseline. Later governed stages separately verified AdsPower Claude Web review-prompt transfer, configured AdsPower profile launch/attach to review-prompt readiness, and the bounded Claude Code verdict-line path.

The AdsPower Claude Web automation verification path verifies only a harmless review-prompt round trip through an already-active AdsPower profile and already-open Claude Web page. It may unlock safe future review-prompt transfer, but it does not unlock AdsPower profile launch/switch control, login automation, secrets/session inspection, high-risk review substitution, Red execution, launch, deployment, external pilot execution, public endpoint work, real-data handling, S5-B/S5-D reopen, ORDIV work, or Red-3 action.

The autonomous ops loop refresh path removes the duplicate loop and narrows automatic closeout permission to Green docs-only stages after this refresh stage itself closes PASS. It may reduce human confirmation load for safe docs-only governance stages, but it does not authorize Yellow implementation, Red execution, full autonomous implementation, AdsPower profile switch, Claude Web login, launch, deployment, external pilot execution, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB changes.

The earlier `cc switch` Claude Code review automation verification path attempted only non-secret local command discovery. No `cc` command/API path was discoverable in the VS Code workspace at that time, so AHQ-020 remained `HOLD_FOR_TOOL_VERIFICATION`. The later cc switch command-path provisioning route supersedes that HOLD only for the bounded `claude.cmd` verdict-line review path.

The VS Code role and toolchain orchestration path clarifies that VS Code is the local workspace/editing execution surface only. Codex remains the orchestrator for governance loading, lane classification, review routing, gate/package/release verification, manifest updates, and governed closeout under policy limits. VS Code is not product memory, approval authority, independent reviewer, route authority, PASS authority, or closeout authority by itself. This path does not authorize implementation, code/test changes, browser login/session access, AdsPower profile launch/switch, Red execution, launch, deployment, real data, public endpoint work, S5-B/S5-D reopen, ORDIV work, AI_COLLAB changes, or full four-tool automation.

The AdsPower profile launch verification path verifies the configured profile launch/attach route to Claude Web review-prompt readiness. It may support future safe review-prompt transfer when the configured profile is not already active, but it does not authorize profile creation, profile switching, login automation, cookie/session/token/auth-header inspection, browser storage/profile-file inspection, reading Claude conversation history, high-risk review substitution, Yellow implementation, Red execution, launch, deployment, external pilot execution, real-data handling, public endpoint work, S5-B/S5-D reopen, ORDIV work, AI_COLLAB changes, or full four-tool automation.

The cc switch command-path provisioning route verifies only Claude Code review-only verdict capture through stdin prompt transfer to `claude.cmd` with `--bare`, JSON wrapper output, disabled tools, no session persistence, plan permission mode, budget cap, first-line verdict parsing, no web requests, and unchanged git status. It may support a limited four-tool Green/docs-only review loop, but it does not authorize Claude Code file edits, file-read review beyond supplied prompt material unless separately governed, command execution, tests, staging, commit, push, Yellow implementation, Red execution, launch, deployment, external pilot execution, credentials, real data, public endpoint work, S5-B/S5-D reopen, ORDIV work, AI_COLLAB changes, or full autonomous implementation.

The L3 deadline is a planning target only. It is not readiness, launch authorization, customer sign-off, or external pilot execution authorization.

Parked items remain parked until explicit governed reopen/approval:

- ORDIV-L1A remains `PARK_LOCAL_VALIDATION_NO_REPORT`.
- S5-B remains `PASS_AND_PARK`.
- S5-D remains `PASS_AND_PARK`.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- External pilot execution remains unauthorized.
- L3 launch execution remains unauthorized.

## 6. Standing Prohibitions

- No implementation is authorized.
- No external pilot input is `READY`.
- No external pilot execution is authorized.
- No S5-B/S5-D/ORDIV/public endpoint/AI_COLLAB route is reopened.
- No evidence retention, storage, replay, deletion, expiry, evidence-pack behavior, or redaction policy freeze is authorized.
- No credentials, tokens, API keys, auth headers, cookies, or secret material may be introduced.

## 7. Next Product Development Route Selection

Selected next route:

- `OPEN_S5C_NEXT_SCOPED_IMPLEMENTATION_TICKET_PREP`

This route may draft a Green docs-only ticket-prep artifact for a possible later S5-C scoped implementation ticket. It is selected because it can move product development toward a bounded implementation decision without crossing current HOLDs.

The route must not implement anything. It must preserve:

- public close-case endpoint `KEEP_DEFERRED`
- S5-B `PASS_AND_PARK`
- S5-D `PASS_AND_PARK`
- ORDIV-L1A `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs `NOT_READY` / `UNKNOWN`
- external pilot execution unauthorized
- S4-A resolver order `asset_id -> hostname -> fqdn -> ip_address -> aliases`
- AI_COLLAB unchanged

Fallback if exact future S5-C scope cannot be safely named:

- `PARK_NEXT_IMPLEMENTATION_AND_OPEN_EXTERNAL_INPUT_TRACKER_REFRESH_DOCS_ONLY`

## 8. S5-C Next Scoped Implementation Ticket Prep

Selected future candidate:

- `OPEN_S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_TICKET`

This route may prepare a later Yellow implementation ticket for internal S5-C close reason taxonomy validation and synthetic tests. It is selected because it can reduce a narrow S5-C-2 implementation gap without opening the public close-case endpoint.

The candidate future route must preserve:

- public close-case endpoint `KEEP_DEFERRED`
- S5-B `PASS_AND_PARK`
- S5-D `PASS_AND_PARK`
- ORDIV-L1A `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs `NOT_READY` / `UNKNOWN`
- external pilot execution unauthorized
- S4-A resolver order `asset_id -> hostname -> fqdn -> ip_address -> aliases`
- AI_COLLAB unchanged

The candidate future route must not implement until a separate scoped ticket, required review, explicit human GO, full gate, release verification, and governed closeout are complete.

## 9. S5-C-IMPL-6 Close Reason Internal Semantics Ticket

Opened route:

- `OPEN_S5C_IMPL6_CLOSE_REASON_INTERNAL_SEMANTICS_TICKET`

This route records the docs-only scoped implementation ticket for a later Yellow implementation of internal S5-C close reason taxonomy validation and synthetic tests.

The future implementation route is limited to:

- internal helper semantics in `backend\app\tools\persistent_case.py`
- synthetic regression tests in `backend\tests\test_case_lifecycle_regression.py`
- synthetic store round-trip tests in `backend\tests\test_case_store.py`
- optional action-request preservation tests in `backend\tests\test_case_action_request_contract.py` only if the later implementation ticket or explicit human GO records that unresolved action-request closure interactions are touched

The future implementation route must preserve:

- public close-case endpoint `KEEP_DEFERRED`
- S5-B `PASS_AND_PARK`
- S5-D `PASS_AND_PARK`
- ORDIV-L1A `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs `NOT_READY` / `UNKNOWN`
- external pilot execution unauthorized
- S4-A resolver order `asset_id -> hostname -> fqdn -> ip_address -> aliases`
- AI_COLLAB unchanged

The future implementation route must not touch `backend\app\runtime_service.py`, `backend\app\main.py`, public API/schema behavior, fixtures, dependencies, release scripts, contracts, real data, credentials, evidence retention, redaction policy freeze, public endpoint work, parked-stream reopen, Red-3 action, or AI_COLLAB. Importing, wiring, or exposing the helper through runtime/API paths requires a separate governed route.

For this S5-C-IMPL-6 manifest draft, `releases\release_manifest.json` path fields follow the existing Windows source-of-truth manifest convention for this repository and do not authorize changing release tooling semantics.

Implementation remains HOLD until required review, explicit human GO, full gate, release verification, and governed closeout are complete.

## 10. S5-C-IMPL-6 Implementation Closeout

Closeout route:

- `S5-C-IMPL-6 Close Reason Internal Semantics Implementation Closeout`

This route records that the bounded Yellow implementation was completed inside the governed S5-C-IMPL-6 file scope.

Implemented scope:

- internal close reason taxonomy validation in `backend\app\tools\persistent_case.py`
- internal `close_persistent_case()` helper
- close reason audit metadata in existing lifecycle audit `details`
- synthetic lifecycle and store tests

Preserved exclusions:

- no `backend\app\runtime_service.py`
- no `backend\app\main.py`
- no public endpoint work
- no runtime/API/schema behavior
- no fixtures, dependencies, release scripts, contracts, real data, credentials, evidence retention, redaction policy freeze, parked-stream reopen, Red-3 action, or AI_COLLAB

Full gate/package/release verification passed for the implementation closeout. Staging, commit, and push remain separately unauthorized.

## 11. Next Product Development Route Selection After S5-C-IMPL-6

Selected route:

- `OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_TICKET_PREP`

This route may draft a Green docs-only ticket-prep artifact for a possible later S5-C-IMPL-7 scoped implementation ticket.

The candidate future task is analyst/manager case review surface or read-model hardening using existing governed data. It is selected because it can move the product toward a bounded in-repo development decision without reopening public close-case endpoint work, launch, real data, credentials, S5-B/S5-D, ORDIV, Red-3, or AI_COLLAB.

The follow-up route must not implement anything. It must preserve:

- public close-case endpoint `KEEP_DEFERRED`
- S5-B `PASS_AND_PARK`
- S5-D `PASS_AND_PARK`
- ORDIV-L1A `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs `NOT_READY` / `UNKNOWN`
- external pilot execution unauthorized
- S4-A resolver order `asset_id -> hostname -> fqdn -> ip_address -> aliases`
- AI_COLLAB unchanged

Candidate future file analysis may include `backend\app\agents\case_view.py`, `backend\tests\test_case_view.py`, and optionally `backend\tests\test_runtime_service.py` only as read-only ticket-prep context. Any later implementation remains HOLD until a separate scoped ticket, required review, explicit GO, full gate, release verification, and governed closeout are complete.

## 12. S5-C-IMPL-7 Case Review Surface Ticket Prep

## 13. S5-C-IMPL-7 Case Review Surface Implementation Ticket

Opened route:

- `OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_IMPLEMENTATION_TICKET`

This route defines the exact scoped Yellow implementation ticket for S5-C-IMPL-7.

Allowed future implementation:

- `backend\app\agents\case_view.py`
- `backend\tests\test_case_view.py`

Frozen behavior:

- add bounded internal review guidance under `analysis_limits["review_guidance"]`
- preserve existing top-level case view panels
- keep `execution_authorized: False` in review/manager decision context
- use synthetic tests only

Excluded:

- `backend\tests\test_runtime_service.py`
- `backend\app\runtime_service.py`
- `backend\app\main.py`
- public endpoint/API/schema files
- `backend\app\tools\persistent_case.py`
- fixtures, dependencies, release scripts, contracts, AI_COLLAB, real data, credentials, runtime behavior, launch, external pilot, S5-B/S5-D, ORDIV, Red-3

Human product/governance supplied Yellow implementation GO in the route prompt, constrained by this ticket and effective only after this ticket closes PASS.

## 14. S5-C-IMPL-7 Case Review Surface Implementation Closeout

Closeout route:

- `S5-C-IMPL-7 Case Review Surface Implementation Closeout`

This route records that the bounded Yellow implementation was completed inside the governed S5-C-IMPL-7 file scope.

Implemented scope:

- internal review guidance under `analysis_limits["review_guidance"]` in `backend\app\agents\case_view.py`
- synthetic regression coverage in `backend\tests\test_case_view.py`
- review context, manager decision context, analyst questions, and audit-focus refs
- explicit non-execution semantics through `execution_authorized: False`

Preserved exclusions:

- no `backend\tests\test_runtime_service.py`
- no `backend\app\runtime_service.py`
- no `backend\app\main.py`
- no public endpoint work
- no runtime/API/schema behavior
- no `backend\app\tools\persistent_case.py`
- no fixtures, dependencies, release scripts, contracts, real data, credentials, evidence retention, redaction policy freeze, parked-stream reopen, Red-3 action, or AI_COLLAB

Full gate/package/release verification passed for the implementation closeout. Staging, commit, and push remain separately governed under `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md` Section 10.

Selected route:

- `OPEN_S5C_IMPL7_CASE_REVIEW_SURFACE_TICKET_PREP`

This route may draft a Green docs-only ticket-prep artifact for a possible later S5-C-IMPL-7 scoped implementation ticket.

The candidate future task is internal case review surface/read-model hardening using existing governed case data. The future implementation candidate must remain bounded to `backend\app\agents\case_view.py` and `backend\tests\test_case_view.py` unless a later ticket explicitly includes `backend\tests\test_runtime_service.py` to protect existing runtime payload assertions.

The follow-up route must not implement anything. It must preserve:

- public close-case endpoint `KEEP_DEFERRED`
- S5-B `PASS_AND_PARK`
- S5-D `PASS_AND_PARK`
- ORDIV-L1A `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs `NOT_READY` / `UNKNOWN`
- external pilot execution unauthorized
- S4-A resolver order `asset_id -> hostname -> fqdn -> ip_address -> aliases`
- AI_COLLAB unchanged

Candidate exclusions remain `backend\app\runtime_service.py`, `backend\app\main.py`, public endpoint/API/schema files, fixtures, dependencies, release scripts, contracts, AI_COLLAB, real data, credentials, and any runtime behavior. Any later implementation remains HOLD until a separate scoped ticket, required review, explicit GO, full gate, release verification, and governed closeout are complete.

## 15. Next Product Development Route Selection After S5-C-IMPL-7

Selected next route:

- `OPEN_POST_S5C_IMPL7_ROUTE_DECISION_STAGE`

This route may draft a Green docs-only post-IMPL7 route-decision artifact. It is selected because S5-C-IMPL-5, S5-C-IMPL-6, and S5-C-IMPL-7 have all closed their bounded implementation scopes, and the next implementation candidate should not be invented without a route decision that reviews remaining product gaps.

The route-decision stage may evaluate:

- whether to open `OPEN_S5C_STREAM_REVIEW_REFRESH_STAGE`
- whether a precise `OPEN_S5C_IMPL8_SCOPED_IMPLEMENTATION_TICKET_PREP` candidate exists
- whether external input tracker refresh is the safer next Green docs-only blocker-reduction route
- whether to park/wait for product input

The follow-up route must not implement anything. It must preserve:

- public close-case endpoint `KEEP_DEFERRED`
- S5-B `PASS_AND_PARK`
- S5-D `PASS_AND_PARK`
- ORDIV-L1A `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs `NOT_READY` / `UNKNOWN`
- external pilot execution unauthorized
- S4-A resolver order `asset_id -> hostname -> fqdn -> ip_address -> aliases`
- AI_COLLAB unchanged

Fallback if exact future product-development scope cannot be safely named:

- `PARK_AND_WAIT_FOR_PRODUCT_INPUT`

## 16. Post S5-C-IMPL-7 Route Decision

Selected next route:

- `OPEN_S5C_STREAM_REVIEW_REFRESH_STAGE`

This route may draft a Green docs-only S5-C stream review refresh. It should review S5-C planning and the S5-C-IMPL-5, S5-C-IMPL-6, and S5-C-IMPL-7 implementation closeouts together before naming any further implementation gap.

The follow-up route may decide among:

- `S5_C_STREAM_COMPLETE_AND_PARK`
- `OPEN_S5C_IMPL8_SCOPED_IMPLEMENTATION_TICKET_PREP`
- `OPEN_AUTONOMOUS_YELLOW_BACKLOG_PREAUTH_STAGE`
- `OPEN_EXTERNAL_INPUT_TRACKER_REFRESH_DOCS_ONLY`

Vacation-mode posture:

- Green docs-only stages can proceed through review, full gate, release verification, manifest PASS, and closeout under AHQ-019 when exact scope/no-HOLD conditions pass.
- Yellow implementation can proceed during human absence only after exact scoped ticket/GO or a later governed preauthorization package defines files, behavior, tests, review path, and HOLD criteria.
- Red, launch, deployment, external pilot execution, real data, credentials, public endpoint activation, parked-stream reopen, Red-3, S4-A resolver change, and AI_COLLAB changes remain unavailable to unattended automation.

This route decision does not authorize implementation, code/test/dependency/fixture/runtime/API/schema/release-script/contract changes, Yellow implementation, Red execution, launch, deployment, external pilot readiness/execution, credentials, real data, evidence retention, redaction policy freeze, public endpoint work, S5-B/S5-D reopen, ORDIV work, S4-A resolver change, Red-3 action, AI_COLLAB changes, AdsPower profile creation/switching, Claude Web login automation, Claude Code file edits/command execution/tests, staging, commit, or push.

## 17. S5-C Stream Review Refresh

Stream decision:

- `S5_C_STREAM_REFRESH_PASS_WITH_YELLOW_BACKLOG_PREAUTH`

This route keeps S5-C moving through exact internal Yellow helper/test hardening rather than parking the stream or inventing a broad IMPL8 scope.

Preauthorized Yellow backlog after this stage closes PASS:

- `S5C-YB-01` internal workflow summary helper
- `S5C-YB-02` audit event vocabulary guard
- `S5C-YB-03` pending action-request boundary helpers
- `S5C-YB-04` case-view review-guidance regression hardening, test-only

The source artifact for exact files, tests, and HOLD rules is `docs\S5C_AUTONOMOUS_YELLOW_BACKLOG_PREAUTHORIZATION.md`.

Default execution order:

1. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_01`
2. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_02`
3. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_03`
4. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_04`

Each item must run one at a time, must obtain implementation review PASS, targeted tests PASS, full gate PASS, release verification PASS, manifest PASS, exact staged scope, and no-HOLD before closeout commit/push.

Still parked/deferred:

- public close-case endpoint remains `KEEP_DEFERRED`
- S5-B remains `PASS_AND_PARK`
- S5-D remains `PASS_AND_PARK`
- ORDIV-L1A remains `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs remain `NOT_READY` / `UNKNOWN`
- external pilot execution remains unauthorized
- S4-A resolver order remains unchanged
- AI_COLLAB remains unchanged

This route does not authorize unlisted implementation, runtime/API/schema work, public endpoint work, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, or AI_COLLAB changes.

## 19. S5-C-IMPL-9 Audit Event Vocabulary Guard Closeout

Closed route:

- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_02`

This route records the second bounded Yellow backlog item from `docs\S5C_AUTONOMOUS_YELLOW_BACKLOG_PREAUTHORIZATION.md`.

Implemented scope:

- governed audit event vocabulary constant in `backend\app\tools\persistent_case.py`
- sorted read helper `governed_audit_event_types()`
- `_require_audit_event_type()` validation helper
- validation during audit-entry deserialization and persistent-case serialization validation
- synthetic action-request contract tests in `backend\tests\test_case_action_request_contract.py`
- synthetic store serializer validation in `backend\tests\test_case_store.py`

Still parked/deferred:

- public close-case endpoint remains `KEEP_DEFERRED`
- S5-B remains `PASS_AND_PARK`
- S5-D remains `PASS_AND_PARK`
- ORDIV-L1A remains `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs remain `NOT_READY` / `UNKNOWN`
- external pilot execution remains unauthorized
- S4-A resolver order remains unchanged
- AI_COLLAB remains unchanged

Next default autonomous route:

1. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_03`
2. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_04`

Each remaining item must still run one at a time under exact item-specific files, tests, review, full gate, release verification, manifest PASS, staged scope, and HOLD rules.

This route does not authorize new audit event types, migrations, backfills, unlisted implementation, runtime/API/schema work, public endpoint work, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, or AI_COLLAB changes.

## 20. S5-C-IMPL-10 Pending Action Request Boundary Helpers Closeout

Closed route:

- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_03`

This route records the third bounded Yellow backlog item from `docs\S5C_AUTONOMOUS_YELLOW_BACKLOG_PREAUTHORIZATION.md`.

Implemented scope:

- `pending_action_request_ids(record)` in `backend\app\tools\persistent_case.py`
- `has_pending_action_requests(record)` in `backend\app\tools\persistent_case.py`
- workflow summary pending count derived from the pending helper
- synthetic action-request contract tests in `backend\tests\test_case_action_request_contract.py`
- synthetic lifecycle regression tests in `backend\tests\test_case_lifecycle_regression.py`

Still parked/deferred:

- public close-case endpoint remains `KEEP_DEFERRED`
- S5-B remains `PASS_AND_PARK`
- S5-D remains `PASS_AND_PARK`
- ORDIV-L1A remains `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs remain `NOT_READY` / `UNKNOWN`
- external pilot execution remains unauthorized
- S4-A resolver order remains unchanged
- AI_COLLAB remains unchanged

Next default autonomous route:

1. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_04`

The remaining item must still run under exact item-specific files, tests, review, full gate, release verification, manifest PASS, staged scope, and HOLD rules.

This route does not authorize endpoint behavior, runtime/API/schema work, public endpoint work, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, or AI_COLLAB changes.

## 18. S5-C-IMPL-8 Internal Workflow Summary Closeout

Closed route:

- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_01`

This route records the first bounded Yellow backlog item from `docs\S5C_AUTONOMOUS_YELLOW_BACKLOG_PREAUTHORIZATION.md`.

Implemented scope:

- read-only `persistent_case_workflow_summary(record)` helper in `backend\app\tools\persistent_case.py`
- lifecycle/action-request/audit/close-reason summary semantics derived only from `PersistentCaseRecord`
- synthetic lifecycle regression tests in `backend\tests\test_case_lifecycle_regression.py`
- synthetic store round-trip tests in `backend\tests\test_case_store.py`

Still parked/deferred:

- public close-case endpoint remains `KEEP_DEFERRED`
- S5-B remains `PASS_AND_PARK`
- S5-D remains `PASS_AND_PARK`
- ORDIV-L1A remains `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs remain `NOT_READY` / `UNKNOWN`
- external pilot execution remains unauthorized
- S4-A resolver order remains unchanged
- AI_COLLAB remains unchanged

Next default autonomous route:

1. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_02`
2. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_03`
3. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_04`

Each remaining item must still run one at a time under exact item-specific files, tests, review, full gate, release verification, manifest PASS, staged scope, and HOLD rules.

This route does not authorize unlisted implementation, runtime/API/schema work, public endpoint work, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, or AI_COLLAB changes.

## 21. S5-C-IMPL-11 Case View Review Guidance Regression Hardening Closeout

Closed route:

- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_04`

This route records the fourth bounded Yellow backlog item from `docs\S5C_AUTONOMOUS_YELLOW_BACKLOG_PREAUTHORIZATION.md`.

Implemented scope:

- synthetic case-view review-guidance regression tests in `backend\tests\test_case_view.py`
- no-chain complete case non-execution guidance coverage
- low-confidence case analyst-review guidance coverage
- degraded case suggested-action disabled execution coverage
- partial evidence-gap bounded question coverage
- top-level case-view panel preservation guard
- `analysis_limits["review_guidance"]` location preservation guard

Still parked/deferred:

- public close-case endpoint remains `KEEP_DEFERRED`
- S5-B remains `PASS_AND_PARK`
- S5-D remains `PASS_AND_PARK`
- ORDIV-L1A remains `PARK_LOCAL_VALIDATION_NO_REPORT`
- external pilot inputs remain `NOT_READY` / `UNKNOWN`
- external pilot execution remains unauthorized
- S4-A resolver order remains unchanged
- AI_COLLAB remains unchanged

Next recommended autonomous route:

1. `OPEN_AUTONOMOUS_YELLOW_BACKLOG_TEMPLATE_ANTI_OVERENGINEERING_REFRESH_STAGE`

The recommended next route is Green docs-only and should add anti-overengineering and max-change-budget rules to the next Yellow backlog preauthorization template. It must not mix with this YB-04 closeout.

This route does not authorize production code changes, runtime/API/schema work, public endpoint work, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, or AI_COLLAB changes.

## 22. Autonomous Yellow Backlog Template Anti-Overengineering Refresh

Current route:

1. `OPEN_AUTONOMOUS_YELLOW_BACKLOG_TEMPLATE_ANTI_OVERENGINEERING_REFRESH_STAGE`

This Green docs-only route updates autonomous operations guidance after the final preauthorized S5-C Yellow backlog item closed.

Updated planning posture:

- active autonomous cadence is every 1 hour
- local Claude Code review-only process-spawn failure can fall back to the verified AdsPower Claude Web review-prompt path when safe
- future Yellow backlog preauthorization packages must use the reusable anti-overengineering template
- each future Yellow item must name exact allowed files, exact tests, exact allowed behavior, max-change budget, review checklist, and HOLD conditions
- unnecessary abstraction, speculative generalization, broad cleanup, and while-we-are-here work are explicit review risks

Next possible route after this stage closes PASS:

1. `OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE`

This route does not authorize implementation, code/test changes, runtime/API/schema work, public endpoint work, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, AI_COLLAB changes, AdsPower profile creation/switching, Claude Web login automation, or Claude Code file edits/command execution/tests/staging/commit/push.

## 23. Current Phase Summary Refresh

Current route:

1. `OPEN_CURRENT_PHASE_SUMMARY_REFRESH_STAGE`

This Green docs-only route creates the governed current phase summary at `docs\SECUPILOT_PHASE_SUMMARY_20260421.md`.

Updated planning posture:

- the stale root summary `SecuPilot_阶段性总结_20260409.md` is superseded for orientation
- current completed automation and S5-C product-development work is summarized in a manifest-governed doc
- remaining HOLDs are listed as boundaries rather than blockers to bounded Green/Yellow progress
- next recommended route remains `OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE`
- future Yellow packages should use `docs\AUTONOMOUS_YELLOW_BACKLOG_PREAUTHORIZATION_TEMPLATE.md`

This route does not authorize implementation, code/test changes, runtime/API/schema work, public endpoint work, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, AI_COLLAB changes, AdsPower profile creation/switching, Claude Web login automation, or Claude Code file edits/command execution/tests/staging/commit/push.

## 24. Next Product Development Route Selection

Current route:

1. `OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE`

Selected next route:

1. `OPEN_NEXT_YELLOW_BACKLOG_PREAUTHORIZATION_STAGE`

This Green docs-only route should prepare the next exact Yellow backlog preauthorization package from the current governed baseline. It should use `docs\AUTONOMOUS_YELLOW_BACKLOG_PREAUTHORIZATION_TEMPLATE.md` and may park if no exact bounded internal product item is ready.

SWE agent posture:

- current state is `NOT_INSTALLED_OR_NOT_VERIFIED`
- not part of the current autonomous execution path
- future role may be bounded implementation accelerator only after `OPEN_SWE_AGENT_CAPABILITY_VERIFICATION_STAGE`
- absence does not block Green docs-only route selection or ordinary Codex/VS Code scoped Yellow work

This route does not authorize implementation, code/test changes, runtime/API/schema work, public endpoint work, SWE agent installation/execution/integration, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, AI_COLLAB changes, AdsPower profile creation/switching, Claude Web login automation, or Claude Code file edits/command execution/tests/staging/commit/push.

## 25. Next Yellow Backlog Preauthorization

Current route:

1. `OPEN_NEXT_YELLOW_BACKLOG_PREAUTHORIZATION_STAGE`

Prepared package:

1. `docs\NEXT_YELLOW_BACKLOG_PREAUTHORIZATION.md`

Prepared future Yellow items:

1. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_05` / `S5C-YB-05`: reopen lifecycle audit regression, test-only in `backend\tests\test_case_lifecycle_regression.py`.
2. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_06` / `S5C-YB-06`: action-request terminal guard regression, expected test-only in `backend\tests\test_case_action_request_contract.py`, with `backend\app\tools\persistent_case.py` allowed only for a bounded existing-helper enforcement bug.
3. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_07` / `S5C-YB-07`: workflow summary immutability regression, test-only in `backend\tests\test_case_lifecycle_regression.py`.

Next default route after this stage closes PASS:

1. `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_05`

Execution posture:

- each item runs one at a time
- each item uses exact allowed files and tests
- anti-overengineering rules prohibit speculative abstraction, broad cleanup, new helpers/modules/frameworks unless item-named, and hidden scope expansion
- SWE agent remains `NOT_INSTALLED_OR_NOT_VERIFIED` and outside this package

This route does not authorize implementation during this docs-only package stage, unlisted Yellow items, unlisted files, runtime/API/schema work, public endpoint work, SWE agent installation/execution/integration, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, AI_COLLAB changes, AdsPower profile creation/switching, Claude Web login automation, or Claude Code file edits/command execution/tests/staging/commit/push outside exact item closeout rules.

## 26. SWE Agent Capability Verification

Current route:

1. `OPEN_SWE_AGENT_CAPABILITY_VERIFICATION_STAGE`

Verification result:

- SWE agent is not installed or discoverable
- no governed local command path exists
- no pip package or Python module exists in the current environment
- no dry run was possible
- no install or execution was performed

Current status:

1. `HOLD_FOR_TOOL_INSTALL_AND_VERIFICATION`

Future possible route:

1. `OPEN_SWE_AGENT_INSTALL_AND_CAPABILITY_VERIFICATION_STAGE`

Future verification must prove repo-root confinement, exact file-scope confinement, harmless dry run, no secret or real-data access, no dependency install without approval, no staging/commit/push, before/after git status, and external review before SWE agent can be used as a bounded implementation accelerator.

This route does not authorize SWE agent installation, SWE agent execution, Yellow backlog participation, code/test changes, dependency changes, runtime/API/schema work, public endpoint work, review replacement, route selection, manifest/gate/release ownership, staging, commit, push, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, AI_COLLAB changes, AdsPower profile creation/switching, Claude Web login automation, or cookie/session/token/auth-header inspection.

## 27. SWE Agent Install And Capability Verification

Current route:

1. `OPEN_SWE_AGENT_INSTALL_AND_CAPABILITY_VERIFICATION_STAGE`

Verification result:

- official tool selection is `mini-swe-agent`
- `mini-swe-agent` version `2.2.8` is present in user Python site-packages
- `mini-extra` help is callable and package import succeeds
- main `mini` / `mini-swe-agent` entrypoint fails in the current Codex non-interactive Windows shell with `NoConsoleScreenBufferError`
- no harmless no-write agent dry run was completed
- no repo-root confinement, exact file-scope confinement, mutation control, or Yellow backlog compatibility was proven

Current status:

1. `PARTIAL_VERIFIED_INSTALL_HELP_ONLY_EXECUTION_HOLD`

Future possible route:

1. `OPEN_MINI_SWE_AGENT_NONINTERACTIVE_DRY_RUN_VERIFICATION_STAGE`

Future verification must prove callable main-agent behavior, harmless no-write dry run, repo-root confinement, exact file-scope confinement, no secret or real-data access, no dependency install without approval, no staging/commit/push, before/after git status, and external review before SWE agent can be used as a bounded implementation accelerator.

This route does not authorize SWE agent execution, Yellow backlog participation, implementation assistance, code/test changes, dependency changes, runtime/API/schema work, public endpoint work, review replacement, route selection, manifest/gate/release ownership, staging, commit, push, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, AI_COLLAB changes, AdsPower profile creation/switching, Claude Web login automation, or cookie/session/token/auth-header inspection.

## 28. Mini SWE Agent Noninteractive Dry Run Verification

Current route:

1. `OPEN_MINI_SWE_AGENT_NONINTERACTIVE_DRY_RUN_VERIFICATION_STAGE`

Verification result:

- WSL2 exists only as `docker-desktop`, not a governed user distro
- probed WSL shell lacked `bash`, had an empty `PATH`, and did not expose usable Python or mini-swe-agent commands
- `winpty` is unavailable
- `cmd.exe /c` still fails with `NoConsoleScreenBufferError`
- no harmless no-write main-agent dry run was completed

Current status:

1. `HOLD_WSL_PTY_DRY_RUN_NOT_AVAILABLE`

Future possible route:

1. `OPEN_MINI_SWE_AGENT_PTY_RUNNER_PROVISIONING_STAGE`

Future provisioning must establish a normal user-controlled WSL2 distro or equivalent PTY runner, exact command path/version, no-write dry run, repo-root confinement, exact file-scope confinement, no secret or real-data access, no dependency install without approval, no staging/commit/push, before/after git status, and external review before SWE agent can be used as a bounded implementation accelerator.

This route does not authorize SWE agent execution, Yellow backlog participation, implementation assistance, WSL distro installation, PTY runner installation, code/test changes, dependency changes, runtime/API/schema work, public endpoint work, review replacement, route selection, manifest/gate/release ownership, staging, commit, push, Red execution, launch, deployment, real data, credentials, external pilot, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver change, AI_COLLAB changes, AdsPower profile creation/switching, Claude Web login automation, or cookie/session/token/auth-header inspection.
