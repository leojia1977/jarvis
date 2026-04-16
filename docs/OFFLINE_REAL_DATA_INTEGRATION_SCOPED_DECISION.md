# Offline Real Data Integration Scoped Decision

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Offline Real Data Integration Scoped Decision |
| Status | Closed as governed docs-only ORDIV scoped decision baseline; not implementation authorization |
| Scope | ORDIV route and scope decision only |
| Baseline snapshot | `S5C-IMPL5-TICKET-DEF-2026-04-16-001` |
| Baseline stage | `s5c-impl5-ticket-definition` |
| Baseline commit | `99ba632bac2be9413a2b9674d1dacf8e9d984c30` |
| Source of truth | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Prior artifact | `docs/S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_TICKET.md` |
| Proposed route | `ORDIV` |
| Recommended next candidate | `NARROW_L1A_FIRST` |
| `primary_implementor` | Codex local, human-authorized in this thread |
| `reviewer` | Claude Code review-only |
| `reviewer_when_cc_implements` | not applicable |
| `requires_external_review` | true |

`requires_external_review` is true because ORDIV introduces offline real security data validation boundaries, output-side redaction requirements, evidence-retention questions, and future adapter behavior that is adjacent to S5-B source authority and S5-D telemetry normalization. External review does not authorize implementation and does not replace human go/no-go.

## 2. Goal

This document drafts a governed docs-only scoped decision for Offline Real Data Integration Validation, abbreviated as `ORDIV`.

The goal is to decide whether ORDIV should be treated as a new route, compare candidate routes, define data and governance boundaries, and recommend the safest first later implementation candidate.

This document must not authorize implementation.

This document answers:

- whether the current baseline is clear enough to open ORDIV as a new route
- whether ORDIV is separate from S5-C-IMPL-5
- which candidate ORDIV routes exist
- which route is recommended first
- which risks and HOLD conditions apply
- why `requires_external_review=true`
- what a later ORDIV-L1A-01 ticket must include before any implementation can begin

## 3. Baseline Summary

- Active baseline snapshot is `S5C-IMPL5-TICKET-DEF-2026-04-16-001`.
- Active baseline stage is `s5c-impl5-ticket-definition`.
- Baseline commit is `99ba632bac2be9413a2b9674d1dacf8e9d984c30`.
- Branch is `codex/s3-a-runtime`.
- `docs/S5C_IMPL5_CASE_LIFECYCLE_ACTION_REQUEST_IMPLEMENTATION_TICKET.md` is the governed S5-C-IMPL-5 implementation-ticket definition baseline.
- S5-C-IMPL-5 defines future case lifecycle and action-request implementation-ticket boundaries only.
- S5-C-IMPL-5 does not authorize real SIEM data ingestion, new file adapters, real external data replay, evidence retention, redaction policy freeze, pilot readiness improvement, or S5-B/S5-D reopen.
- S5-B Source/Input Discovery remains `PASS_AND_PARK`.
- S5-D Telemetry Discovery remains `PASS_AND_PARK`.
- S5-A external pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- Real customer/operator sign-off remains unauthorized.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- AI_COLLAB operating model and contract are not changed by this decision.

## 4. ORDIV Route Position

ORDIV should be treated as a proposed new route, not as a continuation of S5-C-IMPL-5.

ORDIV exists to validate how SecuPilot may process offline real security data while keeping raw data outside the repo and preserving governed product boundaries.

ORDIV does not silently reopen S5-B or S5-D.

If ORDIV work later reveals that source/input authority, host identity authority, telemetry normalization, freshness/provenance, redaction, secret handling, evidence retention, frozen contracts, or pilot readiness semantics need to change, the work must HOLD until a separate governed decision explicitly opens that boundary.

## 5. Data Boundary

Raw real data must remain outside the repository.

The following must not be committed, copied into fixtures, pasted into review material, uploaded to AI, or included unredacted in reports:

- original `.xlsx` alert exports
- syslog files
- device logs
- raw event bodies
- payloads
- SQL statements
- true IP addresses
- hostnames
- usernames
- account identifiers
- IOC values
- screenshots containing real alert content
- customer/operator evidence
- credentials, tokens, API keys, auth headers, cookies, or secret material

The following may be considered for repo entry only after a later governed ticket, for example `ORDIV-L1A-01`, is separately drafted, reviewed, and accepted according to Sections 9 and 14, and only if the content is sanitized:

- adapter source code with no embedded real data
- unit tests using synthetic/mock data only
- local harness code that reads externally supplied paths without committing those files
- validation report templates with no real values
- output-side redacted summary reports if a later ticket explicitly authorizes report generation

## 6. Redaction And Evidence Boundary

ORDIV uses output-side redaction as the proposed boundary.

Engines may need to process real values locally for validation, but any material leaving the local execution boundary must be redacted first. This includes:

