# SecuPilot Reviewer Feedback Product Backlog

Generated at: 2026-05-07T08:13:50.947551Z

```text
candidate = LOCAL_OFFLINE_TRIAL_RC_012_CN
source_candidate = LOCAL_OFFLINE_TRIAL_RC_011_CN
reviewer_decision = PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
item_count = 4
customer_visible_or_deploy_go = false
```

## RFB-RC012-001: N1. /s1-run 首屏仍保留 candidate/run_id/data_mode 等技术对账字段；建议后续继续减少首屏 code 感，但当前不阻塞

```text
category = PACKAGE_CONSISTENCY
priority = P3
status = BACKLOG_OPEN
source_type = non_blocking_observation
```

Acceptance:

  - local/offline only
  - no real or masked-real data
  - no live Qwen/API/connectors
  - no production write-back
  - no customer-visible publish/deploy/output
  - RC consistency validator PASS
  - /s1-run App and Playwright smoke PASS

## RFB-RC012-002: N2. evidence/case_summary.json 中 UAT-19 synthetic title 含 P3 字样；截图中未出现，不构成 reviewer-facing 调试控件泄露。若要求包内全文无 P1/P2/P3，可在下一轮重命名该用例标题

```text
category = REVIEW_SCREENSHOT
priority = P3
status = BACKLOG_OPEN
source_type = non_blocking_observation
```

Acceptance:

  - local/offline only
  - no real or masked-real data
  - no live Qwen/API/connectors
  - no production write-back
  - no customer-visible publish/deploy/output
  - Playwright screenshot and screenshot safety validator PASS

## RFB-RC012-003: N3. package_manifest.json 未自引用；建议后续新增 outer_zip_manifest 或 manifest_self_sha256 做更强完整性闭环

```text
category = PACKAGE_CONSISTENCY
priority = P3
status = BACKLOG_OPEN
source_type = non_blocking_observation
```

Acceptance:

  - local/offline only
  - no real or masked-real data
  - no live Qwen/API/connectors
  - no production write-back
  - no customer-visible publish/deploy/output

## RFB-RC012-004: N01. 技术对账展开按钮加说明文字

```text
category = PRODUCT_COPY
priority = P2
status = BACKLOG_OPEN
source_type = next_round_suggestion
```

Acceptance:

  - local/offline only
  - no real or masked-real data
  - no live Qwen/API/connectors
  - no production write-back
  - no customer-visible publish/deploy/output


## Non-Authorization

```text
real_data = false
masked_real_data = false
live_qwen_api = false
live_connectors = false
production_writeback = false
customer_visible_output = false
push = false
```
