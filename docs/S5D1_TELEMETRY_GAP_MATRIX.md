# S5-D-1 Telemetry Gap Matrix

## Document Control
- Title: S5-D-1 Telemetry Gap Matrix
- Baseline: `S5-D-DISCOVERY-2026-04-15-001`
- Source of truth: `D:\产品设计\New folder`
- Status: Closed as governed telemetry gap matrix baseline
- Scope: S5-D-1 telemetry gap matrix only
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code / human-supervised repo writer
- `reviewer`: Claude Code review-only
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false for this draft if docs-only gap matrix; re-evaluate and set true later if telemetry normalization semantics freeze, timestamp/freshness semantics freeze, real external evidence/access, S4-A identity authority changes, stream/milestone closeout, or redaction/secret/evidence retention boundary changes appear

## 1. Goal
S5-D-1 converts the governed S5-D bounded telemetry discovery baseline into a docs-only telemetry gap matrix.

This document is discovery-only. It classifies telemetry uncertainty for later product/governance review and does not authorize implementation, telemetry adapter work, source adapter work, fixture file creation, runtime/API/schema/test/dependency changes, live telemetry access, real evidence retention, external pilot execution, real customer/operator sign-off, or implementation readiness.

## 2. Non-Goals
- live SIEM/EDR/telemetry access
- connector credentials / auth headers / tokens / API keys
- raw telemetry payloads
- real telemetry event retention without separate evidence-retention/redaction approval
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
- S5-D bounded telemetry discovery is closed as governed discovery baseline under `S5-D-DISCOVERY-2026-04-15-001`.
- `docs/S5D_BOUNDED_TELEMETRY_DISCOVERY.md` recommends `PROCEED_TO_S5_D_1_TELEMETRY_GAP_MATRIX`.
- S5-A external pilot package remains `NOT_READY` / `UNKNOWN`.
- S5-B remains `PASS_AND_PARK` discovery baseline only.
- S5-C remains parked.
- S5-C public close-case endpoint remains `KEEP_DEFERRED`.
- S4-A host identity authority remains unchanged: `AssetInventorySnapshot` remains the current host identity seed, and resolver priority remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- `docs/AI_COLLAB_OPERATING_MODEL.md` governs primary implementor, reviewer separation, single-writer discipline, human go/no-go, and external-review triggers.

## 4. S5-D-1 Stream-Specific Risk Checklist

| Risk category | HOLD trigger |
| --- | --- |
| live SIEM/EDR/telemetry access | HOLD if the matrix requires connecting to live SIEM, EDR, telemetry, source, or customer/operator systems. |
| connector credentials / tokens / API keys | HOLD if credentials, auth headers, tokens, API keys, cookies, or other secret material are requested, stored, pasted, or inferred. |
| raw telemetry payloads | HOLD if raw telemetry exports, event bodies, screenshots, logs, or customer/operator telemetry payloads are introduced. |
| telemetry event retention | HOLD if real telemetry event payloads are retained or real telemetry evidence is collected without separate evidence-retention and redaction approval. |
| telemetry normalization freeze | HOLD if matrix language freezes canonical telemetry fields, normalized event names, category taxonomy, or mapping rules. |
| timestamp/freshness semantics freeze | HOLD if candidate timestamp or freshness labels become fixed semantics, runtime expectations, polling rules, thresholds, or acceptance criteria. |
| queue/fan-out | HOLD if discovery language implies queues, fan-out, streaming pipelines, background workers, delivery guarantees, or concurrency architecture. |
| performance/SLA commitments | HOLD if latency, throughput, freshness SLA, availability, scale, or operational performance commitments appear. |
| alert routing | HOLD if the matrix becomes alert dispatch, notification routing, escalation routing, or SOC workflow design. |
| response automation | HOLD if the matrix implies containment, remediation, blocking, ticket action, or other automated response behavior. |
| runtime/API/schema/test/dependency changes | HOLD if any production code, API, schema, test, fixture, dependency, or release-tooling change is required from this draft. |
| S4-A host identity handoff bypass | HOLD if telemetry identifiers bypass `AssetInventorySnapshot`, change resolver priority, silently resolve ambiguity, or create new identity authority. |
| external pilot readiness being misread as improved | HOLD if the matrix is treated as reducing S5-A `UNKNOWN` categories to external pilot readiness without governed external inputs. |

