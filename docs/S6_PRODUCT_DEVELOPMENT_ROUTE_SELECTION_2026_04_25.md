# S6 Product Development Route Selection 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Product Development Route Selection 2026-04-25 |
| Status | ROUTE_SELECTED_FOR_TICKET_PREP |
| Date | 2026-04-25 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `4d6b380` |
| Intake record | `docs\S6_PRODUCT_SOURCE_INTAKE_2026_04_25.md` |
| Source package root | `D:\产品设计\secupilot0421\incoming_pending` |
| Lane | Green docs-only route selection |

This record selects the next governed product-development route after the 2026-04-25 product-source intake.

It does not authorize implementation, code/test changes, dependency changes, schema/API changes, launch, deploy, public endpoint work, real-data handling, credential handling, external pilot execution, parked-stream reopen, AI_COLLAB changes, staging, commit, or push.

## 2. Governing Source Priority

Implementation planning must use this authority order:

1. `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版 (2).md`
2. `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2 (1).md`
3. Model Contracts:
   - `SecuPilot_P1_L2_Case_Detail_Page_Model_Contract_v0.2 (1).md`
   - `SecuPilot_P2_Approval_Surface_Model_Contract_v0.1 (1).md`
   - `SecuPilot_P3_Manager_View_Model_Contract_v0.1.md`
4. `SecuPilot_High_Fidelity_UI_and_Visual_Interaction_Spec_v0.1 (1).md`
5. Prototype notes and HTML prototypes as visual and interaction references only.

Static HTML prototypes must not be copied into the production frontend as final implementation code.

## 3. Selected Route

Selected route:

```text
OPEN_S6_CORE_SURFACE_CONTRACT_IMPLEMENTATION_PREP
```

Route intent:

```text
Convert P1/P2/P3 core surface contracts into exact bounded implementation tickets.
```

Immediate next artifact:

```text
S6_CORE_SURFACE_TICKET_PREP_2026_04_25
```

The selected route is Green docs-only until the next artifact names exact tickets with allowed files, behavior, tests, review path, rollback, and HOLD conditions.

## 4. Route Sequencing

### 4.1 First: P1/L2 Case Detail

Decision:

```text
SELECTED_FIRST
```

Rationale:

- Current repo already has a minimal `/case/:caseId` path and Case Detail shell from the first S6 frontend slice.
- P1/L2 Case Detail is the core case-first reading surface and upstream interaction model for P2 and P3.
- It exercises the shared narrative spine, honesty visibility, Dialogue Dock, evidence panel control model, and coverage ceiling.
- It can be split into small UI-only tickets without backend/API/schema changes by using synthetic local view-model data.

Candidate ticket-prep groups:

| Group | Scope | Notes |
| --- | --- | --- |
| `P1-CD-A` | Case Detail layout regions and narrative spine | App shell, left rail, center WHAT/WHY/INTENT/HONESTY/DECISION ordering |
| `P1-CD-B` | Right contextual evidence panel controls | Auto/Manual + Pin, click fallback, no hover-only access |
| `P1-CD-C` | P1 Action Request modal semantics | Submit-to-P2 only; no ActionMode / execution-mode choice |
| `P1-CD-D` | Dialogue Dock source boundary | Runtime placeholder only; no hardcoded business chips as final behavior |

### 4.2 Second: P2 Approval Surface

Decision:

```text
SELECTED_SECOND
```

Rationale:

- P2 Model Contract is now present, closing the previous route-selection gap.
- P2 depends on the case-first and evidence-control semantics proven in P1, but can be ticketed independently once P1 primitives exist.
- The P2 contract has crisp acceptance targets for Decision Composer, Strong Confirm, observation window, Reject path, and readonly terminal states.

Candidate ticket-prep groups:

