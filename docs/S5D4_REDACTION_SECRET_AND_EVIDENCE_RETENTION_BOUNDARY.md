# S5-D-4 Redaction Secret And Evidence Retention Boundary

## 1. Document Control
- Title: S5-D-4 Redaction Secret And Evidence Retention Boundary
- Status: Closed as governed redaction, secret, and evidence retention boundary baseline
- Baseline snapshot: `S5-D-DISCOVERY-2026-04-15-004`
- Source of truth: `D:\产品设计\New folder`
- Prior artifact: `docs/S5D3_TELEMETRY_PROVENANCE_AND_FRESHNESS_BOUNDARY.md`
- Scope: S5-D-4 redaction, secret handling, and evidence-retention boundary discovery only
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code
- `reviewer`: Claude Code
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false initially

This draft may ask boundary questions only. If this work changes, freezes, or approves any redaction, secret handling, evidence retention, deletion/expiry, evidence packaging, or real telemetry handling boundary, it must HOLD instead of continuing as normal draft-only work because redaction/secret/evidence retention boundary changes require `requires_external_review=true`.

Re-evaluate and set `requires_external_review=true` later if any of these appear:
- telemetry normalization semantics freeze
- timestamp/freshness semantics freeze
- real external evidence/access
- S4-A identity authority changes
- stream/milestone closeout
- redaction/secret/evidence retention boundary changes

## 2. Goal
S5-D-4 drafts a bounded telemetry redaction, secret handling, and evidence-retention boundary discovery artifact after the governed S5-D-3 provenance/freshness boundary.

The goal is to identify open questions, prohibited categories, and HOLD triggers around synthetic examples, redaction notes, secret material, raw payloads, screenshots/logs/exports, evidence retention language, retention/deletion/expiry wording, and case/evidence handoff language. This document does not approve or freeze redaction policy, secrets handling implementation, evidence retention policy, retention duration, deletion/expiry behavior, storage/replay behavior, evidence-pack behavior, telemetry schema, telemetry normalization, timestamp/freshness semantics, provenance/confidence trust precedence, runtime/API/schema/test behavior, or fixture format.

## 3. Non-Goals
- live SIEM/EDR/source/telemetry access
- connector credentials, tokens, API keys, auth headers, cookies, or secret material
- raw telemetry payloads
- raw logs, screenshots, exports, event bodies, customer/operator evidence
- real telemetry event retention
- redaction policy freeze
- secrets handling implementation
- evidence retention approval
- retention duration policy
- deletion/expiry policy
- storage/replay/evidence-pack behavior
- telemetry schema freeze
- telemetry normalization freeze
- timestamp/freshness semantics freeze
- provenance/confidence trust precedence freeze
- source authority decisions
- queue/fan-out
- performance/SLA commitments
- alert routing
- response automation
- runtime/API/schema/test/dependency changes
- fixture file creation or modification
- S4-A resolver priority changes
- S5-C reopening
- public close-case endpoint work
- external pilot readiness claims
- `docs/HANDOFF.md` updates
- `releases/release_manifest.json` updates
- AI_COLLAB operating model or contract changes

## 4. Inherited Baseline
- S5-A external pilot input remains `NOT_READY` / `UNKNOWN`.
- S5-B remains `PASS_AND_PARK` discovery baseline only.
- S5-C remains parked.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- S4-A host identity authority remains unchanged.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- S5-D-4 does not improve external pilot readiness.
- Human go/no-go remains required before any next ticket.
- S5-D-3 recommended `PROCEED_TO_S5_D_4_REDACTION_SECRET_AND_EVIDENCE_RETENTION_BOUNDARY` as a later docs-only route and did not authorize redaction policy freeze, secrets handling implementation, evidence retention, real telemetry handling, fixture creation, runtime/API/schema/test/dependency changes, external review bypass, S4-A boundary changes, S5-C reopening, or public close-case endpoint work.

## 5. S5-D Fixed Risk Checklist
Any item below becoming authorized or implied is a HOLD condition.

