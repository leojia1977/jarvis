# S6 SH-T02 Dual Coverage Clamp Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 SH-T02 Dual Coverage Clamp Checklist 2026-04-28 |
| Status | CHECKLIST_GO_FOR_BOUNDED_IMPLEMENTATION |
| Date | 2026-04-28 |
| Ticket | `SH-T02` |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |

## 2. Source Evidence

| Source | Use |
| --- | --- |
| `docs/S6_VISUAL_BASELINE_HF_SH_01_02_VF14_RECONCILIATION_2026_04_28.md` | Records `HF-SH-01`, `HF-SH-02`, and `VF-14` v0.2 as PASS visual inputs. |
| `SecuPilot_HF-SH-01_HF-SH-02_Search_History_List_Frames_v0.2.md` | Defines dual coverage labels, clamp reason, missing-signal notice, and read-only approval-audit source anchor. |
| `SecuPilot_VF-14_Historical_Upgrade_Prohibited_Frame_v0.2.md` | Defines historical upgrade prohibition: current coverage cannot unlock fields absent from recorded history. |
| `docs/S6_SH_T03_PATCH_GATE_ISOLATED_LAUNCH_CHECKLIST_2026_04_27.md` | Existing clamp-first route semantics. |
| `docs/S6_SH_T01_HISTORICAL_LIST_ITEM_SKELETON_CLOSEOUT_2026_04_27.md` | Existing Search / History list-item skeleton. |

## 3. Allowed Files

Implementation may modify only:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

Docs/closeout may modify only S6 route, handoff, progress/risk, this checklist, and the SH-T02 closeout record.

The required pilot gate may refresh `releases/release_manifest.json` as a generated verification artifact only. Manual release-script or manifest semantics changes remain out of scope.

## 4. Required Behavior

The implementation must add or preserve:

- `dual-coverage-label-block`;
- `recorded-coverage-label`;
- `current-coverage-label`;
- `effective-visibility-label`;
- `clamp-reason`;
- `missing-signal-notice[data-message-source="ui_messages"]` when clamp/degradation notice is rendered;
- `historical-upgrade-blocked-notice` when current coverage is higher than recorded coverage;
- `view-approval-audit[data-source="history"][data-guard="role-source-data"]` as a read-only history source anchor only.

The effective visibility rule is:

```text
effective_visibility = min(recorded_case_coverage_level, current_customer_coverage_level)
```

## 5. Non-Goals

The implementation must not add:

- Search / History write actions;
- approval controls;
- AP mutation or `ActionMode` creation;
- P3 Manager approval-audit summary;
- route handoff payloads;
- backend/runtime/API/schema changes;
- fixture registry, fixture adapter, `ContextValidator`, or `ResolvedSurfaceContext` changes;
- real data, secrets, deploy, public endpoint, or external pilot behavior.

## 6. Required Tests

Run:

```text
npm test
npm run build
py -3 scripts/git_preflight.py --mode pilot
git diff --check
```

Focused assertions must prove:

- route/storage coverage injection cannot exceed recorded coverage;
- dual coverage labels are attached with recorded/current/effective values;
- historical upgrade blocked notice appears for current > recorded;
- read-only approval-audit source anchor carries `data-source="history"` and `data-guard="role-source-data"`;
- forbidden high-coverage fields remain unmounted.

## 7. Review Path

Claude Code focused review is required for implementation diffs before closeout.

Claude Web is not mandatory unless implementation touches authority behavior beyond the read-only SH-T02 clamp/list semantics.

## 8. HOLD Conditions

HOLD if implementation needs:

- files outside the allowed list;
- final visual styling or visual PASS claims;
- SH-T06 empty-state behavior;
- SH-T08 approval-audit source boundary behavior;
- AP/MV authority changes;
- backend/runtime/API/schema;
- fixture/adapter/validator/`ResolvedSurfaceContext`;
- real data, secrets, deploy, public endpoint, or external pilot.

## 9. Decision

```text
SH_T02_CHECKLIST_GO_FOR_BOUNDED_IMPLEMENTATION
```
