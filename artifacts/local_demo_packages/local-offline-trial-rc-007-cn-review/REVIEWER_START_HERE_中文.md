# SecuPilot 本地离线中文评审包 RC-007

## 评审范围

本包用于内部本地/离线中文评审。请先打开截图，再按页面入口复核 `/s1-trial` 和 `/s1-run`。

允许查看：

```text
中文优先的 S1 本地试用页面
中文优先的 S1 证据查看页面
metadata-only case summary
artifact manifest
safety scan summary
本地反馈预览
Qwen provider planning stub
```

不允许：

```text
真实数据
脱敏真实数据
live Qwen/API 调用
live connector
生产写回
客户可见发布/部署/输出
外部试点
生产上线
push
```

## 建议评审顺序

1. 查看 `screenshots/s1-trial-desktop.png` 和 `screenshots/s1-trial-mobile.png`。
2. 查看 `screenshots/s1-run-desktop.png` 和 `screenshots/s1-run-mobile.png`。
3. 核验 `evidence/final_status.json`、`evidence/case_summary.json`、`evidence/artifact_manifest.json`、`evidence/safety_scan.json`。
4. 对照 `REVIEWER_CHECKLIST_中文.md` 判断是否可进入下一轮内部本地试用。
5. 使用 `FEEDBACK_TEMPLATE_中文.md` 输出结论。

## 当前已知 UI 问题

P1/P2/P3 workbench 仍混有调试态控件、mock fixture、专家模式和产品试用内容。RC-007 只评审 S1 中文本地试用包，不代表 P1/P2/P3 主工作台已经达到客户试用级产品形态。
