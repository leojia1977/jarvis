# S5-D-2 Synthetic Telemetry Event Shape

## Document Control
- Title: S5-D-2 Synthetic Telemetry Event Shape
- Baseline: `S5-D-DISCOVERY-2026-04-15-002`
- Source of truth: `D:\产品设计\New folder`
- Status: Closed as governed synthetic telemetry event shape baseline
- Scope: S5-D-2 synthetic telemetry event shape only
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code / human-supervised repo writer
- `reviewer`: Claude Code review-only
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false for this draft if docs-only synthetic shape; re-evaluate and set true later if telemetry normalization semantics freeze, timestamp/freshness semantics freeze, real external evidence/access, S4-A identity authority changes, stream/milestone closeout, or redaction/secret/evidence retention boundary changes appear

## 1. Goal
S5-D-2 turns the governed S5-D-1 telemetry gap matrix into a docs-only synthetic telemetry event shape discussion.

This document is discovery-only and non-authorizing. It describes candidate telemetry field areas as questions and synthetic/redacted prose only. It does not authorize implementation, fixture files, telemetry adapter work, source adapter work, runtime/API/schema/test/dependency changes, live telemetry access, real telemetry event retention, external pilot execution, real customer/operator sign-off, or implementation readiness.

## 2. Non-Goals
- live SIEM/EDR/telemetry access
- connector credentials / auth headers / tokens / API keys
- raw telemetry payloads
- real telemetry event retention without separate evidence-retention/redaction approval
- telemetry adapter implementation
- source adapter implementation
- runtime/API/schema/test/dependency changes
- fixture file creation or modification
- telemetry schema freeze
- telemetry normalization freeze
- timestamp/freshness semantics freeze
- telemetry provenance/confidence changing trust precedence
- queue/fan-out
- performance/SLA commitments
- alert routing
- response automation
- external pilot READY claim
- external pilot execution
- real customer/operator sign-off
- S4-A host identity authority changes
- S5-C reopening
- public close-case endpoint work

