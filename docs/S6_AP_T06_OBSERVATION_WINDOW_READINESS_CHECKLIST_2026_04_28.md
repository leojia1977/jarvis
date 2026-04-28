# S6 AP-T06 Observation Window Readiness Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T06` |
| Title | Observation-window countdown / state-sync readiness checklist |
| Status | `AP_T06A_STATIC_SKELETON_IMPLEMENTATION_GO_FULL_COUNTDOWN_HOLD` |
| Date | 2026-04-28 |
| Jira | `SCRUM-64`, status `待办`; AP-T06A slice `SCRUM-65`, status `已完成` |

## 2. Current Inputs

Closed prerequisites:

- `AP-T01` approval route shell / guard;
- `AP-T03` approval CTA boundary;
- `AP-T05` delay / observe configuration shell;
- `AP-T10` display-only AR status mapping.

Existing fixture evidence:

- Phase 3 carries `OBSERVATION_WINDOW`;
- Phase 4 carries return to `PENDING_APPROVAL`;
- audit trail includes `AUD-003` observation selected and `AUD-004` observation expired / `RETURN_TO_PENDING_APPROVAL`.

Resolved visual input:

- `VF-11` v0.2 is accepted as `PASS` input for static observation-window skeleton and selector baseline;
- `VF-12` v0.2 is accepted as `PASS` input for the adjacent terminal lock state;

Still missing or incomplete inputs:

- exact frontend state-sync input contract for material migration;
- exact Playwright `emitStateSync` or equivalent test hook;
- explicit rule that frontend clock display cannot cause real status migration.

## 3. Split Decision

```text
AP_T06A_STATIC_READONLY_OBSERVATION_WINDOW_SKELETON_IMPLEMENTATION_GO
AP_T06_FULL_COUNTDOWN_STATE_SYNC_HOLD
```

Interpretation:

- Jarvis authorized AP-T06A implementation GO after `VF-11` v0.2 was accepted as PASS input.
- AP-T06A is limited to a static, read-only observation-window skeleton using existing Phase 3 / Phase 4 fixture data.
- Full countdown / state-sync behavior is not safe yet and remains HOLD.

## 4. AP-T06A Static Skeleton Allowed Shape

AP-T06A implementation may allow only:

- render `OBSERVATION_WINDOW` read-only state label;
- show observation-window duration or expiry action if already present in existing fixture audit trail;
- show `data-timer-authority="none"`;
- show `data-state-sync="not-implemented"`;
- mount observation-window controls as disabled and `aria-disabled="true"` per `VF-11` v0.2;
- include disabled `view-details-button` as a secondary case-context navigation action;
- no material timer, countdown-driven migration, or state-sync behavior;
- no final visual PASS claim.

Allowed files for that later implementation must remain exact:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- closeout / route / handoff docs

Required carried-forward implementation notes:

```text
F-N01: view-details-button is a secondary action for navigating case context and
must be disabled during active OBSERVATION_WINDOW.

D01C-N01: missing-signal-notice must carry data-message-source="ui_messages".
```

## 5. Full AP-T06 HOLD

Full AP-T06 remains HOLD if it needs:

- countdown-driven state migration;
- `setTimeout` / client clock as authority;
- backend `STATE_SYNC`;
- Playwright time travel as a product mechanism instead of test-only display assertion;
- fixture/adapter/validator / `ResolvedSurfaceContext` changes;
- final `VF-11` visual styling or visual PASS claim;
- real data, deploy, public endpoint, or external pilot.

## 6. Next Safe Route

```text
OPEN_AP_T06A_STATIC_OBSERVATION_WINDOW_SKELETON_CLOSEOUT_OR_OPEN_MV_T03_RELAUNCH_CHECKLIST
```
