# S5 External Pilot Decision Checkpoint

## Document Control
- Status: `draft for review`
- Baseline: `S5-A-2026-04-13-006`
- Source of truth: `D:\产品设计\New folder`
- Purpose: post-S5-A decision checkpoint
- Non-goals:
  - not external pilot execution
  - not a real customer/operator sign-off
  - not a runtime change
  - not a replacement for S5-A review pass

## Goal
Choose the next post-S5-A path without violating the governed S5-A preparation boundary.

This checkpoint does not authorize external pilot execution. It only records what inputs are needed before choosing between an external pilot decision package, S5-C, S5-E, or S5-B/S5-D discovery.

## Current Baseline
- `S5-A Controlled Pilot Preparation` is closed as a governed preparation package under `docs/S5A_REVIEW_PASS.md`.
- S5-A provides governed preparation, dry-run evidence, redaction, sign-off, and dry-run/external-pilot boundary materials.
- S5-A does not authorize external pilot execution.
- External pilot execution still requires a separate product/governance decision.
- Current release governance is anchored by `releases/release_manifest.json` and `releases/verify_report.json` for `S5-A-2026-04-13-006`.

## Candidate Paths
- `External pilot decision package`: prepare the explicit go/no-go decision record required before any real external pilot can start.
- `S5-C case workflow hardening`: start only if dry-run feedback or an explicit product decision selects analyst / manager workflow hardening.
- `S5-E AI collaboration operating model governance review`: run lightweight governance review of the existing local draft only if selected through S5-E.
- `S5-B / S5-D discovery`: continue source-mode or telemetry-breadth discovery only within discovery, contract, or fixture boundaries unless external inputs exist.

## Decision Criteria

| Candidate path | Required inputs | What can proceed in-repo | What requires external/product/governance decision | Main risk | HOLD trigger |
| --- | --- | --- | --- | --- | --- |
| External pilot decision package | pilot scope, participating roles, environment/access boundary, evidence retention policy, redaction approval for real pilot records, go/no-go authority, rollback/hold authority | draft the decision package, map S5-A evidence, list open approvals, prepare redacted evidence references | any real pilot start, external operator/customer-like context, real source/system access, real pilot evidence retention, real sign-off | S5-A preparation is mistaken for execution approval | any required authority is missing, or the path implies external pilot execution without separate approval |
| S5-C case workflow hardening | dry-run feedback or explicit product decision; analyst/manager journey target; approval-role scope | draft journey decision, clarify pilot_local analyst/manager workflow, add scoped docs/tests if later authorized | starting S5-C without trigger; expanding approval roles beyond pilot_local; touching RBAC, ticketing, workflow-engine, or destructive response | case workflow work expands into enterprise workflow scope | approval role design exceeds `pilot_local` analyst/manager distinction or touches RBAC/ticketing/workflow-engine scope |
| S5-E AI collaboration operating model governance review | explicit selection of S5-E; existing `docs/AI_COLLAB_OPERATING_MODEL.md` draft; Sprint 5 planning evidence | review-only or light-governance decision work under a later S5-E task | governing the draft, substantial rewrite, new tool policy, or any product-scope change | process governance displaces product decision-making or implicitly governs an off-limits draft | AI collaboration draft is modified or governed without a separate S5-E task and normal snapshot path |
| S5-B / S5-D discovery | external source inputs for S5-B expansion; external telemetry inputs for S5-D expansion; otherwise discovery-only assumptions | discovery docs, contract sketches, fixture-only validation, host-selection policy questions routed through S4-A identity authority | real external source/telemetry connection, live refresh, external auth, multi-tenant data ownership, CMDB sync, async queue/fan-out, performance commitments | discovery drifts into production integration or bypasses S4-A identity authority | work implies real integration, live telemetry/source refresh, queue/fan-out, performance commitments, or S4-A identity bypass without inputs and decision |

## Recommended Default
- Choose `External pilot decision package` if pilot scope, participating roles, environment/access boundary, evidence retention policy, redaction approval, go/no-go authority, and rollback/hold authority are available.
- Otherwise, proceed with `S5-E-1` as lightweight governance work while external pilot inputs are gathered.
- Start `S5-C` only with dry-run feedback or explicit product decision.
- Keep `S5-B / S5-D` discovery-only unless external source or telemetry inputs are available.

## PASS / HOLD / NEEDS_DECISION
- `PASS`: the next path can be selected without violating S5-A boundaries.
- `HOLD`: the selected path would imply external pilot execution without approval, real system access without scope, or ungoverned evidence collection.
- `NEEDS_DECISION`: product/governance must choose among the candidate paths before implementation starts.

## Output
Preliminary recommendation: default to `S5-E-1` lightweight governance review while gathering the external pilot inputs required for an external pilot decision package, unless product/governance can immediately provide all required pilot scope, role, access, evidence, redaction, go/no-go, and rollback/hold authority inputs.

This checkpoint does not declare final governance closeout and does not authorize external pilot execution.