## 3. Current Governed State
- S5-D-1 is closed under `S5-D-DISCOVERY-2026-04-15-002`.
- `docs/S5D1_TELEMETRY_GAP_MATRIX.md` recommends `PROCEED_TO_S5_D_2_SYNTHETIC_TELEMETRY_EVENT_SHAPE`.
- S5-A remains `NOT_READY` / `UNKNOWN`.
- S5-B remains `PASS_AND_PARK` discovery baseline only.
- S5-C remains parked.
- S5-C public close-case endpoint remains `KEEP_DEFERRED`.
- S4-A `AssetInventorySnapshot` authority and resolver priority remain unchanged: `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- `docs/AI_COLLAB_OPERATING_MODEL.md` governs primary implementor, reviewer separation, single-writer discipline, human go/no-go, and external-review triggers.

## 4. S5-D-2 Stream-Specific Risk Checklist

| Risk category | HOLD trigger |
| --- | --- |
| live SIEM/EDR/telemetry access | HOLD if this draft requires connecting to live SIEM, EDR, telemetry, source, or customer/operator systems. |
| connector credentials / tokens / API keys | HOLD if credentials, auth headers, tokens, API keys, cookies, or other secret material are requested, stored, pasted, or inferred. |
| raw telemetry payloads | HOLD if raw telemetry exports, event bodies, screenshots, logs, or customer/operator telemetry payloads are introduced. |
| telemetry event retention | HOLD if real telemetry event payloads are retained or real telemetry evidence is collected without separate evidence-retention and redaction approval. |
| telemetry schema freeze | HOLD if candidate field areas become a frozen telemetry schema, fixture specification, API payload, or persistence model. |
| telemetry normalization freeze | HOLD if this draft freezes canonical telemetry fields, normalized event names, category taxonomy, or mapping rules. |
| timestamp/freshness semantics freeze | HOLD if timestamp or freshness labels become fixed semantics, runtime expectations, polling rules, thresholds, or acceptance criteria. |
| queue/fan-out | HOLD if language implies queues, fan-out, streaming pipelines, background workers, delivery guarantees, or concurrency architecture. |
| performance/SLA commitments | HOLD if latency, throughput, freshness SLA, availability, scale, or operational performance commitments appear. |
| alert routing | HOLD if synthetic shape discussion becomes alert dispatch, notification routing, escalation routing, or SOC workflow design. |
| response automation | HOLD if synthetic shape discussion implies containment, remediation, blocking, ticket action, or other automated response behavior. |
| runtime/API/schema/test/dependency changes | HOLD if any production code, API, schema, test, fixture, dependency, or release-tooling change is required from this draft. |
| fixture file creation or modification | HOLD if the synthetic shape is materialized into a fixture file, JSON file, test fixture, or committed sample payload. |
| S4-A host identity handoff bypass | HOLD if telemetry identifiers bypass `AssetInventorySnapshot`, change resolver priority, silently resolve ambiguity, or create new identity authority. |
| external pilot readiness being misread as improved | HOLD if the synthetic shape is treated as reducing S5-A `UNKNOWN` categories to external pilot readiness without governed external inputs. |

## 5. Synthetic Shape Status Vocabulary

Allowed status values:
- `UNKNOWN`
- `NEEDS_DECISION`
- `DEFERRED`
- `NOT_APPLICABLE`

No status means `READY`, `APPROVED`, `IMPLEMENTABLE`, `PILOT_READY`, `PRODUCTION_READY`, or externally validated.

## 6. Candidate Synthetic Event Shape
The candidate field areas below are questions or discussion labels only. They are not schema, not fixture instructions, not adapter requirements, and not runtime/API behavior.

| Field area | Candidate question | Current status | Allowed synthetic description | Not authorized | HOLD trigger | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `event_time` / `observed_time` / `collected_time` / `ingested_time` | Which timestamp labels are needed to discuss event occurrence, source observation, collection, and ingestion without freezing semantics? | `UNKNOWN` | Prose labels such as synthetic observed time, collected time, or ingested time. | Timestamp contract freeze, polling, sync, freshness threshold, SLA, runtime expectation. | Timestamp labels become accepted semantics or implementation criteria. | Keep labels candidate-only until a later governed decision. |
| `telemetry_source_label` | What generic telemetry family label helps classify the synthetic event shape? | `UNKNOWN` | Generic labels such as EDR-like, SIEM-like, network-like, auth-like, sensor-health-like. | Adapter approval, live source access, source authority. | Label is treated as an approved connector or production source mode. | Label is a discovery handle only. |
| `source_system_label` | What redacted source-system label can clarify provenance without naming a real customer/operator system? | `UNKNOWN` | Non-sensitive placeholder labels such as synthetic source system or redacted source family. | Real system names, external evidence acceptance, source authority. | Label reveals real environment details or creates authority. | Provenance only, not trust precedence. |
| `telemetry_category` | Which high-level event category should a synthetic example discuss? | `NEEDS_DECISION` | Category labels for process, SIEM alert shape, network, auth, sensor health, or case/evidence handoff. | Normalization taxonomy freeze, alert routing, response behavior. | Category becomes a frozen telemetry normalization contract. | Category labels remain candidate discussion aids. |
| host identifier candidates | Which candidate host fields might telemetry provide to the existing S4-A resolver? | `NEEDS_DECISION` | Candidate labels for asset ID, hostname, FQDN, IP address, or aliases. | Resolver priority change, `AssetInventorySnapshot` bypass, ambiguity suppression. | Telemetry confidence silently resolves host ambiguity. | Resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`. |
| actor/user identifier candidate | Could a generic actor or user label be represented without creating RBAC, tenancy, or identity authority? | `NEEDS_DECISION` | Generic actor labels and redacted user-like identifiers. | RBAC, tenant model, identity-provider integration, host identity authority. | User label becomes authorization or host identity authority. | Actor labels are contextual only. |
| process indicator candidate | Which process-like field areas are safe to discuss synthetically? | `UNKNOWN` | Generic process name labels, parent/child relationship notes, or command indicator categories without real payloads. | Raw EDR payloads, command-line retention, process parser implementation. | Process details reveal raw telemetry or become adapter contract. | Avoid real command lines, hashes, paths, or customer data. |
| network indicator candidate | Which network-like field areas are safe to discuss synthetically? | `UNKNOWN` | Reserved/example IP range labels, generic port/protocol labels, redacted flow direction notes. | Raw network flow/proxy logs, real IPs, packet content, parser implementation. | Real network telemetry or retained payloads appear. | Use synthetic or reserved examples only. |
| authentication indicator candidate | Which auth-like field areas are useful without creating identity-system scope? | `NEEDS_DECISION` | Generic login outcome, factor label, or actor/context note as prose. | Identity-provider access, auth logs, RBAC, tenant ownership model. | Auth shape becomes authorization or identity authority semantics. | Keep auth indicators contextual and non-authoritative. |
| sensor/asset health candidate | Which sensor-health or asset-health labels might support later telemetry discussion? | `UNKNOWN` | Generic labels such as sensor present, stale, offline, or unknown as candidate prose. | Runtime readiness changes, health API integration, live sensor checks. | Health labels become monitoring behavior or source authority. | Does not alter S4-A identity seed. |
| severity/confidence label candidate | Could severity or confidence be discussed without changing trust precedence? | `NEEDS_DECISION` | Candidate severity/confidence labels with explicit non-authority notes. | Trust precedence change, automated routing, response trigger, identity override. | Confidence label changes decision authority or resolver behavior. | Confidence is annotation only. |
| provenance note | What non-sensitive provenance note would clarify whether the shape is synthetic or governed-doc-derived? | `NEEDS_DECISION` | Notes such as synthetic-only, derived from governed gap area, or redacted shape description. | Real external evidence acceptance, source authority, retention approval. | Provenance note accepts or retains real evidence. | Provenance cannot create authority. |
| redaction note | What note proves no secret, raw payload, or customer/operator evidence is included? | `NEEDS_DECISION` | Redaction checklist statements and prohibited-category references. | Real payload redaction approval, secret handling changes, raw evidence retention. | Redaction note is treated as approval for real telemetry evidence. | Separate approval required for real evidence. |
| retention note | What boundary should state that no real telemetry event is retained? | `NEEDS_DECISION` | Statement that examples are prose/table-only and synthetic. | Real telemetry event collection, retention, replay, storage, evidence packaging. | Any retained real telemetry event appears. | Retention remains prohibited without separate approval. |
| `synthetic_only` marker | How should the document mark the shape as non-real and non-authorizing? | `NEEDS_DECISION` | Candidate marker language such as synthetic-only discussion label. | Fixture file creation, implementation readiness, external validation. | Marker is treated as schema field or production contract. | Marker is a documentation safety signal only. |

