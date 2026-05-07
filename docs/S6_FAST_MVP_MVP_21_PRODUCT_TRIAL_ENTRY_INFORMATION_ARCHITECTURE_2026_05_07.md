# S6 Fast MVP MVP-21 Product Trial Entry Information Architecture 2026-05-07

## 1. Decision

```text
MVP_21_PRODUCT_TRIAL_ENTRY_INFORMATION_ARCHITECTURE_IMPLEMENTED
CUSTOMER_VISIBLE_OR_DEPLOY_GO = NOT_AUTHORIZED
```

## 2. Product Change

`/s1-trial` now presents a product-style local trial entry before exposing audit details:

```text
primary title: SecuPilot 本地离线试用中心
entry flow: 打开本地试用 -> 核验评审材料 -> 记录本地反馈
material status: 中文入口 / 检查清单 / 反馈模板 / 截图与证据
technical paths: moved under 技术对账信息
debug controls: P1/P2/P3, Mock Fixture, Expert Mode remain hidden in S1 reviewer routes
```

## 3. Why

RC-007 and the user screenshot showed the page still looked like an evidence console. MVP-21 reduces the reviewer-facing cognitive load without removing metadata accountability.

## 4. Verification

```text
frontend: npm run test -- src/App.test.tsx = PASS
frontend: npm run build = PASS
frontend: npx playwright test tests/e2e/s1-artifact-viewer.spec.ts = PASS
git diff --check = PASS
```

## 5. Non-Authorization

This MVP-21 change does not authorize:

```text
real data
masked-real data
live Qwen/API calls
live connectors
production connectors
production write-back
customer-visible publish/deploy/output
external pilot execution
production launch
credential handling
push
```
