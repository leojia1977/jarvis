# ORDIV-L1A Real Data Validation Scoped Decision

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | ORDIV-L1A Real Data Validation Scoped Decision |
| Status | Closed as governed ORDIV-L1A real-data validation scoped decision baseline |
| Scope | Docs-only scoped decision for whether and how a later ORDIV-L1A local real-data validation route may be opened |
| Baseline snapshot | ORDIV-L1A01-ADAPTER-IMPL-2026-04-16-001 |
| Baseline stage | ordiv-l1a01-adapter-implementation |
| Baseline commit | `2665857702a7c9191a68e041102e6f66c84c80b5` |
| Predecessor baseline | ORDIV-L1A SIEM alert XLSX adapter implementation baseline |
| Route | OPEN_L1A_REAL_DATA_VALIDATION_SCOPED_DECISION |
| Codex role | planning and prompt orchestration only |
| Draft creator | VS Code / human-supervised workspace |
| Reviewer | Claude Code review-only |
| Claude Web posture | Required before any later real-data validation attempt |
| Human go/no-go | Required before any later local validation attempt |

This is a docs-only scoped decision baseline. It does not authorize real-data validation now.

This draft does not authorize opening, reading, parsing, copying, uploading, listing, or summarizing any real workbook now. It does not authorize validation report creation now, evidence retention, redaction policy freeze, external pilot readiness, or any alteration to the implemented adapter baseline.

Review closeout note: Claude Code review-only returned `GO` with no `HIGH`, `MEDIUM`, or `LOW` findings. INFO items were addressed or confirmed non-blocking, including inherited-state re-affirmation, logs/commits path scope alignment, and the candidate metric caveat. Claude Web is not required before this docs-only closeout, but remains required before any later real-data validation attempt.

## 2. Goal

Define whether and how a later local real-data validation route may be opened for the already implemented ORDIV-L1A SIEM alert XLSX adapter.

This document compares bounded candidate routes and records the safest next route posture. It is intentionally non-authorizing: any later local real-data validation attempt requires Claude Web external review first and explicit human go/no-go after that review.

## 3. Baseline Summary

- ORDIV-L1A adapter implementation baseline is governed at commit `2665857702a7c9191a68e041102e6f66c84c80b5`.
- Current snapshot is `ORDIV-L1A01-ADAPTER-IMPL-2026-04-16-001`.
- Current stage is `ordiv-l1a01-adapter-implementation`.
- Implemented adapter file: `backend/app/tools/siem_alert_file_adapter.py`.
- Implemented synthetic test file: `backend/tests/test_siem_alert_file_adapter.py`.
- Current implementation is synthetic-only.
- Closeout targeted tests passed: `py -3 -m unittest -q backend.tests.test_siem_alert_file_adapter`.
- Closeout SIEM contract tests passed: `py -3 -m unittest -q backend.tests.test_siem_adapter_contract`.
- Closeout full gate passed: `py -3 scripts\git_preflight.py --mode all`.
- Local-only `openpyxl` was used.
- No tracked dependency was added.
- Current baseline does not authorize real-data validation, evidence retention, redaction policy freeze, external pilot readiness/execution, `SIEMAdapterProtocol` changes, runtime/config integration, S5-B/S5-D reopen, S4-A resolver changes, public close-case endpoint work, or AI_COLLAB changes.
- S5-B and S5-D remain `PASS_AND_PARK`.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- External pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- AI_COLLAB files and contracts remain unchanged.

## 4. Role Boundary

- Codex is planning and prompt orchestration only.
- VS Code / human-supervised workspace creates this docs-only scoped decision draft.
- Claude Code reviews this draft in review-only mode after creation.
- Claude Web is required before any later real-data validation attempt because this route touches real security data handling, redaction/evidence boundaries, validation report handling, and pilot-readiness adjacency.
- Human go/no-go remains required before any later local validation attempt.

## 5. Candidate Routes

