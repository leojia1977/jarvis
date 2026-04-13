# S5-A-4 Pilot Sign-Off Checklist

## Document Control
- Status: `draft for review`
- Baseline: `S5-A-2026-04-13-003`
- Source of truth: `D:\产品设计\New folder`
- Purpose: pilot sign-off checklist
- Non-goals:
  - not external pilot execution
  - not a real customer/operator sign-off record
  - not a replacement for `docs/S5A1_PILOT_PREPARATION_CHECKLIST.md`
  - not a replacement for `docs/S5A2_DRY_RUN_EVIDENCE_TEMPLATE.md`
  - not a replacement for `docs/S5A3_PILOT_RUN_LOG_REDACTION_BOUNDARY.md`

## Goal
Define the checklist used after controlled pilot dry-run preparation to decide whether the evidence is ready for a controlled external pilot decision, should hold, or needs a separate product/governance decision.

This document does not execute a dry run, create a real external pilot sign-off record, start external pilot execution, or change the boundaries already governed by S5-A-1, S5-A-2, or S5-A-3.

## Scope
- Define the sign-off inputs that must be reviewed after controlled dry-run preparation.
- Define `PASS`, `HOLD`, and `NEEDS_DECISION` judgment states.
- Provide PASS, HOLD, and NEEDS_DECISION checklists for pilot-prep sign-off review.
- Provide a blank sign-off record template for later use.
- Hand off dry-run versus external pilot boundary closeout to S5-A-5.

## Sign-Off Inputs
The sign-off review must use governed repo evidence only:

- `docs/S5A1_PILOT_PREPARATION_CHECKLIST.md`
- `docs/S5A2_DRY_RUN_EVIDENCE_TEMPLATE.md`
- `docs/S5A3_PILOT_RUN_LOG_REDACTION_BOUNDARY.md`
- `docs/S4D5_PILOT_READINESS_REVIEW_PASS.md`
- `docs/S4_SPRINT4_PILOT_BASELINE_REVIEW_PASS.md`

Supporting evidence may include current `releases/release_manifest.json`, `releases/verify_report.json`, and local dry-run outputs when they are redacted and tied back to the governed checklist and evidence template.

## Sign-Off Decision States

### PASS
`PASS` means dry-run preparation evidence is complete enough to support a controlled external pilot decision.

`PASS` does not start external pilot execution. It only says the dry-run evidence package is ready to be used by the separate external pilot decision process.

### HOLD
`HOLD` means evidence is incomplete, unsafe, failed without governed triage, or violates governed boundaries.

`HOLD` should stop sign-off progression until the missing or unsafe evidence is corrected and reviewed again.

### NEEDS_DECISION
`NEEDS_DECISION` means evidence is sufficient, but a product or governance decision is required before changing scope.

`NEEDS_DECISION` should not be converted into `PASS` by local judgment or oral approval. It needs an explicit decision path.

## PASS Checklist
Mark `PASS` only when all of the following are true:

- [ ] S5-A-1 preparation checklist is completed.
- [ ] S5-A-2 dry-run evidence is captured for `py -3 scripts\git_preflight.py --mode pilot`.
- [ ] S5-A-2 dry-run evidence is captured for `POST /api/v1/pilot-smoke`.
- [ ] S5-A-3 redaction boundary is followed.
- [ ] No secret values, bearer tokens, auth headers, cookies, connection strings, raw credentials, API keys, or unredacted sensitive payloads are present.
- [ ] Readiness evidence shows `environment_profile=pilot_local`.
- [ ] Readiness evidence shows `ready=true`.
- [ ] Readiness evidence shows `profile_contract_ready=true`.
- [ ] Readiness evidence shows `case_store_ready=true`.
- [ ] Readiness evidence shows `state_class=READY`.
- [ ] Readiness evidence shows `failure_category=none`.
- [ ] Smoke evidence shows `smoke_path.path_id=pilot_local_production_case_round_trip`.
- [ ] Smoke evidence shows `smoke_path.steps` in the governed order: `readiness -> investigate -> create_case -> get_case`.
- [ ] Smoke evidence shows `smoke_path.failed_step=null`.
- [ ] Smoke evidence shows `POST /api/v1/pilot-smoke` outer HTTP status is `200 OK`.
- [ ] Smoke evidence shows internal `create_case` step `http_status=201`; do not confuse this with the outer endpoint status.
- [ ] Smoke evidence shows `case_id` and `persistent_case.case_id` alignment.
- [ ] Smoke evidence shows `persistent_case.lifecycle_status=open`.
- [ ] No unresolved `P1` or `P2` operator ambiguity remains.
- [ ] No external pilot execution occurred as part of dry-run sign-off.

