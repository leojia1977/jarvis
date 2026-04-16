# ORDIV-L1A-01 SIEM Alert XLSX Adapter Implementation Ticket

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | ORDIV-L1A-01 SIEM Alert XLSX Adapter Implementation Ticket |
| Status | Closed as governed ORDIV-L1A-01 adapter implementation ticket baseline; docs-only; not implementation authorization |
| Scope | Docs-only implementation ticket draft for a later bounded ORDIV-L1A-01 SIEM alert `.xlsx` adapter implementation |
| Baseline snapshot | ORDIV-L1A-OPENPYXL-DEPENDENCY-DECISION-2026-04-16-001 |
| Baseline stage | ordiv-l1a-openpyxl-dependency-decision |
| Baseline commit | `be00f3fa0d22b3addbb2595d40b4db2847c4d961` |
| Predecessor artifacts | docs/ORDIV_L1A_OPENPYXL_DEPENDENCY_DECISION.md; docs/ORDIV_L1A_01_SIEM_ALERT_XLSX_MAPPING_TICKET.md |
| Route | ORDIV-L1A-01 SIEM alert `.xlsx` adapter implementation ticket draft |
| Codex role | planning and prompt orchestration only |
| Draft creator | VS Code / human-supervised workspace |
| Reviewer | Claude Code review-only |
| Claude Web posture | Not automatically required for this draft; triggered if this draft or later work modifies/freezes contracts, changes frozen contracts, adds tracked dependencies, changes dependency governance, freezes redaction/evidence policy, or expands real-data handling |
| requires_external_review | true for any later implementation attempt, inherited from ORDIV / ORDIV-L1A boundaries |

This governed ticket-definition baseline by itself does not authorize implementation. Any later implementation must be reviewed, accepted, closed out, and explicitly human-approved before code or tests change.

Review closeout note: Claude Code review-only returned `GO` with no `HIGH`, `MEDIUM`, `LOW`, or `INFO` findings. Claude Web escalation is not required for this docs-only draft closeout. `requires_external_review=true` remains required for any later implementation attempt, and no implementation is authorized by this closeout.

## 2. Goal

Define a later, bounded implementation ticket for ORDIV-L1A-01 SIEM alert `.xlsx` adapter work now that local-only `openpyxl` availability is confirmed.

This document specifies future implementation scope, non-scope, dependency boundaries, event ID behavior, mapping behavior, partial/error behavior, and synthetic-only test expectations.

This document does not create adapter code, tests, fixtures, dependency changes, runtime integration, or local real-data validation.

## 3. Baseline Summary

- Current governed baseline is `ORDIV-L1A-OPENPYXL-DEPENDENCY-DECISION-2026-04-16-001`.
- Current governed baseline commit is `be00f3fa0d22b3addbb2595d40b4db2847c4d961`.
- `docs/ORDIV_L1A_OPENPYXL_DEPENDENCY_DECISION.md` selected `APPROVE_LOCAL_ENV_OPENPYXL_ONLY`, with fallback `PARK_L1A_UNTIL_OPENPYXL_AVAILABLE`.
- Local-only preflight now confirms `openpyxl_available=True`.
- `openpyxl_origin=C:\Users\Administrator\AppData\Roaming\Python\Python314\site-packages\openpyxl\__init__.py`.
- No tracked dependency was added.
- No dependency file may change for ORDIV-L1A-01.
- `docs/ORDIV_L1A_01_SIEM_ALERT_XLSX_MAPPING_TICKET.md` remains the governed mapping ticket-definition baseline.
- ORDIV-L1A implementation remains unauthorized until this draft is reviewed, accepted, closed out, and explicitly human-approved.
- S5-B and S5-D remain `PASS_AND_PARK`.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- External pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- AI_COLLAB files and contracts remain unchanged.

## 4. Role Boundary

- Codex is planning and prompt orchestration only.
- VS Code / human-supervised workspace creates this docs-only draft.
- Claude Code reviews this draft in review-only mode after creation.
- Claude Web is not automatically required for this draft.
- Claude Web or a human-designated qualified external review path must be triggered if this draft or later work modifies/freezes contracts, changes frozen contracts, adds tracked dependencies, changes dependency governance, freezes redaction/evidence policy, or expands real-data handling.
- Human go/no-go remains required before any later implementation attempt.

## 5. Non-Authorization

This draft does not authorize:

