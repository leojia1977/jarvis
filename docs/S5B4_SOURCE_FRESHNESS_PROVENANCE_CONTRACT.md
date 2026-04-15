# S5-B-4 Source Freshness / Provenance Contract Candidate

## Document Control
- Title: S5-B-4 Source Freshness / Provenance Contract Candidate
- Baseline: `S5-B-DISCOVERY-2026-04-15-004`
- Source of truth: `D:\产品设计\New folder`
- Status: Draft for review
- Scope: docs-only non-implementing contract candidate
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code / human-supervised repo writer
- `reviewer`: Claude Code review-only
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false for draft if this candidate remains non-freezing and non-implementing; set to `true` if this document freezes source freshness/provenance semantics, modifies a frozen contract, changes source identity authority, changes trust precedence, accepts real external evidence, or is used for stream closeout

## Goal
Draft candidate source freshness and provenance semantics for later review.

This document does not authorize implementation, source adapter changes, runtime/API/schema/test/dependency changes, real source-system access, live refresh/sync/polling, CMDB sync, multi-tenant ownership, external pilot execution, real customer/operator sign-off, or S4-A identity authority changes. It provides contract-candidate terminology only.

## Non-Goals
- implementation
- runtime/API/schema/test/dependency changes
- source adapter contract freeze
- refresh, sync, polling, or job behavior
- live source-system, SIEM, or EDR access
- credentials, auth headers, tokens, or API keys
- raw customer/operator/source payloads
- CMDB sync
- multi-tenant ownership or RBAC
- trust precedence change
- S4-A identity authority or resolver change
- external pilot package `READY` decision
- external pilot execution or real customer/operator sign-off
- modifying S5-C semantics
- modifying `docs/AI_COLLAB_OPERATING_MODEL.md`

## Current Governed Baseline
- Active baseline is `S5-B-DISCOVERY-2026-04-15-004`.
- `docs/S5B3_SOURCE_IDENTIFIER_MAPPING_DECISION.md` selected `READY_FOR_LATER_CONTRACT_DRAFT` only as a non-authorizing decision.
- S5-B-3 did not freeze identity mapping, change S4-A authority, change resolver priority, approve source adapter behavior, or validate external evidence.
- `docs/S5B2_SYNTHETIC_SOURCE_FIXTURE_SHAPE.md` remains non-authorizing and does not freeze schema, fixture data, source contract, or identity mapping.
- `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md` keeps the external pilot package at `NOT_READY` because all seven required external pilot input categories remain `UNKNOWN`.
- S5-C remains parked, and `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` keeps the public close-case HTTP endpoint at `KEEP_DEFERRED`.

## Contract Candidate Status

| Status | Meaning | Non-meaning |
| --- | --- | --- |
| `CONTRACT_CANDIDATE` | Proposed terminology or evidence field for later review. | Does not mean frozen contract, implementation-ready, production-ready, externally validated, or pilot-ready. |
| `NEEDS_PRODUCT_DECISION` | Product/governance must choose semantics before the candidate can advance. | Does not approve a default behavior. |
| `DEFERRED` | Candidate is intentionally postponed until external inputs, product decision, or later stream work exist. | Does not permit hidden implementation. |
| `HOLD` | Boundary risk blocks continuation until ambiguity is resolved. | Does not authorize workaround or scope expansion. |

Freezing any source freshness/provenance contract requires later governed closeout and `requires_external_review=true`.

## Freshness Semantics Candidate

