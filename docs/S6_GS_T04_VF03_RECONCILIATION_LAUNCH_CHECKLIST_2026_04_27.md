# S6 GS-T04 VF-03 Reconciliation Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 GS-T04 VF-03 Reconciliation Launch Checklist 2026-04-27 |
| Ticket | `GS-T04-VF03-RECONCILIATION` |
| Scope | Align `GS-T04` semantic skeleton with `VF-03 v0.2` anchors |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_SYNCED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Visual source | `D:\产品设计\secupilot0421\SecuPilot_VF-03_Expert_Mode_Entry_Frame_v0.2.md` |
| Prototype source | `D:\产品设计\secupilot0421\SecuPilot_VF-03_Expert_Mode_Entry_Frame_v0.2.html` |
| Parent closeout | `docs\S6_GS_T04_EXPERT_MODE_ENTRY_SKELETON_CLOSEOUT_2026_04_27.md` |
| Primary implementor | Codex |
| Execution surface | codex |
| Reviewer | Claude Code focused review if implementation diff exists |
| Review surface | claude-cmd |
| SWE | disabled |

This checklist inserts a small reconciliation ticket after `GS-T04` because `VF-03 v0.2` arrived after the initial skeleton closeout.

## 2. Launch Decision

Decision:

```text
GO_FOR_BOUNDED_VF03_ANCHOR_RECONCILIATION
```

Meaning:

- Add the exact implementation anchors and selector semantics required by `VF-03 v0.2`.
- Do not copy the static HTML prototype into production code.
- Do not claim final `VF-03` visual PASS.

## 3. Exact Scope

Implement only:

- `data-testid="vf-03-expert-mode-frame"` with `data-expert-mode="false"`, governed case state, coverage, and role attributes;
- `data-testid="expert-mode-toggle"` with `aria-pressed="false"` and governed `data-role-variant`;
- `P1_RESTRICTED` / `P2_TOGGLEABLE` selector semantics and `P3` hidden behavior;
- `expert-mode-on-example`, active banner, and allowed current-field-depth selector anchors;
- `lineage-confidence` and `lineage-confidence-expert` as `DEGRADED`;
- forbidden selector absence tests for `expert-mode-unlock-off-field`, `coverage-upgrade-prompt`, and `blast-radius-expert-unlock`.

## 4. Exact Non-Goals

Do not implement:

- final VF-03 visual styling or visual PASS;
- HTML prototype copy/paste;
- interactive expert-mode switching;
- route, modal, drawer, settings, or backend action;
- field expansion beyond the current field set;
- coverage bypass or permission upgrade;
- P2/P3 authority changes;
- backend/runtime/API/schema changes;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- Storybook, Playwright, real data, secrets, deploy, public endpoint, or external pilot.

## 5. Allowed Files

Allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_GS_T04_VF03_RECONCILIATION_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_GS_T04_VF03_RECONCILIATION_CLOSEOUT_2026_04_27.md
docs/S6_GS_T04_EXPERT_MODE_ENTRY_SKELETON_CLOSEOUT_2026_04_27.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

No other files are authorized.

## 6. Required Tests

Minimum gate:

```powershell
cd frontend
npm run test -- --run
npm run build
cd ..
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
git diff --check
```

## 7. HOLD Conditions

HOLD if:

- implementation requires files outside the allowed list;
- implementation needs final visual interpretation rather than anchors;
- implementation needs interactive switching, route, modal, drawer, settings, or backend action;
- implementation changes field authority, role authority, coverage authority, case state, `ActionMode`, fixture registry, adapter, validator, or `ResolvedSurfaceContext`;
- tests/build fail;
- Claude Code review raises a blocking finding;
- any mandatory external-review trigger fires.

## 8. Next Safe Action

Next safe automation action:

```text
OPEN_IN_T02_P3_READONLY_INBOX_VARIANT_SKELETON_LAUNCH
```