- adapter implementation
- code changes
- test changes
- dependency installation
- dependency file changes
- lockfile/package metadata changes
- fixture creation or modification
- runtime integration
- `SIEMAdapterProtocol` changes
- config changes
- release script changes
- HANDOFF changes
- release manifest changes
- local real-data execution
- real-data validation reports
- evidence retention
- redaction policy freeze
- frozen contract changes
- S5-B reopen
- S5-D reopen
- S4-A resolver changes
- public close-case endpoint work
- AI_COLLAB changes
- external pilot readiness
- external pilot execution
- staging
- commit
- push

## 6. Future Implementation File Scope

If this draft is reviewed, accepted, closed out, and human-approved for implementation, the future implementation file scope must be exactly:

| File | Action | Scope |
| --- | --- | --- |
| `backend/app/tools/siem_alert_file_adapter.py` | NEW only | Implement a local offline `.xlsx` parser that maps governed ORDIV-L1A-01 SIEM alert rows to existing SIEM-compatible alert dictionaries. |
| `backend/tests/test_siem_alert_file_adapter.py` | NEW only | Add synthetic-only tests for workbook parsing, mapping, event ID generation, partial behavior, sanitized gap reasons, and no raw-value leakage. |

No other file may be created or modified by the later ORDIV-L1A-01 implementation ticket.

## 7. Explicitly Out Of Scope / HOLD Files

The later implementation must HOLD if it needs to modify:

- `backend/app/tools/siem_adapter.py`
- `backend/app/config.py`
- `backend/app/runtime_service.py`
- `backend/app/agents/graph.py`
- dependency files
- lockfiles
- release scripts
- fixtures under `backend/tests/fixtures/**`
- `docs/HANDOFF.md`
- `releases/release_manifest.json`
- AI_COLLAB files
- S5-B/S5-D/S4-A docs
- frozen contracts
- public close-case endpoint artifacts
- runtime integration files

## 8. Dependency Boundary

- Use `openpyxl` only because it is available in the local Python environment.
- Current local-only preflight result is `openpyxl_available=True`.
- Current local-only origin is `C:\Users\Administrator\AppData\Roaming\Python\Python314\site-packages\openpyxl\__init__.py`.
- Do not add `openpyxl` to dependency files.
- Do not install dependencies from implementation code or tests.
- Do not create dependency manifests.
- Do not modify lockfiles or package metadata.
- If future implementation requires tracked dependency changes, package metadata changes, dependency pins, or release-process changes, HOLD and open a separate governed tracked-dependency route with external review.

## 9. Data Boundary

The later implementation may parse only `.xlsx` files.

The later implementation and tests must not introduce:

- real `.xlsx` files
- real SIEM/EDR/source/telemetry data
- real IPs
- real hostnames
- real usernames
- real account IDs
- real IOC values
- SQL
- payload text
- screenshots
- customer/operator evidence
- credentials
- tokens
- API keys
- auth headers
- cookies
- secret material

No real data may enter repo files, fixtures, prompts, commits, reports, generated review material, or release artifacts.

## 10. Governed Source Fields

The later implementation must support only the governed 14 Chinese SIEM alert fields:

- `采集时间`
- `威胁名称`
- `威胁类型`
- `威胁等级`
- `受影响主机`
- `协议`
- `源Ip`
- `源端口`
- `目标Ip`
- `目标端口`
- `受影响主机ip`
- `状态`
- `数据来源`
- `CVE`

Missing required headers must produce governed partial behavior with sanitized `gap_reason`; the adapter must not guess from real content or infer alternate schema.

## 11. Mapping Boundary

The later implementation must preserve the governed mapping and guardrails from `docs/ORDIV_L1A_01_SIEM_ALERT_XLSX_MAPPING_TICKET.md`.

