# SecuPilot 本地离线中文评审包 RC-020

## 本轮目标

RC-020 用于验证本地离线试用包、产品化结果页和机器验证证据是否保持一致。

本轮所有 reviewer-facing 口径统一为：

```text
Candidate: LOCAL_OFFLINE_TRIAL_RC_020_CN
Source candidate: LOCAL_OFFLINE_TRIAL_RC_019_CN
Package: artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review
Zip: local-offline-trial-rc-020-cn-review-package-20260508.zip
```

## 评审范围

本包只用于内部本地/离线中文评审。

允许查看：

```text
中文优先的 S1 本地试用页面
中文优先的 S1 试用结果页面
metadata-only case summary
artifact manifest
safety scan summary
本地评审结论预览
离线评审交接材料
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
2. 查看 `screenshots/s1-run-desktop.png` 和 `screenshots/s1-run-mobile.png`，重点判断它是否像产品结果页，而不是证据台。
3. 查看 `screenshots/s1-run-first-load-folded-desktop.png`，确认 AI 建议来源在首屏未交互状态下保持折叠态证据。
4. 核验 `evidence/final_status.json`、`evidence/case_summary.json`、`evidence/artifact_manifest.json`、`evidence/safety_scan.json`。
5. 对照 `REVIEWER_CHECKLIST_中文.md` 判断是否可进入下一轮内部本地试用。
6. 使用 `FEEDBACK_TEMPLATE_中文.md` 输出结论。
