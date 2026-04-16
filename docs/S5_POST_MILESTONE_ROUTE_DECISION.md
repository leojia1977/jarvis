# Sprint 5 Post-Milestone Route Decision

## 1. Document Control
- Title: Sprint 5 Post-Milestone Route Decision
- Status: Closed as governed Sprint 5 post-milestone route decision baseline
- Date: 2026-04-16
- Baseline snapshot: `S5-MILESTONE-REVIEW-PASS-2026-04-15-001`
- Baseline stage: `s5-sprint5-milestone-review-pass`
- Baseline commit: `b8d35fee8ce4d8fc39ce6ef9d514a876d742fb08`
- Prior artifact: `docs/S5_SPRINT5_MILESTONE_REVIEW_PASS.md`
- Scope: docs-only Sprint 5 post-milestone route-selection decision
- Owner: Human-governed Sprint 5 planning
- `primary_implementor`: VS Code
- `reviewer`: Claude Code
- `reviewer_when_cc_implements`: not applicable
- `requires_external_review`: true

## 2. Goal
This document drafts a governed docs-only Sprint 5 post-milestone route decision after `SPRINT5_BASELINE_REVIEW_PASS_WITH_EXTERNAL_INPUTS_PENDING`.

The goal is to compare candidate next routes, record that external pilot inputs remain pending / `NOT_READY` / `UNKNOWN`, and recommend the safest next direction without treating the Sprint 5 milestone pass as an automatic route authorization.

This document is a route-selection decision only. It is not an implementation ticket, external pilot decision package, external pilot readiness package, runtime/API/schema/test/dependency ticket, fixture ticket, public close-case endpoint ticket, S5-B or S5-D reopen ticket, S5-C implementation ticket, or AI_COLLAB amendment ticket.

## 3. Non-Goals
This route decision does not authorize:

- external pilot execution
- external pilot readiness claims
- external pilot decision package
- real customer/operator sign-off
- real SIEM/EDR/source/telemetry access
- connector credentials, tokens, API keys, auth headers, cookies, or secret material
- raw telemetry/source payloads, logs, screenshots, exports, event bodies, or customer/operator evidence
- evidence retention
- redaction policy freeze
- secrets handling implementation
- runtime/API/schema/test/dependency changes
- fixture file creation or modification
- public close-case endpoint work
- S5-C runtime implementation
- S5-B or S5-D reopen
- S5-B source adapter contract freeze
- S5-B identity/source mapping freeze
- S5-D telemetry schema/normalization/freshness/provenance/redaction/retention freeze
- S4-A resolver priority changes
- AI_COLLAB operating model or contract changes
- external review bypass
- automatic next route beyond this route decision
- `docs/HANDOFF.md` updates during this draft-only stage
- `releases/release_manifest.json` updates during this draft-only stage

## 4. Current Governed Baseline
- Active baseline snapshot is `S5-MILESTONE-REVIEW-PASS-2026-04-15-001`.
- Active baseline stage is `s5-sprint5-milestone-review-pass`.
- Baseline commit is `b8d35fee8ce4d8fc39ce6ef9d514a876d742fb08`.
- Current milestone verdict is `SPRINT5_BASELINE_REVIEW_PASS_WITH_EXTERNAL_INPUTS_PENDING`.
- The Sprint 5 milestone verdict parks governed baselines and does not authorize an automatic next route.
- S5-A Controlled Pilot Preparation is governed, but external pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- Real customer/operator sign-off remains unauthorized.
- S5-B Source/Input Discovery is `PASS_AND_PARK`.
- S5-D Telemetry Discovery is `PASS_AND_PARK`.
- S5-C is a governed planning/contract baseline; public close-case endpoint remains `KEEP_DEFERRED`.
- S5-E / AI_COLLAB governance is complete as collaboration workflow guidance only.
- S4-A host identity authority remains unchanged.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.

S5-C-3 status correction:

- `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md` is already recorded by `docs/HANDOFF.md` and `releases/release_manifest.json` as a governed contract/planning artifact.
- The S5-C-3 file header may still say `Draft for review`, but HANDOFF, manifest, and later S5-C / Sprint 5 governance records are the controlling governance evidence.
- Treat the S5-C-3 file-header mismatch as documentation hygiene only, not as an unmet precondition for S5-C scoped implementation decision prep.
- This draft does not modify S5-C-3.

## 5. requires_external_review Rationale
`requires_external_review` is true because this is a post-milestone direction-setting route decision after the Sprint 5 milestone review pass.

The candidate routes include external pilot input tracking, possible external-input collection, possible S5-C scoped implementation decision prep, possible S5-B/S5-D reopen decisions, and other routes with external-review implications. Any later route that changes pilot readiness semantics, case lifecycle semantics, source identity authority, telemetry normalization, redaction/secret/evidence-retention boundaries, real external evidence/access decisions, or stream/milestone closeout must carry its own `requires_external_review` decision.

External review for this route decision does not authorize implementation and does not replace human go/no-go.

## 6. Fixed Post-Milestone Risk Checklist
Any item below becoming authorized or implied is a HOLD condition.

| Risk category | HOLD trigger |
| --- | --- |
| external pilot execution | HOLD if this route decision starts, schedules, approves, or implies external pilot execution. |
| external pilot readiness misread as improved | HOLD if the milestone pass or this route decision is treated as moving external inputs from `UNKNOWN` / `NOT_READY` toward readiness. |
| real customer/operator sign-off | HOLD if this route decision creates or accepts real sign-off. |
| real SIEM/EDR/source/telemetry access | HOLD if live external-system access is required, approved, or implied. |
| connector credentials / tokens / API keys / auth headers / cookies | HOLD if credentials, tokens, API keys, auth headers, cookies, or secret material are requested, stored, pasted, inferred, or retained. |
| raw telemetry/source payloads, logs, screenshots, exports, event bodies, or customer/operator evidence | HOLD if real payloads, logs, screenshots, exports, event bodies, or customer/operator evidence are introduced as route evidence. |
| evidence retention or redaction policy freeze | HOLD if evidence retention, deletion, expiry, storage, redaction, or retention policy is approved or frozen. |
| secrets handling implementation | HOLD if this route decision implies credential workflow, vault, scanner, masking, or other secrets-handling implementation. |
| runtime/API/schema/test/dependency changes | HOLD if runtime, API, schema, test, dependency, or release-tooling changes are authorized. |
| fixture file creation or modification | HOLD if fixture files are created, modified, or authorized. |
| public close-case endpoint work | HOLD if public close-case endpoint work is opened or `KEEP_DEFERRED` is weakened. |
| S5-C runtime implementation without scoped decision | HOLD if S5-C runtime work begins without a later governed scoped implementation decision. |
| S5-B source contract or identity mapping freeze | HOLD if S5-B parked discovery becomes a frozen source contract, adapter contract, or identity/source mapping freeze. |
| S5-D telemetry schema/normalization/freshness/provenance/redaction/retention freeze | HOLD if S5-D parked discovery becomes telemetry schema, normalization, freshness, provenance, redaction, or retention policy. |
| S4-A host identity handoff bypass or resolver priority change | HOLD if S4-A `AssetInventorySnapshot` authority or resolver order changes. |
| AI_COLLAB operating model or contract changes | HOLD if this route modifies or synchronizes AI_COLLAB files. |
| automatic next route without human product/governance decision | HOLD if this document starts follow-up work without a later scoped ticket. |
| reopening S5-B or S5-D without explicit reopen decision | HOLD if S5-B or S5-D resumes from parking without explicit reopen decision and review. |

## 7. Route-Decision-Specific Risk Checklist
Any item below becoming authorized, frozen, or implied is a HOLD condition.