- case views
- API responses used as review material
- validation reports
- screenshots
- copied excerpts
- AI review packets
- any future closeout evidence

Evidence retention is not approved by this decision.

Original real data remains in its original external location and must not be modified by ORDIV work. Any validation-generated case data, reports, or intermediate outputs require a later ticket to define retention, deletion, redaction, and review handling before they can be retained or shared.

## 7. Decision Vocabulary

Allowed decision outcomes:

- `RECOMMEND_SCOPED_DECISION`
- `RECOMMEND_NARROW_L1A_FIRST`
- `PARK_ORDIV`
- `HOLD_EXTERNAL_INPUT`
- `HOLD_REOPEN_DECISION_REQUIRED`
- `HOLD_POLICY_OR_EXTERNAL_REVIEW`
- `HOLD_OUT_OF_SCOPE`
- `NOT_RECOMMENDED_NOW`

Forbidden decision outcomes:

- `READY`
- `APPROVED`
- `IMPLEMENTABLE`
- `PILOT_READY`
- `PRODUCTION_READY`
- `AUTHORIZED_FOR_IMPLEMENTATION`
- `IMPLEMENT_NOW`
- `CODE_NOW`

This document must not use forbidden outcomes as decision values.

`RECOMMEND_NARROW_L1A_FIRST` means only that a later separate ORDIV-L1A-01 governed ticket may be drafted. It is not immediate implementation permission.

## 8. Candidate Routes

| Route | Meaning | Current status | Main risk | External-review posture | Recommendation |
| --- | --- | --- | --- | --- | --- |
| `PARK_ORDIV` | Do not enter ORDIV now; continue prior Sprint 5 routes only. | Available. | Real-data integration risk remains undiscovered. | Usually false if no new artifact or boundary change occurs. | Safe fallback only. |
| `DOCS_ONLY_ORDIV_SCOPED_DECISION` | Create a docs-only scoped decision defining ORDIV route, data boundary, risk, and next candidate. | Available and recommended. | Draft wording could be misread as implementation authorization. | true because route touches real data, redaction, evidence, and S5-B/S5-D adjacent boundaries. | `RECOMMEND_SCOPED_DECISION`. |
| `NARROW_L1A_FIRST` | Later first implementation candidate limited to SIEM alert `.xlsx` ingestion and 14-field mapping validation. | Candidate only after scoped decision closeout and human go/no-go. | Mapping ambiguity, dependency risk, sensitive output risk, and possible frozen contract pressure. | true for any later ticket because real alert data and redaction/evidence boundaries are implicated. | `RECOMMEND_NARROW_L1A_FIRST`. |
| `BROAD_MULTI_LAYER_ORDIV` | Attempt L1 syslog, L2 SIEM `.xlsx`, L3 device statistics, engine replay, and redaction validation together. | Not suitable as first route. | Too much blast radius; can silently reopen S5-B/S5-D or policy boundaries. | true. | `NOT_RECOMMENDED_NOW`. |
| `REOPEN_S5_B_OR_S5_D_FIRST` | Reopen source/input or telemetry discovery before ORDIV. | Not currently justified by governed evidence. | Premature reopen can freeze authority or normalization semantics without a specific gap. | true if source authority, telemetry normalization, stream closeout, or real evidence/access appears. | `HOLD_REOPEN_DECISION_REQUIRED` unless a concrete gap is found. |
| `EXTERNAL_PILOT_DECISION_PACKAGE` | Treat ORDIV as pilot readiness or external pilot decision input now. | Preconditions not met. | False pilot readiness and external execution implication. | true. | `NOT_RECOMMENDED_NOW`. |

## 9. Recommended Route

Preliminary recommendation: `RECOMMEND_SCOPED_DECISION` with later first candidate `RECOMMEND_NARROW_L1A_FIRST`.

Meaning:

- ORDIV may proceed first as a docs-only scoped decision.
- The scoped decision should establish route, boundaries, risks, and HOLD criteria.
- The first later implementation candidate should be `ORDIV-L1A-01`, narrowly focused on SIEM alert `.xlsx` ingestion and 14-field mapping validation.
- `ORDIV-L1A-01` must be drafted, reviewed, and accepted as a separate governed ticket before any code, test, dependency, fixture, or local real-data validation work begins.

Non-meaning:

- does not authorize implementation now
- does not authorize adapter source files
- does not authorize tests
- does not authorize dependency changes
- does not authorize fixture creation
- does not authorize real data entering the repo
- does not authorize raw data retention
- does not authorize redaction policy freeze
- does not authorize S5-B or S5-D reopen
- does not improve or imply external pilot readiness

## 10. Later ORDIV-L1A-01 Candidate Boundary

If a later ORDIV-L1A-01 ticket is opened, its preferred scope should be narrow:

