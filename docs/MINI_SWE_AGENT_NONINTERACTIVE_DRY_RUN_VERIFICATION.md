# Mini SWE Agent Noninteractive Dry Run Verification

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Mini SWE Agent Noninteractive Dry Run Verification |
| Status | Green docs-only capability verification draft |
| Scope | Verify WSL2 or PTY-capable no-write dry-run path for mini-swe-agent |
| Snapshot | S5-MINI-SWE-AGENT-NONINTERACTIVE-DRY-RUN-VERIFICATION-2026-04-21-001 |
| Stage | s5-mini-swe-agent-noninteractive-dry-run-verification |
| Baseline commit | `262dc49081ff4d41b0ae425536b098e53a218136` |
| Baseline snapshot | S5-SWE-AGENT-INSTALL-CAPABILITY-VERIFICATION-2026-04-21-001 |
| Baseline stage | s5-swe-agent-install-capability-verification |
| Baseline manifest status | PASS |
| Baseline release sha256 | `e0dfea31a06b336aeb093c0fba2b230b9bd8e8decde37c6d3db38853fc69ad96` |
| Route | `OPEN_MINI_SWE_AGENT_NONINTERACTIVE_DRY_RUN_VERIFICATION_STAGE` |
| Lane | Green docs-only tool capability verification |

This stage verifies whether mini-swe-agent can run a harmless no-write dry run through WSL2 or another PTY-capable runner. It does not authorize SWE agent execution against product tasks, code/test changes, dependency changes, Yellow backlog integration, staging, commit, or push by itself.

## 2. Verification Question

Can mini-swe-agent advance from:

```text
PARTIAL_VERIFIED_INSTALL_HELP_ONLY_EXECUTION_HOLD
```

to:

```text
VERIFIED_AS_BOUNDED_FUTURE_ACCELERATOR
```

Answer:

```text
NO - HOLD_WSL_PTY_DRY_RUN_NOT_AVAILABLE
```

Reason: no suitable WSL2 user distro, PTY-capable runner, or Windows invocation path was available to complete a harmless no-write main-agent dry run.

## 3. Local Discovery Evidence

Discovery was non-secret and bounded. No model-backed agent task, patch task, implementation, repo dependency edit, code/test edit, staging, commit, push, browser operation, credential read, real-data access, or external-system action was performed.

Known unrelated untracked files remained out of scope and were not touched:

- `CLAUDE.md`
- `SecuPilot_阶段性总结_20260409.md`

| Probe | Result |
| --- | --- |
| `wsl.exe --status` | WSL default distribution is `docker-desktop`; default version is 2 |
| `wsl.exe -l -v` | only `docker-desktop` is listed; it was stopped |
| `wsl.exe sh -lc "..."` | shell started inside docker-desktop context as `root` |
| WSL path | repo mapped as `/mnt/host/d/产品设计/New folder` |
| WSL shell tools | `bash` unavailable; `PATH` empty in the probed shell |
| WSL Python / mini-swe-agent | no usable `python3`, `pip`, `pip3`, `mini`, or `mini-swe-agent` path found |
| WSL warning | localhost proxy configuration detected but not mirrored into WSL NAT mode; future provisioning must treat proxy/NAT behavior as a network-boundary consideration before package fetch or model-backed callbacks |
| `Get-Command winpty` | no command found |
| `Get-Command wt` | Windows Terminal launcher visible, not a controllable noninteractive PTY runner in this stage |
| `Get-Command conhost` | `conhost.exe` visible, not sufficient through this noninteractive tool execution path |
| `cmd.exe /c "...mini.exe --help"` | still fails with `NoConsoleScreenBufferError` |
| `cmd.exe /c "...mini-swe-agent.exe --help"` | still fails with `NoConsoleScreenBufferError` |
| `TERM=xterm-256color` / `PROMPT_TOOLKIT_NO_CPR=1` | still fails; error suggests `winpty` or a real `cmd.exe` console |
| Before/after `git status --short -b` | unchanged except known unrelated untracked files |

## 4. Capability Decision

Current SWE agent status:

```text
HOLD_WSL_PTY_DRY_RUN_NOT_AVAILABLE
```

Meaning:

- Windows user-level `mini-swe-agent` remains installed and help/import evidence remains valid from the prior stage.
- The current Codex noninteractive Windows shell still cannot run the main agent entrypoint.
- The available WSL context is docker-desktop, not a governed user distro suitable for tool execution.
- No PTY runner such as `winpty` is available.
- No harmless no-write main-agent dry run was completed.
- No repo-root confinement, exact file-scope confinement, mutation control, or Yellow backlog compatibility was proven.

