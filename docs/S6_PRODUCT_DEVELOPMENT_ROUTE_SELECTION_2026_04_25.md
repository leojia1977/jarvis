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

## 15. Update 2026-04-25: S6-MF-A Ticket Prep

P1-CD-B was subsequently committed and pushed:

```text
66b45c8 Implement P1 evidence panel controls
```

Next selected mock-fixture ticket:

```text
S6-MF-A: Core Surface Mock Fixture Integration
```

Ticket-prep record:

```text
docs\S6_MF_A_CORE_SURFACE_MOCK_FIXTURE_INTEGRATION_TICKET_PREP_2026_04_25.md
```

Outcome:

```text
S6-MF-A READY_FOR_EXACT_TICKET
```

S6-MF-A is bounded to repo-local fixture import, mock-only resolved context, and a local Phase 0-6 selector. Storybook setup, Playwright setup, P1 to P2 AR propagation, P2 to P3 audit propagation, route handoff, backend-driven state sync, and bounded implementation sprint data-flow work remain separate later tickets.

## 16. Update 2026-04-25: S6-MF-A Implementation Gate

S6-MF-A implementation result:

```text
IMPLEMENTED_GATE_PASS
```

Gate evidence:

- fixture source hash: `814F21AACFE2E2B25514990188F9801D81F0ED4A464F7A03B05DD235E4A02B47`;
- repo-local fixture hash: `814F21AACFE2E2B25514990188F9801D81F0ED4A464F7A03B05DD235E4A02B47`;
- frontend test: `npm run test -- --run` PASS, 9 tests passed;
- frontend build: `npm run build` PASS;
- backend guard: `py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view` PASS, 42 tests passed;
- focused `claude.cmd --print` review found P1 issues that were fixed;
- focused `claude.cmd --print` re-review: NO BLOCKING FINDINGS.

Current closeout state:

```text
PENDING_STAGE_COMMIT_PUSH
```

Do not stage unrelated untracked files during the S6-MF-A closeout.

## 17. Update 2026-04-25: S6-SB-A Storybook Tooling Prep

S6-MF-A was subsequently committed and pushed:

```text
a8b08ef Integrate core surface mock fixture
```

Next selected Storybook preparation ticket:

```text
S6-SB-A: Storybook Static Core Surface Stories
```

Ticket-prep record:

```text
docs\S6_SB_A_STORYBOOK_STATIC_CORE_SURFACE_STORIES_TICKET_PREP_2026_04_25.md
```

Outcome:

```text
S6-SB-A NEEDS_DEPENDENCY_INSTALL_DECISION
```

S6-SB-A is Green docs-only. It does not install Storybook, change frontend package files, create `.storybook` config, create story files, or set up Playwright.

Recommended next route:

```text
OPEN_S6_SB_B_STORYBOOK_REACT_VITE_TOOLING_SETUP
```

S6-SB-B requires explicit dependency-install authorization before any `npm create storybook@latest`, `package.json`, `package-lock.json`, or `.storybook` changes.

## 18. Update 2026-04-25: S6-SB-B Storybook Tooling Setup

S6-SB-A was subsequently committed and pushed:

```text
75aecc2 Prepare Storybook core surface story plan
```

Next selected Storybook tooling ticket:

```text
S6-SB-B: Storybook React Vite Tooling Setup
```

Ticket-prep record:

```text
docs\S6_SB_B_STORYBOOK_REACT_VITE_TOOLING_SETUP_TICKET_PREP_2026_04_25.md
```

Outcome:

```text
S6-SB-B READY_FOR_EXACT_TOOLING_IMPLEMENTATION
```

Human/Jarvis authorization was supplied for Storybook dependency installation. Scope remains minimal Storybook React Vite tooling only; no product stories, no Playwright, no backend/API/schema, no cross-surface propagation, no real data, no launch, and no deployment.

## 19. Update 2026-04-25: S6-SB-B Implementation Gate

S6-SB-B implementation result:

```text
IMPLEMENTED_GATE_PASS
```

Gate evidence:

