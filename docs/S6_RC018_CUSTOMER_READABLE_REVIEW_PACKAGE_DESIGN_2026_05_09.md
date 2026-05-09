# S6 RC-018 Customer-Readable Review Package Design

Date: 2026-05-09

Candidate: `LOCAL_OFFLINE_TRIAL_RC_018_CN`

Package target path: `artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review`

## Decision

RC-018 should be a customer-readable local/offline product review package, not another evidence-table package.

The review should answer one product question:

```text
Can a customer-facing security user understand SecuPilot's judgment path from product home to incident workbench, AI advice source, ECI/VFE explanation, and local feedback without seeing debug or evidence-harness internals?
```

## RC-018 Scope

Allowed:

- local/offline review only
- synthetic fixture metadata only
- product-home and incident-workbench screenshots
- guard-passed ECI/VFE summaries
- local feedback preview
- local package manifest, screenshot index, safety scans, and route map

Not authorized:

- real data
- masked-real data
- live Qwen/API/connectors
- API keys, secrets, tokens, auth headers, raw customer logs, or raw payloads
- production write-back
- customer-visible publish/deploy/output
- external pilot
- production launch
- PoC, exploit steps, payloads, credentials, or attacker-readable topology
- autonomous containment, remediation, isolation, blocking, approval, rejection, or action-mode choice

## Required Pre-Conditions

RC-018 package generation should not start until:

- `GOAL-ECIVFE-32_FORECAST_CARD_UI` is PASS.
- `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE` is PASS.
- `output_guard_scan.json` is PASS with no blocking findings.
- Reviewer-facing screenshots do not expose P1/P2/P3, Mock Fixture, Expert Mode, stale RC wording, fixture/debug labels, raw payloads, tokens, auth headers, live API, connectors, production write-back, deploy, PoC, exploit steps, or attacker-readable topology.
- `ECI/VFE` content is integrated as product explanation, not exposed as a standalone technical route.

## Customer Path To Review

The package should guide reviewer through this path:

```text
REVIEWER_START_HERE_中文.md
  -> 产品首页 / 本地试用入口
  -> 事件工作台 /incident/CASE-2847
  -> 首屏结论 / 建议动作 / 可信边界
  -> 展开 AI 建议来源
  -> 查看攻击链判断 / VFE 预警摘要
  -> 查看缺失证据和补证窗口
  -> 提交本地反馈预览
```

The standalone `/eci-vfe-chain` validation page should not be used as the main customer path. It may appear only in a technical appendix if needed.

## Required Screenshots

RC-018 should include at minimum:

| Screenshot | Purpose |
| --- | --- |
| `01_product_home_desktop.png` | First customer impression: what SecuPilot is and what to do next |
| `02_product_home_mobile.png` | Mobile readability of the product entry |
| `03_incident_first_load_desktop.png` | Incident workbench first screen: judgment, action, trust boundary |
| `04_incident_first_load_mobile.png` | Mobile readability of the main incident path |
| `05_ai_advice_source_expanded_desktop.png` | AI advice source explanation, product language only |
| `06_eci_vfe_summary_expanded_desktop.png` | Attack-chain and VFE summary integrated into product UI |
| `07_feedback_preview_desktop.png` | Local feedback loop and no-writeback boundary |

Optional technical appendix screenshots:

- `08_technical_reconciliation_desktop.png`
- `/eci-vfe-chain` screenshot only if clearly marked as validation appendix, not customer path

## Required Package Files

The package should include:

- `REVIEWER_START_HERE_中文.md`
- `01_REVIEW_PROMPT.md`
- `02_PRODUCT_ROUTE_MAP_中文.md`
- `03_REVIEWER_CHECKLIST_中文.md`
- `04_FEEDBACK_TEMPLATE_中文.md`
- `package_manifest.json`
- `SCREENSHOT_INDEX_中文.json`
- `safety_scan.json`
- `final_status.json`
- `case_summary.json`
- `artifact_manifest.json`
- `eci_vfe/output_guard_scan.json`
- `eci_vfe/chain_assessment_summary.json`
- `eci_vfe/forecast_candidate_summary.json`

Raw chain/forecast artifacts may be included only if they are metadata-only and already guard-passed. They must not be the reviewer entry point.

## Product Acceptance Criteria

Reviewer should be able to answer these in 30 seconds:

