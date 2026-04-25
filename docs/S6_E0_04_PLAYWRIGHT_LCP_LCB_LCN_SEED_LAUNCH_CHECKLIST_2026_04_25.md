# S6 E0-04 Playwright LC-P LC-B LC-N Seed Launch Checklist 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 E0-04 Playwright LC-P LC-B LC-N Seed Launch Checklist 2026-04-25 |
| Ticket | `E0-04` |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_WITH_NON_BLOCKING_NOTES |
| Date | 2026-04-25 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `94ebd21` |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | conditional |
| SWE | disabled |

This checklist launches Sprint 0 `E0-04` only.

## 2. Jarvis Authorization

Jarvis authorized the 48h bounded automation queue:

```text
E0-03-LAUNCH -> E0-03-IMPLEMENT -> E0-04-LAUNCH -> E0-04-IMPLEMENT
```

Authorization includes required gate, Claude Code focused review, Jira cloud sync, and stage/commit/push for each PASS ticket.

## 3. Source Authority

Current governed source-of-truth:

- `SecuPilot_Playwright_E2E_Acceptance_Plan_v0.1.md`
- `SecuPilot_Frontend_Sprint_0_Execution_Checklist_and_PR_Review_Gate_v0.2.md`
- `SecuPilot_Core_Surface_Mock_Fixture_Integration_v0.1.md`
- `SecuPilot_Storybook_Cross_Surface_Stories_v0.1.md`
- `docs/S6_E0_01_RESOLVED_SURFACE_CONTEXT_TICKET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_02_CORE_SURFACE_MOCK_FIXTURE_ADAPTER_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_03_STORYBOOK_FIRST_STORY_SET_LAUNCH_CHECKLIST_2026_04_25.md`

Repo baseline:

```text
E0-01 closed in commit aaaa199.
E0-02 closed in commit 786b579.
E0-03 closed in commit 94ebd21.
```

## 4. Launch Verdict

Decision:

```text
GO_FOR_PLAYWRIGHT_SEED_ONLY
```

Interpretation:

- E0-04 may install the exact Playwright test dependency.
- E0-04 may add Playwright config and seed tests against the existing mock-only Vite app.
- E0-04 may add minimal `data-testid` attributes only when needed for stable red-line assertions.
- E0-04 may verify LC-P / LC-B / LC-N seed coverage for states already represented by the current mock fixture and app.

Blocked within E0-04:

- no P2 strong-confirm composer implementation;
- no P2 delay/observe/reject workflow implementation;
- no CS-P2-05 stale approve/concurrency implementation;
- no backend/runtime/API/schema;
- no real data, secrets, deploy, public endpoint, external pilot, or production readiness claim.

## 5. Exact Allowed Files

Allowed files:

- `docs/S6_E0_04_PLAYWRIGHT_LCP_LCB_LCN_SEED_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `.gitignore`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/playwright.config.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/tests/e2e/core-surface.logic-collision.spec.ts`
- `frontend/tests/e2e/core-surface.permission-guards.spec.ts`
- `frontend/tests/e2e/core-surface.p3-dom-isolation.spec.ts`

Read-only references:

- `frontend/src/secupilot/surface/fixtures/coreSurfaceFixtureAdapter.ts`
- `frontend/fixtures/secupilot_core_surface_fixture_v0_1.json`
- `frontend/src/secupilot/surface/storybook/CoreSurfaceStories.stories.tsx`

No other file may be changed unless a HOLD is triggered.

## 6. Exact Dependency Scope

Allowed dependency change:

```text
npm install --save-dev @playwright/test
```

Allowed browser setup command for local verification:

```text
npx playwright install chromium
```

No other dependency, lockfile, package manager, or browser channel change is authorized.

## 7. Exact Scope

Implement only:

1. `test:e2e` npm script.
2. Playwright config for the local Vite app.
3. Seed Playwright specs that verify currently available fixture-driven states:
   - LC-P seed: P1 phase 0/1, P2 observation phase 3, P2 terminal phase 5, P3 review phase 6.
   - LC-B seed: URL/storage coverage and role injection ignored.
   - LC-N seed: P1 no ActionMode DOM, P3 host raw evidence DOM absent, approved pending execution has no withdraw CTA, invalid deep links do not expose approval operations.
