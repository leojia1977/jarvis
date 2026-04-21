# Mini SWE Agent WSL2 No-Write Dry Run Verification

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Mini SWE Agent WSL2 No-Write Dry Run Verification |
| Status | Green docs-only WSL2 no-write dry-run verification draft |
| Scope | Verify a bounded WSL2 mini-swe-agent runner path without product mutation |
| Snapshot | S5-MINI-SWE-AGENT-WSL2-NO-WRITE-DRY-RUN-VERIFICATION-2026-04-21-001 |
| Stage | s5-mini-swe-agent-wsl2-no-write-dry-run-verification |
| Baseline commit | `e30336adf8ddce098391bd86954a560858a62df6` |
| Baseline snapshot | S5C-IMPL12-REOPEN-LIFECYCLE-AUDIT-IMPLEMENTATION-CLOSEOUT-2026-04-21-001 |
| Baseline stage | s5c-impl12-reopen-lifecycle-audit-implementation-closeout |
| Baseline manifest status | PASS |
| Baseline release sha256 | `d6bf3675262d4df166f73fcba4ebb48f721bec90a094324553753977bf95b055` |
| Route | `OPEN_MINI_SWE_AGENT_WSL2_NO_WRITE_DRY_RUN_VERIFICATION_STAGE` |
| Lane | Green docs-only tool capability verification |

This stage verifies a bounded mini-swe-agent WSL2 runner path. It does not authorize SWE agent execution against product work, Yellow backlog participation, model-backed implementation, code/test changes, dependency changes in the repo, staging, commit, or push by itself.

## 2. Official Reference Baseline

Microsoft WSL documentation identifies `wsl --install`, `wsl --list --online`, and named distributions as the official install/listing mechanism. The selected distro is `Ubuntu-24.04`, installed as a named WSL2 distro:

```text
SecuPilotUbuntu2404
```

mini-swe-agent official documentation identifies `pip install mini-swe-agent` as the installation path and `mini` / `mini-extra` as command entrypoints. This stage uses those references only for an isolated WSL tool venv and a harmless no-write verification.

## 3. Startup Preconditions Checked

| Check | Result |
| --- | --- |
| `docs\DELEGATED_APPROVER_CHARTER.md` readable | PASS |
| `delegation_expires` | `2026-05-06 23:59 Asia/Shanghai`, not passed |
| Baseline manifest | `S5C-IMPL12-REOPEN-LIFECYCLE-AUDIT-IMPLEMENTATION-CLOSEOUT-2026-04-21-001`, `PASS` |
| Git status before verification | clean except known unrelated untracked `CLAUDE.md` and `SecuPilot_阶段性总结_20260409.md` |
| Existing out-of-scope files | not touched, not staged |

## 4. WSL2 Provisioning Evidence

User authorized Codex to provision `Ubuntu-24.04` WSL2 or an equivalent PTY runner for this verification stage.

| Probe | Result |
| --- | --- |
| WSL install route | `wsl.exe --install Ubuntu-24.04 --name SecuPilotUbuntu2404 --no-launch` succeeded |
| WSL distro list | `SecuPilotUbuntu2404`, version 2 |
| Normal Linux user | `secupilot` created and used for tool execution |
| WSL repo path | `/mnt/d/产品设计/New folder` exists |
| Python | `Python 3.12.3` |
| Git | `git version 2.43.0` |
| pip / venv support | available after bounded WSL package setup |
| mini-swe-agent install path | `/home/secupilot/.venvs/mini-swe-agent` |
| mini-swe-agent version | `2.2.8` |
| CLI entrypoints | `mini`, `mini-swe-agent`, `mini-extra`, `mini-e` |
| WSL terminal state after verification | `SecuPilotUbuntu2404` terminated and stopped |

The WSL warning about localhost proxy configuration not being mirrored into WSL NAT mode was observed. It did not block package installation or the deterministic no-write dry run. Future model-backed callbacks or network-dependent agent runs must re-check proxy/network behavior and HOLD if ambiguous.

## 5. No-Write Dry Run Evidence

The dry run used a deterministic mini-swe-agent test model and wrote the trajectory only under WSL `/tmp`, outside the repo:

```text
/tmp/secupilot-mini-swe-no-write/no_write_config.yaml
/tmp/secupilot-mini-swe-no-write/trajectory.json
```

Invocation shape:

```text
MSWEA_CONFIGURED=true /home/secupilot/.venvs/mini-swe-agent/bin/mini --agent-class default --model-class deterministic -c /tmp/secupilot-mini-swe-no-write/no_write_config.yaml -o /tmp/secupilot-mini-swe-no-write/trajectory.json -t "SecuPilot mini-SWE no-write dry run..." --exit-immediately
```

