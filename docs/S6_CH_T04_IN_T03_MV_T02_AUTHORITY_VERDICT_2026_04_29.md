# S6 CH-T04 / IN-T03 / MV-T02 Authority Verdict

## Document Control

| Field | Value |
| --- | --- |
| Document | `S6_CH_T04_IN_T03_MV_T02_AUTHORITY_VERDICT_2026_04_29` |
| Date | 2026-04-29 |
| Review source | Governance / Claude Web authority review |
| Review mode | Authority decision only |
| Implementation authorization | NO |
| Prior input | `docs/S6_CH_T04_IN_T03_MV_T02_AUTHORITY_INPUT_2026_04_29.md` |

## Decision

```text
CH_T04_AUTHORITY_VERDICT_OPTION_A_FRONTEND_ONLY_UI_MESSAGES_SOURCE_HEALTH_SEMANTIC_SLICE
IN_T03_AUTHORITY_VERDICT_OPTION_B_NAVIGATION_ONLY_ENTRY_TO_EXISTING_APPROVAL_CONTEXT
MV_T02_AUTHORITY_VERDICT_OPTION_A_P0_P2_HARD_REDIRECT_OR_NO_MANAGER_ENTRY
IMPLEMENTATION_NOT_AUTHORIZED
EXACT_IMPLEMENTATION_CHECKLIST_REQUIRED_BEFORE_CODE
```

This record captures the authority verdict for the remaining `CH-T04`, `IN-T03`, and `MV-T02` lanes. It does not authorize implementation or Jira Done transitions.

## Verdict Table

| Ticket | Verdict | Next state |
| --- | --- | --- |
| `CH-T04` | `CH_T04_OPTION_A_FRONTEND_ONLY_UI_MESSAGES_SOURCE_HEALTH_SEMANTIC_SLICE` | Create exact implementation checklist |
| `IN-T03` | `IN_T03_OPTION_B_NAVIGATION_ONLY_ENTRY_TO_EXISTING_APPROVAL_CONTEXT` | Create exact implementation checklist |
| `MV-T02` | `MV_T02_OPTION_A_P0_P2_HARD_REDIRECT_OR_NO_MANAGER_ENTRY` | Create exact implementation checklist |

## CH-T04 Verdict

`CH-T04` may proceed only as a frontend-only `ui_messages` source-health semantic slice.

Required implementation boundaries:

- source-health copy must come from governed `ui_messages`;
- the UI may render unavailable / degraded placeholders only;
- the UI must not claim real-time health, live telemetry, current connection health, or runtime truth;
- no polling, websocket, live telemetry, backend endpoint, API contract, runtime protocol, or schema may be introduced.

The future checklist must prove:

- exact `ui_messages` keys or source fields;
- exact distinction between source-health display and live runtime health;
- forbidden DOM / copy assertions for live telemetry claims;
- exact allowed files, test command, rollback, and HOLD conditions.

## IN-T03 Verdict

`IN-T03` may proceed only as a navigation-only entry to the existing governed `/approval` context.

Required implementation boundaries:

- Inbox AR status hint is display-only;
- Inbox must not create, select, or imply `ActionMode`;
- P1 Inbox must not expose `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY`;
- navigation may only target the governed `/approval` route;
- navigation must not carry role, action, AP state, or approval authority through URL or storage;
- P2 can act only after arriving at the governed `/approval` surface.

The future checklist must prove:

- exact role / surface visibility for P1 and P2;
- exact navigation-only behavior;
- P1 cannot trigger any AP operation from Inbox;
- exact allowed files, tests, rollback, and HOLD conditions.

## MV-T02 Verdict

`MV-T02` may proceed only as P0/P2 hard redirect or no Manager entry.

Required implementation boundaries:

- P0/P2 access to `/manager` must hard redirect to the governed target route;
- no Manager View session state may be carried through URL or storage;
- `MV-T01` must remain free of P0/P2 conditional rendering placeholders;
- no P0/P2 Manager readonly degraded variant is authorized by this verdict.

If a future P0/P2 Manager readonly variant is desired, it requires a separate governed field mapping and a separate exact ticket.

The future checklist must prove:

- exact redirect target for P0 and P2;
- no URL/storage Manager state transfer;
- no P0/P2 conditional rendering branch in `MV-T01`;
- exact allowed files, tests, rollback, and HOLD conditions.

## Dependent Ticket Status

| Dependent ticket | Status |
| --- | --- |
| `IN-T06` | HOLD until `IN-T03` implementation checklist passes and implementation closes |
| `MV-T05` | HOLD; `MV-T02 = OPTION_A` does not open `MV-T05` |
| `CH-T04` acceptance closure | Wait for `CH-T04` implementation checklist and closeout |
| `AP-T11` / `AP-T12` | Require their own acceptance checklist; not closed by this review |
| `CD-T07` | Wait for independent checklist after `CD-T06` closeout |

## Non-Authorization

This authority verdict does not authorize implementation, frontend source changes, Storybook changes, Playwright changes, fixture/adapter/validator changes, `ResolvedSurfaceContext` changes, backend/runtime/API/schema, real data, anonymized real data, secrets, deploy, public endpoint, external pilot, Jira Done transition, or launch.

## Next Route

```text
OPEN_CH_T04_IN_T03_MV_T02_EXACT_IMPLEMENTATION_CHECKLISTS
```
