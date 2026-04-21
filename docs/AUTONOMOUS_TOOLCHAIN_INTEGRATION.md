# Autonomous Toolchain Integration

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Toolchain Integration |
| Status | Updated by SWE agent Yellow backlog template integration draft |
| Snapshot | S5-SWE-AGENT-YELLOW-BACKLOG-TEMPLATE-INTEGRATION-2026-04-21-001 |
| Stage | s5-swe-agent-yellow-backlog-template-integration |
| Route | OPEN_SWE_AGENT_YELLOW_BACKLOG_TEMPLATE_INTEGRATION_STAGE |
| Baseline commit | `0b20b9b1fb991cb66d4898d83d0b8ce0609deca3` |
| Baseline snapshot | S5-MINI-SWE-AGENT-WSL2-NO-WRITE-DRY-RUN-VERIFICATION-2026-04-21-001 |
| Baseline stage | s5-mini-swe-agent-wsl2-no-write-dry-run-verification |
| Baseline manifest status | PASS |
| Baseline release artifact | `releases\secupilot-S5-MINI-SWE-AGENT-WSL2-NO-WRITE-DRY-RUN-VERIFICATION-2026-04-21-001.zip` |
| Baseline release sha256 | `4dd7f904eadea00d3f1ce39fe63f83614ee2acbb82dc1313c9febf847fecd84e` |

## 2. Purpose

This stage defines the governed multi-tool autonomous closed loop for:

- Codex autonomous operation loop
- VS Code local workspace
- SWE agent future accelerator candidate
- Claude Code review path through the user-configured `cc switch` API tool
- Claude Web external review path running in the user's AdsPower browser/profile

This document does not by itself authorize full toolchain execution. It defines capability boundaries, commands, review paths, failure modes, HOLD rules, and authorization lanes before any broader autonomous toolchain execution claim.

## 3. Tool Roles

| Tool | Role |
| --- | --- |
| Codex automation | Scheduler, planner, and executor within active policy limits. |
| VS Code workspace | Local repo editing and workspace execution surface for allowed files; not product memory, not a lane authority, not an independent reviewer, and not a closeout authority by itself. |
| SWE agent | Future bounded implementation accelerator candidate only; WSL2 deterministic no-write main-agent dry run is verified with limits, future Yellow templates may include an optional accelerator block, and product-task execution requires a later exact Yellow item that explicitly names SWE agent. |
| Claude Code via cc-switch routed `claude.cmd` | Verified review-only verdict capture path with strict invocation limits; not an editing, command-execution, staging, commit, push, or Red-approval tool. |
| Claude Web in AdsPower browser/profile | External review path; user-confirmed current surface is AdsPower, but it is not assumed automatable until verified by a governed safe path. |

Repo-governed docs, manifest, snapshots, route decisions, closeouts, and periodic reviews remain product memory. Chat windows and local tool sessions are execution context.

## 4. Allowed Flow

1. Codex automation starts run.
2. Reads `docs\DELEGATED_APPROVER_CHARTER.md` and verifies `delegation_expires`.
3. Loads the eight core governance docs.
4. Selects one item.
5. Classifies lane.
6. If Green/Yellow docs-only, drafts or prepares within allowed files through the governed local workspace surface.
7. If review is needed and the stage permits Claude Code review-only evidence, route to Claude Code through the verified `claude.cmd` stdin / `--bare` / verdict-line path in `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md`; otherwise produce a Claude Code review prompt and HOLD for human/tool execution.
8. If Claude Web or external review is needed, prepares an AdsPower/Claude Web prompt for manual transfer or HOLDs if the automation path is not verified.
9. If gate is allowed, runs the closeout gate only when authorized by the current stage and lane rules.
10. During day 1, staging, commit, and push still require explicit human confirmation.

## 5. Current Tool Status