| Risk category | HOLD trigger |
| --- | --- |
| live SIEM/EDR/telemetry access | HOLD if S5-D-4 requires connecting to live SIEM, EDR, telemetry, source, or customer/operator systems. |
| connector credentials / tokens / API keys | HOLD if credentials, auth headers, tokens, API keys, cookies, or other secret material are requested, stored, pasted, inferred, or retained. |
| raw telemetry payloads | HOLD if raw telemetry exports, event bodies, screenshots, logs, or customer/operator payloads are introduced as evidence. |
| telemetry event retention | HOLD if real telemetry event payloads are retained or real telemetry evidence is collected without separate evidence-retention and redaction approval. |
| telemetry normalization freeze | HOLD if this discovery draft freezes telemetry fields, mapping rules, event categories, normalization behavior, or parser behavior. |
| timestamp/freshness semantics freeze | HOLD if candidate timestamp or freshness labels become fixed semantics, runtime expectations, polling rules, acceptance thresholds, or operational recency guarantees. |
| queue/fan-out | HOLD if discovery language implies queues, fan-out, streaming pipelines, background workers, delivery guarantees, or concurrency architecture. |
| performance/SLA commitments | HOLD if latency, throughput, freshness SLA, availability, scale, or operational performance commitments appear. |
| alert routing | HOLD if telemetry discovery becomes alert routing, notification routing, escalation routing, or SOC workflow dispatch. |
| response automation | HOLD if telemetry discovery implies containment, remediation, blocking, ticket action, or other automated response behavior. |
| runtime/API/schema/test/dependency changes | HOLD if any production code, API, schema, test, fixture, dependency, or release-tooling change is required from this draft. |
| S4-A host identity handoff bypass | HOLD if telemetry identifiers bypass `AssetInventorySnapshot`, change resolver priority, silently resolve ambiguity, or create new identity authority. |
| external pilot readiness misread as improved | HOLD if S5-D-4 is treated as reducing S5-A `UNKNOWN` categories to external pilot readiness without governed external inputs. |

## 6. S5-D-4 Specific Risk Checklist
Any item below becoming authorized, frozen, operationalized, or implied is a HOLD condition.

| Risk category | HOLD trigger |
| --- | --- |
| Redaction wording mistaken for redaction policy freeze | HOLD if candidate redaction wording becomes an approved redaction policy, algorithm, mask pattern, required field rule, or implementation requirement. |
| Secret handling wording mistaken for secrets handling implementation | HOLD if candidate secret-handling notes become credential collection, storage, scanning, validation, or runtime secret-management behavior. |
| Evidence-retention wording mistaken for evidence retention approval | HOLD if notes about retention become authorization to collect, store, keep, replay, package, audit, or preserve real telemetry evidence. |
| `redacted` labels mistaken as approval to retain real payloads | HOLD if a redacted label is used to justify keeping raw telemetry, customer/operator data, screenshots, logs, exports, or event bodies. |
| Synthetic examples mistaken for fixture files or schema contracts | HOLD if synthetic prose becomes fixture creation, schema freeze, required field format, or adapter contract. |
| Raw logs, screenshots, exports, event bodies, or customer/operator evidence introduced as validation | HOLD if real evidence is added, requested, pasted, retained, or treated as validation for this draft. |
| Credentials, tokens, API keys, auth headers, cookies, or secret material requested, stored, pasted, inferred, or retained | HOLD if any secret material appears directly, indirectly, or as a derived artifact. |
| Retention notes mistaken for storage, replay, evidence-pack, or audit-retention behavior | HOLD if candidate retention language creates storage locations, replay rules, evidence packs, audit retention, or lifecycle behavior. |
| Deletion/expiry wording mistaken for data lifecycle policy | HOLD if deletion or expiry wording becomes a duration, deletion window, retention lifecycle, or operational policy. |
| Redaction/secret/evidence retention boundary changes without `requires_external_review=true` | HOLD if any boundary change appears without external-review escalation. |
| Case/evidence handoff language reopening S5-C or the public close-case endpoint | HOLD if evidence handoff language changes case workflow, sign-off, public close-case endpoint, ticketing, or workflow behavior. |
| External pilot readiness misread as improved because questions are better organized | HOLD if organizing these questions is treated as external pilot readiness, real sign-off, or external evidence acceptance. |

