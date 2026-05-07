# SecuPilot RC-006 本地离线试用检查清单

## 必查项

| 检查项 | 期望 |
| --- | --- |
| `/s1-trial` 可以打开 | PASS |
| 页面为中文优先 | PASS |
| 证据 ID / artifact path / decision code 保持可对账 | PASS |
| 本地反馈预览不写入后端或 artifact | PASS |
| `customer_visible_output` | false |
| `production_writeback` | false |
| `live_qwen_api` | false |
| `live_connectors` | false |
| `safety_scan.summary.finding_count` | 0 |

## HOLD 条件

```text
页面无法打开
路径指向不存在的 artifact
反馈入口声称会写后端或提交外部系统
出现真实/脱敏真实数据
出现 secret/token/auth header
出现 live Qwen/API/connector 调用
出现客户可见发布、部署、外部试点或生产上线暗示
```
