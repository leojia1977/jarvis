# S6 CH-T02 / CH-T04 Design Runtime Blocker Refresh 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Tickets | `CH-T02` / `CH-T04` |
| Title | Coverage & Health design/runtime blocker refresh |
| Status | `CH_T02_CH_T04_HOLD_CONFIRMED` |
| Date | 2026-04-29 |
| Automation | `secupilot-30m-bounded-burn-runner` |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Prior evidence | `docs\S6_CH_T01_COVERAGE_HEALTH_PAGE_SKELETON_CLOSEOUT_2026_04_27.md` |
| Prior evidence | `docs\S6_CH_T03_UI_MESSAGES_RENDERING_IMPLEMENTATION_CLOSEOUT_2026_04_28.md` |

This refresh rechecks whether `CH-T02` or `CH-T04` can safely reopen under the
extended bounded automation queue.

It is docs-only and does not authorize implementation.

## 2. Decision

```text
CH_T02_HOLD_CONFIRMED_PENDING_VF01_VISUAL_BASELINE
CH_T04_HOLD_CONFIRMED_PENDING_CH_T02_AND_RUNTIME_SCOPE_DECISION
```

Both tickets remain HOLD.

## 3. Evidence Checked

| Evidence | Result |
| --- | --- |
| `docs\S6_CH_T01_COVERAGE_HEALTH_PAGE_SKELETON_CLOSEOUT_2026_04_27.md` | `CH-T01` closed a semantic Coverage & Health skeleton only. It explicitly left final `VF-01`, `CH-T02`, live source health, and runtime readiness out of scope. |
| `docs\S6_CH_T03_UI_MESSAGES_RENDERING_IMPLEMENTATION_CLOSEOUT_2026_04_28.md` | `CH-T03` closed bounded `ui_messages` rendering for exact keys only. It explicitly did not add final `VF-01`, live `/health`, `/ready`, backend telemetry, real source health, or runtime readiness. |
| `docs\S6_REMAINING_BLOCKER_MAP_2026_04_27.md` | `CH-T02` remains blocked by `VF-01`; `CH-T04` depends on `CH-T01`, `CH-T02`, and `CH-T03`. |
| `docs\S6_SPRINT1_4_AUTOMATION_ACCELERATION_MATRIX_2026_04_27.md` | `CH-T04` is an acceptance / hardening dependency row after `CH-T01`, `CH-T02`, and `CH-T03`. |
| `D:\产品设计\secupilot0421\visual negative` | Current available new frames include `HF-SH-01`, `HF-SH-02`, and `VF-14`; no `VF-01` Coverage & Health frame is present in the checked visual-negative directory. |
| `frontend\src\App.tsx` | The Coverage & Health surface still declares `data-live-health-source="none"` and `data-vf-01-state="pending"`. |
| `frontend\src\App.test.tsx` | Current tests assert skeleton anchors and bounded `ui_messages`; they do not assert final `VF-01`, live health, runtime readiness, or cross-surface hardening. |

## 4. CH-T02 Result

`CH-T02` cannot start safely from the current evidence.

Reason:

- `VF-01` final or approved semantic frame anchors are still missing.
- `CH-T01` intentionally created only the semantic skeleton.
- Starting `CH-T02` now would require inventing Coverage & Health visual semantics or treating the skeleton as final visual PASS.

Required before any later `CH-T02` implementation GO:

```text
VF-01 final or approved semantic frame anchors are available
exact visual / semantic acceptance anchors are named
exact allowed files and exact tests are named
implementation stays inside Coverage & Health frontend surface files
no backend/runtime/API/schema or live health source is required
no fixture/adapter/validator/ResolvedSurfaceContext change is required
```

## 5. CH-T04 Result

`CH-T04` cannot start safely from the current evidence.

Reason:

- `CH-T01` and `CH-T03` are closed.
- `CH-T02` remains HOLD pending `VF-01`.
- The current app still has no governed live source-health or runtime-readiness input for Coverage & Health.
- Implementing `CH-T04` now would either skip `CH-T02` or create runtime semantics that are outside the current bounded frontend queue.

Required before any later `CH-T04` implementation GO:

```text
CH-T02 is implemented or explicitly rescoped by governed decision
CH-T03 remains accepted as the ui_messages source boundary
exact cross-surface hardening assertions are named
exact runtime/source-health authority is either absent by design or governed
exact allowed files and exact tests are named
no backend/runtime/API/schema change is needed inside CH-T04,
  or that work has separate governed GO
no real data, secrets, deploy, public endpoint, or external pilot scope enters CH-T04
```

## 6. Jira / Tracker Handling

Do not mark `CH-T02` or `CH-T04` Done.

Allowed Jira action, if credentials are visible:

```text
Add non-transition HOLD comments only:
CH-T02 remains HOLD pending VF-01 final or approved semantic frame anchors.
CH-T04 remains HOLD pending CH-T02 plus governed runtime/source-health scope.
```

No Jira sync was attempted by this docs-only blocker refresh.

## 7. Next Route

```text
OPEN_SH_T09_ACCEPTANCE_CHECKLIST_OR_SAFE_JIRA_PARITY_SYNC
```

Reason:

- `CH-T02` and `CH-T04` remain blocked.
- The progress / risk board already identifies `SH-T09` as the next acceptance
  checklist after the Search / History chain (`SH-T01`, `SH-T02`, `SH-T03`,
  `SH-T05`, `SH-T06`, `SH-T07`, `SH-T08`) has closed or reconciled.
- If `SH-T09` cannot start safely, the idle fallback may perform safe Jira /
  tracker parity for already PASS or no-code reconciled tickets only.

## 8. Non-Authorization

This refresh does not authorize:

- `CH-T02` implementation;
- `CH-T04` implementation;
- final `VF-01` visual PASS;
- live `/health` or `/ready`;
- backend telemetry, runtime readiness, or source-health integration;
- cross-surface hardening implementation;
- fixture registry, fixture adapter, `ContextValidator`, or `ResolvedSurfaceContext` changes;
- Jira Done transition;
- real data, secrets, deploy, public endpoint, or external pilot.
