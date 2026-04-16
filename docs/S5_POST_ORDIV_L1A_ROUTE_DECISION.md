# Sprint 5 Post-ORDIV-L1A Route Decision

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Sprint 5 Post-ORDIV-L1A Route Decision |
| Status | Closed as governed Sprint 5 post-ORDIV-L1A route decision baseline |
| Scope | Docs-only route decision after ORDIV-L1A parked local validation no-report state |
| Baseline snapshot | ORDIV-L1A-REAL-DATA-VALIDATION-SCOPED-DECISION-2026-04-16-001 |
| Baseline stage | ordiv-l1a-real-data-validation-scoped-decision |
| Baseline commit | `a589216bf7dd8689dd955847b5239a0cee2bb65a` |
| Route | RETURN_TO_SPRINT5_MAINLINE_ROUTE_DECISION |
| Codex role | planning and prompt orchestration only |
| Draft creator | VS Code / human-supervised workspace |
| Reviewer | Claude Code review-only |
| Claude Web posture | Not required for this docs-only route decision unless this draft selects report governance with real-data output, CSV input contract freeze, L1B real telemetry handling, pilot readiness claim, frozen contract modification, evidence retention, redaction policy freeze, dependency governance change, or stream/milestone closeout |

This is a docs-only route decision baseline. It does not change the governed ORDIV-L1A baseline and does not authorize report creation, further real-data work, or any implementation activity.

Review closeout note: Claude Code review-only returned `GO` with no `HIGH`, `MEDIUM`, or `LOW` findings. `INFO-1` was addressed by explicitly adding raw filenames and raw full local paths to the non-authorization list. Claude Web is not required before this docs-only route decision closeout.

Closeout lineage note: test-only gate stabilization commit `0f34bbf3caa7501ef9ec8ae6d0085850b9b53bcd` was inserted after the original draft/review and before this route decision closeout. That repair changed only `backend/tests/test_edr_replay.py` to stabilize EDR replay investigate-window tests and does not change the governed ORDIV-L1A route substance or any real-data boundary.

## 2. Goal

Decide the next Sprint 5 route after ORDIV-L1A has been safely parked at `PARK_LOCAL_VALIDATION_NO_REPORT`.

The goal is to return from the bounded ORDIV-L1A local validation lane to Sprint 5 product/governance route selection without recording validation metrics, creating report artifacts, expanding input formats, opening L1B/syslog work, or implying pilot readiness.

## 3. Current Status Summary

- ORDIV-L1A adapter implementation is governed.
- Implemented files are `backend/app/tools/siem_alert_file_adapter.py` and `backend/tests/test_siem_alert_file_adapter.py`.
- Synthetic tests and full gate passed during implementation closeout.
- Real-data validation scoped decision is governed at current baseline `ORDIV-L1A-REAL-DATA-VALIDATION-SCOPED-DECISION-2026-04-16-001`.
- A local-only real `.xlsx` validation run occurred under Claude Web gate and human GO conditions.
- The run completed with no HOLD, no raw-value leak detected, no repo changes, no report artifact, and no staged/committed/pushed files.
- No metric values, row counts, distributions, success rates, real paths, filenames, sheet names, row values, cell values, IPs, hosts, users, IOCs, credentials, SQL, payloads, screenshots, or secrets are recorded in this draft.
- Current ORDIV-L1A posture is `PARK_LOCAL_VALIDATION_NO_REPORT`.
- This draft does not change the governed ORDIV-L1A baseline and does not authorize report creation or further real-data work.

## 4. Inherited Boundaries

- S5-B and S5-D remain `PASS_AND_PARK`.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- External pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- AI_COLLAB remains unchanged.

## 5. Candidate Routes

| Route | Meaning | Risk | Claude Web implication | Recommendation |
| --- | --- | --- | --- | --- |
| `RETURN_TO_SPRINT5_MAINLINE_ROUTE_DECISION` | Park ORDIV-L1A no-report state and return to Sprint 5 product/governance route selection. | Low; may delay report/CSV/L1B learning. | Not required for this docs-only route decision. | Preferred. |
| `OPEN_VALIDATION_REPORT_GOVERNANCE_ROUTE` | Later decide whether redacted/count-based validation metrics may become a repo artifact. | Metric/report leakage, pilot-readiness implication, evidence/redaction policy adjacency. | Required before any report route. | Defer unless report artifact is explicitly needed. |
| `OPEN_CSV_INPUT_FORMAT_ROUTE_DECISION` | Separately evaluate CSV input handling for available CSV files. | Input-format expansion, possible new contract, real-data adjacency. | Required if it freezes a CSV input contract, touches real data, or modifies adapter scope beyond governed XLSX. | Possible later route, not immediate default. |
| `OPEN_L1B_SYSLOG_ROUTE_DECISION` | Separately evaluate L1B/syslog/firewall-log route. | Real telemetry/log handling, redaction/evidence boundaries, S5-D telemetry adjacency. | Likely required before real telemetry handling. | Possible later route, not immediate default. |
| `CONTINUE_AD_HOC_REAL_DATA_WORK` | Continue using real files or metrics without a governed route. | Violates no-report/no-artifact park boundary. | Route should HOLD. | NOT_RECOMMENDED / HOLD. |