- read SIEM alert `.xlsx` exports from a repo-external path
- skip header/title rows deterministically
- map the 14 known SIEM alert fields to SecuPilot alert records or a compatible canonical alert shape
- normalize severity, protocol, outcome, timestamp, IP, and port fields only as explicitly scoped
- return `AdapterResult.partial` or equivalent governed partial behavior for missing/null rows instead of crashing
- use synthetic/mock test data only inside repo
- produce only output-side redacted validation summaries if report generation is separately authorized

The later ticket must not include:

- online Metron, Kafka, Solr, Elastic, SIEM, EDR, source, or telemetry connections
- credentials, auth headers, cookies, tokens, API keys, or secret material
- real xlsx/syslog/device log files in repo
- real IP/host/user/SQL/IOC values in tests, fixtures, reports, commits, review packets, or prompts
- public close-case endpoint work
- S5-B/S5-D reopen
- S4-A resolver priority changes
- frozen contract changes unless explicitly scoped with external review
- AI_COLLAB changes
- pilot readiness or external pilot execution claims

## 11. Field Mapping Candidate

This mapping is a candidate for a later ORDIV-L1A-01 ticket only. It is not implementation authorization.

| SIEM field | Candidate target field | Candidate normalization | Must not imply | HOLD trigger |
| --- | --- | --- | --- | --- |
| `采集时间` | `timestamp` / `event_time` | parse local export timestamp to ISO 8601 only if exact format is confirmed | timestamp/freshness contract freeze | export time format ambiguity changes runtime semantics |
| `威胁名称` | `alert_name` / `activity_name` | preserve value after redaction boundary rules are applied to output | new schema field authorization or unredacted report output | raw alert name appears in repo or review material |
| `威胁类型` | `threat_category` | preserve value after redaction boundary rules are applied to output | new schema field authorization or taxonomy freeze | threat taxonomy changes or raw values leave the local boundary |
| `威胁等级` | `severity` | map high/medium/low labels to governed numeric or text severity only if ticket fixes target shape | severity contract change | existing engine severity semantics must change |
| `受影响主机` | `affected_host_label` | preserve locally; redact before output | host identity authority change | host identity mapping or S4-A resolver behavior must change |
| `协议` | `protocol` | normalize common protocol labels; unknown values remain unknown | telemetry normalization freeze | unknown protocol labels require new normalization semantics |
| `源Ip` | `source_ip` | validate as IP locally; redact before output | unredacted IP retention or source authority change | real IP enters repo, report, fixture, prompt, or review packet |
| `源端口` | `source_port` | integer when parseable | parser/schema implementation authorization | malformed ports require contract or schema changes |
| `目标Ip` | `dest_ip` / `destination_ip` | validate as IP locally; redact before output | unredacted IP retention or destination authority change | real IP enters repo, report, fixture, prompt, or review packet |
| `目标端口` | `dest_port` / `destination_port` | integer when parseable | parser/schema implementation authorization | malformed ports require contract or schema changes |
| `受影响主机ip` | `affected_host_ip` | validate as IP locally; redact before output | host identity authority change or unredacted IP retention | S4-A resolver behavior must change or real IP leaves local boundary |
| `状态` | `outcome` | map only documented labels; unknown labels remain unknown | lifecycle/action semantics change | outcome labels require case lifecycle or action-request semantic changes |
| `数据来源` | `detection_engine` | preserve value after redaction boundary rules are applied to output | source authority or provenance freeze | detection source affects trust precedence or source authority |
| `CVE` | `cve_id` | nullable | IOC/evidence retention authorization | real IOC/evidence appears in repo or review material |

Candidate target field names in this table do not authorize new schema fields, new persisted fields, new adapter-contract fields, or changes to existing frozen contracts. Any later ticket must decide whether the target is an existing `SIEMAdapterProtocol` method output, a file-specific adapter result, or a separate canonical alert event shape. This scoped decision does not modify the frozen adapter protocol.

## 12. External Review Implications

ORDIV and any ORDIV-L1A-01 ticket require `requires_external_review=true` because they touch:

- real external security data handling
- output-side redaction boundaries
- evidence retention and deletion questions
- possible new file adapter behavior
- possible dependency approval
- S5-B source/input authority adjacency
- S5-D telemetry normalization adjacency
- pilot readiness adjacency, even though readiness is not improved by ORDIV

External review may be performed by Claude Web when available, by Claude Code in review-only mode if the human operator explicitly designates it for this scoped decision, or by another human-designated qualified reviewer according to the active AI_COLLAB operating model and human go/no-go decision. External review is evidence for governance; it is not code truth and does not replace the source-of-truth repo or human decision authority.

