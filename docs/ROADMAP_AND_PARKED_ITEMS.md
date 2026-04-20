# Roadmap And Parked Items

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Roadmap And Parked Items |
| Status | Rolling governed roadmap and parked-items map |
| Snapshot | S5C-IMPL7-CASE-REVIEW-SURFACE-TICKET-PREP-2026-04-20-001 |
| Stage | s5c-impl7-case-review-surface-ticket-prep |
| Baseline commit | `7af8841a10685c0420fdea8c3a6bddef2c207f51` |

This file summarizes parked, deferred, and possible future routes. It is a passive governed context and planning aid only. It does not authorize implementation, reopen parked streams, create pilot readiness, or override source governed docs.

## 2. Current Mainline Posture

The current governed mainline outcome is next product-development route selection after S5-C-IMPL-6 implementation closeout.

The route selection chooses Green docs-only preparation for a possible later S5-C-IMPL-7 case review surface ticket. It does not authorize implementation, launch execution, deployment, real-data handling, public endpoint work, login route, AdsPower profile switching/creation, parked-stream reopen, runtime/API/schema behavior, or additional implementation.

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

The autonomous operation startup path adds a default 2-hour operating cadence for safe Green/Yellow docs-only drafting and closeout-gate preparation. During day 1, staging, commit, and push still require explicit human confirmation. Startup does not close AHQ-003 through AHQ-014, does not remove AHQ-017 ambiguity handling, and does not authorize Red execution beyond exact per-action policy requirements.

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
