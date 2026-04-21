# Autonomous Ops Loop Refresh And Day-1 Closeout

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Ops Loop Refresh And Day-1 Closeout |
| Status | Docs-only autonomous ops loop refresh draft |
| Snapshot | S5-AUTONOMOUS-OPS-LOOP-REFRESH-DAY1-CLOSEOUT-2026-04-19-001 |
| Stage | s5-autonomous-ops-loop-refresh-day1-closeout |
| Route | OPEN_AUTONOMOUS_OPS_LOOP_REFRESH_AND_DAY1_CLOSEOUT_STAGE |
| Baseline commit | `62b8943465aa45966c72333ed8d8b07dcac50b7e` |
| Baseline snapshot | S5-ADSPOWER-CLAUDE-WEB-AUTOMATION-VERIFICATION-2026-04-18-001 |
| Baseline manifest status | PASS |

This docs-only stage refreshes the autonomous operations loop after AdsPower Claude Web verification and closes the duplicate-loop/day-1 closeout ambiguity for Green docs-only work. It does not authorize implementation, launch, deployment, external pilot execution, credential handling, real-data handling, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, browser profile launch/switch, Claude Web login automation, or AI_COLLAB change.

## 2. Route Judgment

Current baseline is governed and PASS at commit `62b8943465aa45966c72333ed8d8b07dcac50b7e`.

Candidate routes:

| Route | Risk | Decision |
| --- | --- | --- |
| Keep duplicate autonomous loop cards active | Duplicate runs can race, draft overlapping stages, or produce repeated closeout requests. | Reject. |
| Immediately claim full four-tool unattended automation | AHQ-020 remains HOLD for `cc switch` non-interactive Claude Code review, and AHQ-022 blocks profile launch/switch/login/broader session control. | Reject. |
| Refresh the single ops loop, preserve HOLDs, and allow standing Green docs-only closeout after PASS | Bounded acceleration with review/gate/manifest safeguards and no Red/launch/runtime scope. | Select. |
| Open L3 launch or external pilot execution route now | AHQ-003 through AHQ-014 remain HOLD. | Reject. |

Recommended route: `OPEN_AUTONOMOUS_OPS_LOOP_REFRESH_AND_DAY1_CLOSEOUT_STAGE`.

## 3. Automation Card State

The duplicate `autonomous-ops-loop` automation was removed. The remaining active automation is `autonomous-ops-loop-2`.

Required standing state:

- exactly one active autonomous ops loop should run by default
- cadence is updated by the later anti-overengineering refresh to every 1 hour
- prompt must open an inbox item for each run
- prompt must load current core governance docs, toolchain docs, and AdsPower Claude Web verification/runbook docs before action
- prompt must include the AdsPower Claude Web active-profile review-prompt boundary
- prompt must not claim full four-tool automation while AHQ-020 remains HOLD
- prompt must include anti-overengineering and max-change-budget rules for Yellow backlog work
- prompt must fallback to AdsPower Claude Web review-prompt transfer when Claude Code review-only fails before verdict with local process-spawn errors such as `spawn EPERM`

## 4. Refreshed Per-Run Read Set

Every autonomous ops loop run must read:

- `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
- `docs\DELEGATED_APPROVER_CHARTER.md`
- `docs\AUTONOMOUS_DELIVERY_PIPELINE.md`
- `docs\AUTONOMOUS_HOLD_QUEUE.md`
- `docs\L3_CUSTOMER_TRIAL_LAUNCH_CRITICAL_PATH.md`
- `docs\PRODUCT_STATE.md`
- `docs\ROADMAP_AND_PARKED_ITEMS.md`
- `docs\GOVERNANCE_DECISION_LOG.md`
- `docs\AUTONOMOUS_TOOLCHAIN_INTEGRATION.md`
- `docs\AUTONOMOUS_TOOL_CAPABILITY_MATRIX.md`
- `docs\AUTONOMOUS_TOOL_RUNBOOK.md`
- `docs\ADSPOWER_CLAUDE_WEB_AUTOMATION_VERIFICATION.md`
- `docs\ADSPOWER_CLAUDE_WEB_RUNBOOK.md`

If `docs\DELEGATED_APPROVER_CHARTER.md` cannot be read, `delegation_expires` is missing, or the authorization window has expired, all Red authority is HOLD.

## 5. Standing Green Docs-Only Closeout Rule

After this stage itself closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push, the autonomous ops loop may perform standing Green docs-only closeout without separate per-closeout human confirmation only when every condition below is true:

- the selected work is Green lane and docs-only
- exact file scope is named by the governed stage or prompt before closeout
- touched files match the exact allowed docs/manifest/release-artifact scope for that stage
- no code, tests, dependencies, fixtures, runtime/API/schema, release scripts, contracts, AI_COLLAB, real-data, credentials, public endpoint, S5-B/S5-D, ORDIV, launch, deployment, or external pilot execution files are touched
- no Yellow implementation is involved
- no Red execution is involved
- no AdsPower profile launch or switching is involved
- no Claude Web login is involved
- no credential, session, cookie, token, or auth-header inspection is involved
- review returns PASS where review is required, or the governing stage explicitly states review is not required
- `git diff --check` passes
- full closeout gate/package/release verification is PASS
- manifest status is PASS
- manifest is updated from PENDING to PASS only after gate PASS and release verification PASS
- release sha256 matches the release artifact
- no HOLD applies to the closeout
- exact staged files are limited to the governed docs/manifest/release artifacts allowed by the stage
- pre-existing unrelated untracked files remain unstaged
- push target is the current branch only
- network ambiguity is absent under AHQ-017
- the automation opens an inbox item with baseline, selected task, lane, files touched, checks, review, gate, release sha, commit, push result, and remaining HOLDs

This rule does not allow self-assignment of Green lane. Lane must be clear from the current stage prompt, activated standing policy, or prior governed route decision. Lane ambiguity means HOLD.

## 6. What Remains Human Or Delegated

The following still require explicit human or delegated approval where policy permits:

- Yellow implementation or test/code work
- Red-1 or Red-2 execution
- any `DELEGATED_APPROVER_GO`
- S5-B/S5-D reopen decision or implementation
- ORDIV reopen/report/CSV/L1B work
- public endpoint work
- external pilot readiness or execution
- credential handling path
- evidence retention activation
- redaction policy activation for real records
- production deployment
- customer launch
- legal/commercial commitment
- Red-3 action

## 7. Toolchain State After This Stage

Current toolchain posture remains:

- Codex autonomous loop: active within policy and authorization window
- VS Code/local workspace: available execution surface
- Claude Web in AdsPower: verified only for safe review-prompt transfer through an already-active profile and already-open Claude Web page
- AdsPower API-key provisioning: allowed only through non-secret references; key values must not be printed, pasted, logged, committed, or added to prompts
- Claude Code through `cc switch`: still requires separate non-interactive review verification before full unattended Claude Code review is claimed
- AdsPower profile launch/switch/login/session control: not verified and not authorized

## 8. Next Required Verification Stage

Next recommended stage:

`OPEN_CC_SWITCH_CLAUDE_CODE_REVIEW_AUTOMATION_VERIFICATION_STAGE`

Purpose:

- verify the `cc switch` Claude Code review-only path
- confirm non-interactive request/response format
- confirm review-only behavior does not edit files, stage, commit, push, run unapproved commands, or claim execution
- record failure/HOLD conditions
- update AHQ-020 only if verification passes

## 9. Non-Authorization

This stage does not authorize:

- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime/API/schema changes
- release script changes
- contract changes
- AI_COLLAB changes
- launch execution
- production deployment
- external pilot execution
- credential handling by AI
- real-data handling
- public endpoint work
- S5-B/S5-D reopen
- ORDIV reopen/report/CSV/L1B work
- Red-1/Red-2 execution without exact approval
- any Red-3 action
- AdsPower profile launch or switching
- Claude Web login automation
- cookie/session/token/auth-header inspection
- full four-tool unattended automation claim while AHQ-020 remains HOLD