| Area | Current status |
| --- | --- |
| Codex automation | ACTIVE only within the authorization window and policy limits. |
| VS Code CLI | Visible as `code.cmd` by safe local command detection; governed as the local workspace/editing surface only. |
| SWE agent | `mini-swe-agent` 2.2.8 is installed in `SecuPilotUbuntu2404` under `/home/secupilot/.venvs/mini-swe-agent`; `mini` help is callable, and a deterministic no-write dry run completed from the repo root mapping with unchanged git status. Future Yellow templates may include optional bounded accelerator controls, but product-task use remains unavailable unless a later exact Yellow item explicitly names SWE agent and carries all runbook controls. |
| Claude Code via cc-switch routed `claude.cmd` | Verified for non-interactive review-only verdict-line capture through stdin, `--bare`, JSON wrapper output, disabled tools, no session persistence, plan permission mode, budget cap, no web requests, and unchanged git status. `claude.exe`, local `cc`, non-bare invocation, command-argument multi-line prompts, and `--json-schema` are not accepted. |
| Codex CLI | Visible as `codex.exe` by safe local command detection. |
| AdsPower browser/profile | User-confirmed Claude Web surface; Local API authentication, configured profile start/attach, CDP connection, and Claude Web review-prompt readiness are verified with limits. Profile switching, profile creation, login automation, and session inspection remain unverified. |
| Claude Web automation | Verified for review-prompt test only through an already-open Claude Web page. High-risk review, Red work, launch, deployment, and real-data use remain unauthorized. |

Visibility or a user-confirmed tool path means only that a candidate execution surface exists. It does not prove safe non-interactive behavior, authenticated session state, browser control, external review completion, or permission to use credentials.

AdsPower API-key material must not be pasted into chat, committed to repo, added to prompts, or printed in logs. Any future AdsPower automation verification must use a governed non-secret provisioning path such as a local environment variable, Windows Credential Manager, or another human-controlled secret store that the AI references without displaying the secret value.

## 6. Failure Handling

| Failure | Required handling |
| --- | --- |
| CLI unavailable | HOLD. |
| CLI returns non-zero | HOLD, or focused fix only if Green/Yellow and exact scope is clear. |
| CLI output ambiguous | HOLD. |
| AdsPower browser/profile unavailable | HOLD or produce manual Claude Web prompt. |
| AdsPower login/session/profile state unknown | HOLD. |
| Network slow or unresponsive for more than 5 minutes | Apply existing network slow retry rule. |
| Credential prompt appears | HOLD. |
| Real external access requested | HOLD unless exact lane approval exists and no prohibited boundary is triggered. |

## 7. Toolchain Maturity Levels

This section uses `L0` through `L5` for toolchain maturity only. It is not the L3 Customer Trial Launch target.

| Level | Meaning |
| --- | --- |
| L0 | Prompt-only/manual tool transfer. |
| L1 | CLI/tool path detected or human-confirmed, manual review prompt transfer. |
| L2 | Non-interactive CLI/API review verified. |
| L3 | AdsPower browser/external review path verified without credentials in repo/chat. |
| L4 | Fully scheduled Green/Yellow closeout with human-confirmed commit/push policy. |
| L5 | Delegated Red-1/selected Red-2 preparation with exact `DELEGATED_APPROVER_GO`. |

Current maturity claim: AdsPower / Claude Web path is L3 for a harmless review-prompt round trip and for configured profile launch/attach to review-prompt readiness. Claude Code through cc-switch routed `claude.cmd` reaches L2 for non-interactive review-only verdict-line capture with strict limits. Codex, VS Code, and Codex CLI remain local-tool L1; VS Code is explicitly governed as the local workspace/editing execution surface, not a decision maker, review authority, product memory source, or closeout authority by itself. SWE agent has a verified WSL2 deterministic no-write dry-run path with limits, but model-backed product implementation and Yellow backlog participation require a later exact Yellow item. The full toolchain is a limited four-tool review/planning loop plus a candidate bounded accelerator path, not full autonomous implementation.

## 7.1 AdsPower Claude Web Verification Result

The follow-up verification stage `S5-ADSPOWER-CLAUDE-WEB-AUTOMATION-VERIFICATION-2026-04-18-001` verified:

- AdsPower Local API accepts the user-level environment variable API key without printing the key.
- One already-active AdsPower profile is visible.
- One already-open Claude Web page is visible through CDP target metadata.
- Claude Web input can be focused through CDP.
- A harmless prompt round trip returned the expected non-secret test token.