| Route-decision risk | HOLD trigger |
| --- | --- |
| route decision being mistaken for implementation authorization | HOLD if the selected route is treated as permission to implement code, tests, runtime, API, schema, dependencies, fixtures, adapters, or release tooling. |
| route decision being mistaken for external pilot readiness | HOLD if the route is treated as resolving the seven external pilot input categories. |
| route decision being mistaken for external pilot decision package | HOLD if the route starts or replaces the external pilot decision package. |
| route decision being mistaken for S5-C runtime authorization | HOLD if S5-C planning baseline is treated as runtime authorization. |
| route decision being mistaken for public close-case endpoint authorization | HOLD if public close-case endpoint work appears or `KEEP_DEFERRED` is weakened. |
| route decision being mistaken for S5-B or S5-D reopen authorization | HOLD if source/input or telemetry discovery resumes without explicit reopen decision. |
| route decision being mistaken for policy or contract freeze | HOLD if the route freezes S5-B contracts, S5-D telemetry/policy boundaries, S5-C case behavior, redaction, secrets, or evidence retention. |
| route decision being mistaken for real external-system access approval | HOLD if real SIEM, EDR, source, telemetry, customer, or operator access is approved or implied. |
| route decision being mistaken for evidence retention approval | HOLD if real evidence collection, storage, retention, deletion/expiry, replay, or evidence-pack behavior is approved. |
| route decision bypassing external review | HOLD if `requires_external_review` is removed, skipped, or treated as optional for this route decision. |
| route decision replacing human go/no-go | HOLD if reviewer output replaces human product/governance route authority. |
| route decision changing S4-A identity authority or resolver order | HOLD if S4-A authority or `asset_id -> hostname -> fqdn -> ip_address -> aliases` changes. |
| route decision changing AI_COLLAB operating model or contract files | HOLD if this route edits or synchronizes AI_COLLAB operating model or contract files. |
| route decision creating an automatic next route beyond the selected recommendation | HOLD if later work begins without a separate governed ticket and human go/no-go. |

## 8. Candidate Routes
The candidate routes compared here are:

| Route | Candidate name | Route class |
| --- | --- | --- |
| A | `OPEN_EXTERNAL_INPUT_TRACKER` | Docs-only tracker / decision artifact |
| B | `OPEN_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP` | Docs-only scoped implementation decision prep |
| C | `KEEP_PLANNING_ONLY_WITH_RESTART_CRITERIA` | Safe fallback / planning hold |
| D | `RETURN_TO_EXTERNAL_INPUT_COLLECTION` | External stakeholder input collection path |
| E | `OPEN_EXTERNAL_PILOT_DECISION_PACKAGE` | External pilot decision package path |
| F | `REOPEN_S5_B_DISCOVERY` | Source/input discovery reopen path |
| G | `REOPEN_S5_D_DISCOVERY` | Telemetry discovery reopen path |
| H | `S5_C_RUNTIME_IMPLEMENTATION_DIRECT` | Direct implementation path |

