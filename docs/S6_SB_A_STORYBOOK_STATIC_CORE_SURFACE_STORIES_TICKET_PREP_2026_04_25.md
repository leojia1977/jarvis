# S6-SB-A Storybook Static Core Surface Stories Ticket Prep 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6-SB-A Storybook Static Core Surface Stories Ticket Prep 2026-04-25 |
| Ticket | `S6-SB-A` |
| Scope | Storybook tooling and static core-surface stories readiness |
| Status | NEEDS_DEPENDENCY_INSTALL_DECISION |
| Date | 2026-04-25 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `a8b08ef` |
| Prior fixture ticket | `docs\S6_MF_A_CORE_SURFACE_MOCK_FIXTURE_INTEGRATION_TICKET_PREP_2026_04_25.md` |
| Storybook plan | `D:\产品设计\secupilot0421\incoming_pending\SecuPilot_Storybook_Cross_Surface_Stories_v0.1.md` |
| Fixture | `frontend\fixtures\secupilot_core_surface_fixture_v0_1.json` |
| Lane | Green docs-only tooling decision prep |
| Execution surface | `codex` |
| Review surface | `claude-cmd` focused review if later dependency/tooling diff exists |

This record prepares the Storybook static core-surface stories route after S6-MF-A.

It does not authorize dependency installation, package-lock changes, Storybook generated files, code/test changes, backend/API/schema changes, Playwright setup, P1 to P2 AR propagation, P2 to P3 audit propagation, cross-surface route handoff, launch, deploy, public endpoint work, real-data handling, credential handling, external pilot execution, staging, commit, or push by itself.

## 2. Governing Product Sources

Use this authority order:

1. `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版 (2).md`
2. `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2 (1).md`
3. `SecuPilot_Core_Surface_Logic_Collision_Walkthrough_v0.2.md`
4. `SecuPilot_Core_Surface_Mock_Fixture_Integration_v0.1.md`
5. `secupilot_core_surface_fixture_v0.1.json`
6. `SecuPilot_Storybook_Cross_Surface_Stories_v0.1.md`
7. P1/P2/P3 Model Contracts
8. Storybook official React Vite install documentation as tooling reference only

Binding team instruction:

```text
HTML is visual and interaction prototype. Model Contract, PRD, Walkthrough v0.2, fixture, and Playwright plan are the implementation basis. All implementation must remain mock-only / bounded implementation, with no real data, no launch, and no deploy.
```

## 3. Current Frontend Tooling State

Current frontend stack:

- `vite`
- `react`
- `typescript`
- `vitest`
- `@testing-library/react`

Current frontend has no Storybook dependency, script, `.storybook` config, or story files.

Storybook official docs for React with Vite state:

- existing React projects can install Storybook with `npm create storybook@latest`;
- React Vite support requires React and Vite;
- normal runtime commands after installation are `npm run storybook` and `npm run build-storybook`;
- Storybook installation may add dependencies, scripts, configuration, and boilerplate stories.

Official references:

- `https://storybook.js.org/docs/get-started/frameworks/react-vite`
- `https://storybook.js.org/docs/get-started/install`

## 4. Story Scope Target

Planned Storybook story groups from `SecuPilot_Storybook_Cross_Surface_Stories_v0.1.md`:

| Group | Stories |
| --- | --- |
| P1 Case Detail | Initial investigation, submit modal, waiting on P2, evidence Auto/Manual/Pin |
| P2 Approval Surface | Pending review, strong confirm, approve window disabled, delay/observe window required, reject reason required, observation active, expired, terminal lock, concurrency collision |
| P3 Manager View | Readonly review, approval audit summary, honesty tone preserved, host raw evidence DOM absent, audit unavailable |
| Walkthrough | Phase 0-6 core-surface logic collision |
| Negative Guards | LC-N red-line stories |

S6-SB-A must not implement P2 or P3 product pages. If Storybook stories for P2/P3 are created before full pages exist, they must use static mock-only story shells or placeholders that clearly do not claim product implementation completion.