## 7. Status Vocabulary
Discovery rows in this document use only these status values:
- `UNKNOWN`
- `NEEDS_DECISION`
- `DEFERRED`
- `NOT_APPLICABLE`

These values are non-authorizing discovery labels. They do not approve implementation, policy, retention, external access, evidence handling, fixture creation, runtime behavior, source authority, identity authority, external pilot execution, or stream closeout.

## 8. Redaction Boundary Questions

| Area | Boundary question | Status | Safe discussion scope | HOLD trigger |
| --- | --- | --- | --- | --- |
| Redaction note wording | What wording can indicate that an example is synthetic or redacted without freezing a redaction policy? | `NEEDS_DECISION` | Candidate prose labels only. | Wording becomes redaction policy, mask pattern, algorithm, required field, or implementation behavior. |
| `redacted` label meaning | How should the draft prevent `redacted` from being read as permission to retain real payloads? | `NEEDS_DECISION` | Boundary language that prohibits real payload retention. | `redacted` is used to justify retaining logs, exports, screenshots, event bodies, or customer/operator evidence. |
| Raw payload boundary | Which categories must remain prohibited even if examples are described as redacted? | `NEEDS_DECISION` | Prohibited-category checklist. | Raw telemetry payloads, event bodies, logs, screenshots, exports, or customer/operator evidence appear. |
| Synthetic-only marker | How should synthetic-only examples be marked without creating fixture files or schema contracts? | `UNKNOWN` | Prose/table descriptions only. | Synthetic examples become fixture files, schemas, adapter requirements, or tests. |
| Case/evidence language | How should evidence handoff wording avoid reopening S5-C? | `NEEDS_DECISION` | Boundary statements referencing parked S5-C and `KEEP_DEFERRED`. | Case workflow, public close-case endpoint, workflow engine, ticketing, or sign-off behavior is reopened. |

## 9. Secret Handling Boundary Questions

| Area | Boundary question | Status | Safe discussion scope | HOLD trigger |
| --- | --- | --- | --- | --- |
| Credential handling | How should S5-D-4 state that credentials, tokens, API keys, and auth headers are never allowed in this draft? | `NEEDS_DECISION` | Prohibited-category language only. | Any credential, token, API key, auth header, cookie, or secret material is requested, stored, pasted, inferred, or retained. |
| Inferred secret material | How should the draft prevent screenshots, logs, or exports from indirectly exposing secrets? | `NEEDS_DECISION` | Boundary questions and prohibited evidence categories. | Real screenshots, logs, exports, or payloads are introduced as validation. |
| Secret handling implementation | How should wording avoid becoming secret detection, scanning, storage, rotation, or vault behavior? | `NOT_APPLICABLE` | Non-goal and HOLD language only. | Secret-handling implementation or dependency changes appear. |
| External access path | How should the draft prevent redaction discussion from implying live connector access? | `NEEDS_DECISION` | Boundary statement only. | Live SIEM/EDR/source/telemetry access or connector setup appears. |

## 10. Evidence Retention Boundary Questions