## 9. Route Comparison Matrix
| Route | Meaning | Preconditions | Current precondition status | Main risk | `requires_external_review` implications | HOLD triggers | Recommended? | Non-authorization notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. `OPEN_EXTERNAL_INPUT_TRACKER` | Open a docs-only tracker/decision artifact for the seven external pilot input categories, owners, channels, timeout/restart criteria, escalation path, and HOLD conditions. | Governed external pilot input categories exist; milestone pass confirms inputs remain pending; tracker scope is docs-only. | Met for tracker drafting; all seven categories remain `UNKNOWN` and package remains `NOT_READY`. | Tracker could be mistaken for input completion or pilot readiness. | True for this route decision; later tracker must re-evaluate if it accepts real external evidence/access, changes evidence retention/redaction boundaries, or changes pilot readiness semantics. | HOLD if any input is declared `READY`, tracker becomes external pilot decision package, or real evidence retention/access is authorized. | Recommended as part of next direction. | Does not declare any input ready, does not become external pilot package, and does not authorize pilot execution or real evidence retention. |
| B. `OPEN_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP` | Open a docs-only scoped decision artifact to decide which already-governed S5-C contract clauses may later enter implementation tickets and which remain HOLD. | S5-C planning/contract baseline is governed, including S5-C-3; public close-case endpoint remains `KEEP_DEFERRED`; implementation decision prep is docs-only. | Met for decision-prep drafting; S5-C-3 header mismatch is documentation hygiene only and not a blocker. | Decision prep could be mistaken for runtime implementation or endpoint authorization. | True for this route decision; later decision prep must set its own trigger-based value, especially if case lifecycle semantics, evidence handling, or contracts are frozen/changed. | HOLD if exact clauses/files/tests are skipped, implementation starts directly, public close-case endpoint opens, external pilot execution appears, or real external access appears. | Recommended as part of next direction. | Does not implement anything and must require later exact files, behavior changes, tests, acceptance criteria, redaction/secret/evidence boundaries, `KEEP_DEFERRED` endpoint preservation, and its own external-review decision. |
| C. `KEEP_PLANNING_ONLY_WITH_RESTART_CRITERIA` | Park all next work and define restart criteria for when external inputs, S5-C product decision, or implementation need becomes concrete. | Human product/governance can accept planning-only pause and define restart triggers. | Safe but incomplete; no restart criteria have been drafted yet. | Sole planning route could create stagnation and leave external inputs unowned. | Usually false for routine planning unless it changes milestone/stream closeout, pilot readiness, evidence/access, or contract semantics. | HOLD if planning-only is used to avoid required owner/timeout/escalation decisions. | Safe fallback only; not recommended as sole route. | Does not authorize implementation, pilot package, or readiness; if selected, must define restart criteria. |
| D. `RETURN_TO_EXTERNAL_INPUT_COLLECTION` | Resume collection of external pilot inputs from stakeholders. | External stakeholders are available; channel, owner, requested evidence, redaction, retention, and go/no-go boundaries are explicit. | Not met as sole route; current repo evidence still shows all seven categories `UNKNOWN`. | Collection could drift into real evidence retention or false readiness. | True if real external evidence/access decisions or redaction/secret/evidence-retention boundary changes appear. | HOLD if collection accepts raw payloads, credentials, screenshots/logs, real evidence retention, or claims readiness. | Not recommended as sole route; can be related to Route A. | Does not imply external pilot readiness and should be governed through a tracker before any package claim. |
| E. `OPEN_EXTERNAL_PILOT_DECISION_PACKAGE` | Draft the explicit external pilot go/no-go decision package. | All seven external pilot input categories are `PROVIDED` or explicitly accepted by product/governance. | Not met; all seven categories remain `UNKNOWN` and package remains `NOT_READY`. | Creates false readiness and may imply pilot start. | True because pilot readiness semantics, real evidence/access, go/no-go, and evidence-retention boundaries are implicated. | HOLD if opened before all required inputs are provided or explicitly accepted. | Not recommended now. | Does not proceed while external inputs remain pending / `NOT_READY` / `UNKNOWN`. |
| F. `REOPEN_S5_B_DISCOVERY` | Reopen S5-B source/input discovery from `PASS_AND_PARK`. | Explicit reopen decision and specific source/input coverage gap discovered through external input process. | Not met; S5-B is parked and no new source/input coverage gap is governed. | Reopen could become source adapter contract freeze or identity mapping freeze. | True if source identity authority, mapping, source contract freeze, real external evidence/access, or stream closeout is implicated. | HOLD if S5-B resumes without explicit reopen decision or if source contract/identity mapping freezes silently. | Not recommended now. | Does not reopen S5-B; trigger only if external input process reveals source/input coverage gap. |
| G. `REOPEN_S5_D_DISCOVERY` | Reopen S5-D telemetry discovery from `PASS_AND_PARK`. | Explicit reopen decision and specific telemetry coverage/normalization gap discovered through external input process. | Not met; S5-D is parked and no new telemetry coverage/normalization gap is governed. | Reopen could freeze telemetry schema, normalization, freshness, provenance, redaction, or retention. | True if telemetry normalization, timestamp/freshness, evidence retention/redaction, real external evidence/access, or stream closeout is implicated. | HOLD if S5-D resumes without explicit reopen decision or if telemetry/policy boundaries freeze silently. | Not recommended now. | Does not reopen S5-D; trigger only if external input process reveals telemetry coverage/normalization gap. |
| H. `S5_C_RUNTIME_IMPLEMENTATION_DIRECT` | Start S5-C runtime implementation directly from existing planning/contract baselines. | A governed scoped implementation decision with exact clauses, files, behavior changes, tests, acceptance criteria, evidence boundaries, and review requirements. | Not met; direct runtime implementation is explicitly outside current route scope. | Bypasses decision prep and converts S5-C PASS into implementation authorization. | True if ever considered, because case lifecycle/contract/runtime semantics and possibly external review triggers are implicated. | HOLD immediately if selected without scoped decision. | Explicitly not recommended. | S5-C PASS is not implementation authorization; direct runtime implementation without scoped decision is HOLD. |

