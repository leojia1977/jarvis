# SWE Agent Runbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | SWE Agent Runbook |
| Status | Candidate runbook; SWE agent remains HOLD |
| Snapshot | S5-SWE-AGENT-CAPABILITY-VERIFICATION-2026-04-21-001 |
| Stage | s5-swe-agent-capability-verification |
| Baseline commit | `96aea6cd0b9dc65e913896eab9978b345787f208` |

This runbook records the future safety requirements for SWE agent. It does not authorize installation, execution, implementation, staging, commit, or push.

## 2. Current Status

Current status:

```text
SWE_AGENT_HOLD_FOR_TOOL_INSTALL_AND_VERIFICATION
```

Reason:

- no local command path was found
- no Python package was found
- no Python module was found
- no harmless dry run was possible

## 3. Future Verification Startup

A future governed route must start by:

1. Reading `docs\DELEGATED_APPROVER_CHARTER.md`.
2. Verifying `delegation_expires` has not passed.
3. Loading the core governance docs.
4. Confirming latest manifest baseline is PASS.
5. Confirming clean git status except known unrelated untracked files.
6. Recording exact SWE agent command path or install source.
7. Recording exact version.
8. Recording exact allowed test workspace.
9. Capturing before/after `git status --short`.

## 4. Safe Verification Sequence

Future verification must proceed in this order:

1. Discover command/package path.
2. Print version/help only.
3. Run a harmless no-write or dry-run command if available.
4. Confirm no file mutation.
5. Confirm no staged files.
6. Confirm no remote action.
7. Confirm no credentials or real data are requested.
8. Confirm output is parseable and bounded.
9. Only then consider a synthetic patch-plan test.
10. HOLD before any real repo mutation unless a separate exact Yellow ticket authorizes mutation.

No gate may be skipped, reordered, inferred, or satisfied retroactively.

## 5. Allowed Future Use After Separate PASS

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

## 6. Prohibited Use

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

## 7. HOLD Conditions

HOLD immediately if:

- command path is missing
- install source is ambiguous
- version cannot be captured
- dry run is unavailable
- dry run mutates files unexpectedly
- command writes outside exact scope
- command stages files
- command touches remotes
- command asks for credentials or browser/session access
- output is ambiguous
- test failure requires out-of-scope fix
- any Red-3 trigger appears

## 8. Relationship To Existing Tools

SWE agent is subordinate to the existing governed workflow:

- Codex remains orchestration, gate, manifest, and closeout owner under policy limits.
- VS Code remains the local workspace/editing execution surface.
- Claude Code remains review-only verdict capture under the governed `claude.cmd` path.
- Claude Web in AdsPower remains external review-prompt path.
- Human or jarvis approval remains required where policy requires it.

SWE agent cannot replace any required review or approval.
