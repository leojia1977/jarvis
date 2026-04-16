# ORDIV-L1A-01 SIEM Alert XLSX Mapping Ticket Definition

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | ORDIV-L1A-01 SIEM Alert XLSX Mapping Ticket Definition |
| Status | Closed as governed ORDIV-L1A-01 docs-only ticket-definition baseline; not implementation authorization |
| Scope | Narrow future implementation boundary for a SIEM alert `.xlsx` file adapter only |
| Baseline | ORDIV-SCOPED-DECISION-2026-04-16-001 / commit `38d61ec` |
| Predecessor | docs/OFFLINE_REAL_DATA_INTEGRATION_SCOPED_DECISION.md |
| Route | ORDIV-L1A-01 SIEM alert `.xlsx` mapping ticket definition |
| Future implementation primary implementor | VS Code / human-supervised execution workspace |
| Current Codex role | planning only |
| Reviewer | Claude Code review-only |
| requires_external_review | true |

`requires_external_review` is true because this ticket definition concerns a future adapter boundary for offline real SIEM alert `.xlsx` data, output-side redaction, evidence-retention prohibitions, dependency approval risk, and S5-B/S5-D/S4-A-adjacent governance boundaries. External review does not authorize implementation and does not replace human go/no-go.

Review closeout note: Claude Code review found no HIGH, MEDIUM, or LOW blockers. INFO observations are non-blocking. `event_id` derivation remains deferred to a later implementation ticket.

## 2. Goal

Define the later implementation boundary for `ORDIV-L1A-01`, a narrow SIEM alert `.xlsx` file adapter candidate.

This document is not adapter implementation. It only defines the conditions under which a later implementation ticket may be drafted, reviewed, and accepted.

The future implementation candidate is limited to reading a repo-external SIEM alert `.xlsx` file, mapping known columns into existing SIEM-compatible alert dictionaries, and testing that mapping with synthetic in-repo data only.

## 3. Baseline Summary

- Current governed baseline is `ORDIV-SCOPED-DECISION-2026-04-16-001`.
- Current baseline commit is `38d61ec`.
- Predecessor decision is `docs/OFFLINE_REAL_DATA_INTEGRATION_SCOPED_DECISION.md`.
- ORDIV is a governed offline real-data integration validation route, separate from S5-C-IMPL-5.
- ORDIV-L1A-01 is the narrow first candidate for SIEM alert `.xlsx` mapping only.
- Raw real data remains outside the repo.
- External pilot readiness is not improved by this ticket definition.
- External pilot execution remains unauthorized.
- S5-B and S5-D remain parked unless a later explicit reopen decision is made.
- S4-A host identity resolver authority and order remain unchanged.
- Public close-case endpoint work remains out of scope.
- AI_COLLAB files and contracts remain unchanged.

## 4. Role Boundary

- VS Code / human-supervised workspace is the primary implementor for this docs-only draft.
- Codex role for this artifact is planning only.
- Claude Code role after draft is review-only.
- Future implementation, if later authorized by a separate ticket, must still name its own primary implementor, reviewer, external-review posture, and human go/no-go.
- This role boundary does not authorize code, test, dependency, fixture, runtime, release, or contract changes.

## 5. Non-Authorization

This draft does not authorize:

- implementation
- code changes
- tests
- dependency changes
- fixture creation or modification
- runtime integration
- API/schema changes
- config changes
- local real-data execution
- validation reports
- evidence retention
- redaction policy freeze
- pilot readiness
- external pilot execution
- real customer/operator sign-off
- S5-B reopen
- S5-D reopen
- S4-A resolver changes
- public close-case endpoint work
- AI_COLLAB operating model or contract changes
- release artifact changes
- HANDOFF, manifest, or verify-report changes
- staging, commit, or push

## 6. Future File Scope

If this ticket definition is later accepted, the future implementation candidate may be limited to these new files only:

| Future file | Scope | Guardrail |
| --- | --- | --- |
| `backend/app/tools/siem_alert_file_adapter.py` | New offline `.xlsx` alert file adapter that maps rows to existing SIEM-compatible alert dictionaries. | Must not modify existing SIEM adapter protocol, runtime service, graph, config, fixtures, or dependencies. |
| `backend/tests/test_siem_alert_file_adapter.py` | New synthetic-only unit tests for header handling, row mapping, partial/error semantics, and redaction-safe behavior. | Must not use real `.xlsx`, logs, screenshots, payloads, IPs, hostnames, usernames, IOC values, or customer/operator evidence. |

