# Autonomous Operation Startup

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Operation Startup |
| Status | Docs-only autonomous operation startup draft |
| Snapshot | S5-AUTONOMOUS-OPERATION-STARTUP-2026-04-18-001 |
| Stage | s5-autonomous-operation-startup |
| Route | OPEN_AUTONOMOUS_OPERATION_STARTUP_STAGE |
| Baseline commit | `ab8f022604c86fa6ed6edeb87435ca4f2f49c4b8` |
| Baseline snapshot | S5-AUTONOMOUS-POLICY-FINAL-ACTIVATION-2026-04-18-001 |
| Baseline stage | s5-autonomous-policy-final-activation |
| Baseline manifest status | PASS |
| Baseline release artifact | `releases\secupilot-S5-AUTONOMOUS-POLICY-FINAL-ACTIVATION-2026-04-18-001.zip` |
| Baseline release sha256 | `f7c7f26018b74f4426add0fcf567936e175ab3b9fc8d102cbd921a6bbcb45c7e` |

This document starts the autonomous operating loop. It does not start product launch, external pilot execution, production deployment, credential handling, real-data handling, public endpoint work, S5-B/S5-D reopen, ORDIV work, or Red-3 action.

## 1.1 Toolchain Integration Update

The next governed stage is `S5-AUTONOMOUS-TOOLCHAIN-INTEGRATION-2026-04-18-001` / `s5-autonomous-toolchain-integration`.

That stage upgrades the operating-loop design from Codex-only autonomous operation to a governed four-tool collaboration pipeline:

- Codex autonomous operation loop
- VS Code local workspace
- Claude Code review path through the user-configured `cc switch` API tool
- Claude Web external review path running in the user's AdsPower browser/profile

Toolchain integration is definition and verification planning only. It does not execute the full toolchain, verify browser automation, log into Claude Web, handle credentials, or authorize launch/deploy/pilot/Red-3 work.

## 2. Startup Objective

The objective is to allow safe autonomous progress on governed, non-launch work while the human is unavailable.

Default cadence:

- Run an autonomous operation check every 2 hours.
- Select one next allowed item per run unless the stage prompt explicitly authorizes a different batch.
- Prefer Green/Yellow docs-only stages and closeout-gated drafting where authorization is clear.
- Stop on ambiguity, expired delegation, unreadable charter, missing baseline, unexpected dirty scope, or unresolved HOLD.

## 3. Day-1 Limitation

During day 1 of autonomous operation startup:

- Automation may draft Green/Yellow docs-only stages when lane and authorization are clear.
- Automation may prepare closeout gate material when the stage allows it.
- Staging, commit, and push still require explicit human confirmation.
- No policy text may be interpreted as blanket permission to stage, commit, or push during day 1.

## 4. Per-Run Mandatory Startup Checks

Every autonomous operation run must begin with these checks:

1. Read `docs\DELEGATED_APPROVER_CHARTER.md`.
2. Verify `delegation_expires` has not passed.
3. Load the eight core governance docs:
   - `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
   - `docs\DELEGATED_APPROVER_CHARTER.md`
   - `docs\AUTONOMOUS_DELIVERY_PIPELINE.md`
   - `docs\AUTONOMOUS_HOLD_QUEUE.md`
   - `docs\L3_CUSTOMER_TRIAL_LAUNCH_CRITICAL_PATH.md`
   - `docs\PRODUCT_STATE.md`
   - `docs\ROADMAP_AND_PARKED_ITEMS.md`
   - `docs\GOVERNANCE_DECISION_LOG.md`
4. Confirm manifest baseline and git cleanliness.
5. Identify one next allowed item.
6. Classify the lane as Green, Yellow, Red-1, Red-2, Red-3, or HOLD.
7. Proceed only if lane and authorization are clear.

If `docs\DELEGATED_APPROVER_CHARTER.md` cannot be read, `delegation_expires` is missing, or the authorization window has expired, all Red authority is HOLD and automation must stop.

## 5. Per-Run Output

Each autonomous operation run should report:

- baseline read
- selected task
- lane classification
- files proposed or touched
- checks run
- HOLDs encountered
- next requested human or jarvis action, if any

## 6. Work Selection Priority

Select work in this order:

1. Green docs-only route judgment and planning artifacts.
2. Yellow docs-only or test-plan-only tasks when exact scope exists.
3. Red-1/Red-2 preparation packages only as drafts or `DELEGATED_APPROVER_GO` requests.
4. L3 critical path blocker reduction by drafting templates, checklists, or question sets.
5. HOLD queue maintenance.

## 7. Lane And Authorization Rules

`ACTIVE` does not authorize blanket Red execution.

Every Red-1/Red-2 execution still requires exact per-action `DELEGATED_APPROVER_GO` where policy requires it.

Red-3 remains never AI-self-authorized and is not delegable by normal Red-1/Red-2 approval. Jarvis may not approve Red-3.

Any missing `DELEGATED_APPROVER_GO` field means HOLD. Any expired approval means HOLD. Lane ambiguity defaults to the higher-restriction lane; if still unclear, HOLD. Any unresolved HOLD blocks the action.

## 8. Network Slow Rule

If network access, remote review, GitHub, Claude Web, external reviewer, or remote status check is slow or unresponsive for more than 5 minutes:

- For idempotent/read-only requests, automation may retry once.
- For non-idempotent requests, automation must first check whether the prior request succeeded before retrying.
- For git push, deployment, launch, external access, approval submission, package upload, or any customer/production-affecting action, automation must verify status before resending.
- Maximum automatic retry count is 1.
- If the second attempt exceeds 5 minutes or remains ambiguous, update HOLD context and stop.
- Network slowness never permits bypassing review, gate, release verification, delegated approval, Claude Web/external review, or HOLD conditions.

## 9. HOLD Preservation

This startup stage closes no HOLD item unless later explicitly governed.

Current HOLD preservation:

- AHQ-003 through AHQ-014 remain HOLD.
- AHQ-017 remains `HOLD_IF_AMBIGUOUS`.
- L3 launch execution remains unauthorized.
- External pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- ORDIV-L1A remains `PARK_LOCAL_VALIDATION_NO_REPORT`.
- S5-B and S5-D remain `PASS_AND_PARK`.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- AI_COLLAB remains unchanged.

## 10. Deactivation And Expiry

At policy expiry, replacement, or deactivation, an `AUTONOMOUS_PERIOD_END` marker is required in `docs\GOVERNANCE_DECISION_LOG.md`.

If `delegation_expires` has passed or the charter cannot be read, all Red authority is HOLD and automation must stop.

## 11. Non-Authorization

This startup stage does not authorize:

- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime/API/schema changes
- release script changes
- AI_COLLAB changes
- credential handling by AI
- real-data/report/CSV/L1B work
- public endpoint work
- external pilot execution
- customer launch
- production deployment
- S5-B/S5-D reopen
- ORDIV reopen
- Red-3 execution
- staging, commit, or push without explicit human confirmation during day 1
- full gate or release packaging unless explicitly authorized after review
