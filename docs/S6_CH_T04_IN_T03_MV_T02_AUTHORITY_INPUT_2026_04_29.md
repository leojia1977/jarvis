# S6 CH-T04 / IN-T03 / MV-T02 Authority Input

## Document Control

| Field | Value |
| --- | --- |
| Document | `S6_CH_T04_IN_T03_MV_T02_AUTHORITY_INPUT_2026_04_29` |
| Date | 2026-04-29 |
| Mode | docs-only authority input |
| Implementation authorization | NO |
| Source route | `OPEN_CH_T04_IN_T03_MV_T02_AUTHORITY_INPUT` |

## Decision

```text
CH_T04_IN_T03_MV_T02_AUTHORITY_INPUT_READY
IMPLEMENTATION_NOT_AUTHORIZED
AUTHORITY_DECISION_REQUIRED_BEFORE_CODE
```

This record packages the remaining authority questions after `AP-T09`, `AP-T06`, and `CD-T06` narrow implementations. It does not decide authority, authorize implementation, or mark any dependent ticket Done.

## Source Evidence

- `docs/S6_R1_CH_T04_RUNTIME_SOURCE_HEALTH_AUTHORITY_REVIEW_2026_04_29.md`
- `docs/S6_R1_IN_T03_P2_SHORTCUT_AUTHORITY_REVIEW_2026_04_29.md`
- `docs/S6_R1_MV_T02_P0_P2_MANAGER_AUTHORITY_REVIEW_2026_04_29.md`
- `docs/S6_REMAINING_SCOPE_TRIAGE_AND_BATCH_LAUNCH_PLAN_2026_04_29.md`
- `docs/S6_R2_R1_AUTHORITY_REVIEW_PROMPT_PACK_2026_04_29.md`
- `docs/S6_AP_T06_STATE_SYNC_TEST_HOOK_CLOSEOUT_2026_04_29.md`
- `docs/S6_CD_T06_CLOSED_CONTEXT_CLOSEOUT_2026_04_29.md`

## Current State

| Lane | Current state | Still blocked by |
| --- | --- | --- |
| `CH-T04` | Authority input ready | Runtime/source-health scope decision |
| `IN-T03` | Authority input ready | P2 shortcut approval / close-entry authority |
| `MV-T02` | Authority input ready | P0/P2 Manager authority model |

`AP-T06` and `CD-T06` are now implemented and Jira-synced Done, but that does not unlock these three lanes. They remain separate authority surfaces.

## CH-T04 Authority Input

### Required Decision

Choose exactly one:

```text
CH_T04_OPTION_A_FRONTEND_ONLY_UI_MESSAGES_SOURCE_HEALTH_SEMANTIC_SLICE
CH_T04_OPTION_B_RUNTIME_BACKEND_SOURCE_HEALTH_REQUIRED_HOLD
CH_T04_OPTION_C_REMOVE_OR_DEFER_CH_T04_FROM_CURRENT_RELEASE
```

### Recommended Boundary

Prefer `OPTION_A` only if CH-T04 can remain a frontend-only semantic/status slice:

- source-health copy is driven by governed `ui_messages`;
- the UI may render unavailable/degraded placeholders only from existing mock/source-bound state;
- no live telemetry, polling, websocket, runtime service, backend endpoint, API contract, or schema is introduced;
- no real source health truth is claimed.

If any runtime, telemetry, backend, API, schema, or live source-health protocol is required, choose `OPTION_B` and keep CH-T04 HOLD pending a separate human/governed backend/runtime decision.

### Future Implementation Checklist Must Prove

- exact allowed files and test command;
- exact `ui_messages` keys or source fields;
- explicit distinction between source-health display and live runtime health;
- forbidden DOM/copy assertions for live telemetry claims;
- rollback/HOLD conditions.

## IN-T03 Authority Input

### Required Decision

Choose exactly one:

```text
IN_T03_OPTION_A_NO_INBOX_P2_SHORTCUT_IN_CURRENT_RELEASE
IN_T03_OPTION_B_NAVIGATION_ONLY_ENTRY_TO_EXISTING_APPROVAL_CONTEXT
IN_T03_OPTION_C_DISPLAY_ONLY_STATUS_HINT_NO_NAVIGATION_NO_ACTION
IN_T03_OPTION_D_ACTION_CAPABLE_SHORTCUT_REQUIRED_HOLD_FOR_AUTHORITY_REVIEW
```

