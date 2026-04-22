# Autonomous Delivery Dry Run Rehearsal

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Delivery Dry Run Rehearsal |
| Status | Green docs-only rehearsal baseline |
| Scope | Rehearse the SWE autonomous delivery loop without product implementation, external execution, or invented PRD scope |
| Snapshot | S5-AUTONOMOUS-DELIVERY-DRY-RUN-REHEARSAL-2026-04-22-001 |
| Stage | s5-autonomous-delivery-dry-run-rehearsal |
| Baseline commit | `ddc5022c5524177f3a799cb6c1518dc89e0e39c3` |
| Baseline snapshot | S5-TICKET-READINESS-CHECKLIST-2026-04-22-001 |
| Baseline manifest status | PASS |
| Route | `OPEN_AUTONOMOUS_DELIVERY_DRY_RUN_REHEARSAL_STAGE` |
| Lane | Green docs-only |

This rehearsal validates the delivery choreography created by:

- `docs\SWE_AUTONOMOUS_DELIVERY_ACCELERATION_PLAYBOOK.md`
- `docs\AUTONOMOUS_DELIVERY_PROMPT_PACK.md`
- `docs\TICKET_READINESS_CHECKLIST.md`

It does not authorize implementation, code/test changes, SWE product execution, external review submission, launch, deployment, real-data handling, credential handling, public endpoint work, parked-stream reopen, Red execution, AI_COLLAB changes, staging, commit, or push outside governed closeout rules.

## 2. Rehearsal Objective

The objective is to prove that the autonomous delivery loop can move faster without widening scope.

This rehearsal checks:

- the exact handoff order from PRD intake to ticket readiness
- where VS Code, Codex, SWE, Claude Code, Claude Web, and Human/Jarvis fit
- when Codex may copy prompts
- when external model output is evidence instead of authority
- when Claude Web usage limits create a queue or HOLD
- when SWE remains disabled
- when anti-generalization rules stop speculative implementation
- what gets measured during a later live PRD-driven loop

The rehearsal is intentionally non-product. No placeholder feature becomes product scope.

## 3. Current External Reviewer Constraint

The user reported Claude Web state on 2026-04-22:

```text
Usage limit reached; resets 1:00 AM.
```

Because the active user timezone is Asia/Shanghai, the reset target is treated as:

```text
2026-04-23 01:00 Asia/Shanghai
```

Governed handling:

- Claude Web review is not claimed as completed during the limit window.
- Claude Code cannot replace Claude Web for product, architecture, governance, high-risk, Red, or HOLD review.
- A docs-only rehearsal may continue only if it records Claude Web as queued or unavailable.
- Any live route requiring Claude Web before reset must return `NEEDS_CLAUDE_WEB_REVIEW` or `HOLD_PENDING_CLAUDE_WEB_RESET`.
- No AdsPower profile creation/switching, Claude Web login automation, cookie/session/token/auth-header/browser-storage/profile-file inspection, or conversation-history reading is authorized.

## 4. Dry Run Inputs

This rehearsal uses only governed repo state and synthetic control inputs.

| Input | Dry-run value | Result |
| --- | --- | --- |
| Source root | `D:\产品设计\New folder` | accepted |
| Baseline | `S5-TICKET-READINESS-CHECKLIST-2026-04-22-001` | accepted |
| Product source | latest PRD not provided | guard should stop product route |
| Candidate feature | none | no invented scope |
| Candidate ticket | none | no exact ticket opens |
| SWE execution | not authorized | no prompt sent |
| Claude Code review | no diff | not applicable |
| Claude Web architecture review | usage limited until 2026-04-23 01:00 Asia/Shanghai | queued / not passed |

## 5. Rehearsal Path

The dry run uses this non-product path:

```text
1. Load baseline and required governance docs.
2. Verify delegation window if autonomous authority is relevant.
3. Check whether latest PRD or explicit product direction exists.
4. If missing, return WAIT/HOLD without route invention.
5. Exercise the Ticket Readiness Checklist on the missing-input case.
6. Confirm outcome cannot be READY_FOR_EXACT_TICKET.
7. Confirm outcome cannot be READY_FOR_SWE_ACCELERATION.
8. Confirm Codex may copy but not submit external prompts when prerequisites are missing.
9. Record Claude Web usage limit as queued evidence, not review PASS.
10. Run full gate and release verification for the docs-only rehearsal package.
```

Expected dry-run result:

```text
WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION
```

Ticket-readiness dry-run result:

```text
HOLD_NO_PRODUCT_SOURCE
```

SWE dry-run result:

```text
SWE_AGENT_USE_NOT_AUTHORIZED
```

Claude Web dry-run result:

```text
CLAUDE_WEB_REVIEW_QUEUED_USAGE_LIMIT_UNTIL_2026-04-23_01:00_ASIA_SHANGHAI
```

## 6. Prompt Copy Ledger

Codex may prepare copyable prompt material as orchestration. Copying a prompt does not authorize sending it, receiving review, or treating it as approval.

