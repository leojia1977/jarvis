# S6 E0-04C App Redline Renderability Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 E0-04C App Redline Renderability Launch Checklist 2026-04-27 |
| Ticket | `E0-04C` |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_PENDING_CLOSEOUT_AUTHORIZATION |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `d4d74d4` |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | conditional |
| SWE | disabled |

This checklist launches the exact prerequisite ticket `E0-04C` only.

## 2. Purpose

`E0-04B` remains on implementation HOLD because the current Playwright suite runs the Vite app, while the deeper redline states are currently inspectable only in Storybook registry views.

`E0-04C` creates a narrow app-level renderability bridge so the Vite app can expose existing, validated E0-02B boundary and resolver-degradation fixture states as static mock-only DOM. This gives later Playwright redline tests something real to assert without inventing product workflows.

## 3. Source Authority

Current governed source-of-truth:

- `docs/S6_E0_01_RESOLVED_SURFACE_CONTEXT_TICKET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_02_CORE_SURFACE_MOCK_FIXTURE_ADAPTER_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_02B_FIXTURE_QA_EXPANSION_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_E0_03_STORYBOOK_FIRST_STORY_SET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_03B_STORYBOOK_NEGATIVE_BOUNDARY_STORIES_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_E0_04_PLAYWRIGHT_LCP_LCB_LCN_SEED_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_04B_PLAYWRIGHT_LCB_LCN_REDLINE_EXPANSION_LAUNCH_CHECKLIST_2026_04_27.md`
- `frontend/src/secupilot/surface/fixtures/fixtureRegistry.ts`
- `frontend/src/secupilot/surface/fixtures/mockFixtureAdapter.ts`
- `frontend/src/secupilot/surface/context/validateResolvedSurfaceContext.ts`

Authority notes:

- `ResolvedSurfaceContext` and `ContextValidator` remain the root authority.
- App renderability hooks may use only existing validated fixture registry entries.
- HTML prototypes remain visual reference only, not implementation source.

## 4. Launch Verdict

Decision:

```text
GO_FOR_STATIC_APP_REDLINE_RENDERABILITY_ONLY
```

Interpretation:

- E0-04C may add app-level mock-only renderability for selected existing `boundary_case` and `resolver_degradation` fixture IDs.
- E0-04C may add focused component tests proving the new DOM markers exist for selected static redline states.
- E0-04C must not add Playwright tests; that remains E0-04B or a later ticket after this ticket closes.
- E0-04C must not implement P2 concurrency workflows, state migration, backend signals, or real product behavior.

## 5. Exact Allowed Files

Allowed files:

- `docs/S6_E0_04C_APP_REDLINE_RENDERABILITY_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`

Read-only references:

- `frontend/src/secupilot/surface/fixtures/fixtureRegistry.ts`
- `frontend/src/secupilot/surface/fixtures/mockFixtureAdapter.ts`
- `frontend/src/secupilot/surface/fixtures/fixtureTypes.ts`
- `frontend/src/secupilot/surface/context/types.ts`
- `frontend/src/secupilot/surface/context/validateResolvedSurfaceContext.ts`
- `frontend/src/secupilot/surface/components/SecurityHalt.tsx`
- `frontend/tests/e2e/core-surface.logic-collision.spec.ts`
- `frontend/tests/e2e/core-surface.permission-guards.spec.ts`
- `frontend/tests/e2e/core-surface.p3-dom-isolation.spec.ts`
- `frontend/playwright.config.ts`

No other file may be changed unless a HOLD is triggered and a new exact ticket is created.

## 6. Exact Scope

Implement only:

1. A mock-only app renderability path for selected existing registry fixtures:
   - `boundary-p3-audit-summary-unavailable`;
   - `boundary-p2-cmdb-tags-unavailable`;
   - `boundary-dirty-update-during-observation-window`;
   - `boundary-concurrency-stale-approve-rejected`;
   - `resolver-l1-blast-radius-payload`;
   - `resolver-p3-technical-detail-redaction`.
2. Static DOM markers that later Playwright can assert:
   - `data-testid="missing-signal-notice"` with `data-message-source="ui_messages"` when `ui_messages.missing_signal_notice` exists;
   - `data-testid="concurrency-inline-warning"` when `ui_messages.concurrency_state` or `ui_messages.inline_warning` indicates stale approve rejection;
   - `data-testid="resolver-degradation-notice"` when `ui_messages.resolver_degradation` exists;
   - `data-testid="manager-summary"` for P3 manager summary text that must not over-certify unsupported claims;
   - existing P3 raw host evidence absence remains preserved.
3. Component tests in `App.test.tsx` that prove:
   - boundary missing-signal notice renders with `data-message-source="ui_messages"`;
   - stale approve rejection renders inline warning as disabled/read-only, not as executable workflow;
   - resolver degradation does not unlock L1 blast radius;
   - P3 manager summary remains cautious and does not include over-certain copy such as `完全受控` or `已彻底消除`;
   - poison-pill fixture IDs are not accepted by the app renderability path.

## 7. Non-Goals

This ticket must not implement:

- Playwright tests or Playwright config changes;
- Storybook changes;
- new fixtures, fixture registry entries, fixture adapter changes, or validator changes;
- `validate=false` usage;
- poison-pill rendering;
- P2 approve/reject/delay/observe composer;
- P2 concurrency workflow or actual stale approve mutation;
- observation-window countdown, timer, `page.clock.fastForward`, `emitStateSync`, backend `STATE_SYNC`, polling, WebSocket, runtime, API, or schema behavior;
- route handoff or cross-surface propagation;
- real data, anonymized real data, credentials, tokens, secrets, deploy, public endpoint, or external pilot.

