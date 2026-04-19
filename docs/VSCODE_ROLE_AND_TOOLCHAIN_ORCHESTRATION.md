# VS Code Role And Toolchain Orchestration

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | VS Code Role And Toolchain Orchestration |
| Status | Updated by cc switch command-path provisioning draft |
| Snapshot | S5-CC-SWITCH-COMMAND-PATH-PROVISIONING-2026-04-19-001 |
| Stage | s5-cc-switch-command-path-provisioning |
| Route | OPEN_VSCODE_ROLE_AND_TOOLCHAIN_ORCHESTRATION_STAGE |
| Baseline commit | `5c1d8c1e288c1e16f47279f147fc4a973064e874` |
| Baseline snapshot | S5-ADSPOWER-PROFILE-LAUNCH-VERIFICATION-2026-04-19-001 |
| Baseline stage | s5-adspower-profile-launch-verification |
| Baseline manifest status | PASS |
| Baseline release artifact | `releases\secupilot-S5-ADSPOWER-PROFILE-LAUNCH-VERIFICATION-2026-04-19-001.zip` |
| Baseline release sha256 | `10c213c7d32cd22527c9a41f32102cc0906041882e79cd8420c329982bf214ac` |

## 2. Purpose

This docs-only stage clarifies the role of VS Code in the autonomous workflow.

VS Code is the local workspace and editing execution surface. It is not a separate product-governance authority, not a long-term memory source, not an independent reviewer, and not a bypass around Codex orchestration, governed review, release gates, HOLD queue rules, or human/delegated approvals.

## 3. Role Split

| Surface | Governed role |
| --- | --- |
| Codex automation | Orchestrates the autonomous run, reads governance docs, selects one allowed item, classifies lane, prepares prompts, runs authorized checks/gates, updates manifest after gate PASS, and handles Green docs-only closeout only under the standing rule. |
| VS Code workspace | Provides the local repo editing surface for allowed files. It may be used by Codex or a human-supervised operator to draft scoped docs changes. It does not decide product route, lane authority, review sufficiency, PASS state, or closeout eligibility by itself. |
| Claude Web in AdsPower | Provides the verified active-profile review-prompt transfer path for safe external review prompts only. It does not authorize launch, Red execution, profile launch/switch, login, or session inspection. |
| Claude Code via cc-switch routed `claude.cmd` | Verified only for review-only verdict capture through stdin, `--bare`, JSON wrapper output, disabled tools, no session persistence, plan permission mode, budget cap, first-line verdict parsing, no web requests, and unchanged git status. `claude.exe` is not a substitute. |
| Git/release scripts | Provide local status, deterministic gates, review packs, release zip generation, verification, and governed closeout only when authorized by the current stage and lane rules. |

## 4. VS Code Allowed Use

VS Code may be used as a local editing surface only when all of the following are true:

- the current stage or governed policy allows the file scope
- the lane is clear
- the file set is exact
- no unresolved HOLD blocks the action
- changes remain inside the repo root
- repo-governed docs and manifest remain the source of truth

Allowed examples:

- editing docs-only governance artifacts within the current stage scope
- inspecting local tracked files
- preparing review prompts, summaries, and staging proposals
- supporting human-supervised edits for separately governed implementation tickets

## 5. VS Code Prohibited Use

VS Code may not be treated as authority for:

- product/governance decisions
- lane assignment
- approval substitution
- review PASS
- manifest PASS
- release verification
- external pilot readiness
- customer launch readiness
- long-term product memory

VS Code does not authorize:

- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime/API/schema changes
- release script changes
- contract changes
- AI_COLLAB changes
- credential handling
- real-data handling
- public endpoint work
- external pilot execution
- launch execution
- production deployment
- S5-B/S5-D reopen
- ORDIV reopen/report/CSV/L1B work
- Red-3 action
- browser/profile launch or switching
- Claude Web login
- cookie/session/token/auth-header inspection
- staging, commit, or push outside the standing Green docs-only closeout rule or separate explicit authorization

## 6. Orchestration Order

Autonomous runs should follow this order:

1. Codex reads `docs\DELEGATED_APPROVER_CHARTER.md` and verifies `delegation_expires`.
2. Codex loads the core governance docs, toolchain docs, and current manifest.
3. Codex confirms git status and the current PASS baseline.
4. Codex selects at most one next allowed item.
5. Codex classifies lane and checks HOLD queue entries.
6. VS Code may be used only as the local editing/workspace surface for the selected, allowed file set.
7. Review is routed through the governed review path for the lane.
8. Gate/package/release verification run only when the stage authorizes them.
9. Green docs-only closeout may stage/commit/push only under the standing post-PASS rule; all other staging/commit/push requires separate explicit authorization.

If any role boundary is unclear, the run must HOLD and report the ambiguity.

## 7. Current Outcome

This stage clarifies VS Code as a governed local workspace/editing execution surface and records that Codex remains the orchestration, gate, manifest, release-verification, and closeout owner under policy limits.

It does not raise VS Code maturity above L1. It does not verify a new VS Code automation path. Later `S5-CC-SWITCH-COMMAND-PATH-PROVISIONING-2026-04-19-001` changes AHQ-020 for Claude Code review-only verdict capture only. VS Code still does not gain review, PASS, route, manifest, staging, commit, or push authority.

## 8. Non-Authorization

This stage does not authorize launch execution, production deployment, external pilot execution, credential handling, real-data handling, public endpoint work, S5-B/S5-D reopen, ORDIV reopen/report/CSV/L1B work, Red-3 action, S4-A resolver change, AI_COLLAB change, browser login/session access, code/test implementation, full four-tool automation, full gate, release packaging, staging, commit, or push.
