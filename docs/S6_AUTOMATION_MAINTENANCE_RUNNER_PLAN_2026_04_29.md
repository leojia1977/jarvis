# S6 Automation Maintenance Runner Plan 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Docs-only automation maintenance plan |
| Date | 2026-04-29 |
| Queue | `docs/S6_NON_QWEN_BUILD_READY_EVIDENCE_QUEUE_2026_04_29.md` |
| Replaces | Completed Jira burn-down runner |

## 2. Decision

```text
AUTOMATION_MAINTENANCE_RUNNER_PLAN_CREATED
OLD_JIRA_BURN_DOWN_RUNNER_RETIRED
NON_QWEN_DOCS_ONLY_RUNNER_ACTIVE
QWEN_CLOUD_RUNTIME_HANDOFF_STILL_HOLD
```

This plan keeps automation productive without inventing product scope after Jira reaches 80 Done / 0 Non-Done.

## 3. Runner Purpose

The runner may perform:

- docs-only evidence refresh;
- synthetic payload planning;
- build-ready evidence matrix updates;
- frontend regression evidence review;
- Storybook/Playwright gate review;
- HOLD map updates;
- route/handoff/progress board updates;
- idle reports that explain what would unlock the next safe action.

The runner must stop before:

- code changes;
- Storybook/Playwright edits;
- Qwen execution;
- real or masked-real data;
- backend/runtime/API/schema;
- connector changes;
- credential handling in repo;
- Jira mutation without exact authorization;
- deploy, external pilot, or launch.

## 4. Maintenance Heartbeat

```xml
<heartbeat>
  <automation_id>secupilot-non-qwen-build-ready-evidence-runner</automation_id>
  <instructions>
Continue from D:\产品设计\New folder on branch codex/s3-a-runtime.
First read docs/HANDOFF.md, docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md,
docs/S6_QWEN_HOLD_AND_NON_QWEN_BUILD_READY_QUEUE_2026_04_29.md,
docs/S6_S0_UAT_SYNTHETIC_FIXTURE_MANIFEST_2026_04_29.md,
docs/S6_S0_QWEN_CLOUD_RUNTIME_PRECHECK_2026_04_29.md,
docs/S6_NON_QWEN_BUILD_READY_EVIDENCE_QUEUE_2026_04_29.md,
docs/S6_S0_SYNTHETIC_PAYLOAD_GENERATION_CHECKLIST_2026_04_29.md,
docs/S6_BUILD_READY_EVIDENCE_MATRIX_2026_04_29.md,
docs/S6_FRONTEND_REGRESSION_EVIDENCE_REVIEW_2026_04_29.md,
docs/S6_STORYBOOK_PLAYWRIGHT_CANONICAL_GATE_REVIEW_2026_04_29.md,
and docs/S6_AUTOMATION_MAINTENANCE_RUNNER_PLAN_2026_04_29.md.
Verify git status before work.

Qwen cloud runtime handoff remains HOLD. Do not run Qwen, import model output,
use real/masked-real data, touch secrets, mutate backend/runtime/API/schema,
change connectors, deploy, launch, or create customer-visible output.

Allowed docs-only work:
1. Refresh S0 synthetic payload planning.
2. Refresh build-ready evidence matrix.
3. Refresh frontend regression evidence review.
4. Refresh Storybook/Playwright canonical gate review.
5. Refresh HOLD map and idle report.
6. Prepare exact future checklist drafts that stop at IMPLEMENTATION_GO_REQUIRED.

For PASS docs-only outputs, run git diff --check and py -3 scripts/git_preflight.py --mode pilot.
Revert generated releases/release_manifest.json changes unless explicitly authorized.
Stage/commit/push only when Jarvis explicitly authorizes that batch.
  </instructions>
</heartbeat>
```

## 5. Idle Fallback Policy

If no exact lane is safe:

1. Refresh the HOLD map.
2. Refresh the build-ready evidence matrix.
3. Write an idle report naming the missing source or authorization.
4. Prepare a copy-ready authorization prompt for the next safe docs-only batch.
5. Do not create scope, code, Jira changes, or launch decisions.

## 6. HOLD Reporting Rules

Every HOLD report must name:

- missing input;
- owner surface;
- whether Jarvis/Human action is needed;
- whether Qwen cloud runtime handoff is needed;
- whether a governed source document is needed;
- whether implementation GO is needed;
- exact forbidden action that caused the HOLD.

## 7. Source Intake Watch Rules

Watch for incoming source packages only as input material until repo intake imports them.

Allowed intake steps:

- list package names;
- compute file presence/readability;
- summarize source claims;
- create docs-only intake records.

Forbidden intake steps:

- treat loose files or zips as runnable truth;
- copy credentials into repo;
- import real or masked-real data;
- mutate connectors;
- run Qwen without handoff;
- launch or deploy.

## 8. Safe Gate Schedule

Suggested non-code queue closeout gate:

```text
git diff --check
py -3 scripts/git_preflight.py --mode pilot
```

Suggested future build-ready evidence gate, only when explicitly authorized:

```text
cd frontend && npm test -- --run
cd frontend && npm run build
cd frontend && npm run build-storybook -- --disable-telemetry --loglevel warn
cd frontend && npm run test:e2e
py -3 scripts/git_preflight.py --mode pilot
git diff --check
```

## 9. Multi-Batch Authorization Template

Jarvis may use this to keep the runner from idling:

```text
Authorize non-Qwen build-ready evidence runner batch:
1. Refresh S0 synthetic payload checklist.
2. Refresh build-ready evidence matrix.
3. Refresh frontend regression evidence review.
4. Refresh Storybook/Playwright canonical gate review.
5. Refresh automation maintenance/HOLD report.
6. Prepare exact future checklist drafts, stopping at IMPLEMENTATION_GO_REQUIRED.

Docs-only.
No code, no Storybook/Playwright edits, no Qwen execution, no real/masked-real data,
no backend/runtime/API/schema, no connector changes, no secrets, no Jira mutation,
no deploy, no external pilot, no launch.

PASS docs-only outputs may run git diff --check and pilot preflight.
Stage/commit/push authorized only for this docs-only batch if gates pass.
```

## 10. Next Route

```text
RUN_NON_QWEN_MAINTENANCE_RUNNER_OR_WAIT_FOR_CLOUD_QWEN_RUNTIME_HANDOFF
```

