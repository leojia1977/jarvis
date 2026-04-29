# S6 Non-Qwen Build-Ready Evidence Queue 2026-04-29

## 1. Document Control

- Date: 2026-04-29
- Record type: next-stage automation queue
- Replaces: completed Jira burn-down runner
- Qwen route: `WAIT_FOR_CLOUD_QWEN_RUNTIME_HANDOFF`
- Related record: `docs/S6_QWEN_HOLD_AND_NON_QWEN_BUILD_READY_QUEUE_2026_04_29.md`

## 2. Queue Decision

```text
NON_QWEN_BUILD_READY_EVIDENCE_QUEUE_OPEN
OLD_JIRA_BURN_DOWN_RUNNER_RETIRED
QWEN_CLOUD_RUNTIME_HANDOFF_REMAINS_HOLD
NO_IMPLEMENTATION_WITHOUT_EXACT_GO
```

This queue exists so automation does not idle after Jira reaches 80 Done / 0 Non-Done. It may perform synthetic-only evidence, docs-only planning, regression evidence review, and maintenance runner preparation. It must not invent product scope.

## 3. Queue Lanes

### Lane 1 — S0 Synthetic Payload Generation

Allowed outputs:

- synthetic CaseView payload design for UAT-01 through UAT-20;
- synthetic `QwenFactBundle` design for UAT-01 through UAT-20;
- prompt-injection variant definitions;
- action-command scan list refinement;
- fixture id / output artifact naming conventions.

Stop before:

- model execution;
- real data;
- masked real data;
- connector or backend changes;
- credentials.

### Lane 2 — Build-Ready Evidence Matrix

Allowed outputs:

- matrix of existing frontend/unit/build/Storybook/Playwright/backend guard evidence;
- explicit distinction between mock-only build-ready, staging-planning-ready, and real-data-shadow-planning-ready;
- missing evidence list;
- recommended canonical gate set.

Stop before:

- build-ready approval;
- staging approval;
- deploy approval;
- production release approval.

### Lane 3 — Frontend Regression Evidence Review

Allowed outputs:

- review of current frontend test coverage;
- map completed S6 tickets to regression assertions;
- identify duplicated, stale, or missing regression evidence;
- propose exact future test tickets that stop at `IMPLEMENTATION_GO_REQUIRED`.

Stop before:

- code edits;
- dependency changes;
- product behavior changes.

### Lane 4 — Storybook / Playwright Canonical Gate Review

Allowed outputs:

- identify canonical Storybook stories for current build-ready evidence;
- identify canonical Playwright specs for current build-ready evidence;
- separate AP / CD / SH / MV / CH route coverage;
- identify missing but non-Qwen regression candidates.

Stop before:

- adding stories;
- adding Playwright specs;
- changing app code.

### Lane 5 — Automation Maintenance Runner Plan

Allowed outputs:

- maintenance runner scope;
- heartbeat prompt;
- idle fallback policy;
- HOLD reporting rules;
- source intake watch rules;
- safe gate schedule.

Stop before:

- creating new recurring automation without explicit tool/action authorization;
- Jira issue mutation;
- deployment.

## 4. Required Queue Outputs

Initial batch should create:

```text
docs/S6_S0_SYNTHETIC_PAYLOAD_GENERATION_CHECKLIST_2026_04_29.md
docs/S6_BUILD_READY_EVIDENCE_MATRIX_2026_04_29.md
docs/S6_FRONTEND_REGRESSION_EVIDENCE_REVIEW_2026_04_29.md
docs/S6_STORYBOOK_PLAYWRIGHT_CANONICAL_GATE_REVIEW_2026_04_29.md
docs/S6_AUTOMATION_MAINTENANCE_RUNNER_PLAN_2026_04_29.md
```

These are docs-only queue outputs unless Jarvis later grants an exact implementation GO.

## 5. HOLD Conditions

Hold immediately if:

- real or masked-real data is requested;
- Qwen cloud runtime execution is requested before handoff;
- credentials would enter repo, Jira, docs, prompts, fixtures, or logs;
- backend/runtime/API/schema is needed;
- connector changes are needed;
- code changes are required;
- product scope expands;
- build-ready / staging / deploy / pilot approval is implied rather than explicitly authorized.

## 6. Non-Authorization

This queue does not authorize:

```text
real data
masked real data
closed shadow
customer-visible output
production write-back
autonomous action
backend/runtime/API/schema
connector changes
secrets
deploy
external pilot
launch
new implementation without exact GO
Jira mutation
```

## 7. Final Route

```text
NEXT_ROUTE: RUN_NON_QWEN_BUILD_READY_EVIDENCE_QUEUE
QWEN_ROUTE: WAIT_FOR_CLOUD_QWEN_RUNTIME_HANDOFF
```
