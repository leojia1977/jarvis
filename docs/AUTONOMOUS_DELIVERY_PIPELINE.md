# Autonomous Delivery Pipeline

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Delivery Pipeline |
| Status | Updated by PRD intake automation trigger baseline |
| Snapshot | S5-PRD-INTAKE-AUTOMATION-TRIGGER-2026-04-22-001 |
| Stage | s5-prd-intake-automation-trigger |
| Baseline commit | `47f86dc4249155a30bc617eb26f522f9caf4b739` |

This pipeline defines how autonomous work should move from PRD/product-source trigger or backlog item to governed closeout. It does not authorize implementation or launch execution.

## 1.1 Autonomous Session Startup Requirements

Before autonomous action, the activation prompt must require loading the core governance docs:

- `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
- `docs\DELEGATED_APPROVER_CHARTER.md`
- `docs\AUTONOMOUS_DELIVERY_PIPELINE.md`
- `docs\AUTONOMOUS_HOLD_QUEUE.md`
- `docs\L3_CUSTOMER_TRIAL_LAUNCH_CRITICAL_PATH.md`
- `docs\PRODUCT_STATE.md`
- `docs\ROADMAP_AND_PARKED_ITEMS.md`
- `docs\GOVERNANCE_DECISION_LOG.md`

At the start of every autonomous session, Codex must re-read `docs\DELEGATED_APPROVER_CHARTER.md` and verify that `delegation_expires` has not passed. If the charter cannot be read, the timestamp is missing, or the authorization window has expired, all Red authority is HOLD and AI must not proceed with any Red-lane action.

Lane ambiguity defaults to the higher-restriction lane. If still unclear, HOLD.

The policy is `ACTIVE` only during the authorization window and only after the charter reread and expiry check pass. `ACTIVE` does not create blanket Red execution; Red-1/Red-2 still require exact per-action `DELEGATED_APPROVER_GO` where policy requires it, and any unresolved HOLD blocks the action.

The autonomous ops loop must also load `docs\AUTONOMOUS_TOOLCHAIN_INTEGRATION.md`, `docs\AUTONOMOUS_TOOL_CAPABILITY_MATRIX.md`, `docs\AUTONOMOUS_TOOL_RUNBOOK.md`, `docs\VSCODE_ROLE_AND_TOOLCHAIN_ORCHESTRATION.md`, `docs\ADSPOWER_CLAUDE_WEB_AUTOMATION_VERIFICATION.md`, `docs\ADSPOWER_CLAUDE_WEB_RUNBOOK.md`, `docs\ADSPOWER_PROFILE_LAUNCH_VERIFICATION.md`, `docs\ADSPOWER_PROFILE_LAUNCH_RUNBOOK.md`, `docs\CC_SWITCH_COMMAND_PATH_PROVISIONING.md`, `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md`, `docs\SWE_AGENT_CAPABILITY_VERIFICATION.md`, `docs\SWE_AGENT_INSTALL_AND_CAPABILITY_VERIFICATION.md`, `docs\MINI_SWE_AGENT_NONINTERACTIVE_DRY_RUN_VERIFICATION.md`, `docs\MINI_SWE_AGENT_PTY_RUNNER_PROVISIONING.md`, `docs\MINI_SWE_AGENT_WSL2_NO_WRITE_DRY_RUN_VERIFICATION.md`, `docs\SWE_AGENT_RUNBOOK.md`, `docs\SWE_AGENT_YELLOW_BACKLOG_TEMPLATE_INTEGRATION.md`, `docs\LIVE_PRD_INTAKE_RUNBOOK.md`, `docs\LIVE_PRD_INTAKE_METRICS_RECORD.md`, `docs\PRD_INTAKE_AUTOMATION_TRIGGER_RULES.md`, and `docs\PRD_INTAKE_RUN_TRIGGER.md` before using Claude Web review-prompt transfer, Claude Code review-only automation, SWE agent, or PRD intake automation.

## 1.2 Autonomous Operation Cadence

Default autonomous operation cadence is every 1 hour.

Each run should select one next allowed item, classify the lane, and report baseline read, selected task, files proposed or touched, checks run, HOLDs encountered, and any requested human or jarvis action.

Each run must apply the anti-overengineering guard before editing:

- implement the smallest change that satisfies the exact ticket behavior and required tests
- do not introduce a new abstraction, helper, registry, vocabulary, adapter, service, module, or generalized framework unless the ticket explicitly names it
- do not generalize for future routes, states, statuses, formats, roles, backends, transports, or workflows
- do not do unrelated renames, reorganizations, cleanup refactors, or while-we-are-here improvements
- every changed line should map to an explicit ticket sentence or required test
- if a broader abstraction seems desirable, HOLD and record a scoped design note instead of implementing it

Work selection priority is:

1. PRD intake trigger check when the loop is in `WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION`.
2. Green docs-only route judgment and planning artifacts.
3. Yellow docs-only or test-plan-only tasks when exact scope exists.
4. Red-1/Red-2 preparation packages only as drafts or `DELEGATED_APPROVER_GO` requests.
5. L3 critical path blocker reduction by drafting templates, checklists, or question sets.
6. HOLD queue maintenance.

### 1.2.1 PRD Intake Automation Trigger

When the current posture is:

```text
WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION
```

each autonomous ops loop run should first apply:

```text
docs\PRD_INTAKE_AUTOMATION_TRIGGER_RULES.md
```

If a positive trigger exists, the loop should execute:

```text
docs\PRD_INTAKE_RUN_TRIGGER.md
```

The run trigger may start:

```text
docs\LIVE_PRD_INTAKE_RUNBOOK.md
```

and may create or update:

```text
docs\LIVE_PRD_INTAKE_METRICS_RECORD.md
```

only after a positive product-source trigger and safety screen pass.

If no positive trigger exists, the loop must report waiting state and must not edit the metrics record.

The trigger layer does not authorize product route invention, implementation, SWE execution, code/test changes, Claude Web PASS without an actual verdict, launch, deployment, external pilot execution, real data, credentials, public endpoint work, or parked-stream reopen.

During day 1, automation may draft Green/Yellow docs-only stages and prepare closeout gate material where authorized, but staging, commit, and push require explicit human confirmation.

After `S5-AUTONOMOUS-OPS-LOOP-REFRESH-DAY1-CLOSEOUT-2026-04-19-001` closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push, standing Green docs-only closeout may proceed only under `docs\AUTONOMOUS_OPS_LOOP_REFRESH_AND_DAY1_CLOSEOUT.md`. It requires exact file scope, no HOLD, manifest PASS, exact staged files, and inbox reporting. Yellow implementation, Red execution, browser profile launch/switch, Claude Web login, launch, deployment, external pilot execution, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, code/test/runtime/API/schema/dependency/fixture/release-script/contract changes, and AI_COLLAB changes remain outside this rule.

## 1.3 Toolchain Routing

The governed multi-tool pipeline is:

1. Codex automation starts the run.
2. Codex reads the charter, verifies `delegation_expires`, and loads core governance docs.
3. Codex selects one item and classifies the lane.
4. VS Code remains the local workspace/editing execution surface for exact allowed files; it is not product memory, lane authority, review authority, release authority, or independent closeout authority.
5. SWE agent has a verified WSL2 deterministic no-write dry-run path with limits. Future Yellow backlog templates may include it only as an optional bounded implementation accelerator, and it remains unavailable for product work unless a later exact Yellow item explicitly names it with exact files, exact tests, max-change budget, independent review, and HOLD conditions.
6. Claude Code access is verified only through cc-switch routed `claude.cmd` for review-only verdict capture using stdin, `--bare`, JSON wrapper output, disabled tools, no session persistence, plan permission mode, budget cap, first-line verdict parsing, no web requests, and unchanged git status.
7. Claude Web runs in the user's AdsPower browser/profile. The configured-profile AdsPower/CDP path is verified for governed review-prompt transfer readiness only; high-risk use still requires the applicable review and GO gates.
8. Full gate, release packaging, staging, commit, and push run only when explicitly authorized by the current stage or later closeout instruction.

If the Claude Code review-only path, configured AdsPower browser/profile, Claude Web path, or SWE agent future accelerator path is unavailable, ambiguous, mutates files unexpectedly, creates staged files, makes unexpected web requests, or requires credentials/session access, the action is HOLD.

If Claude Code review-only fails before a verdict because of local process-spawn failure such as `spawn EPERM`, do not retry indefinitely. Record the failure once, then route non-secret review material through the verified AdsPower Claude Web review-prompt path. If that fallback is unavailable, ambiguous, or cannot produce a clear verdict, HOLD.

## 1.3.1 SWE Agent Yellow Template Rule

SWE agent / mini-swe-agent is disabled by default for Yellow items. Future backlog packages may include an optional SWE agent block only after `S5-SWE-AGENT-YELLOW-BACKLOG-TEMPLATE-INTEGRATION-2026-04-21-001` closes PASS.

The block must state either:

```text
SWE agent use: not authorized for this item
```

or:

```text
SWE agent use: authorized only as bounded implementation accelerator for this item
```

The authorized form is valid only when the same item explicitly names exact repo root, files, behavior, tests, max-change budget, WSL command path/version, model credential non-secret path if needed, output location, independent review, before/after git status checks, and HOLD conditions.

Existing current or closed Yellow items do not inherit SWE agent authority retroactively.

## 1.4 VS Code Workspace Boundary

VS Code may be used only as the local repo editing/workspace surface for the selected governed task. Codex remains responsible for orchestration, governance doc loading, lane classification, review routing, gate/package/release verification when authorized, manifest updates, and governed closeout under policy limits.

VS Code editor state, terminals, and local windows are execution context. They do not override repo-governed docs, the manifest, release verification, review results, or current git status. If VS Code-visible state conflicts with governed repo evidence, prefer governed repo evidence; if still ambiguous, HOLD.

This boundary does not authorize code/test implementation, browser login/session access, AdsPower profile creation/switching, Claude Web login, credential/session/cookie/token/auth-header inspection, Red execution, launch, deployment, real-data handling, public endpoint work, S5-B/S5-D reopen, ORDIV work, AI_COLLAB changes, staging, commit, or push.

## 2. Pipeline Stages

| Stage | Required input | Output |
| --- | --- | --- |
| PRD trigger check | Current thread/product source, manifest, rolling maps | Live intake trigger, WAIT, or HOLD |
| Live PRD intake | Positive governed product-source trigger | Intake summary and metrics record |
| Backlog item | Human/delegated/governed source need | Candidate work item |
| Route judgment | Baseline, boundaries, risk lane | Route decision or HOLD |
| Scoped ticket | Exact files, behavior, tests, lane, HOLD rules | Implementation or docs ticket |
| Draft/implement | Authorized file set | Draft or patch |
| Review | Claude Code review-only, and Claude Web/external when triggered | PASS, findings, or HOLD |
| Full gate | `py -3 scripts\git_preflight.py --mode all` | PASS or FAIL |
| Package | Release process and manifest | Review pack, release zip, verification |
| Commit/push | PASS, clean scope, lane permission | Governed commit |
| Product map update | Accepted closeout | Updated rolling maps |
| Next/HOLD | Remaining inputs and risks | Next route or HOLD queue entry |

## 3. Review Gates

- Claude Code review-only is required for governed drafts and implementations unless a stage explicitly says otherwise.
- Claude Web or a designated external reviewer is required when high-risk triggers apply.
- Review does not replace human or delegated GO where GO is required.
- Claude Code review automation may use only the verified `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md` path: stdin prompt to `claude.cmd`, `--bare`, JSON wrapper output, disabled tools, no session persistence, plan permission mode, budget cap, first-line verdict parsing, no web requests, and unchanged git status.
- `claude.exe`, local `cc`, non-bare invocation, command-argument multi-line prompts, and `--json-schema` are not accepted for autonomous review evidence.
- If Claude Web is required and the verified configured-profile AdsPower path is unavailable, generate a Claude Web prompt and HOLD for manual transfer.

## 4. Gate Commands

Fast gate:

```text
py -3 scripts\git_preflight.py --mode fast
```

Full gate:

```text
py -3 scripts\git_preflight.py --mode all
```

Full gate is required before governed closeout commit/push when release/manifest verification must be refreshed.

## 5. Release Package And Manifest Rules

- Release artifacts may be generated only through the repo release process.
- Manifest snapshot/stage must match the governed stage.
- Manifest hashes must match tracked key files.
- Do not fabricate PASS, release SHA, or verification metadata.
- Release artifacts may be generated through the release process, but only tracked files may be staged for commit.

## 6. Product Map Updates

After closeout, update rolling maps when the governed state changes:

- `docs\PRODUCT_STATE.md`
- `docs\GOVERNANCE_DECISION_LOG.md`
- `docs\ROADMAP_AND_PARKED_ITEMS.md`

These maps summarize truth and do not authorize implementation.

`docs\PRODUCT_STATE.md` and `docs\ROADMAP_AND_PARKED_ITEMS.md` are passive governed context. They are not active authorization.

## 7. Commit Message Conventions

Use scoped messages such as:

- `docs: close <stage>`
- `test: <bounded test change>`
- `feat: <bounded implementation>`

The message must not imply readiness, customer launch, or implementation authorization beyond the governed scope.

## 8. Branch Rules

- Work from the governed branch named in the prompt.
- Confirm branch and HEAD before starting high-risk or closeout work.
- Do not include unrelated untracked files.
- Do not rewrite pushed history unless explicitly instructed by the human.

## 9. Network Slow Retry Rule

If network access, remote review, GitHub, Claude Web, external reviewer, or remote status check is slow/unresponsive for more than 5 minutes:

- For idempotent/read-only requests, AI may retry once.
- For non-idempotent requests, AI must first check whether the prior request succeeded before retrying.
- For git push, deployment, launch, external access, approval submission, package upload, or any customer/production-affecting action, AI must verify status before resending.
- Maximum automatic retry count: 1.
- If the second attempt exceeds 5 minutes or remains ambiguous, create/update HOLD queue and stop.
- Network slowness never permits bypassing review, gate, release verification, delegated approval, Claude Web/external review, or HOLD conditions.
- Do not duplicate approval requests unless the first request is confirmed not delivered or marked expired/void.
- If delivery status cannot be confirmed due to network conditions, treat the request as ambiguous and apply HOLD.
- Do not repeat non-idempotent launch/deploy/access actions without explicit delegated/human GO.

## 10. Failure Handling

- Fix failures if Green/Yellow and scoped.
- HOLD if Red, ambiguous, or external input is missing.
- HOLD if the gate failure points outside the allowed file set.
- HOLD if external access, real data, secrets, launch execution, or public endpoint work becomes necessary.
