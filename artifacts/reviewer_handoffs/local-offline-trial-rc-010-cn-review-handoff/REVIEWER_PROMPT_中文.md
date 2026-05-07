# 给 reviewer 的中文提示词

请对 SecuPilot `LOCAL_OFFLINE_TRIAL_RC_010_CN` 本地离线评审交接包做一次离线审查。

请按以下顺序检查：

1. 先读 `REVIEWER_START_HERE_中文.md` 和 `RC010_REVIEWER_START_HERE_中文.md`。
2. 核验 RC package manifest、screenshot safety scan、RC consistency check。
3. 打开四张 `/s1-trial` 和 `/s1-run` 截图，确认页面没有 P1/P2/P3、Mock Fixture、Expert Mode 或旧 RC 口径。
4. 打开 Qwen dry provider UI preview 截图，确认它只是 dry contract 预览，没有 live Qwen/API、connector、写回、自主动作或 API key。
5. 输出结论：

```text
PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL
PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
HOLD_FOR_UI_OR_PACKAGE_FIXES
NO_GO_FOR_CURRENT_PRODUCT_PATH
```

本评审不授权客户可见发布、部署、真实数据、live Qwen/API、connector、生产写回、外部试点或生产上线。
