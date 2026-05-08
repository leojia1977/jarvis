# 部署边界

本结构包不授权以下事项：

- 使用真实数据或脱敏真实数据
- 调用 live Qwen/API
- 配置 API key、token、auth header 或 secret
- 调用 live connector
- 写回生产系统
- 发布客户可见输出
- 外部试点或生产上线

任何后续任务如需越过以上边界，必须创建新的可执行 Goal，并附带验收命令和 HOLD 条件。
