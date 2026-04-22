# Autonomous Delivery Prompt Pack

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Delivery Prompt Pack |
| Status | Green docs-only prompt template baseline |
| Scope | Provide reusable prompt templates for Codex prompt routing to SWE, Claude Code, Claude Web, and Human/Jarvis |
| Snapshot | S5-SWE-AUTONOMOUS-DELIVERY-ACCELERATION-BASELINE-2026-04-22-001 |
| Stage | s5-swe-autonomous-delivery-acceleration-baseline |
| Baseline commit | `4912cf5579a52efc04dfd033ccc1edaa71c2e427` |
| Baseline manifest status | PASS |
| Lane | Green docs-only |

This prompt pack turns the SWE autonomous delivery acceleration playbook into reusable, bounded prompts. It does not authorize implementation, code/test changes, SWE product execution, Claude Code file edits, Claude Web login automation, release changes, staging, commit, push, launch, deployment, external pilot execution, real-data handling, credential handling, public endpoint work, parked-stream reopen, Red execution, or AI_COLLAB changes.

Codex may copy and route these prompts as orchestration material. Routed output is evidence or suggestion only unless the governing reviewer or approver explicitly has authority under the active policy.

## 2. Required Prompt Header

Every routed prompt must start with:

```text
Single source of truth: D:\产品设计\New folder
Snapshot ID: <current manifest snapshot id>
Baseline commit: <current baseline commit>
Manifest: D:\产品设计\New folder\releases\release_manifest.json
Allowed files or docs-only scope: <exact list>
Lane: <Green / Yellow / Conditional Red / HOLD>
Secrets and real data: excluded
Do not use files outside the source root as current truth.
Do not invent product scope.
Do not generalize beyond the exact task.
```

## 3. Anti-Generalization Clause

Add this clause to every SWE, Claude Code, and Claude Web prompt unless the task is explicitly about architecture design:

```text
Anti-generalization rule:
Solve only the exact task below. Do not introduce a new helper, module, registry, framework, service layer, reusable abstraction, future-proofing design, cleanup refactor, rename, directory reorganization, new product requirement, new status, new event vocabulary, new API/schema behavior, or future workflow support unless the task explicitly names it. If a broader abstraction seems useful, report it as a HOLD/design note instead of implementing or recommending it as part of this task.
```

## 4. PRD Intake And Route Selection Prompt

Use with Claude Web or another product/governance reviewer when a new PRD or explicit product direction arrives.

```text
<Required Prompt Header>

Review type: product / architecture / governance route review
Output role: route verdict and risk findings

Input:
- PRD or explicit product direction: <paste or reference governed input>
- Current baseline summary: <brief governed baseline>
- Current parked/HOLD boundaries: <brief list>

Task:
1. Summarize product goals.
2. Summarize non-goals.
3. Identify changed assumptions from the current baseline.
4. Identify impacted product areas.
5. Propose candidate routes.
6. Classify each route lane.
7. Identify required reviews and approvals.
8. Identify HOLD triggers.
9. Recommend the next governed artifact.

Required output:
- Verdict: PASS / PASS_WITH_FINDINGS / HOLD
- Recommended route:
- Lane:
- Blocking findings:
- Non-blocking findings:
- Required Human/Jarvis GO:
- Required Claude Code review:
- Required Claude Web/external review:
- Non-authorization reminders:
```

## 5. SWE Bounded Implementation Prompt

Use only when a later exact Yellow item explicitly authorizes SWE as `bounded implementation accelerator`.

Before this prompt is sent, the candidate ticket must pass `docs\TICKET_READINESS_CHECKLIST.md` with `READY_FOR_SWE_ACCELERATION`.

```text
<Required Prompt Header>
<Anti-Generalization Clause>

Review type: bounded implementation acceleration
Output role: implementation suggestion only
SWE agent role: bounded implementation accelerator
Execution mode: no-write plan / patch suggestion unless the ticket explicitly says otherwise

Ticket:
- Item ID:
- Route:
- Exact behavior:
- Exact allowed files:
- Exact tests:
- Max-change budget:
- Output location:
- HOLD conditions:

Task:
1. Inspect only the exact scope supplied.
2. Propose the smallest implementation plan.
3. If useful, provide a minimal patch suggestion.
4. Do not apply changes unless the ticket explicitly authorizes writes.
5. Do not run unlisted commands.
6. Do not access secrets, real data, browser sessions, tokens, cookies, auth headers, external systems, or files outside scope.

Required output:
- Summary:
- Minimal plan:
- Patch suggestion or no-patch reason:
- Tests to run:
- Scope risks:
- HOLD if any:
```

## 5.1 Ticket Readiness Record Prompt

Use after PRD intake and route selection, before opening an implementation ticket.

