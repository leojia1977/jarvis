# S6 AP-T06 Observation Window Readiness Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T06` |
| Title | Observation-window countdown / state-sync readiness checklist |
| Status | `READINESS_SPLIT_STATIC_SKELETON_CANDIDATE_FULL_COUNTDOWN_HOLD` |
| Date | 2026-04-28 |
| Jira | `SCRUM-64`, status `待办` |

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

Missing or incomplete inputs:

- final `VF-11` visual frame for observation-window state header;
- exact frontend state-sync input contract for material migration;
- exact Playwright `emitStateSync` or equivalent test hook;
- explicit rule that frontend clock display cannot cause real status migration.

## 3. Split Decision

```text
AP_T06A_STATIC_READONLY_OBSERVATION_WINDOW_SKELETON_READY_FOR_LATER_IMPLEMENTATION_GO
AP_T06_FULL_COUNTDOWN_STATE_SYNC_HOLD
```

Interpretation:

- A future small implementation may be safe if it is limited to a static, read-only observation-window skeleton using existing Phase 3 / Phase 4 fixture data.
- Full countdown / state-sync behavior is not safe yet and remains HOLD.

## 4. AP-T06A Static Skeleton Allowed Shape

A later implementation GO may allow only:

- render `OBSERVATION_WINDOW` read-only state label;
- show observation-window duration or expiry action if already present in existing fixture audit trail;
- show `data-timer-authority="none"`;
- show `data-state-sync="not-implemented"`;
- assert no approve/reject/delay/observe controls attach while in observation window;
- no final `VF-11` visual PASS.

Allowed files for that later implementation must remain exact:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- closeout / route / handoff docs

## 5. Full AP-T06 HOLD

Full AP-T06 remains HOLD if it needs:

- countdown-driven state migration;
- `setTimeout` / client clock as authority;
- backend `STATE_SYNC`;
- Playwright time travel as a product mechanism instead of test-only display assertion;
- fixture/adapter/validator / `ResolvedSurfaceContext` changes;
- final `VF-11` visual styling;
- real data, deploy, public endpoint, or external pilot.

## 6. Next Safe Route

```text
OPEN_AP_T06A_STATIC_OBSERVATION_WINDOW_SKELETON_IMPLEMENTATION_GO_OR_OPEN_MV_T03_RELAUNCH_CHECKLIST
```
