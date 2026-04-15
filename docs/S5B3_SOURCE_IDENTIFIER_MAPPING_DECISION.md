# S5-B-3 Source Identifier Mapping Decision

## Document Control
- Title: S5-B-3 Source Identifier Mapping Decision
- Baseline: `S5-B-DISCOVERY-2026-04-15-003`
- Source of truth: `D:\产品设计\New folder`
- Status: Draft for review
- Scope: docs-only source identifier mapping decision
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code / human-supervised repo writer
- `reviewer`: Claude Code review-only
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false for draft; set to `true` if this decision freezes identity/source semantics, changes S4-A authority, changes resolver behavior, changes trust precedence, changes source ownership semantics, or accepts real external evidence; re-evaluate at closeout

## Goal
Evaluate source identifier mapping questions surfaced by `docs/S5B1_SOURCE_INPUT_GAP_MATRIX.md` and `docs/S5B2_SYNTHETIC_SOURCE_FIXTURE_SHAPE.md`.

This document does not freeze identity mapping, change S4-A identity authority, change resolver priority, authorize source adapter implementation, authorize runtime/API/schema/test/dependency changes, or authorize real external source access. It only classifies mapping questions and recommends whether a later non-implementing contract candidate is safe to draft.

## Non-Goals
- freezing identifier mapping
- changing S4-A identity authority
- changing resolver priority
- silently resolving ambiguity
- changing trust precedence or source ownership semantics
- production source integration
- source adapter contract freeze
- fixture file creation or modification
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
- Active baseline is `S5-B-DISCOVERY-2026-04-15-003`.
- `docs/S5B2_SYNTHETIC_SOURCE_FIXTURE_SHAPE.md` recommended `PROCEED_TO_S5_B_3_SOURCE_IDENTIFIER_MAPPING_DECISION`.
- S5-B-2 fixture shape remains non-authorizing and does not freeze schema, fixture data, source contract, or identity mapping.
- S4-A identity authority remains inherited.
- `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md` keeps the external pilot package at `NOT_READY` because all seven required input categories remain `UNKNOWN`.
- S5-C remains parked, and `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` keeps the public close-case HTTP endpoint at `KEEP_DEFERRED`.
- This document is a decision planning artifact only.

## Decision Vocabulary

| Outcome | Meaning | Non-meaning |
| --- | --- | --- |
| `KEEP_DISCOVERY_ONLY` | Mapping questions remain useful discovery notes only. | Does not authorize contract drafting or implementation. |
| `NEEDS_PRODUCT_DECISION` | Product/governance input is required before a later contract candidate can be drafted. | Does not approve any mapping rule. |
| `READY_FOR_LATER_CONTRACT_DRAFT` | A later non-implementing contract candidate may be drafted for review. | Does not freeze mapping, authorize implementation, or validate external evidence. |
| `HOLD` | A boundary risk blocks even decision-planning continuation. | Does not authorize workaround or scope expansion. |

No outcome means identity mapping is approved, production-ready, pilot-ready, externally validated, implementation-ready, or accepted as a source adapter contract.

## Identifier Mapping Questions

