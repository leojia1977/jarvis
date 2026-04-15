# S5-B Bounded Source/Input Discovery

## Document Control
- Title: S5-B Bounded Source/Input Discovery
- Baseline: `S5-NEXT-ROUTE-2026-04-15-001`
- Source of truth: `D:\产品设计\New folder`
- Status: Draft for review
- Scope: bounded source/input discovery only
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code / human-supervised repo writer
- `reviewer`: Claude Code review-only
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false for draft; re-evaluate at closeout or if contract freeze, source semantics, or identity authority changes appear

## Goal
Prepare bounded `S5-B` discovery by identifying missing source inputs, safe in-repo evidence, and future decision points for source/input work.

This document does not authorize implementation, runtime/API/schema/test/dependency changes, real source-system access, live refresh, external authentication, CMDB sync, multi-tenant ownership, external pilot execution, real customer/operator sign-off, or S4-A identity authority changes. It only defines a safe discovery frame for later docs, fixture, or contract work.

## Non-Goals
- production source integration
- runtime/API/schema/test changes
- dependency changes
- real source-system or SIEM/EDR access
- external authentication or credential handling
- live refresh or sync jobs
- CMDB sync
- multi-tenant ownership model
- bypassing S4-A identity authority
- external pilot execution
- real customer/operator sign-off
- ticketing integration
- workflow-engine behavior
- destructive response automation
- modifying `docs/AI_COLLAB_OPERATING_MODEL.md`
- changing S5-C semantics

## Current Baseline
- Active baseline is `S5-NEXT-ROUTE-2026-04-15-001`.
- `docs/S5_NEXT_ROUTE_AFTER_AI_COLLAB_AMENDMENT.md` recommended `OPEN_BOUNDED_S5_B_DISCOVERY_TICKET`.
- `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md` records the external pilot input package as `NOT_READY` because all seven categories remain `UNKNOWN`.
- S5-C remains parked, and `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` keeps the public close-case HTTP endpoint at `KEEP_DEFERRED`.
- `docs/AI_COLLAB_OPERATING_MODEL.md` governed fields apply to this ticket, including `primary_implementor`, `reviewer`, single-writer lock, and trigger-based external review.
- S5-B remains discovery-only unless governed source inputs become available and a later product/governance decision expands scope.
- S4-A remains the source and identity authority baseline:
  - `docs/S4A1_STATIC_DATA_SOURCE_CONTRACT.md` freezes static source contracts and source modes.
  - `docs/S4A2_STATIC_DATA_ADAPTER_BASELINE.md` establishes the adapter envelope and keeps `api` / `hybrid` unavailable in Sprint 4.
  - `docs/S4A3_HOST_IDENTITY_RESOLVER.md` freezes canonical host identity resolution.
  - `docs/S4A5_SOURCE_INTEGRATION_REVIEW_PASS.md` accepts `AssetInventorySnapshot` as the Sprint 4 host identity seed.

## Discovery Questions

| Question | Why it matters | Current evidence | Safe in-repo discovery action | HOLD trigger |
| --- | --- | --- | --- | --- |
| What source systems are expected to provide asset, user, or context inputs? | Source targets drive future contract boundaries and missing-input assessment. | Sprint 5 docs mention source-system candidates but no governed external source is named. | Create a source/input gap matrix with candidate source classes and `UNKNOWN` status. | A real source system is treated as approved without governed input. |
| Which source identifiers must map to S4-A identity authority? | Host selection and case context must not bypass the canonical resolver. | S4-A freezes `AssetInventorySnapshot` and resolver order: `asset_id -> hostname -> fqdn -> ip_address -> aliases`. | List identifier types as mapping questions and mark unresolved mappings as future decisions. | Source mapping changes identity authority, normalization semantics, or trust precedence. |
| What minimum fields are needed for fixture-only source records? | Synthetic fixtures need enough shape to support discovery without becoming production contracts. | S4-A defines asset, baseline, intel seed, and topology snapshot shapes. | Sketch minimal synthetic/redacted field shapes and tag them non-authorizing. | Fixture shape is treated as frozen external source contract. |
| Which fields are sensitive and must be redacted or excluded? | Source/input discovery can accidentally capture secrets or real operator payloads. | S5-A redaction and external pilot intake prohibit secret values and raw sensitive payloads. | Add field-level redaction notes and prohibited-evidence examples. | Secret values, credentials, tokens, auth headers, cookies, API keys, or raw source payloads appear. |
| What freshness or refresh expectations are product requirements versus future implementation choices? | Freshness can drift into live refresh, sync jobs, or CMDB behavior. | S4-A freezes `startup`, `ttl`, and `manual`; Sprint 5 defers live refresh design. | Record freshness as discovery questions and separate `refresh_policy` labels from implementation. | Live refresh, sync job, stale-serve-through, or CMDB sync is implied. |
| What source/input examples are missing from external pilot inputs? | S5-B can reduce ambiguity but cannot invent external inputs. | External pilot assessment keeps all required categories `UNKNOWN`; no source samples are governed. | Produce a missing-input list with allowed synthetic or redacted placeholders. | Discovery output is treated as real customer/operator evidence or pilot readiness. |
| What would make S5-B ready for a later contract or implementation decision? | A future decision needs clear readiness criteria. | Sprint 5 backlog permits discovery/contract depth only until external inputs exist. | Define readiness signals: explicit source candidates, sample shapes, redaction approval, identity mapping decision, and product priority. | Runtime/API/schema/test/dependency changes start from this discovery draft. |

