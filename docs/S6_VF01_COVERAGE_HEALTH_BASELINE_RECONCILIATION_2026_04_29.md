# S6 VF-01 Coverage & Health Baseline Reconciliation 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `VF-01` |
| Title | Coverage & Health P0 main frame baseline reconciliation |
| Status | VF01_BASELINE_RECONCILED_READY_FOR_CH_T02_CHECKLIST |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Source folder | `D:\产品设计\secupilot0421\visual negative` |
| Source MD | `SecuPilot_VF-01_Coverage_Health_Main_Frame_v0.1.md` |
| Source HTML | `SecuPilot_VF-01_Coverage_Health_Main_Frame_v0.1.html` |
| Source PNG | `SecuPilot_VF-01_Coverage_Health_Main_Frame_v0.1.png` |

## 2. Decision

Decision:

```text
VF01_BASELINE_RECONCILED_READY_FOR_CH_T02_CHECKLIST
```

`VF-01` is accepted as the current semantic visual baseline for the Coverage & Health P0 frame.
The HTML remains a visual/interaction reference only; implementation must use the model contract,
existing `ResolvedSurfaceContext`, and governed frontend code, not copy static HTML into production.

## 3. Reconciled Anchors

Approved semantic anchors:

```text
coverage-health-root
current-coverage-level
field-presence-rate
join-health-rate
data-freshness-indicator
capability-tier-reference
field-switch-matrix
capability-package-list
ui-message-preview
missing-signal-notice
confidence-notice
escalation-hint
```

Required `ui_messages` rule:

```text
missing-signal-notice, confidence-notice, and escalation-hint must carry
data-message-source="ui_messages".
```

Forbidden DOM anchors:

```text
hardcoded-unlock-copy
frontend-generated-upgrade-copy
coverage-upgrade-prompt
real-data-sample-row
secret-or-connector-config
```

## 4. Boundary

This reconciliation does not authorize:

- backend/runtime/API/schema work;
- live `/health` or `/ready` source health;
- real data, anonymized real data, secrets, deploy, public endpoint, or external pilot;
- fixture registry, adapter, validator, or `ResolvedSurfaceContext` changes;
- coverage escalation, unlock copy, or frontend-created missing-signal explanations;
- final visual PASS beyond semantic frame anchors.

## 5. Next Safe Action

Next safe action:

```text
OPEN_CH_T02_COVERAGE_HEALTH_MAIN_FRAME_LAUNCH_CHECKLIST
```
