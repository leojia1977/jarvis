# SecuPilot 本地离线试用入口 RC-006

## 试用范围

本包只用于内部本地/离线试用。

允许查看：

```text
S1 本地离线试用页面
S1 证据查看页面
metadata-only case summary
artifact manifest
safety scan summary
reviewer feedback preview
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

## 启动方式

在 repo 根目录执行：

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\launch_s1_local_offline_trial.ps1
```

浏览器入口：

```text
http://127.0.0.1:4174/s1-trial
```

## 评审顺序

1. 打开 `/s1-trial`。
2. 按页面中的 5 步 walkthrough 检查 README、manifest、final status、safety scan 和截图。
3. 在页面的本地反馈预览区选择结论并填写备注。
4. 对照 `REVIEWER_CHECKLIST.md` 完成离线检查。
5. 将最终意见写入 `FEEDBACK_TEMPLATE.md` 对应格式，或提交到 governed review note。