1. What is SecuPilot?
2. What incident did SecuPilot judge?
3. What does SecuPilot recommend now?
4. Why is the judgment trustworthy but still conservative?
5. What evidence is missing?
6. What will SecuPilot not do automatically?
7. How can the reviewer leave local feedback?

Role coverage:

- Engineer: understands the next operational step and missing evidence.
- Manager: understands risk, urgency, confidence, and human decision boundary.
- CTO: understands local/offline boundary, no write-back, no live connector, no customer deployment.

## ECI/VFE Product Rules

ECI/VFE should appear as product explanation:

- `攻击链判断`
- `当前阶段判断`
- `风险预警摘要`
- `还缺什么证据`
- `建议补证窗口`
- `如果补不到证据，保持保守判断`

ECI/VFE should not appear as:

- `ECI-FIX-001` as primary user-facing heading
- `Guard-passed local/offline fixture output`
- `output_guard_scan`
- `provider`
- `stub`
- `dry-run`
- attacker-readable `attack_path`
- topology reachability detail
- exploit or payload guidance

VFE must use defensive wording such as `attack_path_defensive_summary`; it must never expose an attacker-readable attack path.

## RC-018 HOLD Conditions

HOLD if any reviewer-facing page or screenshot shows:

- P1/P2/P3 role switches or internal approval-level labels
- Mock Fixture, Expert Mode, fixture/debug labels, provider/stub/dry-run engineering language
- stale RC candidate/source/package path
- raw logs, raw payload, token, secret, auth header, credentials, PoC, exploit steps, or payloads
- internal topology reachability detail or attacker-readable attack path
- live Qwen/API/connectors or real/masked-real data language
- production write-back or customer-visible deploy/publish authorization
- autonomous containment, remediation, isolation, blocking, approval, rejection, or action-mode choice
- ECI/VFE output rendered before schema validation and output guard PASS
- VFE semantic correlation independently upgrades a case
- package manifest missing SHA256/bytes for required files
- screenshot index missing route, viewport, candidate, source candidate, sha256, or folded/expanded state where relevant

## Reviewer Prompt

Use this prompt for RC-018 local/offline review:

```text
You are reviewing LOCAL_OFFLINE_TRIAL_RC_018_CN as a local/offline SecuPilot product review package.

Review scope:
- local/offline only
- synthetic fixture metadata only
- no real data
- no masked-real data
- no live Qwen/API/connectors
- no production write-back
- no customer-visible deploy/publish/output
- no autonomous containment/remediation/action

Review order:
1. Read REVIEWER_START_HERE_中文.md.
2. Follow the product route map, not the raw artifact list.
3. Inspect the required screenshots first.
4. Check package_manifest.json and SCREENSHOT_INDEX_中文.json only after the product path is clear.
5. Confirm output_guard_scan.json is PASS before accepting ECI/VFE content.

Questions to answer:
1. Can a customer understand what SecuPilot is within the first screen?
2. Can an engineer understand the next operational step?
3. Can a manager understand risk, urgency, confidence, and human decision boundary?
4. Can a CTO understand local/offline, no-writeback, no-live-connector, and no-deploy boundaries?
5. Does ECI/VFE read like product judgment support rather than engineering output?
6. Are attack-chain and forecast details defensive and non-actionable for an attacker?
7. Does the package avoid debug controls, stale RC wording, secrets, raw payloads, and live-system language?

Return:
- PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL
- PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
- HOLD_FOR_UI_OR_PACKAGE_FIXES
- NO_GO_SECURITY_BOUNDARY

List blocking findings first, then non-blocking notes, then next recommended product goal.
```

## Next Automation Route

Automation should continue in this order:

1. `GOAL-ECIVFE-32_FORECAST_CARD_UI`
2. `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE`
3. `GOAL-RC018_CUSTOMER_READABLE_PACKAGE`
4. `GOAL-RC018_REVIEW_DECISION_EXPORT`
5. Product-home and incident-workbench polish based on RC-018 feedback

## Done When

RC-018 is ready for reviewer only when:

- required screenshots exist
- package manifest and screenshot index are complete
- safety scan reports no blocking findings
- ECI/VFE guard scan is PASS
- product route map starts from product experience rather than artifact list
- reviewer prompt is included
- package is zipped and locally reviewable without repo knowledge

## Non-Authorization

RC-018 design does not authorize customer-visible publishing, cloud deployment, external pilot, production launch, real or masked-real data, live Qwen/API/connectors, production write-back, or autonomous security action.
