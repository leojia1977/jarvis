# SWE Agent Install And Capability Verification

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | SWE Agent Install And Capability Verification |
| Status | Green docs-only install/capability verification draft |
| Scope | Govern user-level mini-swe-agent installation visibility and safe dry-run eligibility |
| Snapshot | S5-SWE-AGENT-INSTALL-CAPABILITY-VERIFICATION-2026-04-21-001 |
| Stage | s5-swe-agent-install-capability-verification |
| Baseline commit | `eaa473d28cf3b1b029f46a240b5b1e853a00f980` |
| Baseline snapshot | S5-SWE-AGENT-CAPABILITY-VERIFICATION-2026-04-21-001 |
| Baseline stage | s5-swe-agent-capability-verification |
| Baseline manifest status | PASS |
| Baseline release sha256 | `8544ca1a09372152658507dc1ed0c96fb604a5f37e841e06b8c76100c1095405` |
| Route | `OPEN_SWE_AGENT_INSTALL_AND_CAPABILITY_VERIFICATION_STAGE` |
| Lane | Green docs-only tool capability verification |

This stage records a conservative local verification of the SWE agent candidate. It does not add SWE agent to Yellow backlog execution, does not authorize implementation, and does not authorize repo dependency changes.

## 2. Official Tool Selection

Official SWE-agent documentation states that the older SWE-agent is in maintenance mode and recommends `mini-swe-agent` for new use. The official installation page lists `mini-swe-agent` version `2.2.8` and installation options including `pipx install mini-swe-agent`, `uv tool install mini-swe-agent`, and `python -m pip install mini-swe-agent`.

Local prerequisite discovery found:

- `pipx`: not available
- `uv` / `uvx`: not available
- `py` / Python 3.14: available
- `mini-swe-agent` user package: present at verification time

The package is installed in the user Python site-packages location, not in repo dependencies. No repo dependency file was modified.

## 3. Local Verification Evidence

Discovery was non-secret and bounded. No model task, patch task, code/test implementation, repo dependency edit, staging, commit, push, browser operation, credential read, real-data access, or external system action was performed.

Known unrelated untracked files remained out of scope and were not touched:

- `CLAUDE.md`
- `SecuPilot_阶段性总结_20260409.md`

Disposition: these two files are pre-existing local/untracked orientation inputs only. They are deliberately excluded from this stage, manifest key files, release packaging scope decisions, staging, commit, and push unless a later governed route explicitly imports or retires them.

| Probe | Result |
| --- | --- |
| `py -3 -m pip --version` | pip 25.3 on Python 3.14 |
| `py -3 -m pip show mini-swe-agent` | package present, version `2.2.8`, user site-packages |
| `py -3 -m pip show pipx` | no package found |
| `Get-Command pipx,uv,uvx` | no command found |
| Entry points from package metadata | `mini`, `mini-swe-agent`, `mini-extra`, `mini-e` |
| Script location | `C:\Users\Administrator\AppData\Roaming\Python\Python314\Scripts` |
| `Get-Command mini` / PATH discovery | no PATH command found |
| `mini-extra.exe --help` | succeeded |
| `mini-extra.exe config --help` | succeeded and printed config help without secret values |
| `py -3 -c "import minisweagent"` | import succeeded, version `2.2.8` |
| `mini.exe --help` | failed before help because `prompt_toolkit` raised `NoConsoleScreenBufferError` |
| `mini-swe-agent.exe --help` | failed before help because `prompt_toolkit` raised `NoConsoleScreenBufferError` |
| Before/after `git status --short -b` | unchanged except known unrelated untracked files |

The main agent command is therefore not verified as callable from the current Codex non-interactive Windows shell.

PATH resolution is not satisfied for the main commands. A future dry-run stage must verify either PATH resolution or an explicit absolute command path before any main-agent invocation attempt.

## 4. Capability Decision

Current SWE agent status:

```text
PARTIAL_VERIFIED_INSTALL_HELP_ONLY_EXECUTION_HOLD
```

Meaning:

- the `mini-swe-agent` user package is present
- version and package import are verified
- auxiliary `mini-extra` help is callable
- the main `mini` / `mini-swe-agent` agent entrypoint is not callable in the current non-interactive shell
- no harmless no-write agent dry run was completed
- no repo-root confinement, exact file-scope confinement, or mutation control was proven
- no Yellow backlog use is allowed

This stage does not advance SWE agent to:

```text
VERIFIED_AS_BOUNDED_FUTURE_ACCELERATOR
```

## 5. Why Execution Remains HOLD

The main entrypoint imports prompt-session support before producing help. In the current Codex tool execution environment, `prompt_toolkit` cannot obtain a Windows console screen buffer and raises:

```text
NoConsoleScreenBufferError: No Windows console found. Are you running cmd.exe?
```

Because even `--help` fails for the main entrypoint, this stage cannot prove unattended agent invocation, no-write behavior, repo confinement, file-scope control, or safe synthetic dry-run behavior.

This is an environment-specific blocker for the current Codex non-interactive Windows shell. It is not recorded as a package-wide defect or as proof that `mini-swe-agent` cannot work in a compatible terminal, WSL2, PTY-capable runner, or future governed invocation environment.

## 6. Future Unblock Route

Required future route before any Yellow backlog integration:

```text
OPEN_MINI_SWE_AGENT_NONINTERACTIVE_DRY_RUN_VERIFICATION_STAGE
```

That future route must prove at least one of:

1. A Windows non-interactive invocation mode that does not require a console screen buffer.
2. A WSL2 or other governed PTY-capable route that is explicitly scoped to the repo and exact allowed files.
3. A documented mini-swe-agent mode that can generate a reviewable plan or patch proposal without writing files.

Required future evidence:

1. Exact command path and version.
2. PATH resolution or absolute-path invocation is verified before any main-agent attempt.
3. The selected shell/runner is explicitly declared compatible with mini-swe-agent's console requirements.
4. No secret values printed, read, logged, or committed.
5. Before/after `git status --short` captured.
6. Harmless synthetic no-write dry run completed.
7. No file mutation, staged files, remote actions, dependency installs, browser actions, real data, or credential access.
8. If mutation mode is ever considered later, exact file-scope confinement must be proven in a throwaway workspace before any real repo use.
9. External review confirms the bounded role.

If any item cannot be proven, SWE agent remains HOLD.

## 7. Allowed Future Role After Separate PASS

Only after a later governed PASS may SWE agent be considered as:

```text
bounded implementation accelerator
```

It would remain subordinate to Codex/VS Code and may not:

- select product route or scope
- define acceptance criteria
- expand the exact file list
- decide lane authority
- act as final reviewer
- own manifest, gate, package, release verification, staging, commit, or push
- touch Red-3, launch, deployment, public endpoint, credentials, real data, S5-B/S5-D, ORDIV, or AI_COLLAB

## 8. Current Effect On Yellow Backlog

No current Yellow backlog item may use SWE agent.

The current preauthorized Yellow backlog remains governed by existing Codex/VS Code paths only:

- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_05`
- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_06`
- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_07`

This stage does not modify their allowed files, tests, HOLD conditions, or anti-overengineering rules.

## 8.1 Manifest Draft State Note

`current_release_sha256: null`, `verification.last_verified_at: null`, and `verification.overall_status: PENDING_FULL_GATE_AFTER_REVIEW` are intentional for this draft state. They must remain pending until full gate, release package, and release verification pass. The installed version `2.2.8` is recorded in this governed document and protected by the manifest key-file hash; the manifest itself should not grow ad hoc tool-version fields because `scripts\verify_release.py` rewrites the verification object during closeout.

## 9. HOLD Conditions

HOLD if any future SWE agent route:

- cannot run from the governed automation environment
- requires interactive console behavior that automation cannot provide
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

- SWE agent execution
- SWE agent integration into Yellow backlog items
- implementation assistance
- code changes
- test changes
- dependency changes
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

## 11. Follow-Up Noninteractive Dry Run Verification

`S5-MINI-SWE-AGENT-NONINTERACTIVE-DRY-RUN-VERIFICATION-2026-04-21-001` attempted the required WSL2 / PTY-capable no-write dry-run route.

Follow-up result:

- WSL2 exists only as `docker-desktop`, not a governed user distro.
- The probed WSL shell lacked `bash`, had an empty `PATH`, and did not expose usable Python or mini-swe-agent commands.
- `winpty` was not available.
- `cmd.exe /c` did not resolve `NoConsoleScreenBufferError`.
- No harmless no-write main-agent dry run was completed.

Updated status:

```text
HOLD_WSL_PTY_DRY_RUN_NOT_AVAILABLE
```

Future route:

```text
OPEN_MINI_SWE_AGENT_PTY_RUNNER_PROVISIONING_STAGE
```