Any later implementation ticket must still restate exact file scope and may still HOLD if the scope cannot remain this narrow.

## 7. Out-of-Scope Files

Later implementation must HOLD if it needs to modify any of the following:

- `backend/app/tools/siem_adapter.py`
- `backend/app/config.py`
- `backend/app/runtime_service.py`
- `backend/app/agents/graph.py`
- `backend/tests/fixtures/**`
- dependency files
- release scripts
- AI_COLLAB files/contracts
- S5-B/S5-D/S4-A contract docs

Out-of-scope means no edits, no refactors, no compatibility shims, no fixture additions, and no indirect behavior changes in this ticket path.

## 8. Dependency Boundary

The only dependency candidate is `openpyxl`.

Use `openpyxl` only if it is already available in the current environment and no dependency file changes are needed.

If `openpyxl` is unavailable, if a new package is needed, or if any dependency file must change, the later implementation must HOLD for dependency approval and external review.

This draft does not authorize dependency installation, dependency pin changes, lockfile changes, package metadata changes, or fallback parser work that expands file scope.

## 9. Data Boundary

No real `.xlsx`, syslog, device logs, payloads, SQL, IPs, hostnames, usernames, account IDs, IOC values, screenshots, customer/operator evidence, credentials, tokens, API keys, auth headers, cookies, or secret material may enter:

- repository files
- fixtures
- prompts
- commits
- reports
- generated review material
- release artifacts
- screenshots
- issue text
- copied examples
- AI review packets

Any future real-data validation must use repo-external local paths only and must not retain or copy raw source material into the repo.

## 10. Redaction and Evidence Boundary

Raw input values may not leave the local validation boundary unredacted.

Any future validation output, if separately authorized, must redact or syntheticize:

- source and destination IPs
- affected host labels and host IPs
- usernames and account identifiers
- IOC values
- SQL or payload-like values
- CVE-like values if tied to customer/operator evidence
- detection engine values if they identify a customer/operator environment
- screenshots or copied table rows

This ticket definition does not authorize evidence retention, validation report retention, screenshot retention, evidence-pack behavior, replay storage, deletion/expiry policy, or redaction policy freeze.

## 11. Target Alert Shape

The future adapter candidate may emit existing SIEM-compatible alert dictionaries only, using this key set:

- `event_id`
- `event_time`
- `severity`
- `activity_name`
- `source_ip`
- `destination_ip`
- `destination_asset_id`
- `extra`

This target shape does not authorize new schema, persisted fields, API fields, runtime contracts, or changes to `SIEMAdapterProtocol`.

The later implementation ticket must decide how `event_id` is derived without storing raw evidence. This draft does not choose a hash, row number, persisted ID, or schema rule.

## 12. Field Mapping

Every mapping below is candidate boundary text for a later implementation ticket. It does not authorize implementation.

| Source field | Target field | Normalization | Must-not-imply guardrail | HOLD trigger |
| --- | --- | --- | --- | --- |
| `采集时间` | `event_time` | Parse only the exact confirmed timestamp format; unknown or invalid values produce partial behavior. | Must not freeze timestamp/freshness semantics or runtime clock behavior. | Timestamp format ambiguity requires broader semantics or schema changes. |
| `威胁名称` | `activity_name` and/or `extra.alert_name` | Use as the alert activity label after output-side redaction rules. | Must not authorize unredacted alert names in repo/review material or new schema fields. | Raw alert names leave local boundary or activity naming changes frozen contracts. |
| `威胁类型` | `extra.threat_category` | Preserve as category text after output-side redaction if needed. | Must not freeze threat taxonomy or detection category normalization. | Taxonomy decisions become product/contract requirements. |
| `威胁等级` | `severity` | Map `高危`/`HIGH` to high, `中危`/`MEDIUM` to medium, `低危`/`LOW` to low; unknown values produce partial behavior. | Must not change existing severity contracts or imply alert routing/SLA. | Unknown severity needs new severity semantics or routing behavior. |
| `受影响主机` | `destination_asset_id` and/or `extra.affected_host_label` | Use only as a candidate destination label; redact before any output leaves local boundary. | Must not change S4-A host identity authority or resolver order. | Mapping requires resolver priority changes or real host labels enter repo. |
| `协议` | `extra.protocol` | Trim and preserve common protocol labels; unknown values remain in partial/extra handling if later scoped. | Must not freeze telemetry normalization. | Unknown protocol handling requires normalized telemetry contract changes. |
| `源Ip` | `source_ip` | Validate as IP-like locally; redact before output leaves local boundary. | Must not permit real IP retention or source authority changes. | Real source IP appears in repo, report, review packet, or prompt. |
| `源端口` | `extra.source_port` | Parse as integer-like text if valid; otherwise partial behavior. | Must not create new schema or API fields. | Port parsing requires schema or runtime contract changes. |
| `目标Ip` | `destination_ip` | Validate as IP-like locally; redact before output leaves local boundary. | Must not permit real IP retention or destination authority changes. | Real destination IP appears in repo, report, review packet, or prompt. |
| `目标端口` | `extra.destination_port` | Parse as integer-like text if valid; otherwise partial behavior. | Must not create new schema or API fields. | Port parsing requires schema or runtime contract changes. |
| `受影响主机ip` | `extra.affected_host_ip` | Validate as IP-like locally; redact before output leaves local boundary. | Must not change S4-A host identity behavior or retain real IP evidence. | Real affected-host IP appears outside local boundary or resolver behavior must change. |
| `状态` | `extra.outcome` | Map `攻击失败` to `blocked`, `疑似成功` to `suspected`, unknown values to `unknown`. | Must not change case lifecycle, action-request, or response semantics. | Outcome mapping becomes workflow/action semantics. |
| `数据来源` | `extra.detection_engine` | Preserve source label after redaction if it identifies an environment. | Must not freeze source authority, trust precedence, or provenance semantics. | Detection engine value changes S5-B/S5-D authority or trust ordering. |
| `CVE` | `extra.cve_id` | Preserve nullable CVE-like value only after redaction/evidence boundary review. | Must not authorize IOC/evidence retention or vulnerability workflow semantics. | CVE value becomes customer evidence, IOC retention, or workflow input. |