## 6. Recommended Route

Preferred route:

`RETURN_TO_SPRINT5_MAINLINE_ROUTE_DECISION`

Meaning:

- ORDIV-L1A remains parked at `PARK_LOCAL_VALIDATION_NO_REPORT`.
- Sprint 5 product/governance route selection should decide the next mainline direction.
- No validation metrics, report artifacts, real workbook details, CSV handling, L1B/syslog handling, implementation work, or pilot readiness claims are introduced by this route decision.

Fallback:

`PARK_ORDIV_L1A_NO_REPORT_AND_WAIT`

Use the fallback if the human does not want to choose the next Sprint 5 mainline route immediately.

## 7. Why Not The Other Routes Now

- `OPEN_VALIDATION_REPORT_GOVERNANCE_ROUTE` is deferred because any report artifact needs separate external review and exact allowed fields/examples before any metrics can be recorded.
- `OPEN_CSV_INPUT_FORMAT_ROUTE_DECISION` is not the immediate default because CSV handling could expand input contracts and real-data adjacency beyond the governed XLSX adapter lane.
- `OPEN_L1B_SYSLOG_ROUTE_DECISION` is not the immediate default because real telemetry/log handling touches S5-D adjacency, redaction/evidence boundaries, and likely Claude Web review requirements.
- `CONTINUE_AD_HOC_REAL_DATA_WORK` is HOLD because it would bypass the governed no-report/no-artifact park boundary.

## 8. Claude Web Trigger Conditions

Claude Web is not required for this docs-only route decision as long as it only parks ORDIV-L1A and returns to Sprint 5 mainline routing.

Claude Web is required before selecting or executing any route that includes:

- report governance with real-data output
- tracked validation report artifact
- CSV input contract freeze
- L1B real telemetry/log handling
- external pilot readiness claim
- frozen contract modification
- evidence retention
- redaction policy freeze
- dependency governance change
- stream/milestone closeout

## 9. Non-Authorization

This draft does not authorize:

- code changes
- test changes
- dependency changes
- runtime/config integration
- `SIEMAdapterProtocol` changes
- report creation
- metric recording
- validation report artifact
- real-data validation rerun
- workbook access/listing/opening/parsing/copying/inspection/summarization/upload/retention
- raw filenames or raw full local paths in repo, review material, prompts, reports, logs, or commits
- CSV processing
- L1B syslog/log parsing
- evidence retention
- redaction policy freeze
- external pilot readiness
- external pilot execution
- real customer/operator sign-off
- S5-B reopen
- S5-D reopen
- S4-A resolver changes
- public close-case endpoint work
- AI_COLLAB changes
- staging
- commit
- push

## 10. HOLD Conditions

Hold this route if any of the following occur:

- Any attempt to record validation metrics without report governance.
- Any real path, filename, sheet name, row value, cell value, IP, host, user, IOC, credential, SQL, payload, screenshot, or secret enters the draft, prompt, repo, review material, report, log, or commit.
- Any CSV processing is attempted from this route decision.
- Any L1B/syslog parsing is attempted from this route decision.
- Any report artifact is requested without separate report governance.
- Any claim appears that ORDIV-L1A validation improves or implies pilot readiness.
- Any code/test/dependency/runtime/config/protocol change is requested.
- Any S5-B boundary change is requested.
- Any S5-D boundary change is requested.
- Any S4-A boundary change is requested.
- Any AI_COLLAB boundary change is requested.
- Any public close-case boundary change is requested.

## 11. Acceptance Criteria

This docs-only route decision draft is acceptable if:

- exactly one new docs-only file is created
- no code files are changed
- no test files are changed
- no dependency files are changed
- `docs/HANDOFF.md` is not changed
- `releases/release_manifest.json` is not changed
- no real data is touched
- no workbook is accessed, listed, opened, parsed, copied, inspected, summarized, uploaded, retained, or validated
- no CSV is accessed or processed
- no syslog/log source is accessed or parsed
- no report artifact is created
- ORDIV-L1A park state is clear
- candidate routes are compared
- recommended route is `RETURN_TO_SPRINT5_MAINLINE_ROUTE_DECISION`
- Claude Web trigger conditions are explicit
- no staging, commit, push, or full gate is performed

## 12. Preliminary Recommendation

`PRELIMINARY_RECOMMENDATION_RETURN_TO_SPRINT5_MAINLINE_ROUTE_DECISION`

Meaning:

- Return to Sprint 5 product/governance route selection.
- Keep ORDIV-L1A parked at `PARK_LOCAL_VALIDATION_NO_REPORT`.
- Defer report governance, CSV input handling, and L1B/syslog decisions unless the human explicitly opens those later routes.

Non-meaning:

- Does not authorize report creation.
- Does not authorize metric recording.
- Does not authorize further real-data validation.
- Does not authorize CSV processing.
- Does not authorize L1B/syslog parsing.
- Does not imply external pilot readiness.
- Does not change the governed ORDIV-L1A implementation baseline.