### Recommended Boundary

Prefer `OPTION_B` or `OPTION_C` only if implementation remains non-mutating:

- Inbox must not create, select, or imply `ActionMode`;
- P1 must not see `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY`;
- any navigation must go to an already governed route and must not carry role/action authority through URL or storage;
- no AP state mutation, approval submission, close execution, backend/runtime/API/schema, fixture/adapter/validator, or `ResolvedSurfaceContext` change is allowed.

If product requires an action-capable Inbox shortcut, choose `OPTION_D` and keep IN-T03 HOLD until a separate authority review defines the P2 ownership model.

### Future Implementation Checklist Must Prove

- exact role/surface visibility;
- display-only vs navigation-only vs action-capable behavior;
- exact files and tests;
- no P1 ActionMode creation;
- no P2 authority leakage into Inbox;
- rollback/HOLD conditions.

## MV-T02 Authority Input

### Required Decision

Choose exactly one:

```text
MV_T02_OPTION_A_P0_P2_HARD_REDIRECT_OR_NO_MANAGER_ENTRY
MV_T02_OPTION_B_SEPARATE_READONLY_DEGRADED_P0_P2_MANAGER_VARIANTS
MV_T02_OPTION_C_DEFER_MV_T02_AND_KEEP_MV_T05_HOLD
```

### Recommended Boundary

Prefer `OPTION_A` unless a governed P0/P2 read-only field model is explicitly approved.

If `OPTION_B` is selected, it must be a separate exact ticket and must not retrofit placeholders into `MV-T01`:

- P0/P2 fields must be explicitly listed;
- P0/P2 must not reuse P3-only raw/technical audit surfaces;
- raw evidence DOM, host evidence DOM, approval controls, P2 workbench controls, and route/storage authority fallback must remain absent;
- P3 manager summary components remain P3-only unless a new governed mapping says otherwise.

### Future Implementation Checklist Must Prove

- exact P0/P2 visibility fields;
- exact forbidden DOM list;
- exact files and tests;
- whether separate renderable contexts are required;
- no URL/storage role authority;
- rollback/HOLD conditions.

## Dependent Ticket Impact

| Dependent ticket | Status after this input |
| --- | --- |
| `IN-T06` | HOLD until `IN-T03` authority decision |
| `MV-T05` | HOLD until `MV-T02` authority decision or explicit rescope |
| `CH-T04` acceptance closure | HOLD until CH-T04 scope decision |
| `AP-T11` / `AP-T12` | Still require their own acceptance checklist after `AP-T06` + `AP-T09`; this input does not close them |
| `CD-T07` | May be considered later after `CD-T06` closeout is committed and an exact acceptance/reconciliation checklist is opened |

## Copy-Ready Governance Request

```text
Governance / Claude Web / Jarvis authority review:

Review CH-T04, IN-T03, and MV-T02 authority only.

CH-T04: choose frontend-only ui_messages source-health semantic slice, runtime/backend source-health HOLD, or defer/remove from current release.
IN-T03: choose no shortcut, navigation-only, display-only, or action-capable HOLD.
MV-T02: choose hard redirect/no manager entry, separate readonly degraded P0/P2 variants, or defer.

Do not authorize implementation, launch, deploy, real data, secrets, public endpoint, external pilot,
backend/runtime/API/schema, fixture/adapter/validator, or ResolvedSurfaceContext changes from this review.
Any PASS must be converted into a later exact implementation checklist with allowed files, tests, reviewer path, rollback, and HOLD conditions.
```

## Non-Authorization

This record does not authorize implementation, frontend source changes, Storybook changes, Playwright changes, fixture/adapter/validator changes, `ResolvedSurfaceContext` changes, backend/runtime/API/schema, real data, anonymized real data, secrets, deploy, public endpoint, external pilot, Jira Done transition, or launch.

## Next Route

```text
WAIT_FOR_CH_T04_SCOPE_DECISION_OR_IN_T03_AUTHORITY_DECISION_OR_MV_T02_AUTHORITY_DECISION_OR_NEXT_EXACT_LOW_RISK_BURN_POOL
```