| Route | Meaning | Main risk | Recommendation |
| --- | --- | --- | --- |
| `PARK_REAL_DATA_VALIDATION` | Keep L1A synthetic implementation baseline only; do not validate a real workbook yet. | Low risk, but product learning pauses. | Safe fallback. |
| `OPEN_LOCAL_REDACTED_VALIDATION_RUN` | Later human-supervised local-only validation may run against a repo-external real `.xlsx` path, with no raw workbook content entering repo, prompts, commits, review material, logs, or reports. | Real security data handling and redaction/reporting mistakes. | Preferred only after Claude Web external review and explicit human go/no-go. |
| `OPEN_VALIDATION_REPORT_TEMPLATE_ONLY` | Create a later docs-only report template using only redacted/count-based fields before any real run. | May create premature reporting expectations. | Acceptable intermediate route. |
| `OPEN_TRACKED_REDACTED_SUMMARY_REPORT_ROUTE` | After a later local run, commit a redacted count-only summary report to repo. | Report may accidentally leak sensitive values or imply pilot readiness. | HOLD until separate external review defines exact allowed fields and examples. |
| `START_REAL_DATA_VALIDATION_NOW` | Run adapter on real `.xlsx` immediately. | Violates current boundaries. | NOT_RECOMMENDED / HOLD. |

## 6. Route Comparison

| Route | Preconditions | External review implication | HOLD triggers |
| --- | --- | --- | --- |
| `PARK_REAL_DATA_VALIDATION` | None beyond preserving current implementation baseline. | No immediate Claude Web route needed if no real data is touched. | Any attempt to run, open, inspect, list, summarize, or copy real workbook data. |
| `OPEN_LOCAL_REDACTED_VALIDATION_RUN` | Claude Web review completed; explicit human go/no-go; repo-external workbook path; redacted/count-only output; no raw data leaves local boundary. | Claude Web required before any later validation attempt. | Missing Claude Web review, missing human go/no-go, workbook path inside repo, raw values in output, evidence retention request. |
| `OPEN_VALIDATION_REPORT_TEMPLATE_ONLY` | Separate docs-only ticket and review; no real workbook access. | Claude Web may be required if allowed fields/examples could freeze redaction/evidence/report policy. | Template includes raw-value examples, report fields imply pilot readiness, or template becomes validation authorization. |
| `OPEN_TRACKED_REDACTED_SUMMARY_REPORT_ROUTE` | Separate external review defining exact fields/examples; completed local validation under prior authorization. | Claude Web required before any tracked report route. | Unapproved fields, raw values, path/file leaks, evidence retention, or pilot-readiness claims. |
| `START_REAL_DATA_VALIDATION_NOW` | None; this route conflicts with the current boundary. | Not applicable because route is HOLD. | Any immediate real-data run, workbook inspection, report creation, or AI upload. |

## 7. Recommended Route

Preferred next candidate route:

`OPEN_LOCAL_REDACTED_VALIDATION_RUN`

This is recommended only if all of the following are completed first:

- Claude Web external review gate is completed before the validation attempt.
- Explicit human go/no-go is given after external review.
- Workbook path remains repo-external.
- No raw workbook content enters repo, prompts, commits, review material, logs, or reports.
- Output is redacted/count-based only.
- Evidence retention remains prohibited unless separately approved.

Fallback:

`PARK_REAL_DATA_VALIDATION`

Use this fallback if Claude Web review is not complete, human go/no-go is absent, the workbook cannot remain repo-external, report fields are not pre-approved, or any sensitive value could leave the local boundary.

## 8. Potential Later Validation Boundaries

These boundaries describe what a later route may need to define. They do not authorize validation now.

- Real workbook path must be repo-external.
- No raw workbook content may be committed.
- No workbook screenshots may be created for repo, prompt, report, or review use.
- No workbook copy may be placed into fixtures.
- No workbook or raw workbook content may be uploaded to AI tools.
- No raw IPs, hostnames, usernames, account IDs, IOC values, CVE values tied to customer context, SQL, payload text, credentials, tokens, auth headers, cookies, or secrets may appear in prompts, reports, commits, logs, or review material.
- No raw filenames or raw full local paths may appear in repo, review material, prompts, reports, logs, or commits.
- Only count-based or category-based metrics may leave the local boundary.
- Any sample rows must be synthetic or fully redacted.
- Validation report, if later authorized, must be a separate governed artifact.
- Evidence retention is prohibited unless separately approved.
- Validation success threshold must not imply pilot readiness.

