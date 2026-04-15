# S5-B-1 Source Input Gap Matrix

## Document Control
- Title: S5-B-1 Source Input Gap Matrix
- Baseline: `S5-B-DISCOVERY-2026-04-15-001`
- Source of truth: `D:\产品设计\New folder`
- Status: Draft for review
- Scope: docs-only source/input gap matrix
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code / human-supervised repo writer
- `reviewer`: Claude Code review-only
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false for draft; re-evaluate at closeout or if source contract freeze, source semantics, identity authority, or stream closeout scope appears

## Goal
Turn S5-B source/input uncertainty into governed gap categories for later product and governance decisions.

This matrix does not authorize implementation, source adapter changes, runtime/API/schema/test/dependency changes, real source-system access, live refresh or sync, external authentication, CMDB sync, multi-tenant ownership, external pilot execution, real customer/operator sign-off, or S4-A identity authority changes.

## Status Vocabulary

| Status | Meaning | Non-meaning |
| --- | --- | --- |
| `UNKNOWN` | Governed evidence is absent or insufficient. | Does not mean the input is missing forever or safe to infer from chat. |
| `NEEDS_DECISION` | Evidence exists enough to frame a product or governance decision, but no decision is made here. | Does not approve the decision or authorize implementation. |
| `DEFERRED` | Intentionally postponed until later input, ticket, or stream. | Does not silently remove the need if later scope depends on it. |
| `NOT_APPLICABLE` | Not relevant to S5-B source/input discovery at this stage. | Does not authorize another stream to proceed without its own governed basis. |

No status in this document means `READY`, `APPROVED`, `IMPLEMENTABLE`, or `PILOT_READY`.

## Non-Goals
- production source integration
- freezing source adapter contract
- changing source identity authority
- runtime/API/schema/test/dependency changes
- real source-system, SIEM, or EDR access
- credentials, auth headers, tokens, or API keys
- raw customer/operator/source payloads
- live refresh or sync jobs
- CMDB sync
- multi-tenant ownership or RBAC
- external pilot execution or real sign-off
- modifying S5-C semantics
- modifying `docs/AI_COLLAB_OPERATING_MODEL.md`

## Current Governed Baseline
- Active baseline is `S5-B-DISCOVERY-2026-04-15-001`.
- `docs/S5B_BOUNDED_SOURCE_INPUT_DISCOVERY.md` recommended `PROCEED_TO_S5_B_1_SOURCE_INPUT_GAP_MATRIX`.
- S4-A identity authority remains inherited and must not be bypassed.
- `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md` keeps the S5-A external pilot package `NOT_READY` because all seven external pilot input categories remain `UNKNOWN`.
- S5-C remains parked, and `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` keeps the public close-case endpoint at `KEEP_DEFERRED`.
- This document is a gap matrix only, not a source contract freeze.

## Gap Matrix