This verification does not authorize AdsPower profile launch, profile switching, login automation, cookie/session/token/auth-header inspection, high-risk review automation, or Red execution.

## 7.2 Ops Loop Refresh Result

`S5-AUTONOMOUS-OPS-LOOP-REFRESH-DAY1-CLOSEOUT-2026-04-19-001` removes the duplicate autonomous ops loop and keeps one active loop as default. The later anti-overengineering template refresh updates the active cadence to every 1 hour.

The loop may reference AdsPower Claude Web verification docs for safe review-prompt transfer only. At that baseline it could not claim full four-tool automation while AHQ-020 remained HOLD for `cc switch` non-interactive Claude Code review. Section 7.6 supersedes this only for limited verdict-line review capture.

Standing Green docs-only closeout is allowed only after the ops-loop refresh stage itself closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push, and only under the exact Green docs-only closeout rule in `docs\AUTONOMOUS_OPS_LOOP_REFRESH_AND_DAY1_CLOSEOUT.md`.

## 7.3 CC Switch Claude Code Verification Result

`S5-CC-SWITCH-CLAUDE-CODE-REVIEW-AUTOMATION-VERIFICATION-2026-04-19-001` attempted only non-secret local discovery for the governed `cc switch` Claude Code review-only path.

Result:

- no local `cc` command or PowerShell alias was available
- `where.exe cc` found no match
- `claude.exe` was visible but is not the governed `cc switch` API path for this stage
- no harmless non-interactive review-only request was submitted
- no parseable review result was returned
- AHQ-020 remained `HOLD_FOR_TOOL_VERIFICATION` at that baseline

The stage does not verify Claude Code edits, implementation, code execution, staging, commit, push, Red execution, launch/deploy, real data, external pilot execution, or full four-tool automation.

## 7.4 VS Code Role Orchestration Result

`S5-VSCODE-ROLE-TOOLCHAIN-ORCHESTRATION-2026-04-19-001` clarifies the VS Code role in the governed autonomous workflow.

Result:

- VS Code is the local workspace and editing execution surface.
- Codex remains the orchestrator for run startup, governance loading, lane classification, review routing, gate/package/release verification, manifest updates, and governed closeout.
- VS Code does not decide lane authority, product route, review sufficiency, PASS state, release verification, or closeout eligibility.
- VS Code editor state, unsaved buffers, terminal sessions, and local tool windows are execution context, not product memory.
- Repo-governed docs, manifest, release artifacts, review packs, and committed closeouts remain product memory.
- This clarification does not raise VS Code above L1 and does not claim full four-tool automation.

If Codex and VS Code context disagree, the repo-governed docs, manifest, current git status, and current committed baseline control. If the conflict cannot be resolved from governed sources, HOLD.

## 7.5 AdsPower Profile Launch Verification Result

`S5-ADSPOWER-PROFILE-LAUNCH-VERIFICATION-2026-04-19-001` verifies the configured AdsPower profile launch/attach path to Claude Web review-prompt readiness.

Result:

- `ADSPOWER_API_KEY` and `ADSPOWER_USER_ID` were present through local non-secret references; values were not printed or recorded.
- AdsPower Local API `browser/start` succeeded for the configured profile identifier.
- The returned CDP endpoint was reachable through HTTP and WebSocket.
- A `claude.ai` page target was found after profile start/attach.
- A minimal DOM probe confirmed `claude.ai`, an editable input surface, and no credential prompt.
- No prompt was submitted in this stage.
- No conversation text, cookies, sessions, tokens, auth headers, browser storage, profile files, API-key value, or profile identifier value were read or recorded.

This verification does not authorize profile creation, profile switching, login automation, cookie/session/token/auth-header inspection, high-risk review automation, Red execution, launch/deploy, real data, external pilot execution, or full four-tool automation.

## 7.6 CC Switch Command Path Provisioning Result

`S5-CC-SWITCH-COMMAND-PATH-PROVISIONING-2026-04-19-001` verifies a callable Claude Code review-only command path.

Result:

- no local `cc` command or alias is available
- `claude.exe` remains rejected as the governed path
- npm shim `claude.cmd` is available and reports Claude Code `2.1.86`
- cc-switch environment variable names were present, but values were not printed or recorded
- non-bare invocation returned stale project context and is rejected
- command-argument multi-line prompts were truncated and are rejected
- `--json-schema` timed out twice and is not verified
- stdin prompt plus `--bare`, JSON wrapper output, disabled tools, no session persistence, plan permission mode, and budget cap returned parseable `VERDICT: PASS`
- no web search/fetch requests were made
- before/after git status was unchanged

This verifies only review-only verdict capture. Claude Code may not edit files, run commands, read secrets, stage, commit, push, perform Red work, replace human/delegated GO, or serve as the sole independent final reviewer when Claude Code or cc-switch behavior is itself under verification.

## 7.7 SWE Agent Capability Verification Result

`S5-SWE-AGENT-CAPABILITY-VERIFICATION-2026-04-21-001` verifies that SWE agent is not currently available as a governed local tool.

Result:

- no `sweagent`, `swe-agent`, `swe`, `sweagent-run`, or `swe-agent-run` command was found
- no `swe-agent` or `sweagent` pip package was found
- no `sweagent`, `swe_agent`, or `sweagent_run` Python module was found
- no install, network package pull, dry run, implementation, test execution, or repo mutation was performed
- SWE agent remains `HOLD_FOR_TOOL_INSTALL_AND_VERIFICATION`

SWE agent may become only a future bounded implementation accelerator after a separate governed install and capability verification route proves repo-root confinement, exact file-scope confinement, no secret/real-data access, no dependency install without approval, no staging/commit/push, harmless dry run, before/after git status, and external review.

## 7.8 SWE Agent Install And Capability Verification Result

`S5-SWE-AGENT-INSTALL-CAPABILITY-VERIFICATION-2026-04-21-001` records that `mini-swe-agent` is present but not yet usable as an autonomous implementation accelerator.

Result:

- official tool selection is `mini-swe-agent` rather than legacy SWE-agent
- `mini-swe-agent` version `2.2.8` is present in user Python site-packages
- entrypoints exist under `C:\Users\Administrator\AppData\Roaming\Python\Python314\Scripts`
- `mini-extra --help` and `mini-extra config --help` succeed
- package import succeeds
- `mini --help` and `mini-swe-agent --help` fail in the current Codex non-interactive Windows shell with `NoConsoleScreenBufferError`
- no harmless no-write agent dry run was completed
- before/after git status stayed unchanged except known unrelated untracked files

SWE agent status is `PARTIAL_VERIFIED_INSTALL_HELP_ONLY_EXECUTION_HOLD`. It may not be used for Yellow backlog implementation until a later governed non-interactive dry-run verification stage proves callable main-agent behavior, no-write dry run, repo-root confinement, exact file-scope confinement, no secret/real-data access, no dependency install without approval, no staging/commit/push, before/after git status, and external review.

## 7.9 Mini SWE Agent Noninteractive Dry Run Verification Result

`S5-MINI-SWE-AGENT-NONINTERACTIVE-DRY-RUN-VERIFICATION-2026-04-21-001` attempted the WSL2 / PTY-capable no-write dry-run route.

Result:

- WSL2 is installed, but the only listed distribution is `docker-desktop`
- `docker-desktop` is not a normal user-controlled distro for governed repo tooling
- probed WSL shell lacked `bash`, exposed an empty `PATH`, and did not provide usable Python or mini-swe-agent commands
- WSL reported a localhost proxy warning in NAT mode
- `winpty` is unavailable
- `cmd.exe /c` still fails with `NoConsoleScreenBufferError`
- no harmless no-write main-agent dry run was completed
- git status stayed unchanged except known unrelated untracked files

SWE agent remains `HOLD_WSL_PTY_DRY_RUN_NOT_AVAILABLE` and may not be used for Yellow backlog implementation.

## 7.10 Mini SWE Agent PTY Runner Provisioning Result

`S5-MINI-SWE-AGENT-PTY-RUNNER-PROVISIONING-2026-04-21-001` records the safe provisioning route for mini-swe-agent.

Result:

- WSL version `2.6.3.0` is installed
- only `docker-desktop` is installed as a WSL distro
- `wsl.exe --list --online` is reachable and lists `Ubuntu-24.04`
- `winget.exe` is visible, but no install was performed
- `winpty` is unavailable
- `wt.exe` and `conhost.exe` visibility is not accepted as a governed noninteractive PTY runner
- selected future route is human-controlled `Ubuntu-24.04` WSL2 user distro provisioning
- new PRD is expected soon, so product development should wait for PRD intake/rebase before starting new Yellow implementation unless product/governance explicitly proceeds with the existing YB-05 route

SWE agent status is `HOLD_PENDING_HUMAN_WSL2_USER_DISTRO_PROVISIONING`. This stage does not authorize WSL distro installation by Codex, PTY runner installation by Codex, mini-swe-agent execution, Yellow backlog integration, code/test changes, dependency changes, staging, commit, or push outside closeout. It may not be used for Yellow backlog implementation until a later human-controlled WSL2/PTY provisioning step is complete and a separate no-write dry-run verification route passes.

## 7.11 Mini SWE Agent WSL2 No-Write Dry Run Verification Result

`S5-MINI-SWE-AGENT-WSL2-NO-WRITE-DRY-RUN-VERIFICATION-2026-04-21-001` verifies the bounded WSL2 mini-swe-agent runner path.

Result:

- `SecuPilotUbuntu2404` is installed as a WSL2 `Ubuntu-24.04` distro
- normal user `secupilot` was used
- repo path `/mnt/d/产品设计/New folder` was visible
- `mini-swe-agent` version `2.2.8` is installed in `/home/secupilot/.venvs/mini-swe-agent`
- `mini --help` is callable in WSL when first-run config prompting is bypassed with `MSWEA_CONFIGURED=true`
- a deterministic no-write dry run used `--agent-class default`, `--model-class deterministic`, a temporary config under `/tmp`, and an output trajectory under `/tmp`
- the only executed command was `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`
- trajectory output recorded `exit_status=Submitted`, `api_calls=1`, `instance_cost=0.0`, and repo-root cwd `/mnt/d/产品设计/New folder`
- before/after git status was unchanged except known unrelated untracked files
- WSL was terminated after verification

This verifies runner mechanics only. It does not authorize model-backed implementation, real product patch generation, Yellow backlog participation, dependency changes, review replacement, manifest/gate/release ownership, staging, commit, or push.

## 7.12 SWE Agent Yellow Backlog Template Integration Result

`S5-SWE-AGENT-YELLOW-BACKLOG-TEMPLATE-INTEGRATION-2026-04-21-001` integrates SWE agent into future Yellow backlog templates only as an optional bounded implementation accelerator.

Result:

- the reusable Yellow backlog preauthorization template now requires an explicit per-item SWE agent posture
- the default is `SWE agent use: not authorized for this item`
- the authorized form must be exactly `bounded implementation accelerator`
- a later exact Yellow item must name repo root, files, behavior, tests, max-change budget, command path/version, model credential non-secret path if needed, output location, independent review, before/after git status checks, and HOLD rules
- current and closed Yellow items are not retroactively SWE-enabled

This integration does not authorize SWE agent execution against product work, model-backed implementation, review replacement, route selection, manifest/gate/release ownership, staging, commit, push, or any product code/test change.

## 8. Non-Authorization

This stage does not authorize:

- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime/API/schema changes
- release script changes
- AI_COLLAB changes
- credential handling
- real-data/report/CSV/L1B work
- public endpoint work
- external pilot execution
- customer launch
- production deployment
- S5-B/S5-D reopen
- ORDIV reopen
- Red-3 execution
- treating VS Code as product memory, approval authority, review authority, lane authority, or independent closeout authority
- SWE agent execution against product work, model-backed implementation assistance, review replacement, manifest/gate/release ownership, staging, commit, push, or Yellow backlog participation unless a later exact Yellow item explicitly names SWE agent after the no-write verification PASS
- AdsPower profile creation, profile switching, login automation, or broader session control
- Claude Web login or account/session handling
- staging, commit, or push
- full gate or release packaging unless explicitly authorized after review
