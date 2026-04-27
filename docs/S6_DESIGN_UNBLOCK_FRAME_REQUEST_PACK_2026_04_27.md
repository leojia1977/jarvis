# S6 Design Unblock Frame Request Pack 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Design Unblock Frame Request Pack 2026-04-27 |
| Status | LOW_RISK_QUEUE_OUTPUT_DESIGN_REQUESTS |
| Queue item | `LR-07` |
| Date | 2026-04-27 |

This pack gives design a prioritized list of visual frame requests that unlock the most engineering work.

It requests visual treatment of already frozen semantics only. It does not request new product scope, new workflow, new data, final implementation, or visual PASS by itself.

## 2. Priority List

| Priority | Frame | Unblocks | Needed semantic anchors |
| ---: | --- | --- | --- |
| 1 | `VF-11` | `CD-T06` | `OBSERVATION_WINDOW` state-header treatment; read-only/return-to-pending semantics; no frontend timer authority. |
| 2 | `VF-12` | `CD-T06` | `APPROVED_PENDING_EXECUTION` state-header treatment; locked/read-only state; no action controls. |
| 3 | `VF-13` | `CD-T06` | `CLOSED` state-header treatment; terminal-state expression; no reopen or hidden workflow. |
| 4 | `VF-01` | `CH-T02`, later `CH-T04` | Coverage & Health visual treatment; honest unavailable/degraded states; no live backend health claim. |
| 5 | `HF-SH-01` / `HF-SH-02` / `VF-08` / `VF-14` | `SH-T02`, `SH-T06`, `SH-T09` | Search/History list/detail/focus semantics; recorded vs current coverage; structural empty vs degraded empty. |

## 3. CD-T06 Frame Details

`VF-11`, `VF-12`, and `VF-13` should answer:

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

## 4. Coverage & Health Frame Details

`VF-01` should answer:

- page region structure for Coverage & Health;
- how coverage ceiling and visible coverage are shown;
- how unavailable source health is represented without pretending live backend status;
- how `ui_messages` can later render safely;
- which anchors are skeleton-safe versus final visual styling.

Do not introduce live `/health`, `/ready`, backend telemetry, or public readiness claims.

## 5. Search/History Frame Details

`HF-SH-01`, `HF-SH-02`, `VF-08`, and `VF-14` should answer:

- list item hierarchy;
- detail/focus scope treatment;
- recorded coverage vs current visible coverage;
- structural empty state vs degraded empty state;
- write CTA absence or disabled treatment;
- P3 approval-audit source display boundary.

Do not introduce write actions, approval controls, route handoff, or raw host evidence.

## 6. Suggested Message To Design

```text
Please prioritize VF-11/VF-12/VF-13, then VF-01, then HF-SH-01/HF-SH-02/VF-08/VF-14. These requests are for visual treatment of already frozen semantics only. They should include stable anchors/test-id guidance where possible and must not add new workflow, data, backend, or action scope.
```