| Gap area | Current governed evidence | Status | Why it matters | Safe next evidence | Not authorized | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- |
| Source system inventory | Sprint 5 PRD/backlog identify S5-B source-mode discovery, but no governed external source systems are named. | `UNKNOWN` | Future source contracts need known source classes before scope can be narrowed. | Source/input request list naming candidate asset, baseline, intel, topology, or context sources without credentials or payloads. | Real source access, source approval, production integration. | A named source is treated as approved or connected without product/governance evidence. |
| Asset identifier mapping | S4-A freezes `AssetInventorySnapshot` and `HostIdentityRecord` fields. | `NEEDS_DECISION` | External asset identifiers must map to the canonical identity seed without bypassing it. | Non-authorizing mapping question list for `asset_id`, `hostname`, `fqdn`, `ip_addresses[]`, `aliases[]`, and `source_refs[]`. | Resolver priority changes, identity federation, authority replacement. | Mapping changes identity authority, trust precedence, or ambiguity behavior. |
| Hostname / FQDN / IP / alias mapping | S4-A resolver priority is `asset_id -> hostname -> fqdn -> ip_address -> aliases`. | `NEEDS_DECISION` | Host lookup semantics affect SIEM, EDR, T3 host selection, and blast-radius targeting. | Gap list of which identifier forms external sources may provide. | Silent fallback, new persisted identity state, runtime resolver changes. | Ambiguous identifiers are silently resolved or priority is redefined. |
| User identifier inputs | No governed S5-B user identity source contract exists. | `UNKNOWN` | User/context inputs may be useful but can drift into RBAC or tenancy. | Product question: whether user identity belongs in S5-B discovery and which non-sensitive shape is allowed. | User directory integration, access-control design, tenancy model. | User fields become enterprise RBAC, authz, or multi-tenant ownership scope. |
| Host/context enrichment | S4-A asset fields and loosely typed topology exist; deeper topology typing is deferred. | `NEEDS_DECISION` | Enrichment can improve context but must not become identity authority or CMDB sync. | Synthetic/redacted context-shape examples marked non-authorizing. | CMDB sync, topology API, trust precedence changes. | Enrichment is treated as authoritative identity source. |
| Source freshness expectation | S4-A defines `startup`, `ttl`, and `manual`; Sprint 5 defers live refresh design. | `NEEDS_DECISION` | Freshness expectations can imply runtime sync or data platform scope. | Freshness question list separating product expectations from implementation choices. | Live refresh, background jobs, stale-serve-through, performance commitments. | Freshness wording implies runtime refresh behavior. |
| Refresh trigger / polling / sync behavior | S4-A keeps live background refresh and stale-serve-through out of scope. | `DEFERRED` | Refresh mechanics require implementation and operational decisions not present here. | Future decision placeholder only. | Polling, sync jobs, CMDB sync, queueing, scheduler dependencies. | Discovery introduces live refresh, polling, or sync behavior. |
| Source confidence / provenance | S4-A includes `source_refs[]` and `confidence`; S4-A review lists unsupported fields. | `NEEDS_DECISION` | Confidence and provenance may influence trust but cannot silently change authority. | Provenance field inventory and trust-precedence questions. | New trust model, automatic source precedence, hidden fallback. | Confidence is used to bypass resolver authority or ambiguity rules. |
| Missing field handling | S4-A lists unsupported source fields and deferred items; S4-A adapter failures are diagnosable. | `NEEDS_DECISION` | Missing fields must stay explicit rather than becoming implicit defaults. | Matrix of `UNKNOWN`, `DEFERRED`, and optional synthetic fields. | Treating absent fields as provided; production readiness claims. | Unknown fields are accepted as complete without decision. |
| Redaction / secret handling | S5-A intake and assessment prohibit secret values and raw sensitive payloads; real pilot redaction remains `UNKNOWN`. | `NEEDS_DECISION` | Source examples can contain secrets, identity data, or customer context. | Redaction rule checklist and prohibited-field list only. | Real credentials, raw payloads, auth material, unredacted customer/operator data. | Credentials, tokens, auth headers, cookies, API keys, or raw payloads appear. |
| Synthetic fixture shape needs | S5-B discovery allows synthetic fixtures and redacted example shapes only. | `NEEDS_DECISION` | Future fixture work needs safe shape boundaries before tests or contracts. | Non-authorizing fixture-shape proposal using synthetic asset/context examples. | Real payloads, test changes, contract freeze, production readiness. | Synthetic shape is treated as real source contract or external evidence. |
| External pilot sample payload needs | External pilot input assessment has all seven categories `UNKNOWN`; no real sample payloads are governed. | `UNKNOWN` | Real source samples may inform later decisions, but are not available now. | External input request list without payload capture. | Collecting raw sample payloads, declaring pilot package ready. | Matrix output is treated as real customer evidence or pilot authorization. |
| Source adapter contract readiness | S4-A adapter envelope exists; `api` and `hybrid` are unavailable; `bundle` reuses local files. | `DEFERRED` | Contract readiness requires source inputs and product/governance decisions. | Future contract-sketch decision after gap matrix and synthetic fixture shape. | Freezing adapter contract, implementing adapters, changing dependencies. | Adapter contract is frozen or implemented from this matrix. |
| Identity authority impact | S4-A accepts asset inventory as canonical host authority and requires resolver routing. | `NEEDS_DECISION` | Any source expansion must be checked against identity authority before contract freeze. | Identity-impact checklist for later S5-B-3 decision. | S4-A authority change, resolver priority change, multi-source federation. | Identity authority, normalization semantics, or trust precedence change without external review. |
| Telemetry handoff to S5-D | S5-D remains discovery/fixture-only until telemetry inputs are available. | `DEFERRED` | Source and telemetry discovery overlap at identity and host-selection boundaries. | Handoff note listing telemetry-specific questions for S5-D. | Telemetry implementation, live EDR/SIEM access, queue/fan-out, performance commitments. | S5-B expands into S5-D implementation or telemetry source access. |

