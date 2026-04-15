# S5-D Bounded Telemetry Discovery

## Document Control
- Title: S5-D Bounded Telemetry Discovery
- Baseline: `S5-ROUTE-POST-S5B-2026-04-15-001`
- Source of truth: `D:\产品设计\New folder`
- Status: Closed as governed discovery baseline
- Scope: S5-D bounded telemetry discovery only
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code / human-supervised repo writer
- `reviewer`: Claude Code review-only
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false for this draft if discovery-only; re-evaluate and set true later if telemetry normalization semantics freeze, timestamp/freshness semantics freeze, real external evidence/access, S4-A identity authority changes, stream/milestone closeout, or redaction/secret/evidence retention boundary changes appear

## 1. Goal
S5-D opens a bounded telemetry / external-system discovery stream after S5-B was parked as a governed discovery baseline.

This document is discovery-only. It does not authorize telemetry implementation, source or telemetry adapter work, runtime/API/schema/test/dependency changes, fixture file creation, live telemetry access, external pilot execution, real customer/operator sign-off, or any claim that the project is ready for implementation or external pilot execution.

## 2. Non-Goals
- live SIEM/EDR/telemetry access
- connector credentials / auth headers / tokens / API keys
- raw telemetry payloads
- telemetry event retention without separate evidence-retention/redaction approval
- telemetry adapter implementation
- source adapter implementation
- runtime/API/schema/test/dependency changes
- fixture file creation or modification
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
- S5-A external pilot package remains `NOT_READY` / `UNKNOWN`.
- S5-B is `PASS_AND_PARK` and accepted as a discovery baseline only.
- S5-C remains parked.
- S5-C public close-case endpoint remains `KEEP_DEFERRED`.
- S4-A host identity authority remains unchanged: `AssetInventorySnapshot` remains the current host identity seed, and resolver priority remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- `docs/AI_COLLAB_OPERATING_MODEL.md` governs primary implementor, reviewer separation, single-writer discipline, human go/no-go, and external-review triggers.
- `docs/S5_ROUTE_AFTER_S5B_DISCOVERY_CLOSEOUT.md` recommended `OPEN_S5_D_BOUNDED_TELEMETRY_DISCOVERY`, but did not authorize implementation.

## 4. S5-D Stream-Specific Risk Checklist

| Risk category | HOLD trigger |
| --- | --- |
| live SIEM/EDR/telemetry access | HOLD if S5-D requires connecting to live SIEM, EDR, telemetry, source, or customer/operator systems. |
| connector credentials / tokens / API keys | HOLD if credentials, auth headers, tokens, API keys, cookies, or secret material are requested, stored, pasted, or inferred. |
| raw telemetry payloads | HOLD if raw telemetry exports, event bodies, screenshots, logs, or customer/operator payloads are introduced as evidence. |
| telemetry event retention | HOLD if real telemetry event payloads are retained or real telemetry evidence is collected without separate evidence-retention and redaction approval. |
| telemetry normalization freeze | HOLD if this discovery draft freezes canonical telemetry fields, mapping rules, event categories, or normalization behavior. |
| timestamp/freshness semantics freeze | HOLD if candidate timestamp or freshness labels become fixed semantics, runtime expectations, polling rules, or acceptance thresholds. |
| queue/fan-out | HOLD if discovery language implies queues, fan-out, streaming pipelines, background workers, delivery guarantees, or concurrency architecture. |
| performance/SLA commitments | HOLD if latency, throughput, freshness SLA, availability, scale, or operational performance commitments appear. |
| alert routing | HOLD if telemetry discovery becomes alert routing, notification routing, escalation routing, or SOC workflow dispatch. |
| response automation | HOLD if telemetry discovery implies containment, remediation, blocking, ticket action, or other automated response behavior. |
| runtime/API/schema/test/dependency changes | HOLD if any production code, API, schema, test, fixture, dependency, or release-tooling change is required from this draft. |
| S4-A host identity handoff bypass | HOLD if telemetry identifiers bypass `AssetInventorySnapshot`, change resolver priority, silently resolve ambiguity, or create new identity authority. |
| external pilot readiness being misread as improved | HOLD if S5-D discovery is treated as reducing S5-A `UNKNOWN` categories to external pilot readiness without governed external inputs. |