| Group | Scope | Notes |
| --- | --- | --- |
| `P2-AP-A` | Approval surface route and queue/narrative shell | P2-only operable surface; P1/P3 no operable approval route |
| `P2-AP-B` | Decision Composer four modes | Approve / Delay / Observe / Reject mutually exclusive |
| `P2-AP-C` | Strong Confirm modal | Approve cannot submit directly |
| `P2-AP-D` | Observation window / terminal readonly guards | No auto-execute, no revoke CTA, disabled rules |

### 4.3 Third: P3 Manager View

Decision:

```text
SELECTED_THIRD
```

Rationale:

- P3 Manager View has a model contract and prototype references, but it benefits from shared language stabilized by P1 and P2.
- P3 must use independent summary components, not masked P2 technical components.
- P3 can remain read-only and synthetic-data backed in early implementation.

Candidate ticket-prep groups:

| Group | Scope | Notes |
| --- | --- | --- |
| `P3-MV-A` | Manager view route and independent summary shell | P3 first-level nav; no approval workflow action |
| `P3-MV-B` | Attention queue and coverage/ROI source boundaries | Placeholder/source labels; no frontend-inferred numbers |
| `P3-MV-C` | Approval audit readonly summary | `source=manager/history`, not coverage unlock |
| `P3-MV-D` | Manager Dialogue Dock boundaries | Management questions only; no case action buttons |

### 4.4 Optional: Jira/Linear Import Reconciliation

Decision:

```text
OPTIONAL_GREEN_TOOLING
```

This route is useful only if issue tracker sync must happen before ticket prep. It should not block repo-local exact ticket drafting.

## 5. Lane Classification

| Route | Lane now | Later lane | Current outcome |
| --- | --- | --- | --- |
| `OPEN_S6_CORE_SURFACE_CONTRACT_IMPLEMENTATION_PREP` | Green docs-only | Yellow prep per exact ticket | SELECTED |
| `P1-CD-*` ticket prep | Green docs-only | Yellow implementation after readiness | NEXT |
| `P2-AP-*` ticket prep | Green docs-only | Yellow implementation after readiness | NEXT_AFTER_P1 |
| `P3-MV-*` ticket prep | Green docs-only | Yellow implementation after readiness | NEXT_AFTER_P2 |
| Jira/Linear reconciliation | Green docs-only / tooling | N/A | OPTIONAL |

## 6. Shared Non-Goals

The selected route must not:

- implement from static HTML by copy/paste;
- add backend/API/schema changes;
- add launch, deploy, public endpoint, external pilot, or real-data behavior;
- handle credentials, tokens, cookies, auth headers, or secrets;
- reopen S5-B, S5-D, ORDIV, or AI_COLLAB;
- add broad design-system or reusable platform work;
- invent routes beyond PRD-governed routes;
- hardcode business follow-up chips, unlock messages, queue windows, ROI numbers, CMDB business tags, or remediation suggestions as final runtime behavior;
- grant P1 or P3 approval authority;
- let P3 reuse P2 technical components by masking/hiding fields.

## 7. Shared Ticket Prep Requirements

Every next ticket-prep record must include:

- product source references;
- exact route and lane;
- exact behavior;
- exact non-goals;
- exact allowed files;
- exact required tests and assertions;
- exact data mode;
- exact review path;
- full gate expectation;
- commit/push rule;
- rollback and HOLD conditions;
- anti-generalization check;
- Red/HOLD trigger check;
- SWE eligibility statement.

Default SWE statement for the next prep stage:

```text
SWE agent use: not authorized for this ticket unless a later exact Yellow ticket explicitly names SWE as bounded implementation accelerator.
```

## 8. Review Routing

Current route-selection review state:

```text
Claude Web state: UNKNOWN_AVAILABILITY
Claude Code state: NOT_REQUIRED_NO_DIFF
Human/Jarvis state: route authorization supplied for next step
```

Route selection may proceed as a Green docs-only artifact, but implementation tickets must not claim product/architecture/governance review PASS unless an actual reviewer verdict exists.