## 13. Header and Row Handling

Future implementation may define deterministic `.xlsx` sheet/header handling only inside the later implementation ticket.

Candidate row-handling boundaries:

- Header/title rows may be skipped only by exact column-name detection, not by fuzzy inference over real content.
- Empty rows may be ignored if every mapped source field is empty.
- Partially populated rows must not crash the adapter.
- Unknown columns must be ignored unless later scope explicitly maps them.
- Duplicate headers, missing required headers, or ambiguous header rows must produce partial/error semantics instead of guessing.
- Raw row values must not be logged, committed, copied, or included in review material.

## 14. Adapter Behavior Boundary

The later adapter, if authorized by a separate ticket, may be a narrow offline file adapter only.

It may:

- accept a repo-external `.xlsx` file path
- read the workbook locally
- map the 14 known fields into existing SIEM-compatible alert dictionaries
- return partial/error information for invalid rows or missing headers
- avoid network access entirely
- avoid persistent storage entirely

It must not:

- connect to SIEM, EDR, Metron, Kafka, Solr, Elastic, source, or telemetry systems
- modify `SIEMAdapterProtocol`
- modify runtime service behavior
- modify graph/orchestrator behavior
- add config knobs
- create fixtures
- retain raw data
- emit unredacted validation reports
- imply pilot readiness

## 15. Partial / Error Semantics

Future implementation must prefer governed partial/error behavior over crash-or-guess behavior.

Candidate semantics:

- Missing workbook path: error without reading any data.
- Missing worksheet or unreadable workbook: error without retaining file contents.
- Missing required headers: partial/error with header names only if names are non-sensitive, otherwise redacted.
- Missing `采集时间`: partial row because `event_time` is not reliable.
- Unknown `威胁等级`: partial row because severity mapping is unknown.
- Invalid IP-like values: partial row with redacted field reference, not raw value.
- Empty mapped row: skipped or counted as ignored only if later ticket specifies exact behavior.

This draft does not freeze adapter result classes, runtime error payloads, API responses, or SIEM adapter protocol behavior.

## 16. Test Plan for Later Implementation

Later tests may be added only in `backend/tests/test_siem_alert_file_adapter.py`.

Synthetic-only test cases should cover:

- workbook with exact 14 mapped headers
- skipped title row before headers
- empty rows ignored or counted according to later exact scope
- unknown severity returns partial behavior
- missing timestamp returns partial behavior
- invalid source/destination IP-like value returns partial behavior without raw value leakage
- `攻击失败` maps to `blocked`
- `疑似成功` maps to `suspected`
- unknown `状态` maps to `unknown`
- output dictionaries use only `event_id`, `event_time`, `severity`, `activity_name`, `source_ip`, `destination_ip`, `destination_asset_id`, and `extra`
- no fixture file is created
- tests construct synthetic workbook content in memory or temporary local test files only

