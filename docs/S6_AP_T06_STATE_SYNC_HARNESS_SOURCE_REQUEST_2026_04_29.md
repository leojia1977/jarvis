# S6 AP-T06 State-Sync Harness Source Request 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 AP-T06 State-Sync Harness Source Request 2026-04-29 |
| Ticket | `AP-T06` |
| Related split | `AP-T06A` |
| Status | AP_T06_STATE_SYNC_HARNESS_SOURCE_REQUEST_READY_NO_IMPLEMENTATION |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Automation id | `secupilot-30m-bounded-burn-runner` |
| Trigger | Idle fallback blocker/source request refresh |

## 2. Decision

```text
AP_T06_STATE_SYNC_HARNESS_SOURCE_REQUEST_READY_NO_IMPLEMENTATION
```

This record converts the remaining full `AP-T06` blocker into an exact
state-sync source and test-harness request.

It does not implement full `AP-T06`, transition Jira, authorize backend
`STATE_SYNC`, or change frontend state semantics.

## 3. Current State

Closed safe split:

```text
AP-T06A static observation-window readonly skeleton
```

Open parent:

```text
AP-T06 full countdown / state-sync
SCRUM-64 remains not Done
```

Full `AP-T06` remains HOLD because the current repo intentionally exposes:

```text
data-timer-authority="none"
data-state-sync="not-implemented"
data-state-migration="none"
```

Those anchors must remain true until a governed state-sync source exists.

## 4. Required Source / Harness Decisions

Product, governance, or test-source delivery must define:

- exact state-sync input contract name;
- exact material migration event that returns `OBSERVATION_WINDOW` to
  `PENDING_APPROVAL`;
- exact authority that emits the material migration;
- exact rule that frontend countdown display is presentation-only;
- whether a test-only `emitStateSync` helper is authorized;
- where that helper may live;
- whether Playwright `page.clock.fastForward()` is allowed only for display
  assertions;
- how state migration is driven after display time is advanced;
- how stale or missing state-sync events fail closed;
- whether state-sync assertions can run without backend/runtime/API/schema
  changes.

## 5. Minimum Future Test Semantics

A later full `AP-T06` checklist must be able to test all of the following
without inventing product behavior:

```text
observation-window countdown display is read-only
client clock does not mutate ar_status
page.clock.fastForward only changes presentation-time display
material state migration requires explicit state-sync input
state-sync input changes OBSERVATION_WINDOW -> PENDING_APPROVAL
missing state-sync keeps AP surface read-only
stale state-sync is rejected or safely ignored
no backend/runtime/API/schema dependency appears
```

## 6. Suggested Anchors

The future source may confirm or replace these anchors:

```text
data-timer-authority="presentation-only"
data-state-sync="external-input-required"
data-state-migration="state-sync-only"
data-state-sync-source="governed-test-harness"
emitStateSync(event)
```

If different anchors or helper names are chosen, they must be explicitly listed
before implementation begins.

## 7. Dependency Impact

This source request directly affects:

- full `AP-T06`;
- `AP-T11` full state-transition assertions;
- `AP-T12` AP acceptance suite;
- any future Playwright observation-window LC-B / LC-N material migration
  tests.

It does not affect the closed `AP-T06A` static skeleton.

## 8. Future Implementation Eligibility

Full `AP-T06` can return to launch checklist only after a later record proves:

- exact state-sync input contract exists;
- exact display-vs-authority rule exists;
- exact test hook exists;
- exact allowed files and test commands are known;
- no backend/runtime/API/schema dependency is required, or a separate governed
  backend/runtime/API/schema decision record has authorized it;
- no fixture/adapter/validator or `ResolvedSurfaceContext` change is required,
  or a separate governed source expansion ticket has authorized it.

## 9. Non-Authorization

This request does not authorize:

- full `AP-T06` implementation;
- countdown-driven state migration;
- `setTimeout` or client-clock authority;
- backend `STATE_SYNC`;
- Playwright time travel as product behavior;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext`
  changes;
- backend/runtime/API/schema work;
- Jira Done transition;
- real data;
- secrets;
- deploy;
- public endpoint;
- external pilot.

## 10. Next Route

```text
WAIT_FOR_MV_T04_IMPLEMENTATION_GO_OR_AP_T06_STATE_SYNC_SOURCE_DELIVERY_OR_AP_T09_VF15_SOURCE_DELIVERY_OR_SH_T09_RECONCILIATION_GO_OR_JIRA_MAPPING_GO_OR_NEXT_IDLE_FALLBACK
```