Claude Web or equivalent external product/architecture/governance review is required if a later route-selection closeout claims broad P1/P2/P3 architecture readiness rather than simply drafting exact ticket prep.

## 9. HOLD Conditions

HOLD if:

- any next step tries to implement before exact ticket readiness;
- any ticket cannot name exact files or tests;
- implementation requires backend/API/schema changes not separately authorized;
- the HTML prototype is treated as final source code;
- a ticket encourages broad framework/component-library/platform abstraction before exact behavior requires it;
- route selection discovers a conflict between PRD and a Model Contract;
- Claude Web/external review is required but unavailable and no alternative is named;
- Red/HOLD triggers appear.

## 10. Decision

Decision:

```text
READY_FOR_CORE_SURFACE_TICKET_PREP
```

Next governed artifact:

```text
OPEN_S6_CORE_SURFACE_TICKET_PREP_2026_04_25
```

Recommended immediate ticket-prep focus:

```text
P1-CD-A: Case Detail layout regions and narrative spine
```

Reason:

```text
It is the smallest contract-driven bridge from the current frontend scaffold to the new product package and provides the shared interaction language needed by P2 and P3.
```

## 11. Update 2026-04-25: P1-CD-A Ticket Prep

The recommended immediate ticket-prep focus has been converted into:

```text
docs\S6_P1_CD_A_CASE_DETAIL_LAYOUT_TICKET_PREP_2026_04_25.md
```

Outcome:

```text
P1-CD-A READY_FOR_EXACT_TICKET
```

Implementation remains bounded to the exact allowed files, required tests, review path, and HOLD conditions named in that ticket-prep record.

## 12. Update 2026-04-25: P1-CD-A Implementation Gate

P1-CD-A implementation result:

```text
IMPLEMENTED_GATE_PASS
```

Gate evidence:

- frontend test: `npm run test -- --run` PASS, 6 tests passed;
- frontend build: `npm run build` PASS;
- backend guard: `py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view` PASS, 42 tests passed;
- focused `claude.cmd --print` review: NO BLOCKING FINDINGS.

Current closeout state:

```text
PENDING_STAGE_COMMIT_PUSH
```

The working tree still contains earlier uncommitted intake records and unrelated untracked files. Do not stage unrelated files during the P1-CD-A closeout.

## 13. Update 2026-04-25: P1-CD-A Commit And P1-CD-B Ticket Prep

P1-CD-A was subsequently committed and pushed:

```text
40929a2 Implement P1 case detail layout spine
```

Next selected P1 ticket:

```text
P1-CD-B: Right contextual evidence panel controls
```

Ticket-prep record:

```text
docs\S6_P1_CD_B_EVIDENCE_PANEL_CONTROLS_TICKET_PREP_2026_04_25.md
```

Outcome:

```text
P1-CD-B READY_FOR_EXACT_TICKET
```

P1-CD-B remains bounded to right evidence-panel `Auto / Manual`, `Pin / Lock`, manual frame switching, and click/focus fallback on narrative sections. Cross-surface AR propagation, backend-driven state sync, route handoff, E2E migration tests, and concurrency collision handling remain deferred until the logic-collision walkthrough sign-off unlocks them.

## 14. Update 2026-04-25: P1-CD-B Implementation Gate

P1-CD-B implementation result:

```text
IMPLEMENTED_GATE_PASS
```

Gate evidence:

- frontend test: `npm run test -- --run` PASS, 7 tests passed;
- frontend build: `npm run build` PASS;
- backend guard: `py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view` PASS, 42 tests passed;
- focused `claude.cmd --print` review found P1 issues that were fixed;
- focused `claude.cmd --print` re-review: NO BLOCKING FINDINGS.

Current closeout state:

```text
PENDING_STAGE_COMMIT_PUSH
```

Do not stage unrelated untracked files during the P1-CD-B closeout.