## Safe In-Repo Evidence
Allowed evidence for this S5-B discovery:
- existing governed docs
- synthetic fixtures
- redacted example shapes
- contract sketches marked non-authorizing
- read-only inventory of current adapters, tests, fixtures, and docs
- source/input gap matrix
- unresolved decision matrix

Prohibited evidence:
- real credentials
- real customer/operator payloads
- raw SIEM/EDR/source payloads
- auth headers
- cookies
- bearer tokens
- API keys
- live external calls
- screenshots or files outside `D:\产品设计\New folder` treated as source truth

## Source/Input Boundary Matrix

| Area | Current governed evidence | Safe discovery output | Not authorized | Future decision needed | HOLD trigger |
| --- | --- | --- | --- | --- | --- |
| Asset identity inputs | S4-A `AssetInventorySnapshot`; S4-A host identity resolver; S4-A review pass. | Gap list for asset identifiers, aliases, source refs, ownership fields, and confidence inputs. | Replacing `AssetInventorySnapshot` as authority; changing resolver priority. | Whether external asset source examples should become a governed contract input. | Asset source bypasses canonical resolver or silently resolves ambiguity. |
| User identity inputs | No governed user identity source contract in current S4-A/S5-B evidence. | Mark as `UNKNOWN`; list potential non-sensitive field names only if synthetic. | Enterprise user directory integration, RBAC, tenancy, authz model. | Product decision on whether user identity belongs in S5-B source scope. | User source work creates access-control or tenant semantics. |
| Host/context enrichment | S4-A asset fields; topology snapshot remains loosely typed; S4-B telemetry aligns to host identity. | Redacted/synthetic context-shape sketch with provenance notes. | CMDB sync, topology API, trust precedence changes. | Which enrichment fields are evidence, context, or authority. | Enrichment becomes identity authority or production CMDB behavior. |
| Source freshness / refresh metadata | S4-A `StaticSourceMetadata`; `startup`, `ttl`, `manual`; S4-A cache tests. | Freshness question list and non-authorizing metadata examples. | Live refresh, background sync, stale-serve-through, performance commitments. | Product decision on refresh expectations before implementation. | Refresh metadata implies live integration or sync job. |
| Source confidence / provenance | S4-A `HostIdentityRecord.source_refs[]` and `confidence`; S4-A ambiguity semantics. | Provenance field inventory and unresolved trust-precedence questions. | New trust model, silent fallback, identity federation. | Whether confidence/provenance affects downstream decisions. | Trust precedence changes without external review. |
| Missing or unknown source fields | S4-A unsupported source fields list; Sprint 5 source-input gaps. | Missing-field matrix with `UNKNOWN`, `NEEDS_DECISION`, or `DEFERRED`. | Treating unknowns as provided or production-ready. | Product/governance acceptance of required external inputs. | Discovery declares package ready while fields remain unknown. |
| Redaction / secret handling | S5-A redaction boundary; external pilot intake and assessment; release process evidence discipline. | Prohibited-field list and redacted example shapes. | Secret collection, raw payload retention, unredacted customer/operator records. | Redaction approval if real source examples are later supplied. | Credentials, tokens, auth headers, cookies, API keys, or raw payloads are recorded. |
| Future source adapter contract | S4-A adapter envelope; `api` and `hybrid` are governed unavailable; `bundle` currently reuses local files. | Non-authorizing contract sketch and decision questions for `api`, `hybrid`, and distinct `bundle`. | Production adapter implementation, external auth, dependency changes. | Whether to freeze or implement a later source adapter contract. | Source contract is frozen or implementation starts without external review and scoped ticket. |

## Relationship To S4-A
S5-B must inherit S4-A identity authority. It may not bypass, redefine, or replace the accepted Sprint 4 asset-inventory identity seed or canonical host resolver.

S4-A governed rules that S5-B must preserve:
- `AssetInventorySnapshot` is the authoritative host-identity seed for the current baseline.
- Host resolution flows through the canonical resolver instead of source-specific lookup shortcuts.
- Resolver priority remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- Ambiguity must be explicit and must not silently choose a host.
- `api` and `hybrid` static-data source modes remain unavailable outcomes until a later governed decision changes them.
- `bundle` currently reuses local-file behavior and is not a distinct production backend.

Any source identifier mapping must remain a discovery question unless a later governed contract freezes it. HOLD if source mapping changes identity authority, normalization semantics, resolver priority, ambiguity handling, trust precedence, or source ownership semantics.

## Relationship To External Pilot Inputs
S5-B can reduce `UNKNOWN` source/input ambiguity by preparing a source/input gap matrix, synthetic fixture shapes, and non-authorizing contract questions. It cannot declare the external pilot package `READY` without governed external pilot inputs.

