# S6 MVP-67 PRD Role Mapping And Product Home IA

Date: 2026-05-08

Status: MVP67_PRD_ALIGNMENT_READY

Scope: docs-only PRD alignment for the MVP-67 product home implementation.

This file answers only three questions:

1. How PRD user roles map to customer-facing product-home entries.
2. How internal P1/P2/P3 surfaces map to customer-visible information architecture.
3. What the MVP-67 first screen should show and should not show.

## Source References

- `docs/SPRINT3_PRD.md`
- `docs/S3B_CASE_EXPERIENCE_PRD.md`
- `docs/SPRINT4_PRD.md`
- `docs/SPRINT5_PRD.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/PRODUCT_STATE.md`

## Jarvis / Lao Jia Clarification

Exact Chinese role names `老贾` and `贾维斯` were not found in the repo PRD files checked for this alignment.

`Jarvis` appears in two different meanings:

- Product capability / assistant output: passive hunt planner, `hunt_plan`, case embedding, and the case-level `Jarvis Plan`.
- Governance or authorization actor: Human/Jarvis decision owner, delegated approver, or product-governance reviewer.

MVP-67 should not treat `老贾` / `Jarvis` as a customer user role unless a later PRD amendment explicitly defines that role. For the product home, the correct mapping is:

```text
SecuPilot / Jarvis / Lao Jia = security analysis assistant persona and reasoning output,
not a customer role with separate permissions.
```

If the product owner wants `老贾` to become a named customer-facing assistant persona, the UI may use it as copy, but the PRD should record it as a product persona rather than a user role.

## PRD Roles To Product Home Entries

| PRD role | Customer-facing home entry | First question this entry answers | MVP-67 treatment |
| --- | --- | --- | --- |
| `L1 analyst` | `一线研判` | 我现在最应该先看哪件事? | Show a low-cognitive-load incident summary, current conclusion, and next safe action. |
| `L2 analyst` | `深度分析` | 为什么这么判断, 证据和缺口在哪里? | Show evidence chain, pivots, degraded visibility, and assistant reasoning plan behind a clear summary. |
| `SOC manager` | `管理审阅` | 这件事是否需要确认, 延迟, 观察, 或拒绝? | Show manager-readable summary, approval state, audit summary, and non-destructive decision language. |
| `Security engineer` | `部署与集成` | 这个试用包能否稳定运行, 后续怎么接入? | Show local/offline run status, package readiness, integration assumptions, and dry provider path. |
| `Operator` | `部署与集成` | 如何启动, 验证, 交付证据, 处理异常? | Share the same deployment entry with operational runbook, launcher, report, and HOLD path. |
| `Product/review owner` | `试用结论` / `管理审阅` | 当前是否可以进入下一轮内部试用? | Show PASS/HOLD conclusion, reviewer notes, open backlog, and next unlock. |
| CTO / CISO reader | `管理审阅` executive lens | 风险、价值、可信边界、下一步投入是什么? | Serve as an executive overlay on manager view, not as a separate internal P-label surface. |
| SecuPilot / Jarvis / Lao Jia | Assistant persona | 系统帮我判断了什么, 下一步建议是什么, 为什么可信? | Present as the product's digital security analyst assistant, not as a customer permission role. |

## P1 / P2 / P3 To Customer-Facing IA

P1/P2/P3 are internal implementation and model-contract labels. They should not appear as primary customer-facing navigation, homepage labels, reviewer-clean screenshots, or package handoff copy.

| Internal surface | Customer-facing name | Customer should understand it as | Visible behavior |
| --- | --- | --- | --- |
| P1 / L2 Case Detail | `事件研判` | SecuPilot has analyzed one security event and explains what happened, why it matters, what to do next, and what evidence is missing. | Conclusion first, evidence folded, gaps explicit, no approval authority. |
| P2 / Approval Surface | `人工确认与处置建议` | The system recommends a human-in-the-loop decision, but does not execute destructive or production actions. | Approve, delay, observe, reject language may exist only as non-destructive review state unless separately authorized. |
| P3 / Manager View | `风险总览` / `管理审阅` | A manager can understand risk, attention items, audit posture, and decision status without reading technical evidence tables. | Read-only management summary, no case-action buttons, no hidden P2 component reuse. |

Customer-facing IA should therefore group the product home around:

1. `当前结论`
2. `建议动作`
3. `可信证据`
4. `风险与边界`
5. `试用反馈`
6. `部署与集成`

## MVP-67 First Screen Must Show

The first screen should answer:

```text
SecuPilot 是谁?
它帮我判断什么?
现在建议我做什么?
为什么可信?
当前边界是什么?
```

Required first-screen content:

- Product identity: `SecuPilot` as an enterprise security analysis and judgment assistant.
- One-sentence value proposition: detect, explain, recommend, and hand off human-reviewed security decisions.
- Current local/offline trial status: latest RC candidate, PASS/HOLD state, and synthetic/local-only data mode summarized in plain Chinese.
- Role entry cards:
  - `一线研判`
  - `深度分析`
  - `管理审阅`
  - `部署与集成`
- Assistant reasoning preview: `SecuPilot 研判计划` or `老贾研判计划` if the product owner explicitly chooses the Lao Jia persona naming.
- Next action area:
  - open event result
  - review recommended action
  - submit local feedback
  - view deployment readiness
- Trust strip:
  - evidence chain available
  - limitations explicit
  - real data not used
  - live Qwen/API/connectors not used
  - production write-back not used
  - customer-visible publish/deploy not authorized

## MVP-67 First Screen Must Not Show

The first screen must not show:

- `P1`, `P2`, or `P3` as customer-facing labels.
- `Mock Fixture`, `Mock Redline Fixture`, `Expert Mode`, role-switch controls, or internal debug controls.
- Raw artifact tables, SHA256 hashes, manifest paths, package internals, or evidence file paths as first-screen content.
- RC/package lineage as the dominant headline.
- Claims that live Qwen, live APIs, connectors, real data, masked-real data, production write-back, deployment, customer-visible publishing, external pilot, or production launch are active.
- Destructive action buttons or autonomous approval/action wording.
- Hardcoded business remediation suggestions as final runtime behavior.

Technical reconciliation may remain available only behind a secondary expandable section.

## MVP-67 Implementation Guidance

MVP-67 should update the current local/offline trial product entry, preferably the existing `/s1-trial` experience, into a product home rather than adding another evidence-console route.

Implementation expectations:

- Chinese-first user-facing copy.
- Role-based entry cards aligned to the PRD role mapping above.
- No P1/P2/P3, Mock Fixture, Expert Mode, or stale RC wording in reviewer-clean screenshots.
- Result and readiness summaries should remain local/offline and synthetic/package-backed.
- Technical details stay available only as secondary reconciliation.
- No backend/runtime/API/schema change.
- No live Qwen/API/connector call.
- No real or masked-real data.
- No customer-visible deploy/publish behavior.

## MVP-67 Acceptance Gates

MVP-67 can be considered ready for local review only if:

- Product-home screenshot answers the five first-screen questions in plain Chinese.
- Reviewer-clean screenshot contains no `P1`, `P2`, `P3`, `Mock Fixture`, `Expert Mode`, or stale RC candidate wording.
- Role entries map to PRD roles without creating new unauthorized permission roles.
- `老贾` / `Jarvis` is either absent from customer-facing copy or used only as assistant persona copy, not as a user role.
- Existing frontend tests and local screenshot/package validators pass for the changed route.

Decision:

```text
READY_FOR_GOAL_MVP_67_PRODUCT_HOME_UI_IMPLEMENTATION
```