| Area | Boundary question | Status | Safe discussion scope | HOLD trigger |
| --- | --- | --- | --- | --- |
| Evidence retention note | What note can state that real telemetry retention is prohibited without separate approval? | `NEEDS_DECISION` | Governance boundary wording only. | Real telemetry evidence is retained or accepted. |
| Retention duration wording | How should the draft avoid specifying duration, expiry, deletion, or lifecycle policy? | `NEEDS_DECISION` | Open question only. | A retention duration, deletion window, expiry rule, or data lifecycle policy is defined. |
| Storage/replay wording | How should the draft prevent retention notes from implying storage location, replay, audit, or evidence-pack behavior? | `NEEDS_DECISION` | Boundary language only. | Storage, replay, audit retention, evidence packaging, or persistence behavior appears. |
| Real external evidence | What separates future evidence collection questions from accepting real evidence now? | `UNKNOWN` | Future-governance question only. | Real external evidence/access appears without separate governed scope and external review. |
| Evidence-pack language | How should evidence pack wording remain out of scope? | `DEFERRED` | Non-goal and HOLD language only. | Evidence-pack format, contents, retention, packaging, or delivery behavior is defined. |

## 11. Synthetic Example And Non-Payload Boundary
Synthetic examples in S5-D-4 may be prose or table descriptions only. They must not become fixture files, schema definitions, required fields, adapter contracts, parser inputs, normalized event formats, runtime behavior, API behavior, tests, or evidence-pack content.

Allowed synthetic discussion:
- generic labels that contain no real organization, source, operator, customer, user, host, event, credential, token, API key, auth header, cookie, or payload data
- high-level redaction notes that explain prohibited categories
- candidate questions about what a later governed route would need to decide

Forbidden evidence and payload categories:
- raw telemetry payloads
- raw SIEM/EDR/source exports
- raw logs
- screenshots from real systems
- event bodies
- customer/operator evidence
- credentials, tokens, API keys, auth headers, cookies, or secret material
- retained real telemetry events without separate evidence-retention/redaction approval

## 12. Case / Evidence Handoff Boundary
S5-D-4 may ask how telemetry evidence wording could avoid ambiguity, but it must not create case workflow behavior, evidence-pack behavior, sign-off workflow, public endpoint work, ticketing integration, workflow engine behavior, alert routing, response automation, or any S5-C reopening.

S5-C remains parked. The public close-case endpoint remains `KEEP_DEFERRED`. Case/evidence handoff notes in this document are boundary questions only and do not authorize evidence retention, evidence packaging, operator sign-off, external pilot execution, or public close-case endpoint work.

## 13. Boundary Matrix

