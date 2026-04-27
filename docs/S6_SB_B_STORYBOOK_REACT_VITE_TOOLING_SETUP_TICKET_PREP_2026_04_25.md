# S6-SB-B Storybook React Vite Tooling Setup Ticket Prep 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6-SB-B Storybook React Vite Tooling Setup Ticket Prep 2026-04-25 |
| Ticket | `S6-SB-B` |
| Scope | Storybook React Vite dependency installation and minimal config |
| Status | IMPLEMENTED_GATE_PASS_COMMITTED_PUSHED |
| Date | 2026-04-25 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `75aecc2` |
| Prior Storybook decision | `docs\S6_SB_A_STORYBOOK_STATIC_CORE_SURFACE_STORIES_TICKET_PREP_2026_04_25.md` |
| Fixture | `frontend\fixtures\secupilot_core_surface_fixture_v0_1.json` |
| Lane | Yellow bounded frontend tooling |
| Execution surface | `codex` |
| Review surface | `claude-cmd` focused review after dependency/config diff |
| Human authorization | Storybook dependency install approved |

This record authorizes the minimal Storybook React Vite tooling setup needed before static core-surface stories can be implemented.

It does not authorize Playwright setup, product story implementation, P2 Approval Surface implementation, P3 Manager View implementation, backend/API/schema changes, P1 to P2 AR propagation, P2 to P3 audit propagation, route handoff, real-data handling, launch, deploy, public endpoint work, external pilot execution, staging, commit, or push by itself.

## 2. Governing Sources

Use this authority order:

1. `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版 (2).md`
2. `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2 (1).md`
3. `SecuPilot_Core_Surface_Logic_Collision_Walkthrough_v0.2.md`
4. `SecuPilot_Core_Surface_Mock_Fixture_Integration_v0.1.md`
5. `SecuPilot_Storybook_Cross_Surface_Stories_v0.1.md`
6. `docs\S6_SB_A_STORYBOOK_STATIC_CORE_SURFACE_STORIES_TICKET_PREP_2026_04_25.md`
7. Storybook official React Vite / install documentation as tooling reference only

Official Storybook tooling references:

- `https://storybook.js.org/docs/get-started/install`
- `https://storybook.js.org/docs/get-started/frameworks/react-vite`

## 3. Exact Behavior

Install and configure Storybook for the existing Vite React TypeScript frontend.

Required behavior:

| Area | Required behavior |
| --- | --- |
| Dependency setup | Add the minimal Storybook React Vite dependencies and scripts to `frontend/package.json` / `frontend/package-lock.json`. |
| Config setup | Add minimal `.storybook` configuration for React Vite. |
| Boilerplate handling | Do not keep generic tutorial/sample stories as final governed output. Remove generated boilerplate or replace it with a minimal governed placeholder that does not claim product story coverage. |
| Commands | `npm run storybook -- --help` and `npm run build-storybook` must be available after setup. |
| Existing gates | Preserve existing frontend tests/build and backend guard. |

## 4. Exact Non-Goals

This ticket must not implement:

- P1/P2/P3 static product stories;
- Walkthrough/CoreSurfaceLogicCollision story;
- Playwright setup;
- Playwright tests;
- product page implementation beyond existing app;
- P2 Approval Surface implementation;
- P3 Manager View implementation;
- P1 Action Request modal;
- P1 to P2 AR propagation;
- P2 to P3 audit propagation;
- route handoff;
- backend/API/schema changes;
- real-data integration;
- localStorage/sessionStorage/URL-based authorization or coverage;
- static HTML prototype copy/paste;
- launch/deploy/public endpoint/external pilot behavior.

## 5. Exact Allowed Files

Allowed files for this ticket:

- `docs/S6_SB_B_STORYBOOK_REACT_VITE_TOOLING_SETUP_TICKET_PREP_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/.storybook/main.ts`
- `frontend/.storybook/preview.ts`
- generated sample files only if removed or replaced with governed placeholders before closeout

No other file may be changed for S6-SB-B unless a HOLD is triggered and a new decision record expands scope.

## 6. Required Commands

Frontend:

