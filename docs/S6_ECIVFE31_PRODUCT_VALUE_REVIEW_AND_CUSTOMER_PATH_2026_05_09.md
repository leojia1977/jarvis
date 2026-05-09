# S6 ECIVFE-31 Product Value Review And Customer Path

Date: 2026-05-09

## Decision

ECIVFE-31 is technically useful but not product-ready as a customer-facing page.

It proves that guard-passed ECI chain assessment can be rendered after `output_guard_scan.json` is PASS. However, the current `/eci-vfe-chain` surface is a raw validation page, not a SecuPilot product experience.

## Evidence Reviewed

- `docs/goals/GOAL-ECIVFE-31_CHAIN_INDICATOR_UI.md`
- `docs/S6_FAST_MVP_GOAL_ECIVFE_31_CHAIN_INDICATOR_UI_2026_05_08.md`
- `frontend/src/secupilot/eciVfe/EciChainIndicator.tsx`
- `frontend/src/secupilot/eciVfe/EciEvidenceGapPanel.tsx`
- `frontend/src/secupilot/eciVfe/eciVfeUiModel.ts`
- `artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-desktop.png`
- `artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-mobile.png`

## Product Value

ECI/VFE can add real product value if it answers:

- where the incident appears in the attack chain
- whether SecuPilot is confident or still conservative
- what evidence is missing
- how urgent the missing evidence is
- what the human should collect next
- why no automatic containment is authorized

This is aligned with the desired SecuPilot product direction: a security analysis and judgment assistant that hides complex reasoning in the background and gives the user a clear, useful next step.

## Current Gap

The current ECIVFE-31 page is not suitable as a customer-visible product page because:

- It is English-first.
- It displays fixture IDs such as `ECI-FIX-001` as the main headings.
- It uses raw implementation labels such as `Guard-passed local/offline fixture output`.
- It renders a long vertical list rather than a decision-oriented incident card.
- It is not integrated into the product homepage or incident workbench flow.
- It does not reuse the current SecuPilot visual language from the incident workbench.

This page should remain a validation artifact, not a customer entry route.

## Required Product Integration

ECI/VFE should be integrated behind the existing product path:

```text
产品首页
  -> 事件工作台
  -> AI 建议来源 / 攻击链判断
  -> ECI/VFE 解释
  -> 人工反馈提交
```

## Customer-Readable IA Mapping

| Current ECIVFE-31 concept | Product wording |
| --- | --- |
| ECI chain indicator | 攻击链判断 |
| Stage | 当前阶段判断 |
| Status | 当前研判状态 |
| Confidence | 可信度 |
| Evidence gaps | 还缺什么证据 |
| Urgency | 补证优先级 |
| Collection window | 建议补证窗口 |
| Fallback | 如果补不到证据，保持保守判断 |

## Next UI Requirement

For GOAL-ECIVFE-32 and the following product polish, ECI/VFE must not be exposed as a standalone technical page.

The recommended product placement is:

1. Incident workbench first screen:
   - add a compact `攻击链判断` card near the current conclusion and recommended action
   - show only the highest-value summary: stage, confidence, missing evidence, and human next step

2. AI advice source section:
   - include a folded `为什么这么判断` explanation
   - keep technical guard/output details hidden behind `技术对账`

3. Evidence detail:
   - show evidence gaps as operator-readable collection guidance
   - do not show raw logs, PoC, exploit steps, payloads, topology reachability, or attacker-readable paths

4. Feedback loop:
   - ask whether the attack-chain judgment is useful, accurate, and missing context
   - store feedback locally/offline only

## Customer Path For Next RC

The next customer-readable review path should be:

```text
/s1-trial
  -> 进入产品首页
  -> 打开事件工作台 /incident/CASE-2847
  -> 查看首屏结论、建议动作、可信边界
  -> 展开 AI 建议来源
  -> 查看攻击链判断 / ECI-VFE 摘要
  -> 提交本地反馈
```

## Automation Route

After GOAL-AUTO-04, automation should resume on:

1. `GOAL-ECIVFE-32_FORECAST_CARD_UI`
2. `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE`
3. RC-018 package that includes the incident-workbench customer path
4. Product homepage and incident-workbench polish

## Non-Authorization

This review does not authorize real data, masked-real data, live Qwen/API/connectors, production write-back, customer-visible publish/deploy/output, external pilot, production launch, autonomous containment/remediation, or attacker-readable ECI/VFE detail.