## 5. Discovery Questions

| Area | Discovery question | Current evidence status | Allowed evidence | Blocked evidence or HOLD trigger | Notes |
| --- | --- | --- | --- | --- | --- |
| Telemetry source categories | Which telemetry families should S5-D describe for later review: EDR, SIEM, network, identity/auth, sensor health, or case/evidence handoff? | `UNKNOWN` | Governed docs, synthetic category labels, redacted shape descriptions. | HOLD if live connectors, vendor exports, credentials, or raw payloads are required. | Category labels are discovery handles only. |
| Event minimum field shape | What minimum field areas might a later synthetic telemetry shape discuss? | `UNKNOWN` | Non-authorizing field-area questions and synthetic examples embedded as prose. | HOLD if fields become schema, fixture files, adapter requirements, or normalized event contract. | No schema is frozen here. |
| Host identity handoff into S4-A resolver | How could telemetry provide candidate host identifiers for the existing S4-A resolver? | `NEEDS_DECISION` | Candidate identifier labels and S4-A resolver references. | HOLD if telemetry bypasses `AssetInventorySnapshot`, changes resolver order, or silently resolves ambiguity. | S4-A remains authoritative. |
| Timestamp and freshness questions | Which timestamp concepts require later product/governance decision? | `UNKNOWN` | Candidate timestamp labels and gap notes. | HOLD if timestamp/freshness semantics become fixed, imply polling, or create SLA/performance commitments. | Freshness remains an open question. |
| Telemetry provenance and confidence questions | What provenance or confidence labels might be useful without changing trust precedence? | `NEEDS_DECISION` | Candidate labels and non-authorizing contract sketches. | HOLD if confidence overrides source authority, resolver priority, or prior governed boundaries. | Confidence is annotation only unless later governed. |
| Redaction and secret-handling questions | What must be excluded before any telemetry example can be considered safe? | `NEEDS_DECISION` | Redaction checklists, prohibited categories, synthetic-only examples. | HOLD if credentials, tokens, API keys, auth headers, raw telemetry, or customer/operator evidence appear. | Real evidence needs separate approval. |
| Synthetic/redacted evidence boundary | What shape descriptions can be prepared without creating fixtures or retaining raw data? | `UNKNOWN` | Synthetic examples embedded as documentation and redacted descriptions. | HOLD if fixture files are created or raw telemetry is retained. | Shape language supports later discussion only. |
| Telemetry event retention boundary | What approvals would be required before retaining real telemetry event evidence? | `NEEDS_DECISION` | Governance questions and references to evidence-retention/redaction boundaries. | HOLD if real telemetry evidence is collected or retained without separate evidence-retention and redaction approval. | This draft cannot approve retention. |
| No live SIEM/EDR access | How can S5-D remain useful without connecting to live telemetry systems? | `NEEDS_DECISION` | Governed docs, synthetic categories, redacted shapes, read-only repo inventory. | HOLD if live SIEM/EDR/telemetry/source access becomes required. | No access path is authorized. |
| No queue/fan-out | Which telemetry concerns must remain out of runtime architecture scope? | `NOT_APPLICABLE` | Boundary statements only. | HOLD if queues, fan-out, streaming ingestion, workers, or delivery guarantees appear. | Runtime architecture is out of scope. |
| No alert routing or response automation | How should S5-D avoid becoming operational SOC workflow design? | `NOT_APPLICABLE` | Boundary statements only. | HOLD if alert routing, escalation routing, response automation, containment, or remediation appears. | S5-D discovery is not an actioning system. |
| No performance/SLA commitment | Which scale, latency, throughput, or freshness commitments remain blocked? | `NOT_APPLICABLE` | Boundary statements only. | HOLD if SLA, performance, freshness guarantees, or throughput commitments appear. | Performance topics require later governed scope. |
| Relationship to S5-A external pilot inputs | Can telemetry discovery reduce S5-A `UNKNOWN` categories? | `DEFERRED` | Gap mapping and questions for future input collection. | HOLD if S5-D output is treated as external pilot evidence, sign-off, or package readiness. | S5-A remains `NOT_READY` / `UNKNOWN`. |
| Relationship to S5-B source/input discovery baseline | How should S5-D inherit S5-B evidence boundaries without reopening S5-B? | `NEEDS_DECISION` | S5-B gap matrix, fixture-shape concepts, freshness/provenance candidate language. | HOLD if S5-B PASS is treated as source contract freeze or implementation authorization. | S5-B remains parked. |
| Relationship to S5-C parked case workflow | Does telemetry discovery imply case workflow changes? | `NOT_APPLICABLE` | Boundary references to S5-C parked state and `KEEP_DEFERRED` endpoint decision. | HOLD if S5-C is reopened, runtime case workflow changes appear, or public close-case endpoint work begins. | S5-C stays parked. |

