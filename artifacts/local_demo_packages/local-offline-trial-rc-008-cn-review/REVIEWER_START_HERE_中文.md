# SecuPilot 本地离线中文评审包 RC-008

## 本轮修复目标

RC-008 用于修复 RC-007 中文包的版本与路径不一致问题。

本轮所有 reviewer-facing 口径统一为：

```text
Candidate: LOCAL_OFFLINE_TRIAL_RC_008_CN
Source candidate: LOCAL_OFFLINE_TRIAL_RC_007_CN
Package: artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review
Zip: local-offline-trial-rc-008-cn-review-package-20260507.zip
```

## 评审范围

本包只用于内部本地/离线中文评审。

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

## UI 说明

本轮截图使用 reviewer clean mode：`/s1-trial` 与 `/s1-run` 默认隐藏 P1/P2/P3 role switcher、Mock Fixture Phase、Mock Redline Fixture 与 Expert Mode 调试控件。

这只代表本地离线 reviewer 入口已收敛，不代表完整 P1/P2/P3 主 workbench 已达到客户试用形态。