## S4-A Identity Authority Preservation
- S5-B does not replace `AssetInventorySnapshot` as the current host identity seed.
- S5-B does not change resolver priority: `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- S5-B does not silently resolve ambiguity.
- `api` and `hybrid` source modes remain unavailable unless a later governed decision changes them.
- `bundle` behavior remains governed by the current S4-A adapter baseline and is not redefined here.
- Any identity mapping change requires a later governed decision and external review if it changes authority or semantics.

## Safe Evidence Plan

| Evidence type | Use | Boundary |
| --- | --- | --- |
| Governed docs | Source of existing S4-A/S5-B/S5-A/S5-D constraints and known deferrals. | Docs are evidence of current baseline, not permission to implement. |
| Synthetic fixture examples | Explore possible source shapes without real source payloads. | Must be clearly synthetic and non-authorizing. |
| Redacted shape examples | Show field categories while excluding sensitive values. | Must not include raw customer/operator/source payloads or secrets. |
| Source/input question list | Record decisions needed before source contract or implementation work. | Questions are not approvals. |
| Non-authorizing contract sketch | Prepare language for later product/governance review. | Must not freeze adapter contract or identity mapping. |
| Read-only repo inventory | Identify current adapters, tests, fixtures, and docs already present. | Inventory must not modify code, tests, fixtures, or manifest. |
| External input request list | Ask product/governance what external inputs are needed. | Must not collect real credentials, raw payloads, or live access through this document. |

Prohibited evidence:
- real credentials
- raw external payloads
- real customer/operator data
- screenshots or files outside `D:\产品设计\New folder` as source truth
- live external calls
- auth headers
- cookies
- bearer tokens
- API keys

## External Pilot Input Relationship
This gap matrix can support future external pilot input collection by making source/input unknowns explicit. It cannot mark the external pilot package `READY`, cannot create real customer/operator evidence, and cannot authorize external pilot execution.

| S5-A unknown category | Related S5-B gap area | Matrix contribution | Boundary |
| --- | --- | --- | --- |
| Pilot scope | Source system inventory; external pilot sample payload needs. | Identifies which source inputs would need scoping if a future pilot uses source data. | Does not define pilot scope. |
| Participating roles | Not directly applicable to S5-B source/input discovery; source ownership and external input request list may later identify who can provide or approve source examples. | Records that source/provider ownership may need product/governance confirmation before real inputs are accepted. | Does not create participating roles, approval authority, RBAC, or real sign-off. |
| Environment and access boundary | Real source-system access; refresh/sync behavior; adapter contract readiness. | Lists source access and live refresh decisions that remain absent. | Does not authorize access. |
| Evidence retention policy | Redaction / secret handling; external pilot sample payload needs. | Flags that real source examples need retention policy before collection. | Does not retain real evidence. |
| Redaction approval for real pilot records | Redaction / secret handling; safe evidence plan. | Provides prohibited evidence categories and redacted-shape-only boundary. | Does not approve real pilot redaction. |
| Go/no-go authority | Identity authority impact; source contract readiness. | Shows source decisions that would need governance before go/no-go. | Does not create go authority. |
| Rollback/hold authority | HOLD conditions across source access, identity, and secrets. | Lists source-related hold triggers for later pilot planning. | Does not define pilot rollback authority. |

HOLD if matrix output is treated as real customer evidence, real operator sign-off, external pilot authorization, or proof that the external pilot package is `READY`.

## Candidate Follow-Up
Recommended next route: `PROCEED_TO_S5_B_2_SYNTHETIC_SOURCE_FIXTURE_SHAPE`.

Meaning:
- prepare a non-authorizing synthetic source fixture shape based on this gap matrix
- keep fixture examples synthetic, redacted, and docs-only unless a later ticket explicitly scopes fixture or test changes
- preserve S4-A identity authority and keep unresolved source fields marked as gaps

Non-meaning:
- no source adapter implementation
- no source contract freeze
- no real source access
- no identity mapping freeze
- no external pilot `READY` claim
- no runtime/API/schema/test/dependency change

If the next task attempts to freeze identity/source semantics, change S4-A authority, close S5-B, or accept real external evidence, re-evaluate `requires_external_review`.

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This matrix is treated as `READY`, `APPROVED`, `IMPLEMENTABLE`, or `PILOT_READY`. | Status vocabulary is intentionally non-authorizing. |
| Real source-system access is required. | No governed external source access exists. |
| Credentials or raw payloads appear. | S5-B-1 allows no secrets or raw source evidence. |
| Source adapter contract is frozen. | Contract freeze requires a later governed path and likely external review. |
| S4-A identity authority or resolver semantics change. | S5-B-1 inherits S4-A and does not alter it. |
| `api`, `hybrid`, or `bundle` behavior is redefined. | Source-mode behavior remains governed by S4-A/S4-A adapter baseline. |
| Runtime/API/schema/test/dependency changes appear. | This document is docs-only. |
| Live refresh, sync, CMDB, or multi-tenant behavior appears. | These require separate product/governance decisions. |
| External pilot or real sign-off is implied. | S5-A package remains `NOT_READY` / `UNKNOWN`. |
| AI_COLLAB `primary_implementor`, `reviewer`, or single-writer rules are bypassed. | Governed collaboration rules apply to this ticket. |

## Acceptance Criteria
This draft is acceptable when:
- all required gap areas are classified
- status vocabulary is bounded and non-authorizing
- S4-A identity authority is preserved
- external pilot `NOT_READY` / `UNKNOWN` boundary is preserved
- safe evidence plan excludes real credentials, payloads, and access
- follow-up recommendation is bounded
- no implementation, source adapter, runtime/API/schema/test/dependency change is authorized
- preliminary recommendation is one of `PROCEED_TO_S5_B_2_SYNTHETIC_SOURCE_FIXTURE_SHAPE`, `NEEDS_PRODUCT_DECISION`, `KEEP_DISCOVERY_ONLY`, or `HOLD`
