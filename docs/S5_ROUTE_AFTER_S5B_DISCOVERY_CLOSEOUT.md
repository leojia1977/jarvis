# Sprint 5 Route After S5-B Discovery Closeout

## Document Control
- Title: Sprint 5 Route After S5-B Discovery Closeout
- Baseline: `S5-B-DISCOVERY-2026-04-15-006`
- Source of truth: `D:\产品设计\New folder`
- Status: Draft for review
- Scope: Sprint 5 route-selection checkpoint only
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code / human-supervised repo writer
- `reviewer`: Claude Code review-only
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: false for draft; re-evaluate at closeout or if milestone/stream closeout or semantics freeze occurs

## Goal
S5-B discovery is now parked as a governed discovery baseline. This checkpoint reviews the current Sprint 5 state after that closeout and recommends the safest next route.

This checkpoint does not authorize implementation, runtime/API/schema/test/dependency changes, real source or telemetry access, source adapter changes, telemetry adapter changes, external pilot execution, real customer/operator sign-off, S4-A identity authority changes, S5-C reopening, or public close-case endpoint work.

## Non-Goals
- implementation
- source adapter or telemetry adapter implementation
- runtime/API/schema/test/dependency changes
- real source-system, SIEM, EDR, or telemetry access
- credentials, auth headers, tokens, or API keys
- raw customer/operator/source/telemetry payloads
- live refresh, sync, polling, queue, or fan-out behavior
- alert routing
- response automation
- CMDB sync
- multi-tenant ownership or RBAC
- S4-A identity authority or resolver changes
- S5-C reopening
- public close-case endpoint work
- declaring the external pilot package `READY`
- external pilot execution or real customer/operator sign-off
- modifying `docs/AI_COLLAB_OPERATING_MODEL.md`

## Current Governed State
- Active baseline is `S5-B-DISCOVERY-2026-04-15-006`.
- `docs/S5B5_SOURCE_INPUT_DISCOVERY_REVIEW_PASS.md` records the S5-B stream verdict as `PASS_AND_PARK_S5_B_DISCOVERY`.
- S5-B accepted outputs are discovery baseline only: gap matrix, synthetic fixture shape, non-freezing source identifier mapping decision, freshness/provenance contract candidates, HOLD triggers, and evidence boundaries.
- S5-C remains parked, and `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` keeps the public close-case HTTP endpoint at `KEEP_DEFERRED`.
- `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md` keeps the external pilot package at `NOT_READY` because all seven external pilot input categories remain `UNKNOWN`.
- S4-A identity authority remains unchanged: `AssetInventorySnapshot` remains the current host identity seed, and resolver priority remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- `docs/AI_COLLAB_OPERATING_MODEL.md` governs next-ticket fields, single-writer discipline, reviewer separation, human go/no-go, and trigger-based external review.

## Stream State Matrix

