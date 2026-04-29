# S6 CH-T04 Source-Health Semantic Implementation Checklist

## Document Control

| Field | Value |
| --- | --- |
| Document | `S6_CH_T04_SOURCE_HEALTH_SEMANTIC_IMPLEMENTATION_CHECKLIST_2026_04_29` |
| Date | 2026-04-29 |
| Ticket | `CH-T04` |
| Verdict source | `docs/S6_CH_T04_IN_T03_MV_T02_AUTHORITY_VERDICT_2026_04_29.md` |
| Mode | exact implementation checklist |
| Implementation authorization | NO |

## Decision

```text
CH_T04_EXACT_IMPLEMENTATION_CHECKLIST_READY
CH_T04_IMPLEMENTATION_GO_REQUIRED_BEFORE_CODE
```

`CH-T04` is implementable only if Jarvis grants a later exact implementation GO. This checklist does not authorize code.

## Authority Verdict

```text
CH_T04_OPTION_A_FRONTEND_ONLY_UI_MESSAGES_SOURCE_HEALTH_SEMANTIC_SLICE
```

The implementation must remain frontend-only and `ui_messages` sourced. It must not claim live runtime health.

## Allowed Scope

- Render source-health unavailable / degraded semantic placeholders on the existing Coverage & Health surface.
- Source displayed copy from governed `ui_messages` only.
- Add DOM anchors proving the distinction between source-health display and live runtime health.
- Add regression tests proving forbidden live telemetry claims are absent.

## Allowed Files

```text
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/src/App.css
docs/S6_CH_T04_SOURCE_HEALTH_SEMANTIC_IMPLEMENTATION_CLOSEOUT_2026_04_29.md
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

- Coverage & Health source-health region exists only as semantic display.
- `data-source-health-mode="ui_messages_semantic"` or equivalent explicit anchor is present.
- `data-live-health-source="none"` remains true or equivalent non-live anchor remains present.
- Unavailable / degraded copy is sourced from `ui_messages`.
- DOM/text must not claim:
  - current connection normal;
  - realtime source health;
  - live telemetry;
  - runtime readiness;
  - backend health truth.
- No polling/websocket/API/schema/runtime/backend code appears.

## Non-Goals

- no live `/health` or `/ready`;
- no polling / websocket / live telemetry;
- no backend/runtime/API/schema;
- no fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- no real data, secrets, deploy, public endpoint, external pilot, or launch.

## HOLD Conditions

HOLD if implementation needs:

- any backend/runtime/API/schema change;
- live source-health truth;
- non-`ui_messages` copy source;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- new route handoff;
- files outside the allowed list;
- visual semantics beyond VF-01 semantic baseline;
- failed tests/build/preflight;
- mandatory external review trigger.

## Reviewer

Claude Code focused review is required for implementation diff if Jarvis later grants implementation GO.

## Next Route

```text
WAIT_FOR_CH_T04_IMPLEMENTATION_GO_OR_OPEN_NEXT_EXACT_CHECKLIST
```
