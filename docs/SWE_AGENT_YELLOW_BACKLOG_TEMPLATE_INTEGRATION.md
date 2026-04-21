# SWE Agent Yellow Backlog Template Integration

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | SWE Agent Yellow Backlog Template Integration |
| Status | Green docs-only template integration draft |
| Scope | Add optional bounded SWE agent accelerator controls to future Yellow backlog templates |
| Snapshot | S5-SWE-AGENT-YELLOW-BACKLOG-TEMPLATE-INTEGRATION-2026-04-21-001 |
| Stage | s5-swe-agent-yellow-backlog-template-integration |
| Baseline commit | `0b20b9b1fb991cb66d4898d83d0b8ce0609deca3` |
| Baseline snapshot | S5-MINI-SWE-AGENT-WSL2-NO-WRITE-DRY-RUN-VERIFICATION-2026-04-21-001 |
| Baseline stage | s5-mini-swe-agent-wsl2-no-write-dry-run-verification |
| Baseline manifest status | PASS |
| Baseline release sha256 | `4dd7f904eadea00d3f1ce39fe63f83614ee2acbb82dc1313c9febf847fecd84e` |
| Current release sha256 | `null` until full gate and release verification PASS |
| Route | `OPEN_SWE_AGENT_YELLOW_BACKLOG_TEMPLATE_INTEGRATION_STAGE` |
| Lane | Green docs-only |

This stage integrates SWE agent / mini-swe-agent into future Yellow backlog templates only as an optional bounded implementation accelerator. It does not authorize SWE agent product execution, model-backed implementation, code/test changes, staging, commit, push, or retroactive use on current or closed Yellow items.

## 2. Baseline Evidence

The current baseline verified:

- `SecuPilotUbuntu2404` exists as a WSL2 `Ubuntu-24.04` distro.
- normal WSL user `secupilot` is available.
- `mini-swe-agent` version `2.2.8` is installed in `/home/secupilot/.venvs/mini-swe-agent`.
- deterministic no-write main-agent dry run completed from the repo root mapping.
- dry-run trajectory recorded one harmless `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT` command, zero cost, and unchanged git status.
- AHQ-024 is `VERIFIED_NO_WRITE_DRY_RUN_WITH_LIMITS`.
- baseline release sha256 is copied from the prior PASS manifest and is the full 64-hex value `4dd7f904eadea00d3f1ce39fe63f83614ee2acbb82dc1313c9febf847fecd84e`.

This evidence proves runner mechanics only. It does not prove model-backed implementation safety, prompt-injection resistance for real tasks, live file-write confinement, or suitability for any specific product item.

## 3. Template Integration Decision

Future Yellow backlog preauthorization packages may include an optional SWE agent accelerator block only when the package is being prepared after this stage closes with review PASS, full gate PASS, release verification PASS, manifest PASS, closeout commit, and push.

The optional block must default to:

```text
SWE agent use: not authorized for this item unless explicitly named below
```

If a later Yellow item explicitly names SWE agent, the item must define:

- exact SWE agent role: `bounded implementation accelerator`
- exact repo root
- exact allowed files
- exact allowed behavior
- exact required tests
- exact maximum change budget
- exact model mode and credential non-secret path if model-backed execution is needed
- exact WSL command path and version check
- exact output and trajectory location, preferably outside the repo
- before/after `git status --short`
- independent review of any generated output
- Codex-owned orchestration, gate, manifest, release, and closeout
- HOLD conditions for scope expansion, unexpected mutation, staged files, secrets, real data, Red triggers, network/model ambiguity, or out-of-scope test failures

## 4. Non-Retroactive Rule

This stage does not add SWE agent to any current or past Yellow item.

Specifically, this stage does not authorize SWE agent participation in:

- `S5C-YB-05`, which is already closed.
- `S5C-YB-06`, as currently defined in `docs/NEXT_YELLOW_BACKLOG_PREAUTHORIZATION.md`.
- `S5C-YB-07`, as currently defined in `docs/NEXT_YELLOW_BACKLOG_PREAUTHORIZATION.md`.
- any closed `S5C-YB-*` item.

