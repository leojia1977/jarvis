# SecuPilot 本地离线试用入口

Package ID: `secupilot-private-deployment-windows-local-v0_1`

本入口面向客户试用负责人、内部 reviewer 和交付同学，用于快速确认 SecuPilot 私有化交付包的本地打开方式、边界状态和下一步反馈路径。

## 先做什么

1. 双击 `START_SECUPILOT_LOCAL_TRIAL.cmd`。
2. 如果 Windows 安全提示拦截，请在 PowerShell 中运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\START_CUSTOMER_TRIAL.ps1
```

3. 打开生成的 `trial_output/customer_trial_status.json`。
4. 把终端输出和 `customer_trial_status.json` 交给内部 reviewer 或项目负责人。

## 这个入口会做什么

- 读取本包的 `package_manifest.json`。
- 执行 `scripts/VERIFY_BOUNDARIES.ps1`。
- 生成 `trial_output/customer_trial_status.json`。
- 打印本地离线试用状态。

## 这个入口不会做什么

- 不部署服务。
- 不启动生产系统。
- 不读取密钥。
- 不访问网络。
- 不调用 live Qwen/API。
- 不连接 live connector。
- 不写回生产。
- 不使用真实数据或脱敏真实数据。

## 通过标准

终端出现：

```text
LOCAL_TRIAL_ENTRY_READY
BOUNDARY_CHECK_PASS
```

并且 `trial_output/customer_trial_status.json` 中所有边界字段保持 `false`。
