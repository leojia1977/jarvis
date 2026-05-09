# SecuPilot RC-018 Reviewer Feedback Product Backlog

Generated at: 2026-05-09T05:01:51Z

```text
candidate = LOCAL_OFFLINE_TRIAL_RC_018_CN
source_candidate = LOCAL_OFFLINE_TRIAL_RC_017_CN
reviewer_decision = PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
item_count = 5
open_item_count = 3
closed_item_count = 2
customer_visible_or_deploy_go = false
```

## RFB-RC018-001: Move engineering annex terms into internal validation or rewrite as local/offline synthetic metadata validation

```text
category = PACKAGE_ANNEX_COPY
priority = P2
status = BACKLOG_OPEN
source_type = non_blocking_observation
maps_to_goal = GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH
```

Acceptance:

  - local/offline only
  - no real or masked-real data
  - no live Qwen/API/connectors
  - no production write-back
  - no customer-visible publish/deploy/output
  - customer-facing package does not foreground `qwen_fact_bundle`, `source_payload`, `provider_decision_hint`, or `provider = fixture`

## RFB-RC018-002: Make deployment and remediation wording more conservative

```text
category = UI_COPY
priority = P1
status = BACKLOG_OPEN
source_type = non_blocking_observation
maps_to_goal = GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH
```

Acceptance:

  - `查看部署准备` is changed to `查看本地接入准备`
  - `隔离 finance-042 并锁定凭据` is changed to `待复核：finance-042 隔离与凭据锁定建议`
  - local/offline and human-review boundaries remain visible
  - no autonomous action, write-back, deploy, or customer-visible output is implied

## RFB-RC018-003: Add mobile incident scrolled-state screenshot in next package

```text
category = REVIEW_SCREENSHOT
priority = P2
status = BACKLOG_OPEN
source_type = non_blocking_observation
maps_to_goal = GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH
```

Acceptance:

  - package includes one mobile incident scrolled-state screenshot showing conclusion cards, trusted boundary, and recommended action
  - screenshot safety scan covers the new screenshot
  - no real or masked-real data
  - no live Qwen/API/connectors
  - no production write-back

## RFB-RC018-004: Preserve AI advice source default folded behavior

```text
category = REGRESSION_GUARD
priority = P3
status = BACKLOG_CLOSED
source_type = accepted_behavior
maps_to_goal = GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH
```

Resolution:

```text
AI advice source default folded behavior is accepted in RC-018 and should be preserved as a regression check in the next package.
```

## RFB-RC018-005: Preserve defensive ECI/VFE product framing

```text
category = REGRESSION_GUARD
priority = P3
status = BACKLOG_CLOSED
source_type = accepted_behavior
maps_to_goal = GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH
```

Resolution:

```text
ECI/VFE framing is accepted in RC-018 and should remain defensive: no reusable attack path, payload, PoC, exploit steps, or topology reachability.
```

## Non-Authorization

```text
real_data = false
masked_real_data = false
live_qwen_api = false
live_connectors = false
production_writeback = false
customer_visible_output = false
external_pilot = false
production_launch = false
push = false
```