| Boundary area | Candidate question | Status | Not authorized | HOLD trigger | Candidate follow-up |
| --- | --- | --- | --- | --- | --- |
| Redaction note wording | What wording can describe synthetic/redacted examples without freezing policy? | `NEEDS_DECISION` | Redaction policy, mask pattern, algorithm, implementation. | Wording becomes required redaction behavior. | Product/governance route decision. |
| Synthetic-only marker | How should a synthetic-only marker avoid becoming fixture format? | `UNKNOWN` | Fixture files, schema fields, tests, adapter contracts. | Marker becomes a required field or fixture instruction. | Product/governance route decision. |
| Prohibited secret categories | Which secret categories must remain explicitly prohibited? | `NEEDS_DECISION` | Secret collection, storage, scanning, validation, dependencies. | Any secret material appears or is requested. | Product/governance route decision. |
| Credential/token/API-key handling boundary | How should credentials, tokens, and API keys be excluded from all S5-D draft evidence? | `NEEDS_DECISION` | Credential handling implementation, vault behavior, connector setup. | Credentials, tokens, or API keys are pasted, stored, inferred, or retained. | Product/governance route decision. |
| Auth header/cookie handling boundary | How should auth headers and cookies remain prohibited even in redacted examples? | `NEEDS_DECISION` | Auth handling, header parsing, cookie capture. | Auth headers or cookies appear in any form. | Product/governance route decision. |
| Raw telemetry payload boundary | How should the draft prohibit raw event bodies and vendor payloads? | `NEEDS_DECISION` | Payload retention, schema extraction, parser behavior. | Raw telemetry payloads appear. | Product/governance route decision. |
| Raw log/screenshot/export boundary | How should logs, screenshots, and exports from real systems remain out of scope? | `NEEDS_DECISION` | Real logs, screenshots, exports, evidence files. | Real logs, screenshots, or exports are added as validation. | Product/governance route decision. |
| Customer/operator evidence boundary | How should real customer/operator evidence remain prohibited? | `NEEDS_DECISION` | Customer/operator files, sign-off, evidence acceptance. | Real customer/operator evidence appears or is implied. | Product/governance route decision. |
| Evidence retention note | What note clarifies that real telemetry event retention is not authorized? | `NEEDS_DECISION` | Real evidence retention, evidence approval. | Real telemetry evidence is retained without separate approval. | Product/governance route decision. |
| Retention duration wording | How should retention duration stay undecided? | `UNKNOWN` | Retention duration policy, retention windows. | Any duration or retention window is defined. | Product/governance route decision. |
| Deletion/expiry wording | How should deletion and expiry remain open questions? | `UNKNOWN` | Deletion policy, expiry policy, lifecycle behavior. | Any deletion or expiry policy is defined. | Product/governance route decision. |
| Storage/replay wording | How should storage and replay remain out of scope? | `NEEDS_DECISION` | Storage locations, replay behavior, audit retention. | Storage, replay, or audit-retention behavior appears. | Product/governance route decision. |
| Evidence pack wording | How should evidence-pack language avoid creating package behavior? | `DEFERRED` | Evidence-pack format, contents, delivery, retention. | Evidence-pack behavior is defined. | Product/governance route decision. |
| Provenance note interaction | How should provenance notes reference redaction boundaries without creating source authority? | `NEEDS_DECISION` | Source authority, trust precedence, external evidence acceptance. | Provenance note becomes authority or validation. | Product/governance route decision. |
| Freshness/timestamp note interaction | How should timestamp/freshness notes avoid retention or lifecycle implications? | `UNKNOWN` | Timestamp/freshness freeze, retention duration, SLA. | Timestamp/freshness notes become semantics or recency guarantees. | Product/governance route decision. |
| Confidence note interaction | How should confidence notes avoid trust-precedence implications? | `NEEDS_DECISION` | Confidence scoring, trust ordering, resolver override. | Confidence changes trust precedence or identity handling. | Product/governance route decision. |
| Host identity note interaction | How should host identity notes preserve S4-A resolver order? | `NEEDS_DECISION` | S4-A authority change, resolver priority change. | Telemetry confidence bypasses `AssetInventorySnapshot` or changes resolver order. | Product/governance route decision. |
| Case/evidence handoff note | How should case/evidence wording avoid reopening S5-C? | `NEEDS_DECISION` | Case workflow changes, public endpoint work, sign-off flow. | S5-C or public close-case endpoint work is reopened. | Product/governance route decision. |
| External pilot evidence note | How should external pilot evidence remain out of scope? | `DEFERRED` | External pilot readiness, execution, sign-off, real evidence acceptance. | S5-D-4 is treated as improving external pilot status. | Product/governance route decision. |

