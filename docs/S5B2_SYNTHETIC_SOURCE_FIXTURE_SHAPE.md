# S5-B-2 Synthetic Source Fixture Shape

## Document Control
- Title: S5-B-2 Synthetic Source Fixture Shape
- Baseline: `S5-B-DISCOVERY-2026-04-15-002`
- Source of truth: `D:\产品设计\New folder`
- Status: Draft for review
- Scope: docs-only synthetic fixture shape discovery
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code / human-supervised repo writer
- `reviewer`: Claude Code review-only
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false for draft; re-evaluate at closeout or if fixture shape is treated as contract freeze, source semantics freeze, identity authority change, or stream closeout

## Goal
Sketch a synthetic, redacted, non-authorizing source fixture shape to support later S5-B source/input decisions.

This document does not authorize implementation, fixture file creation, source adapter changes, source contract freeze, runtime/API/schema/test/dependency changes, real source-system access, live refresh/sync, external authentication, CMDB sync, multi-tenant ownership, external pilot execution, real customer/operator sign-off, or S4-A identity authority changes.

## Non-Goals
- creating or modifying fixture files
- production source integration
- freezing a source adapter contract
- changing S4-A identity authority or resolver priority
- runtime/API/schema/test/dependency changes
- real source-system, SIEM, or EDR access
- credentials, auth headers, tokens, or API keys
- raw customer/operator/source payloads
- live refresh or sync jobs
- CMDB sync
- multi-tenant ownership or RBAC
- external pilot execution or real customer/operator sign-off
- modifying S5-C semantics
- modifying `docs/AI_COLLAB_OPERATING_MODEL.md`

## Current Governed Baseline
- Active baseline is `S5-B-DISCOVERY-2026-04-15-002`.
- `docs/S5B1_SOURCE_INPUT_GAP_MATRIX.md` recommended `PROCEED_TO_S5_B_2_SYNTHETIC_SOURCE_FIXTURE_SHAPE`.
- S5-B-1 gap statuses remain non-authorizing and do not mean `READY`, `APPROVED`, `IMPLEMENTABLE`, or `PILOT_READY`.
- S4-A identity authority remains inherited.
- `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md` keeps the external pilot package at `NOT_READY` because all seven required input categories remain `UNKNOWN`.
- S5-C remains parked, and `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` keeps the public close-case HTTP endpoint at `KEEP_DEFERRED`.
- This document is a fixture-shape discovery artifact only, not a source contract freeze.

## Fixture Shape Principles
- Synthetic only: examples must be invented, generic, and safe.
- Redacted by design: source examples must omit sensitive payloads before they are written.
- Non-authorizing: field names and labels support discussion only.
- No real credentials, auth material, raw payloads, or live calls are allowed.
- S4-A identity authority remains authoritative for host identity.
- The fixture shape does not freeze a source adapter contract.
- Unresolved fields remain `UNKNOWN`, `NEEDS_DECISION`, or `DEFERRED`.
- The shape supports future discussion and review, not implementation.

## Proposed Synthetic Fixture Shape
This table is documentation only. It is not code, JSON, schema, fixture data, adapter input, or an implementation-ready contract.

