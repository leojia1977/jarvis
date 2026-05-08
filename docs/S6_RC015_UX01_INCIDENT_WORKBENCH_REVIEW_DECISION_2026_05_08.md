# S6 RC-015 UX01 Incident Workbench Review Decision

Date: 2026-05-08

Route: `/incident/CASE-2847`

Review basis:

- `artifacts/product_experience/ux01/incident-product-desktop.png`
- `artifacts/product_experience/ux01/incident-product-mobile.png`
- `artifacts/product_experience/ux01/incident-product-desktop.text.json`
- `artifacts/product_experience/ux01/incident-product-mobile.text.json`
- `artifacts/reviews/claude_web/ux01_incident_workbench_review_package_20260508.zip`

Reviewer: Jarvis / TL / Product-governance reviewer

Decision:

```text
RC-015_CN = PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
```

## Pass Basis

- Main path identity is clear: product home -> incident judgment -> `CASE-2847`.
- First screen answers:
  - what SecuPilot judged
  - what action is recommended
  - why the judgment is credible
  - what remains uncertain
  - what will not be executed automatically
- Product direction is consistent with the prior design:
  - incident queue
  - conclusion first
  - event timeline
  - recommended action
  - human confirmation boundary
  - folded detailed evidence
- No reviewer-facing `P1`, `P2`, `P3`, `Mock Fixture`, `Expert Mode`, raw payload, token, auth header, or stale RC wording was observed.

## Findings

F1: Internal engineering language remains visible in the AI/model section:

- `Qwen dry-run stub`
- `provider stub`
- `stub 案例数`
- `模拟延迟`
- `HOLD 输入包`
- `Dry-run 输出预览`

F2: The model preview section is currently embedded in the main operation path. It reads like a product/engineering review surface rather than an operator surface.

F3: `SECUPILOT · INVESTIGATION REPORT` creates a small English-heavy feel in an otherwise Chinese-first route.

## Non-Blocking Notes

N01: `技术对账信息` should show a clearer expand affordance.

N02: The directly visible event timeline is acceptable as a light timeline plus folded evidence structure.

N03: Exposing the `Qwen` brand in formal customer-facing copy should remain a product strategy decision.

N04: Mobile should fold the model preview by default and keep feedback touch targets at least 44px.

N05: `查看本地记录预览` should make its expand behavior clearer.

## Next Goal

Recommended next single-scope product Goal:

```text
GOAL-UX-02_INCIDENT_AI_ADVICE_LANGUAGE_AND_COLLAPSE
```

Purpose:

```text
Replace model/provider/dry-run/HOLD engineering terms with operator-readable AI advice language and make the AI advice source section collapsed by default.
```

## Boundary

This decision does not authorize:

- real data
- masked-real data
- live Qwen/API/connectors
- secrets, tokens, auth headers, or raw customer logs
- production write-back
- customer-visible publish/deploy/output
- external pilot
- production launch
- backend/runtime/API/schema changes
- autonomous approval, isolation, blocking, account closure, or action