The deterministic model output contained exactly one action:

```text
echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT
```

Observed trajectory facts:

| Field | Value |
| --- | --- |
| `trajectory_exists` | `True` |
| `exit_status` | `Submitted` |
| `mini_version` | `2.2.8` |
| `api_calls` | `1` |
| `instance_cost` | `0.0` |
| `environment_cwd` | `/mnt/d/产品设计/New folder` |
| `commands` | `['echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT']` |

Before/after repo status stayed unchanged except known unrelated untracked files.

The raw trajectory remains outside the repo by design. It is ephemeral tool-run evidence under WSL `/tmp`, not product evidence, and the dry run contains no product patch, no customer/operator data, and no secret material. This governed doc records the bounded parsed facts needed for review. Future model-backed or product-task runs must define whether any trajectory, log, or summary is retained before execution; absent that decision, HOLD.

## 6. Capability Decision

AHQ-024 may advance from:

```text
HOLD_PENDING_HUMAN_WSL2_USER_DISTRO_PROVISIONING
```

to:

```text
VERIFIED_NO_WRITE_DRY_RUN_WITH_LIMITS
```

Meaning:

- a normal WSL2 distro runner exists for this project
- mini-swe-agent is installed in an isolated WSL user venv
- the `mini` main entrypoint is callable non-interactively through WSL
- a deterministic no-write main-agent dry run completed with parseable trajectory output
- repo-root working directory mapping was proven
- no repo file mutation, staged files, remote action, browser action, real-data access, or credential access occurred

This is a limited capability. It verifies runner mechanics only. It does not prove model-backed product implementation, prompt-injection resistance for real tasks, safe patch generation, or Yellow backlog compatibility for any concrete product item.

## 7. Future Allowed Role

After this stage closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push, SWE agent / mini-swe-agent may be referenced only as:

```text
bounded future implementation accelerator
```

It may be used only if a later Yellow implementation ticket explicitly names SWE agent and defines:

- exact repo root
- exact allowed files
- exact allowed behavior
- exact required tests
- exact maximum change budget
- exact no-secret and no-real-data boundary
- exact output review path
- Codex-owned orchestration and closeout
- independent review after generated output
- full gate and release verification before closeout

If any item omits these controls, SWE agent remains unavailable for that item.

## 8. Still Not Verified

This stage does not verify:

- model-backed mini-swe-agent implementation
- use of real model API keys or tokens
- secret provisioning for model calls
- WSL proxy/NAT behavior for model-backed callbacks
- patch generation against product code
- file write confinement under real implementation prompts
- exact file-scope enforcement for a live Yellow item
- prompt-injection resistance for implementation tasks
- test execution by SWE agent
- dependency installation for product code
- review replacement
- route selection
- manifest/gate/release ownership
- staging, commit, push, PR creation, or remote actions

## 9. HOLD Conditions For Any Future SWE Agent Use

HOLD immediately if future SWE agent use:

- is not explicitly named by the current Yellow item
- requires unlisted files
- requires model API credentials without a governed non-secret provisioning path
- requires network/model callbacks while WSL proxy/NAT behavior is ambiguous
- prints, reads, logs, stores, or summarizes secrets
- touches real data, customer/operator evidence, credentials, browser sessions, cookies, tokens, auth headers, or profile files
- writes outside exact file scope
- creates staged files unexpectedly
- modifies dependencies, fixtures, runtime/API/schema, release scripts, contracts, or AI_COLLAB
- attempts route selection, review replacement, manifest update, gate ownership, release ownership, staging, commit, push, or PR creation
- produces ambiguous output
- triggers Red, Red-3, launch, deployment, external pilot, public endpoint, S5-B/S5-D, ORDIV, or evidence-retention concerns

## 10. Product Development Interaction

This stage does not block ordinary Codex/VS Code product development. It also does not permit SWE agent to join the existing YB-06 or YB-07 implementation flow unless a later governed route explicitly amends those items.

Recommended next toolchain route after this closeout:

```text
OPEN_SWE_AGENT_YELLOW_BACKLOG_TEMPLATE_INTEGRATION_STAGE
```

That later Green docs-only route may add the bounded accelerator role to future Yellow backlog templates. It must not enable SWE agent for current or past Yellow items retroactively.

## 11. Non-Authorization

This stage does not authorize:

- SWE agent execution against product work
- SWE agent integration into existing Yellow backlog items
- model-backed implementation
- implementation assistance
- code changes
- test changes
- dependency changes in the repo
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