| Candidate field | Synthetic example or allowed value shape | S5-B-1 gap link | S4-A relationship | Redaction / sensitivity boundary | Status | Not authorized |
| --- | --- | --- | --- | --- | --- | --- |
| `fixture_id` | Synthetic label such as `synthetic-source-fixture-001`. | synthetic fixture shape needs | No resolver effect. | Must not include customer, operator, system, or environment names. | `NEEDS_DECISION` | Fixture file creation or persisted fixture ID contract. |
| `source_system_label` | Generic label such as `asset_source_candidate` or `context_source_candidate`. | source system inventory | Source label cannot become identity authority. | Must not name a real customer/source system unless separately governed. | `UNKNOWN` | Real source-system approval or production source inventory. |
| `source_mode_candidate` | Discussion labels only: `local_file_like`, `api_candidate`, `hybrid_candidate`, `bundle_like`. | source adapter contract readiness | S4-A source modes remain governed; `api` and `hybrid` stay unavailable for implementation. | Label only; no URL, token, endpoint, or vendor payload. | `NEEDS_DECISION` | Approved adapter mode, source contract freeze, or implementation. |
| `asset_id_candidate` | Synthetic asset ID such as `asset-synth-001`. | asset identifier mapping | Candidate input to S4-A resolver; cannot replace `AssetInventorySnapshot`. | Synthetic only; no real asset IDs. | `NEEDS_DECISION` | Identity authority change or mapping freeze. |
| `hostname_candidate` | Synthetic hostname such as `workstation-alpha`. | hostname / FQDN / IP / alias mapping | Candidate input only; resolver priority remains after `asset_id`. | No real hostnames or customer naming patterns. | `NEEDS_DECISION` | Silent hostname authority or resolver priority change. |
| `fqdn_candidate` | Synthetic FQDN such as `workstation-alpha.example.invalid`. | hostname / FQDN / IP / alias mapping | Candidate input only; resolver priority remains after hostname. | Use reserved or invalid example domains only. | `NEEDS_DECISION` | DNS validation, external lookup, or identity freeze. |
| `ip_address_candidate` | Reserved example IP such as `192.0.2.10`. | hostname / FQDN / IP / alias mapping | Candidate input only; resolver priority remains after FQDN. | Use reserved/example IP ranges only. | `NEEDS_DECISION` | Real network targeting or source-system access. |
| `alias_candidates` | Synthetic list shape such as `alias-alpha`, `endpoint-alpha`. | hostname / FQDN / IP / alias mapping | Candidate inputs only; resolver priority checks aliases last. | No real aliases, account names, or hostnames. | `NEEDS_DECISION` | Alias precedence change or ambiguity suppression. |
| `user_identifier_candidate` | Generic user label such as `user-alpha` or `analyst-synthetic`. | user identifier inputs | No S4-A host identity authority; may require future product decision. | No real names, emails, SIDs, employee IDs, or directory identifiers. | `UNKNOWN` | Enterprise identity, RBAC, tenant model, or authz semantics. |
| `host_context_labels` | Non-sensitive labels such as `finance-like`, `critical-workstation-like`, `lab-segment`. | host/context enrichment | Context may inform discussion but cannot become identity authority. | Generic labels only; no real business unit, owner, or segment names. | `NEEDS_DECISION` | CMDB sync, trust precedence, or ownership model. |
| `source_freshness_label` | Discussion label such as `snapshot_like`, `manual_review_needed`, or `stale_unknown`. | source freshness expectation | S4-A `startup`, `ttl`, and `manual` remain governed refresh semantics. | No live refresh metadata from external systems. | `NEEDS_DECISION` | Live refresh, polling, sync job, or freshness SLA. |
| `source_observed_at_utc_example` | Synthetic timestamp shape such as `2026-04-15T00:00:00Z`. | source freshness expectation | Timestamp is example evidence only; it does not alter S4-A metadata rules. | Use synthetic or placeholder times only. | `NEEDS_DECISION` | Real evidence timestamp retention or replay requirement. |
| `source_confidence_label` | Discussion label such as `synthetic_high`, `synthetic_medium`, or `unknown`. | source confidence / provenance | Cannot create new trust precedence or resolver behavior. | No vendor confidence scores from raw payloads. | `NEEDS_DECISION` | Production trust model or confidence contract freeze. |
| `source_provenance_note` | Redacted note such as `synthetic example derived from governed docs`. | source confidence / provenance | Provenance informs traceability but cannot override resolver authority. | No raw source excerpts, screenshots, or repo-external files as truth. | `NEEDS_DECISION` | Real evidence retention or source provenance authority. |
| `missing_fields` | List shape such as `owner_unknown`, `source_scope_unknown`. | missing or unknown source fields | Missing fields remain explicit and must not be silently filled. | Do not infer real values from chat or external files. | `UNKNOWN` | Treating unknowns as provided or pilot-ready. |
| `redaction_notes` | Notes such as `no secrets`, `no raw payload`, `use reserved IP`. | redaction / secret handling | Supports S5-A/S5-B redaction boundary; does not change S4-A. | Must omit credentials, tokens, auth headers, cookies, and raw payloads. | `NEEDS_DECISION` | Redaction approval for real pilot records. |
| `identity_mapping_status` | One of `UNKNOWN`, `NEEDS_DECISION`, `DEFERRED`, or `NOT_APPLICABLE`. | identity authority impact | Unresolved mapping must stay explicit; no ambiguity suppression. | Status only; no real identity mapping record. | `NEEDS_DECISION` | Mapping freeze or S4-A authority change. |
| `pilot_input_gap_refs` | References to gap categories such as `pilot_scope_unknown` or `environment_access_unknown`. | external pilot sample payload needs | No S4-A effect. | Gap references only; no real external payloads or sign-off. | `UNKNOWN` | Pilot package readiness claim. |
| `s5b_status` | One of `UNKNOWN`, `NEEDS_DECISION`, `DEFERRED`, or `NOT_APPLICABLE`. | missing or unknown source fields | Status labels do not alter source contracts. | Status only; no production readiness claim. | `UNKNOWN` | `READY`, `APPROVED`, `IMPLEMENTABLE`, or `PILOT_READY` status. |