## 7. Category-Specific Shape Notes

| Category | Synthetic/redacted shape discussion only | Boundary |
| --- | --- | --- |
| EDR process/event shaped telemetry | May discuss process/event-like field areas such as process label, parent relation, detection context, or endpoint label using synthetic prose only. | Does not authorize live EDR access, raw EDR payloads, fixture files, parser changes, or EDR adapter implementation. |
| SIEM query or alert-shaped telemetry | May discuss alert-shaped field areas such as alert label, query-result context, or rule-like category using redacted prose only. | Does not authorize live SIEM queries, auth headers, tokens, raw alerts, alert routing, notification routing, or SIEM adapter work. |
| Network flow or proxy-shaped telemetry | May discuss generic source/destination direction, reserved/example IP labels, protocol category, or proxy-like context as synthetic descriptions. | Does not authorize raw network flow retention, proxy exports, packet data, real IP/customer payloads, or network telemetry adapter work. |
| Identity/authentication event telemetry | May discuss generic actor, login outcome, auth context, or identity-source label as candidate annotations only. | Does not authorize identity-provider access, RBAC, tenant ownership, auth log retention, or host identity authority changes. |
| Endpoint asset or sensor health telemetry | May discuss sensor status, endpoint health, or asset-health labels as synthetic status notes. | Does not authorize sensor-health APIs, runtime readiness changes, monitoring implementation, or live endpoint checks. |
| Case/evidence handoff telemetry, if applicable | May discuss whether a future event-reference label is useful if product/governance opens this area later. | Does not authorize S5-C reopening, public close-case endpoint work, evidence retention, ticketing, workflow engine, alert routing, or response automation. |

All category notes are synthetic/redacted prose only. They do not authorize live access, fixture files, adapters, raw payloads, or retention.

