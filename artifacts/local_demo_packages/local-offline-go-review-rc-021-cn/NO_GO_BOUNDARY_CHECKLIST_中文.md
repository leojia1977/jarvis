# NO-GO Boundary Checklist

以下任一项命中即 NO_GO_SECURITY_BOUNDARY 或 HOLD：

- 出现 real data 或 masked-real data
- 出现 secret/token/auth header/raw payload/raw customer log/customer identifier
- 出现 exploit/PoC/payload/attacker-readable attack path/topology reachability 可利用细节
- 出现 live connector/live API/production deployment/production writeback 授权暗示
- 出现自动隔离/自动阻断/自动审批/自动关闭/自动修复暗示
- 出现建议发布/建议试点/建议客户使用
