# S6 CH-T02 Coverage & Health Main Frame Launch Checklist 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `CH-T02` |
| Title | Coverage & Health P0 semantic frame |
| Status | CH_T02_LAUNCH_CHECKLIST_GO_FOR_BOUNDED_FRONTEND_IMPLEMENTATION |
| Date | 2026-04-29 |
| Primary implementor | Codex |
| Execution surface | codex |
| Reviewer | Claude Code focused review |
| Review surface | claude-cmd |
| External review | Not mandatory unless architecture/governance boundary changes |
| Source reconciliation | `docs\S6_VF01_COVERAGE_HEALTH_BASELINE_RECONCILIATION_2026_04_29.md` |

## 2. Decision

Decision:

```text
CH_T02_LAUNCH_CHECKLIST_GO_FOR_BOUNDED_FRONTEND_IMPLEMENTATION
```

Rationale:

- `VF-01` semantic anchors are now available.
- Implementation can stay inside the existing Coverage & Health frontend surface.
- No backend/runtime/API/schema work is needed.
- No fixture registry, adapter, validator, or `ResolvedSurfaceContext` change is needed.
- Existing `CH-T01` and `CH-T03` provide the route skeleton and bounded `ui_messages` slot.

Boundary note:

```text
The current mock fixture set does not create a production P0 route context. CH-T02 may implement
and component-test the P0 semantic frame branch without changing fixture/adapter/validator
authority. P2 remains the existing reduced/skeleton route until a later exact ticket authorizes
P2 Coverage & Health behavior.
```

## 3. Allowed Files

Implementation files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

Governance files:

```text
docs/S6_VF01_COVERAGE_HEALTH_BASELINE_RECONCILIATION_2026_04_29.md
docs/S6_CH_T02_COVERAGE_HEALTH_MAIN_FRAME_LAUNCH_CHECKLIST_2026_04_29.md
docs/S6_CH_T02_COVERAGE_HEALTH_MAIN_FRAME_CLOSEOUT_2026_04_29.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

## 4. Scope

Allowed:

- P0 Coverage & Health semantic frame branch;
- `VF-01` test ids and semantic landmarks;
- `ui_messages` anchors for `missing-signal-notice`, `confidence-notice`, and `escalation-hint`;
- forbidden DOM absence assertions;
- preservation of current P2 reduced/skeleton Coverage & Health behavior.

Not allowed:

- final visual PASS or pixel implementation;
- backend/runtime/API/schema changes;
- live source health, `/health`, `/ready`, telemetry, or connector status;
- real data, anonymized real data, secrets, deploy, public endpoint, or external pilot;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- coverage escalation, ActionMode, approval mutation, P2/P3 authority change, or route handoff.

## 5. Acceptance Checks

Required checks:

```text
coverage-health-root is rendered for the P0 component branch
current-coverage-level renders the current coverage ceiling
field-presence-rate renders from existing resolved_visibility.fields only
join-health-rate does not claim live backend health
data-freshness-indicator renders mock freshness
capability-tier-reference is read-only and preserves hard ceiling semantics
field-switch-matrix renders existing field switch states
capability-package-list does not create unlock packages
ui-message-preview renders governed ui_messages only
missing-signal-notice carries data-message-source="ui_messages"
confidence-notice carries data-message-source="ui_messages"
escalation-hint carries data-message-source="ui_messages"
forbidden DOM anchors are not attached
P2 Coverage & Health remains reduced/skeleton and not upgraded to the P0 frame
```

## 6. Gate Commands

Required gates:

```text
npm run test -- --run
npm run build
py -3 scripts/git_preflight.py --mode pilot
git diff --check
Claude Code focused review on implementation diff
```

## 7. HOLD Conditions

HOLD immediately if implementation requires:

- backend/runtime/API/schema changes;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- live source health, real data, secrets, deploy, public endpoint, or external pilot;
- P2/P3 authority change or route handoff;
- coverage unlock copy not sourced from existing governed data;
- exact tests cannot prove the semantic anchors or forbidden DOM assertions.