## Status and Value Constraints
Allowed status labels in this document:
- `UNKNOWN`
- `NEEDS_DECISION`
- `DEFERRED`
- `NOT_APPLICABLE`

No status label in this document means `READY`, `APPROVED`, `IMPLEMENTABLE`, or `PILOT_READY`.

Allowed `source_mode_candidate` values are discussion labels only:
- `local_file_like`
- `api_candidate`
- `hybrid_candidate`
- `bundle_like`

`api_candidate` and `hybrid_candidate` remain unavailable for implementation under S4-A unless a later governed decision changes them. `bundle_like` does not redefine current bundle behavior. No value in this document means production source mode, approved adapter mode, source contract freeze, or implementation readiness.

## Relationship To S4-A Identity Resolver
S5-B-2 inherits S4-A identity authority:
- `AssetInventorySnapshot` remains the current host identity seed.
- Resolver priority remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- Ambiguity is explicit and must never be silently resolved.
- Fixture fields are candidate inputs only and cannot override resolver behavior.
- `identity_mapping_status` should mark unresolved mapping as `UNKNOWN` or `NEEDS_DECISION`.

HOLD if the synthetic fixture shape changes identity authority, resolver priority, ambiguity handling, normalization semantics, trust precedence, or source ownership semantics.

## Redaction and Secret Handling
Prohibited categories:
- credentials
- auth headers
- cookies
- bearer tokens
- API keys
- raw customer/operator payloads
- raw SIEM/EDR/source payloads
- screenshots or files outside the repo as source truth
- live external calls

Allowed safe categories:
- synthetic hostnames
- synthetic asset IDs
- reserved/example IP ranges
- generic user labels
- redacted provenance notes
- non-sensitive labels

If a proposed example cannot be proven synthetic and non-sensitive, it must be omitted or marked `UNKNOWN` until product/governance provides an approved redacted form.

## External Pilot Input Relationship
The fixture shape may reference S5-A and S5-B gap areas, but it cannot satisfy them. It cannot make the external pilot package `READY`, create real operator/customer evidence, create real customer/operator sign-off, or authorize external pilot execution.

`pilot_input_gap_refs` must point to gap categories rather than real external payloads.