## 5. Dependency Decision

Current decision:

```text
DO_NOT_INSTALL_STORYBOOK_YET
```

Reason:

- dependency install changes `frontend/package.json` and `frontend/package-lock.json`;
- Storybook CLI may generate `.storybook` config and boilerplate stories;
- generated files and dependency versions should be reviewed as a separate tooling implementation ticket;
- Playwright remains separate and later.

Recommended next decision:

```text
Authorize S6-SB-B Storybook React Vite Dependency Setup
```

Recommended installation approach after explicit authorization:

```powershell
cd frontend
npm create storybook@latest
```

During that future ticket, select the minimal React + Vite setup and remove or replace generic boilerplate stories before closeout.

## 6. Exact Future Ticket Split

| Ticket | Lane | Purpose | Dependency changes |
| --- | --- | --- | --- |
| `S6-SB-A` | Green docs-only | Tooling decision and static story scope prep | No |
| `S6-SB-B` | Yellow tooling | Install/configure Storybook React Vite | Yes, after explicit authorization |
| `S6-SB-C` | Yellow frontend | P1 static stories from fixture phases | No new deps after S6-SB-B |
| `S6-SB-D` | Yellow frontend | P2/P3 static mock story shells | No new deps after S6-SB-B |
| `S6-SB-E` | Yellow frontend | Walkthrough/CoreSurfaceLogicCollision story | No new deps after S6-SB-B |
| `S6-PW-A` | Later tooling | Playwright E2E setup and LC-P/LC-B/LC-N plan | Separate decision |

## 7. Proposed S6-SB-B Exact Scope

If authorized, S6-SB-B should be limited to Storybook installation and minimal config.

Allowed files for S6-SB-B should be:

- `docs/S6_SB_B_STORYBOOK_REACT_VITE_TOOLING_SETUP_TICKET_PREP_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/.storybook/main.ts`
- `frontend/.storybook/preview.ts`
- generated sample story files only if they are immediately removed or replaced with governed placeholders in the same ticket

Required commands for S6-SB-B should be:

```powershell
cd frontend
npm run test -- --run
npm run build
npm run storybook -- --help
npm run build-storybook
```

Backend guard should remain:

```powershell
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
```

## 8. Proposed Story Acceptance After Tooling

After Storybook tooling exists, static story implementation tickets must preserve:

- all stories use `frontend\fixtures\secupilot_core_surface_fixture_v0_1.json`;
- role, coverage, case_state, AR status, and surface context are fixture-derived;
- no URL/localStorage/sessionStorage authority;
- no real data or real telemetry;
- no backend calls;
- no static HTML prototype copy;
- no P1 ActionMode exposure;
- no P3 host-level raw evidence DOM;
- no Playwright setup inside Storybook tickets.

## 9. Exact Non-Goals

S6-SB-A must not implement:

- dependency installation;
- `package.json` or `package-lock.json` changes;
- `.storybook` config;
- story files;
- Playwright setup;
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

## 10. HOLD Conditions

HOLD if:

- Storybook install is attempted before explicit dependency authorization;
- package files change in S6-SB-A;
- Storybook generated boilerplate is committed without review;
- stories require product surfaces that do not exist and pretend they are implemented;
- implementation pulls from static HTML as source code;
- real data, credentials, network calls, launch, deploy, public endpoint, or external pilot behavior appears;
- Playwright setup is mixed into Storybook setup;
- a broad frontend platform abstraction or component registry appears before exact stories require it.

## 11. Decision

Decision:

```text
NEEDS_DEPENDENCY_INSTALL_DECISION
```

Recommended next route:

```text
OPEN_S6_SB_B_STORYBOOK_REACT_VITE_TOOLING_SETUP
```

Required human/Jarvis decision before implementation:

```text
Authorize or reject Storybook dependency installation in frontend.
```
