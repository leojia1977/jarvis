# S6 E0-04B Playwright LC-B LC-N Redline Expansion Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 E0-04B Playwright LC-B LC-N Redline Expansion Launch Checklist 2026-04-27 |
| Ticket | `E0-04B` |
| Status | RELAUNCH_READY_FOR_STATIC_REDLINE_PLAYWRIGHT_GO_WITH_BOUNDS |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `d944887` |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | conditional |
| SWE | disabled |

This checklist evaluates the exact follow-up ticket `E0-04B` only.

## 2. Purpose

`E0-04B` is intended to expand Playwright LC-B / LC-N redline coverage after the completed `E0-04` seed and `E0-04C` app redline renderability hooks.

The current launch decision is narrowed to static app redline assertions only. Material observation-window migration, P2 workflow behavior, and backend state-sync behavior remain out of scope.

## 3. Source Authority

Current governed source-of-truth:

- `docs/S6_E0_01_RESOLVED_SURFACE_CONTEXT_TICKET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_02_CORE_SURFACE_MOCK_FIXTURE_ADAPTER_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_02B_FIXTURE_QA_EXPANSION_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_E0_03_STORYBOOK_FIRST_STORY_SET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_04_PLAYWRIGHT_LCP_LCB_LCN_SEED_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_03B_STORYBOOK_NEGATIVE_BOUNDARY_STORIES_LAUNCH_CHECKLIST_2026_04_27.md`
- `D:\产品设计\secupilot0421\visual negative\SecuPilot_Automation_Team_Handoff_and_E0-02_Launch_Pack_v0.1.md`
- `D:\产品设计\secupilot0421\visual negative\SecuPilot_Visual_Negative_Frames_Brief_v0.1.md`
- `D:\产品设计\secupilot0421\visual negative\SecuPilot_Automation_Team_E0-02_Launch_Pack_v0.1.1.zip`

Authority notes:

- `AI_COLLAB Amendment v0.2` governs execution surface, reviewer floor, single-writer lock, and SWE HOLD-on-expansion behavior throughout Sprint 0.
- Playwright may verify only behavior that is already renderable through governed mock-only contexts.
- Playwright must not become the mechanism that invents missing product behavior.

## 4. Launch Verdict

Decision:

```text
GO_FOR_STATIC_APP_REDLINE_PLAYWRIGHT_ASSERTIONS_ONLY
```

Reason:

- E0-03B is implemented and closed, so the Storybook/fixture inspection surface for negative and boundary cases exists.
- E0-04C is implemented and closed, so the Vite app now exposes exact static DOM markers for selected existing boundary and resolver-degradation fixtures.
- `missing-signal-notice`, `concurrency-inline-warning`, `resolver-degradation-notice`, `blast-radius-redline`, and `manager-summary` are now renderable through governed mock-only fixture IDs.
- Playwright can safely assert these static markers without inventing P2 workflow behavior, backend `STATE_SYNC`, `emitStateSync`, or material observation-window migration.

## 5. Exact Allowed Files

Implementation files:

- `docs/S6_E0_04B_PLAYWRIGHT_LCB_LCN_REDLINE_EXPANSION_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/tests/e2e/core-surface.redline-expansion.spec.ts`

Read-only references:

- `frontend/src/App.tsx`
- `frontend/tests/e2e/core-surface.logic-collision.spec.ts`
- `frontend/tests/e2e/core-surface.permission-guards.spec.ts`
- `frontend/tests/e2e/core-surface.p3-dom-isolation.spec.ts`
- `frontend/playwright.config.ts`
- `frontend/package.json`

Not allowed for edits in this ticket:

- `frontend/src/App.tsx`
- `frontend/src/secupilot/surface/storybook/CoreSurfaceStories.stories.tsx`
- `frontend/src/secupilot/surface/fixtures/fixtureRegistry.ts`
- `frontend/src/secupilot/surface/fixtures/mockFixtureAdapter.ts`
- `frontend/src/secupilot/surface/context/types.ts`
- `frontend/playwright.config.ts`
- `frontend/package.json`

If any assertion requires changing a not-allowed file, this ticket must HOLD and a separate exact ticket must be created.

## 6. Exact Implementation Scope

Allowed static Playwright assertions:

1. `boundary-p2-cmdb-tags-unavailable`
   - selecting the mock redline fixture renders `missing-signal-notice`;
   - `missing-signal-notice` carries `data-message-source="ui_messages"`;
   - hidden or unavailable fields remain unavailable and do not unlock UI behavior.
2. `boundary-concurrency-stale-approve-rejected`
   - selecting the mock redline fixture renders `concurrency-inline-warning`;
   - the warning is static and read-only;
   - approve/reject/delay/observe operation buttons remain absent.
3. `resolver-l1-blast-radius-payload`
   - selecting the mock redline fixture keeps coverage at L1;
   - `resolver-degradation-notice` is rendered;
   - `blast-radius-redline` is rendered with `data-visibility-state="OFF"`;
   - blast radius content remains unavailable under L1.
