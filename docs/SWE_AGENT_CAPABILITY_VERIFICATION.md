# SWE Agent Capability Verification

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | SWE Agent Capability Verification |
| Status | Green docs-only capability verification draft |
| Scope | Verify whether SWE agent can be used as a bounded future implementation accelerator |
| Snapshot | S5-SWE-AGENT-CAPABILITY-VERIFICATION-2026-04-21-001 |
| Stage | s5-swe-agent-capability-verification |
| Baseline commit | `96aea6cd0b9dc65e913896eab9978b345787f208` |
| Baseline snapshot | S5-NEXT-YELLOW-BACKLOG-PREAUTHORIZATION-2026-04-21-001 |
| Baseline stage | s5-next-yellow-backlog-preauthorization |
| Baseline manifest status | PASS |
| Baseline release sha256 | `02ffbfa63dbab0dcb00b39980c9ee7641d5958b6d2b66097fec6d033e46388b5` |
| Route | `OPEN_SWE_AGENT_CAPABILITY_VERIFICATION_STAGE` |
| Lane | Green docs-only tool capability verification |

This stage verifies only local SWE agent availability and whether a safe future verification route can be named. It does not install SWE agent, execute SWE agent, modify code/tests, or add SWE agent to any Yellow backlog template.

## 2. Verification Question

Can SWE agent be moved from:

```text
NOT_INSTALLED_OR_NOT_VERIFIED
```

to:

```text
VERIFIED_AS_BOUNDED_FUTURE_ACCELERATOR
```

Answer:

```text
NO - HOLD_FOR_TOOL_INSTALL_AND_VERIFICATION
```

Reason: no governed local SWE agent command, package, or Python module is available in the current workspace environment.

## 3. Local Discovery Evidence

Discovery was non-secret and read-only. No install, network package pull, agent execution, repo mutation, dependency change, or code/test edit was performed.

Known unrelated untracked files remained out of scope and were not touched:

- `CLAUDE.md`
- `SecuPilot_阶段性总结_20260409.md`

| Probe | Result |
| --- | --- |
| `Get-Command sweagent,swe-agent,swe,sweagent-run,swe-agent-run` | no command found |
| `where.exe sweagent` | no match |
| `where.exe swe-agent` | no match |
| `where.exe swe` | no match |
| `where.exe sweagent-run` | no match |
| `where.exe swe-agent-run` | no match |
| `py -3 -m pip show swe-agent sweagent` | no installed package found |
| Python module lookup: `sweagent` | missing |
| Python module lookup: `swe_agent` | missing |
| Python module lookup: `sweagent_run` | missing |

Current capability result:

```text
SWE_AGENT_NOT_INSTALLED_OR_NOT_DISCOVERABLE
```

## 4. Capability Decision

SWE agent remains:

```text
HOLD_FOR_TOOL_INSTALL_AND_VERIFICATION
```

This stage does not claim:

- installed SWE agent
- callable SWE agent command
- bounded implementation acceleration
- sandboxed SWE agent execution
- read-only or patch-only behavior
- repo-root confinement
- network confinement
- file-write controls
- test execution controls
- staging/commit/push controls
- prompt-injection resistance
- compatibility with the autonomous Yellow backlog flow

## 5. Required Future Unblock Route

A later route may attempt capability verification only if it explicitly governs installation or a preinstalled command path.

Required future route:

```text
OPEN_SWE_AGENT_INSTALL_AND_CAPABILITY_VERIFICATION_STAGE
```

Required future evidence before SWE agent can be called `VERIFIED_AS_BOUNDED_FUTURE_ACCELERATOR`:

1. Exact install or command path is governed.
2. Tool version is captured without exposing secrets.
3. Tool is confined to `D:\产品设计\New folder`.
4. Tool cannot touch files outside an exact allowed file set.
5. Tool cannot stage, commit, push, force-push, or rewrite history.
6. Tool cannot install dependencies unless a separate governed dependency route allows it.
7. Tool cannot access secrets, credentials, real data, browser sessions, or external systems.
8. Tool can produce a reviewable patch plan or patch suggestion without applying changes, or can apply changes only under an exact Yellow item file scope.
9. Before/after `git status --short` is captured.
10. A harmless synthetic dry run is completed with no unexpected file mutation.
11. Any mutation mode is proven reversible and limited before being allowed in future Yellow tickets.
12. External review confirms the bounded role.

If any item cannot be proven, SWE agent remains HOLD.

## 6. Allowed Future Role After Separate PASS

Only after a later governed verification stage PASS may SWE agent be considered for this role:

```text
bounded implementation accelerator
```

Meaning:

- may assist only inside an exact scoped Yellow item
- may only operate on exact allowed files
- may not choose product route or scope
- may not decide lane authority
- may not be final reviewer
- may not own manifest, gate, package, release verification, staging, commit, or push
- may not touch Red-3, launch, deployment, public endpoint, credentials, real data, S5-B/S5-D, ORDIV, or AI_COLLAB

SWE agent must never be treated as:

- independent product/governance decision maker
- autonomous closeout owner
- release authority
- Red approver
- unrestricted coding agent
- replacement for Codex orchestration, Claude Code review-only, Claude Web/external review, or human/jarvis approval

## 7. Current Effect On Yellow Backlog

No current Yellow backlog item may use SWE agent.

Specifically, this stage does not modify:

- `docs\NEXT_YELLOW_BACKLOG_PREAUTHORIZATION.md`
- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_05`
- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_06`
- `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_07`

The next Yellow item remains executable by the existing Codex/VS Code governed path only.

## 8. HOLD Conditions

HOLD if any future SWE agent route:

- requires credentials, tokens, cookies, browser sessions, API keys, or raw secrets
- needs real data or customer/operator evidence
- needs dependency installation without a governed dependency decision
- cannot prove repo-root confinement
- cannot prove exact file-scope confinement
- writes files outside exact scope
- modifies generated artifacts, fixtures, release scripts, contracts, or AI_COLLAB unexpectedly
- stages, commits, pushes, rewrites history, opens PRs, or touches remotes
- runs broad commands outside an exact ticket test list
- launches browsers, AdsPower profiles, Claude Web login, or external systems
- attempts launch, deployment, public endpoint activation, S5-B/S5-D reopen, ORDIV work, or Red-3 action
- produces ambiguous output

## 9. Non-Authorization

This stage does not authorize:

- SWE agent installation
- SWE agent execution
- SWE agent integration into autonomous loop
- SWE agent use in Yellow backlog items
- code changes
- test changes
- dependency changes
- fixture changes
- runtime/API/schema changes
- release script changes
- contract changes
- AI_COLLAB changes
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
