# SWE Autonomous Delivery Acceleration Playbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | SWE Autonomous Delivery Acceleration Playbook |
| Status | Green docs-only design draft |
| Scope | Define role boundaries, prompt routing, SWE accelerator use, anti-generalization rules, and delivery-loop metrics before the next PRD arrives |
| Snapshot | S5-WAIT-FOR-PRD-AND-ROUTE-SELECTION-READINESS-2026-04-22-001 |
| Stage | s5-wait-for-prd-and-route-selection-readiness |
| Baseline commit | `ec491a1da73464e930a9bed7f3586b3d92cb59eb` |
| Baseline manifest status | PASS |
| Lane | Green docs-only readiness note |

This playbook is a readiness design for faster PRD-driven delivery. It does not authorize implementation, code or test changes, release changes, external access, launch execution, production deployment, real-data handling, credential handling, public endpoint work, parked-stream reopen, Red execution, staging, commit, or push.

The current product posture remains:

```text
WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION
```

When the latest PRD or explicit product direction arrives, delivery must still route through:

```text
OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE
```

## 2. Objective

The goal is to shorten the path from PRD to governed release without allowing model-driven scope invention.

Target delivery shape:

```text
PRD or explicit product direction
-> PRD intake
-> route selection
-> exact ticket
-> bounded SWE acceleration where explicitly allowed
-> Codex implementation in the VS Code workspace
-> Claude Code focused code review
-> Claude Web product, architecture, or governance review where required
-> targeted tests
-> full gate where required
-> release verification where authorized
-> closeout
```

Acceleration is useful only when it produces:

- smaller diffs
- clearer tickets
- faster local code comprehension
- faster focused review
- fewer gate failures
- less rework

Acceleration is not permission to broaden scope, invent requirements, skip review, skip release verification, or move high-risk work out of HOLD.

## 3. Role Matrix

| Role | Position | Primary duties | Must not do |
| --- | --- | --- | --- |
| Codex | Orchestrator, implementation owner, prompt router, verification and release owner | Load baseline and governance docs, classify lane, draft route and tickets, package prompts for other models, review SWE output, edit in the repo when authorized, run tests, route reviews, manage release verification and closeout where allowed | Invent product scope, approve its own Red authority, treat routed output as approval, bypass review, handle secrets or real data, launch, deploy, stage/commit/push without authority |
| VS Code | Local workspace and execution surface | Provide the editing, diff, terminal, test, and local execution surface for exact allowed files | Act as product memory, reviewer, approver, route authority, release authority, or independent closeout authority |
| SWE / mini-swe-agent | Bounded implementation accelerator | Read exact local scope, propose an implementation plan or patch suggestion, help diagnose test failures when a later exact Yellow item explicitly allows it | Select route, expand scope, define acceptance criteria, review itself, own closeout, update manifest, run release packaging, stage, commit, push, or handle secrets/real data/browser sessions |
| Claude Code | Focused code reviewer | Review supplied diffs and tests for bugs, regressions, scope creep, missing tests, and unnecessary abstraction | Decide product direction, replace Claude Web architecture/governance review, approve Red work, directly edit files, run implementation commands |
| Claude Web | Product, architecture, and governance reviewer | Review PRD intake, route selection, high-risk boundaries, architecture decisions, Red/HOLD packages, external pilot/public endpoint/evidence rules | Act as local executor, replace tests/gates/manifest verification, approve code by implication |
| Human / Jarvis | Product direction and authorization boundary | Provide PRD, product direction, GO/no-go, and governed approvals where policy requires them | Be required for every low-risk mechanical step unless the policy or lane requires it |

Short form:

```text
VS Code is the workbench.
Codex is the orchestrator, implementation owner, prompt router, and verification owner.
SWE is the bounded accelerator.
Claude Code is code review.
Claude Web is product, architecture, and governance review.
Human/Jarvis owns product direction and authorization boundaries.
```

## 4. Prompt Routing Protocol

Codex may package, copy, transfer, and record prompts for SWE, Claude Code, Claude Web, and Human/Jarvis approval requests. Prompt routing is an orchestration duty, not review authority or approval authority.

Every routed prompt must include:

- source root
- snapshot
- baseline commit
- manifest path
- exact question
- allowed files or explicit docs-only scope
- explicit non-authorization boundaries
- secrets and real-data exclusion
- expected output format
- output role: `implementation suggestion`, `review evidence`, `route verdict`, or `approval request`

### 4.1 SWE Prompt

Use only when a later exact Yellow item explicitly authorizes SWE.

Required prompt constraints:

- exact repo root
- exact allowed files
- exact behavior
- exact tests
- max-change budget
- SWE role exactly `bounded implementation accelerator`
- default execution mode `no-write plan / patch suggestion`
- output location
- before/after git status requirements if writes are ever separately authorized
- HOLD triggers for unexpected mutation, staged files, secrets, real data, browser/session material, network/model ambiguity, Red triggers, or out-of-scope failures

SWE output is never authority. Codex must review it before any repo edit.

### 4.2 Claude Code Prompt

Use for focused code review of supplied material.

Expected output:

```text
PASS
```

or

```text
PASS_WITH_FINDINGS
```

or

```text
HOLD
```

Claude Code must review:

- correctness risk
- regression risk
- missing tests
- scope creep
- unnecessary abstraction
- hidden behavior change
- alignment with exact files and exact ticket behavior

Claude Code review evidence does not replace Claude Web review where product, architecture, governance, Red, external pilot, public endpoint, evidence, real-data, or launch boundaries are triggered.

