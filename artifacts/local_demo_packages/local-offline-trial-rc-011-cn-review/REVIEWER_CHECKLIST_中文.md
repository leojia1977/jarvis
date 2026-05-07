# RC-011 中文本地离线评审检查清单

## 必查项

| 检查项 | 期望 |
| --- | --- |
| `/s1-trial` 截图为中文优先 | PASS |
| `/s1-run` 截图为产品化结果页，不是证据台 | PASS |
| 截图中 candidate 为 `LOCAL_OFFLINE_TRIAL_RC_011_CN` | PASS |
| 截图中 source candidate 为 `LOCAL_OFFLINE_TRIAL_RC_010_CN` | PASS |
| 截图中 package path 指向 `local-offline-trial-rc-011-cn-review` | PASS |
| 截图中不再出现上一轮旧版本 reviewer package 口径 | PASS |
| 桌面截图不显示 P1/P2/P3 / Mock Fixture / Expert Mode 调试控件 | PASS |
| 手机截图不显示 P1/P2/P3 / Mock Fixture / Expert Mode 调试控件 | PASS |
| 证据 ID / artifact path / decision code 保持可对账 | PASS |
| 本地评审结论预览不写后端或 artifact | PASS |
| `customer_visible_output` | false |
| `production_writeback` | false |
| `live_qwen_api` | false |
| `live_connectors` | false |
| `safety_scan.summary.finding_count` | 0 |
| `validation/screenshot_safety_scan.json` 阻塞项 | 0 |

## HOLD 条件

```text
截图无法打开
页面入口仍主要依赖英文说明才能理解
/s1-run 仍像证据台而不是产品结果页
页面仍显示上一轮旧版本 reviewer package 口径
路径指向不存在的 artifact
反馈入口声称会写后端或提交外部系统
出现真实/脱敏真实数据
出现 secret/token/auth header
出现 live Qwen/API/connector 调用
出现客户可见发布、部署、外部试点或生产上线暗示
```
