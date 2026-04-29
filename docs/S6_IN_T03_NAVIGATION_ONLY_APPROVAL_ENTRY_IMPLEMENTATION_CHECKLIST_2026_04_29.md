# S6 IN-T03 Navigation-Only Approval Entry Implementation Checklist

## Document Control

| Field | Value |
| --- | --- |
| Document | `S6_IN_T03_NAVIGATION_ONLY_APPROVAL_ENTRY_IMPLEMENTATION_CHECKLIST_2026_04_29` |
| Date | 2026-04-29 |
| Ticket | `IN-T03` |
| Verdict source | `docs/S6_CH_T04_IN_T03_MV_T02_AUTHORITY_VERDICT_2026_04_29.md` |
| Mode | exact implementation checklist |
| Implementation authorization | NO |

## Decision

```text
IN_T03_EXACT_IMPLEMENTATION_CHECKLIST_READY
IN_T03_IMPLEMENTATION_GO_REQUIRED_BEFORE_CODE
```

`IN-T03` is implementable only if Jarvis grants a later exact implementation GO. This checklist does not authorize code.

## Authority Verdict

```text
IN_T03_OPTION_B_NAVIGATION_ONLY_ENTRY_TO_EXISTING_APPROVAL_CONTEXT
```

The implementation must be navigation-only and non-mutating. Inbox may point to the governed `/approval` route but must not perform approval work inside Inbox.

## Allowed Scope

- Add an Inbox AR hint / entry affordance that navigates to the existing governed `/approval` context.
- Keep the hint display-only before navigation.
- Preserve P1 boundaries: P1 must not see or select `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY`.
- Ensure no role, AP state, action, or approval authority is carried through URL or storage.

## Allowed Files

```text
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/src/App.css
docs/S6_IN_T03_NAVIGATION_ONLY_APPROVAL_ENTRY_IMPLEMENTATION_CLOSEOUT_2026_04_29.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
releases/release_manifest.json
```

Any need outside these files is a HOLD.

## Required Test Command

```text
cd frontend && npm test
cd frontend && npm run build
git diff --check
py -3 scripts/git_preflight.py --mode pilot
```

## Mandatory Assertions

- Inbox AR hint is present only as display/navigation affordance.
- Inbox does not create, select, or imply `ActionMode`.
- Inbox text / DOM does not expose `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` for P1.
- Navigation target is existing `/approval`.
- No URL query, route param, localStorage, or sessionStorage carries role/action/AP authority.
- P2 can act only after arriving at the governed `/approval` surface.
- No approve/reject/delay/observe/close action fires from Inbox.

## Non-Goals

- no action-capable Inbox shortcut;
- no approval submission or close execution;
- no AP state mutation;
- no new P2 authority model;
- no backend/runtime/API/schema;
- no fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- no real data, secrets, deploy, public endpoint, external pilot, or launch.

## HOLD Conditions

HOLD if implementation needs:

- action-capable shortcut behavior;
- role/action authority through URL/storage;
- AP mutation inside Inbox;
- P1 exposure to `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY`;
- route handoff beyond governed `/approval` navigation;
- files outside the allowed list;
- failed tests/build/preflight;
- mandatory external review trigger.

## Reviewer

Claude Code focused review is required for implementation diff if Jarvis later grants implementation GO.

## Dependent Ticket Impact

`IN-T06` remains HOLD until `IN-T03` implementation closes and a separate acceptance/reconciliation checklist is opened.

## Next Route

```text
WAIT_FOR_IN_T03_IMPLEMENTATION_GO_OR_OPEN_NEXT_EXACT_CHECKLIST
```