## 14. HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| Live SIEM/EDR/source/telemetry access is required. | This draft has no governed real access approval. |
| Connector credentials, auth headers, tokens, API keys, cookies, or secret material appear. | Secret material is prohibited in this docs-only boundary draft. |
| Raw telemetry payloads, raw SIEM/EDR/source exports, raw logs, screenshots, event bodies, or customer/operator evidence appear. | S5-D-4 permits only governed docs and synthetic/redacted prose descriptions. |
| Real telemetry event payloads are retained or real telemetry evidence is collected without separate evidence-retention and redaction approval. | Evidence retention requires separate governed approval and external-review evaluation. |
| Redaction wording becomes redaction policy, mask pattern, algorithm, or implementation requirement. | S5-D-4 asks questions only and does not freeze redaction behavior. |
| Secret handling wording becomes secrets handling implementation. | Secret handling implementation is out of scope. |
| Evidence-retention wording becomes evidence retention approval. | This draft does not authorize retaining real telemetry evidence. |
| Retention duration, deletion window, expiry rule, storage behavior, replay behavior, audit-retention behavior, or evidence-pack behavior is defined. | Data lifecycle and evidence-pack behavior are not authorized. |
| Telemetry schema, normalization, timestamp/freshness semantics, provenance/confidence semantics, or trust precedence is frozen. | Semantics freeze requires separate governed work and external-review evaluation. |
| Source authority decision appears. | Provenance, confidence, source labels, and redaction notes cannot create authority. |
| Queue/fan-out, performance/SLA commitments, alert routing, or response automation appears. | Operational telemetry architecture and SOC workflow behavior are out of scope. |
| Runtime/API/schema/test/dependency changes appear. | This task is docs-only and creates no implementation behavior. |
| Fixture files are created or modified. | Synthetic examples are prose/table descriptions only. |
| S4-A host identity handoff is bypassed or resolver priority changes. | S4-A authority and resolver order remain unchanged. |
| S5-C is reopened or public close-case endpoint work appears. | S5-C remains parked and the public close-case endpoint remains `KEEP_DEFERRED`. |
| External pilot readiness, execution, or real sign-off is implied. | S5-A remains `NOT_READY` / `UNKNOWN`, and no real sign-off exists. |
| `docs/HANDOFF.md`, `releases/release_manifest.json`, AI_COLLAB operating model, or contract files are modified. | This is a draft-only one-file task. |
| AI_COLLAB primary implementor, reviewer separation, single-writer, human go/no-go, or external-review rules are bypassed. | Governed collaboration rules apply to all later S5-D work. |

## 15. Preliminary Recommendation
Recommendation: `ROUTE_DECISION_REQUIRED_AFTER_S5_D_4`.

Reason:
S5-D-4 touches the highest-risk S5-D boundary area. After documenting redaction, secret handling, and evidence-retention boundary questions, the next step should be an explicit product/governance route decision rather than automatically continuing into a policy, implementation, fixture, or stream-closeout ticket.

The route decision should determine whether later work remains planning-only, opens a reviewed docs-only policy-candidate discussion, returns to external input collection, opens another bounded discovery artifact, or parks S5-D pending product/governance direction. Any route touching redaction/secret/evidence-retention boundary changes must re-evaluate `requires_external_review` and HOLD or set it true before proceeding.

## 16. Preliminary Recommendation Non-Meaning
`ROUTE_DECISION_REQUIRED_AFTER_S5_D_4` does not authorize:
- redaction policy freeze
- secrets handling implementation
- evidence retention
- retention/deletion/expiry policy
- evidence-pack/storage/replay behavior
- real telemetry handling
- raw payload handling
- fixture creation
- runtime/API/schema/test/dependency changes
- live SIEM/EDR/source/telemetry access
- credentials/tokens/API keys/auth headers/cookies collection
- S4-A identity authority changes
- S5-C reopening
- public close-case endpoint work
- external pilot readiness or execution
- stream/milestone closeout
- external review bypass

## 17. Acceptance Criteria
This draft is acceptable if:
- exactly one new docs-only file is created
- the S5-D fixed risk checklist is present and complete
- the S5-D-4 specific risks are present
- redaction, secret handling, and evidence retention are framed as open boundary questions only
- no redaction policy, secrets handling implementation, evidence retention, retention duration, deletion/expiry, evidence-pack, storage, replay, schema, normalization, timestamp, freshness, provenance, confidence, or trust semantics are frozen
- S4-A host identity handoff and resolver order are preserved
- S5-C and public close-case endpoint remain parked/deferred
- no live access, credentials, raw payloads, logs, screenshots, exports, customer/operator evidence, retention, fixtures, runtime/API/schema/test/dependency changes are authorized
- the `requires_external_review` decision and AI_COLLAB-complete re-evaluation triggers are documented
- if any redaction/secret/evidence-retention boundary change appears, the draft must HOLD or set `requires_external_review=true`
- the preliminary recommendation is explicitly non-authorizing
- HANDOFF and manifest are not modified
