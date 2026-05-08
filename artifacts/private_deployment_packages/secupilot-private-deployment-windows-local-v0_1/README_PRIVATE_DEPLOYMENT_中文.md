# SecuPilot 私有化部署包结构

Package ID: `secupilot-private-deployment-windows-local-v0_1`

本包是 Windows/local-first 私有化部署结构草案，并包含一个本地离线试用入口。当前仅用于安装路径、交付结构和 dry-run 启动体验核验。

## 当前状态

- 结构包：YES
- 实际部署：NO
- 真实数据：NO
- 脱敏真实数据：NO
- live Qwen/API：NO
- live connectors：NO
- 生产写回：NO
- 客户可见发布：NO

## 推荐阅读顺序

1. `CUSTOMER_TRIAL_START_HERE_中文.md`
2. `START_SECUPILOT_LOCAL_TRIAL.cmd`
3. `docs/WINDOWS_LOCAL_FIRST_STRUCTURE_中文.md`
4. `docs/DEPLOYMENT_BOUNDARIES_中文.md`
5. `configs/secupilot.env.template`
6. `configs/provider.dry-run.json`
7. `scripts/VERIFY_BOUNDARIES.ps1`

## 说明

`START_SECUPILOT_LOCAL_TRIAL.cmd` 和 `scripts/START_CUSTOMER_TRIAL.ps1` 只生成本地 dry-run 状态，不启动生产服务，不读取密钥，不访问网络。
