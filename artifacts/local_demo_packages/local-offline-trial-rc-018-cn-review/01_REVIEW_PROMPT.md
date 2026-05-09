# RC018 Review Prompt

请以客户可读产品路径评审 `LOCAL_OFFLINE_TRIAL_RC_018_CN`，并确保：
- 只允许本地/离线
- 不使用真实数据或脱敏真实数据
- 不使用 live Qwen/API/connectors
- 不允许生产写回、客户可见发布、外部试点或生产上线
- ECI/VFE 只作为攻击链判断、风险预警摘要、缺失证据和补证窗口，不泄露 attacker-readable attack path
- 请重点判断它是否像产品解释，而不是裸验证页或证据包目录