| Candidate term | Candidate meaning | Current evidence | Status | Not authorized | Product decision needed | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- |
| `source_observed_at` | Candidate timestamp for when the source claims the asset, user, or context state was observed. | S5-B-2 includes synthetic timestamp shape; S4-A carries static source metadata but no real external observation evidence. | `CONTRACT_CANDIDATE` | Real external timestamp retention, runtime freshness evaluation, source trust change. | Whether this is required for real source inputs and what redaction/precision rules apply. | Treated as proof of real source evidence or pilot readiness. |
| `source_collected_at` | Candidate timestamp for when the source record was collected into a governed package or synthetic fixture. | S4-A has local static bootstrap metadata; S5-B remains discovery-only. | `CONTRACT_CANDIDATE` | Live collection jobs, polling, sync behavior, external authentication. | Whether collection time is required separately from observed time. | Collection wording implies live refresh or source integration. |
| `source_ingested_at` | Candidate timestamp for when a later governed system would ingest a source record. | No current S5-B runtime ingestion scope exists. | `DEFERRED` | Runtime ingestion behavior, schema field, API response, persistence, tests. | Whether a later implementation needs an ingestion timestamp at all. | Ingestion timestamp is added to schema or tests from this document. |
| `source_age_label` | Candidate label for describing age in bounded language such as recent-like, stale-like, or unknown. | S5-B-1 identifies freshness expectation as a gap; no product threshold exists. | `CONTRACT_CANDIDATE` | Trust precedence, resolver priority changes, automated stale filtering. | Exact labels and whether thresholds are product-defined or source-provided. | Age label is used to accept/reject records at runtime. |
| `freshness_window_candidate` | Candidate review window for discussing acceptable source age. | No governed external source freshness requirement exists. | `NEEDS_PRODUCT_DECISION` | SLA, polling interval, production freshness guarantee, performance commitment. | Product/governance must decide if any freshness window is needed before a future contract freeze. | A window is treated as a production SLA or adapter requirement. |
| `stale_source_behavior_candidate` | Candidate language for what a later workflow might do when source freshness is stale. | Current S4-A adapter failures are bootstrap-diagnosable; S5-B has no stale-source runtime behavior. | `NEEDS_PRODUCT_DECISION` | Runtime fallback, stale-serve-through, source suppression, alert routing. | Product/governance must decide whether stale records are allowed, flagged, or blocked in a later ticket. | Candidate behavior changes runtime output or trust precedence. |
| `unknown_freshness_behavior` | Candidate rule that absent freshness evidence remains explicit and must not be silently upgraded. | S5-B-1 uses `UNKNOWN`; S5-A inputs remain `UNKNOWN`. | `CONTRACT_CANDIDATE` | Treating unknown as fresh, provided, approved, or pilot-ready. | Whether unknown freshness is acceptable for synthetic-only review. | Unknown freshness is hidden or inferred from chat/context. |
| `refresh_policy_label` | Candidate label for discussing source refresh expectations. | S4-A configuration includes refresh placeholders such as startup/TTL/manual semantics, but S5-B does not change them. | `CONTRACT_CANDIDATE` | Polling, sync jobs, live refresh, background workers, new dependencies. | Whether labels remain descriptive or become a later product requirement. | Label is interpreted as implemented polling/sync behavior. |

`refresh_policy_label` is a discussion label only. It does not imply polling, sync, job scheduling, stale-serve-through behavior, or a production refresh guarantee.

## Provenance Semantics Candidate

