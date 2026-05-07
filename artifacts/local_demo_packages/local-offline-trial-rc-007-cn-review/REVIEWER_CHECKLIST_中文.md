# RC-007 中文本地离线评审检查清单

## 必查项

| 检查项 | 期望 |
| --- | --- |
| `/s1-trial` 截图为中文优先 | PASS |
| `/s1-run` 截图为中文优先 | PASS |
| 桌面截图可读，无明显遮挡 | PASS |
| 手机截图可读，无明显遮挡 | PASS |
| 证据 ID / artifact path / decision code 保持可对账 | PASS |
| 本地反馈预览不写后端或 artifact | PASS |
| Qwen provider 处于 `qwen-cloud-disabled` | PASS |
| `customer_visible_output` | false |
| `production_writeback` | false |
| `live_qwen_api` | false |
| `live_connectors` | false |
| `safety_scan.summary.finding_count` | 0 |

## HOLD 条件

```text
截图无法打开
页面入口仍主要依赖英文说明才能理解
路径指向不存在的 artifact
反馈入口声称会写后端或提交外部系统
出现真实/脱敏真实数据
出现 secret/token/auth header
出现 live Qwen/API/connector 调用
出现客户可见发布、部署、外部试点或生产上线暗示
```

## 非阻塞但需记录

```text
P1/P2/P3 主 workbench 信息架构仍混乱
mock fixture / expert mode / role switcher 仍暴露在试用视图附近
S1 local trial 页面仍像证据台而不是正式产品首页
```
