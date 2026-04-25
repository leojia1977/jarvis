# S6 E0-03 Storybook First Story Set Launch Checklist 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 E0-03 Storybook First Story Set Launch Checklist 2026-04-25 |
| Ticket | `E0-03` |
| Status | READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO |
| Date | 2026-04-25 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `786b579` |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | conditional |
| SWE | disabled |

This checklist launches Sprint 0 `E0-03` only.

## 2. Jarvis Authorization

Jarvis authorized a 48h bounded automation queue:

```text
E0-03-LAUNCH -> E0-03-IMPLEMENT -> E0-04-LAUNCH -> E0-04-IMPLEMENT
```

Authorization includes required gate, Claude Code focused review, Jira cloud sync, and stage/commit/push for each PASS ticket.

HOLD remains mandatory for scope expansion, missing exact allowed files, dependency ambiguity, failed tests/build, Claude Web mandatory trigger, backend/runtime/API/schema need, real data/secrets/deploy/external pilot, or any non-ready ticket.

## 3. Source Authority

Current governed source-of-truth:

- `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版.md`
- `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2.1.md`
- `SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx`
- `SecuPilot_Frontend_Sprint_0_Execution_Checklist_and_PR_Review_Gate_v0.2.md`
- `SecuPilot_Storybook_Cross_Surface_Stories_v0.1.md`
- `SecuPilot_Core_Surface_Mock_Fixture_Integration_v0.1.md`
- `SecuPilot_Core_Surface_Logic_Collision_Walkthrough_v0.2.md`
- `docs/S6_E0_01_RESOLVED_SURFACE_CONTEXT_TICKET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_02_CORE_SURFACE_MOCK_FIXTURE_ADAPTER_LAUNCH_CHECKLIST_2026_04_25.md`

Repo baseline:

```text
E0-01 closed in commit aaaa199.
E0-02 closed in commit 786b579.
Storybook dependencies and .storybook config already exist.
```

## 4. Launch Verdict

Decision:

```text
GO_FOR_STATIC_FIRST_STORY_SET_ONLY
```

Interpretation:

- E0-03 may create the first Storybook stories that render the existing mock-only workbench from validated fixture phases.
- E0-03 may add a minimal `initialPhaseNumber` story hook to `App` so stories can render Phase 0-6 without URL/storage authority.
- E0-03 may add Storybook build verification.

Blocked within E0-03:

- no P2 strong-confirm composer implementation;
- no P2 delay/observe/reject interactive workflow implementation;
- no CS-P2-05 stale approve/concurrency implementation;
- no Playwright E2E;
- no P1/P2/P3 new page implementation beyond the existing workbench story frame;
- no P3 contract ratification claims;
- no backend/runtime/API/schema, real data, secrets, deploy, or external pilot.

## 5. Exact Allowed Files

Allowed files:

- `docs/S6_E0_03_STORYBOOK_FIRST_STORY_SET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/.storybook/preview.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/secupilot/surface/storybook/CoreSurfaceStories.stories.tsx`

Read-only references:

- `frontend/src/secupilot/surface/fixtures/coreSurfaceFixtureAdapter.ts`
- `frontend/fixtures/secupilot_core_surface_fixture_v0_1.json`
- `frontend/src/secupilot/surface/context/types.ts`
- `frontend/src/secupilot/surface/context/validateResolvedSurfaceContext.ts`
- `frontend/src/secupilot/surface/components/SecurityHalt.tsx`
- `frontend/package.json`
- `frontend/.storybook/main.ts`

No other file may be changed unless a HOLD is triggered and the later automation queue has explicit safe scope.

## 6. Exact Scope

Implement only:

1. Storybook stories for safe static fixture phases:
   - P1 initial investigation, Phase 0;
   - P1 waiting on P2, Phase 1;
   - P2 pending approval, Phase 2;
   - P2 observation window active, Phase 3;
   - P2 window expired back to pending, Phase 4;
   - P2 terminal lock / approved pending execution, Phase 5;
   - P3 manager read-only review, Phase 6;
   - a cross-surface Phase 0-6 overview driven by adapter metadata.
2. Minimal app story hook to set the initial fixture phase.
3. Storybook CSS loading only if needed by `.storybook/preview.ts`.
4. Focused tests proving initial story phase rendering and existing guardrails remain intact.

## 7. Non-Goals

This ticket must not implement:

- new product behavior;
- static HTML prototype copy/paste;
- P2 decision composer, strong confirm modal, delay/observe/reject forms, or stale approve collision;
- P3 new manager component or P3 ratification;
- Playwright tests or Playwright dependency/configuration;
- backend/runtime/API/schema changes;
- route handoff or cross-surface propagation;
- real data, sanitized real data, customer data, credentials, tokens, secrets, launch, deploy, public endpoint, or external pilot;
- broad component registry, data layer, global store, service framework, or cleanup refactor.

## 8. Required Semantics

Required:

- stories must use `App` and/or E0-02 adapter outputs;
- role, surface, coverage level, case state, AR status, and action mode must come from validated `ResolvedSurfaceContext`;
- URL/localStorage/sessionStorage must not become authority sources;
- P1 stories must not expose `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY`;
- P3 story must keep host-level raw evidence DOM absent;
- story labels may reference fixture phase and story IDs, but stories must not claim production readiness.

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

Claude Web/external review is conditional and required only if implementation changes product semantics, authority semantics, validator strictness, backend/runtime/API/schema, P2/P3 ratification scope, real-data behavior, route handoff, cross-surface propagation, or Go/No-Go mandatory trigger categories.

## 10. HOLD Conditions

HOLD immediately if:

- implementation needs files outside the allowed list;
- Storybook cannot build without dependency changes;
- implementation needs new page components beyond the static story frame;
- implementation needs P2/P3 interaction behavior not already present in current App;
- implementation needs Playwright, backend/runtime/API/schema, route handoff, or cross-surface propagation;
- URL/localStorage/sessionStorage is used as role, coverage, state, AR status, action mode, or surface authority;
- P3 raw host evidence enters DOM;
- tests/build/storybook build fail;
- Claude Code review returns blocking findings;
- Claude Web mandatory trigger fires.

## 11. Rollback

Rollback condition:

```text
Revert E0-03 storybook/app/test/checklist/route/handoff changes if Storybook build fails, frontend tests/build fail, backend guard fails, review finds blocking issues, scope expands outside allowed files, or HOLD triggers fire.
```

## 12. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- execution surface is `codex`;
- scope is small and Storybook/static-fixture oriented;
- no separate SWE exact sub-ticket has been created.

## 13. Implementation Decision

Decision:

```text
READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO
```

Authorized next action:

```text
Implement E0-03 static first Storybook story set inside the exact allowed file scope.
```