## 9. Possible Later Count-Based Metrics

The following metric names are candidate discussion items only, not pre-approved report fields. A later external review may delete, rename, narrow, or reject any metric. Listing these names does not authorize collecting, reporting, committing, or using them now.

- `workbook_rows_seen`
- `rows_parsed_ok`
- `rows_partial`
- `rows_unavailable`
- `missing_required_header_count`
- `invalid_timestamp_count`
- `invalid_ip_like_count`
- `invalid_port_count`
- `partial_row_count`
- `severity_distribution`
- `outcome_distribution`
- `extra_field_presence_counts`
- `parser_status`
- `gap_reason_category_counts`
- `validation_runtime_ms`

## 10. Non-Authorization

This draft does not authorize:

- opening real `.xlsx`
- running adapter on real data
- copying real workbook
- committing real workbook
- committed fixtures
- screenshots
- raw row samples
- raw filenames or raw full paths in repo, review material, prompts, reports, logs, or commits
- validation report creation
- evidence retention
- redaction policy freeze
- dependency changes
- code changes
- test changes
- runtime/config integration
- `SIEMAdapterProtocol` changes
- S5-B reopen
- S5-D reopen
- S4-A resolver changes
- public close-case endpoint work
- AI_COLLAB changes
- external pilot readiness
- external pilot execution
- real customer/operator sign-off
- staging
- commit
- push

## 11. HOLD Conditions

Hold the route if any of the following occur:

- Claude Web external review is not completed before a validation attempt.
- Human go/no-go is absent.
- Real workbook path is inside the repo.
- Raw workbook content would enter repo, prompt, report, logs, commits, or review material.
- Raw sensitive values would appear in output.
- Evidence retention is requested without separate approval.
- Report fields are not pre-approved.
- Validation threshold is used to imply pilot readiness.
- Code changes are requested.
- Test changes are requested.
- Dependency changes are requested.
- Runtime integration is requested.
- External pilot claim appears.
- Any S5-B boundary change appears.
- Any S5-D boundary change appears.
- Any S4-A boundary change appears.
- Any AI_COLLAB boundary change appears.

## 12. Acceptance Criteria

This docs-only scoped decision draft is acceptable if:

- exactly one new docs-only file is created
- no code files are changed
- no test files are changed
- no dependency files are changed
- `docs/HANDOFF.md` is not changed
- `releases/release_manifest.json` is not changed
- candidate routes are compared
- recommended route is bounded and non-authorizing
- Claude Web is required before any later validation attempt
- human go/no-go is required before any later validation attempt
- real-data, redaction, evidence, report, and pilot boundaries are explicit
- no real workbook is accessed, opened, read, parsed, copied, inspected, summarized, listed, uploaded, or retained
- no validation report is created
- no staging, commit, push, or full gate is performed

## 13. Preliminary Recommendation

`PRELIMINARY_RECOMMENDATION_OPEN_LOCAL_REDACTED_VALIDATION_RUN_AFTER_EXTERNAL_REVIEW_OR_PARK`

Meaning:

- The preferred later route is `OPEN_LOCAL_REDACTED_VALIDATION_RUN` only after Claude Web external review and explicit human go/no-go.
- The fallback is `PARK_REAL_DATA_VALIDATION`.
- A later local validation route must be human-supervised, repo-external for workbook path, and redacted/count-based only.
- Any later report route must be separately governed.

Non-meaning:

- Does not authorize real-data validation now.
- Does not authorize opening, reading, parsing, copying, listing, or summarizing any real workbook now.
- Does not authorize validation report creation now.
- Does not authorize evidence retention.
- Does not authorize redaction policy freeze.
- Does not imply external pilot readiness.
- Does not alter the implemented adapter baseline.
