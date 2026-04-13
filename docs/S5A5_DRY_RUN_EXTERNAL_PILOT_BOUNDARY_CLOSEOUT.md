# S5-A-5 Dry-Run External Pilot Boundary Closeout

## Document Control
- Status: `draft for review`
- Baseline: `S5-A-2026-04-13-004`
- Source of truth: `D:\产品设计\New folder`
- Purpose: dry-run versus external pilot boundary closeout
- Non-goals:
  - not external pilot execution
  - not a real customer/operator sign-off record
  - not a runtime change
  - not the S5-A stream review pass
  - not a replacement for `docs/S5A1_PILOT_PREPARATION_CHECKLIST.md`
  - not a replacement for `docs/S5A2_DRY_RUN_EVIDENCE_TEMPLATE.md`
  - not a replacement for `docs/S5A3_PILOT_RUN_LOG_REDACTION_BOUNDARY.md`
  - not a replacement for `docs/S5A4_PILOT_SIGN_OFF_CHECKLIST.md`

## Goal
Define the closeout boundary for `S5-A Controlled Pilot Preparation`.

`S5-A-1` through `S5-A-4` provide governed pilot-prep materials. They prepare the project to collect and review controlled dry-run evidence, but they do not authorize real external pilot execution, real external system access, or real customer/operator sign-off.

## Scope
- Close the dry-run versus external pilot boundary for S5-A.
- State what the S5-A preparation package can prove.
- State what remains outside S5-A unless separately approved.
- Define `PASS` and `HOLD` criteria for S5-A closeout review.
- Hand off post-S5-A decision paths without starting them.

## Upstream Governed Inputs
- `docs/S5A1_PILOT_PREPARATION_CHECKLIST.md`: defines the controlled pilot preparation checklist, source-of-truth confirmation, governed evidence set, and preparation boundaries.
- `docs/S5A2_DRY_RUN_EVIDENCE_TEMPLATE.md`: defines fillable dry-run evidence capture for `py -3 scripts\git_preflight.py --mode pilot` and `POST /api/v1/pilot-smoke`.
- `docs/S5A3_PILOT_RUN_LOG_REDACTION_BOUNDARY.md`: defines which dry-run, pilot-prep, and future sign-off evidence may be retained, and what must be omitted or redacted.
- `docs/S5A4_PILOT_SIGN_OFF_CHECKLIST.md`: defines `PASS`, `HOLD`, and `NEEDS_DECISION` judgment for pilot-prep sign-off review without creating a real external pilot sign-off record.
- `docs/S4_SPRINT4_PILOT_BASELINE_REVIEW_PASS.md`: accepts the integrated Sprint 4 baseline as coherent enough for controlled pilot use.
- `docs/S4D5_PILOT_READINESS_REVIEW_PASS.md`: accepts the D-stream operator baseline for pilot readiness, including `pilot_local`, readiness semantics, `POST /api/v1/pilot-smoke`, failure triage, and `--mode pilot`.

Supporting evidence may include the current `releases/release_manifest.json` and `releases/verify_report.json` when they remain aligned to the governed snapshot under review.

## Boundary Definitions

### Dry-Run Completion
Dry-run completion means governed evidence can show that `pilot_local` preparation was exercised through the accepted in-repo and local dry-run paths.

Dry-run completion may include:
- completed S5-A-1 preparation evidence
- S5-A-2 evidence for `py -3 scripts\git_preflight.py --mode pilot`
- S5-A-2 evidence for `POST /api/v1/pilot-smoke`
- S5-A-3 redaction confirmation
- current manifest and verification evidence

Dry-run completion does not mean the project has started an external pilot.

### Sign-Off Readiness
Sign-off readiness means the S5-A-4 checklist can determine whether the dry-run evidence is complete enough to support a later controlled external pilot decision.

S5-A-4 can produce a pilot-prep judgment such as:
- `PASS`
- `HOLD`
- `NEEDS_DECISION`

That judgment supports decision-making. It does not itself create a customer/operator sign-off record or authorize execution.

### External Pilot Execution
External pilot execution means a real pilot start involving external operators, customer-like context, real source/system access, live operational evidence, or real customer/operator sign-off expectations.