4. `resolver-p3-technical-detail-redaction`
   - selecting the mock redline fixture renders `manager-summary`;
   - `manager-summary` avoids over-certain wording, including `expect(summaryText).not.toMatch(/完全受控|已彻底消除/i)`;
   - host raw evidence remains absent from the DOM.
5. Poison-pill fixtures remain unavailable through the app redline selector.

Allowed implementation pattern:

- create one focused Playwright spec file for static redline assertions;
- use the existing Vite app served by the current Playwright config;
- use the existing `Mock redline fixture` selector and existing test IDs from E0-04C;
- do not add, rename, or reinterpret product behavior.

## 7. Non-Goals

This ticket must not implement:

- P2 concurrency workflow;
- P2 approve/reject/delay/observe composer;
- backend `STATE_SYNC`, polling, WebSocket, runtime, API, or schema behavior;
- new app UI, components, pages, routes, or data-test IDs;
- Storybook changes;
- fixture registry or adapter changes;
- dependency or Playwright config changes;
- `emitStateSync` or material observation-window state migration;
- `page.clock.fastForward()` timer behavior;
- real data, anonymized real data, credentials, tokens, secrets, deploy, public endpoint, or external pilot.

## 8. Required Semantics

Required:

- Playwright tests may only assert already-renderable governed mock-only states;
- `page.clock.fastForward()` may never be used as material state authority;
- material observation-window migration remains out of scope for this ticket and requires a later exact ticket with `emitStateSync` / resolved context input;
- P3 raw evidence must be absent from DOM, not merely hidden by CSS;
- P3 manager summary must avoid over-certain copy when unsupported claims exist;
- LC-N redlines must remain fail-closed and must not be relaxed to make tests pass.

## 9. Required Tests And Commands

Frontend:

```powershell
cd frontend
npm run test -- --run
npm run build
npm run build-storybook
npm run test:e2e
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

Claude Web/external review is conditional and required if implementation touches architecture/governance authority, root context semantics, validator strictness, backend/runtime/API/schema, route handoff, cross-surface propagation, or Go/No-Go mandatory trigger categories.

## 10. HOLD Conditions

HOLD if any of the following become true:

- any selected redline assertion requires changing App, fixture, adapter, validator, Storybook, Playwright config, dependency, backend, runtime, API, or schema files;
- exact renderable DOM/test IDs for the selected static redlines are missing or insufficient;
- Playwright tests require app UI, component, route, Storybook, fixture, adapter, validator, backend/runtime/API/schema, dependency, or config changes;
- tests would need to assert product behavior not already implemented;
- observation-window material migration, `emitStateSync`, backend `STATE_SYNC`, or P2 concurrency workflow behavior is needed;
- real data, secrets, deploy, public endpoint, external pilot, or launch behavior is needed.

## 11. Rollback

Rollback must revert only:

- `frontend/tests/e2e/core-surface.redline-expansion.spec.ts`
- this checklist closeout edits;
- route/handoff closeout edits.

## 12. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- Playwright redline assertions are narrow but security-sensitive;
- no separate SWE exact sub-ticket has been created;
- if SWE is later used, it must receive an exact sub-ticket with the single Playwright spec file, exact test commands, rollback path, HOLD conditions, and reviewer assigned.

## 13. Implementation Decision

Decision:

```text
READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO_WITH_BOUNDS
```

Allowed implementation:

```text
Implement static Playwright assertions only in frontend/tests/e2e/core-surface.redline-expansion.spec.ts.
```

## 14. Relaunch Readiness Check 2026-04-27

Relaunch input:

```text
E0-03B is closed as COMMITTED_PUSHED_f6d0fed.
E0-04C is closed as COMMITTED_PUSHED_37362e0.
```

Readiness reassessment:

```text
STATIC_REDLINE_PLAYWRIGHT_GO
```

What changed since the first launch checklist:

- E0-03B now provides Storybook registry views for validated phase, boundary-case, resolver-degradation, and non-renderable poison-pill inventory inspection.
- E0-04C now provides Vite-app renderability for selected existing boundary and resolver-degradation fixture IDs.
- E0-04C exposes exact static DOM markers that Playwright can assert without changing App, fixture, adapter, validator, Storybook, dependency, or Playwright config.

Why the old HOLD is lifted narrowly:

- current Playwright config serves the Vite app, and E0-04C made the selected redlines renderable in that app;
- static LC-B/LC-N marker assertions can now be implemented without scope invention;
- material observation-window migration, real stale-state workflow execution, and backend `STATE_SYNC` remain HOLD for a later exact ticket.

Allowed next route:

```text
OPEN_E0_04B_STATIC_REDLINE_PLAYWRIGHT_IMPLEMENTATION
```

No config, dependency, Storybook, App, fixture, adapter, validator, backend/runtime/API/schema, real-data, secrets, deploy, public endpoint, external pilot, material observation-window migration, or P2 workflow change is authorized by this readiness check.