## 5. Gap Matrix Status Vocabulary

| Status | Meaning | Non-meaning |
| --- | --- | --- |
| `UNKNOWN` | Governed evidence is absent or insufficient for this telemetry gap. | Does not mean the answer can be inferred from chat, prior memory, or ungoverned external context. |
| `NEEDS_DECISION` | Enough evidence exists to frame a product/governance decision, but no decision is made here. | Does not approve the decision, freeze semantics, or authorize implementation. |
| `DEFERRED` | Intentionally postponed until a later scoped ticket, external input, or stream decision. | Does not remove the need if later scope depends on it. |
| `NOT_APPLICABLE` | Not relevant to S5-D-1 telemetry gap classification at this stage. | Does not authorize another stream to proceed without its own governed basis. |

No status means `READY`, `APPROVED`, `IMPLEMENTABLE`, `PILOT_READY`, `PRODUCTION_READY`, or externally validated.

Terms such as `NOT_READY` may appear only when restating inherited S5-A baseline facts, not as a matrix status.

## 6. Telemetry Gap Matrix

| Gap area | Current status | Why it matters | Current governed evidence | Allowed next evidence | Not authorized | HOLD trigger | Candidate follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Telemetry source category inventory | `UNKNOWN` | S5-D needs bounded telemetry categories before later event-shape discussion. | S5-D baseline names EDR, SIEM, network, identity/auth, sensor health, and case/evidence handoff as candidate categories. | Docs-only category list with synthetic/redacted descriptions. | Live SIEM/EDR/source access, credential collection, real inventory pull. | Category inventory requires live access or raw payloads. | S5-D-2 synthetic event shape can carry category handles forward. |
| EDR process/event telemetry shape | `UNKNOWN` | EDR-like process/event telemetry may influence later event-field discussions but must not reopen S4-B implementation. | S4-B docs exist; S5-D baseline permits only discovery questions. | Synthetic process/event field-area questions. | EDR adapter changes, raw EDR exports, vendor payload retention, fixture files. | EDR shape becomes adapter contract or real payload evidence. | S5-D-2 may describe synthetic EDR-like shape questions. |
| SIEM query or alert-shaped telemetry shape | `UNKNOWN` | SIEM-like alert/query outputs can be confused with alert routing or production query behavior. | S5-D baseline blocks live SIEM access and alert routing. | Redacted alert-shaped field-area questions. | Live SIEM queries, auth headers, tokens, raw alerts, alert routing. | SIEM shape implies query execution or routing behavior. | S5-D-2 may define synthetic alert-shaped examples as prose only. |
| Network flow or proxy-shaped telemetry shape | `UNKNOWN` | Network/proxy indicators can contain sensitive payloads and real infrastructure data. | S5-D baseline permits no raw payloads or live telemetry access. | Reserved/example IP ranges and generic network labels as descriptions only. | Raw flow logs, proxy exports, real IP/customer payloads, parser implementation. | Real network telemetry or retained payloads appear. | S5-D-2 may ask which synthetic network indicators are safe. |
| Identity/authentication event telemetry shape | `NEEDS_DECISION` | Auth events can drift into RBAC, tenancy, or user identity authority. | S5-D baseline allows actor/user identifiers only as open questions; S5-C rejects RBAC. | Generic actor/user labels and product questions. | Identity-provider access, RBAC, tenant model, host identity authority change. | User/auth labels become identity authority or authorization semantics. | S5-D-2 may include generic actor fields with strict non-authorizing boundary. |
| Endpoint asset or sensor health telemetry shape | `UNKNOWN` | Sensor-health or asset-health data may be useful but can imply readiness, monitoring, or source authority. | S5-D baseline blocks telemetry adapter work and runtime readiness behavior. | Synthetic health labels and provenance questions. | Sensor-health APIs, live status checks, runtime readiness changes. | Health telemetry becomes operational monitoring or source authority. | S5-D-2 may include synthetic sensor-state labels. |
| Case/evidence handoff telemetry, if applicable | `DEFERRED` | Case/evidence events can reopen S5-C or imply retention approval. | S5-C remains parked; public close-case endpoint remains `KEEP_DEFERRED`. | Boundary questions only. | Case workflow changes, ticketing/workflow-engine behavior, evidence retention, endpoint work. | Case/evidence telemetry reopens S5-C or stores real evidence. | Later product decision before any case/evidence telemetry shape. |
| Event minimum field-area shape | `UNKNOWN` | Future synthetic examples need field areas, but field areas can look like schema. | S5-D baseline lists candidate field areas as questions only. | Docs-only field-area question list. | Schema freeze, normalized field freeze, API/test changes, fixture files. | Field-area list is treated as telemetry schema. | S5-D-2 synthetic event shape. |
| Host identity handoff into S4-A resolver | `NEEDS_DECISION` | Telemetry host identifiers must preserve S4-A authority and ambiguity behavior. | S4-A resolver priority remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`. | Candidate host identifier questions mapped to existing resolver order. | Resolver behavior changes, `AssetInventorySnapshot` bypass, ambiguity suppression. | Telemetry confidence silently resolves host ambiguity. | S5-D-2 may include host candidate fields as questions only. |
| Timestamp/freshness terminology | `UNKNOWN` | Telemetry often has event, observed, collected, and ingested timestamps that can be misread. | S5-D baseline frames timestamp/freshness as open questions. | Candidate timestamp labels with no thresholds or runtime behavior. | Timestamp semantics freeze, polling, sync, SLA, performance commitment. | Freshness labels become runtime acceptance or service guarantees. | S5-D-2 may ask which timestamp labels belong in synthetic examples. |
| Provenance/confidence terminology | `NEEDS_DECISION` | Provenance and confidence can help review but must not alter trust precedence. | S5-D baseline says telemetry confidence cannot override S4-A or S5-B boundaries. | Non-authorizing provenance/confidence labels. | Trust precedence change, source authority, identity authority, routing decisions. | Confidence becomes authority or operational decision input. | S5-D-2 may include provenance/confidence notes as open questions. |
| Redaction and secret-handling boundary | `NEEDS_DECISION` | Telemetry may contain secrets, identifiers, payload fragments, command lines, or customer/operator details. | S5-D baseline prohibits credentials, raw payloads, and customer/operator evidence. | Redaction checklist and prohibited-category list. | Secrets, auth material, raw payloads, real evidence retention. | Credentials, tokens, API keys, auth headers, or raw payloads appear. | S5-D-2 should keep examples synthetic/redacted by design. |
| Telemetry event retention boundary | `DEFERRED` | Real telemetry retention requires governance separate from discovery. | S5-D baseline blocks retained real telemetry events without evidence-retention/redaction approval. | Governance questions only. | Real telemetry event collection, storage, retention, or replay. | Real telemetry is retained without separate approval. | Separate evidence-retention/redaction decision before any real telemetry evidence. |
| Synthetic/redacted evidence boundary | `NEEDS_DECISION` | Synthetic/redacted descriptions can support review without real payloads. | S5-D baseline permits synthetic examples embedded as shape descriptions only. | Prose/table descriptions with synthetic values and redaction notes. | Raw payloads, screenshots/logs, fixture files, external evidence. | Synthetic examples are mistaken for real evidence or contract. | S5-D-2 should define synthetic shape as documentation only. |
| Fixture-file boundary | `NOT_APPLICABLE` | S5-D-1 does not create or modify fixtures. | User scope forbids fixture file creation or modification. | Boundary statement only. | Fixture files, test changes, JSON examples committed as fixtures. | Any fixture file is created or changed. | Later scoped ticket only if product/governance authorizes fixtures. |
| Queue/fan-out boundary | `NOT_APPLICABLE` | Queue/fan-out is runtime architecture, not discovery classification. | S5-D baseline blocks queue/fan-out. | Boundary statement only. | Queues, fan-out, streaming pipelines, workers, delivery guarantees. | Runtime ingestion architecture appears. | None in S5-D-1. |
| Performance/SLA boundary | `NOT_APPLICABLE` | Performance/SLA commitments can imply production readiness. | Route and S5-D baseline block performance/SLA commitments. | Boundary statement only. | Latency, throughput, availability, freshness SLA, scale commitments. | Any SLA or performance guarantee appears. | None in S5-D-1. |
| Alert routing boundary | `NOT_APPLICABLE` | Alert routing would turn discovery into operational workflow design. | S5-D baseline blocks alert routing. | Boundary statement only. | Dispatch, notification, escalation, SOC routing. | Alert routing is introduced. | None in S5-D-1. |
| Response automation boundary | `NOT_APPLICABLE` | Response automation would imply action execution outside discovery. | S5-C and S5-D baselines block destructive response automation. | Boundary statement only. | Containment, remediation, blocking, ticket action, workflow engine. | Response automation is introduced. | None in S5-D-1. |
| Relationship to S5-A external pilot inputs | `DEFERRED` | Telemetry gaps may inform future input collection but cannot make S5-A ready. | S5-A assessment keeps all seven categories `UNKNOWN` and decision readiness `NOT_READY`. | Gap-to-input questions without real evidence collection. | External pilot READY claim, real sign-off, evidence acceptance, pilot execution. | Matrix output is treated as external pilot evidence or go/no-go. | Later external input collection if product/governance provides owners. |
| Relationship to S5-B source/input discovery baseline | `NEEDS_DECISION` | Telemetry handoff overlaps with source provenance, freshness, and host identity. | S5-B is `PASS_AND_PARK` discovery baseline only. | References to S5-B gaps and boundaries. | Reopening S5-B, freezing source contract, source adapter implementation. | S5-B PASS is treated as implementation or contract freeze. | S5-D-2 can reuse S5-B boundaries without changing them. |
| Relationship to S5-C parked case workflow | `NOT_APPLICABLE` | Telemetry discovery must not reopen case workflow or endpoint work. | S5-C is parked; S5-C-4 is `KEEP_DEFERRED`. | Boundary reference only. | Case workflow changes, public endpoint work, ticketing/workflow engine. | S5-C is reopened or endpoint work begins. | None in S5-D-1. |

## 7. Source Category Notes
Telemetry source categories are discovery handles only.

They do not authorize:
- live access
- connector credentials
- raw payloads
- adapter implementation
- fixture files
- source authority

Any later source category decision that freezes telemetry semantics, changes source identity authority, accepts real external evidence, or changes redaction/secret/evidence retention boundaries must re-evaluate `requires_external_review`.

## 8. Event Shape Notes
Field-area shape notes are questions only.

They do not freeze:
- telemetry schema
- normalized fields
- timestamp/freshness semantics
- provenance/confidence semantics
- trust precedence
- runtime/API behavior

S5-D-1 may identify field-area gaps, but any later event shape must remain synthetic, redacted, and non-authorizing unless a separate governed ticket explicitly changes scope.

## 9. Host Identity Handoff Boundary
- S5-D-1 may only classify gaps about how telemetry could provide host identifier candidates.
- S5-D-1 must not change resolver behavior.
- S5-D-1 must not bypass `AssetInventorySnapshot` authority.
- S5-D-1 must not change resolver priority: `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- Telemetry confidence must not silently resolve host ambiguity.
- Host identity ambiguity remains explicit and governed by S4-A unless a later governed decision changes authority or semantics.

