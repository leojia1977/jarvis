# S6 E0-03B Storybook Negative Boundary Stories Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 E0-03B Storybook Negative Boundary Stories Launch Checklist 2026-04-27 |
| Ticket | `E0-03B` |
| Status | READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO_WITH_BOUNDS |
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

This checklist launches the exact follow-up ticket `E0-03B` only.

## 2. Purpose

`E0-03B` is a Storybook-only follow-up to the completed `E0-03` first story set and completed `E0-02B` fixture QA expansion.

The goal is to expose the already-governed fixture registry in Storybook so design, QA, and governance reviewers can inspect negative, boundary, and resolver-degradation states before page or E2E work expands.

## 3. Source Authority

Current governed source-of-truth:

- `docs/S6_E0_01_RESOLVED_SURFACE_CONTEXT_TICKET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_02_CORE_SURFACE_MOCK_FIXTURE_ADAPTER_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_02B_FIXTURE_QA_EXPANSION_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_E0_03_STORYBOOK_FIRST_STORY_SET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_E0_04_PLAYWRIGHT_LCP_LCB_LCN_SEED_LAUNCH_CHECKLIST_2026_04_25.md`
- `D:\产品设计\secupilot0421\visual negative\SecuPilot_Automation_Team_Handoff_and_E0-02_Launch_Pack_v0.1.md`
- `D:\产品设计\secupilot0421\visual negative\SecuPilot_E0-01_Closeout_Record_v0.1.md`
- `D:\产品设计\secupilot0421\visual negative\SecuPilot_Visual_Negative_Frames_Brief_v0.1.md`
- `D:\产品设计\secupilot0421\visual negative\SecuPilot_Automation_Team_E0-02_Launch_Pack_v0.1.1.zip`

Authority notes:

- `AI_COLLAB Amendment v0.2` governs execution surface, reviewer floor, single-writer lock, and SWE HOLD-on-expansion behavior throughout Sprint 0.
- HTML prototypes remain visual and interaction reference only; Model Contract, PRD, Walkthrough, fixture registry, and Playwright plans remain implementation authority.
- E0-03B must not reopen E0-03 or E0-04; it is a narrow follow-up.

## 4. Launch Verdict

Decision:

```text
GO_FOR_STORYBOOK_REGISTRY_NEGATIVE_BOUNDARY_STORIES_ONLY
```

Interpretation:

- E0-03B may add Storybook stories that summarize and display existing validated `phase`, `boundary_case`, and `resolver_degradation` fixture registry entries.
- E0-03B may add Storybook documentation cards for `poison_pill` fixture IDs as non-renderable fail-closed cases.
- E0-03B must use the existing fixture registry and adapter as input; it must not create new product states.
- E0-03B must not render invalid poison-pill contexts, must not use `validate=false`, and must not loosen `ContextValidator`.

## 5. Exact Allowed Files

Allowed files:

- `docs/S6_E0_03B_STORYBOOK_NEGATIVE_BOUNDARY_STORIES_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/src/secupilot/surface/storybook/CoreSurfaceStories.stories.tsx`

Read-only references:

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/secupilot/surface/fixtures/coreSurfaceFixtureAdapter.ts`
- `frontend/src/secupilot/surface/fixtures/fixtureRegistry.ts`
- `frontend/src/secupilot/surface/fixtures/mockFixtureAdapter.ts`
- `frontend/src/secupilot/surface/fixtures/fixtureTypes.ts`
- `frontend/src/secupilot/surface/fixtures/README.md`
- `frontend/src/secupilot/surface/context/types.ts`
- `frontend/src/secupilot/surface/context/validateResolvedSurfaceContext.ts`
- `frontend/src/secupilot/surface/components/SecurityHalt.tsx`
- `frontend/.storybook/main.ts`
- `frontend/.storybook/preview.ts`
- `frontend/package.json`

No other file may be changed unless a HOLD is triggered and a new exact ticket is created.

## 6. Exact Scope

Implement only:

1. Storybook sections for already-existing validated fixture groups:
   - phase registry, including Phase 07 `CROSS_SURFACE` as fixture-only walkthrough metadata;
   - boundary cases:
     - `boundary-p3-audit-summary-unavailable`;
     - `boundary-p2-cmdb-tags-unavailable`;
     - `boundary-dirty-update-during-observation-window`;
     - `boundary-concurrency-stale-approve-rejected`;
   - resolver degradation:
     - `resolver-l1-blast-radius-payload`;
     - `resolver-l1-lineage-confidence-degraded`;
     - `resolver-p3-technical-detail-redaction`;
     - `resolver-search-history-current-lower-than-recorded`;
     - `resolver-search-history-current-higher-than-recorded`.
2. A poison-pill inventory story that lists fail-closed fixture IDs without rendering their invalid contexts.
3. Story text that clearly labels these as mock-only, fixture-only, and non-production stories.

## 7. Non-Goals

This ticket must not implement:

- App, page, component, layout, route, or product workflow changes;
- new fixtures or fixture registry entries;
- `validate=false` usage in Storybook;
- poison-pill context rendering;
- P1/P2/P3 page stitching;
- P2 strong-confirm, decision composer, stale approve, or concurrency behavior;
- P3 contract ratification or new manager summary component;
- Playwright tests;
- backend/runtime/API/schema;
- real data, anonymized real data, credentials, tokens, secrets, deploy, public endpoint, or external pilot;
- broad story framework, global store, renderer abstraction, or reusable platform layer.

## 8. Required Semantics

Required:

- all renderable fixture data must come from `mockFixtureAdapter` or the existing registry path with validation enabled;
- `validate=true` remains default and mandatory for Storybook;
- `validate=false` must not be accepted or forwarded by any Storybook helper;
- poison-pill fixtures may be listed as fail-closed documentation only;
- Storybook must not treat URL, localStorage, sessionStorage, Storybook args, or route params as role, coverage, surface, case state, AR status, or action mode authority;
- boundary stories must preserve the meaning that missing signals degrade honestly rather than unlocking hidden fields;
- P3-related stories must keep raw host evidence non-renderable and must avoid over-certain summary language.

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
- implementation needs App, component, page, route, fixture registry, adapter, validator, Playwright, backend/runtime/API/schema, or dependency changes;
- Storybook cannot represent the negative/boundary material without rendering invalid contexts;
- Storybook needs `validate=false`;
- any poison-pill fixture is rendered as if it were a valid context;
- URL/localStorage/sessionStorage/Storybook args become authority sources;
- P3 raw host evidence enters DOM;
- tests/build/storybook build fail;
- Claude Code review returns blocking findings;
- Claude Web mandatory trigger fires.

## 11. Rollback

Rollback condition:

```text
Revert E0-03B story/checklist/route/handoff changes if Storybook build fails, frontend tests/build fail, backend guard fails, review finds blocking issues, scope expands outside allowed files, or HOLD triggers fire.
```

## 12. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- execution surface is `codex`;
- scope is one Storybook file plus docs records;
- no separate SWE exact sub-ticket has been created.

## 13. Implementation Decision

Decision:

```text
READY_FOR_AUTONOMOUS_IMPLEMENTATION_GO_WITH_BOUNDS
```

Authorized implementation boundary:

```text
Implement E0-03B only if changes remain limited to the Storybook registry-negative/boundary stories in `CoreSurfaceStories.stories.tsx` plus closeout records.
```

Any need to change `App`, components, fixture registry, fixture adapter, validator, Playwright specs, dependencies, or backend/runtime/API/schema converts this ticket to HOLD.
