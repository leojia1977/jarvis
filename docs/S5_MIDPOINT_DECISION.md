# Sprint 5 Midpoint Decision

## Document Control
- Status: `draft for review`
- Baseline: `S5-E-2026-04-13-004`
- Source of truth: `D:\产品设计\New folder`
- Purpose: Sprint 5 midpoint decision
- Non-goals:
  - not external pilot execution
  - not external pilot authorization
  - not S5-C implementation
  - not S5-B/S5-D implementation
  - not runtime or test changes

## Goal
Choose the next Sprint 5 mainline after `S5-A Controlled Pilot Preparation` and `S5-E AI Collaboration Operating Model` governance have closed.

This document is a decision record draft only. It does not start external pilot execution, authorize real system access, implement S5-C, implement S5-B/S5-D, or change runtime/test behavior.

## Current Baseline
- `S5-A Controlled Pilot Preparation` is closed as a governed preparation package.
- `S5-E AI Collaboration Operating Model` is governed as collaboration workflow guidance.
- External pilot execution is still not authorized.
- Product/governance must choose the next mainline before implementation begins.
- `docs/AI_COLLAB_OPERATING_MODEL.md` now guides collaboration workflow only; product/runtime decisions remain governed by their own PRDs, contracts, tests, and release process.

## Candidate Paths
- `External pilot decision package`: prepare the explicit product/governance go/no-go package required before any real external pilot execution.
- `S5-C Case Workflow Hardening`: harden pilot-local analyst / manager case workflow only if dry-run feedback or explicit product decision selects it.
- `S5-B / S5-D Discovery`: keep source-mode and telemetry-breadth work at discovery, contract, or fixture depth until external inputs exist.
- `Pause mainline and collect missing external pilot inputs`: avoid starting a product stream until required pilot decision inputs are available.

## Decision Matrix

| Candidate path | Required inputs | What can proceed in repo | What requires external/product/governance decision | Main risk | HOLD trigger | Expected output document or ticket |
| --- | --- | --- | --- | --- | --- | --- |
| External pilot decision package | pilot scope, participating roles, environment/access boundary, evidence retention policy, redaction approval, go/no-go authority, rollback/hold authority | decision package draft, S5-A evidence mapping, open-approval checklist, redacted evidence reference plan | any real external pilot start, real operator/customer context, real source/system access, real evidence retention, final go/no-go | S5-A preparation is mistaken for pilot execution authorization | any required authority or boundary is missing, or the work implies external pilot execution before approval | `docs/S5_EXTERNAL_PILOT_DECISION_PACKAGE.md` or equivalent approved decision-package ticket |
| S5-C Case Workflow Hardening | dry-run feedback that identifies case workflow gaps, or explicit product decision; pilot-local analyst/manager journey target | journey decision record, scoped workflow hardening plan, docs/tests only after a later scoped implementation ticket | starting S5-C without trigger; expanding roles beyond pilot-local analyst/manager; touching RBAC, ticketing, workflow engine, or destructive response automation | case workflow hardening drifts into enterprise workflow scope | approval role design exceeds `pilot_local` analyst/manager distinction or touches RBAC, ticketing, workflow-engine, or destructive response scope | `docs/S5C1_ANALYST_MANAGER_JOURNEY_DECISION.md` or S5-C-1 ticket |
| S5-B / S5-D Discovery | S5-B source/input examples or concrete source-mode targets; S5-D telemetry breadth samples, host-selection questions, or fixture-driven scale questions | discovery docs, contract sketches, fixture-only validation, host-selection questions routed through S4-A identity authority | real external source/telemetry access, live refresh, external auth, CMDB sync, async queue/fan-out, performance commitments, identity-authority changes | discovery becomes production integration without inputs or authority | work implies live integration, external auth, CMDB sync, async fan-out, performance commitments, or S4-A identity authority bypass | S5-B source-mode discovery record and/or S5-D telemetry-breadth discovery record |
| Pause mainline and collect missing external pilot inputs | list of missing pilot decision inputs, owner for each input, target review point | in-repo decision-gap record, evidence-input checklist, follow-up prompts or review package | final selection of product mainline, external pilot authorization, any runtime/product scope change | momentum stalls or teams infer unstated authorization from silence | no clear owner, no next review date, or pressure to execute external pilot without the required decision inputs | `docs/S5_MIDPOINT_INPUT_GAP_LOG.md` or product/governance input request |

## External Pilot Package Criteria
The external pilot decision package path is appropriate only if all of the following are available:
- pilot scope
- participating roles
- environment and access boundary
- evidence retention policy
- redaction approval for real pilot records
- go/no-go authority
- rollback/hold authority

If any of these are missing, the project should not treat S5-A completion as authorization to start an external pilot.

## S5-C Criteria
`S5-C Case Workflow Hardening` is appropriate if:
- dry-run feedback points to case workflow gaps, or
- product explicitly chooses case workflow hardening as the next product stream

S5-C boundaries:
- no enterprise RBAC
- no ticketing integration
- no workflow engine
- no destructive response automation

If approval role design exceeds the `pilot_local` analyst/manager distinction, pause for an independent product decision before continuing.

## S5-B / S5-D Criteria
`S5-B` and `S5-D` remain discovery-only unless external inputs are available.

`S5-B` requires source/input examples or concrete source-mode targets before moving beyond discovery or contract sketches.

`S5-D` requires telemetry breadth samples, host-selection questions, or fixture-driven scale questions before moving beyond discovery or fixture work.

S5-B / S5-D boundaries:
- no live refresh
- no external auth implementation
- no CMDB sync
- no async queue/fan-out implementation
- no performance commitments
- no S4-A identity authority bypass

Any host-selection or source-mode suggestion must remain routed through the accepted S4-A asset-inventory identity authority.

## Recommendation
Preliminary recommendation:
- If all external pilot decision inputs are available, proceed to an `External Pilot Decision Package`.
- If not, recommend `S5-C` only if product explicitly wants case workflow hardening now.
- If neither is true, collect missing pilot inputs and keep S5-B/S5-D discovery-only.
- S5-E is already governed and should now serve as collaboration guidance, not as the product mainline.

This recommendation preserves the current governed boundaries while giving product/governance a clean decision point before implementation resumes.

## PASS / HOLD / NEEDS_DECISION
- `PASS`: a next path can be selected without violating current governed boundaries.
- `HOLD`: the proposed path would imply unapproved external pilot execution, real system access, ungoverned evidence collection, or S4-A/S4-D boundary drift.
- `NEEDS_DECISION`: product/governance must choose among candidates or provide missing inputs before implementation begins.

## Next Step
Preliminary next-step recommendation: ask product/governance to confirm whether the complete external pilot decision inputs are available.

If they are available, draft the external pilot decision package next. If they are not available, choose either `S5-C` by explicit product decision or pause the product mainline to collect the missing pilot inputs while keeping S5-B/S5-D discovery-only.

This document does not declare governance closeout and does not authorize external pilot execution.