## 8. Host Identity Handoff Boundary
- S5-D-2 may only describe candidate host identifier fields for later discussion.
- S5-D-2 must not change S4-A resolver behavior.
- S5-D-2 must not bypass `AssetInventorySnapshot`.
- S5-D-2 must not change resolver priority: `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- Telemetry confidence must not silently resolve ambiguity.
- Candidate host identifier fields cannot override governed S4-A host identity authority.

## 9. Timestamp / Freshness Boundary
All timestamp labels are candidate questions only.

S5-D-2 does not freeze timestamp semantics, freshness thresholds, polling rules, sync behavior, SLA, performance commitments, runtime expectations, or acceptance criteria. Labels such as event time, observed time, collected time, and ingested time remain discussion handles until a later governed decision explicitly changes scope.

## 10. Provenance / Confidence Boundary
Provenance and confidence are candidate annotations only.

They must not change trust precedence, source authority, host identity authority, alert routing, or response behavior. Telemetry confidence cannot override S4-A resolver order, S5-B source/input boundaries, or human go/no-go authority. Any later confidence semantics that affect identity, routing, evidence acceptance, or response behavior must use a separate governed ticket and re-evaluate `requires_external_review`.

## 11. Redaction / Secret / Retention Boundary
Explicitly forbidden:
- credentials
- tokens
- API keys
- auth headers
- raw telemetry payloads
- customer/operator evidence
- retained real telemetry events
- screenshots/logs from real systems

Synthetic examples may be prose/table descriptions only. Do not create fixture files.

Any later ticket that changes redaction, secret, or evidence retention boundaries must set `requires_external_review=true` under `docs/AI_COLLAB_OPERATING_MODEL.md`.

## 12. HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| Live SIEM/EDR/telemetry/source access is required. | S5-D-2 is docs-only discovery and has no governed real access approval. |
| Connector credentials, auth headers, tokens, API keys, cookies, or secrets appear. | Secret handling and credential collection are prohibited. |
| Raw telemetry payloads, raw SIEM/EDR exports, screenshots, logs, or customer/operator evidence appear. | S5-D-2 permits only governed docs and synthetic/redacted prose descriptions. |
| Real telemetry event payloads are retained or real telemetry evidence is collected without separate evidence-retention and redaction approval. | Telemetry event retention requires separate governance before real evidence can be accepted. |
| Telemetry schema is frozen. | Candidate field areas are questions only, not schema. |
| Telemetry normalization semantics are frozen. | This draft creates no normalized telemetry contract or taxonomy. |
| Timestamp/freshness semantics are frozen. | Candidate timing language must not become runtime behavior, freshness threshold, or acceptance criteria. |
| Telemetry provenance/confidence changes trust precedence or creates source authority. | Provenance and confidence remain annotations only. |
| Queue, fan-out, streaming, worker, delivery guarantee, or performance/SLA commitment appears. | Runtime telemetry architecture and operational commitments are out of scope. |
| Alert routing appears. | S5-D-2 is not alert dispatch, notification routing, escalation routing, or SOC workflow design. |
| Response automation appears. | S5-D-2 is not containment, remediation, blocking, ticket action, or destructive automation. |
| Runtime/API/schema/test/dependency changes appear. | This draft authorizes no implementation changes. |
| Fixture files are created or modified. | The synthetic event shape is prose/table-only. |
| S4-A host identity handoff is bypassed or resolver priority changes. | `AssetInventorySnapshot` and resolver order remain governed by S4-A. |
| External pilot READY claim is made. | S5-A remains `NOT_READY` / `UNKNOWN`. |
| External pilot execution is implied. | External pilot execution remains unauthorized. |
| Real customer/operator sign-off is implied. | No real sign-off exists or is created by this draft. |
| S5-C is reopened. | S5-C remains parked. |
| Public close-case endpoint work appears. | S5-C-4 remains `KEEP_DEFERRED`. |
| AI_COLLAB primary implementor, reviewer separation, single-writer, human go/no-go, or external-review rules are bypassed. | Governed collaboration rules apply to all later S5-D work. |

## 13. Preliminary Recommendation
Recommendation: `PROCEED_TO_S5_D_3_TELEMETRY_PROVENANCE_AND_FRESHNESS_BOUNDARY`.

Meaning:
- A later docs-only S5-D-3 artifact may clarify telemetry provenance, confidence, timestamp, and freshness boundaries using governed docs and synthetic/redacted descriptions only.
- The later artifact should keep provenance and freshness terms as candidate semantics unless a separate governed decision changes scope.
- The later artifact must preserve S5-A, S5-B, S5-C, and S4-A boundaries.

Non-meaning:
- no implementation
- no fixture files
- no telemetry adapter work
- no source adapter work
- no runtime/API/schema/test/dependency changes
- no telemetry schema freeze
- no telemetry normalization freeze
- no timestamp/freshness semantics freeze
- no provenance/confidence trust change
- no live SIEM/EDR/telemetry access
- no credentials or raw telemetry payloads
- no real telemetry event retention
- no stream closeout
- no external pilot readiness claim

## 14. Acceptance Criteria
This draft is acceptable if:
- it is one new doc only
- it preserves S5-A/S5-B/S5-C/S4-A boundaries
- it lists S5-D-2 stream-specific risks early
- it uses only allowed status vocabulary
- it does not authorize implementation
- it does not authorize live telemetry access
- it does not authorize credentials or raw payloads
- it does not authorize real telemetry event retention
- it does not create or modify fixture files
- it does not freeze schema, normalization, timestamp/freshness semantics, or provenance/confidence semantics
- it documents a `requires_external_review` decision with AI_COLLAB-complete re-evaluation triggers
- it does not modify runtime/API/schema/test/dependency behavior
- it does not modify HANDOFF, manifest, AI_COLLAB files, or contracts
- it does not claim external pilot readiness
- it identifies the recommended next docs-only route or records the route as an open product/governance question