## 10. Recommended Route
Preliminary recommendation: `RECOMMEND_EXTERNAL_INPUT_TRACKER_AND_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP`.

Meaning:

The next governed direction should prepare two bounded follow-up routes:

- External Input Tracker: a docs-only tracker/decision artifact for seven external pilot input categories, owners, channels, timeout/restart criteria, escalation path, and HOLD conditions.
- S5-C Scoped Implementation Decision Prep: a docs-only scoped decision artifact that determines which already-governed S5-C contract clauses may later enter implementation tickets and which clauses remain HOLD.

Why this route is recommended:

- It addresses the most important unresolved milestone fact: external inputs remain pending / `NOT_READY` / `UNKNOWN`.
- It creates ownership and restart structure without pretending the external pilot decision package is ready.
- It lets S5-C move toward a scoped decision artifact without starting implementation.
- It respects that S5-C contract/planning baseline is already governed, including S5-C-3.
- It avoids reopening S5-B or S5-D without a new evidence-triggered reason.
- It preserves S5-C public close-case endpoint `KEEP_DEFERRED`.
- It preserves S4-A identity authority and resolver order.

## 11. Why Not The Other Routes
- `KEEP_PLANNING_ONLY_WITH_RESTART_CRITERIA` is safe as fallback, but not recommended as the sole route because it risks stagnation unless restart criteria are explicit.
- `RETURN_TO_EXTERNAL_INPUT_COLLECTION` is useful only if external stakeholders are available and should be structured through Route A so it does not imply readiness.
- `OPEN_EXTERNAL_PILOT_DECISION_PACKAGE` is not recommended because all seven external pilot input categories remain `UNKNOWN` and current readiness is `NOT_READY`.
- `REOPEN_S5_B_DISCOVERY` is not recommended because S5-B is `PASS_AND_PARK`; reopen requires explicit decision and a source/input coverage gap.
- `REOPEN_S5_D_DISCOVERY` is not recommended because S5-D is `PASS_AND_PARK`; reopen requires explicit decision and a telemetry coverage/normalization gap.
- `S5_C_RUNTIME_IMPLEMENTATION_DIRECT` is explicitly not recommended and is HOLD without a scoped S5-C implementation decision.

## 12. External Review Implications
- This route decision has `requires_external_review=true` because it is a post-milestone direction-setting decision with candidate routes that touch pilot readiness, S5-C implementation prep, external inputs, possible reopen paths, and external-review-triggering boundaries.
- Route A must re-evaluate `requires_external_review` in its own ticket and set it true if it accepts real external evidence/access, changes redaction/secret/evidence-retention boundaries, or changes pilot readiness semantics.
- Route B must re-evaluate `requires_external_review` in its own ticket and set it true if it freezes or changes case lifecycle semantics, evidence handling, contract clauses, runtime/API behavior, or any other AI_COLLAB trigger.
- Routes E, F, G, and H carry high external-review implications and are not recommended now.
- Any later stream/milestone closeout requires `requires_external_review=true`.
- External review does not authorize implementation and does not replace human go/no-go.

## 13. Non-Authorization
`RECOMMEND_EXTERNAL_INPUT_TRACKER_AND_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP` does not authorize:

