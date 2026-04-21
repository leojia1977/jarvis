# Autonomous Operation Startup

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Operation Startup |
| Status | Updated by anti-overengineering template refresh draft |
| Snapshot | S5-AUTONOMOUS-YELLOW-BACKLOG-TEMPLATE-ANTI-OVERENGINEERING-REFRESH-2026-04-21-001 |
| Stage | s5-autonomous-yellow-backlog-template-anti-overengineering-refresh |
| Route | OPEN_AUTONOMOUS_YELLOW_BACKLOG_TEMPLATE_ANTI_OVERENGINEERING_REFRESH_STAGE |
| Baseline commit | `54f2408f026a971ec969db7c8a49a2300d324cb2` |
| Baseline snapshot | S5C-IMPL11-CASE-VIEW-REVIEW-GUIDANCE-REGRESSION-HARDENING-IMPLEMENTATION-CLOSEOUT-2026-04-21-001 |
| Baseline stage | s5c-impl11-case-view-review-guidance-regression-hardening-implementation-closeout |
| Baseline manifest status | PASS |
| Baseline release artifact | `releases\secupilot-S5C-IMPL11-CASE-VIEW-REVIEW-GUIDANCE-REGRESSION-HARDENING-IMPLEMENTATION-CLOSEOUT-2026-04-21-001.zip` |
| Baseline release sha256 | `89a1ea2581e2bb08953375a41c4b206051e45bb04e158559f63ca0ff8a36a677` |

This document starts the autonomous operating loop. It does not start product launch, external pilot execution, production deployment, credential handling, real-data handling, public endpoint work, S5-B/S5-D reopen, ORDIV work, or Red-3 action.

## 1.0 Current Refresh

The current governed refresh stage is `S5-AUTONOMOUS-OPS-LOOP-REFRESH-DAY1-CLOSEOUT-2026-04-19-001` / `s5-autonomous-ops-loop-refresh-day1-closeout`.

That stage records:

- duplicate autonomous ops loop removal
- one active 1-hour ops loop as the default after the later anti-overengineering refresh
- expanded per-run read set including the toolchain docs, VS Code role orchestration doc, AdsPower Claude Web verification/runbook docs, and AdsPower profile launch verification/runbook docs
- standing Green docs-only closeout conditions after the refresh stage itself closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push
- AHQ-019 supersession only for Green docs-only closeout
- AHQ-020 remaining HOLD until `cc switch` non-interactive Claude Code review is verified
- later anti-overengineering refresh requiring minimal ticket-mapped changes for future Yellow backlog items

It does not authorize Yellow implementation, Red execution, browser profile creation/switching, Claude Web login, launch, deployment, external pilot execution, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB changes.

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

- Run an autonomous operation check every 1 hour.
- Select one next allowed item per run unless the stage prompt explicitly authorizes a different batch.
- Prefer Green/Yellow docs-only stages and closeout-gated drafting where authorization is clear.
- Stop on ambiguity, expired delegation, unreadable charter, missing baseline, unexpected dirty scope, or unresolved HOLD.

Anti-overengineering guard:

- Implement the smallest change that satisfies the exact ticket behavior and required tests.
- Do not introduce a new abstraction, helper, registry, vocabulary, adapter, service, module, or generalized framework unless the ticket explicitly names it.
- Do not generalize for future routes, states, statuses, formats, roles, backends, transports, or workflows.
- Do not do unrelated renames, reorganizations, cleanup refactors, or while-we-are-here improvements.
- Every changed line should map to an explicit ticket sentence or required test.
- If a broader abstraction seems desirable, HOLD and record a scoped design note instead of implementing it.

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
4. Load toolchain and AdsPower Claude Web governance docs when toolchain/review automation is relevant:
   - `docs\AUTONOMOUS_TOOLCHAIN_INTEGRATION.md`
   - `docs\AUTONOMOUS_TOOL_CAPABILITY_MATRIX.md`
   - `docs\AUTONOMOUS_TOOL_RUNBOOK.md`
   - `docs\VSCODE_ROLE_AND_TOOLCHAIN_ORCHESTRATION.md`
   - `docs\ADSPOWER_CLAUDE_WEB_AUTOMATION_VERIFICATION.md`
   - `docs\ADSPOWER_CLAUDE_WEB_RUNBOOK.md`
   - `docs\ADSPOWER_PROFILE_LAUNCH_VERIFICATION.md`
   - `docs\ADSPOWER_PROFILE_LAUNCH_RUNBOOK.md`
   - `docs\CC_SWITCH_COMMAND_PATH_PROVISIONING.md`
   - `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md`
5. Confirm manifest baseline and git cleanliness.
6. Identify one next allowed item.
7. Classify the lane as Green, Yellow, Red-1, Red-2, Red-3, or HOLD.
8. Proceed only if lane and authorization are clear.

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

## 12. Standing Green Docs-Only Closeout

After `S5-AUTONOMOUS-OPS-LOOP-REFRESH-DAY1-CLOSEOUT-2026-04-19-001` closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push, the autonomous ops loop may close Green docs-only stages without separate per-closeout human confirmation only under the standing Green docs-only closeout rule in `docs\AUTONOMOUS_OPS_LOOP_REFRESH_AND_DAY1_CLOSEOUT.md`.

This standing rule is narrow. It does not apply to Yellow implementation, code/test changes, dependency changes, fixture changes, runtime/API/schema changes, release-script changes, contract changes, Red work, browser profile creation/switching, Claude Web login, launch, deployment, external pilot execution, credentials, real data, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, S4-A resolver changes, or AI_COLLAB changes.

## 13. CC Switch Review-Only Path

After `S5-CC-SWITCH-COMMAND-PATH-PROVISIONING-2026-04-19-001` closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push, the autonomous ops loop may use Claude Code review-only evidence only through `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md`.

The verified path is limited to stdin prompt transfer to `claude.cmd` with `--bare`, JSON wrapper output, disabled tools, no session persistence, plan permission mode, budget cap, first-line verdict parsing, no web requests, and unchanged git status.

This path does not authorize Claude Code edits, file-read review beyond supplied prompt material unless separately governed, command execution, tests, staging, commit, push, Red execution, launch, deployment, external pilot execution, credentials, real data, public endpoint work, S5-B/S5-D reopen, ORDIV work, AI_COLLAB changes, or replacing required human/delegated/Claude Web/external review.

If the Claude Code review-only path fails before producing a verdict because of local process-spawn failure such as `spawn EPERM`, automation must not retry indefinitely. It must record the failure once, then use the verified AdsPower Claude Web review-prompt path as a fallback only for non-secret review material. If that fallback is unavailable, ambiguous, or cannot return a clear verdict, HOLD.
