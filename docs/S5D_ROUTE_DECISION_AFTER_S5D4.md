# S5-D Route Decision After S5-D-4

## 1. Document Control
- Title: S5-D Route Decision After S5-D-4
- Status: Closed as governed S5-D route decision after S5-D-4 baseline
- Baseline snapshot: `S5-D-DISCOVERY-2026-04-15-005`
- Source of truth: `D:\产品设计\New folder`
- Prior artifact: `docs/S5D4_REDACTION_SECRET_AND_EVIDENCE_RETENTION_BOUNDARY.md`
- Scope: S5-D route-selection checkpoint only
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code
- `reviewer`: Claude Code
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false initially

This route-decision draft may compare routes only. It must not itself close the S5-D stream or milestone, freeze redaction, secret handling, evidence retention, telemetry normalization, timestamp/freshness, provenance/confidence, source authority, or S4-A identity boundaries.

Re-evaluate and set `requires_external_review=true` later if any of these appear:
- telemetry normalization semantics freeze
- timestamp/freshness semantics freeze
- real external evidence/access
- S4-A identity authority changes
- stream/milestone closeout
- redaction/secret/evidence retention boundary changes

## 2. Goal
This checkpoint compares bounded candidate next routes after S5-D-4 documented redaction, secret handling, and evidence-retention boundary questions.

The goal is to identify which next routes are safe, which routes require external-review implications, and which routes must remain blocked unless a later human product/governance decision explicitly opens them. This document does not authorize implementation, policy freeze, evidence retention, stream/milestone closeout, external pilot readiness, or any runtime/API/schema/test/dependency/fixture changes.

## 3. Non-Goals
- implementation authorization
- runtime/API/schema/test/dependency changes
- fixture file creation or modification
- live SIEM/EDR/source/telemetry access
- connector credentials, tokens, API keys, auth headers, cookies, or secret material
- raw telemetry payloads
- raw logs, screenshots, exports, event bodies, customer/operator evidence
- real telemetry event retention
- redaction policy freeze
- secrets handling implementation
- evidence retention approval
- retention/deletion/expiry policy
- storage/replay/evidence-pack behavior
- telemetry schema freeze
- telemetry normalization freeze
- timestamp/freshness semantics freeze
- provenance/confidence trust precedence freeze
- source authority decisions
- S4-A resolver priority changes
- S5-C reopening
- public close-case endpoint work
- external pilot readiness claims
- external pilot execution
- real customer/operator sign-off
- stream/milestone closeout
- external review bypass
- `docs/HANDOFF.md` updates
- `releases/release_manifest.json` updates
- AI_COLLAB operating model or contract changes