- Storybook React Vite tooling installed with `--no-features`;
- direct Storybook devDependencies added: `storybook`, `@storybook/react-vite`;
- `frontend/.storybook/main.ts` uses React Vite framework and no addons;
- generated tutorial/sample stories were removed from governed output;
- `npm run storybook -- --help` PASS;
- `npm run test -- --run` PASS, 9 tests passed;
- `npm run build` PASS;
- `npm run build-storybook -- --disable-telemetry --loglevel warn` PASS with expected no-story warning;
- backend guard PASS, 42 tests passed;
- `git diff --check` PASS;
- corrected frontend-directory forbidden dependency check returned empty for Playwright/test-runner/addon-vitest packages;
- focused `claude.cmd --print` review and follow-up found NO BLOCKING FINDINGS.

Current closeout state:

```text
PENDING_STAGE_COMMIT_PUSH
```

Recommended next route after S6-SB-B closeout:

```text
OPEN_S6_SB_C_STORYBOOK_STATIC_CORE_SURFACE_STORIES
```

S6-SB-C should remain bounded to mock-only P1/P2/P3 static Storybook stories driven by the repo-local fixture, with Playwright still separate.

## 20. Update 2026-04-25: G0 Pre-Start Confirmation

G0 pre-start confirmation record:

```text
docs\S6_G0_PRE_START_CONFIRMATION_2026_04_25.md
```

Decision:

```text
G0_PRE_START_CONFIRMATION_PASS_WITH_NON_BLOCKING_RATIFICATION_CHECKPOINTS
```

Confirmed items:

- G0-01 checklist receipt is now recorded as a repo-local automation receipt for implementor / reviewer / TL / design / governance owner surfaces;
- G0-02 baseline version table is confirmed from PRD v1.0 and GoNoGo v0.2.1 current execution package references;
- G0-05 P3 Contract full ratification is scheduled before the first `P3-MV-*` implementation ticket;
- G0-06 P2 v0.3 lightweight ratification is scheduled before the first `P2-AP-*` implementation ticket;
- G0-07 `NV-01`~`NV-07` plus `HF-01` are present in Visual Kickoff v0.3 first design batch evidence;
- G0-08 first bounded Sprint 0 Jira smoke tickets are created and verified;
- G0-09 AI_COLLAB execution fields are present in Backlog Tracker v0.4 and Jira smoke task metadata.

Interpretation:

- G0 confirmation is automation-owned; Human/Jarvis is not responsible for manually executing these checks.
- Current P1, Storybook, mock fixture, route/handoff, and other bounded mock-only automation can continue under exact ticket checklists.
- P2 implementation remains gated by `P2_V0_3_LIGHTWEIGHT_RATIFICATION_BEFORE_FIRST_P2_AP_IMPLEMENTATION`.
- P3 implementation remains gated by `P3_FULL_RATIFICATION_BEFORE_FIRST_P3_MV_IMPLEMENTATION`.
- Full Jira/Linear backlog import or idempotent sync still requires separate authorization.

Recommended next route remains:

```text
OPEN_S6_SB_C_STORYBOOK_STATIC_CORE_SURFACE_STORIES
```

## 21. Update 2026-04-25: Sprint 0 E0-01 Route Insertion

New incoming Sprint 0 execution-gate inputs were reviewed:

```text
D:\产品设计\secupilot0421\incoming_pending\SecuPilot_Frontend_Sprint_0_Execution_Checklist_and_PR_Review_Gate_v0.2.md
D:\产品设计\secupilot0421\incoming_pending\SecuPilot_PR_Brief_E0-01_ResolvedSurfaceContext_ContextValidator_SH-08_v0.2.md
```

Route decision:

```text
OPEN_E0_01_RESOLVED_SURFACE_CONTEXT_VALIDATOR_SH08
```

Ticket launch checklist:

```text
docs\S6_E0_01_RESOLVED_SURFACE_CONTEXT_TICKET_LAUNCH_CHECKLIST_2026_04_25.md
```

Reason:

- `E0-01` defines the root frontend rendering authority before page composition;
- Storybook first story set depends on validated `ResolvedSurfaceContext` / provider behavior;
- Playwright seed should test the validator and `SH-08` red lines after the foundation exists;
- SWE remains disabled because `E0-01` defines authority and fail-closed security behavior, not a bulk implementation task.

