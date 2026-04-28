# S6 AP-T06A Static Observation-Window Skeleton Closeout 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T06A` |
| Parent / Related Ticket | `AP-T06` |
| Title | Static observation-window readonly skeleton |
| Status | `IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED` |
| Date | 2026-04-28 |
| Jira | `SCRUM-65`, status `已完成` |

## 2. Scope Implemented

AP-T06A implements a narrow static skeleton for the existing Phase 3
`OBSERVATION_WINDOW` context:

- renders an observation-window readonly boundary;
- exposes `data-timer-authority="none"`;
- exposes `data-state-sync="not-implemented"`;
- exposes `data-state-migration="none"`;
- shows fixture-provided total/remaining minutes and expiry action as display evidence only;
- mounts the VF-11 readonly controls as disabled and `aria-disabled="true"`;
- includes disabled `view-details-button` as secondary case-context navigation;
- does not mount the active AP-T03 CTA boundary in observation-window state.

## 3. Files Changed

Implementation files:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

Governance records:

- `docs/S6_VISUAL_BASELINE_VF03_VF11_VF12_VF13_RECONCILIATION_2026_04_28.md`
- `docs/S6_AP_T06_OBSERVATION_WINDOW_READINESS_CHECKLIST_2026_04_28.md`
- `docs/S6_AP_T06A_STATIC_OBSERVATION_WINDOW_SKELETON_CLOSEOUT_2026_04_28.md`
- route / handoff / progress-board updates

## 4. Evidence

Gate results:

```text
npm --prefix frontend test                 PASS, 81 tests
npm --prefix frontend run build            PASS
npm --prefix frontend run test:e2e         PASS, 10 tests
py -3 scripts/git_preflight.py --mode pilot PASS, backend unittest guard 164 tests
git diff --check                           PASS, Windows line-ending warnings only
Claude Code focused review                 PASS
```

Jira sync:

```text
SCRUM-65 created and transitioned to Done.
SCRUM-64 kept open with comment: full AP-T06 countdown/state-sync remains HOLD.
```

## 5. Explicit Non-Goals

AP-T06A does not implement:

- countdown-driven state migration;
- `setTimeout` or client-clock authority;
- backend `STATE_SYNC`;
- Playwright `emitStateSync` harness;
- AP-T06 full countdown / state-sync behavior;
- final VF-11 visual PASS styling;
- backend/runtime/API/schema changes;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- real data, secrets, deploy, public endpoint, or external pilot.

## 6. Residual HOLD

Full AP-T06 remains HOLD until a later exact checklist proves:

- exact state-sync input contract;
- exact test hook such as `emitStateSync`;
- exact allowed files and test command;
- no backend/runtime/API/schema dependency;
- no material authority ambiguity.

Next safe route:

```text
OPEN_MV_T03_RELAUNCH_CHECKLIST_OR_AP_T08_SH_T08_NARROW_IMPLEMENTATION_CHECKLIST
```