## 6. Candidate Telemetry Source Categories

| Telemetry category | Discovery-only status | No live access / credentials | No raw payload retention | No adapter implementation | Possible synthetic/redacted shape questions |
| --- | --- | --- | --- | --- | --- |
| EDR process/event telemetry | `UNKNOWN` | Live EDR access and connector credentials are prohibited. | Raw EDR events must not be retained. | No EDR adapter change or implementation is authorized. | Which synthetic process, file, parent/child, or detection labels would be safe to discuss? |
| SIEM query or alert-shaped telemetry | `UNKNOWN` | Live SIEM queries, auth headers, and tokens are prohibited. | Raw SIEM alerts, query results, and screenshots must not be retained. | No SIEM adapter change or implementation is authorized. | Which alert-like labels or query-result field areas might be represented synthetically? |
| Network flow or proxy-shaped telemetry | `UNKNOWN` | Live network/proxy access and credentials are prohibited. | Raw flow records or proxy logs must not be retained. | No network telemetry adapter or parser is authorized. | Which reserved IP examples and redacted flow labels are safe for later discussion? |
| Identity/authentication event telemetry | `NEEDS_DECISION` | Live identity-provider access and tokens are prohibited. | Raw authentication logs or user records must not be retained. | No identity connector, RBAC, or tenant model is authorized. | Which generic user/actor labels could be discussed without creating identity authority? |
| Endpoint asset or sensor health telemetry | `UNKNOWN` | Live sensor-health APIs and credentials are prohibited. | Raw sensor records must not be retained. | No sensor-health adapter or runtime readiness behavior is authorized. | Which synthetic sensor state labels could help future telemetry-gap review? |
| Case/evidence handoff telemetry, if applicable | `DEFERRED` | No case-system integration or external evidence system access is authorized. | Real case/evidence event payloads must not be retained. | No case workflow, public endpoint, ticketing, or workflow-engine implementation is authorized. | Which non-sensitive event-reference labels might be useful if a later scoped ticket opens this area? |

## 7. Candidate Event Shape Questions
The items below are candidate field areas for discussion only. They are questions, not a frozen schema, not fixture instructions, and not adapter requirements.

| Field area | Candidate question | Boundary |
| --- | --- | --- |
| `event_time` or `observed_time` | Which event-time labels might be needed to distinguish source-observed time from collection or ingestion time? | Does not freeze timestamp/freshness semantics or imply polling, sync, queueing, SLA, or performance commitments. |
| `telemetry_source_label` | What non-sensitive telemetry family label could help reviewers understand event shape? | Does not create source authority or approve adapter mode. |
| `source_system_label` | What redacted source-system label is useful without identifying a real customer/operator system? | Does not authorize real source evidence or external validation. |
| host identifiers | Which candidate host identifiers could telemetry provide to the existing S4-A resolver? | Does not bypass `AssetInventorySnapshot` or change resolver priority. |
| actor/user identifiers if present | Could generic actor labels be represented without creating RBAC, tenant, or identity authority? | Does not create enterprise identity, authorization, or host identity authority. |
| process/network/auth indicators if present | Which indicator field areas are useful for discussion without raw payloads? | Does not retain raw telemetry, vendor payloads, or customer/operator data. |
| event category | Which high-level event categories are useful for a later gap matrix? | Does not freeze normalization categories or production taxonomy. |
| severity/confidence labels if present | Could severity or confidence be described without changing trust precedence? | Does not override S4-A identity authority or source boundaries. |
| provenance notes | What redacted provenance note would clarify whether an example is synthetic or governed-doc-derived? | Does not accept real external evidence. |
| redaction notes | What redaction note is needed to prove no secret or raw payload is included? | Does not approve retaining real telemetry events. |