## 10. Evidence Boundary

Allowed evidence:
- governed repo docs
- synthetic examples as shape descriptions only
- redacted shape descriptions
- read-only repo inventory
- gap matrices
- non-authorizing contract sketches

Forbidden evidence:
- real telemetry payloads
- raw SIEM/EDR exports
- screenshots/logs from customer/operator systems
- credentials, tokens, API keys, auth headers
- customer/operator evidence
- real external access
- retained real telemetry events without separate evidence-retention/redaction approval

## 11. HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| Live SIEM/EDR/telemetry/source access is required. | S5-D-1 is docs-only and has no governed real access approval. |
| Connector credentials, auth headers, tokens, API keys, cookies, or other secrets appear. | Secret handling and credential collection are prohibited. |
| Raw telemetry payloads, raw SIEM/EDR exports, screenshots/logs, or customer/operator evidence appear. | S5-D-1 permits only governed docs and synthetic/redacted shape descriptions. |
| Real telemetry event payloads are retained or real telemetry evidence is collected without separate evidence-retention and redaction approval. | Telemetry retention requires separate governance. |
| Telemetry normalization semantics are frozen. | The matrix classifies gaps only and creates no normalized telemetry contract. |
| Timestamp/freshness semantics are frozen. | Candidate timing language must not become runtime behavior or acceptance thresholds. |
| Telemetry provenance/confidence changes trust precedence or creates source authority. | Provenance and confidence are open questions only. |
| Queue, fan-out, streaming, worker, delivery guarantee, or performance/SLA commitment appears. | Runtime telemetry architecture and operational commitments are out of scope. |
| Alert routing appears. | S5-D-1 is not alert dispatch, notification routing, or escalation routing. |
| Response automation appears. | S5-D-1 is not containment, remediation, blocking, ticket action, or destructive automation. |
| Runtime/API/schema/test/dependency changes appear. | This draft authorizes no implementation changes. |
| Fixture files are created or modified. | S5-D-1 is documentation only and creates no fixtures. |
| S4-A host identity handoff is bypassed or resolver priority changes. | `AssetInventorySnapshot` and resolver order remain governed by S4-A. |
| External pilot READY claim is made. | S5-A remains `NOT_READY` / `UNKNOWN`. |
| External pilot execution is implied. | External pilot execution remains unauthorized. |
| Real customer/operator sign-off is implied. | No real sign-off exists or is created by this draft. |
| S5-C is reopened. | S5-C remains parked. |
| Public close-case endpoint work appears. | S5-C-4 remains `KEEP_DEFERRED`. |
| AI_COLLAB primary implementor, reviewer separation, single-writer, human go/no-go, or external-review rules are bypassed. | Governed collaboration rules apply to all later S5-D work. |