## 13. HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This scoped decision is treated as implementation authorization. | ORDIV must not start implementation from a scoped decision alone. |
| Any code, test, runtime, API, schema, dependency, fixture, release-tooling, or manifest change appears in this draft stage. | This task is docs-only route scoping. |
| Any real `.xlsx`, syslog, device log, payload, screenshot, SQL, IP, host, username, IOC, or customer/operator evidence enters repo or review material unredacted. | Raw real data is outside the repo boundary. |
| Credentials, tokens, API keys, auth headers, cookies, or secret material appear. | Secret material is prohibited. |
| Output-side redaction is skipped or treated as optional for reports, review packets, or copied material. | Redaction is required before data leaves the local validation boundary. |
| Evidence retention, deletion, expiry, replay, storage, or evidence-pack behavior is approved. | Evidence retention needs a separate governed decision. |
| A new runtime/build dependency is required. | Dependency approval and external review are required before proceeding. |
| Existing frozen contracts or `SIEMAdapterProtocol` must change. | Contract changes require a separate scoped decision and external review. |
| S5-B source/input authority must change. | S5-B is `PASS_AND_PARK`; reopen requires explicit decision. |
| S5-D telemetry normalization, provenance, freshness, or redaction/retention boundary must change. | S5-D is `PASS_AND_PARK`; reopen requires explicit decision. |
| S4-A resolver priority changes. | Resolver order remains fixed. |
| Public close-case endpoint work appears. | `KEEP_DEFERRED` remains in force. |
| ORDIV is treated as external pilot readiness or execution evidence. | External pilot inputs remain `NOT_READY` / `UNKNOWN`. |
| AI_COLLAB operating model or contract changes appear. | This route does not modify collaboration governance. |
| External review is skipped or treated as replacing human go/no-go. | External review is required, and human go/no-go remains required. |
| Protected untracked files are touched. | Protected untracked files must remain untouched. |

## 14. Future Ticket Requirements

Before any ORDIV implementation can begin, a later governed ticket must define:

- exact title and route, preferably `ORDIV-L1A-01`
- exact baseline snapshot and commit
- exact `primary_implementor`
- exact `reviewer`
- `reviewer_when_cc_implements` if relevant
- `requires_external_review=true` with rationale
- exact files in scope
- exact files out of scope
- exact data boundary
- exact redaction boundary
- exact evidence-retention non-authorization
- exact dependency decision, including HOLD if dependency files must change
- exact target canonical shape or adapter contract relationship
- exact field mapping rules
- exact partial/null/error behavior
- exact synthetic test plan
- exact local real-data validation plan with repo-external paths only
- exact validation report redaction requirements if reports are in scope
- exact HOLD and rollback criteria
- human go/no-go before implementation

If the later ticket cannot make these details exact, it must HOLD rather than infer implementation scope.

## 15. Non-Authorization

This scoped decision does not authorize:

- implementation
- adapter code
- test changes
- runtime/API/schema changes
- dependency changes
- fixture creation or modification
- release tooling changes
- manifest or HANDOFF updates during draft stage
- local real-data execution
- online SIEM, EDR, source, telemetry, Metron, Kafka, Solr, or Elastic access
- credentials, tokens, API keys, auth headers, cookies, or secret material
- real `.xlsx`, syslog, device log, payload, screenshot, SQL, IP, host, username, IOC, customer/operator evidence in repo
- evidence retention
- redaction policy freeze
- public close-case endpoint work
- destructive response automation
- RBAC, ticketing, or workflow engine integration
- S5-B reopen
- S5-D reopen
- S4-A resolver priority or authority changes
- AI_COLLAB changes
- external pilot execution
- external pilot readiness
- real customer/operator sign-off
- external review bypass
- human go/no-go replacement
- automatic implementation ticket

## 16. Acceptance Criteria

This draft is acceptable if:

- exactly one new docs-only scoped decision file is created
- baseline snapshot, commit, branch, and source-of-truth repo are accurate
- ORDIV is clearly positioned as a new route, not an S5-C-IMPL-5 continuation
- `requires_external_review` is true with rationale
- candidate routes are compared
- recommended route is `RECOMMEND_SCOPED_DECISION` with later first candidate `RECOMMEND_NARROW_L1A_FIRST`
- recommendation is explicitly non-authorizing
- data boundary keeps raw real data outside repo and review material
- output-side redaction boundary is documented
- evidence retention is not approved
- ORDIV-L1A-01 is described only as a later governed ticket candidate
- S5-B and S5-D remain `PASS_AND_PARK` unless later explicit reopen decision
- external pilot inputs remain `NOT_READY` / `UNKNOWN`
- external pilot execution and readiness remain unauthorized
- public close-case endpoint remains `KEEP_DEFERRED`
- S4-A resolver order remains unchanged
- AI_COLLAB files are not modified
- HANDOFF, manifest, verify report, review pack, and release artifacts are not modified in this draft stage
- no staging, commit, or push is performed in this draft stage