| Target | Prompt source | Copy status | Send status | Expected verdict handling |
| --- | --- | --- | --- | --- |
| Claude Web | `docs\AUTONOMOUS_DELIVERY_PROMPT_PACK.md` section 7 | ready to copy after reset | not sent during usage limit | must be `PASS`, `PASS_WITH_FINDINGS`, or `HOLD` when actually run |
| SWE / mini-swe-agent | `docs\AUTONOMOUS_DELIVERY_PROMPT_PACK.md` section 5 | blocked until exact Yellow item | not sent | `SWE agent use: not authorized for this item` |
| Claude Code | `docs\AUTONOMOUS_DELIVERY_PROMPT_PACK.md` section 6 | blocked until diff exists | not sent | not applicable because no implementation diff exists |
| Human/Jarvis | `docs\AUTONOMOUS_DELIVERY_PROMPT_PACK.md` section 8 | not required for this Green docs-only rehearsal | not sent | not applicable |

### 6.1 Claude Web Queued Prompt Skeleton

Use only after reset if a later stage needs architecture/governance review. Do not submit during the usage-limit window.

```text
Single source of truth: D:\产品设计\New folder
Snapshot ID: S5-AUTONOMOUS-DELIVERY-DRY-RUN-REHEARSAL-2026-04-22-001
Baseline commit: ddc5022c5524177f3a799cb6c1518dc89e0e39c3
Manifest: D:\产品设计\New folder\releases\release_manifest.json
Allowed files or docs-only scope:
- docs\AUTONOMOUS_DELIVERY_DRY_RUN_REHEARSAL.md
- docs\AUTONOMOUS_DELIVERY_DRY_RUN_REHEARSAL_CLOSEOUT.md
Lane: Green docs-only
Secrets and real data: excluded
Do not use files outside the source root as current truth.
Do not invent product scope.
Do not generalize beyond the exact task.

Review type: product / architecture / governance dry-run review
Output role: review evidence only

Task:
Review the dry-run rehearsal package. Confirm whether it correctly preserves:
1. no PRD means no product route invention
2. Ticket Readiness Checklist cannot pass without product source
3. SWE remains disabled without an exact Yellow item
4. Claude Code cannot replace Claude Web for architecture/governance review
5. Claude Web usage limit is queued/unavailable, not PASS
6. no implementation, launch, real-data, credential, public endpoint, parked-stream, Red, or AI_COLLAB authority is created

Required output:
- Verdict: PASS / PASS_WITH_FINDINGS / HOLD
- Blocking findings:
- Non-blocking findings:
- Lane:
- Required approval:
- Required follow-up:
- Non-authorization reminders:
```

## 7. Anti-Generalization Drill

During the rehearsal, any model suggestion that does one of the following is rejected:

- creates a helper, module, registry, framework, service layer, or reusable abstraction
- adds a future workflow, status, role, backend, route, adapter, or panel
- turns the missing PRD into a guessed feature
- turns rehearsal into implementation
- treats a review prompt as approval
- treats Claude Web usage limit as review completion
- treats SWE planning as ticket authority

Correct handling:

```text
Record as HOLD/design note, do not implement.
```

## 8. Acceptance Criteria

The rehearsal package is accepted only if:

- no product scope is invented
- missing PRD remains a WAIT/HOLD outcome
- ticket readiness cannot pass without product source
- SWE is not invoked
- Claude Code review is not required because no diff exists
- Claude Web is recorded as queued/unavailable due usage limit, not passed
- prompt-copy boundaries are explicit
- docs-only full gate and release verification pass
- release manifest references this stage and accepted artifacts
- no unrelated untracked files are staged

## 9. Metrics To Capture In Future Live Runs

For the first live PRD-driven loop after this rehearsal, record:

- PRD intake time
- route selection time
- checklist completion time
- prompt-copy time
- Claude Web queue or review turnaround
- SWE planning time if authorized
- Codex implementation time
- Claude Code review turnaround
- targeted test time
- full gate time
- release verification time
- scope creep findings
- over-generalization findings
- HOLD count
- files changed count
- ticket open-to-closeout cycle time

## 10. Standing Non-Authorization

This rehearsal does not authorize:

- implementation
- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime/API/schema behavior changes
- release script changes
- contract changes
- AI_COLLAB changes
- Yellow implementation
- SWE product execution
- direct SWE repo writes
- Red execution
- launch execution
- production deployment
- external pilot execution or readiness claims
- credential handling
- real-data handling
- evidence retention or redaction policy freeze
- public endpoint work
- S5-B/S5-D reopen
- ORDIV work
- S4-A resolver change
- Red-3 action
- AdsPower profile creation/switching
- Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection
- staging, commit, or push outside governed closeout rules

## 11. Next Use

If no latest PRD or explicit product direction exists, continue:

```text
WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION
```

When the latest PRD or explicit product direction arrives, open:

```text
OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE
```

Then use this rehearsal package as the checklist for keeping prompt routing, Claude Web review state, SWE eligibility, and anti-generalization controls honest.
