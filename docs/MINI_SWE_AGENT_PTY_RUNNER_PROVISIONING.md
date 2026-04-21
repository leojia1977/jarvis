# Mini SWE Agent PTY Runner Provisioning

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Mini SWE Agent PTY Runner Provisioning |
| Status | Green docs-only PTY runner provisioning decision draft |
| Scope | Decide the safe runner provisioning route for mini-swe-agent no-write dry-run verification |
| Snapshot | S5-MINI-SWE-AGENT-PTY-RUNNER-PROVISIONING-2026-04-21-001 |
| Stage | s5-mini-swe-agent-pty-runner-provisioning |
| Baseline commit | `839392406907824cbbf7b3320f3cd3479aaba0be` |
| Baseline snapshot | S5-MINI-SWE-AGENT-NONINTERACTIVE-DRY-RUN-VERIFICATION-2026-04-21-001 |
| Baseline stage | s5-mini-swe-agent-noninteractive-dry-run-verification |
| Baseline manifest status | PASS |
| Baseline release sha256 | `4b88b134fdfbb13f380f07d842bb0c702b8da90b9d87112cce624f5c3a470eab` |
| Route | `OPEN_MINI_SWE_AGENT_PTY_RUNNER_PROVISIONING_STAGE` |
| Lane | Green docs-only tool provisioning decision |

This stage decides the safe provisioning route for a future mini-swe-agent no-write dry run. It does not install a WSL distribution, install a PTY runner, run mini-swe-agent against product work, modify code/tests, or add SWE agent to Yellow backlog execution.

## 2. Official Reference Baseline

Official Microsoft WSL documentation identifies `wsl --install` as the install entry and `wsl --list --online` as the command for listing available distributions. Official mini-swe-agent documentation identifies `mini-swe-agent` as the recommended SWE-agent family tool and documents user-level install options.

This stage uses those references only to select a future governed provisioning route. It does not perform installation.

## 3. Local Provisioning Discovery

Discovery was non-secret and bounded. No system install, WSL distro install, PTY runner install, model-backed agent task, patch task, implementation, repo dependency edit, code/test edit, staging, commit, push, browser operation, credential read, real-data access, or external-system action was performed.

Known unrelated untracked files remained out of scope and were not touched:

- `CLAUDE.md`
- `SecuPilot_阶段性总结_20260409.md`

| Probe | Result |
| --- | --- |
| `wsl.exe --status` | default distribution remains `docker-desktop`; default version is 2 |
| `wsl.exe --version` | WSL version `2.6.3.0`; kernel `6.6.87.2-1`; Windows `10.0.26200.8246` |
| `wsl.exe -l -v` | only `docker-desktop` is listed; it was stopped |
| `wsl.exe --list --online` | online distro list is reachable; includes `Ubuntu`, `Ubuntu-24.04`, `Ubuntu-22.04`, `Debian`, and others |
| `Get-Command winget` | `winget.exe` visible |
| `Get-Command winpty` | no command found |
| `Get-Command wt` | Windows Terminal launcher visible, not accepted as noninteractive PTY runner |
| `Get-Command conhost` | `conhost.exe` visible, not accepted as governed noninteractive PTY runner |
| `Get-Command mini` / `mini-swe-agent` | no PATH command found |
| `py -3 -m pip show mini-swe-agent` | user package present at version `2.2.8` |
| Before/after `git status --short -b` | unchanged except known unrelated untracked files |

Negative-action record: `wsl --install`, `winget install Ubuntu-24.04`, and all equivalent automated distro-provisioning or PTY-runner install commands were not invoked by Codex. Provisioning is deferred to the human operator.

## 4. Provisioning Decision

Selected future provisioning route:

```text
HUMAN_CONTROLLED_WSL2_USER_DISTRO_FIRST
```

Recommended distro:

```text
Ubuntu-24.04
```

Reason:

- a normal user-controlled WSL2 distro provides a real PTY-style Linux shell and predictable Python/toolchain setup
- `docker-desktop` is not appropriate for governed product-tool execution
- `winpty` is not currently installed
- `wt.exe` / `conhost.exe` visibility alone does not provide a governed noninteractive PTY route
- installing a WSL distro or PTY runner is a host/toolchain change and should remain human-controlled unless a later explicit governed install route authorizes Codex to execute it

This stage keeps SWE agent status as:

```text
HOLD_PENDING_HUMAN_WSL2_USER_DISTRO_PROVISIONING
```

## 5. Human-Controlled Provisioning Checklist

If the human chooses to provision WSL2 for this route, the recommended manual path is:

1. Install a normal user-controlled WSL2 distro such as `Ubuntu-24.04`.
2. Complete first-run user creation in that distro.
3. Confirm distro inspection works, for example with `wsl.exe -d Ubuntu-24.04 --status` or equivalent.
4. Confirm the repo path is visible from WSL.
5. Confirm proxy/NAT behavior is understood before package fetch or model-backed callbacks.
6. Install Python tooling inside WSL only through a governed toolchain route.
7. Install `mini-swe-agent` inside WSL only through a governed toolchain route.
8. Do not put secrets into repo, chat, prompts, review packs, logs, shell history, or dotfiles.

This checklist is for human/toolchain preparation only. It is not an instruction for Codex to run install commands.

## 6. Future Verification Route

After a normal WSL2 user distro or governed PTY runner exists, open:

```text
OPEN_MINI_SWE_AGENT_WSL2_NO_WRITE_DRY_RUN_VERIFICATION_STAGE
```

That later stage must prove:

1. Exact runner path and version.
2. Exact mini-swe-agent command path and version.
3. PATH resolution or absolute-path invocation before main-agent attempt.
4. Repo path mapping and repo-root confinement.
5. No secret values printed, read, logged, or committed.
6. Before/after `git status --short` captured.
7. Harmless synthetic no-write dry run completed.
8. No file mutation, staged files, remote actions, repo dependency installs, browser actions, real data, or credential access.
9. Output is parseable and bounded.
10. External review confirms the bounded role.

If any item cannot be proven, SWE agent remains HOLD.

## 6.1 Manifest Draft Convention

The release manifest remains in the established pre-gate draft state for this stage: `current_release_sha256` and `last_verified_at` are `null`, and verification fields remain `PENDING_FULL_GATE_AFTER_REVIEW` until full gate and release verification pass. This stage does not add a new manifest schema field because manifest schema changes require a separate scoped release-process route.

## 7. Product Development Interaction

This tool-provisioning stage does not block existing Codex/VS Code product development.

However, because a new product PRD is expected soon, the recommended product-development posture after this stage is:

```text
WAIT_FOR_NEW_PRD_THEN_OPEN_PRD_INTAKE_AND_ROUTE_REBASE
```

If the new PRD is not available by the next autonomous product-development selection run, the existing preauthorized `S5C-YB-05` route remains available under its exact file/test/HOLD conditions. Do not start a new Yellow implementation that could conflict with the imminent PRD unless product/governance explicitly chooses to proceed.

## 8. Current Effect On Yellow Backlog

No current Yellow backlog item may use SWE agent.

The current preauthorized Yellow backlog remains governed by existing Codex/VS Code paths only:

- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_05`
- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_06`
- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_07`

This stage does not modify their allowed files, tests, HOLD conditions, or anti-overengineering rules.

## 9. Non-Authorization

This stage does not authorize:

- WSL distro installation by Codex
- PTY runner installation by Codex
- Python or mini-swe-agent installation inside WSL
- SWE agent execution against product work
- SWE agent integration into Yellow backlog items
- implementation assistance
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