## 8. Required Semantics

Required:

- every renderable redline state must come from an existing validated fixture via `mockFixtureAdapter.getFixture(id)` default validation;
- app renderability must be read-only and mock-only;
- URL/localStorage/sessionStorage must not become authority sources;
- Storybook args must not become authority sources;
- poison-pill fixtures must not render;
- missing signals must degrade honestly and must not unlock hidden fields;
- P3 raw host evidence must remain absent from DOM;
- P3 manager summary must avoid over-certain wording when unsupported claims exist;
- any app prop or selector introduced for tests/stories must be explicitly mock-only and must not imply production route authority.

## 9. Required Tests And Commands

Frontend:

```powershell
cd frontend
npm run test -- --run
npm run build
npm run build-storybook
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

Claude Web/external review is conditional and required only if implementation changes authority semantics, validator strictness, backend/runtime/API/schema, route handoff, cross-surface propagation, product workflow semantics, or Go/No-Go mandatory trigger categories.

## 10. HOLD Conditions

HOLD immediately if:

- implementation needs files outside the allowed list;
- implementation needs new fixtures, fixture registry changes, adapter changes, validator changes, Playwright changes, Storybook changes, dependencies, backend/runtime/API/schema, route handoff, or cross-surface propagation;
- implementation needs `validate=false`;
- poison-pill contexts must be rendered to satisfy tests;
- UI behavior becomes executable workflow instead of static read-only redline renderability;
- P2 concurrency or observation-window state migration is needed;
- P3 raw host evidence enters DOM;
- tests/build/storybook build fail;
- Claude Code review returns blocking findings;
- Claude Web mandatory trigger fires.

## 11. Rollback

Rollback condition:

```text
Revert E0-04C app/test/checklist/route/handoff changes if frontend tests/build, Storybook build, backend guard, diff check, or review fail, or if scope expands outside allowed files.
```

## 12. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- exact scope is small and app/test-local;
- no separate SWE exact sub-ticket has been created.

## 13. Implementation Decision

Decision:

```text
READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO_WITH_BOUNDS
```

Authorized implementation boundary:

```text
Implement E0-04C only if changes remain limited to App static redline renderability, focused component tests, and closeout records.
```

E0-04B Playwright implementation remains HOLD until E0-04C closes and a separate E0-04B relaunch proves exact Playwright assertions.

## 14. Implementation Closeout Evidence

Implementation result:

```text
IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_PENDING_CLOSEOUT_AUTHORIZATION
```

Implemented files:

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`

Implemented behavior:

- added a mock-only `Mock redline fixture` selector that accepts only the closed E0-04C allowlist;
- renders selected existing E0-02B boundary and resolver-degradation fixtures through `mockFixtureAdapter.getFixture(id)` with default validation;
- added static, read-only app DOM markers for later Playwright assertions:
  - `data-testid="missing-signal-notice"` with `data-message-source="ui_messages"`;
  - `data-testid="concurrency-inline-warning"` with disabled/read-only semantics;
  - `data-testid="resolver-degradation-notice"`;
  - `data-testid="blast-radius-redline"` with `data-visibility-state="OFF"`;
  - `data-testid="manager-summary"` with cautious P3 copy.
- redline mode clears when selecting a normal phase or role, preventing stale redline authority from leaking into baseline phase navigation.

Focused tests added:

- missing-signal notice renders from `ui_messages`;
- stale approve rejection renders as disabled inline warning without workflow controls;
- L1 resolver degradation does not unlock blast radius;
- P3 manager summary avoids over-certain copy and keeps raw host evidence absent;
- poison-pill fixture IDs are not exposed as app renderability options.

Explicitly not implemented:

- Playwright tests;
- Storybook changes;
- fixture registry, fixture adapter, or validator changes;
- `validate=false`;
- poison-pill rendering;
- P2 concurrency workflow;
- observation-window timer/state migration, `emitStateSync`, backend `STATE_SYNC`;
- route handoff, cross-surface propagation;
- backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot behavior.

Gate evidence:

```text
npm run test -- --run
PASS: 5 test files, 52 tests

npm run build
PASS

npm run build-storybook
PASS: Storybook completed successfully; Vite chunk-size warning only

py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
PASS: 42 tests

git diff --check
PASS: line-ending warning only
```

Claude Code focused review:

```text
PASS_WITH_FINDINGS, then PASS after F2 was fixed
```

Final review result:

```text
PASS
```

External review:

```text
NOT_REQUIRED_FOR_E0_04C
```

Reason:

- no authority semantic change;
- no validator strictness change;
- no fixture registry or adapter change;
- no executable product workflow;
- no Playwright/backend/runtime/API/schema, route handoff, cross-surface propagation, real-data, secrets, deploy, public endpoint, or external pilot behavior.

## 15. Closeout Decision

Decision:

```text
READY_FOR_AUTHORIZED_STAGE_COMMIT_PUSH
```

Next route after closeout:

```text
OPEN_E0_04B_STATIC_REDLINE_PLAYWRIGHT_RELAUNCH_AFTER_E0_04C_CLOSEOUT
```

The next E0-04B relaunch may evaluate static Playwright assertions for the newly renderable app DOM markers, but material observation-window migration, P2 concurrency workflow execution, backend `STATE_SYNC`, and route handoff remain out of scope unless a later exact ticket creates those capabilities.
