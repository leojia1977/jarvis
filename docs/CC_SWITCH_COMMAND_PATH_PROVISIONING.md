# CC Switch Command Path Provisioning

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | CC Switch Command Path Provisioning |
| Status | Docs-only command-path provisioning draft |
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

This stage provisions and verifies a callable Claude Code review-only command path for the autonomous toolchain.

The verified path is not a raw `cc` command and is not `claude.exe`. The verified path is the npm Claude Code shim `claude.cmd` when invoked under the user's configured cc-switch environment through local non-secret references. Environment variable names may be recorded; values must never be printed, pasted into chat, committed to repo, added to prompts, or stored in logs.

This stage closes the prior AHQ-020 blocker only for non-interactive review-only verdict capture with the limits in this document and `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md`.

## 3. Route Judgment

| Route | Risk | Decision |
| --- | --- | --- |
| Treat `cc` as required command name | No local `cc` command or alias exists in the workspace. | Reject as unavailable. |
| Treat `claude.exe` as the governed path | Prior governance explicitly rejected `claude.exe` as the substitute path. | Reject. |
| Use npm shim `claude.cmd` with cc-switch environment references | Local shim exists, reports Claude Code version, and can return non-interactive review results without repo mutation. | Select with limits. |
| Use non-bare Claude Code invocation | Non-bare invocation returned stale project context unrelated to the supplied review prompt. | Reject. |
| Use command-argument multi-line prompt | Multi-line prompt passed as an argument was truncated. | Reject. |
| Use `--json-schema` strict output | `--json-schema` timed out twice and left residual node processes that required termination. | Reject / HOLD. |
| Use stdin prompt plus bare JSON wrapper and first-line verdict contract | Harmless review prompt returned parseable `VERDICT: PASS`, no tool use, no web requests, and unchanged git status. | Select as verified review-only path. |

## 4. Verification Preconditions

Before probing, Codex loaded the governed baseline and confirmed:

- branch: `codex/s3-a-runtime`
- baseline commit: `5c1d8c1e288c1e16f47279f147fc4a973064e874`
- baseline manifest snapshot: `S5-ADSPOWER-PROFILE-LAUNCH-VERIFICATION-2026-04-19-001`
- baseline manifest status: `PASS`
- worktree had only the known out-of-scope untracked files:
  - `CLAUDE.md`
  - `SecuPilot_阶段性总结_20260409.md`
- `docs\DELEGATED_APPROVER_CHARTER.md` was readable and the authorization window had not expired

## 5. Non-Secret Discovery

Discovery used only non-secret command and environment-name checks:

- `Get-Command cc,cc-switch,ccswitch,claude-code,claude,claude-code-router,ccr,codex`
- `Get-Alias cc,cc-switch,ccswitch,claude-code,claude,claude-code-router,ccr`
- `where.exe cc`
- `where.exe claude`
- npm global package inventory for Claude Code package presence
- environment variable name listing for relevant toolchain variables

Recorded facts:

- no `cc`, `cc-switch`, `ccswitch`, `claude-code`, or `ccr` command/alias was discoverable
- `claude.exe` was visible but remains rejected as the governed path
- npm shim `claude.cmd` was visible under the user npm directory
- `claude.cmd --version` returned Claude Code `2.1.86`
- the environment variable names `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` were present
- no environment variable values were printed or recorded

## 6. Verified Invocation

The verified invocation pattern is:

```text
<stdin prompt> | claude.cmd -p --bare --output-format json --tools "" --no-session-persistence --permission-mode plan --max-budget-usd 0.05
```

The prompt must be passed through stdin. The prompt must require the first line of the model result to match exactly one of:

```text
VERDICT: PASS
VERDICT: PASS_WITH_FINDINGS
VERDICT: FAIL
VERDICT: HOLD
```

The successful harmless review prompt contained no secrets, raw customer data, unredacted evidence, credentials, sessions, cookies, tokens, auth headers, browser storage, profile data, launch instructions, deployment instructions, external pilot instructions, or real-data content.

Successful evidence:

- process exit code was `0`
- wrapper output parsed as JSON
- first line of `result` parsed as `VERDICT: PASS`
- `permission_denials` count was `0`
- `web_search_requests` count was `0`
- `web_fetch_requests` count was `0`
- before/after `git status --short -b` was unchanged
- no files were staged
- known out-of-scope untracked files remained untracked