| S5-A input category | Fixture-shape relationship | Boundary |
| --- | --- | --- |
| Pilot scope | May reference `pilot_scope_unknown` as a gap. | Does not define pilot scope. |
| Participating roles | May reference future source ownership or input-request role questions. | Does not create real role roster, customer/operator sign-off, RBAC, or authority. |
| Environment and access boundary | May reference `environment_access_unknown`. | Does not approve real source-system, SIEM, EDR, or remote access. |
| Evidence retention policy | May reference retention as a required future decision for real source samples. | Does not authorize retention of real source evidence. |
| Redaction approval for real pilot records | May list redaction needs for future real samples. | Does not approve redaction for real pilot records. |
| Go/no-go authority | May reference go/no-go as a pilot readiness gap. | Does not name go/no-go authority. |
| Rollback/hold authority | May reference hold criteria for future real source access. | Does not create rollback or hold authority. |

## Candidate Follow-Up
Preferred preliminary recommendation: `PROCEED_TO_S5_B_3_SOURCE_IDENTIFIER_MAPPING_DECISION`.

Use this route only if the fixture shape surfaces identity mapping questions that need a product/governance decision.

Because S5-B-3 concerns source identifier mapping, its ticket must re-evaluate `requires_external_review` and set it to `true` if the decision freezes identity/source semantics, changes S4-A authority, changes resolver behavior, or accepts real external evidence.

Meaning:
- prepare a later decision document for source identifier mapping questions
- keep source identifiers aligned to S4-A authority before any source contract or adapter work is considered
- decide whether candidate identifier fields remain `UNKNOWN`, need a bounded mapping decision, or should stay deferred

Non-meaning:
- no identity mapping freeze now
- no S4-A authority change
- no source adapter implementation
- no fixture file creation
- no real source-system access
- no external pilot `READY` claim

Allowed next-route values:
- `PROCEED_TO_S5_B_3_SOURCE_IDENTIFIER_MAPPING_DECISION`
- `NEEDS_PRODUCT_DECISION`
- `KEEP_DISCOVERY_ONLY`
- `HOLD`

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This fixture shape is treated as contract freeze or implementation-ready schema. | S5-B-2 is docs-only discovery. |
| Fixture files are created or modified. | This ticket permits no fixture file changes. |
| Real source-system access is required. | No governed external source access approval exists. |
| Credentials, auth headers, tokens, cookies, API keys, or raw payloads appear. | Synthetic source discovery must not collect secrets or raw evidence. |
| `api_candidate`, `hybrid_candidate`, or `bundle_like` are treated as approved source modes. | These are discussion labels only. |
| S4-A resolver priority or ambiguity handling changes. | S4-A identity authority is inherited unchanged. |
| Identity mapping is frozen. | Mapping decisions require a later governed decision and possible external review. |
| Runtime/API/schema/test/dependency changes appear. | This artifact authorizes no implementation changes. |
| Live refresh, sync jobs, CMDB sync, or multi-tenant behavior appears. | These remain outside bounded S5-B discovery. |
| External pilot execution or real sign-off is implied. | S5-A external pilot package remains `NOT_READY` / `UNKNOWN`. |
| AI_COLLAB `primary_implementor`, `reviewer`, or single-writer rules are bypassed. | The governed operating model applies to this ticket. |

## Acceptance Criteria
This draft is acceptable when:
- all required candidate fields are described
- the shape is table/documentation only, not code, JSON, schema, or fixture file
- statuses are bounded and non-authorizing
- `source_mode_candidate` values are discussion labels only
- S4-A identity authority and resolver order are preserved
- redaction and secret-handling boundaries are explicit
- external pilot `NOT_READY` / `UNKNOWN` boundary is preserved
- follow-up recommendation is bounded
- no implementation, source adapter change, runtime/API/schema/test/dependency change, real source access, fixture file creation, external pilot execution, or real customer/operator sign-off is authorized
- preliminary recommendation is one of `PROCEED_TO_S5_B_3_SOURCE_IDENTIFIER_MAPPING_DECISION`, `NEEDS_PRODUCT_DECISION`, `KEEP_DISCOVERY_ONLY`, or `HOLD`