External pilot execution remains outside S5-A unless separately approved through a product/governance decision. S5-A documents may be used as inputs to that decision, but they are not the decision.

## Accepted S5-A Guarantees
When S5-A closes successfully, the accepted preparation package can guarantee:
- `S5-A-1` provides a preparation checklist.
- `S5-A-2` provides a dry-run evidence template.
- `S5-A-3` provides a pilot run log evidence redaction boundary.
- `S5-A-4` provides a pilot sign-off checklist.
- All four artifacts are scoped to pilot-prep and dry-run governance.
- The S5-A package does not require live external SIEM, EDR, source-system, customer, or operator access.
- The S5-A package does not change runtime readiness semantics, the governed smoke path, Sprint 4 integrated pilot behavior, or S4-D operator triage rules.

## Explicit Non-Authorization
- S5-A-4 `PASS` does not authorize external pilot execution.
- S5-A closeout does not authorize real SIEM, EDR, or source-system connections.
- S5-A closeout does not authorize collection of real customer/operator evidence beyond governed redacted artifacts.
- S5-A closeout does not change S4 integrated pilot baseline behavior.
- S5-A closeout does not convert dry-run evidence into real external pilot feedback.
- S5-A closeout does not replace the separate product/governance decision required before external pilot start.

## Required Decision Before External Pilot
Before any external pilot execution starts, a separate product/governance decision must define:
- pilot scope and participating roles
- environment and access boundary
- evidence retention policy
- redaction approval for real pilot records
- go/no-go authority
- rollback/hold authority
- whether S5-C should start from dry-run feedback or explicit product decision

The decision should also confirm whether any external pilot activity requires additional legal, security, privacy, customer, or operational approval outside the current repo-governed preparation package.

## PASS / HOLD For S5-A Closeout

### PASS
Mark S5-A closeout `PASS` only when all of the following are true:

- S5-A-1, S5-A-2, S5-A-3, and S5-A-4 are governed and internally consistent.
- No unresolved `P1` or `P2` boundary ambiguity remains.
- Dry-run evidence and sign-off readiness are clearly separated from external pilot execution.
- The redaction boundary is clear and compatible with S4-D-3 / `RELEASE_PROCESS`.
- S5-A documents do not require real external SIEM, EDR, or source-system connectivity for acceptance.
- S5-A documents do not require secret values, raw credentials, bearer tokens, API keys, auth headers, cookies, connection strings, or unredacted sensitive payloads.
- S5-A documents preserve the accepted Sprint 4 integrated pilot baseline behavior.

### HOLD
Mark S5-A closeout `HOLD` when any of the following are true:

- Any S5-A artifact implies external pilot can start automatically.
- S5-A-4 `PASS` is written as execution authorization.
- Real external connections are required for S5-A acceptance.
- The redaction boundary is ambiguous or conflicts with S4-D-3 / `RELEASE_PROCESS`.
- Operator judgment must rely on oral knowledge to distinguish dry-run from external pilot execution.
- S5-A evidence requires unredacted secrets, credentials, tokens, customer-identifying payloads, or other prohibited evidence.
- S5-A changes runtime behavior, smoke-path semantics, Sprint 4 integrated pilot behavior, or governed release rules.

## Handoff After S5-A
If S5-A closes `PASS`, next work can be:
- external pilot decision package, if product/governance chooses to proceed
- S5-C case workflow hardening, if dry-run feedback or explicit product decision triggers it
- S5-E collaboration operating model governance, as lightweight parallel work

S5-B and S5-D remain discovery-only unless external inputs are available.

S5-A `PASS` should be treated as readiness for a later decision path, not as authorization to execute that path.

## Acceptance
`S5-A-5 Dry-Run External Pilot Boundary Closeout` is complete when:
- the document defines dry-run completion, sign-off readiness, and external pilot execution as separate states
- accepted S5-A guarantees are limited to preparation, dry-run evidence, redaction, and sign-off checklist materials
- explicit non-authorization prevents S5-A-4 `PASS` or S5-A closeout from being read as external pilot approval
- required decisions before external pilot are listed clearly
- `PASS` and `HOLD` criteria protect against dry-run / external pilot ambiguity
- post-S5-A handoff options are listed without starting any external pilot, S5-C, S5-E, S5-B, or S5-D work