| Candidate term | Candidate meaning | Current evidence | Status | Not authorized | Product decision needed | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- |
| `source_system_label` | Candidate non-sensitive label naming the source family or synthetic source group. | S5-B-2 includes source system label shape; S4-A metadata carries source kind/name. | `CONTRACT_CANDIDATE` | Source authority, external validation, source ownership semantics. | Whether labels are product-controlled, operator-provided, or synthetic-only. | Label is treated as trusted identity authority. |
| `source_mode_candidate` | Candidate discussion label for local-file-like, api-candidate, hybrid-candidate, or bundle-like source mode. | S5-B-2 keeps these as discussion labels; S4-A keeps `api` and `hybrid` unavailable and does not redefine `bundle`. | `CONTRACT_CANDIDATE` | Approved adapter mode, `api`/`hybrid` enablement, bundle behavior change. | Whether any future source-mode decision should be drafted separately. | Candidate mode is treated as implementation-ready. |
| `source_confidence_label` | Candidate provenance label for confidence discussion. | S4-A exposes confidence in identity records, but S5-B has not frozen trust semantics. | `NEEDS_PRODUCT_DECISION` | Resolver priority change, trust precedence, automatic conflict resolution. | Product/governance must decide if confidence labels affect later contracts, or remain annotation only. | Confidence label changes authority or silently resolves ambiguity. |
| `source_provenance_note` | Candidate redacted note explaining where a synthetic or future source shape came from. | S5-B-1 permits redacted shape descriptions and governed docs only. | `CONTRACT_CANDIDATE` | Raw payload retention, real customer/operator detail, external evidence acceptance. | Whether provenance notes need a fixed redaction checklist in later work. | Note includes raw source/customer/operator payloads. |
| `source_record_scope` | Candidate scope label describing whether a record is asset, user, host-context, or mixed context. | S5-B-1 gap matrix separates identity, user, context, and telemetry handoff areas. | `CONTRACT_CANDIDATE` | Multi-tenant ownership model, RBAC, CMDB sync, host identity authority change. | Whether mixed-scope records require a later product decision. | Scope label creates ownership or authorization semantics. |
| `source_transform_note` | Candidate redacted note describing synthetic normalization, omission, or redaction applied to an example shape. | S4-A adapter baseline normalizes static data; S5-B-2 is documentation-only and creates no fixtures. | `CONTRACT_CANDIDATE` | Runtime transform behavior, schema mapping, adapter implementation. | Whether future contract candidates need required transform-note fields. | Transform note is treated as implemented adapter behavior. |
| `redaction_applied` | Candidate marker that a synthetic or future shape has been redacted. | S5-A requires separate real-pilot redaction approval; S5-B permits synthetic/redacted shapes only. | `CONTRACT_CANDIDATE` | Real redaction approval, real evidence retention, secret handling waiver. | Whether future real evidence requests need separate redaction approval before acceptance. | Marker is treated as approval to retain real pilot/source evidence. |
| `synthetic_fixture_marker` | Candidate marker that a described example is synthetic and not real source evidence. | S5-B-2 defines synthetic-only fixture shape but does not create fixture files. | `CONTRACT_CANDIDATE` | Fixture file creation, source adapter contract freeze, pilot evidence claim. | Whether a later fixture ticket should create actual files. | Synthetic marker is omitted or example is mistaken for real evidence. |
| `external_evidence_status` | Candidate status for whether external evidence is absent, requested, provided, rejected, or deferred in later work. | S5-A external pilot inputs remain `UNKNOWN`; S5-B has no real external evidence. | `DEFERRED` | Acceptance or retention of real external evidence, pilot readiness decision. | Product/governance must define any future external evidence intake path. | Status is used to accept real external evidence without governed approval. |

`source_mode_candidate` remains discussion-only. It does not change `api`, `hybrid`, or `bundle` availability and does not authorize source adapter implementation.

## Trust / Authority Boundary
- Provenance metadata does not create identity authority.
- Confidence labels do not change resolver priority.
- Freshness labels do not change trust precedence.
- `source_system_label` is provenance only.
- `source_mode_candidate` is adapter discussion only.
- `AssetInventorySnapshot` remains the current host identity seed.
- Resolver priority remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- Ambiguity remains explicit and must not be silently resolved.

## Safe Evidence Boundary

Allowed evidence:
- governed docs
- synthetic fixture examples from S5-B-2
- redacted shape descriptions
- non-authorizing contract candidate language
- `UNKNOWN`, `NEEDS_PRODUCT_DECISION`, and `DEFERRED` markers

Prohibited evidence:
- real credentials
- auth headers
- cookies
- bearer tokens
- API keys
- raw source/SIEM/EDR payloads
- raw customer/operator payloads
- real external evidence retention
- live external calls

## External Pilot Relationship
Freshness and provenance candidate terms can help formulate future pilot input requests, especially environment/access boundary, evidence retention, redaction approval, and source/input sample questions.

They cannot:
- mark the external pilot package `READY`
- accept real external evidence
- create redaction approval for real pilot records
- create retention approval for real pilot records
- create real customer/operator sign-off
- authorize external pilot execution

S5-A remains `NOT_READY` / `UNKNOWN` until product/governance explicitly provides or accepts all required external pilot inputs.

## Recommended Decision
Preliminary decision: `READY_FOR_S5_B_5_DISCOVERY_REVIEW_PASS`.

This recommendation applies only because this document remains non-freezing and no product decision is required before reviewing the S5-B discovery artifacts as a stream.

