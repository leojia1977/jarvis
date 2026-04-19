# Roadmap And Parked Items

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Roadmap And Parked Items |
| Status | Rolling governed roadmap and parked-items map |
| Snapshot | S5-CC-SWITCH-COMMAND-PATH-PROVISIONING-2026-04-19-001 |
| Stage | s5-cc-switch-command-path-provisioning |
| Baseline commit | `5c1d8c1e288c1e16f47279f147fc4a973064e874` |

This file summarizes parked, deferred, and possible future routes. It is a passive governed context and planning aid only. It does not authorize implementation, reopen parked streams, create pilot readiness, or override source governed docs.

## 2. Current Mainline Posture

The current governed mainline outcome is `PARK_AND_WAIT_FOR_PRODUCT_INPUT`.

The human product/governance input for this stage opens only the cc switch command-path provisioning route for Claude Code review-only verdict capture. It does not open a next implementation scoped ticket, launch execution route, deployment route, real-data route, public endpoint route, login route, AdsPower profile switching/creation route, Claude Code implementation route, Claude Code file-edit route, or parked-stream reopen route. Future work requires a separate governed route or ticket with review and human or delegated decision where policy permits.

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
