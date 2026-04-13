# Sprint 5 PRD

## Document Control
- Product: `SecuPilot`
- Source of truth: `D:\产品设计\New folder`
- Planning baseline: `S4-INTEGRATED-2026-04-13-001`
- Discovery input: `docs/SPRINT5_DISCOVERY_BRIEF.md`
- Status: draft for review
- Primary owners:
  - Product and review decisions: `Claude`
  - Implementation and release: `Codex`

## Background
Sprint 4 closed the integrated pilot baseline for SecuPilot.

The governed `S4-INTEGRATED-2026-04-13-001` baseline accepts:
- `S4-A` source contracts and identity resolution
- `S4-B` production-facing EDR contract and replay validation
- `S4-C` durable case lifecycle and audit semantics
- `S4-D` pilot-ready operator guidance, release checks, and staging validation

The current baseline is coherent enough for controlled pilot use, and the manifest, release zip, review pack, pilot validation, and test evidence all pass under the integrated Sprint 4 closeout.

Sprint 5 should not reopen the Sprint 4 baseline. It should turn that accepted baseline into controlled pilot preparation materials, while keeping deferred source, telemetry, case workflow, and collaboration-governance decisions explicit and bounded.

## Problem Statement
SecuPilot now has a governed integrated pilot baseline, but it is not yet packaged as a controlled pilot preparation program.

The remaining Sprint 5 planning gaps are:
- pilot preparation needs execution, evidence, dry-run, and sign-off materials before any external pilot activity begins
- collaboration governance exists as an ungoverned local draft and needs an explicit planning decision before it becomes part of governed workflow
- analyst and manager workflow hardening may be useful, but should be triggered by pilot-prep dry-run feedback or an explicit product decision, not assumed external pilot feedback
- production source expansion still lacks external source-system inputs and must remain discovery/contract depth until those inputs exist
- telemetry breadth and host-selection scale still lack external telemetry inputs and must remain discovery/fixture depth until those inputs exist

## Sprint 5 Goal
Prepare SecuPilot for controlled pilot execution without starting the external pilot itself.

Sprint 5 should:
- make `S5-A Controlled Pilot Preparation` the first product direction
- treat `S5-E Governance And Collaboration Operating Model` as a lightweight parallel governance decision
- allow `S5-C Analyst / Manager Case Workflow Hardening` as a second stream only after pilot-prep dry-run feedback or an explicit product decision
- keep `S5-B Production Source Mode Expansion` at discovery/contract depth until external source inputs exist
- keep `S5-D Telemetry Breadth And Host Selection Scale` at discovery/fixture depth until external telemetry inputs exist

## Non-Goals
- external pilot execution
- connecting to real external SIEM, EDR, or source systems
- enterprise RBAC, tenancy, or organization management
- full data platform work or CMDB synchronization
- destructive response execution
- autonomous containment or remediation
- governing `docs/AI_COLLAB_OPERATING_MODEL.md` directly inside this PRD
- rewriting the AI collaboration model from scratch
- implementing live source refresh, multi-tenant data ownership, external authentication, or CMDB sync without a separate product decision
- implementing queueing, fan-out, or async runtime scale work before telemetry breadth inputs justify it

## Target Users
- `Security engineer`: needs a controlled pilot preparation checklist, deterministic dry-run evidence, and clear environment assumptions
- `Operator`: needs pilot-prep instructions that distinguish readiness checks, smoke-path execution, evidence capture, and escalation artifacts
- `L1 analyst`: needs case workflow expectations that remain retrievable, understandable, and non-destructive
- `L2 analyst`: needs source, telemetry, and identity boundaries that remain explicit when pilot preparation expands beyond happy-path dry-runs
- `SOC manager`: needs pilot sign-off criteria, evidence boundaries, and action/approval language that can be reviewed without hidden local knowledge
- `Product/review owner`: needs a clear decision point before Sprint 5 expands into real pilot execution, source-system integration, or broader workflow scope

## Product Principles
1. Pilot preparation precedes pilot execution.
2. Dry-run evidence must be governed, repeatable, and redacted.
3. Pilot run log evidence redaction is distinct from the operator escalation triage redaction already governed by `S4-D-3` and `RELEASE_PROCESS`.
4. Collaboration governance supports product execution; it must not redefine product scope ahead of product discovery.
5. Source and telemetry expansion must stay contract- or fixture-backed until external inputs exist.
6. Analyst and manager workflow hardening may be driven by internal product decisions; it does not require real pilot user feedback.
7. Destructive response execution remains out of scope.

## Scope

### S5-A Controlled Pilot Preparation
Create the controlled pilot preparation package for the accepted Sprint 4 integrated baseline.