4. Minimal `data-testid` attributes only for stable LC assertions.

## 8. Non-Goals

This ticket must not implement:

- P2 strong confirm modal;
- P2 approve/delay/observe/reject composer;
- CS-P2-05 concurrency collision behavior;
- route handoff implementation;
- cross-surface propagation;
- backend runtime signal, polling, WebSocket, or API;
- Storybook changes beyond using E0-03 as reference;
- real data, sanitized real data, credentials, tokens, secrets, launch, deploy, public endpoint, or external pilot;
- broad component/data/service abstraction.

## 9. Required Commands

Dependency setup:

```powershell
cd frontend
npm install --save-dev @playwright/test
npx playwright install chromium
```

Frontend:

```powershell
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

Claude Web/external review is conditional and required only if implementation changes product semantics, authority semantics, validator strictness, backend/runtime/API/schema, P2/P3 ratification scope, real-data behavior, route handoff, cross-surface propagation, or Go/No-Go mandatory trigger categories.

## 10. HOLD Conditions

HOLD immediately if:

- dependency installation requires anything beyond `@playwright/test` or Chromium setup;
- Playwright cannot run locally after exact dependency setup;
- implementation needs files outside the allowed list;
- tests require P2 workflow, concurrency, backend signal, or route handoff behavior not currently implemented;
- LC-N red lines cannot be asserted without implementing new product behavior;
- URL/localStorage/sessionStorage becomes authority for role, coverage, state, AR status, action mode, or surface;
- P3 raw host evidence enters DOM;
- real data, secrets, deploy, public endpoint, external pilot, backend/runtime/API/schema, or broad abstraction is needed;
- Claude Code review returns blocking findings;
- Claude Web mandatory trigger fires.

## 11. Rollback

Rollback condition:

```text
Revert E0-04 dependency/config/spec/app/checklist/route/handoff changes if dependency install fails, Playwright cannot run, tests/build fail, review finds blocking issues, scope expands outside allowed files, or HOLD triggers fire.
```

## 12. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- execution surface is `codex`;
- dependency and browser setup require close local gate control;
- no separate SWE exact sub-ticket has been created.

## 13. Implementation Decision

Decision:

```text
READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO
```

Authorized next action:

```text
Implement E0-04 Playwright seed inside the exact dependency and file scope.
```

## 14. Implementation Closeout

Implementation result:

```text
IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_WITH_NON_BLOCKING_NOTES
```

Implemented:

- exact Playwright dependency `@playwright/test`;
- `test:e2e` script;
- Playwright Chromium seed config for the local Vite app;
- LC-P / LC-B / LC-N seed specs for current fixture-driven states;
- minimal `data-testid` attributes for stable browser assertions;
- `.gitignore` entries for Playwright local reports and test results.

Still not implemented:

- P2 strong-confirm composer;
- P2 approve/delay/observe/reject workflows;
- CS-P2-05 stale approve/concurrency behavior;
- route handoff or cross-surface propagation;
- backend/runtime/API/schema;
- real data, secrets, launch, deploy, public endpoint, or external pilot.

Gate evidence:

```text
npm install --save-dev @playwright/test
PASS

npx playwright install chromium
PASS

npm run test -- --run
PASS: 4 test files, 36 tests

npm run build
PASS

npm run build-storybook
PASS

npm run test:e2e
PASS: 5 tests

py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
PASS: 42 tests

git diff --check
PASS: line-ending warnings only
```

Claude Code focused review:

```text
PASS with non-blocking notes
```

Non-blocking notes accepted:

- some LC-N assertions are forward guards that intentionally pass by proving absent DOM today and become stronger once later views exist;
- phase-number assertions depend on the governed E0-02 fixture records;
- `action-request-panel` text assertions intentionally catch fixture-string drift;
- invalid `/approval` deep-link behavior depends on the current app catch-all layout behavior;
- future build-fidelity E2E may switch from Vite dev server to preview.

External review:

```text
NOT_REQUIRED_FOR_E0_04
```

Reason:

- no E0-01 authority semantic change;
- no `ContextValidator` loosening;
- no product workflow implementation;
- no route handoff, cross-surface propagation, backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot behavior.

Closeout decision:

```text
READY_FOR_AUTHORIZED_STAGE_COMMIT_PUSH
```
