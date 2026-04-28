# S6 30m Runner Idle Fallback 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 30m Runner Idle Fallback 2026-04-28 |
| Status | ACTIVE_IDLE_FALLBACK_AUTHORIZED |
| Date | 2026-04-28 |
| Automation | `secupilot-30m-bounded-burn-runner` |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |

This record defines the safe idle fallback for the active bounded burn runner.

It exists so the runner does not silently stop after completing a short exact ticket queue, while still preserving the governed no-scope-invention boundary.

## 2. Entry Condition

The runner may enter idle fallback only when all currently authorized exact ticket actions are exhausted, blocked, or unsafe to start.

Before entering fallback, the runner must confirm:

- `git status --short --branch` is clean or only contains files created by the current heartbeat;
- no implementation ticket has exact `GO` remaining in the active queue;
- no checklist can safely prove exact files/tests without additional source evidence;
- no mandatory external review trigger is open and unhandled;
- no HOLD condition is being bypassed.

Idle fallback is not a replacement for implementation GO.

## 3. Allowed Idle Fallback Actions

The runner may perform one safe fallback action per heartbeat, in this priority order:

| Priority | Action | Allowed output |
| ---: | --- | --- |
| 1 | Progress / Risk Board refresh | Update counts, move already evidenced tickets, record blockers. |
| 2 | Jira parity audit for already PASS or no-code reconciled tickets | Notes only, or safe status sync when repo evidence already proves Done. |
| 3 | Next exact checklist preparation | Draft a checklist for a named ticket only if source evidence and non-goals are exact. |
| 4 | Blocker / authority pack refresh | Clarify HOLD reason, missing source evidence, design dependency, or external review need. |
| 5 | Design-frame request refresh | Update existing frame request ordering without inventing product scope. |
| 6 | Idle report | Record that no safe code/docs action exists and list the first blocker. |

## 4. Forbidden Idle Fallback Actions

The runner must not use idle fallback to:

- create new product requirements;
- infer missing P2/P3 authority behavior;
- implement code without exact ticket GO;
- change frontend/backend/fixture/script/config/dependency files unless a separate exact implementation ticket authorizes it;
- change backend/runtime/API/schema;
- change fixture registry, fixture adapter, `ContextValidator`, or `ResolvedSurfaceContext`;
- mark HOLD, visual-missing, authority-missing, blocked, or non-ready Jira tickets Done;
- convert visual PASS into launch, deploy, real-data, or external-pilot authorization;
- create broad reusable abstractions, helper layers, frameworks, registries, or platform work.

## 5. Allowed Files During Idle Fallback

Unless a named checklist gives a narrower allowed file list, idle fallback is docs-only and may update only:

```text
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
docs/S6_*CHECKLIST*.md
docs/S6_*RECONCILIATION*.md
docs/S6_*AUTHORITY*.md
docs/S6_*BLOCKER*.md
docs/S6_*JIRA*.md
docs/S6_*RUNNER*.md
```

If the required update falls outside these files, the runner must HOLD.

## 6. Gate

For every idle fallback docs-only batch:

```text
git diff --check
```

If a fallback action changes Jira only, the runner must still record the intended repo-side note in a governed doc or HOLD if no allowed doc exists.

## 7. Commit / Push Rule

Idle fallback may stage, commit, and push only when:

- the fallback output is PASS docs-only evidence;
- `git diff --check` passes except Windows line-ending warnings already tolerated by the repo;
- no HOLD condition exists;
- the heartbeat or Jarvis authorization explicitly allows docs-only stage/commit/push.

## 8. Exit Condition

Idle fallback ends immediately when a new exact bounded ticket GO appears.

Next implementation queue then resumes from the current runner authorization, not from the fallback action.

## 9. Decision

```text
IDLE_FALLBACK_ACTIVE_FOR_30M_BOUNDED_BURN_RUNNER
```

Next route:

```text
CONTINUE_EXTENDED_QUEUE_WITH_IDLE_FALLBACK_AFTER_AP_T08_CLOSEOUT
```
