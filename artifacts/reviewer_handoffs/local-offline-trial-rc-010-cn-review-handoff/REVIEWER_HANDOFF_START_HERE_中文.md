# SecuPilot RC-010 中文本地离线评审交接包

## 先读这个

本交接包用于把 RC-010 本地离线评审材料一次性交给 reviewer。

```text
candidate = LOCAL_OFFLINE_TRIAL_RC_010_CN
source_candidate = LOCAL_OFFLINE_TRIAL_RC_009_CN
rc_package_zip = local-offline-trial-rc-010-cn-review-package-20260507.zip
review_mode = LOCAL_OFFLINE_REVIEW_ONLY
customer_visible_or_deploy_go = false
```

## 推荐评审顺序

1. 打开 `reviewer_entry/RC010_REVIEWER_START_HERE_中文.md`。
2. 打开 `reviewer_entry/RC010_REVIEWER_CHECKLIST_中文.md`。
3. 核对 `validation/screenshot_safety_scan.json` 和 `validation/rc_consistency_check.json`。
4. 查看 `qwen_preview/s1-qwen-dry-provider-preview.png`，确认 dry provider 只是本地 UI 预览。
5. 如需完整 RC 包，解压 `rc_package/local-offline-trial-rc-010-cn-review-package-20260507.zip`。

## 明确不授权

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