- implementation
- tests
- runtime/API/schema/dependency changes
- fixture creation or modification
- external pilot execution
- external pilot readiness
- external pilot decision package
- real customer/operator sign-off
- real SIEM/EDR/source/telemetry access
- credentials, tokens, API keys, auth headers, cookies, or secret material
- raw telemetry/source payloads, logs, screenshots, exports, event bodies, or customer/operator evidence
- evidence retention
- redaction policy freeze
- secrets handling implementation
- public close-case endpoint work
- S5-C runtime implementation
- S5-B reopen
- S5-D reopen
- S5-B source contract freeze or identity/source mapping freeze
- S5-D telemetry schema/normalization/freshness/provenance/redaction/retention freeze
- S4-A resolver priority or authority changes
- AI_COLLAB operating model or contract changes
- external review bypass
- automatic next route beyond the selected follow-up drafts

## 14. HOLD Conditions
| HOLD condition | Why it holds |
| --- | --- |
| Any route starts implementation directly. | This is a docs-only route decision, not implementation authorization. |
| External pilot execution, readiness, real sign-off, or real access appears. | External inputs remain pending / `NOT_READY` / `UNKNOWN`. |
| Real evidence, credentials, raw payloads, evidence retention, redaction policy freeze, or secrets handling implementation appears. | No real evidence/access/retention/secrets boundary is approved by this route. |
| Runtime/API/schema/test/dependency or fixture changes appear. | Follow-up routes must be docs-only unless a later scoped implementation ticket explicitly authorizes changes. |
| Public close-case endpoint work appears. | S5-C public close-case endpoint remains `KEEP_DEFERRED`. |
| S5-B or S5-D reopen is implied without explicit reopen decision. | Both streams remain `PASS_AND_PARK` unless a later governed reopen decision is made. |
| S4-A resolver priority or authority changes appear. | S4-A identity authority and resolver order remain unchanged. |
| AI_COLLAB operating model or contract changes appear. | This route decision is not an AI_COLLAB amendment. |
| A new AI_COLLAB amendment is explicitly marked by human product/governance as a prerequisite for this route. | This route must HOLD until that amendment is handled through its own governed path. |
| `docs/HANDOFF.md` or `releases/release_manifest.json` is modified during draft-only stage. | This task may create exactly one new docs-only file. |
| Protected untracked files are touched. | `CLAUDE.md` and `SecuPilot_阶段性总结_20260409.md` are explicitly protected. |

## 15. Final Recommendation
Final recommendation: `RECOMMEND_EXTERNAL_INPUT_TRACKER_AND_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP`.

This means the next governed direction should prepare:

- a docs-only External Input Tracker for the seven external pilot input categories, owners, channels, timeout/restart criteria, escalation path, and HOLD conditions
- a docs-only S5-C Scoped Implementation Decision Prep artifact that maps already-governed S5-C contract clauses to possible later implementation tickets or HOLD outcomes

This recommendation is non-authorizing. It does not start either follow-up ticket by itself, and it does not authorize implementation, tests, runtime/API/schema/dependency changes, fixture creation, external pilot execution, real sign-off, real access, evidence retention, public close-case endpoint work, S5-B/S5-D reopen, S4-A resolver changes, or AI_COLLAB changes.

## 16. Acceptance Criteria
This draft is acceptable if:

- exactly one new docs-only route decision file is created
- `requires_external_review` is true and rationale is documented
- current Sprint 5 baseline is accurately summarized
- S5-C-3 status correction is included and does not authorize modifying S5-C-3
- all eight candidate routes are compared
- recommended route is `RECOMMEND_EXTERNAL_INPUT_TRACKER_AND_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP`
- recommendation is explicitly non-authorizing
- External Input Tracker is not an external pilot decision package
- S5-C Scoped Implementation Decision Prep is not implementation authorization
- S5-B and S5-D remain `PASS_AND_PARK` unless later explicit reopen decision
- S5-C public close-case endpoint remains `KEEP_DEFERRED`
- S4-A resolver order is preserved
- AI_COLLAB operating model and contract files are not modified
- no runtime/API/schema/test/dependency/fixture change is authorized
- HANDOFF and manifest are not modified