### 4.3 Claude Web Prompt

Use for PRD route, product, architecture, governance, high-risk, and Red/HOLD review.

Expected output should name:

- verdict
- blocking findings
- non-blocking findings
- route recommendation
- lane or HOLD status
- required human/Jarvis approval if any
- explicit non-authorization reminders

Claude Web review is not local execution, release verification, or manifest PASS.

### 4.4 Human / Jarvis Prompt

Use only when human or delegated approval is required.

Approval prompts must avoid secrets, raw customer data, unredacted evidence, cookies, tokens, auth headers, or browser session material.

Any delegated approval must use the `DELEGATED_APPROVER_GO` format in `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`. Missing fields mean HOLD.

## 5. PRD Intake Flow

When a new PRD or explicit product direction arrives, Codex must not begin implementation first.

Codex should draft a PRD intake artifact or route-selection note containing:

- PRD source and date
- product goals
- non-goals
- changed assumptions
- affected existing baseline areas
- candidate routes
- risk lane classification
- exact next artifact
- required review path
- HOLD conditions
- explicit no-go boundaries

Claude Web review is required when the PRD or route touches:

- architecture direction
- external pilot or readiness
- launch/deployment
- real data
- credentials
- evidence retention or redaction
- public endpoint work
- S5-B/S5-D reopen
- ORDIV work
- Red lane
- AI_COLLAB changes
- schema/API breaking changes

PRD intake output may select a route or HOLD. It does not directly authorize code.

## 6. SWE-Enabled Ticket Flow

SWE is disabled by default for Yellow items.

Every future Yellow item must state one of:

```text
SWE agent use: not authorized for this item
```

or:

```text
SWE agent use: authorized only as bounded implementation accelerator for this item
```

The authorized form is valid only when the item defines:

- item ID
- route
- lane
- exact behavior
- exact allowed files
- exact required tests
- max-change budget
- SWE command path and version check
- model/credential path as `not used` or governed non-secret path
- output location
- independent review path
- closeout owner
- HOLD conditions

Default SWE mode for the first use on any product item should be:

```text
no-write plan / patch suggestion
```

Codex remains responsible for applying any accepted implementation inside the VS Code workspace under exact file scope.

## 7. Anti-Generalization Contract

All models must solve only the current ticket's exact behavior.

Default prohibited actions:

- introduce a new helper
- introduce a new module
- introduce a registry
- introduce a framework
- introduce a service layer
- introduce reusable architecture
- do cleanup refactors
- do unrelated renames
- reorganize directories
- design for future backends
- design for future roles
- design for future statuses
- design for future workflows
- turn a test fix into a product semantics change
- turn a review finding into an architecture rewrite
- turn a local ticket into new requirements

Allowed abstraction exception:

```text
1. The ticket explicitly names the abstraction.
2. Current duplication or complexity blocks the exact behavior.
3. A smaller alternative cannot satisfy required tests.
4. Review explicitly accepts the abstraction.
5. Exact file and test scope remains intact.
```

If a broader abstraction appears useful, record a scoped HOLD/design note instead of implementing it inside the current ticket.

Claude Code reviews must flag:

- scope creep
- over-abstraction
- speculative future-proofing
- hidden requirement creation
- unlisted helper/module/service introduction
- behavior not mapped to the ticket
- tests that prove future generality instead of exact behavior

## 8. Standard Delivery Loop

Use this loop after PRD or explicit product direction exists and a governed route has selected the work.

```text
1. Load baseline and required governance docs.
2. Verify delegation window when autonomous policy applies.
3. Confirm PRD or explicit product direction exists.
4. Draft PRD intake or route selection.
5. Route to Claude Web when product, architecture, governance, or high-risk review is required.
6. Draft exact ticket.
7. Decide whether SWE is allowed.
8. Send bounded SWE prompt only if the ticket explicitly allows it.
9. Codex reviews SWE output.
10. Codex edits exact files in the VS Code workspace when implementation is authorized.
11. Run targeted tests.
12. Send focused diff to Claude Code.
13. Fix blocking findings inside exact scope.
14. Run full gate when required.
15. Package and verify release only when authorized.
16. Create closeout artifact when required.
17. Stage, commit, and push only when the governing authority explicitly allows it.
18. Report outcome, tests, review status, HOLDs, and next route.
```

Any step that requires unlisted files, real data, credentials, browser/session access, public endpoint work, launch/deploy action, parked-stream reopen, or Red-3 action is HOLD.

## 9. Metrics

Each accelerated delivery loop should record:

- PRD intake time
- route selection time
- ticket preparation time
- SWE planning time
- estimated SWE time saved
- implementation time
- targeted test time
- Claude Code review turnaround
- Claude Web review turnaround where used
- gate failure count
- release verification time
- number of HOLDs
- scope creep findings
- overgeneralization findings
- files changed count
- cycle time from ticket open to closeout

The preferred trend is:

```text
smaller diffs
fewer findings
fewer scope resets
faster focused review
more stable gates
shorter PRD-to-release cycle
```

## 10. Standing Non-Authorization

This playbook does not authorize:

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
- AdsPower profile creation or switching
- Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection
- SWE agent product execution without a later exact Yellow item
- staging, commit, or push

## 11. Next Use

Before the next PRD arrives, this playbook may be used only as a readiness reference.

After the next PRD or explicit product direction arrives, the first governed step remains:

```text
OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE
```

That stage should use this playbook to keep role boundaries clear, route prompts through Codex, limit SWE to bounded acceleration, and prevent model-driven over-generalization.
