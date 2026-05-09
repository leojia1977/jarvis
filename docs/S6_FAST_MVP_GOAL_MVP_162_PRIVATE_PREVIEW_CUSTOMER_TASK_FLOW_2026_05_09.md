# S6 Fast MVP GOAL-MVP-162 Private Preview Customer Task Flow

Date: 2026-05-09

Goal: GOAL-MVP-162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW

Decision: PASS

## Scope

把 `/s1-trial` 的私有预览入口明确成“工程师/经理/CTO”客户任务流，修正 stale RC 文案，并保持本地离线边界与无调试控件暴露。

## Executable Object Delivered

```text
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
```

## Files Changed

```text
docs/goals/GOAL-MVP-162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW.md
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/S6_FAST_MVP_GOAL_MVP_162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW_2026_05_09.md
```

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW.md
```

Result: PASS.

```text
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
```

Result: PASS, 63 tests passed.

```text
Set-Location -LiteralPath frontend; npm run build
```

Result: PASS, Vite production build completed.

```text
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
```

Result: PASS, 8 tests passed.

```text
git -c core.quotepath=false diff --check
```

Result: PASS（仅有 pre-existing picker 文件和行尾转换 warning）。

## HOLD Condition Check

- `customer task flow exposes P1/P2/P3, Mock Fixture, Expert Mode, or stale RC wording`: PASS（仍保留禁止断言；首页当前包文案更新为 RC-019）。
- `first screen is dominated by evidence paths instead of product tasks and next actions`: PASS（首页保持任务流入口与 next actions 为主）。
- `engineer, manager, or CTO path is missing`: PASS（角色入口明确包含工程师、经理、CTO）。
- `frontend unit/build/playwright fails twice in the same way`: PASS（全部一次通过）。
- `scope expands beyond listed files`: PASS（Playwright 生成截图证据已回滚，不纳入提交）。

## Automated Review Status

```text
Tool: not executed
Status: NOT_RUN
Reason: deterministic frontend test/build/playwright acceptance chain already complete
```

## Safety and Boundaries

- real_data=false
- masked_real_data=false
- live_qwen_api=false
- live_connectors=false
- production_writeback=false
- customer_visible_output=false
- push=false

## Next Suggested Goal

提交后重新运行 picker，继续执行下一条私有预览产品加速 Goal。