| Candidate identifier | Current S4-A relationship | Decision status | Why it matters | Safe next step | Not authorized | `requires_external_review` trigger if advanced | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `asset_id_candidate` to S4-A `asset_id` | `asset_id` is the first resolver priority and maps to the current `AssetInventorySnapshot` identity seed. | `READY_FOR_LATER_CONTRACT_DRAFT` | This is the cleanest candidate mapping, but still cannot be frozen here. | Draft a later non-implementing mapping candidate that preserves S4-A authority. | Mapping freeze, runtime resolver change, source adapter implementation. | Trigger if a later ticket freezes accepted asset ID mapping or changes authority. | Candidate asset IDs are treated as authoritative without governed contract review. |
| `hostname_candidate` to resolver `hostname` | `hostname` is the second resolver priority after `asset_id`. | `READY_FOR_LATER_CONTRACT_DRAFT` | Hostname mappings are common but can be ambiguous across environments. | Define ambiguity-preserving candidate language for later review. | Silent fallback, priority change, production lookup change. | Trigger if hostname mapping semantics are frozen or resolver behavior changes. | Hostname ambiguity is silently resolved. |
| `fqdn_candidate` to resolver `fqdn` | `fqdn` is the third resolver priority. | `READY_FOR_LATER_CONTRACT_DRAFT` | FQDN can disambiguate hostnames but may encode environment details. | Draft redacted/synthetic FQDN mapping guidance only. | Real DNS lookup, external validation, priority change. | Trigger if FQDN mapping becomes a frozen source semantic. | Real FQDNs or external lookup behavior are introduced. |
| `ip_address_candidate` to resolver `ip_address` | `ip_address` is the fourth resolver priority and must not override stronger identifiers. | `READY_FOR_LATER_CONTRACT_DRAFT` | IP addresses can be reused, stale, or NAT-obscured. | Draft stale/ambiguous IP mapping questions for later contract review. | Real network targeting, IP authority change, runtime lookup change. | Trigger if IP trust precedence or stale-IP semantics are frozen. | IP is promoted above asset ID, hostname, or FQDN. |
| `alias_candidates` to resolver `aliases` | `aliases` are checked last in the S4-A resolver priority. | `READY_FOR_LATER_CONTRACT_DRAFT` | Aliases are useful but high-risk for ambiguity. | Draft alias handling as lowest-priority and ambiguity-explicit. | Alias precedence change, alias authority, ambiguity suppression. | Trigger if alias semantics or trust precedence are frozen. | Alias mapping silently resolves multiple candidates. |
| `user_identifier_candidate` relationship to S5-B | No current S4-A host resolver authority. | `NEEDS_PRODUCT_DECISION` | User identifiers may support context but can drift into RBAC, tenancy, or directory integration. | Ask product/governance whether user identity belongs in S5-B source scope. | Enterprise identity, RBAC, authz, tenant model, host identity authority. | Trigger if user identifiers become source semantics or identity authority. | User identifiers are treated as host identity authority. |
| `host_context_labels` relationship to enrichment | Context labels may enrich source records but are not identity authority. | `READY_FOR_LATER_CONTRACT_DRAFT` | Context can help analysts but must not override resolver output. | Draft non-authorizing enrichment wording with provenance limits. | CMDB sync, ownership model, trust precedence change. | Trigger if context labels affect identity/source authority. | Context labels become canonical identity or ownership authority. |
| `source_system_label` relationship to provenance | Source labels describe provenance and do not create authority. | `READY_FOR_LATER_CONTRACT_DRAFT` | Provenance is needed for auditability and source-gap tracking. | Draft provenance-only language for later contract candidate. | Real source approval, source ownership semantics, source authority. | Trigger if source labels freeze ownership, trust, or authority semantics. | Source label is treated as proof of trusted authority. |
| `source_mode_candidate` relationship to adapter mode | Discussion labels only; `api` and `hybrid` remain unavailable, and `bundle` behavior is not redefined. | `KEEP_DISCOVERY_ONLY` | Mode labels can be misread as approved adapter modes. | Keep as discussion labels until a later source-mode decision. | Approved adapter mode, source adapter implementation, dependency changes. | Trigger if source mode semantics are frozen or implementation is proposed. | `api_candidate`, `hybrid_candidate`, or `bundle_like` becomes approved mode. |
| `missing_fields` impact on mapping confidence | Missing fields remain explicit and must not be silently filled. | `NEEDS_PRODUCT_DECISION` | Unknown fields can create false confidence in source readiness. | Keep missing-field list explicit and ask which fields are required later. | Treating unknowns as provided, readiness claim, hidden defaults. | Trigger if missing-field acceptance becomes source contract semantics. | Unknowns are accepted as complete. |
| `identity_mapping_status` handling | Status labels track unresolved mapping only and do not change resolver behavior. | `READY_FOR_LATER_CONTRACT_DRAFT` | A status field can help review without creating mapping truth. | Draft bounded status semantics for later review if needed. | `READY`, `APPROVED`, `IMPLEMENTABLE`, or `PILOT_READY` meaning. | Trigger if status labels are frozen as contract or runtime semantics. | Status is treated as mapping approval. |

## S4-A Preservation Rules
- `AssetInventorySnapshot` remains the current host identity seed.
- Resolver priority remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- Ambiguity must remain explicit and must not be silently resolved.
- User identifiers are not host identity authority unless a later governed decision says so.
- Context labels are enrichment, not identity authority.
- Source system labels are provenance, not identity authority.
- `source_mode_candidate` labels do not change `api`, `hybrid`, or `bundle` availability.
- Any mapping freeze or authority/semantics change requires a later governed contract and external review.

## Recommended Decision
Preliminary decision: `READY_FOR_LATER_CONTRACT_DRAFT`.

This is the conservative decision only because it is framed as permission to draft a later non-implementing contract candidate for review. It does not freeze mapping.

Meaning:
- later S5-B-4 or S5-B-4A may draft source freshness/provenance or mapping contract candidates for review
- later drafts remain non-implementing unless separately governed
- external review must be evaluated if a later ticket freezes identity/source semantics, changes S4-A authority, changes resolver behavior, changes trust precedence, changes source ownership semantics, or accepts real external evidence

