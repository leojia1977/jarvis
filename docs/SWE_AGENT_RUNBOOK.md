# SWE Agent Runbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | SWE Agent Runbook |
| Status | Candidate runbook; mini-swe-agent PTY runner remains HOLD |
| Snapshot | S5-MINI-SWE-AGENT-PTY-RUNNER-PROVISIONING-2026-04-21-001 |
| Stage | s5-mini-swe-agent-pty-runner-provisioning |
| Baseline commit | `839392406907824cbbf7b3320f3cd3479aaba0be` |

This runbook records the current safe boundary for SWE agent / mini-swe-agent. It does not authorize agent execution, implementation, staging, commit, or push.

## 2. Current Status

Current status:

```text
HOLD_PENDING_HUMAN_WSL2_USER_DISTRO_PROVISIONING
```

Reason:

- `mini-swe-agent` version `2.2.8` is present in user Python site-packages
- entrypoint scripts exist under `C:\Users\Administrator\AppData\Roaming\Python\Python314\Scripts`
- `mini-extra --help` and `mini-extra config --help` are callable
- package import succeeds
- `mini --help` and `mini-swe-agent --help` fail in the current Codex non-interactive Windows shell with `NoConsoleScreenBufferError`
- WSL2 is present only as docker-desktop, not a governed user distro; no usable WSL Python or mini-swe-agent path is available
- the docker-desktop WSL probe emitted a localhost proxy/NAT warning; future WSL provisioning must resolve or document proxy behavior before package fetch, model-backed callbacks, or agent execution
- no `winpty` or governed PTY runner is available
- `wsl.exe --list --online` can see `Ubuntu-24.04`, but no normal user-controlled WSL2 distro is installed
- this stage selects human-controlled `Ubuntu-24.04` WSL2 provisioning as the preferred future route
- no harmless no-write agent dry run was completed

## 3. Allowed Commands In This State

Allowed for future Green docs-only verification only:

```text
py -3 -m pip show mini-swe-agent
py -3 -c "import minisweagent, importlib.metadata as m; print(m.version('mini-swe-agent'))"
C:\Users\Administrator\AppData\Roaming\Python\Python314\Scripts\mini-extra.exe --help
C:\Users\Administrator\AppData\Roaming\Python\Python314\Scripts\mini-extra.exe config --help
```

These commands may verify installation and help text only. They must not read or print config values, secrets, tokens, API keys, model keys, or environment variable values.

Any future main-agent verification must first prove PATH resolution or use an explicit absolute command path. PATH absence is a blocker, not a warning.

## 4. Prohibited Commands In This State

Do not invoke the main agent entrypoints for repo work:

```text
mini
mini-swe-agent
mini.exe
mini-swe-agent.exe
```

They are not verified as safe or callable for unattended automation in the current environment.

Do not run:

- any task prompt against the repo
- any mutation or patch command
- any model-backed run
- any command that may install dependencies
- any command that may write trajectories, logs, cache, or generated files into the repo unless a later route governs the exact output location

## 5. Future Verification Startup

A future governed route must start by:

1. Reading `docs\DELEGATED_APPROVER_CHARTER.md`.
2. Verifying `delegation_expires` has not passed.
3. Loading the core governance docs.
4. Confirming latest manifest baseline is PASS.
5. Confirming clean git status except known unrelated untracked files.
6. Recording exact mini-swe-agent command path.
7. Recording exact version.
8. Recording exact test workspace and output directory.
9. Capturing before/after `git status --short`.

## 6. Safe Verification Sequence

Future verification must proceed in this order:

1. Confirm official install source and version.
2. Print package/version/help only.
3. Verify PATH resolution or explicit absolute-path invocation before any main-agent attempt.
4. Declare the compatible shell/runner for mini-swe-agent's console requirements.
5. Resolve the current Codex non-interactive Windows `NoConsoleScreenBufferError` or move to a governed PTY-capable route such as a normal user-controlled WSL2 distro.
6. Run a harmless no-write or dry-run command if available.
7. Confirm no file mutation.
8. Confirm no staged files.
9. Confirm no remote action.
10. Confirm no credentials or real data are requested.
11. Confirm output is parseable and bounded.
12. Only then consider a synthetic patch-plan test in a throwaway workspace.
13. HOLD before any real repo mutation unless a separate exact Yellow ticket authorizes mutation.

No gate may be skipped, reordered, inferred, or satisfied retroactively.

## 7. Allowed Future Use After Separate PASS

After a later verification PASS, SWE agent may be proposed only as a:

```text
bounded implementation accelerator
```

Allowed only when a later Yellow item explicitly names it:

- exact repo root
- exact files
- exact behavior
- exact tests
- no secrets
- no real data
- no Red trigger
- Codex-owned orchestration
- independent review after output
- full gate and release verification before closeout

## 8. Prohibited Use

SWE agent must not:

- select product route
- expand scope
- define acceptance criteria
- approve its own output
- act as final reviewer
- own manifest updates
- own release verification
- stage, commit, push, force-push, or rewrite history
- install dependencies unless separately governed
- touch files outside exact scope
- access credentials, tokens, cookies, browser sessions, API keys, auth headers, or secrets
- process real customer/operator data
- launch browsers or AdsPower profiles
- log into Claude Web
- access external systems
- execute launch or deployment
- activate public endpoints
- reopen S5-B, S5-D, or ORDIV
- perform Red-3 action
- modify AI_COLLAB

## 9. HOLD Conditions

HOLD immediately if:

- command path is missing
- PATH resolution or explicit absolute-path invocation is not verified
- install source is ambiguous
- version cannot be captured
- the main agent command still fails before help in the automation environment
- only docker-desktop WSL is available instead of a governed user distro
- normal user-controlled WSL2 distro provisioning has not been completed
- PTY runner such as `winpty` is unavailable
- WSL localhost proxy/NAT behavior is unresolved for the proposed runner
- dry run is unavailable
- dry run mutates files unexpectedly
- command writes outside exact scope
- command stages files
- command touches remotes
- command asks for credentials or browser/session access
- output is ambiguous
- test failure requires out-of-scope fix
- any Red-3 trigger appears

## 10. Relationship To Existing Tools

SWE agent is subordinate to the existing governed workflow:

- Codex remains orchestration, gate, manifest, and closeout owner under policy limits.
- VS Code remains the local workspace/editing execution surface.
- Claude Code remains review-only verdict capture under the governed `claude.cmd` path.
- Claude Web in AdsPower remains external review-prompt path.
- Human or jarvis approval remains required where policy requires it.

SWE agent cannot replace any required review or approval.