```text
<Required Prompt Header>
<Anti-Generalization Clause>

Review type: ticket readiness check
Output role: readiness decision

Candidate work:
- Product source:
- Route:
- Lane:
- Proposed behavior:
- Proposed files:
- Proposed tests:
- Proposed SWE use:
- Known HOLD boundaries:

Task:
Evaluate the candidate work against docs\TICKET_READINESS_CHECKLIST.md.

Required output:
- Decision: READY_FOR_EXACT_TICKET / READY_FOR_SWE_ACCELERATION / NEEDS_GREEN_DOCS_ONLY_TICKET_PREP / NEEDS_CLAUDE_WEB_REVIEW / NEEDS_HUMAN_OR_JARVIS_GO / HOLD
- Missing required fields:
- Red/HOLD triggers:
- Anti-generalization risks:
- SWE eligibility:
- Required next artifact:
```

## 6. Claude Code Focused Review Prompt

Use for focused code review after Codex has produced a bounded diff.

```text
<Required Prompt Header>
<Anti-Generalization Clause>

Review type: focused code review
Output role: review evidence

Diff under review:
<paste exact diff or generated review material>

Ticket scope:
- Exact behavior:
- Exact allowed files:
- Exact tests:
- Non-goals:

Review for:
1. Bugs or regressions.
2. Missing or weak tests.
3. Scope creep.
4. Over-abstraction or speculative generalization.
5. Hidden behavior changes.
6. Violations of exact file or test scope.

Required output:
- First line exactly one of: PASS / PASS_WITH_FINDINGS / HOLD
- Findings ordered by severity:
- Does this block acceptance:
- Required fixes:
- Optional notes:
```

Claude Code review evidence does not approve product direction, Red work, launch, deployment, external pilot execution, real-data handling, credential handling, public endpoint work, or parked-stream reopen.

## 7. Claude Web Architecture / Governance Prompt

Use when product, architecture, governance, or high-risk boundaries are involved.

```text
<Required Prompt Header>
<Anti-Generalization Clause>

Review type: product / architecture / governance review
Output role: route or governance verdict

Material under review:
<paste docs-only route, PRD intake, architecture decision, Red/HOLD package, or evidence policy material>

Questions:
1. Is the route/product interpretation correct?
2. Does it cross a Red or HOLD boundary?
3. Does it require Human/Jarvis approval?
4. Does it require external/security/privacy review?
5. Does it introduce hidden scope, hidden readiness claims, or over-generalization?
6. Is the next artifact correctly bounded?

Required output:
- Verdict: PASS / PASS_WITH_FINDINGS / HOLD
- Blocking findings:
- Non-blocking findings:
- Lane:
- Required approval:
- Required follow-up:
- Non-authorization reminders:
```

## 8. Human / Jarvis GO-No-Go Prompt

Use only when the governing lane requires human or delegated approval.

```text
<Required Prompt Header>

Approval request type: GO / NO-GO / HOLD

Stage/ticket:
Lane:
Approved action requested:
Allowed files/systems:
External access: yes/no
Real data: yes/no
Evidence retention: yes/no
Redaction reference:
Rollback/HOLD criteria:
Review status:
Gate status:
Expiration:

Requested response:
- GO with exact scope, or
- NO-GO, or
- HOLD with missing inputs.
```

For delegated Red-lane approvals, the response must use:

```text
DELEGATED_APPROVER_GO
Approver:
Date:
Stage/ticket:
Lane:
Approved action:
Allowed files/systems:
External access: yes/no
Real data: yes/no
Evidence retention: yes/no
Redaction reference:
Rollback/HOLD criteria:
Expiration:
Required review:
```

Any missing field means HOLD.

## 9. Prompt Routing Record

After routing a prompt, record:

```text
Prompt target:
Prompt type:
Snapshot:
Baseline commit:
Allowed files/scope:
Output received:
Verdict:
Findings:
HOLDs:
Follow-up action:
```

Do not record secrets, raw customer data, unredacted evidence, cookies, tokens, auth headers, API keys, browser session material, profile identifiers, or real external-system payloads.

## 10. Standing Non-Authorization

This prompt pack does not authorize:

- implementation
- code changes
- test changes
- dependency changes
- fixture changes
- runtime/API/schema behavior changes
- release script changes
- contract changes
- AI_COLLAB changes
- SWE product execution without a later exact Yellow item
- Claude Code file edits or command execution
- Claude Web login automation
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
- staging, commit, or push

## 11. Next Use

When the latest PRD or explicit product direction arrives, use this prompt pack with `docs\SWE_AUTONOMOUS_DELIVERY_ACCELERATION_PLAYBOOK.md` during:

```text
OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE
```

If no PRD or explicit product direction exists, continue waiting and do not open implementation.
