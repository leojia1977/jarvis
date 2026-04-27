# S6 E0-02B Fixture QA Expansion Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 E0-02B Fixture QA Expansion Launch Checklist 2026-04-27 |
| Ticket | `E0-02B` |
| Status | RECONCILIATION_READY_IMPLEMENTATION_NOT_AUTHORIZED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Current repo baseline | `2a71408` |
| Primary implementor | TBD at implementation GO |
| Execution surface | `codex` unless later changed by Jarvis |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | conditional |
| SWE | disabled unless a later exact sub-ticket names it |

This record creates the `E0-02B` reconciliation and launch checklist only.

It does not authorize implementation, code changes, dependency changes, Storybook changes, Playwright changes, backend/runtime/API/schema changes, real data, secrets, deploy, public endpoint work, external pilot, stage, commit, or push.

## 2. Reconciliation Decision

Decision:

```text
ACCEPT_2026_04_27_E0_02_BRIEF_AS_POST_CLOSEOUT_EXPANSION_INPUT
```

Required note:

```text
2026-04-27 E0-02 brief v0.1 is accepted as post-closeout expansion input; it does not invalidate E0-02/E0-03/E0-04, but gates future fixture QA / cross-surface / boundary expansion.
```

Interpretation:

- `E0-02` remains closed in commit `786b579`.
- `E0-03` remains closed in commit `94ebd21`.
- `E0-04` remains closed in commit `2a71408`.
- The new 2026-04-27 brief expands fixture QA depth beyond the already closed E0-02 baseline.
- Future fixture QA, cross-surface walkthrough, boundary-case expansion, poison-pill registry, and resolver-degradation expansion should pass through `E0-02B` or a narrower child ticket.

## 3. Source Inputs

Primary new source:

```text
D:\产品设计\secupilot0421\SecuPilot_PR_Brief_E0-02_Mock_Fixture_Adapter_Phase_States_v0.1 (1).md
```

Existing governed repo sources:

- `docs/S6_E0_01_RESOLVED_SURFACE_CONTEXT_TICKET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_02_CORE_SURFACE_MOCK_FIXTURE_ADAPTER_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_03_STORYBOOK_FIRST_STORY_SET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_04_PLAYWRIGHT_LCP_LCB_LCN_SEED_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`

If the new brief conflicts with `E0-01` root context authority or `ContextValidator`, `E0-02B` must HOLD rather than weaken validation.

## 4. Current Coverage Assessment

Already covered by closed E0-02/E0-03/E0-04:

- Phase 0-6 fixture records adapt into `ResolvedSurfaceContext`.
- Each adapted phase passes `validateResolvedSurfaceContext`.
- URL, localStorage, and sessionStorage are not authority sources.
- `fixture_meta.real_data_derived=true` triggers `SH-08`.
- P1 cannot choose `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY`.
- P3 raw host evidence is excluded from context and DOM.
- Storybook and Playwright consume the validated fixture path.

Not yet covered by the closed E0-02 baseline:

- formal `MockFixtureAdapter.getFixture(id, { validate })` API;
- `validate=false` restriction for poison-pill rejection tests only;
- phase, boundary-case, poison-pill, and resolver-degradation registries;
- Phase 07 `CROSS_SURFACE` fixture;
- boundary cases for P3 audit unavailable, P2 CMDB tags unavailable, dirty observation-window update, and stale approve rejection;
- resolver degradation for L1 blast radius, L1 lineage confidence, P3 technical redaction, and search-history recorded/current level conflicts;
- fixture ownership README;
- temporal consistency checks.

## 5. Candidate Future Scope

Future E0-02B implementation may include only:

1. a mock fixture adapter API that defaults to validation;
2. fixture ID registry for phase, boundary-case, poison-pill, and resolver-degradation cases;
3. fully artificial fixture metadata validation helpers;
4. poison-pill test fixtures that intentionally fail closed to `SH-08`;
5. resolver-degradation fixtures that remain valid contexts and do not over-trigger `SH-08`;
6. boundary-case fixtures that represent degraded, readonly, disabled, or inline-warning states without page implementation;
7. focused unit tests;
8. a fixture README explaining ownership and directory rules.

## 6. Candidate Exact File Scope

A later implementation GO should stay inside this repo-conforming file set unless a new HOLD decision revises it:

- `docs/S6_E0_02B_FIXTURE_QA_EXPANSION_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/src/secupilot/surface/fixtures/coreSurfaceFixtureAdapter.ts`
- `frontend/src/secupilot/surface/fixtures/mockFixtureAdapter.ts`
- `frontend/src/secupilot/surface/fixtures/fixtureRegistry.ts`
- `frontend/src/secupilot/surface/fixtures/fixtureTypes.ts`
- `frontend/src/secupilot/surface/fixtures/README.md`
- `frontend/src/secupilot/surface/fixtures/__tests__/coreSurfaceFixtureAdapter.test.ts`
- `frontend/src/secupilot/surface/fixtures/__tests__/mockFixtureAdapter.test.ts`

Implementation must HOLD if it needs:

- `frontend/src/App.tsx`;
- Storybook story files;
- Playwright E2E files;
- backend/runtime/API/schema files;
- dependency or lockfile changes;
- real-data fixtures or anonymized real-data samples.

## 7. Required Behavior For Future Implementation

Future E0-02B implementation must preserve:

- `validate=true` as default.
- `validate=false` is allowed only inside poison-pill rejection tests.
- Production-like, Storybook, and Playwright fixture usage must use validated contexts.
- URL query, localStorage, and sessionStorage role/coverage/surface/state injection must be ignored.
- `ResolvedSurfaceContext` remains the authority.
- `fixture_meta.real_data_derived=true` triggers `SH-08`.
- Coverage degradation is not the same as fixture contamination.
- `coverage=L1 + blast_radius payload` must resolve/degrade to `blast_radius=OFF`, not trigger `SH-08`, if the resolved context is otherwise valid.
- Poison pills must fail closed and must not render P1/P2/P3 surface content.
- Boundary cases must avoid inventing product UI beyond fixture-state and test assertions.

Implementation should include the following comment where the `validate` option is defined:

```ts
// validate=false is ONLY allowed when testing poison pill rejection behavior.
// All production-like, Storybook, and Playwright fixture usage must use validate=true.
// Never set validate=false to work around context issues in page rendering.
```

## 8. Non-Goals

E0-02B must not implement:

- P1/P2/P3 page UI;
- Storybook stories;
- Playwright E2E tests;
- P2 strong confirm, approve, delay, observe, or reject workflows;
- concurrency behavior beyond fixture-state representation and unit assertions;
- route handoff or cross-surface propagation runtime behavior;
- backend/runtime/API/schema;
- live data connectors;
- real, anonymized, redacted, masked, sampled, or customer-derived data;
- secrets, credentials, launch, deploy, public endpoint, or external pilot;
- new product scope, roles, approval semantics, broad registries, or framework abstractions beyond the exact fixture layer.

## 9. Required Gates For Future Implementation

Required commands:

```powershell
cd frontend
npm run test -- --run
npm run build
```

Backend guard:

```powershell
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
```

Repo hygiene:

```powershell
git diff --check
```

Review:

```text
Claude Code focused review via claude-cmd after implementation diff.
```

Claude Web/external review is conditional and required if implementation changes root authority semantics, loosens `ContextValidator`, changes product workflow semantics, touches Storybook/Playwright/backend/runtime/API/schema, changes route handoff or cross-surface propagation behavior, introduces real-data handling, or triggers Go/No-Go mandatory review categories.

## 10. HOLD Conditions

HOLD immediately if:

- exact file scope is insufficient;
- implementation requires loosening `ContextValidator`;
- fixture adapter bypasses validation for renderable fixtures;
- `validate=false` is used outside poison-pill rejection tests;
- real, anonymized, redacted, masked, sampled, or customer-derived data is requested;
- page implementation, Storybook implementation, or Playwright implementation is needed;
- backend/runtime/API/schema changes are needed;
- URL/storage becomes authority;
- poison-pill behavior is ambiguous;
- boundary-case paths or fixture IDs cannot be assigned;
- resolver degradation would require product behavior not yet ratified;
- tests/build fail;
- Claude Code returns blocking findings;
- Claude Web mandatory trigger fires and review is unavailable.

## 11. Implementation Decision

Current decision:

```text
IMPLEMENTATION_NOT_AUTHORIZED_YET
```

Automation queue registration:

```text
AUTOMATION_CANDIDATE_PENDING_JARVIS_IMPLEMENTATION_GO
```

Interpretation:

- E0-02B is now listed as the next bounded automation candidate.
- Autonomous implementation must not start until Jarvis explicitly authorizes E0-02B bounded implementation GO.
- Until that GO exists, automation may only preserve this checklist, route, and handoff state.

Next required Jarvis decision:

```text
Authorize or hold E0-02B bounded implementation GO.
```