## 4. Current Governed Baseline
- Active baseline is `S5-D-DISCOVERY-2026-04-15-005`.
- `docs/S5D4_REDACTION_SECRET_AND_EVIDENCE_RETENTION_BOUNDARY.md` is the governed S5-D-4 redaction, secret handling, and evidence-retention boundary baseline.
- S5-D-4 preliminary recommendation is `ROUTE_DECISION_REQUIRED_AFTER_S5_D_4`.
- S5-A external pilot input remains `NOT_READY` / `UNKNOWN`.
- S5-B remains `PASS_AND_PARK` discovery baseline only.
- S5-C remains parked.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- S4-A host identity authority remains unchanged.
- S4-A resolver order must remain: `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- S5-D route decision does not improve external pilot readiness.
- Human go/no-go remains required before any next ticket.
- `docs/AI_COLLAB_OPERATING_MODEL.md` governs primary implementor, reviewer separation, single-writer discipline, human go/no-go, and trigger-based external review.

## 5. S5-D Fixed Risk Checklist
Any item below becoming authorized or implied is a HOLD condition.

| Risk category | HOLD trigger |
| --- | --- |
| live SIEM/EDR/telemetry access | HOLD if this route checkpoint requires connecting to live SIEM, EDR, telemetry, source, or customer/operator systems. |
| connector credentials / tokens / API keys | HOLD if credentials, auth headers, tokens, API keys, cookies, or secret material are requested, stored, pasted, inferred, or retained. |
| raw telemetry payloads | HOLD if raw telemetry exports, event bodies, screenshots, logs, or customer/operator payloads are introduced as evidence. |
| telemetry event retention | HOLD if real telemetry event payloads are retained or real telemetry evidence is collected without separate evidence-retention and redaction approval. |
| telemetry normalization freeze | HOLD if the route decision freezes telemetry fields, mapping rules, event categories, normalization behavior, or parser behavior. |
| timestamp/freshness semantics freeze | HOLD if candidate timestamp or freshness labels become fixed semantics, runtime expectations, polling rules, acceptance thresholds, or operational recency guarantees. |
| queue/fan-out | HOLD if route language implies queues, fan-out, streaming pipelines, background workers, delivery guarantees, or concurrency architecture. |
| performance/SLA commitments | HOLD if latency, throughput, freshness SLA, availability, scale, or operational performance commitments appear. |
| alert routing | HOLD if telemetry discovery becomes alert routing, notification routing, escalation routing, or SOC workflow dispatch. |
| response automation | HOLD if telemetry discovery implies containment, remediation, blocking, ticket action, or other automated response behavior. |
| runtime/API/schema/test/dependency changes | HOLD if any production code, API, schema, test, fixture, dependency, or release-tooling change is required from this route checkpoint. |
| S4-A host identity handoff bypass | HOLD if telemetry identifiers bypass `AssetInventorySnapshot`, change resolver priority, silently resolve ambiguity, or create new identity authority. |
| external pilot readiness misread as improved | HOLD if this route checkpoint is treated as reducing S5-A `UNKNOWN` categories to external pilot readiness without governed external inputs. |

## 6. Route-Decision-Specific Risk Checklist
Any item below becoming authorized, frozen, closed, or implied is a HOLD condition.

| Risk category | HOLD trigger |
| --- | --- |
| route decision being mistaken for implementation authorization | HOLD if any route option is treated as permission to implement telemetry, source, runtime, API, schema, test, dependency, fixture, or release-tooling changes. |
| route decision being mistaken for redaction policy freeze | HOLD if comparing redaction routes is treated as approving redaction policy, mask rules, required fields, or algorithms. |
| route decision being mistaken for secrets handling implementation | HOLD if comparing secret-handling routes is treated as authorizing secret collection, storage, scanning, validation, vault behavior, or credential workflow. |
| route decision being mistaken for evidence retention approval | HOLD if any route option is treated as approval to retain, store, replay, package, audit, or preserve real telemetry evidence. |
| route decision being mistaken for retention/deletion/expiry policy | HOLD if any route option defines retention duration, deletion windows, expiry rules, or data lifecycle behavior. |
| route decision being mistaken for stream/milestone closeout | HOLD if this checkpoint itself is treated as S5-D stream closeout. |
| route decision being mistaken for external review bypass | HOLD if a high-risk route is selected without recording required `requires_external_review` implications. |
| S5-D discovery baseline being mistaken for external pilot readiness improvement | HOLD if S5-D discovery artifacts are treated as making S5-A external pilot inputs available or validated. |
| S5-D route decision reopening S5-C or the public close-case endpoint | HOLD if any route implies case workflow changes, close-case endpoint work, ticketing, workflow engine, sign-off workflow, alert routing, or response automation. |
| S5-D route decision changing S4-A host identity authority or resolver order | HOLD if route language changes `AssetInventorySnapshot` authority or `asset_id -> hostname -> fqdn -> ip_address -> aliases`. |
| S5-D route decision changing AI_COLLAB operating model or contract files | HOLD if this checkpoint modifies or synchronizes AI_COLLAB operating model or contract files. |
| choosing a high-risk route without explicitly marking `requires_external_review` implications | HOLD if a policy, evidence, closeout, real external evidence/access, or identity-boundary route omits external-review implications. |

## 7. Candidate Routes

| Candidate route | What it would mean | Why it might be considered | Main risk | External review implication | HOLD trigger | Recommended |
| --- | --- | --- | --- | --- | --- | --- |
| `OPEN_S5_D_5_REDACTION_POLICY_CANDIDATE` | Open a later docs-only candidate that discusses possible redaction policy boundaries. | S5-D-4 surfaced redaction wording and synthetic/redacted label ambiguity. | Policy-candidate language may be mistaken for policy freeze or implementation. | Must re-evaluate; set `requires_external_review=true` if the ticket freezes, changes, or approves redaction boundaries, and likely at closeout if policy acceptance is attempted. | HOLD if the route freezes redaction policy, mask patterns, required fields, algorithms, runtime behavior, or evidence approval. | No. |
| `OPEN_S5_D_5_EVIDENCE_RETENTION_POLICY_CANDIDATE` | Open a later docs-only candidate that discusses possible evidence-retention policy boundaries. | S5-D-4 identified retention, deletion/expiry, storage, replay, and evidence-pack ambiguity. | Highest risk of being read as evidence retention approval. | Must re-evaluate; set `requires_external_review=true` if the ticket freezes, changes, or approves evidence retention, deletion/expiry, storage/replay, evidence-pack, or real evidence handling boundaries. | HOLD if real telemetry evidence retention, retention duration, deletion policy, storage, replay, audit retention, or evidence-pack behavior is approved. | No. |
| `OPEN_S5_D_5_SYNTHETIC_EXAMPLE_BOUNDARY_REFINEMENT` | Open a later docs-only refinement focused only on synthetic-example wording and non-payload boundaries. | It may be lower risk than policy candidates if product wants one more clarity pass. | Even synthetic wording could drift into fixture format, schema, or redaction policy. | Usually false for draft if strictly wording-only; must set `requires_external_review=true` if it changes redaction/secret/evidence-retention boundaries or freezes schema/normalization semantics. | HOLD if synthetic examples become fixture files, schema contracts, tests, payload handling, or policy acceptance. | Not as default; possible only after human route decision. |
| `OPEN_S5_D_DISCOVERY_REVIEW_PASS` | Open a stream-level review pass to accept or park the S5-D discovery baseline. | S5-D has accumulated bounded discovery artifacts and may be ready to park. | Stream closeout can be misread as implementation or external pilot readiness. | Requires `requires_external_review=true` because stream/milestone closeout is an AI_COLLAB trigger. | HOLD if review pass authorizes implementation, policy freeze, evidence retention, external pilot readiness, or bypasses external review. | Not automatic; possible after human route decision. |
| `RETURN_TO_EXTERNAL_INPUT_COLLECTION` | Return focus to collecting governed external input categories without claiming readiness. | S5-A remains `NOT_READY` / `UNKNOWN`; real external inputs may unblock product decisions later. | External input collection may accidentally accept real evidence or imply pilot readiness. | False if planning-only; true if real external evidence/access, pilot/customer/operator evidence, redaction/retention boundary changes, or sign-off decisions appear. | HOLD if real external access, raw payloads, sign-off, evidence retention, or external pilot execution is implied. | Possible, but not selected by this checkpoint. |
| `KEEP_PLANNING_ONLY` | Park active S5-D movement and keep planning-only until human product/governance direction is available. | Safest if product inputs are missing and boundary risks are high. | Stagnation or loss of decision momentum. | False if no stream closeout, policy freeze, evidence handling, or semantic changes occur. | HOLD if planning-only is treated as stream closeout, pilot readiness, or implementation authorization. | Safe fallback, but not the primary verdict. |
| `S5_C_RUNTIME_IMPLEMENTATION_DECISION` | Shift to deciding whether S5-C runtime work should open. | Product may ask to revisit parked case workflow work. | Reopens a parked stream by inertia and could open public endpoint/runtime changes prematurely. | Must re-evaluate; true if case lifecycle semantics, runtime/API/schema/test changes, or stream/milestone closeout are included. | HOLD if S5-C PASS is treated as runtime authorization or public close-case endpoint work begins. | No. |
| `PRODUCT_GOVERNANCE_ROUTE_DECISION_REQUIRED` | Require a later human product/governance decision to choose the next route after S5-D-4. | S5-D-4 touches the highest-risk boundary area, so automatic continuation would be unsafe. | Decision deferral can slow progress if not followed by a concrete ticket. | False for this route-decision draft because it compares routes only; later selected route must carry its own external-review decision. | HOLD if this verdict is treated as authorizing any specific next route without a separate governed ticket. | Yes. |

## 8. Route Comparison Matrix

| Route | Safety posture | Work type if later selected | External-review posture | Why not automatic |
| --- | --- | --- | --- | --- |
| `OPEN_S5_D_5_REDACTION_POLICY_CANDIDATE` | High-risk | Docs-only policy-candidate discussion only | `requires_external_review=true` if boundary freeze/change/approval appears | Redaction policy language can become policy freeze. |
| `OPEN_S5_D_5_EVIDENCE_RETENTION_POLICY_CANDIDATE` | Highest-risk | Docs-only policy-candidate discussion only | `requires_external_review=true` if retention/deletion/evidence handling freeze/change/approval appears | Evidence retention can imply real data handling approval. |
| `OPEN_S5_D_5_SYNTHETIC_EXAMPLE_BOUNDARY_REFINEMENT` | Lower-risk if strictly wording-only | Docs-only refinement only | Usually false for draft; true if boundaries or semantics change | Still can drift into fixture/schema/policy language. |
| `OPEN_S5_D_DISCOVERY_REVIEW_PASS` | Medium-to-high | Stream review / parking decision only | `requires_external_review=true` because stream closeout is a trigger | Review pass can be misread as implementation readiness. |
| `RETURN_TO_EXTERNAL_INPUT_COLLECTION` | Medium | External input planning/collection decision only | True if real external evidence/access or retention/redaction decisions appear | Could be misread as external pilot readiness. |
| `KEEP_PLANNING_ONLY` | Low | Planning pause / no new artifact by default | False if no trigger appears | Safe but may stagnate without human direction. |
| `S5_C_RUNTIME_IMPLEMENTATION_DECISION` | High | Separate product/runtime decision only | True if runtime/API/schema/test or case semantics are in scope | S5-C remains parked and should not reopen by inertia. |
| `PRODUCT_GOVERNANCE_ROUTE_DECISION_REQUIRED` | Conservative | Later human route decision only | False for this comparison draft | It chooses governance sequencing, not product work. |

## 9. External Review Implications
- This route-decision draft has `requires_external_review=false initially` because it compares routes only and does not close S5-D, freeze semantics, accept real evidence, change S4-A authority, or modify redaction/secret/evidence-retention boundaries.
- Any stream/milestone closeout candidate, including `OPEN_S5_D_DISCOVERY_REVIEW_PASS`, requires `requires_external_review=true` if selected.
- Any route that freezes, changes, or approves redaction, secret handling, evidence retention, deletion/expiry, evidence packaging, real telemetry handling, or raw payload handling requires `requires_external_review=true` if selected.
- Any route that freezes telemetry normalization, timestamp/freshness semantics, provenance/confidence trust precedence, source authority, or telemetry schema must re-evaluate `requires_external_review` and set it true if semantics are frozen or changed.
- Any route that changes S4-A identity authority, resolver behavior, or trust precedence must set `requires_external_review=true` and should generally HOLD unless explicitly governed by a separate scoped ticket.
- Real external evidence/access, customer/operator evidence, external pilot access, or sign-off decisions require `requires_external_review=true`.
- External review does not replace human go/no-go.
- Routine docs-only comparison work does not require external review unless one of the trigger categories appears.

## 10. Recommended Route
Recommended route: `PRODUCT_GOVERNANCE_ROUTE_DECISION_REQUIRED`.

After S5-D-4, the safest next step is a human product/governance route decision choosing among:
- parking S5-D discovery
- preparing a stream review pass with `requires_external_review=true`
- opening another docs-only low-risk refinement
- explicitly opening a high-risk policy-candidate path with `requires_external_review` implications
- returning to external input collection without claiming pilot readiness

This is a conservative route-selection verdict only. It does not recommend implementation, redaction policy freeze, evidence retention approval, external pilot execution, or stream/milestone closeout as automatically authorized.

## 11. Why Not The Other Routes
- `OPEN_S5_D_5_REDACTION_POLICY_CANDIDATE` is not selected automatically because redaction policy language can become policy freeze unless the later ticket is carefully scoped and external-review implications are explicit.
- `OPEN_S5_D_5_EVIDENCE_RETENTION_POLICY_CANDIDATE` is not selected automatically because evidence retention is the highest-risk boundary and could be mistaken for permission to retain real telemetry evidence.
- `OPEN_S5_D_5_SYNTHETIC_EXAMPLE_BOUNDARY_REFINEMENT` may be viable, but only if a human route decision prefers another low-risk wording pass over parking or review.
- `OPEN_S5_D_DISCOVERY_REVIEW_PASS` may be viable, but it is stream closeout and therefore requires `requires_external_review=true`; this draft must not perform that closeout.
- `RETURN_TO_EXTERNAL_INPUT_COLLECTION` may be useful, but it must not imply external pilot readiness or real evidence acceptance.
- `KEEP_PLANNING_ONLY` is safe but risks stagnation unless paired with a human decision about what condition would restart work.
- `S5_C_RUNTIME_IMPLEMENTATION_DECISION` is premature from this checkpoint because S5-C remains parked, the public close-case endpoint remains `KEEP_DEFERRED`, and S5-D route selection should not reopen S5-C by inertia.

## 12. HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This checkpoint is treated as implementation authorization. | The artifact compares routes only. |
| Runtime/API/schema/test/dependency changes appear. | No implementation behavior is authorized. |
| Fixture files are created or modified. | No fixture work is in scope. |
| Live SIEM/EDR/source/telemetry access is required. | No real access is authorized. |
| Credentials, tokens, API keys, auth headers, cookies, or secret material appear. | Secret material remains prohibited. |
| Raw telemetry payloads, raw logs, screenshots, exports, event bodies, or customer/operator evidence appear. | Raw or real evidence is outside this checkpoint. |
| Real telemetry event retention is authorized or implied. | Evidence retention requires a separate governed decision and external-review evaluation. |
| Redaction policy, secrets handling implementation, evidence retention, retention/deletion/expiry, storage/replay, or evidence-pack behavior is frozen or approved. | S5-D-4 identified these as high-risk boundaries requiring separate governance. |
| Telemetry schema, normalization, timestamp/freshness semantics, provenance/confidence trust precedence, or source authority is frozen. | This checkpoint does not freeze telemetry semantics. |
| S4-A host identity authority or resolver priority changes. | S4-A authority and resolver order remain unchanged. |
| S5-C is reopened or public close-case endpoint work appears. | S5-C remains parked and S5-C-4 remains `KEEP_DEFERRED`. |
| External pilot readiness, external pilot execution, or real customer/operator sign-off is implied. | S5-A remains `NOT_READY` / `UNKNOWN`. |
| This checkpoint is treated as S5-D stream/milestone closeout. | Stream/milestone closeout requires a separate ticket and `requires_external_review=true`. |
| A high-risk route is selected without recording external-review implications. | AI_COLLAB trigger-based external review must not be bypassed. |
| `docs/HANDOFF.md`, `releases/release_manifest.json`, `releases/verify_report.json`, AI_COLLAB files, contract files, runtime files, or fixture files are modified. | This is a draft-only one-file task. |

## 13. Preliminary Verdict
Preliminary verdict: `PRODUCT_GOVERNANCE_ROUTE_DECISION_REQUIRED`.

Meaning:
A later human product/governance decision must choose the next route after S5-D-4. This document records the route options and their risks only.

The later decision must name the selected route, exact file scope, `primary_implementor`, `reviewer`, `reviewer_when_cc_implements` if relevant, `requires_external_review` decision, non-goals, acceptance criteria, validation command if relevant, and HOLD criteria.

## 14. Preliminary Verdict Non-Meaning
`PRODUCT_GOVERNANCE_ROUTE_DECISION_REQUIRED` does not authorize:
- S5-D stream review pass
- stream/milestone closeout
- implementation
- policy freeze
- evidence retention
- external review bypass
- runtime/API/schema/test/dependency changes
- fixture creation
- live external access
- credentials or secret handling
- raw telemetry evidence handling
- S4-A authority changes
- S5-C reopening
- public close-case endpoint work
- external pilot readiness or execution

## 15. Acceptance Criteria
This draft is acceptable if:
- exactly one new docs-only route-decision file is created
- the S5-D fixed risk checklist is present and complete
- route-decision-specific risks are present
- all candidate routes are compared with risk and external-review implication
- the recommended route is non-authorizing
- any stream/milestone closeout route is identified as requiring `requires_external_review=true` if selected
- any redaction/secret/evidence-retention boundary change route is identified as requiring `requires_external_review=true` if selected
- no implementation, policy freeze, evidence retention, stream closeout, external pilot readiness, S4-A/S5-C boundary change, or external review bypass is authorized
- S4-A host identity handoff and resolver order are preserved
- S5-C and public close-case endpoint remain parked/deferred
- the `requires_external_review` decision and AI_COLLAB-complete re-evaluation triggers are documented
- HANDOFF and manifest are not modified
