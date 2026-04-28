# S6 Design Unblock Frame Request Pack 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Design Unblock Frame Request Pack 2026-04-27 |
| Status | LOW_RISK_QUEUE_OUTPUT_DESIGN_REQUESTS_UPDATED_2026_04_28 |
| Queue item | `LR-07` |
| Date | 2026-04-27 |

This pack gives design a prioritized list of visual frame requests that unlock the most engineering work.

It requests visual treatment of already frozen semantics only. It does not request new product scope, new workflow, new data, final implementation, or visual PASS by itself.

## 2. Priority List

| Priority | Frame | Unblocks | Needed semantic anchors |
| ---: | --- | --- | --- |
| 1 | `VF-12` | `AP-T07`, `CD-T06` | `APPROVED_PENDING_EXECUTION` state-header treatment; locked/read-only state; no action controls. |
| 2 | `VF-11` | `AP-T06`, `CD-T06` | `OBSERVATION_WINDOW` state-header treatment; read-only/return-to-pending semantics; no frontend timer authority. |
| 3 | `VF-13` | `CD-T06`, `CD-T07` | `CLOSED` state-header treatment; terminal-state expression; no reopen or hidden workflow. |
| 4 | `HF-SH-01` | `SH-T01`, `SH-T02` | Normal Search/History list item hierarchy; recorded vs current visible coverage anchors. |
| 5 | `HF-SH-02` | `SH-T02`, `SH-T06` | Degraded/empty Search/History treatment; structural empty vs degraded empty. |
| 6 | `VF-14` | `SH-T02`, `SH-T09` | Current-greater-than-recorded upgrade prohibition; visible clamp-first affordance. |
| 7 | `VF-01` | `CH-T02`, later `CH-T04` | Sprint 4 Coverage & Health visual treatment; honest unavailable/degraded states; no live backend health claim. |
| 8 | `VF-08` | Pending confirmation | Likely deprecated as a duplicate of `HF-SH-01`; do not schedule as an independent frame unless design redefines it. |

## 3. CD-T06 Frame Details

`VF-12`, `VF-11`, and `VF-13` should answer, in that priority order:

- where the state header appears in Case Detail;
- how `OBSERVATION_WINDOW`, `APPROVED_PENDING_EXECUTION`, and `CLOSED` differ visually;
- how read-only/locked/terminal semantics are represented without creating controls;
- how missing or unavailable state information degrades honestly;
- which test ids or visual anchors engineering should attach.

Do not introduce:

- approve/reject/delay/observe controls;
- state migration;
- countdown-driven state change;
- hidden reopen behavior;
- backend or real-data dependency.

## 4. Search/History Frame Details

`HF-SH-01`, `HF-SH-02`, and `VF-14` should answer:

- list item hierarchy;
- detail/focus scope treatment;
- recorded coverage vs current visible coverage;
- structural empty state vs degraded empty state;
- current-greater-than-recorded upgrade prohibition;
- write CTA absence or disabled treatment;
- P3 approval-audit source display boundary.

Do not introduce write actions, approval controls, route handoff, or raw host evidence.

`VF-08` is pending confirmation and likely deprecated. The current visual kickoff tracker does not carry an independent `VF-08` row; treat it as removed unless design explicitly redefines it as a separate frame.

## 5. Coverage & Health Frame Details

`VF-01` should answer before Sprint 4:

- page region structure for Coverage & Health;
- how coverage ceiling and visible coverage are shown;
- how unavailable source health is represented without pretending live backend status;
- how `ui_messages` can later render safely;
- which anchors are skeleton-safe versus final visual styling.

Do not introduce live `/health`, `/ready`, backend telemetry, or public readiness claims.

## 6. Suggested Message To Design

```text
Please prioritize VF-12 -> VF-11 -> VF-13, then HF-SH-01 -> HF-SH-02 -> VF-14 before Sprint 3A, and VF-01 before Sprint 4. Treat VF-08 as pending confirmation / likely deprecated unless design redefines it as an independent frame. These requests are for visual treatment of already frozen semantics only. They should include stable anchors/test-id guidance where possible and must not add new workflow, data, backend, or action scope.
```
