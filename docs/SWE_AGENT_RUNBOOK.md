# SWE Agent Runbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | SWE Agent Runbook |
| Status | Candidate runbook; WSL2 no-write dry run verified with limits |
| Snapshot | S5-MINI-SWE-AGENT-WSL2-NO-WRITE-DRY-RUN-VERIFICATION-2026-04-21-001 |
| Stage | s5-mini-swe-agent-wsl2-no-write-dry-run-verification |
| Baseline commit | `e30336adf8ddce098391bd86954a560858a62df6` |

This runbook records the current safe boundary for SWE agent / mini-swe-agent. It does not authorize product-task agent execution, implementation, staging, commit, or push.

## 2. Current Status

Current status:

```text
VERIFIED_NO_WRITE_DRY_RUN_WITH_LIMITS
```

Verified facts:

- `SecuPilotUbuntu2404` is installed as a WSL2 `Ubuntu-24.04` distro
- normal WSL user `secupilot` exists and was used for tool execution
- repo path `/mnt/d/产品设计/New folder` is visible from WSL
- Python `3.12.3` and git `2.43.0` are available in WSL
- `mini-swe-agent` version `2.2.8` is installed in `/home/secupilot/.venvs/mini-swe-agent`
- `mini`, `mini-swe-agent`, `mini-extra`, and `mini-e` entrypoints are present in that venv
- `mini --help` is callable in WSL when `MSWEA_CONFIGURED=true` avoids first-run secret/config prompting
- a deterministic no-write main-agent dry run completed with `exit_status=Submitted`, `api_calls=1`, `instance_cost=0.0`, and a single harmless command: `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`
- trajectory/config output was written only under `/tmp/secupilot-mini-swe-no-write`, outside the repo
- before/after repo git status was unchanged except known unrelated untracked files
- WSL was terminated after verification

The WSL localhost proxy/NAT warning remains a future network consideration. Any model-backed mini-swe-agent run must re-check proxy behavior and HOLD if network or secret provisioning is ambiguous.

## 3. Allowed Commands In This State

Allowed for future Green docs-only verification and exact later Yellow items that explicitly name SWE agent:

```text
py -3 -m pip show mini-swe-agent
py -3 -c "import minisweagent, importlib.metadata as m; print(m.version('mini-swe-agent'))"
C:\Users\Administrator\AppData\Roaming\Python\Python314\Scripts\mini-extra.exe --help
C:\Users\Administrator\AppData\Roaming\Python\Python314\Scripts\mini-extra.exe config --help
wsl.exe -d SecuPilotUbuntu2404 -u secupilot -- sh -lc "MSWEA_CONFIGURED=true /home/secupilot/.venvs/mini-swe-agent/bin/mini --help"
wsl.exe -d SecuPilotUbuntu2404 -u secupilot -- sh -lc "/home/secupilot/.venvs/mini-swe-agent/bin/python -c 'import importlib.metadata as m; print(m.version(\"mini-swe-agent\"))'"
```

These commands may verify installation and help text only. They must not read or print config values, secrets, tokens, API keys, model keys, or environment variable values.

Any future main-agent use must use an explicit absolute command path unless PATH resolution is separately proven. PATH absence is a blocker, not a warning.

## 4. Prohibited Commands In This State

Do not invoke the main agent entrypoints for product work unless a later Yellow item explicitly names SWE agent and all current runbook requirements are met:

```text
mini
mini-swe-agent
mini.exe
mini-swe-agent.exe
```

The WSL no-write entrypoint is verified only for deterministic no-write dry-run mechanics. It is not verified for model-backed implementation by default.

Do not run:

- any product task prompt against the repo without an exact later Yellow item that names SWE agent
- any mutation or patch command
- any model-backed run
- any command that may install dependencies in the repo
- any command that may write trajectories, logs, cache, or generated files into the repo unless a later route governs the exact output location

## 5. Future Use Startup

Any future governed SWE-agent use must start by:

1. Reading `docs\DELEGATED_APPROVER_CHARTER.md`.
2. Verifying `delegation_expires` has not passed.
3. Loading the core governance docs.
4. Confirming latest manifest baseline is PASS.
5. Confirming clean git status except known unrelated untracked files.
6. Recording exact mini-swe-agent command path.
7. Recording exact version.
8. Recording exact test workspace and output directory.
9. Capturing before/after `git status --short`.
10. Confirming the current Yellow item explicitly names SWE agent as a bounded implementation accelerator.
11. Confirming model credential provisioning, if needed, uses a governed non-secret path and no values are printed.
12. Confirming WSL proxy/NAT behavior is safe for any network or model-backed callback; if not, HOLD.

## 6. Safe Future Use Sequence

Future SWE-agent use must proceed in this order:

1. Confirm `SecuPilotUbuntu2404` is present and stopped or in a known clean state before launch.
2. Confirm exact command path and version.
3. Confirm exact Yellow item names SWE agent and exact allowed files/tests.
4. Confirm git status is clean except known unrelated untracked files.
5. Confirm no secrets, real data, browser/session material, or external system access is needed.
6. Use explicit output paths outside the repo unless the Yellow item names otherwise.
7. Run the bounded agent step.
8. Confirm changed files match the exact item file scope.
9. Confirm no staged files were created unexpectedly.
10. Route generated output through independent review.
11. Run the exact targeted tests and full gate only under the governing item closeout rules.
12. HOLD if any step requires broader scope.

No gate may be skipped, reordered, inferred, or satisfied retroactively.

## 7. Allowed Future Use After This PASS

After this verification closes PASS, SWE agent may be proposed only as a:

```text
bounded implementation accelerator
```

Allowed only when a later Yellow item explicitly names it:

- exact repo root
- exact files
- exact behavior
- exact tests
- exact max-change budget
- no secrets
- no real data
- no Red trigger
- Codex-owned orchestration
- independent review after output
- full gate and release verification before closeout
- no staging, commit, push, PR creation, or remote action by SWE agent

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
- `SecuPilotUbuntu2404` is missing, corrupted, ambiguous, or cannot be started
- the WSL `mini` command path is missing or version cannot be captured
- WSL proxy/NAT behavior is ambiguous for a network or model-backed run
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