Non-meaning:
- no identity mapping freeze now
- no S4-A authority change
- no resolver behavior change
- no source adapter implementation
- no fixture file creation
- no real source-system access
- no external pilot `READY` claim
- no runtime/API/schema/test/dependency change

If product/governance considers user identifiers, missing-field acceptance, source ownership, or source-mode semantics part of the immediate decision, switch to `NEEDS_PRODUCT_DECISION` before any contract draft proceeds.

## Relationship To External Review
Identifier mapping can affect source identity authority. Any later ticket that includes a new contract freeze or modification to a frozen contract, freezes mapping, changes S4-A authority, changes resolver behavior, changes trust precedence, changes source ownership semantics, or accepts real external evidence must set `requires_external_review=true`.

This draft remains `requires_external_review=false` because it does not freeze mapping, change semantics, or accept real external evidence.

Stream or milestone closeout requires external review under `docs/AI_COLLAB_OPERATING_MODEL.md`.

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This decision is treated as mapping freeze. | S5-B-3 is decision planning only. |
| S4-A authority or resolver priority changes. | S4-A identity authority is inherited unchanged. |
| Ambiguity is silently resolved. | S4-A requires explicit ambiguity. |
| User, context, or source labels are promoted to identity authority. | They are context/provenance questions unless later governed. |
| `source_mode_candidate` labels become approved adapter modes. | S5-B-3 does not change `api`, `hybrid`, or `bundle` availability. |
| Source adapter contract is frozen. | Contract freeze requires a later governed path and external review. |
| Fixture files are created or modified. | This is docs-only and creates no fixtures. |
| Real source-system access is required. | No governed real source access approval exists. |
| Credentials, auth headers, tokens, cookies, API keys, or raw payloads appear. | S5-B discovery must not collect secrets or raw source evidence. |
| Runtime/API/schema/test/dependency changes appear. | This artifact authorizes no implementation changes. |
| Live refresh, sync jobs, CMDB sync, or multi-tenant behavior appears. | These are outside bounded discovery. |
| External pilot execution or real sign-off is implied. | S5-A external pilot package remains `NOT_READY` / `UNKNOWN`. |
| AI_COLLAB `primary_implementor`, `reviewer`, single-writer, or external-review rules are bypassed. | The governed operating model applies to this ticket. |

## Candidate Follow-Up Tickets

| Candidate | Purpose | Allowed scope | Not authorized | `requires_external_review` decision | HOLD trigger |
| --- | --- | --- | --- | --- | --- |
| `S5-B-4 Source Freshness / Provenance Contract` | Draft non-implementing freshness, provenance, and confidence contract candidates. | Docs-only contract candidate preserving S4-A identity authority and implementation deferrals. | Live refresh, sync jobs, dependencies, source adapter changes, real source access. | `true` if it freezes source semantics, trust precedence, or provenance authority; otherwise re-evaluate at ticket start and closeout. | Freshness wording implies runtime refresh or source authority change. |
| `S5-B-4A Source Identifier Mapping Contract Candidate` | Draft a non-implementing candidate mapping contract if S5-B-4 would become too broad. | Docs-only candidate for asset ID, hostname, FQDN, IP, alias, user/context, and status semantics. | Mapping freeze, resolver behavior changes, fixture/test/code changes, real evidence acceptance. | `true` if it freezes mapping, changes S4-A authority, changes resolver behavior, or accepts real external evidence. | Candidate is treated as approved mapping or implementation-ready schema. |
| `S5-B-5 S5-B Discovery Review Pass` | Review S5-B discovery artifacts and decide PASS/HOLD/NEEDS_DECISION for the stream. | Stream review pass and governed closeout only. | Implementation, source adapter changes, real source access, pilot readiness claim. | `true` because stream or milestone closeout triggers external review. | Review pass declares production readiness or pilot readiness without external inputs. |

## Acceptance Criteria
This draft is acceptable when:
- all identifier candidates are classified
- S4-A authority and resolver priority are preserved
- decision vocabulary is bounded and non-authorizing
- external review triggers are explicit
- no identity mapping is frozen
- no implementation, source adapter, runtime/API/schema/test/dependency change is authorized
- external pilot `NOT_READY` / `UNKNOWN` boundary is preserved
- preliminary recommendation is one of `KEEP_DISCOVERY_ONLY`, `NEEDS_PRODUCT_DECISION`, `READY_FOR_LATER_CONTRACT_DRAFT`, or `HOLD`