In scope:
- pilot preparation checklist
- pilot dry-run checklist
- pilot sign-off checklist
- pilot run log evidence template
- pilot run log evidence redaction boundary
- mapping from `POST /api/v1/pilot-smoke` and `py -3 scripts\git_preflight.py --mode pilot` evidence into pilot-prep acceptance
- explicit separation between dry-run completion and external pilot execution

Out of scope:
- running the external pilot
- changing runtime readiness semantics
- changing the governed smoke path
- collecting real customer or external environment evidence

### S5-E Governance And Collaboration Operating Model
Review the existing `docs/AI_COLLAB_OPERATING_MODEL.md` draft as a lightweight parallel governance decision.

In scope:
- review the existing draft
- lightly revise it if needed
- decide whether it should be governed through the normal snapshot path
- decide whether a structured ticket template is needed for Sprint 5 execution
- confirm one-writer-at-a-time and review-only expectations for Sprint 5 work

Out of scope:
- governing `docs/AI_COLLAB_OPERATING_MODEL.md` directly inside this PRD
- designing collaboration rules from scratch
- materially rewriting the operating model without a separate ticket
- allowing process governance to change Sprint 5 product scope

Execution note:
- if the operating model requires a substantial rewrite, Sprint 5 must open a separate planning/governance ticket before governing it.

### S5-C Analyst / Manager Case Workflow Hardening
Prepare a second product stream for case workflow hardening only if triggered by pilot-prep dry-run feedback or an explicit product decision.

In scope when triggered:
- analyst journey definition
- manager journey definition
- approval roles and review ownership
- public close-case API decision
- close reason and action-request denial reason taxonomy
- audit readability and replayability improvements
- regression tests for accepted workflow changes

Out of scope:
- enterprise workflow engine
- ticketing-system sync
- RBAC, tenancy, or organization management
- destructive or autonomous response approval

Execution note:
- analyst and manager journey definitions, approval roles, and close/denial semantics may come from internal product decisions. They do not need to wait for real external pilot user feedback.
- Hold trigger: if approval role design exceeds the `pilot_local` analyst/manager distinction or touches enterprise RBAC, ticketing, or workflow-engine scope, pause and require an independent product decision before continuing.

### S5-B Production Source Mode Expansion
Keep production source mode work at discovery/contract depth until external source inputs exist.

In scope:
- source-mode discovery for `api`, `hybrid`, and distinct `bundle` behavior
- contract sketches for source adapter inputs and outputs
- fixture-only validation with synthetic or already-governed data
- failure semantics for missing source inputs, unsupported modes, and stale fixture data
- documentation of required external source-system inputs

Out of scope:
- real external source-system connections
- external authentication implementation
- live refresh design
- multi-tenant data ownership
- CMDB synchronization
- replacing the Sprint 4 asset-inventory identity authority

Hold trigger:
- if `S5-B` work touches live refresh design, multi-tenant data ownership, external authentication, or CMDB sync, pause and require an independent product decision before continuing.

### S5-D Telemetry Breadth And Host Selection Scale
Keep telemetry breadth and host-selection scale work at discovery/fixture depth until external telemetry inputs exist.

In scope:
- synthetic or already-governed replay fixture expansion
- host-selection policy discovery for broader replay sets
- partial and degraded behavior review under broader fixture inputs
- explicit protection against vendor-field leakage into T3 or case contracts
- documentation of external telemetry inputs required for deeper work

Out of scope:
- live external EDR/SIEM connectivity
- async queueing or fan-out implementation
- performance-scale commitments without telemetry breadth requirements
- changes that bypass the S4-A identity authority

## Functional Requirements

### FR-1 Pilot Preparation Package
- The project must define one controlled pilot preparation checklist.
- The checklist must distinguish dry-run readiness from external pilot execution.
- The checklist must reference governed evidence sources rather than chat-only instructions.

### FR-2 Pilot Dry-Run Evidence
- The project must define the dry-run evidence expected from the current integrated baseline.
- Dry-run evidence must include the relevant readiness, pilot-smoke, release, review-pack, and verification artifacts.
- Dry-run evidence must not require real external SIEM, EDR, or source-system connections.

### FR-3 Pilot Run Log Redaction
- The project must define a pilot run log evidence redaction boundary.
- The pilot run log evidence redaction boundary must be distinct from `S4-D-3` and `RELEASE_PROCESS` operator escalation triage redaction.
- No secret values, raw credentials, or sensitive customer data may be required in pilot-prep evidence.

### FR-4 Collaboration Governance Decision
- Sprint 5 must decide whether `docs/AI_COLLAB_OPERATING_MODEL.md` remains an ungoverned local draft or enters governed review.
- If governed, it must use the normal snapshot path rather than being implicitly accepted by this PRD.
- Any rewrite beyond light revision must be handled by a separate ticket.