| Source field | Target field | Future implementation boundary |
| --- | --- | --- |
| `采集时间` | `event_time` | Parse exact confirmed timestamp shape only; invalid timestamps produce partial behavior. |
| `威胁名称` | `activity_name` and/or `extra.alert_name` | Use as alert label only after redaction-safe handling; do not create new schema fields. |
| `威胁类型` | `extra.threat_category` | Preserve as extra metadata only; do not freeze taxonomy. |
| `威胁等级` | `severity` | Map `高危`/`HIGH`, `中危`/`MEDIUM`, `低危`/`LOW`; unknown severity produces partial behavior. |
| `受影响主机` | `destination_asset_id` and/or `extra.affected_host_label` | Do not change S4-A host identity authority or resolver order. |
| `协议` | `extra.protocol` | Preserve protocol metadata only; do not freeze telemetry normalization. |
| `源Ip` | `source_ip` | Validate IP-like value syntactically; do not leak raw values in errors. |
| `源端口` | `extra.source_port` | Parse port-like value only if valid; do not create schema/API fields. |
| `目标Ip` | `destination_ip` | Validate IP-like value syntactically; do not leak raw values in errors. |
| `目标端口` | `extra.destination_port` | Parse port-like value only if valid; do not create schema/API fields. |
| `受影响主机ip` | `extra.affected_host_ip` | Keep as extra metadata only; do not change S4-A resolver behavior. |
| `状态` | `extra.outcome` | Map `攻击失败` to `blocked`, `疑似成功` to `suspected`, unknown values to `unknown`; do not change workflow semantics. |
| `数据来源` | `extra.detection_engine` | Preserve source metadata only; do not freeze source authority, provenance, or trust ordering. |
| `CVE` | `extra.cve_id` | Preserve nullable CVE-like value only in synthetic tests; do not authorize IOC/evidence retention. |

## 12. Target Alert Shape

The later implementation must satisfy existing SIEM-compatible alert dictionary expectations without modifying `SIEMAdapterProtocol`.

Allowed output keys are:

- `event_id`
- `event_time`
- `severity`
- `activity_name`
- `source_ip`
- `destination_ip`
- `destination_asset_id`
- `extra`

Use `extra` only for ORDIV-L1A local adapter values that do not create new schema/API/runtime contract fields.

If implementation appears to require `SIEMAdapterProtocol` changes, runtime integration, config changes, dependency file changes, fixtures, real-data retention, or schema/API changes, HOLD.

## 13. Event ID Decision

The later implementation must generate `event_id` locally from row position, not raw row content.

Preferred format:

```text
ordiv_l1a_row_<row_number>
```

Rules:

- `row_number` may be derived from the worksheet row index or normalized parsed row index, as defined by the later implementation.
- `event_id` must be local, non-persistent, and row-index-derived.
- `event_id` must not hash raw row values.
- `event_id` must not include filenames, workbook paths, sheet names, cell values, IPs, hosts, usernames, SQL, IOCs, credentials, payload text, or customer/operator evidence.
- `event_id` must not imply persisted identity, API identity, cross-run stability, or schema/contract freeze.
- Hashing raw row values into `event_id` is prohibited unless a later governed evidence-retention decision explicitly approves it.

## 14. Header and Workbook Handling

The later implementation may:

- parse `.xlsx` workbooks using locally available `openpyxl`
- detect the governed 14 headers by exact header names
- skip title rows only when exact headers are found later in the worksheet
- ignore empty rows if exact behavior is defined in the later implementation
- return partial/error behavior for missing headers, duplicate headers, invalid workbook shape, unreadable workbook, or unavailable workbook

The later implementation must not:

- parse `.xls`, `.csv`, JSON, syslog, device logs, or screenshots
- infer headers from raw real content
- log raw workbook paths or row values
- retain workbook contents
- commit workbook files
- rely on external services or live data access

## 15. Partial and Error Semantics

Missing required headers, invalid workbook shape, invalid timestamps, invalid IP-like values, or unavailable workbook must produce governed partial behavior with sanitized `gap_reason`.

Sanitized `gap_reason` may include:

- missing governed header category
- invalid timestamp category
- invalid IP-like category
- invalid workbook structure category
- workbook unavailable category
- row index if it does not reveal sensitive source data

Sanitized `gap_reason` must not include:

- raw filenames
- workbook paths
- sheet names
- cell values
- IPs
- hosts
- users
- SQL
- IOCs
- credentials
- payload text
- customer/operator evidence

The later implementation must not freeze runtime error payloads, API response contracts, or cross-cutting partial/error semantics.

## 16. Testing Scope

The later implementation may add tests only in `backend/tests/test_siem_alert_file_adapter.py`.

Testing must use only synthetic data.

Runtime-generated synthetic workbook content in a temporary location is allowed.

No committed workbook fixtures are allowed.

Tests should cover:

- happy path with all 14 governed headers
- title row skipped before exact headers
- missing required headers
- partial row behavior
- invalid timestamp values
- invalid IP-like values
- severity mapping for `高危`/`HIGH`, `中危`/`MEDIUM`, `低危`/`LOW`
- outcome mapping for `攻击失败`, `疑似成功`, and unknown values
- row-index-derived `event_id` such as `ordiv_l1a_row_<row_number>`
- sanitized `gap_reason`
- no raw value leakage in `gap_reason`
- output keys limited to SIEM-compatible alert dictionary expectations
- no committed workbook fixtures
- no dependency-file changes

Tests must not include real `.xlsx`, real IPs, real hostnames, real usernames, real IOCs, customer/operator evidence, secrets, tokens, API keys, auth headers, cookies, SQL, payloads, or screenshots.

## 17. Local Real-Data Validation Boundary

Local real-data validation is not authorized by this draft.

The later implementation ticket must not run or document real `.xlsx` validation unless a separate governed validation route explicitly authorizes:

- repo-external paths
- redaction requirements
- evidence-retention prohibition or approval boundary
- validation report handling
- review material handling
- human go/no-go

If local real-data validation is requested before such a route exists, HOLD.

## 18. HOLD Conditions

This draft or any later implementation must HOLD if:

- implementation starts before this ticket is reviewed, accepted, closed out, and human-approved
- any file outside the exact future file scope is needed
- `backend/app/tools/siem_adapter.py` must change
- `backend/app/config.py` must change
- `backend/app/runtime_service.py` must change
- `backend/app/agents/graph.py` must change
- dependency files or lockfiles must change
- release scripts must change
- fixtures under `backend/tests/fixtures/**` are created or modified
- HANDOFF or release manifest changes are needed during implementation
- AI_COLLAB files must change
- S5-B/S5-D/S4-A docs must change
- frozen contracts must change
- public close-case endpoint work appears
- runtime integration appears
- real SIEM/EDR/source/telemetry access appears
- committed real `.xlsx` files appear
- real-data validation reports appear
- evidence retention appears
- redaction policy freeze appears
- external pilot readiness or execution appears
- `SIEMAdapterProtocol` changes are needed
- schema/API changes are needed
- `event_id` requires hashing raw row values
- `gap_reason` would expose raw filenames, workbook paths, sheet names, cell values, IPs, hosts, users, SQL, IOCs, credentials, payload text, or customer/operator evidence
- Claude Web or another required external review path is triggered but not completed

## 19. Acceptance Criteria

This docs-only closeout is acceptable if:

- exactly one new docs-only file is created
- status is closed as a governed ORDIV-L1A-01 adapter implementation ticket baseline
- local-only `openpyxl_available=True` and `openpyxl_origin` are recorded
- no tracked dependency was added
- no dependency file may change
- future implementation file scope is exactly `backend/app/tools/siem_alert_file_adapter.py` and `backend/tests/test_siem_alert_file_adapter.py`, both NEW only
- out-of-scope/HOLD files and boundaries are explicit
- governed 14 Chinese SIEM source fields are listed
- governed mapping and guardrails are preserved
- event ID generation is defined as local, non-persistent, row-index-derived
- raw-row hashing for `event_id` is prohibited absent later evidence-retention approval
- sanitized `gap_reason` rules are explicit
- testing scope is synthetic-only and forbids committed workbook fixtures
- no code, tests, dependency files, lockfiles, fixtures, release scripts, AI_COLLAB files, S5-B/S5-D/S4-A docs, frozen contracts, or implementation files are changed by this closeout
- full gate is run and passes before commit
- only this ticket, `docs/HANDOFF.md`, and `releases/release_manifest.json` are staged, committed, and pushed for closeout

## 20. Preliminary Recommendation

`PRELIMINARY_RECOMMENDATION_READY_FOR_CLAUDE_CODE_REVIEW_ONLY`

Meaning:

- This docs-only implementation ticket draft may be reviewed by Claude Code in review-only mode.
- If accepted and closed out later, it may define the governed implementation boundary for a future ORDIV-L1A-01 SIEM alert `.xlsx` adapter implementation.
- Any later implementation attempt still requires closeout, explicit human approval, `requires_external_review=true`, and exact file/test scope adherence.

Non-meaning:

- Does not authorize adapter implementation now.
- Does not authorize code changes.
- Does not authorize test changes.
- Does not authorize dependency changes.
- Does not authorize fixtures.
- Does not authorize local real-data validation.
- Does not authorize runtime integration.
- Does not authorize `SIEMAdapterProtocol` changes.
- Does not authorize external pilot readiness or execution.
