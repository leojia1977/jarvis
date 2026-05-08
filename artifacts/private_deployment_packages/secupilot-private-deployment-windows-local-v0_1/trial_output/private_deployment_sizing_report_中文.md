# SecuPilot 私有化部署 Sizing 报告

Report ID: `secupilot-private-deployment-windows-local-v0_1-private-deployment-sizing-report`

Package ID: `secupilot-private-deployment-windows-local-v0_1`

Status: `SIZING_DRAFT_READY_NOT_BENCHMARKED`

## 一句话结论

本地 precheck 已通过；当前 sizing 仅为私有化试用与实验室 dry-run 草案，不是生产 benchmark 或客户试点规格。

## 本机 Precheck 结果

- WIN-PREQ-01: Windows 本地执行环境 = PASS (platform=Win32NT)
- WIN-PREQ-02: PowerShell 执行能力 = PASS (powershell_version=5.1.26100.8115)
- WIN-PREQ-03: Python 启动器 = PASS (Python 3.14.2)
- WIN-PREQ-04: 本地文件权限 = PASS (trial_output writable)

## Sizing 档位

- SIZE-LOCAL-TRIAL: 本地离线评审试用，用于打开包、报告和截图 / CPU 2 vCPU draft / 内存 4 GB RAM draft / 磁盘 2 GB free local workspace draft / 状态：NOT_BENCHMARKED_DRAFT_ONLY / 说明：仅用于 dry-run 包和本地报告，不是生产 benchmark。
- SIZE-LAB-PILOT-DRAFT: 私有化实验室 dry-run，用于更大的 synthetic 包 / CPU 4 vCPU draft / 内存 8 GB RAM draft / 磁盘 10 GB free local workspace draft / 状态：NOT_BENCHMARKED_DRAFT_ONLY / 说明：任何客户试点或生产 sizing 结论前都需要后续 benchmark。
- SIZE-PRODUCTION-TBD: 未来私有化生产部署 / CPU TBD / 内存 TBD / 磁盘 TBD / 状态：NOT_BENCHMARKED_DRAFT_ONLY / 说明：本 Goal 不授权、不 benchmark、不声明生产规格。

## 假设条件

- 当前仅覆盖 local/offline private deployment package 与报告生成链路。
- local trial 档位只用于打开包、运行本地脚本、查看报告和截图。
- lab dry-run 档位仍需后续 benchmark 才能用于客户试点或生产 sizing 判断。
- production 档位保持 TBD，不在本 Goal 内授权或声明。

## 非生产 Caveat

- Not a production benchmark.
- Not a customer pilot sizing claim.
- Not a deployment authorization.
- No live Qwen/API/connectors were used.
- No real or masked-real data was used.

## 后续动作

- ACTION-01: 为实验室档位制作 benchmark dry-run harness -> GOAL-MVP-80_MODEL_PROVIDER_SETUP_FLOW_DRY_RUN
- ACTION-02: 把 precheck 与 sizing report 汇入私有化包入口说明 -> GOAL-MVP-81_PRIVATE_DEPLOYMENT_PACKAGE_REFRESH_WITH_PRECHECK

## 边界

- 本报告不执行部署。
- 本报告不做生产 benchmark。
- 本报告不声明客户试点或生产规格。
- 本报告不调用 live Qwen/API。
- 本报告不连接 live connector。
- 本报告不读取、保存或要求 secret/token/auth header。
- 本报告不使用真实数据或脱敏真实数据。