This discovery may support later product/governance decisions by listing missing source candidates, sample payload needs, redaction requirements, identity mapping questions, and refresh expectations. It does not create real operator/customer sign-off, external pilot execution authorization, source-system access approval, or retention approval for real source data.

HOLD if discovery output is treated as real customer/operator sign-off, real pilot evidence, external pilot execution authorization, or proof that the external pilot package is `READY`.

## Candidate Follow-Up Tickets

| Candidate | Purpose | Allowed scope | Not authorized | `requires_external_review` decision | HOLD trigger |
| --- | --- | --- | --- | --- | --- |
| `S5-B-1 Source Input Gap Matrix` | Record missing source systems, sample shapes, identity mapping questions, and decision owners. | Docs-only gap matrix using governed docs and synthetic/redacted placeholders. | Runtime, tests, real source access, contract freeze. | `false` for draft; re-evaluate at closeout or if source semantics are accepted. | Matrix treats `UNKNOWN` inputs as provided. |
| `S5-B-2 Synthetic Source Fixture Shape` | Define safe fixture-only source shapes for future exploration. | Synthetic fixture sketch or docs-only fixture shape; no test edits unless later scoped. | Real payloads, raw source exports, production readiness claims. | `false` if synthetic and non-authorizing; `true` if contract freeze is proposed. | Fixture is treated as external source contract or real evidence. |
| `S5-B-3 Source Identifier Mapping Decision` | Decide how candidate identifiers map to S4-A authority before any contract freeze. | Docs-only mapping decision or HOLD record. | Resolver priority changes, identity bypass, runtime implementation. | `true` if it modifies identity authority or freezes mapping semantics. | Mapping redefines S4-A identity authority without external review. |
| `S5-B-4 Source Freshness / Provenance Contract` | Clarify freshness, provenance, confidence, and refresh expectations. | Contract/planning doc with explicit implementation deferrals. | Live refresh, sync jobs, performance commitments, dependencies. | `true` if it freezes source semantics or refresh contract. | Freshness wording implies live refresh or CMDB sync. |
| `S5-B-5 S5-B Discovery Review Pass` | Review S5-B discovery artifacts and decide PASS/HOLD/NEEDS_DECISION. | Stream review pass and governed closeout only. | Implementation, source adapter changes, real access. | `true` because stream closeout triggers external review. | Review pass declares production readiness without external inputs. |

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This document is treated as implementation authorization. | It is discovery only. |
| Real source-system access is required. | No governed source access approval exists. |
| Credentials, auth headers, tokens, cookies, or API keys are introduced. | S5-B discovery must not collect secrets or auth material. |
| Raw customer/operator/source payloads are included. | Only synthetic or redacted shapes are allowed. |
| Live refresh, sync jobs, CMDB sync, or multi-tenant behavior appears. | These are Sprint 5 non-goals without separate product decision. |
| S4-A identity authority is bypassed or redefined. | S5-B must inherit the accepted S4-A resolver and authority model. |
| Source contract is frozen without external review. | Contract freeze and source semantics trigger `requires_external_review=true`. |
| Runtime/API/schema/test/dependency changes appear. | This ticket allows docs-only discovery. |
| External pilot or real sign-off is implied. | S5-A package remains `NOT_READY`; real sign-off is unauthorized. |
| AI_COLLAB `primary_implementor`, `reviewer`, or single-writer rules are bypassed. | The amended collaboration model governs execution discipline. |

## Preliminary Recommendation
Recommendation: `PROCEED_TO_S5_B_1_SOURCE_INPUT_GAP_MATRIX`.

Meaning:
- Create a later docs-only ticket to produce a source/input gap matrix from governed docs and synthetic or redacted evidence only.
- Keep all missing external source inputs marked `UNKNOWN`, `NEEDS_DECISION`, or `DEFERRED` unless explicitly provided through governed product/governance evidence.
- Use the S4-A identity authority as the non-negotiable boundary for any identifier mapping questions.

Non-meaning:
- does not authorize implementation
- does not authorize source adapter changes
- does not authorize real external access
- does not freeze identity mapping
- does not make external pilot package `READY`
- does not authorize runtime/API/schema/test/dependency changes

Allowed preliminary recommendation values:
- `PROCEED_TO_S5_B_1_SOURCE_INPUT_GAP_MATRIX`
- `NEEDS_PRODUCT_DECISION`
- `KEEP_DISCOVERY_ONLY`
- `HOLD`

## Acceptance Criteria
This draft is acceptable when:
- all discovery questions are listed
- safe evidence boundaries are explicit
- S4-A relationship is preserved
- external pilot `UNKNOWN` / `NOT_READY` boundary is preserved
- candidate follow-up tickets are bounded
- HOLD conditions cover real access, credentials, source semantics, identity authority, and runtime changes
- preliminary recommendation is one of `PROCEED_TO_S5_B_1_SOURCE_INPUT_GAP_MATRIX`, `NEEDS_PRODUCT_DECISION`, `KEEP_DISCOVERY_ONLY`, or `HOLD`
- no implementation, source adapter change, runtime/API/schema/test/dependency change, external pilot execution, real source access, or real customer/operator sign-off is authorized
