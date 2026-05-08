# Claude Web Review Prompt: UX-01 Incident Workbench Main Path

请作为 SecuPilot 产品 / 安全运营工作台设计评审者，评审本地离线页面 `/incident/CASE-2847` 的两张截图：

- `artifacts/product_experience/ux01/incident-product-desktop.png`
- `artifacts/product_experience/ux01/incident-product-mobile.png`

评审范围只限本地离线、合成案例、无真实数据、无 live Qwen/API、无连接器、无生产写回、无客户发布。

重点评审：

1. 首页之后进入这个深度页面，客户是否会理解这是 SecuPilot 的事件工作台主路径，而不是证据台或调试台。
2. 一线工程师、经理、CTO 是否能在第一屏理解：
   - SecuPilot 判断了什么
   - 现在建议做什么
   - 为什么可信
   - 还有哪些不确定性
   - 当前哪些动作不会自动执行
3. 页面是否延续既有产品方向：事件队列、结论优先、证据折叠、时间线、建议动作、人工确认边界。
4. 是否仍有调试感或内部实现泄露，例如 `P1`、`P2`、`P3`、`Mock Fixture`、`Expert Mode`、旧 RC 口径、raw payload、token、auth header。
5. 是否需要在下一轮继续调整信息架构、视觉密度、中文表达或移动端可读性。

请输出：

```text
Decision:
  PASS | PASS_WITH_NOTES | HOLD_FOR_UI_FIXES

Findings:
  F1 ...

Non-blocking notes:
  N1 ...

Next suggested product Goal:
  ...
```