```powershell
cd frontend
npm run test -- --run
npm run build
npm run storybook -- --help
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

## 7. Required Assertions

Closeout-visible assertions must cover:

- `frontend/package.json` contains Storybook scripts;
- `.storybook/main.ts` uses React Vite framework;
- Storybook can build successfully;
- generated generic tutorial/sample story files are not retained as final product stories;
- no Playwright dependency or config is introduced;
- no backend/API/schema files are changed;
- no product semantics or cross-surface propagation are implemented.

## 8. Max Change Budget

Maximum expected implementation scope:

- Storybook dependencies in `package.json` / `package-lock.json`;
- minimal `.storybook` configuration;
- no product component refactor;
- no app code changes unless the Storybook CLI generates a file that must be removed.

## 9. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- dependency/tooling install is local and bounded;
- the exact file scope is small;
- no separate SWE command path is required.

## 10. Review Path

Required review path:

```text
Focused code/tooling review after dependency/config diff, preferably via claude-cmd / Claude Code if available.
```

Claude Web / external product-architecture-governance review is not required unless implementation:

- adds product stories or product behavior;
- changes architecture beyond Storybook setup;
- introduces Playwright or other tooling outside Storybook;
- changes backend/API/schema behavior;
- touches Red/HOLD trigger categories.

## 11. Rollback

Rollback condition:

```text
Revert S6-SB-B Storybook setup if install fails, build-storybook fails, existing gates fail, scope expands outside allowed files, or HOLD triggers fire.
```

## 12. HOLD Conditions

HOLD if:

- Storybook CLI asks for an ambiguous product/framework choice that cannot be resolved from Vite React TypeScript;
- dependency install fails or produces incompatible versions;
- generated files extend outside the allowed file list and cannot be safely removed;
- Playwright dependencies or config appear;
- product story implementation begins inside S6-SB-B;
- backend/API/schema files change;
- real data, credentials, network app behavior, launch, deploy, public endpoint, or external pilot behavior appears;
- broad component abstraction, design-system registry, or app refactor appears.

## 13. Decision

Decision:

```text
READY_FOR_EXACT_TOOLING_IMPLEMENTATION
```

Authorized next technical action:

```text
Install and configure minimal Storybook React Vite tooling inside the exact allowed file scope, then run the required gates.
```

## 14. Implementation Result 2026-04-25

Implementation result:

```text
IMPLEMENTED_GATE_PASS
```

Install command used:

```powershell
npm create storybook@latest -- --yes --no-dev --no-features --type react --builder vite --package-manager npm --disable-telemetry --loglevel info
```

Installed Storybook CLI version:

```text
10.3.5
```

Implemented files:

- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/.storybook/main.ts`
- `frontend/.storybook/preview.ts`

Documentation files updated:

- `docs/S6_SB_B_STORYBOOK_REACT_VITE_TOOLING_SETUP_TICKET_PREP_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`

Generated tutorial/sample Storybook files under `frontend/src/stories` were removed and are not retained as governed output.

No Playwright setup was introduced. The corrected frontend-directory dependency check returned empty for:

```text
playwright
@playwright/test
@storybook/addon-vitest
@storybook/test-runner
@vitest/browser
@vitest/browser-playwright
```

## 15. Gate Evidence 2026-04-25

Gate evidence:

- `npm run storybook -- --help` PASS;
- `npm run test -- --run` PASS, 9 tests passed;
- `npm run build` PASS;
- `npm run build-storybook -- --disable-telemetry --loglevel warn` PASS;
- `py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view` PASS, 42 tests passed;
- `git diff --check` PASS;
- focused `claude.cmd --print` review: no blocking findings;
- focused `claude.cmd --print` follow-up after corrected frontend-directory dependency check: NO BLOCKING FINDINGS.

Storybook build emitted the expected tooling-only warning:

```text
No story files found for the specified pattern.
```

This warning is acceptable for S6-SB-B because product stories are explicitly out of scope and are reserved for the next bounded Storybook story ticket.

## 16. Closeout State

Current closeout state:

```text
COMMITTED_PUSHED_1e06550
```

S6-SB-B was committed and pushed in `1e06550 Install Storybook React Vite tooling`.