## 12. Preliminary Recommendation
Recommendation: `PROCEED_TO_S5_D_2_SYNTHETIC_TELEMETRY_EVENT_SHAPE`.

Meaning:
- A later docs-only S5-D-2 artifact may describe a non-authorizing synthetic telemetry event shape based on this gap matrix.
- S5-D-2 should keep event fields as questions or candidate field areas, not schema.
- S5-D-2 should preserve S5-A, S5-B, S5-C, and S4-A boundaries.

Non-meaning:
- no implementation
- no fixture files
- no telemetry adapter work
- no source adapter work
- no runtime/API/schema/test/dependency changes
- no live SIEM/EDR/telemetry access
- no credentials or raw telemetry payloads
- no schema freeze
- no telemetry normalization freeze
- no timestamp/freshness semantics freeze
- no provenance/confidence trust change
- no closeout
- no external pilot readiness claim

## 13. Acceptance Criteria
This draft is acceptable if:
- it is one new doc only
- it preserves S5-A/S5-B/S5-C/S4-A boundaries
- it lists S5-D-1 stream-specific risks early
- it uses only allowed matrix status vocabulary
- it does not authorize implementation
- it does not authorize live telemetry access
- it does not authorize credentials or raw payloads
- it does not authorize real telemetry event retention
- it does not freeze telemetry normalization, timestamp/freshness semantics, or provenance/confidence semantics
- it documents a `requires_external_review` decision with AI_COLLAB-complete re-evaluation triggers
- it does not create or modify fixture files
- it does not modify runtime/API/schema/test/dependency behavior
- it does not modify HANDOFF or manifest
- it does not claim external pilot readiness
- it identifies the recommended next docs-only route or explicitly records the route as an open product/governance question
