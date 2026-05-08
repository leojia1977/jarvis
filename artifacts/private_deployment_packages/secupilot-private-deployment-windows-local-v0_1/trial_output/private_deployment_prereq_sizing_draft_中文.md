# SecuPilot 私有化部署前置条件与 Sizing 草案

Draft ID: `secupilot-private-deployment-windows-local-v0_1-private-deployment-prereq-sizing-draft`

Package ID: `secupilot-private-deployment-windows-local-v0_1`

Status: `DRAFT_READY_FOR_INTERNAL_PRODUCT_REVIEW`

## 一句话结论

已将反馈样本转成 Windows 前置依赖、资源 sizing 和模型接入路径草案，下一步可做本地 precheck 脚本。

## 来源反馈

- FB-SAMPLE-002 / security_manager: 希望下一版补充 Windows 前置依赖检查。
- FB-SAMPLE-003 / cto: 希望看到私有化部署资源需求和模型接入路径。

## Windows 前置依赖草案

- WIN-PREQ-01: Windows 本地执行环境 - 可运行本地 PowerShell 脚本的 Windows 工作站或 Windows Server 主机。
- WIN-PREQ-02: PowerShell 执行能力 - PowerShell 可运行本包内的本地 dry-run 脚本。
- WIN-PREQ-03: Python 启动器 - Python 启动器可执行本地 SecuPilot 包与报告生成命令。
- WIN-PREQ-04: 本地文件权限 - 当前用户可读取包文件，并可写入 trial_output 产物目录。

## 资源需求 / Sizing 草案

- SIZE-LOCAL-TRIAL: 本地离线评审试用，用于打开包、报告和截图 / CPU 2 vCPU draft / 内存 4 GB RAM draft / 磁盘 2 GB free local workspace draft / 说明：仅用于 dry-run 包和本地报告，不是生产 benchmark。
- SIZE-LAB-PILOT-DRAFT: 私有化实验室 dry-run，用于更大的 synthetic 包 / CPU 4 vCPU draft / 内存 8 GB RAM draft / 磁盘 10 GB free local workspace draft / 说明：任何客户试点或生产 sizing 结论前都需要后续 benchmark。
- SIZE-PRODUCTION-TBD: 未来私有化生产部署 / CPU TBD / 内存 TBD / 磁盘 TBD / 说明：本 Goal 不授权、不 benchmark、不声明生产规格。

## 模型接入路径草案

- MODEL-01: 当前 dry-run provider - 仅使用本地 fixture/provider dry-run 输出。
- MODEL-02: 云端 Qwen contract 模拟 - 在无 API key 条件下验证请求/响应形态、延迟状态、错误状态和回退 UI。
- MODEL-03: 私有化模型 connector 设计 - 定义模型 endpoint 配置未来放在哪里；secret 处理不在本草案内。
- MODEL-04: 未来 live 模型授权 - 需要单独 Goal 明确 API、数据、secret、网络和回滚边界。

## 阻塞点

- none

## 建议后续 Goal

- ACTION-01: 制作 Windows 本地前置依赖 precheck 脚本 -> GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT
- ACTION-02: 把 sizing 草案推进为可 benchmark 的资源报告 -> GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT
- ACTION-03: 把 dry-run 模型接入路径映射到客户可理解的配置流程 -> GOAL-MVP-80_MODEL_PROVIDER_SETUP_FLOW_DRY_RUN

## 边界

- 本草案不执行部署。
- 本草案不调用 live Qwen/API。
- 本草案不连接 live connector。
- 本草案不读取、保存或要求 secret/token/auth header。
- 本草案不使用真实数据或脱敏真实数据。
- 本草案不授权客户可见发布、外部试点或生产上线。
