# Autonomous Toolchain Integration

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Toolchain Integration |
| Status | Updated by cc switch verification draft |
| Snapshot | S5-CC-SWITCH-CLAUDE-CODE-REVIEW-AUTOMATION-VERIFICATION-2026-04-19-001 |
| Stage | s5-cc-switch-claude-code-review-automation-verification |
| Route | OPEN_AUTONOMOUS_TOOLCHAIN_INTEGRATION_STAGE |
| Baseline commit | `73be4bc2669545be5b4357058fcf446eb461787c` |
| Baseline snapshot | S5-AUTONOMOUS-OPS-LOOP-REFRESH-DAY1-CLOSEOUT-2026-04-19-001 |
| Baseline stage | s5-autonomous-ops-loop-refresh-day1-closeout |
| Baseline manifest status | PASS |
| Baseline release artifact | `releases\secupilot-S5-AUTONOMOUS-OPS-LOOP-REFRESH-DAY1-CLOSEOUT-2026-04-19-001.zip` |
| Baseline release sha256 | `d10d9f2f6cb24db0dd5ccf14e8ee770416e81026f151f8af13640191290518f1` |

## 2. Purpose

This stage defines the governed multi-tool autonomous closed loop for:

- Codex autonomous operation loop
- VS Code local workspace
- Claude Code review path through the user-configured `cc switch` API tool
- Claude Web external review path running in the user's AdsPower browser/profile

This stage does not execute the full toolchain. It defines capability boundaries, commands, review paths, failure modes, HOLD rules, and authorization lanes before any later autonomous toolchain execution claim.

## 3. Tool Roles

| Tool | Role |
| --- | --- |
| Codex automation | Scheduler, planner, and executor within active policy limits. |
| VS Code workspace | Local editing and workspace surface; not long-term product memory. |
| Claude Code via `cc switch` API tool | Candidate review-only and possible non-interactive review runner after command/API format and behavior are verified. |
| Claude Web in AdsPower browser/profile | External review path; user-confirmed current surface is AdsPower, but it is not assumed automatable until verified by a governed safe path. |

Repo-governed docs, manifest, snapshots, route decisions, closeouts, and periodic reviews remain product memory. Chat windows and local tool sessions are execution context.

## 4. Allowed Flow

1. Codex automation starts run.
2. Reads `docs\DELEGATED_APPROVER_CHARTER.md` and verifies `delegation_expires`.
3. Loads the eight core governance docs.
4. Selects one item.
5. Classifies lane.
6. If Green/Yellow docs-only, drafts or prepares within allowed files.
7. If review is needed, routes to Claude Code through the `cc switch` API tool only after review-only command/API behavior is verified, or produces a Claude Code review prompt and HOLDs for human/tool execution.
8. If Claude Web or external review is needed, prepares an AdsPower/Claude Web prompt for manual transfer or HOLDs if the automation path is not verified.
9. If gate is allowed, runs the closeout gate only when authorized by the current stage and lane rules.
10. During day 1, staging, commit, and push still require explicit human confirmation.

## 5. Current Tool Status

| Area | Current status |
| --- | --- |
| Codex automation | ACTIVE only within the authorization window and policy limits. |
| VS Code CLI | Visible as `code.cmd` by safe local command detection. |
| Claude Code via `cc switch` API tool | User-confirmed candidate access path, but the current verification found no local `cc` command or alias. `claude.exe` is visible but is not treated as the governed `cc switch` automation path. |
| Codex CLI | Visible as `codex.exe` by safe local command detection. |
| AdsPower browser/profile | User-confirmed Claude Web surface; Local API authentication and already-active profile CDP connection are verified for a harmless prompt round trip. Profile launch, profile switching, login automation, and session inspection remain unverified. |
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

Current maturity claim: AdsPower / Claude Web path is L3 for a harmless review-prompt round trip through an already-active profile. Codex, VS Code, and Codex CLI remain local-tool L1. Claude Code through `cc switch` remains HOLD/L1-manual because no local `cc` command/API invocation was discoverable and non-interactive review behavior is not verified. The full four-tool autonomous closed loop is not verified.

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

The loop may reference AdsPower Claude Web verification docs for safe review-prompt transfer only. It must not claim full four-tool automation while AHQ-020 remains HOLD for `cc switch` non-interactive Claude Code review.

Standing Green docs-only closeout is allowed only after the ops-loop refresh stage itself closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push, and only under the exact Green docs-only closeout rule in `docs\AUTONOMOUS_OPS_LOOP_REFRESH_AND_DAY1_CLOSEOUT.md`.

## 7.3 CC Switch Claude Code Verification Result

`S5-CC-SWITCH-CLAUDE-CODE-REVIEW-AUTOMATION-VERIFICATION-2026-04-19-001` attempted only non-secret local discovery for the governed `cc switch` Claude Code review-only path.

Result:

- no local `cc` command or PowerShell alias was available
- `where.exe cc` found no match
- `claude.exe` was visible but is not the governed `cc switch` API path for this stage
- no harmless non-interactive review-only request was submitted
- no parseable review result was returned
- AHQ-020 remains `HOLD_FOR_TOOL_VERIFICATION`

The stage does not verify Claude Code edits, implementation, code execution, staging, commit, push, Red execution, launch/deploy, real data, external pilot execution, or full four-tool automation.

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
- AdsPower/browser launch, profile control, or browser automation
- Claude Web login or account/session handling
- staging, commit, or push
- full gate or release packaging unless explicitly authorized after review