### FR-5 Case Workflow Trigger
- `S5-C` may start only after pilot-prep dry-run feedback or an explicit product decision.
- The trigger may come from internal product review and does not require real pilot user feedback.
- Any accepted workflow changes must preserve the non-destructive Sprint 4 case lifecycle semantics.

### FR-6 Source Expansion Boundary
- `S5-B` must remain discovery/contract depth until external source inputs exist.
- Fixture-only validation may proceed without external credentials.
- Live refresh, external authentication, multi-tenant data ownership, and CMDB sync require an independent product decision.

### FR-7 Telemetry Breadth Boundary
- `S5-D` must remain discovery/fixture depth until external telemetry inputs exist.
- Synthetic or already-governed replay expansion may proceed in repo.
- Host-selection changes must continue to route identity decisions through the accepted Sprint 4 identity authority.

## UX / Operator Requirements
- Operator-facing pilot preparation materials must be executable without hidden local knowledge.
- Pilot-prep steps must clearly distinguish:
  - readiness preflight
  - pilot-smoke execution
  - dry-run evidence capture
  - pilot run log evidence redaction
  - operator escalation triage redaction
  - sign-off readiness
- Analyst and manager workflow language must remain non-destructive.
- Any case workflow hardening must preserve the analyst-first reading order and manager-review clarity accepted in Sprint 4.
- Source and telemetry discovery docs must explain what can be tested with fixtures and what is blocked on external inputs.

## Success Metrics
- one controlled pilot preparation checklist exists
- one pilot dry-run evidence checklist exists
- one pilot sign-off checklist exists
- pilot run log evidence redaction is documented separately from operator escalation triage redaction
- Sprint 5 explicitly decides whether `docs/AI_COLLAB_OPERATING_MODEL.md` should remain ungoverned or enter governed review
- any `S5-C` work is triggered by pilot-prep dry-run feedback or explicit product decision
- `S5-B` and `S5-D` remain bounded to discovery/contract/fixture depth unless external inputs and product decisions are present
- no Sprint 5 work requires external pilot execution or real external system connectivity to pass its in-repo acceptance checks

## Delivery Definition
Sprint 5 is complete when:
- `S5-A` produces governed controlled pilot preparation, dry-run evidence, and sign-off materials
- `S5-E` records a governed decision on whether and how to handle the existing AI collaboration operating model draft
- `S5-C` is either completed as a triggered workflow-hardening stream or explicitly deferred with rationale
- `S5-B` records source-mode discovery/contract outputs and hold triggers without connecting real external source systems
- `S5-D` records telemetry-breadth discovery/fixture outputs and hold triggers without connecting real external telemetry systems
- all accepted Sprint 5 outputs are included in governed release and review artifacts if they change the baseline

## Risks
- pilot preparation may be mistaken for external pilot execution
- dry-run evidence may accidentally collect information that belongs under operator escalation triage redaction instead of pilot run log evidence redaction
- collaboration governance may distract from product discovery or expand into a from-scratch process redesign
- source-mode discovery may drift into live refresh, external authentication, multi-tenant ownership, or CMDB sync without product approval
- telemetry breadth work may drift into queueing, fan-out, async runtime, or performance commitments before external inputs justify it
- case workflow hardening may expand into RBAC, ticketing integration, or destructive response approval
- Sprint 5 planning may overfit to hypothetical pilot feedback instead of using dry-run evidence and explicit product decisions

## Dependencies
- `S4-INTEGRATED-2026-04-13-001` governed integrated pilot baseline
- `docs/SPRINT5_DISCOVERY_BRIEF.md`
- `docs/S4_SPRINT4_PILOT_BASELINE_REVIEW_PASS.md`
- `docs/S4D5_PILOT_READINESS_REVIEW_PASS.md`
- current release manifest and verification report
- current `S4-D` pilot readiness, smoke path, runbook, and validation-gate docs
- current `S4-C` durable case lifecycle and product review baseline
- current `S4-A` identity authority and source-contract baseline
- current `S4-B` EDR replay and T3 parity baseline
- `docs/AI_COLLAB_OPERATING_MODEL.md` as an ungoverned local draft for review consideration only

## Acceptance Summary By Stream
- `S5-A`: one governed controlled pilot preparation package with dry-run evidence, sign-off, and pilot run log evidence redaction boundaries
- `S5-E`: one explicit planning/governance decision on reviewing, lightly revising, and potentially governing the existing AI collaboration operating model draft
- `S5-C`: one triggered case workflow hardening stream, or an explicit defer decision, based on pilot-prep dry-run feedback or product decision
- `S5-B`: one source-mode discovery/contract record with hold triggers for live refresh, multi-tenant data ownership, external authentication, and CMDB sync
- `S5-D`: one telemetry-breadth and host-selection discovery/fixture record with hold triggers for live external telemetry, async fan-out, and identity-authority drift