This section does not freeze schema, authorize fixture files, authorize raw telemetry retention, or change trust precedence.

## 8. Host Identity Handoff Boundary
- S5-D may only ask how telemetry could provide host identifier candidates.
- S5-D must not change resolver behavior.
- S5-D must not bypass `AssetInventorySnapshot` authority.
- S5-D must not change resolver priority: `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- Ambiguity must remain explicit and must not be silently resolved by telemetry confidence, source labels, event categories, or candidate host identifiers.

## 9. Freshness / Timestamp Boundary
Freshness and timestamp topics are open questions only.

Candidate labels such as event time, observed time, collected time, source freshness, or telemetry age must not freeze semantics, imply live polling, imply live sync, introduce queueing, create SLA/performance commitments, or become acceptance thresholds without a later governed decision.

## 10. Provenance / Confidence Boundary
Provenance and confidence topics are open questions only.

Telemetry provenance does not create source authority. Telemetry confidence does not change trust precedence, resolver priority, S4-A identity authority, or prior governed S5-B source boundaries. Any future confidence semantics that affect decisions, trust, routing, or identity must be handled by a later governed ticket and must re-evaluate `requires_external_review`.

## 11. Allowed Evidence Sources

Allowed evidence:
- governed repo docs
- synthetic examples embedded as shape descriptions only
- redacted shape descriptions
- read-only repo inventory
- gap matrices
- non-authorizing contract sketches

Forbidden evidence:
- real telemetry payloads
- raw SIEM/EDR exports
- credentials, tokens, API keys, auth headers
- customer/operator evidence
- real external access
- retained real telemetry events without separate evidence-retention/redaction approval

## 12. Preliminary Gap Matrix

| Gap area | Current status | Why it matters | Safe next evidence | Not authorized | HOLD trigger |
| --- | --- | --- | --- | --- | --- |
| Telemetry source category inventory | `UNKNOWN` | S5-D needs bounded categories before any later telemetry-gap work. | Synthetic category list and governed-doc references. | Live connector inventory, real system access, credentials. | Category inventory requires real SIEM/EDR/source access. |
| Event field-area shape | `UNKNOWN` | Later discovery needs to know which field areas are worth discussing. | Non-authorizing field-area questions. | Schema freeze, fixture file creation, adapter mapping. | Field-area list becomes a normalized telemetry schema. |
| Host identifier handoff | `NEEDS_DECISION` | Telemetry host identifiers must preserve S4-A authority. | S4-A resolver references and candidate identifier questions. | Resolver priority change, ambiguity suppression, identity authority change. | Telemetry confidence bypasses `AssetInventorySnapshot`. |
| Timestamp/freshness terminology | `UNKNOWN` | Telemetry often has multiple timestamps that can be misread. | Candidate labels framed as questions. | Freshness semantics freeze, polling, sync, SLA. | Timestamp labels become runtime behavior or acceptance criteria. |
| Provenance/confidence terminology | `NEEDS_DECISION` | Provenance is useful, but trust precedence must not drift. | Non-authorizing provenance/confidence questions. | Trust precedence change, source authority, external evidence acceptance. | Confidence becomes authority or routing decision input. |
| Redaction / secret handling | `NEEDS_DECISION` | Telemetry can contain secrets, identities, and sensitive payloads. | Prohibited-category checklist and synthetic-only examples. | Raw payloads, credentials, customer/operator evidence. | Secrets, tokens, raw payloads, or real evidence appear. |
| Real telemetry event retention | `DEFERRED` | Retention requires separate evidence and redaction governance. | Governance question only. | Real telemetry event collection or retention. | Real telemetry is retained without separate approval. |
| Queue/fan-out architecture | `NOT_APPLICABLE` | Runtime architecture is outside bounded discovery. | Boundary statement only. | Queues, fan-out, workers, streaming, performance guarantees. | Runtime architecture appears. |
| Alert routing / response automation | `NOT_APPLICABLE` | Operational routing and response are outside S5-D discovery. | Boundary statement only. | Alert routing, response automation, containment, remediation. | S5-D becomes SOC workflow or automation design. |
| External pilot relationship | `DEFERRED` | S5-D can structure questions but cannot provide external inputs. | Gap relationship notes. | External pilot readiness, execution, or sign-off. | Discovery output is treated as pilot evidence or go/no-go. |

## 13. HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| Live SIEM/EDR/telemetry/source access is required. | S5-D draft is docs-only discovery and has no governed real access approval. |
| Connector credentials, auth headers, tokens, API keys, cookies, or secrets appear. | Secret handling is out of scope and prohibited. |
| Raw telemetry payloads, raw SIEM/EDR exports, screenshots, logs, or customer/operator evidence appear. | S5-D permits only governed docs and synthetic/redacted shape descriptions. |
| Real telemetry event payloads are retained or real telemetry evidence is collected without separate evidence-retention and redaction approval. | Telemetry event retention requires separate governance before real evidence can be accepted. |
| Telemetry normalization semantics are frozen. | This draft asks questions only and creates no normalized telemetry contract. |
| Timestamp/freshness semantics are frozen. | Candidate timestamp/freshness language must not become runtime behavior or acceptance thresholds. |
| Queue, fan-out, streaming, worker, delivery guarantee, or performance/SLA commitment appears. | Runtime telemetry architecture is not authorized. |
| Alert routing appears. | S5-D discovery is not alert dispatch or escalation routing. |
| Response automation appears. | S5-D discovery is not containment, remediation, ticket action, or destructive automation. |
| Runtime/API/schema/test/dependency changes appear. | This draft authorizes no implementation changes. |
| Fixture files are created or modified. | This draft may describe shape questions only. |
| S4-A host identity handoff is bypassed or resolver priority changes. | `AssetInventorySnapshot` and resolver order remain governed by S4-A. |
| Telemetry provenance/confidence changes trust precedence or creates source authority. | Provenance and confidence remain open questions only. |
| External pilot READY claim is made. | S5-A remains `NOT_READY` / `UNKNOWN`. |
| External pilot execution is implied. | External pilot execution remains unauthorized. |
| Real customer/operator sign-off is implied. | No real sign-off exists or is created by this draft. |
| S5-C is reopened. | S5-C remains parked. |
| Public close-case endpoint work appears. | S5-C-4 remains `KEEP_DEFERRED`. |
| AI_COLLAB primary implementor, reviewer separation, single-writer, human go/no-go, or external-review rules are bypassed. | Governed collaboration rules apply to all later S5-D work. |

## 14. Preliminary Recommendation
Recommendation: `PROCEED_TO_S5_D_1_TELEMETRY_GAP_MATRIX`.

Meaning:
- A later docs-only S5-D-1 artifact may classify telemetry discovery gaps using governed docs, synthetic/redacted shape descriptions, and explicit HOLD triggers.
- The later artifact should preserve S5-A, S5-B, S5-C, and S4-A boundaries.

Non-meaning:
- no implementation
- no fixture files
- no runtime/API/schema/test/dependency changes
- no live SIEM/EDR/telemetry access
- no credentials or raw telemetry payloads
- no telemetry normalization freeze
- no timestamp/freshness semantics freeze
- no provenance/confidence trust change
- no stream closeout
- no external pilot readiness claim

## 15. Acceptance Criteria
This draft is acceptable if:
- it is one new doc only
- it preserves S5-A/S5-B/S5-C/S4-A boundaries
- it lists S5-D stream-specific risks early
- it uses only allowed status vocabulary
- it does not authorize implementation
- it does not authorize live telemetry access
- it does not authorize credentials or raw payloads
- it does not freeze telemetry normalization, timestamp/freshness semantics, or provenance/confidence semantics
- it documents a `requires_external_review` decision with AI_COLLAB-complete re-evaluation triggers
- it does not modify runtime/API/schema/test/dependency behavior
- it does not modify HANDOFF or manifest
- it does not claim external pilot readiness