## HOLD Checklist
Mark `HOLD` when any of the following are true:

- [ ] S5-A-1 preparation evidence is missing.
- [ ] S5-A-2 dry-run evidence is missing.
- [ ] S5-A-3 redaction confirmation is missing.
- [ ] `py -3 scripts\git_preflight.py --mode pilot` evidence is failed, incomplete, or not tied to the current governed baseline.
- [ ] `/ready` evidence is incomplete.
- [ ] `POST /api/v1/pilot-smoke` evidence is incomplete.
- [ ] `smoke_path.failed_step` is present without S4-D-3 triage mapping.
- [ ] Evidence contains an unredacted secret value or sensitive payload.
- [ ] A real external SIEM, EDR, or source connection was used unintentionally.
- [ ] Readiness profile is not `pilot_local`.
- [ ] `case_store_ready` is not `true`.
- [ ] Smoke path identity is ambiguous or `smoke_path.path_id` is missing.
- [ ] Sign-off relies on oral knowledge instead of governed evidence.
- [ ] Evidence changes or bypasses S5-A-1, S5-A-2, or S5-A-3 boundaries.

## NEEDS_DECISION Checklist
Mark `NEEDS_DECISION` when the evidence package is otherwise sufficient but one or more scope decisions are required:

- [ ] Decide whether to start real external pilot execution.
- [ ] Decide whether to start S5-C after dry-run feedback.
- [ ] Decide whether to expand S5-B source modes beyond discovery.
- [ ] Decide whether to expand S5-D telemetry breadth beyond fixture/discovery.
- [ ] Decide whether S5-E / `docs/AI_COLLAB_OPERATING_MODEL.md` should be governed.
- [ ] Decide whether any finding requires changing the S5-A-3 redaction boundary through separate review.

## Sign-Off Record Template
Use this blank template only after dry-run evidence exists. Do not treat this template as a filled real customer/operator sign-off record.

```markdown
## Pilot Prep Sign-Off Record
- snapshot ID:
- branch:
- commit hash:
- reviewer / approver:
- decision: PASS / HOLD / NEEDS_DECISION
- evidence references:
- redaction confirmation:
- unresolved decisions:
- notes:
```

## Review Guidance
- Prefer `HOLD` when evidence is missing, unsafe, or not redacted.
- Prefer `NEEDS_DECISION` when the evidence is adequate but would change product or governance scope.
- Use `PASS` only when the dry-run evidence is complete, governed, redacted, and still clearly separate from external pilot execution.
- Do not use this checklist to authorize external pilot execution directly.

## Handoff To Later Tickets
- S5-A-5 owns dry-run versus external pilot boundary closeout.
- S5-C may start only from dry-run feedback or explicit product decision.
- S5-E remains lightweight parallel governance and does not block S5-A unless explicitly decided.
- Any later sign-off closeout may reference this checklist, but must not rewrite S5-A-1 preparation, S5-A-2 evidence capture, or S5-A-3 redaction boundaries without separate review.

## Acceptance
- The checklist distinguishes readiness for external pilot consideration from starting external pilot execution.
- The checklist requires S5-A-1 preparation evidence, S5-A-2 dry-run evidence, and S5-A-3 redaction boundary acceptance.
- The checklist defines PASS, HOLD, and NEEDS_DECISION judgments without filling a real sign-off record.
- The checklist does not depend on real external pilot feedback.
- The checklist identifies reviewer / approver evidence fields without introducing enterprise RBAC, tenancy, ticketing, or workflow-engine scope.
