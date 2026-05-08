# SecuPilot 私有化部署包结构

Package ID: `secupilot-private-deployment-windows-local-v0_1`

本包是 Windows/local-first 私有化部署结构草案，仅用于内部安装路径和交付结构核验。

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

1. `docs/WINDOWS_LOCAL_FIRST_STRUCTURE_中文.md`
2. `docs/DEPLOYMENT_BOUNDARIES_中文.md`
3. `configs/secupilot.env.template`
4. `configs/provider.dry-run.json`
5. `scripts/VERIFY_BOUNDARIES.ps1`

## 说明

`scripts/START_LOCAL_DRY_RUN.ps1` 只打印 dry-run 状态，不启动生产服务，不读取密钥，不访问网络。