## 7. Verification Result

Final result: `VERIFIED_REVIEW_ONLY_VERDICT_LINE_WITH_LIMITS`.

AHQ-020 may advance from `HOLD_FOR_TOOL_VERIFICATION` to `VERIFIED_REVIEW_ONLY_VERDICT_LINE_WITH_LIMITS`.

This closes the callable non-interactive Claude Code review-only path blocker for Green/docs-only review prompt transfer and parseable verdict capture only. It does not authorize Claude Code to edit files, run commands, inspect secrets, stage, commit, push, approve Red work, replace required human/delegated GO, or serve as the sole independent final reviewer for stages that verify Claude Code behavior itself.

## 8. Not Verified

This stage does not verify:

- local `cc` command availability
- `claude.exe` as a governed automation path
- non-bare Claude Code review behavior
- command-argument multi-line prompt safety
- strict JSON result contract
- `--json-schema` reliability
- tool use by Claude Code
- file reads by Claude Code
- file edits by Claude Code
- command execution by Claude Code
- test execution by Claude Code
- dependency installation
- staging, commit, push, or remote actions
- authenticated account/session management beyond the already configured local environment
- use with secrets, raw customer data, unredacted evidence, real data, launch, deployment, external pilot execution, Red work, public endpoint work, S5-B/S5-D reopen, ORDIV work, or AI_COLLAB changes

## 9. Required Runtime Checks

Every future autonomous use of this path must:

1. Read `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md`.
2. Confirm the prompt contains no secrets, raw customer data, unredacted evidence, credentials, sessions, cookies, tokens, auth headers, browser storage, profile data, launch instructions, deployment instructions, or external pilot execution content.
3. Run `git status --short -b` before the request.
4. Invoke `claude.cmd` through stdin with the exact review-only flags in Section 6.
5. Parse wrapper JSON.
6. Parse the first line of `result` as a verdict line.
7. Confirm no web requests, no permission-denial escalation, and no unexpected tool behavior.
8. Run `git status --short -b` after the request.
9. Treat any file mutation, staged file, non-zero exit, timeout, ambiguous output, missing verdict line, or network ambiguity as HOLD.

## 10. Four-Tool Loop Impact

The governed toolchain may claim a limited four-tool review loop only after these gates complete in this strict order:

1. This external review returns `PASS`, or all blocking findings are fixed and focused re-review returns `PASS`.
2. Full gate returns `PASS`.
3. Release package is produced.
4. Release verification returns `PASS` and manifest verification fields are updated from PENDING to `PASS`.
5. Closeout commit is created with the exact governed file set.
6. Push to the governed branch succeeds.

No prior gate may be skipped, reordered, inferred, or satisfied retroactively. The limited four-tool review-loop entitlement may be claimed only after all six gates are complete in order.

After all six gates complete, the governed limited loop is:

1. Codex orchestrates and owns governance/gate/manifest/closeout under policy limits.
2. VS Code remains the local workspace/editing execution surface only.
3. Claude Web in AdsPower remains the external review-prompt transfer path with configured-profile launch/attach limits.
4. Claude Code through `claude.cmd` under cc-switch environment is verified only for non-interactive review-only verdict capture with the limits in this stage.

This is not full autonomous implementation. It is a limited Green/docs-only review loop. Any Yellow implementation, Red execution, launch/deploy, external pilot execution, real data, credentials, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, AI_COLLAB change, browser login/session access, or broader tool use still requires separate governed authority.

## 11. Non-Authorization

This stage does not authorize:

- code changes
- test changes
- dependency changes
- fixture changes
- runtime/API/schema changes
- release script changes
- contract changes
- AI_COLLAB changes
- Yellow implementation
- Red execution
- launch execution
- production deployment
- external pilot execution
- credential handling
- real-data handling
- public endpoint work
- S5-B/S5-D reopen
- ORDIV work
- AdsPower profile creation or switching
- Claude Web login
- cookie, session, token, auth-header, browser-storage, or profile-file inspection
- Claude Code file edits, command execution, staging, commit, push, or remote actions
- Claude Code replacing human, delegated, Claude Web, or external review where those are required
- full gate or release packaging unless separately authorized after review
- staging, commit, or push unless governed closeout rules authorize them after PASS
