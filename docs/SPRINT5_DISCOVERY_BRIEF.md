# Sprint 5 Discovery Brief

## Goal
Create the Sprint 5 discovery record that evaluates the next product and governance direction after the governed Sprint 4 integrated pilot baseline.

This brief is not the Sprint 5 PRD. It exists to compare candidate directions, surface required inputs, and define the recommended planning sequence before Sprint 5 scope is frozen.

## Baseline
- current governed snapshot: `S4-INTEGRATED-2026-04-13-001`
- governed stage: `Sprint 4 integrated pilot baseline closeout`
- source-of-truth root: `D:\产品设计\New folder`
- Sprint 4 integrated closeout accepts `S4-A / S4-B / S4-C / S4-D` as jointly satisfying the Sprint 4 Delivery Definition.
- current governed baseline is accepted as coherent enough for controlled pilot use.
- current verification evidence records:
  - manifest key files: `PASS`
  - release zip: `PASS`
  - review pack: `PASS`
  - pilot validation: `PASS`
  - tests: `PASS`

## Discovery Scope
- identify the highest-value Sprint 5 product direction after Sprint 4 pilot readiness
- distinguish work that can proceed entirely inside the repository from work that requires external pilot or source-system input
- preserve the accepted Sprint 4 integrated pilot baseline as the planning anchor
- keep collaboration and governance improvements visible without letting them redefine product scope before product discovery is complete

## Non-Goals
- do not declare the Sprint 5 PRD or backlog
- do not start external pilot execution
- do not change runtime contracts, adapter contracts, case lifecycle contracts, or release governance rules
- do not govern `docs/AI_COLLAB_OPERATING_MODEL.md` in this brief
- do not expand Sprint 5 into full enterprise deployment, full data-platform integration, or full workflow/RBAC scope

## Candidate Directions

### S5-A Controlled Pilot Preparation
Prepare the controlled pilot execution package that turns the Sprint 4 integrated pilot baseline into operator-ready pilot materials.

Expected focus:
- pilot execution checklist
- pilot sign-off checklist
- operator evidence capture template
- redacted pilot run log template
- dry-run acceptance criteria against the current `pilot_local` baseline

### S5-B Production Source Mode Expansion
Advance deferred source modes for static-data ingestion, especially `api`, `hybrid`, or a distinct `bundle` behavior, without weakening the accepted Sprint 4 identity authority.

Expected focus:
- source-mode contract refinement
- source adapter input and failure semantics
- fixture-backed source-mode tests
- data-sovereignty and refresh expectations
- explicit distinction between repo-local fixture validation and real source integration

### S5-C Analyst / Manager Case Workflow Hardening
Strengthen the persisted case lifecycle surface for pilot analyst and manager use while preserving the non-destructive Sprint 4 case semantics.

Expected focus:
- public close-case API decision
- action-request denial and closure reason granularity
- manager review and approval wording
- audit readability and replayability
- pilot-facing case workflow acceptance tests

### S5-D Telemetry Breadth And Host Selection Scale
Explore telemetry breadth, host-selection scale, and T3 behavior under broader EDR replay or multi-host conditions.

Expected focus:
- host-selection behavior when cache or identity context is sparse
- multi-host replay fixture expansion
- fan-out or queue-readiness discovery without implementing a full async runtime
- partial and degraded semantics under broader telemetry inputs
- continued prevention of vendor-field leakage into T3 or case contracts

### S5-E Governance And Collaboration Operating Model
Review the existing `docs/AI_COLLAB_OPERATING_MODEL.md` draft and decide whether it should be governed so Sprint 5 execution remains stable across VS Code, Codex Web, Claude Code, Claude Web, and the human operator.

This direction is not a from-scratch collaboration redesign. It is a lightweight planning/governance decision about whether the existing draft should be revised and governed through the normal snapshot path.

Expected focus:
- review the existing `docs/AI_COLLAB_OPERATING_MODEL.md` draft
- lightly revise the draft if needed
- decide whether `docs/AI_COLLAB_OPERATING_MODEL.md` should become a governed key file
- structured ticket template decision
- review-only and one-writer-at-a-time rules
- conversation reset and handoff discipline
- governance closure criteria for planning versus implementation work

## Direction Comparison Matrix

