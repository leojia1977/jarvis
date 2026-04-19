# Autonomous Toolchain Integration

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Toolchain Integration |
| Status | Updated by cc switch command-path provisioning draft |
| Snapshot | S5-CC-SWITCH-COMMAND-PATH-PROVISIONING-2026-04-19-001 |
| Stage | s5-cc-switch-command-path-provisioning |
| Route | OPEN_CC_SWITCH_COMMAND_PATH_PROVISIONING_STAGE |
| Baseline commit | `5c1d8c1e288c1e16f47279f147fc4a973064e874` |
| Baseline snapshot | S5-ADSPOWER-PROFILE-LAUNCH-VERIFICATION-2026-04-19-001 |
| Baseline stage | s5-adspower-profile-launch-verification |
| Baseline manifest status | PASS |
| Baseline release artifact | `releases\secupilot-S5-ADSPOWER-PROFILE-LAUNCH-VERIFICATION-2026-04-19-001.zip` |
| Baseline release sha256 | `10c213c7d32cd22527c9a41f32102cc0906041882e79cd8420c329982bf214ac` |

## 2. Purpose

This stage defines the governed multi-tool autonomous closed loop for:

- Codex autonomous operation loop
- VS Code local workspace
- Claude Code review path through the user-configured `cc switch` API tool
- Claude Web external review path running in the user's AdsPower browser/profile

This document does not by itself authorize full toolchain execution. It defines capability boundaries, commands, review paths, failure modes, HOLD rules, and authorization lanes before any broader autonomous toolchain execution claim.

## 3. Tool Roles

| Tool | Role |
| --- | --- |
| Codex automation | Scheduler, planner, and executor within active policy limits. |
| VS Code workspace | Local repo editing and workspace execution surface for allowed files; not product memory, not a lane authority, not an independent reviewer, and not a closeout authority by itself. |
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

Current maturity claim: AdsPower / Claude Web path is L3 for a harmless review-prompt round trip and for configured profile launch/attach to review-prompt readiness. Claude Code through cc-switch routed `claude.cmd` reaches L2 for non-interactive review-only verdict-line capture with strict limits. Codex, VS Code, and Codex CLI remain local-tool L1; VS Code is explicitly governed as the local workspace/editing execution surface, not a decision maker, review authority, product memory source, or closeout authority by itself. The full toolchain is a limited four-tool review loop for Green/docs-only review evidence only, not full autonomous implementation.

## 7.1 AdsPower Claude Web Verification Result

The follow-up verification stage `S5-ADSPOWER-CLAUDE-WEB-AUTOMATION-VERIFICATION-2026-04-18-001` verified:

- AdsPower Local API accepts the user-level environment variable API key without printing the key.
- One already-active AdsPower profile is visible.
- One already-open Claude Web page is visible through CDP target metadata.
- Claude Web input can be focused through CDP.
- A harmless prompt round trip returned the expected non-secret test token.

This verification does not authorize AdsPower profile launch, profile switching, login automation, cookie/session/token/auth-header inspection, high-risk review automation, or Red execution.

## 7.2 Ops Loop Refresh Result

`S5-AUTONOMOUS-OPS-LOOP-REFRESH-DAY1-CLOSEOUT-2026-04-19-001` removes the duplicate autonomous ops loop and keeps one 2-hour loop as default.

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
- AdsPower profile creation, profile switching, login automation, or broader session control
- Claude Web login or account/session handling
- staging, commit, or push
- full gate or release packaging unless explicitly authorized after review