If product/governance later wants SWE agent assistance on YB-06, YB-07, or another item, a later exact Yellow item or amended package must explicitly name SWE agent and carry the controls in this stage and `docs/SWE_AGENT_RUNBOOK.md`.

## 5. Tool Role

SWE agent may only be described as:

```text
bounded implementation accelerator
```

It is not:

- an independent decision maker
- a route selector
- a product owner
- a reviewer of its own output
- a final reviewer
- a closeout owner
- a manifest, gate, release, stage, commit, or push owner

Codex remains orchestration, lane classification, review routing, gate/package/release verification, manifest update, and closeout owner under policy limits. VS Code remains the local workspace/editing execution surface. Claude Code and Claude Web remain review paths under their governed limits.

## 6. Updated Files

This Green docs-only stage updates only docs and manifest:

- `docs/SWE_AGENT_YELLOW_BACKLOG_TEMPLATE_INTEGRATION.md`
- `docs/AUTONOMOUS_YELLOW_BACKLOG_PREAUTHORIZATION_TEMPLATE.md`
- `docs/NEXT_YELLOW_BACKLOG_PREAUTHORIZATION.md`
- `docs/AUTONOMOUS_OPERATION_STARTUP.md`
- `docs/AUTONOMOUS_DELIVERY_PIPELINE.md`
- `docs/AUTONOMOUS_TOOLCHAIN_INTEGRATION.md`
- `docs/AUTONOMOUS_TOOL_CAPABILITY_MATRIX.md`
- `docs/AUTONOMOUS_TOOL_RUNBOOK.md`
- `docs/SWE_AGENT_RUNBOOK.md`
- `docs/AUTONOMOUS_HOLD_QUEUE.md`
- `docs/PRODUCT_STATE.md`
- `docs/ROADMAP_AND_PARKED_ITEMS.md`
- `docs/GOVERNANCE_DECISION_LOG.md`
- `docs/HANDOFF.md`
- `releases/release_manifest.json`

No code, tests, dependencies, fixtures, runtime/API/schema files, release scripts, contracts, or AI_COLLAB files are changed.

Known out-of-scope untracked local files remain excluded and must not be staged:

- `CLAUDE.md`
- `SecuPilot_阶段性总结_20260409.md`

## 7. HOLD Conditions

HOLD if this stage would:

- authorize SWE agent product-task execution directly
- enable SWE agent for current or closed Yellow items retroactively
- weaken exact file/test/max-change rules
- allow SWE agent to choose scope, route, acceptance criteria, review status, or closeout state
- allow SWE agent to stage, commit, push, run release packaging, update manifest, or own gate results
- require secrets, real data, browser/session material, external system access, launch, deployment, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB change
- require code, test, dependency, fixture, runtime/API/schema, release-script, or contract edits

## 8. Non-Authorization

This stage does not authorize:

- implementation
- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime/API/schema changes
- release script changes
- contract changes
- AI_COLLAB changes
- SWE agent execution against product work
- model-backed SWE agent implementation
- SWE agent participation in current or past Yellow items
- review replacement
- route selection by SWE agent
- manifest/gate/release ownership by SWE agent
- staging, commit, push, force-push, PR creation, or remote action by SWE agent
- launch execution
- production deployment
- external pilot execution or readiness
- credential handling
- real-data handling
- evidence retention or redaction policy freeze
- public endpoint work
- S5-B/S5-D reopen
- ORDIV work
- S4-A resolver order change
- Red-3 action
- AdsPower profile creation/switching
- Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection

## 9. Closeout Recommendation

```text
CLOSEOUT_ACCEPTED_AS_GOVERNED_SWE_AGENT_YELLOW_BACKLOG_TEMPLATE_INTEGRATION_AFTER_FULL_GATE_PASS
```

Meaning:

- future Yellow backlog templates may include an optional SWE agent bounded accelerator block
- actual SWE agent use remains unavailable unless a later exact Yellow item explicitly names it
- current and closed Yellow items are not retroactively SWE-enabled
- full gate, package, release verification, manifest PASS, exact staging, commit, and push must complete before this stage becomes the governed baseline

Recommended next route after this stage closes PASS:

```text
OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE
```
