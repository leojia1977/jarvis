# Autonomous Vacation Operating Model

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Vacation Operating Model |
| Status | Docs-only draft for autonomous vacation operating model review |
| Snapshot | S5-AUTONOMOUS-VACATION-OPERATING-MODEL-2026-04-17-001 |
| Stage | s5-autonomous-vacation-operating-model |
| Baseline snapshot | S5-GOVERNANCE-CONTEXT-MODEL-2026-04-17-001 |
| Baseline commit | `da15c383e14bc4cae6c97017f91549194c37487d` |
| Route | OPEN_AUTONOMOUS_VACATION_OPERATING_MODEL_DOCS_ONLY_STAGE |
| Target | L3 Customer Trial Launch acceleration |

This operating model defines how Codex, VS Code, Claude Code, Claude Web, and any designated external reviewer may maximize safe autonomous progress while the human is unavailable. It is an authorization framework only. It does not execute autonomous implementation, external pilot execution, real customer launch, real-data handling, public endpoint work, production deployment, or credential handling.

## 2. L3 Definition

`L3 Customer Trial Launch` means a controlled customer-trial launch or private launch candidate.

It does not mean:

- unrestricted public GA
- multi-customer commercial GA
- legal/commercial commitment
- real customer sign-off
- production deployment without a governed approval path

## 3. AI Roles

| Role | Responsibility | Limits |
| --- | --- | --- |
| Codex | Route judgment, implementation where explicitly authorized, release/gate orchestration, manifest-aware closeout support. | May not invent external inputs, approve its own Red-lane authority, handle raw secrets, claim customer readiness, or execute customer launch without recorded delegated or human GO. |
| VS Code / human-supervised workspace | Drafting/editing workspace when the human is active, final human-supervised staging/commit/push when authorized. | Does not replace governed human product/governance decision authority. |
| Claude Code | Review-only by default unless separately scoped. | Must not edit files, stage, commit, or push when assigned review-only. |
| Claude Web or external reviewer | High-risk authorization/review path when required by trigger rules. | Review does not itself authorize implementation or launch unless the governing policy and delegated/human approval explicitly say so. |

## 4. Operating State Machine

Autonomous work should move through this state machine:

`BACKLOG_ITEM -> ROUTE_JUDGMENT -> SCOPED_TICKET -> DRAFT/IMPLEMENT -> REVIEW -> FULL_GATE -> PACKAGE -> COMMIT/PUSH -> PRODUCT_MAP_UPDATE -> NEXT/HOLD`

Rules:

- A state may be skipped only if the governing artifact explicitly marks it not applicable.
- Any implementation branch requires a scoped ticket before `DRAFT/IMPLEMENT`.
- Any closeout requires review and full gate before commit/push.
- Any unresolved HOLD stops the state machine.

## 5. Authorization Lanes

### Green Lane

Green lane work is low-risk and may proceed autonomously when the current stage allows the files and work type.

Examples:

- docs-only governance drafts
- route decisions
- rolling product maps
- review-pack preparation
- manifest key-file alignment
- full gates and release packaging during authorized closeout
- commit/push after PASS only when the current stage prompt, activated standing policy, or explicit human/delegated instruction assigns Green lane authority and explicitly allows commit/push, and no HOLD remains

### Yellow Lane

Yellow lane work may proceed only with a scoped ticket that defines exact files, behavior, tests, review path, rollback/HOLD criteria, and confirms no Red trigger is present.

Examples:

- bounded implementation in named files
- bounded test updates in named files
- deterministic runtime behavior changes covered by tests

### Conditional Red Lane

Conditional Red work may be prepared as docs-only material, but execution requires delegated or human approval according to `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`.

Examples:

- external pilot decision package
- customer-trial deployment prep
- read-only external access prep
- evidence/redaction policy drafting
- L3 launch package drafting

## 6. Red Categories

| Category | Meaning | Authorization |
| --- | --- | --- |
| Red-1 | High-risk but delegable if policy permits and evidence is complete. | Delegated approver may authorize using the required approval format. |
| Red-2 | May be prepared, but execution is blocked unless explicitly authorized. | Delegated or human GO required for the exact action. |
| Red-3 | Never AI-self-authorized. | Human pre-authorization or separate legal/commercial/security authority is required. |

Red-3 includes legal/commercial commitments, real customer sign-off, raw secret handling, deletion of real evidence, and incident responsibility judgments.

## 7. Daily Or Per-Stage Summary Format

Autonomous agents should produce summaries in this format:

```text
Stage:
Baseline:
Lane:
Work completed:
Files changed:
Review status:
Gate status:
Release/package status:
Open HOLDs:
Delegated/human approvals used:
Next recommended action:
Non-authorizations preserved:
```

## 8. Failure Handling

- Retry transient tool failures once when the command is safe and in scope.
- Fix scoped Green/Yellow failures only inside the authorized file set.
- Stop on any Red ambiguity, missing external input, missing delegated approval, secret/raw data exposure risk, or public endpoint ambiguity.
- Do not continue after full gate failure unless the fix is Green/Yellow, scoped, and does not create new risk.
- Rollback means stop and report unless a governed rollback method is explicitly authorized.

## 9. Maximum Automation Rule

Maximum automation is allowed only inside explicit authorization lanes.

AI may accelerate delivery, but may not invent external inputs, approve its own Red-lane authority, handle raw secrets, claim customer readiness, or execute customer launch without recorded delegated or human GO.

## 10. Standing Boundaries

- ORDIV-L1A remains `PARK_LOCAL_VALIDATION_NO_REPORT`.
- S5-B remains `PASS_AND_PARK`.
- S5-D remains `PASS_AND_PARK`.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- External pilot inputs remain `NOT_READY` / `UNKNOWN` unless explicitly governed later.
- External pilot execution remains unauthorized.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- AI_COLLAB remains unchanged.