The later ticket must name exact test commands before implementation begins.

## 17. Local Real-Data Validation Plan for Later Implementation

Local real-data validation is not authorized by this draft.

If a later accepted ticket authorizes validation planning, the plan must:

- use repo-external local paths only
- keep original files outside the repo
- avoid modifying original files
- avoid committing validation inputs or outputs
- avoid screenshots containing real values
- redact all output before any review or report leaves the local boundary
- avoid evidence retention unless a separate governed evidence-retention decision approves it
- record only aggregate, redacted validation results if reporting is separately authorized
- HOLD if validation needs credentials, live access, customer/operator sign-off, or real evidence retention

## 18. HOLD Conditions

This ticket definition or any later implementation must HOLD if:

- implementation starts from this draft
- code changes appear in this draft stage
- tests appear in this draft stage
- dependency changes appear
- `openpyxl` is unavailable and dependency approval has not been granted
- fixture files are created or modified
- real `.xlsx`, syslog, device logs, payloads, SQL, IPs, hostnames, usernames, account IDs, IOC values, screenshots, customer/operator evidence, credentials, tokens, API keys, auth headers, cookies, or secret material enters repo, prompts, commits, reports, review material, or release artifacts unredacted
- local real-data execution starts before a separate accepted implementation/validation ticket
- validation reports are generated or retained before explicit authorization
- evidence retention, deletion, expiry, replay, storage, or evidence-pack behavior is approved
- redaction policy is frozen
- runtime integration is needed
- `SIEMAdapterProtocol` changes are needed
- `backend/app/tools/siem_adapter.py` must change
- `backend/app/config.py` must change
- `backend/app/runtime_service.py` must change
- `backend/app/agents/graph.py` must change
- `backend/tests/fixtures/**` must change
- dependency files must change
- release scripts must change
- AI_COLLAB files/contracts must change
- S5-B/S5-D/S4-A contract docs must change
- S5-B or S5-D reopen is implied without explicit reopen decision
- S4-A resolver priority or authority changes
- public close-case endpoint work appears
- external pilot readiness or execution is implied
- human go/no-go is skipped
- external review is skipped or treated as implementation authorization

## 19. Acceptance Criteria for This Ticket Definition

This ticket definition is acceptable if:

- exactly one new docs-only file is created
- status is closed as governed ORDIV-L1A-01 docs-only ticket-definition baseline and explicitly non-authorizing
- baseline is `ORDIV-SCOPED-DECISION-2026-04-16-001 / commit 38d61ec`
- predecessor is `docs/OFFLINE_REAL_DATA_INTEGRATION_SCOPED_DECISION.md`
- `requires_external_review` is true
- role boundary preserves VS Code / human-supervised future implementation and Claude Code review-only posture
- future file scope is limited to `backend/app/tools/siem_alert_file_adapter.py` and `backend/tests/test_siem_alert_file_adapter.py`
- out-of-scope file HOLD list is explicit
- dependency rule allows `openpyxl` only if already available and no dependency file changes are needed
- target alert shape uses only existing SIEM-compatible alert dictionary keys
- all 14 source fields are mapped with target field, normalization, guardrail, and HOLD trigger
- no implementation, code, tests, dependencies, fixtures, runtime integration, local real-data execution, validation report, evidence retention, pilot readiness, S5-B/S5-D reopen, S4-A resolver change, public close-case endpoint work, or AI_COLLAB change is authorized
- HANDOFF and release manifest are modified only for governed closeout metadata; verify report, code, tests, fixtures, config, dependencies, and AI_COLLAB files are not manually modified
- staging and commit are performed only for governed closeout after full gate PASS; push still requires human confirmation

## 20. Preliminary Recommendation

`PRELIMINARY_RECOMMENDATION_READY_FOR_REVIEW_ONLY`

Meaning:

- This document may be reviewed by Claude Code in review-only mode.
- If accepted, it may become the governed ticket-definition baseline for a later ORDIV-L1A-01 implementation ticket.
- Any later implementation ticket must still be separately drafted, externally reviewed, human-approved, and closed before code or tests change.

Non-meaning:

- It does not authorize implementation.
- It does not authorize adapter code.
- It does not authorize tests.
- It does not authorize dependency changes.
- It does not authorize fixtures.
- It does not authorize runtime integration.
- It does not authorize local real-data validation.
- It does not authorize evidence retention.
- It does not authorize external pilot readiness.
- It does not authorize S5-B/S5-D/S4-A/AI_COLLAB boundary changes.