This stage does not unlock SWE agent as a bounded implementation accelerator.

## 5. Why WSL2 Is Not Sufficient Yet

The only discovered WSL2 distribution is `docker-desktop`. It is not a normal user-controlled Ubuntu/Debian-style distro for governed repo tooling. The probed shell lacked `bash`, had an empty `PATH`, did not expose a usable Python/mini-swe-agent toolchain, and produced a WSL NAT proxy warning.

This is not a safe base for autonomous product-development tooling because it cannot satisfy:

- exact install path governance
- stable user identity / workspace expectations
- predictable Python/toolchain availability
- safe repo-root confinement
- no-write dry-run reproducibility
- reviewable command sequence

Future WSL provisioning must explicitly resolve or document localhost proxy/NAT behavior before any network package fetch, model-backed callback, or agent execution attempt.

## 6. Why Windows PTY Is Not Sufficient Yet

The existing Windows Python package remains visible, but the main agent entrypoint fails before help because `prompt_toolkit` cannot access a Windows console screen buffer from the current noninteractive tool channel.

Attempts through `cmd.exe /c` and terminal-related environment variables did not resolve the error. `winpty` is not installed. `wt.exe` and `conhost.exe` visibility alone is not a governed noninteractive PTY runner and was not used to launch agent work.

## 7. Required Future Unblock Route

Required future route before any SWE agent dry-run retry:

```text
OPEN_MINI_SWE_AGENT_PTY_RUNNER_PROVISIONING_STAGE
```

Acceptable future approaches:

1. Install/provision a normal WSL2 user distro such as Ubuntu with explicit workspace path mapping, Python, and mini-swe-agent install governance.
2. Install/provision a Windows PTY bridge such as `winpty` or an equivalent governed PTY runner.
3. Identify an official mini-swe-agent noninteractive mode that bypasses prompt-toolkit console-buffer requirements.

Future route must prove:

1. Exact runner path and version.
2. Exact mini-swe-agent command path and version.
3. PATH resolution or absolute-path invocation before main-agent attempt.
4. No secret values printed, read, logged, or committed.
5. Before/after `git status --short` captured.
6. Harmless synthetic no-write dry run completed.
7. No file mutation, staged files, remote actions, dependency installs in repo, browser actions, real data, or credential access.
8. Output is parseable and bounded.
9. External review confirms the bounded role.

Manifest draft control records the same future route preconditions under `future_route.preconditions`, and records `verification.hold_reason` while the stage remains pending full gate.

If any item cannot be proven, SWE agent remains HOLD.

## 8. Current Effect On Yellow Backlog

No current Yellow backlog item may use SWE agent.

The current preauthorized Yellow backlog remains governed by existing Codex/VS Code paths only:

- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_05`
- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_06`
- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_07`

This stage does not modify their allowed files, tests, HOLD conditions, or anti-overengineering rules.

## 9. HOLD Conditions

HOLD if any future SWE agent route:

- lacks a normal user-controlled WSL2 distro or governed PTY runner
- cannot run from the governed automation environment
- cannot prove PATH resolution or explicit absolute-path invocation
- requires interactive console behavior automation cannot provide
- requires secrets, tokens, cookies, browser sessions, API keys, or raw credentials
- needs real data or customer/operator evidence
- needs dependency installation without a governed dependency decision
- cannot prove repo-root confinement
- cannot prove exact file-scope confinement
- writes files unexpectedly
- stages, commits, pushes, rewrites history, opens PRs, or touches remotes
- launches browsers, AdsPower profiles, Claude Web login, or external systems
- attempts launch, deployment, public endpoint activation, S5-B/S5-D reopen, ORDIV work, or Red-3 action
- produces ambiguous output

## 10. Non-Authorization

This stage does not authorize:

- SWE agent execution against product work
- SWE agent integration into Yellow backlog items
- implementation assistance
- WSL distro installation
- PTY runner installation
- dependency changes
- code changes
- test changes
- fixture changes
- runtime/API/schema changes
- release script changes
- contract changes
- AI_COLLAB changes
- review replacement
- route selection by SWE agent
- manifest/gate/release ownership by SWE agent
- launch execution
- production deployment
- external pilot execution or readiness
- credential handling
- real-data handling
- evidence retention or redaction policy changes
- public endpoint work
- S5-B/S5-D reopen
- ORDIV work
- S4-A resolver order change
- Red-3 action
- AdsPower profile creation/switching
- Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection
- staging, commit, or push before closeout rules are satisfied
