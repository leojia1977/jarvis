# ECI/VFE 本地离线评审包（RC001）

## 评审边界

```text
Candidate: ECI_VFE_LOCAL_OFFLINE_RC_001
Source candidate: ECI_VFE_FIXTURE_RC001
Package: D:/产品设计/New folder/artifacts/local_demo_packages/eci-vfe-local-offline-rc-001
Zip: eci-vfe-local-offline-rc-001-review-package.zip
real_data=false
masked_real_data=false
live_qwen_api=false
live_connectors=false
production_writeback=false
customer_visible_output=false
push=false
```

## 评审入口

1. 先看 `SCREENSHOT_INDEX_中文.json` 的 4 张截图条目，确认 route/viewport/sha256。
2. 再看 `output_guard_scan.json`，确认 `status=PASS` 且 `blocking_finding_count=0`。
3. 再看 `chain_assessment.json` / `forecast_candidates.json` / `correlation_result.json`。
4. 最后对照 `package_manifest.json` 的文件哈希与安全类别。

## HOLD 条件

- 任何 boundary 字段不是 false
- output guard 不是 PASS
- 出现 raw payload/token/auth header/attacker-readable attack path
- manifest 缺失 sha256 / bytes / safety_class