| Direction | Goal | Why now | Major risks | Required inputs | Can proceed purely in repo? |
| --- | --- | --- | --- | --- | --- |
| `S5-A Controlled Pilot Preparation` | Convert the integrated pilot baseline into execution, evidence, and sign-off materials for a controlled pilot. | Sprint 4 already accepts the baseline as coherent enough for controlled pilot use; the next gap is operationalizing that acceptance. | Scope may drift into real deployment engineering or external sign-off before inputs are ready. | pilot scope, operator roles, sign-off owner, allowed evidence, pilot run log evidence redaction boundary, target environment assumptions. | Partially. Templates, checklists, dry-run flow, and governed docs can proceed in repo; real pilot evidence requires external inputs. |
| `S5-B Production Source Mode Expansion` | Move beyond the local-file source baseline toward production-shaped `api`, `hybrid`, or distinct `bundle` source behavior. | S4-A deferred these modes, and a real pilot may need live asset, baseline, intel, or topology sources. | Source contracts may expand into a data platform; real systems may introduce auth, schema, freshness, and ownership ambiguity. | target source systems, sample payloads, auth model, refresh expectations, data-sovereignty constraints, failure semantics. | Partially. Contracts, mock transports, fixtures, and tests can proceed in repo; real integration needs external source details. |
| `S5-C Analyst / Manager Case Workflow Hardening` | Improve pilot-facing case workflow completeness for analysts and managers. | S4-C accepted durable lifecycle safety but deferred some workflow surfaces that may matter during pilot usage. | Work may drift into RBAC, ticketing integration, or full workflow-engine design. | analyst and manager journey, close-case requirements, approval roles, denial reason taxonomy, audit review expectations. | Mostly. API contracts, helpers, tests, and docs can proceed in repo if product decisions are available. |
| `S5-D Telemetry Breadth And Host Selection Scale` | Explore broader telemetry replay, host-selection behavior, and scale-readiness before pilot data volume grows. | S4-B accepted current telemetry parity but deferred broader host-selection behavior. | Work may trigger async runtime, queueing, or performance scope before product need is proven. | target telemetry breadth, sample replay sets, expected host-selection policy, performance boundary, partial/degraded expectations. | Partially. Fixtures and contract tests can proceed in repo; realistic breadth needs external samples. |
| `S5-E Governance And Collaboration Operating Model` | Review the existing collaboration-model draft, lightly revise it if needed, and decide whether to govern it. | Sprint 5 will likely cross planning, pilot prep, review, and implementation; stable collaboration rules reduce tool contention. | Process governance may distract from product discovery or accidentally redefine product scope. | decision on governing `docs/AI_COLLAB_OPERATING_MODEL.md`, ticket-template scope, review ownership, snapshot transition expectations. | Yes. This can proceed entirely in repo as governance documentation if explicitly selected. |

## Recommended Priority
1. first: `S5-A Controlled Pilot Preparation`
2. parallel/lightweight: `S5-E Governance And Collaboration Operating Model`
3. second depending on pilot-prep dry-run feedback or explicit product decision: `S5-C Analyst / Manager Case Workflow Hardening`
4. discovery only until external inputs exist: `S5-B Production Source Mode Expansion`
5. discovery only until external inputs exist: `S5-D Telemetry Breadth And Host Selection Scale`

## Required External Inputs
- controlled pilot scope and success criteria
- pilot operator, analyst, manager, and sign-off roles
- acceptable evidence capture and pilot run log evidence redaction boundary for pilot execution
- target environment assumptions beyond `pilot_local`, if any
- production source-system candidates and sample payloads for any `S5-B` work
- broader telemetry samples or expected host-selection policies for any `S5-D` work
- product decision on whether Sprint 5 should optimize for pilot preparation, case workflow hardening, source expansion, or telemetry breadth first

## Pure Repo Work Candidates
- draft a controlled pilot preparation checklist and dry-run evidence template
- draft a pilot sign-off checklist based on the current integrated baseline
- create a Sprint 5 structured ticket template if selected by planning
- evaluate whether to govern `docs/AI_COLLAB_OPERATING_MODEL.md` as a separate planning/governance task
- define source-mode contracts and fixture-only validation without real external credentials
- define case workflow hardening contracts and tests once product decisions are available
- expand replay fixtures only with synthetic or already-governed data

## Governance Considerations
- `docs/AI_COLLAB_OPERATING_MODEL.md` remains an ungoverned local draft.
- whether to govern `docs/AI_COLLAB_OPERATING_MODEL.md` must be an explicit Sprint 5 planning decision.
- collaboration governance should support Sprint 5 execution, but it should not change governed product scope before product discovery confirms the Sprint 5 direction.
- if the operating model is governed, it should be added through the normal snapshot path: `docs/HANDOFF.md`, `releases/release_manifest.json`, regenerated `releases/verify_report.json`, release packaging, and review-pack verification.
- Sprint 5 planning should continue to treat Git plus governed repo artifacts as source of truth; chat history remains coordination context only.

## Preliminary Recommendation
Create this discovery brief first, then confirm the Sprint 5 direction before writing `docs/SPRINT5_PRD.md`.

The recommended planning path is:
- use `S5-A Controlled Pilot Preparation` as the default first Sprint 5 product direction
- treat `S5-E Governance And Collaboration Operating Model` as a lightweight parallel governance decision, not a product-scope blocker
- keep `S5-B` and `S5-D` at discovery depth until external source or telemetry inputs exist
- use pilot-prep dry-run feedback or an explicit product decision to decide whether `S5-C` should become the second implementation stream

## Next Step
- run a review-only pass against this discovery brief
- decide whether to govern `docs/AI_COLLAB_OPERATING_MODEL.md` before or during Sprint 5 PRD work
- confirm the selected Sprint 5 direction
- draft `docs/SPRINT5_PRD.md` only after direction confirmation
