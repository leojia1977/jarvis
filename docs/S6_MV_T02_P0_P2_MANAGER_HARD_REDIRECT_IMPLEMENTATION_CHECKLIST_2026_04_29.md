# S6 MV-T02 P0/P2 Manager Hard Redirect Implementation Checklist

## Document Control

| Field | Value |
| --- | --- |
| Document | `S6_MV_T02_P0_P2_MANAGER_HARD_REDIRECT_IMPLEMENTATION_CHECKLIST_2026_04_29` |
| Date | 2026-04-29 |
| Ticket | `MV-T02` |
| Verdict source | `docs/S6_CH_T04_IN_T03_MV_T02_AUTHORITY_VERDICT_2026_04_29.md` |
| Mode | exact implementation checklist |
| Implementation authorization | NO |

## Decision

```text
MV_T02_EXACT_IMPLEMENTATION_CHECKLIST_READY
MV_T02_IMPLEMENTATION_GO_REQUIRED_BEFORE_CODE
```

`MV-T02` is implementable only if Jarvis grants a later exact implementation GO. This checklist does not authorize code.

## Authority Verdict

```text
MV_T02_OPTION_A_P0_P2_HARD_REDIRECT_OR_NO_MANAGER_ENTRY
```

P0/P2 Manager readonly degraded variants are not authorized. Current implementation must hard redirect or deny Manager entry for P0/P2.

## Allowed Scope

- Ensure P0/P2 access to `/manager` does not render Manager content.
- Hard redirect P0/P2 to governed target routes or preserve an explicit no-entry guard if redirect cannot be safely proven.
- Keep `MV-T01` P3-only without P0/P2 conditional rendering placeholders.
- Add regression tests proving no P0/P2 Manager content, raw evidence DOM, or Manager state transfer exists.

## Allowed Files

```text
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/src/App.css
docs/S6_MV_T02_P0_P2_MANAGER_HARD_REDIRECT_IMPLEMENTATION_CLOSEOUT_2026_04_29.md
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

- P0/P2 `/manager` access does not mount P3 Manager content.
- P0/P2 route behavior uses governed redirect or explicit no-entry guard.
- Redirect/no-entry does not transfer Manager session state through URL, localStorage, or sessionStorage.
- `MV-T01` remains free of P0/P2 placeholder branches.
- No P0/P2 readonly degraded Manager variant is added.
- No raw evidence DOM, host evidence DOM, approval controls, P2 workbench controls, or P3-only audit leakage is mounted for P0/P2.

## Non-Goals

- no P0/P2 Manager readonly degraded variant;
- no governed field mapping invention;
- no MV-T05 acceptance closure;
- no raw evidence or host evidence DOM;
- no backend/runtime/API/schema;
- no fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- no real data, secrets, deploy, public endpoint, external pilot, or launch.

## HOLD Conditions

HOLD if implementation needs:

- P0/P2 field mapping;
- P0/P2 Manager readonly variant;
- URL/storage authority;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- MV-T05 acceptance scope;
- files outside the allowed list;
- failed tests/build/preflight;
- mandatory external review trigger.

## Reviewer

Claude Code focused review is required for implementation diff if Jarvis later grants implementation GO.

## Dependent Ticket Impact

`MV-T05` remains HOLD. `MV-T02 = OPTION_A` does not open `MV-T05`; a future `MV-T05` route requires explicit rescope or separate authority review.

## Next Route

```text
WAIT_FOR_MV_T02_IMPLEMENTATION_GO_OR_NEXT_EXACT_LOW_RISK_BURN_POOL
```
