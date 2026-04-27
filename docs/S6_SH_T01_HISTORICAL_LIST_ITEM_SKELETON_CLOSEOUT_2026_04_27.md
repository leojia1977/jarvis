# S6 SH-T01 Historical List Item Skeleton Closeout 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 SH-T01 Historical List Item Skeleton Closeout 2026-04-27 |
| Ticket | `SH-T01` |
| Scope | `Historical list item semantic skeleton and test ids only` |
| Status | IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Launch checklist | `docs\S6_SH_T01_HISTORICAL_LIST_ITEM_SKELETON_LAUNCH_CHECKLIST_2026_04_27.md` |
| Jira issue | `SCRUM-40` |

## 2. Decision

Decision:

```text
SH_T01_VISUAL_SKELETON_IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED
```

`SH-T01` is implemented as a semantic skeleton. Final `HF-SH-01` / `VF-08` visual styling and visual PASS remain pending.

## 3. Implemented Behavior

Implemented:

- a historical case list item skeleton inside the existing Search / History surface;
- `data-list-item-context="summary-only"`, `data-detail-context-authority="case-route"`, `data-effective-visibility-owned-by="case-detail"`, `data-handoff-state="not-implemented"`, `data-visual-state="skeleton"`, and `data-frame-state="hf-sh-01-vf-08-pending"` anchors;
- lightweight list fields for case id, verdict, summary snippet, timestamp availability, recorded coverage, and current visible coverage;
- regression coverage proving the list item is summary-only, keeps detail visibility out of the list layer, has no route-handoff implementation, and attaches no write or approval controls.

## 4. Implemented Files

Implemented files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

Governance / closeout files:

```text
docs/S6_SH_T01_HISTORICAL_LIST_ITEM_SKELETON_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_SH_T01_HISTORICAL_LIST_ITEM_SKELETON_CLOSEOUT_2026_04_27.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

## 5. Gate Evidence

Gate evidence:

```text
frontend tests: PASS, 66 tests
frontend build: PASS
backend guard: PASS, 42 tests
git diff --check: PASS with Windows line-ending warnings only
Claude Code focused review: PASS
Jira cloud sync: SCRUM-40 transitioned to 已完成
```

## 6. Non-Goals Preserved

This closeout does not authorize or implement:

- final `HF-SH-01` / `VF-08` visual styling or visual PASS;
- `SH-T02` dual coverage visual treatment, `SH-T04`, `SH-T06`, `SH-T07`, `SH-T08`, or `SH-T09`;
- case-detail route handoff, focus-route handoff, deep links, or detail permission decisions;
- evidence timeline, blast radius, host raw evidence, approval controls, close controls, or ActionMode;
- fixture registry changes, fixture adapter changes, validator changes, or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema changes;
- Storybook, Playwright, real data, anonymized real data, secrets, deploy, public endpoint, or external pilot.

## 7. SWE Status

SWE was not used for this product patch. Current automation remains Codex-led implementation with Claude Code focused review. SWE remains disabled unless a later exact ticket explicitly names SWE with exact files, tests, rollback, reviewer, and HOLD conditions.

## 8. Next Safe Action

Next safe automation action:

```text
OPEN_CH_T01_COVERAGE_HEALTH_PAGE_SKELETON_LAUNCH
```
