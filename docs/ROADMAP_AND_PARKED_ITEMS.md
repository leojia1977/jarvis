# Roadmap And Parked Items

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Roadmap And Parked Items |
| Status | Rolling governed roadmap and parked-items map |
| Snapshot | S5-ADSPOWER-CLAUDE-WEB-AUTOMATION-VERIFICATION-2026-04-18-001 |
| Stage | s5-adspower-claude-web-automation-verification |
| Baseline commit | `bfd0920050d4780866dfdaba88fd3c7afece4e0c` |

This file summarizes parked, deferred, and possible future routes. It is a passive governed context and planning aid only. It does not authorize implementation, reopen parked streams, create pilot readiness, or override source governed docs.

## 2. Current Mainline Posture

The current governed mainline outcome is `PARK_AND_WAIT_FOR_PRODUCT_INPUT`.

The human product/governance input for this stage opens only this AdsPower / Claude Web automation verification route. It does not open a next implementation scoped ticket, launch execution route, deployment route, real-data route, public endpoint route, login route, broader AdsPower profile-launch route, or parked-stream reopen route. Future work requires a separate governed route or ticket with review and human or delegated decision where policy permits.

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

The autonomous toolchain integration path defines a four-tool collaboration model and current capability matrix. It may reduce planning risk by clarifying Codex, VS Code, Claude Code through the user-configured `cc switch` API tool, Claude Web running in the user's AdsPower browser/profile, Git, and release/gate boundaries, but it does not claim full four-tool automation. AdsPower Local API is reachable locally but requires API-key authentication, so any future automation route needs a human-controlled non-secret API-key provisioning path. AHQ-020 through AHQ-022 remain HOLD until Claude Code non-interactive review through `cc switch`, AdsPower/Claude Web automation, and AdsPower browser/profile/session control are separately governed and verified.

The AdsPower Claude Web automation verification path verifies only a harmless review-prompt round trip through an already-active AdsPower profile and already-open Claude Web page. It may unlock safe future review-prompt transfer, but it does not unlock AdsPower profile launch/switch control, login automation, secrets/session inspection, high-risk review substitution, Red execution, launch, deployment, external pilot execution, public endpoint work, real-data handling, S5-B/S5-D reopen, ORDIV work, or Red-3 action.

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
