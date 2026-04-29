# S6 Storybook / Playwright Canonical Gate Review 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Docs-only Storybook / Playwright canonical gate review |
| Date | 2026-04-29 |
| Queue | `docs/S6_NON_QWEN_BUILD_READY_EVIDENCE_QUEUE_2026_04_29.md` |
| Code changes | Not authorized |

## 2. Decision

```text
STORYBOOK_PLAYWRIGHT_CANONICAL_GATE_REVIEW_CREATED
CURRENT_STORY_AND_E2E_SURFACES_INDEXED
NO_STORY_OR_TEST_CHANGE_AUTHORIZED
```

## 3. Canonical Storybook Stories

Current story file:

```text
frontend/src/secupilot/surface/storybook/CoreSurfaceStories.stories.tsx
```

Canonical stories for current mock-only build-ready evidence:

| Story | Evidence purpose |
| --- | --- |
| `P1InitialInvestigation` | P1 Case Detail initial investigation. |
| `P1WaitingOnP2` | P1 waiting-on-P2 state. |
| `P2PendingReview` | P2 pending approval shell. |
| `P2ObservationWindowActive` | Observation-window readonly state. |
| `P2WindowExpiredReturnPending` | Mock return to pending state. |
| `P2TerminalLock` | Approved-pending terminal lock. |
| `APT12CPendingReviewRoute` | AP-T12C P2 `/approval` acceptance route. |
| `APT12CObservationWindowRoute` | AP-T12C observation-window route. |
| `APT12CWindowExpiredRoute` | AP-T12C expired route. |
| `APT12CTerminalLockRoute` | AP-T12C terminal lock route. |
| `P3ReadonlyReview` | P3 Manager readonly review. |
| `CrossSurfacePhaseOverview` | Phase 0-6 walkthrough overview. |
| `FixtureRegistryValidatedPhases` | Validated phase fixture inventory. |
| `FixtureRegistryBoundaryCases` | Boundary fixture inventory. |
| `FixtureRegistryResolverDegradation` | Resolver degradation fixture inventory. |
| `FixtureRegistryPoisonPillInventory` | Fail-closed poison-pill inventory, not renderable as app context. |
| `FixtureRegistryNegativeBoundaryOverview` | Combined negative and boundary fixture overview. |

Canonical Storybook command:

```text
cd frontend && npm run build-storybook -- --disable-telemetry --loglevel warn
```

## 4. Canonical Playwright Specs

| Spec | Current tests | Evidence purpose |
| --- | --- | --- |
| `frontend/tests/e2e/core-surface.logic-collision.spec.ts` | LC-P phase seed path | P1/P2/terminal/P3 phases resolve from fixture context only. |
| `frontend/tests/e2e/core-surface.permission-guards.spec.ts` | Permission guards | URL/storage injection rejected; P1 ActionMode absent; invalid deep links do not expose approval operations. |
| `frontend/tests/e2e/core-surface.p3-dom-isolation.spec.ts` | P3 DOM isolation | Host raw evidence and approval controls absent for P3. |
| `frontend/tests/e2e/core-surface.redline-expansion.spec.ts` | Redline expansion | Missing-signal `ui_messages`, stale approve warning, L1 resolver degradation, cautious P3 summary, poison-pill app exclusion. |
| `frontend/tests/e2e/approval.acceptance.spec.ts` | AP-T12C acceptance lane | Source-bound P2 approval shell, mock `STATE_SYNC`, URL/storage authority rejection. |

Canonical Playwright command:

```text
cd frontend && npm run test:e2e
```

## 5. Route Coverage

| Route / surface | Storybook coverage | Playwright coverage | Status |
| --- | --- | --- | --- |
| P1 Case Detail | Phase stories | LC-P and permission specs | Covered for mock-only build-ready evidence. |
| P2 Approval | Phase stories plus AP-T12C route stories | AP acceptance spec and permission guards | Covered for current bounded AP acceptance. |
| P3 Manager | P3 readonly story | P3 DOM isolation and redline spec | Covered for P3-only scope. |
| Search / History | Indirect story coverage through fixture registry | Redline and permission specs | Covered for current guardrail evidence. |
| Coverage & Health | No dedicated canonical story in current story file | Component/unit evidence exists; Playwright route evidence is indirect | Candidate for future story/test expansion, but code changes require exact GO. |
| S0 Qwen evaluation | Not applicable | Not applicable | HOLD until cloud Qwen handoff and output artifacts exist. |

## 6. Canonical Gate Bundle

For a build-ready evidence refresh, Storybook/Playwright should be reported with:

```text
cd frontend && npm run build-storybook -- --disable-telemetry --loglevel warn
cd frontend && npm run test:e2e
```

Capture:

- command;
- timestamp;
- commit hash;
- pass/fail;
- failure screenshots or traces if applicable;
- exact Storybook story list;
- exact Playwright spec list;
- environment note stating mock-only / synthetic-only.

## 7. HOLD Conditions

HOLD if the gate refresh requires:

- new Storybook stories;
- new Playwright specs;
- app code changes;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema;
- Qwen model execution;
- real or masked-real data;
- deployment, external pilot, or launch.

## 8. Non-Authorization

This record does not authorize:

```text
storybook edits
playwright edits
app code edits
dependency changes
Qwen execution
real data
masked real data
backend/runtime/API/schema
deploy
external pilot
launch
```

## 9. Next Route

```text
OPEN_CANONICAL_STORYBOOK_PLAYWRIGHT_GATE_RUN_OR_STOP_AT_IMPLEMENTATION_GO_REQUIRED
```