Meaning:
- S5-B discovery artifacts can be reviewed together for stream-level `PASS`, `HOLD`, or `NEEDS_DECISION`.
- Freshness/provenance semantics remain candidates only.
- No implementation or external access is authorized.

Non-meaning:
- no contract freeze
- no runtime behavior
- no source adapter implementation
- no live refresh/sync/polling
- no real evidence acceptance
- no external pilot `READY` claim

If product/governance decides freshness windows, stale behavior, confidence semantics, or external evidence status must be selected before stream review, change the decision to `NEEDS_PRODUCT_DECISION`.

## Candidate Follow-Up Tickets

| Candidate | Purpose | Allowed scope | Not authorized | `requires_external_review` decision | HOLD trigger |
| --- | --- | --- | --- | --- | --- |
| `S5-B-5 S5-B Discovery Review Pass` | Review S5-B discovery artifacts and produce stream-level `PASS`, `HOLD`, or `NEEDS_DECISION`. | Docs-only stream review and closeout. | Implementation, source adapter changes, real source access, pilot readiness claim. | `true` because stream or milestone closeout triggers external review under AI_COLLAB. | Review pass declares production readiness, pilot readiness, or frozen source contract. |
| `S5-B-4A Source Identifier Mapping Contract Candidate` | Draft a separate non-implementing mapping candidate if identity mapping needs focused review. | Docs-only candidate preserving S4-A authority and ambiguity handling. | Mapping freeze, resolver changes, fixture/test/code changes, real evidence acceptance. | `true` if it freezes mapping, changes S4-A authority, changes resolver behavior, changes trust precedence, modifies a frozen contract, or accepts real external evidence. | Candidate mapping is treated as approved identity authority. |
| `S5-D bounded telemetry discovery` | Start telemetry-focused discovery if S5-B artifacts reveal telemetry handoff questions. | Docs-only telemetry questions, gap matrix, and non-authorizing evidence boundaries. | Telemetry implementation, external source connection, normalization freeze, dependencies. | `true` if it changes telemetry normalization semantics, closes a stream, or accepts real external telemetry evidence. | Telemetry discovery becomes production integration or real external access. |

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| Candidate terms are treated as frozen contract. | This artifact is a non-implementing contract candidate only. |
| Freshness labels imply live refresh, sync, polling, stale-serve-through, or job behavior. | Runtime refresh behavior is out of scope. |
| Provenance or confidence labels change trust precedence. | S4-A authority and resolver priority remain unchanged. |
| `source_system_label` or `source_mode_candidate` creates source authority. | These labels are provenance/discussion only. |
| S4-A identity authority or resolver priority changes. | S5-B inherits S4-A without change. |
| `api`, `hybrid`, or `bundle` behavior is redefined. | S5-B-4 does not change source-mode availability. |
| Real source-system access is required. | No governed real source access exists. |
| Real external evidence is accepted or retained. | External evidence intake and retention require separate approval. |
| Credentials, auth headers, cookies, bearer tokens, API keys, or raw payloads appear. | Secrets and raw external/customer/operator payloads are prohibited. |
| Runtime/API/schema/test/dependency changes appear. | This document authorizes no implementation changes. |
| External pilot execution or real customer/operator sign-off is implied. | S5-A remains `NOT_READY` / `UNKNOWN`. |
| AI_COLLAB `primary_implementor`, `reviewer`, single-writer, or external-review rules are bypassed. | Governed collaboration rules apply to this work. |

## Acceptance Criteria
This draft is acceptable when:
- freshness candidate terms are defined
- provenance candidate terms are defined
- `CONTRACT_CANDIDATE` is non-authorizing
- trust/authority boundary preserves S4-A identity authority
- safe evidence boundary excludes real credentials, raw payloads, real external access, and real evidence retention
- external pilot `NOT_READY` / `UNKNOWN` status is preserved
- recommended decision is bounded
- no implementation, source adapter, runtime/API/schema/test/dependency change is authorized
- preliminary recommendation is one of `READY_FOR_S5_B_5_DISCOVERY_REVIEW_PASS`, `NEEDS_PRODUCT_DECISION`, `KEEP_DISCOVERY_ONLY`, or `HOLD`