| Stream | Current governed evidence | Current state | What is accepted | What remains blocked | Safe next route | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- |
| S5-A external pilot input path | `docs/S5_EXTERNAL_PILOT_INPUT_INTAKE.md`; `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md`; `docs/S5_EXTERNAL_PILOT_DECISION_CHECKPOINT.md`; HANDOFF. | External pilot package remains `NOT_READY` / `UNKNOWN`. | Intake and assessment structure for seven required external pilot inputs. | External pilot decision package, external pilot execution, real sign-off, real access, real evidence retention. | Continue external input collection in parallel if product/governance has owners. | Any attempt to mark pilot package `READY` while required inputs remain `UNKNOWN`. |
| S5-B source/input discovery | `docs/S5B_BOUNDED_SOURCE_INPUT_DISCOVERY.md`; `docs/S5B1_SOURCE_INPUT_GAP_MATRIX.md`; `docs/S5B2_SYNTHETIC_SOURCE_FIXTURE_SHAPE.md`; `docs/S5B3_SOURCE_IDENTIFIER_MAPPING_DECISION.md`; `docs/S5B4_SOURCE_FRESHNESS_PROVENANCE_CONTRACT.md`; `docs/S5B5_SOURCE_INPUT_DISCOVERY_REVIEW_PASS.md`. | `PASS_AND_PARK`; governed discovery baseline only. | Source/input gaps, synthetic fixture shape, non-freezing mapping decision, freshness/provenance candidates, external-review triggers. | Source adapter contract freeze, implementation, fixture files, real source access, S4-A authority changes. | Park S5-B unless product chooses S5-B-4A or external input collection. | S5-B PASS is treated as contract freeze or implementation authorization. |
| S5-C case workflow hardening | `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; `docs/S5C_IMPL4_TEST_HARDENING_REVIEW_PASS.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`. | Planning/contract and test-hardening streams are parked. | S5-C planning/test baseline; public close-case endpoint `KEEP_DEFERRED`. | Runtime implementation by inertia, public close-case endpoint work, S5-C reopening without product decision. | Keep parked unless a later product decision selects a scoped S5-C implementation decision. | S5-C PASS is treated as runtime authorization. |
| S5-D telemetry/external-system discovery | Sprint 5 route docs and S5-B telemetry handoff notes. | Remaining natural discovery stream; not yet opened in this route. | Discovery-only opportunity for telemetry gaps, fixture/contract questions, and external-system boundaries. | Live SIEM/EDR access, raw telemetry payloads, telemetry adapter implementation, queue/fan-out, normalization freeze, performance/SLA commitments, alert routing, response automation, dependencies. | `OPEN_S5_D_BOUNDED_TELEMETRY_DISCOVERY`. | S5-D is opened as live telemetry integration or implementation. |
| AI_COLLAB / governance hygiene | `docs/AI_COLLAB_OPERATING_MODEL.md`; HANDOFF; manifest. | Governed collaboration operating model active. | Primary implementor, reviewer, `reviewer_when_cc_implements`, single-writer lock, human go/no-go, trigger-based external review. | Further AI_COLLAB edits without separate ticket, bypassing external-review triggers. | Apply governed ticket fields to the next route. | Next ticket omits AI_COLLAB fields or bypasses reviewer separation. |
| Release / snapshot hygiene | `docs/HANDOFF.md`; `releases/release_manifest.json`; `releases/verify_report.json`. | Current snapshot verified at S5-B closeout. | Release pack, manifest, review pack, full gate discipline. | Snapshot transition without governed closeout, stale review pack, manifest drift. | Keep normal closeout path for whichever route is selected next. | Work proceeds without manifest/HANDOFF/review-pack alignment when closeout is required. |

## Candidate Next Routes

| Candidate | Meaning | Required inputs | Allowed scope | Not authorized | `requires_external_review` decision | Main risk | HOLD trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `OPEN_S5_D_BOUNDED_TELEMETRY_DISCOVERY` | Open a docs-only S5-D discovery ticket for telemetry/external-system questions. | Current Sprint 5 baselines, S5-B parked state, S4/S5 telemetry boundaries, AI_COLLAB ticket fields. | Discovery questions, gap matrix, synthetic/redacted evidence boundaries, non-authorizing contract sketches. | Telemetry implementation, live SIEM/EDR/source access, queue/fan-out, runtime/API/schema/test/dependency changes. | False for draft if discovery-only; true if telemetry normalization semantics freeze, real external evidence/access, or stream closeout appears. | Discovery language is mistaken for live telemetry integration. | Ticket requires real SIEM/EDR access or queue/fan-out behavior. |
| `OPEN_S5_B_4A_MAPPING_CONTRACT_CANDIDATE` | Draft a focused source identifier mapping contract candidate if product wants mapping language before moving on. | Product/governance reason to deepen S5-B, S4-A identity constraints, S5-B-3 questions. | Docs-only non-implementing mapping candidate. | Mapping freeze, S4-A authority change, resolver behavior change, source adapter implementation. | True if mapping/source semantics are frozen, S4-A authority changes, or real external evidence is accepted; otherwise re-evaluate. | Optional S5-B depth becomes source contract freeze by inertia. | Candidate mapping is treated as approved identity authority. |
| `RETURN_TO_EXTERNAL_INPUT_COLLECTION` | Pause mainline docs work and collect missing S5-A external pilot/source/telemetry inputs. | Named owner, input collection plan, S5-A seven-category checklist. | Intake updates, product/governance questions, redacted request lists. | External pilot execution, real evidence retention without approval, real access, pilot package `READY` claim. | True if real external pilot/customer/operator evidence/access decisions are made. | Collection is treated as sign-off or pilot approval. | Real access, real payloads, or sign-off is implied without governed approval. |
| `KEEP_PLANNING_ONLY` | Park all active product streams and wait for product/governance priority. | Explicit decision to pause or wait. | No-op planning note or next-route hold record. | Implementation, source/telemetry integration, external pilot execution. | False unless used as milestone closeout or semantics decision. | Momentum stalls without owner for next inputs. | Teams proceed from chat-only context despite wait decision. |
| `SPRINT5_MILESTONE_REVIEW` | Review Sprint 5 progress across S5-A/S5-B/S5-C/S5-D and governance state. | Product/governance choice to perform milestone review. | Docs-only milestone review, artifact matrix, PASS/HOLD/NEEDS_DECISION. | Implementation, external pilot, source/telemetry expansion. | True because milestone closeout triggers external review. | Milestone review becomes substitute for scoped next-ticket selection. | Review is used to authorize implementation or pilot readiness. |
| `S5_C_RUNTIME_IMPLEMENTATION_DECISION` | Decide whether parked S5-C should move toward a scoped runtime/API/schema/test implementation ticket. | Explicit product need, exact behavior, exact files, acceptance criteria, test plan, hold/rollback criteria. | Decision document only unless later implementation ticket is approved. | Runtime work, public close-case endpoint work, enterprise RBAC, ticketing, workflow engine, destructive response automation. | True if case lifecycle semantics, public endpoint, or stream/milestone closeout is affected. | S5-C planning/test PASS is mistaken for runtime authorization. | Runtime/API/schema/test changes start from this checkpoint. |

## Recommended Route
Recommendation: `OPEN_S5_D_BOUNDED_TELEMETRY_DISCOVERY`.

Rationale:
- S5-B source/input discovery is now parked.
- S5-C is already parked and should not continue by inertia.
- S5-A remains `NOT_READY` because external inputs are still `UNKNOWN`.
- S5-D is the remaining natural discovery stream and can be bounded to docs, fixtures, and contracts without live EDR/SIEM/telemetry access.
- S5-B-4A mapping contract candidate can remain optional unless product wants to freeze or deepen source mapping semantics.
- S5-C runtime implementation decision remains premature without stronger product need.
- External input collection remains available in parallel but cannot force pilot readiness.

Non-authorization:
- no telemetry implementation
- no live EDR/SIEM access
- no queue/fan-out
- no performance/SLA commitment
- no alert routing
- no response automation
- no runtime/API/schema/test/dependency changes
- no external pilot `READY` claim

## Proposed Next Ticket Shape
If product/governance accepts `OPEN_S5_D_BOUNDED_TELEMETRY_DISCOVERY`, the next ticket should be shaped as follows.

| Field | Proposed value or requirement |
| --- | --- |
| `primary_implementor` | VS Code / human-supervised repo writer, unless explicitly assigned otherwise. |
| `reviewer` | Claude Code review-only. |
| `reviewer_when_cc_implements` | Not applicable unless Claude Code is explicitly assigned primary implementor. |
| `requires_external_review` decision | False for draft if docs-only discovery; set true if telemetry normalization semantics freeze, real external evidence/access, source identity authority changes, or stream/milestone closeout appears. |
| Exact files likely in scope | A new S5-D bounded telemetry discovery doc only; no runtime, tests, fixtures, manifest, or HANDOFF during draft. |
| Discovery questions | Explicitly cover telemetry source categories, event shape / minimum fields, host identity handoff to S4-A, telemetry freshness / timestamp semantics, event provenance / confidence, redaction and secret-handling checklist, fixture-only evidence boundary, no live SIEM/EDR access, no queue/fan-out, no performance/SLA commitment, and no alert routing or response automation. |
| Allowed evidence sources | Governed docs, synthetic examples, redacted shape descriptions, read-only repo inventory, gap matrices, and non-authorizing contract sketches. |
| Non-goals | Live SIEM/EDR/source access, credentials, raw telemetry payloads, queue/fan-out, performance/SLA commitments, alert routing, response automation, runtime/API/schema/test/dependency changes, external pilot execution. |
| Acceptance criteria | Discovery questions listed, evidence boundary explicit, S5-A/S5-B/S5-C boundaries preserved, no implementation authorized, preliminary route bounded. |
| Validation command if relevant | `git status --short`; no full gate for draft unless closeout ticket requests it. |
| HOLD triggers | Real access, credentials, raw payloads, real telemetry event payload retention without separate evidence-retention/redaction approval, queue/fan-out, performance/SLA commitments, alert routing, response automation, runtime changes, external pilot readiness, S4-A authority change, AI_COLLAB rule bypass. |

This is only a proposed ticket shape, not the actual S5-D ticket.

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This checkpoint is treated as implementation authorization. | It is route selection only. |
| S5-D is opened as live telemetry integration. | Recommended route is bounded discovery only. |
| Real SIEM, EDR, source, or telemetry access is required. | No governed real access approval exists. |
| Credentials, auth headers, tokens, API keys, or raw payloads appear. | Discovery must not collect secrets or raw external evidence. |
| Real telemetry event payloads are retained, or real telemetry evidence is collected, without separate evidence-retention and redaction approval. | Evidence retention and redaction approval remain separate governed requirements before any real telemetry evidence can be accepted. |
| Queue, fan-out, or performance commitments appear. | S5-D route is not runtime architecture implementation. |
| Alert routing or response automation appears. | S5-D discovery must not become operational routing or response behavior. |
| Runtime/API/schema/test/dependency changes appear. | This checkpoint authorizes no implementation changes. |
| S5-B PASS is treated as contract freeze or implementation authorization. | S5-B is parked as discovery baseline only. |
| S5-C PASS is treated as runtime authorization. | S5-C remains parked. |
| Public close-case endpoint is opened. | S5-C-4 remains `KEEP_DEFERRED`. |
| External pilot `READY`, execution, or real sign-off is implied. | S5-A remains `NOT_READY` / `UNKNOWN`. |
| S4-A identity authority changes. | S4-A authority remains unchanged. |
| AI_COLLAB rules are bypassed. | Next tickets must preserve primary implementor, reviewer, single-writer, human go/no-go, and external-review triggers. |

## Preliminary Verdict
Verdict: `RECOMMEND_OPEN_S5_D_BOUNDED_TELEMETRY_DISCOVERY`.

Allowed preliminary verdict values:
- `RECOMMEND_OPEN_S5_D_BOUNDED_TELEMETRY_DISCOVERY`
- `RECOMMEND_OPEN_S5_B_4A_MAPPING_CONTRACT_CANDIDATE`
- `RECOMMEND_EXTERNAL_INPUT_COLLECTION`
- `RECOMMEND_KEEP_PLANNING_ONLY`
- `NEEDS_PRODUCT_DECISION`
- `HOLD`

## Acceptance Criteria
This draft is acceptable when:
- S5-B `PASS_AND_PARK` is reviewed
- S5-C parked status and public close-case endpoint `KEEP_DEFERRED` status are preserved
- S5-A `NOT_READY` / `UNKNOWN` status is preserved
- S5-D is recommended only as bounded discovery
- no implementation, live telemetry, queue/fan-out, runtime/API/schema/test/dependency change is authorized
- no real telemetry event retention occurs without separate evidence-retention and redaction approval
- no performance/SLA commitment is authorized
- no alert routing or response automation is authorized
- next-ticket shape includes AI_COLLAB governed fields
- external pilot execution and real customer/operator sign-off remain unauthorized
- preliminary verdict is one of the allowed values