Version reconciliation:

```text
Accept Sprint 0 checklist v0.2 and E0-01 PR Brief v0.2 as execution-gate inputs.
Do not roll current source of truth back to Backlog Tracker v0.2.
GoNoGo v0.2.1, Backlog Tracker v0.4, Visual Kickoff v0.3, and G0 confirmation remain current.
```

Updated route order:

1. `E0-01` — ResolvedSurfaceContext + ContextValidator + SH-08.
2. `E0-02` — Mock Fixture Adapter phase states.
3. `E0-03` — Storybook first story set.
4. `E0-04` — Playwright LC-P / LC-B / LC-N seed.

Route implications:

- `OPEN_S6_SB_C_STORYBOOK_STATIC_CORE_SURFACE_STORIES` is deferred until `E0-01` closeout passes or is explicitly accepted by Jarvis.
- No P1/P2/P3 page implementation starts under `E0-01`.
- Claude Code focused review is required after implementation diff.
- Claude Web architecture/governance review is required because `E0-01` defines root rendering authority and fail-closed validation behavior.
- `E0-01` later closed in commit `aaaa199`.

## 22. Update 2026-04-25: E0-01 Implementation Gate

E0-01 implementation result:

```text
IMPLEMENTED_GATE_PASS_CLAUDE_WEB_PASS
```

Implemented:

- `ResolvedSurfaceContext` type contract;
- fail-closed `ContextValidator`;
- sanitized `SH-08 / Security Halt`;
- `ResolvedSurfaceContextProvider` skeleton;
- unit/component tests.

Gate evidence:

- frontend test PASS, 25 tests passed;
- frontend build PASS;
- backend guard PASS, 42 tests passed;
- `git diff --check` PASS;
- Claude Code focused review: `NO BLOCKING FINDINGS` after P2 fix and re-review;
- Claude Web architecture/governance review via governed AdsPower review-prompt transfer: `E0-01_DECISION: PASS`.

Claude Web informational notes were non-blocking: simple fail-closed real-data-like marker detection may false-positive on future synthetic fixtures, visible `SecurityHaltCode` reason text can be hardened later, and non-P2 `action_mode === null` semantics were confirmed intentional.

Claude Code review found one P2 closeout-before-finish issue: raw technical payload detection was limited to P3 role/surface. The issue was fixed by rejecting raw technical payloads across all surfaces, with added tests for P1 raw payload and `CROSS_SURFACE` walkthrough behavior.

Mandatory external architecture/governance state:

```text
CLAUDE_WEB_REVIEW_PASS
```

No downstream implementation has started yet for:

```text
E0-02
E0-03
E0-04
```

The Claude Web review gate no longer blocks E0-01. E0-01 closeout was committed and pushed as `aaaa199 Implement Sprint 0 E0-01 surface context`.

## 23. Update 2026-04-25: E0-02 Launch Checklist

E0-02 launch checklist:

```text
docs\S6_E0_02_CORE_SURFACE_MOCK_FIXTURE_ADAPTER_LAUNCH_CHECKLIST_2026_04_25.md
```

Checklist result:

```text
READY_FOR_JARVIS_IMPLEMENTATION_GO
```

Scope:

- map the repo-local fixture Phase 0-6 records into `ResolvedSurfaceContext`;
- validate every adapted phase through `validateResolvedSurfaceContext`;
- optionally update current app wiring only to replace existing app-local phase/role/coverage/case-state derivation with adapter output while preserving behavior;
- add focused unit/component tests.

Non-goals remain:

- no new P1/P2/P3 page implementation;
- no Storybook stories;
- no Playwright E2E;
- no backend/runtime/API/schema;
- no real data, secrets, launch, deploy, public endpoint, or external pilot;
- no broad abstraction or service/registry layer.

Jira cloud state:

```text
NO_CLOUD_MUTATION
```

Jira delta artifacts are generated outside the repo under `D:\产品设计\secupilot0421` for Jarvis review before any cloud sync.

Next required human/Jarvis decision:

```text
Approve or hold E0-02 implementation GO.
```
