# S6 E0-04B Playwright LC-B LC-N Redline Expansion Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 E0-04B Playwright LC-B LC-N Redline Expansion Launch Checklist 2026-04-27 |
| Ticket | `E0-04B` |
| Status | HOLD_FOR_IMPLEMENTATION_PENDING_RENDERABLE_REDLINE_SCOPE |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `4afc584` |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | conditional |
| SWE | disabled |

This checklist evaluates the exact follow-up ticket `E0-04B` only.

## 2. Purpose

`E0-04B` is intended to expand Playwright LC-B / LC-N redline coverage after the completed `E0-04` seed.

The current launch decision is intentionally conservative because several requested redlines need a renderable UI or explicit state-sync harness that does not yet exist in the current app.

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
HOLD_FOR_IMPLEMENTATION_PENDING_E0_03B_CLOSEOUT_AND_EXACT_RENDERABLE_REDLINE_SCOPE
```

Reason:

- E0-03B has not yet been implemented or closed, so the final Storybook/fixture inspection surface for negative and boundary cases is not available.
- `missing-signal-notice`, `concurrency-inline-warning`, stale approve rejection, and observation-window timer migration need exact renderable DOM or state-sync harness entry points before Playwright can assert them safely.
- The current app has E0-04 seed coverage for LC-P and selected LC-B/LC-N guards, but it does not implement P2 concurrency workflow, backend `STATE_SYNC`, or `emitStateSync` material migration.

## 5. Future Exact Allowed Files

If this ticket is later reopened after E0-03B closeout and exact renderable scope exists, candidate allowed files must be narrowed again. The current candidate set is:

- `docs/S6_E0_04B_PLAYWRIGHT_LCB_LCN_REDLINE_EXPANSION_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/tests/e2e/core-surface.logic-collision.spec.ts`
- `frontend/tests/e2e/core-surface.permission-guards.spec.ts`
- `frontend/tests/e2e/core-surface.p3-dom-isolation.spec.ts`

Optional new file only if explicitly selected during relaunch:

- `frontend/tests/e2e/core-surface.redline-expansion.spec.ts`

Read-only references:

- `frontend/src/App.tsx`
- `frontend/src/secupilot/surface/storybook/CoreSurfaceStories.stories.tsx`
- `frontend/src/secupilot/surface/fixtures/fixtureRegistry.ts`
- `frontend/src/secupilot/surface/fixtures/mockFixtureAdapter.ts`
- `frontend/src/secupilot/surface/context/types.ts`
- `frontend/playwright.config.ts`
- `frontend/package.json`

No implementation may begin from this candidate scope until the HOLD is lifted by a later exact launch decision.

## 6. Future Candidate Scope

Candidate redlines for a later GO:

1. Existing LC-N hardening:
   - P3 raw host evidence remains `not.toBeAttached()` / absent from DOM;
   - approval operations remain absent outside P2 authority;
   - URL/localStorage/sessionStorage role and coverage injection remain ignored or rejected.
2. Missing-signal visibility once a renderable boundary story or app route exists:
   - `missing-signal-notice` must carry `data-message-source="ui_messages"`;
   - missing signals must not unlock hidden fields.
3. P3 summary caution once `unsupported_claims` is renderable:
   - `expect(summaryText).not.toMatch(/完全受控|已彻底消除/i)`.
4. Observation-window timer behavior only if an explicit state-sync harness exists:
   - `await page.clock.fastForward()` may verify read-only timer display only;
   - material state migration must be driven by explicit `emitStateSync` / resolved context input immediately after the clock step.

## 7. Non-Goals

This ticket must not implement:

- P2 concurrency workflow;
- P2 approve/reject/delay/observe composer;
- backend `STATE_SYNC`, polling, WebSocket, runtime, API, or schema behavior;
- new app UI, components, pages, routes, or data-test IDs;
- Storybook changes;
- fixture registry or adapter changes;
- dependency or Playwright config changes;
- real data, anonymized real data, credentials, tokens, secrets, deploy, public endpoint, or external pilot.

## 8. Required Semantics For Any Later GO

Required:

- Playwright tests may only assert already-renderable governed mock-only states;
- `page.clock.fastForward()` may never be used as material state authority;
- material observation-window migration requires `emitStateSync` / resolved context input;
- P3 raw evidence must be absent from DOM, not merely hidden by CSS;
- P3 manager summary must avoid over-certain copy when unsupported claims exist;
- LC-N redlines must remain fail-closed and must not be relaxed to make tests pass.

## 9. Required Tests And Commands For Any Later GO

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

HOLD remains active while any of the following are true:

- E0-03B is not implemented and closed;
- exact renderable DOM/test IDs for the selected redlines are not present;
- `emitStateSync` / resolved context input is not available for material observation-window migration;
- Playwright tests require app UI, component, route, Storybook, fixture, adapter, validator, backend/runtime/API/schema, dependency, or config changes;
- tests would need to assert product behavior not already implemented;
- real data, secrets, deploy, public endpoint, external pilot, or launch behavior is needed.

## 11. Rollback

No implementation is authorized in the current state, so no code rollback path is opened.

If a later relaunch lifts HOLD, rollback must revert only the exact Playwright spec/checklist/route/handoff changes from that relaunch.

## 12. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- implementation is currently on HOLD;
- no exact file/test scope has been proven implementable;
- no separate SWE exact sub-ticket has been created.

## 13. Implementation Decision

Decision:

```text
IMPLEMENTATION_HOLD
```

Allowed next action:

```text
Close out E0-03B first, then relaunch E0-04B with exact renderable redline scope.
```
