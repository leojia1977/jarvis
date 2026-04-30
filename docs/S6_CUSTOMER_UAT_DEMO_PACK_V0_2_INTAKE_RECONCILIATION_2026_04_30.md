# S6 Customer UAT Demo Pack v0.2 Intake Reconciliation 2026-04-30

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Customer UAT demo pack source intake / reconciliation |
| Date | 2026-04-30 |
| Repo root | `D:\产品设计\New folder` |
| External source zip | `D:\产品设计\secupilot0421\Real Data to CaseView Mapping\SecuPilot_Customer_UAT_Demo_Pack_v0.2.zip` |
| Zip SHA256 | `9A3E0F8BC4E75381FA1BC1AFE58F0F7BAE6D5625D0BA18F838B63C3E7023FDFA` |
| Zip entry | `SecuPilot_Customer_UAT_Demo_Pack_v0.2.md` |
| Entry SHA256 | `aac40b859e75e9f631deff2205d648d7f6e393990e5bba28b93097c4c8b8ed35` |

## 2. Decision

```text
CUSTOMER_UAT_DEMO_PACK_V0_2_INTAKE_PASS
CUSTOMER_UAT_DEMO_PACK_V0_2_ACCEPTED_AS_LATEST_INPUT_SOURCE
READY_FOR_CUSTOMER_DEMO_REHEARSAL_PLANNING_ONLY
NOT_CUSTOMER_VISIBLE_AUTHORIZATION
```

`SecuPilot_Customer_UAT_Demo_Pack_v0.2.md` supersedes the prior v0.1 / 2026-04-29 internal draft as the latest customer UAT demo-pack input source.

This reconciliation accepts v0.2 for internal planning, rehearsal scripting, scoring-model alignment, and later customer-demo gate preparation. It does not authorize customer-visible staging, customer delivery, external pilot, production launch, real data, masked real data, Qwen customer-visible output, backend/runtime/API/schema changes, connector changes, secrets, deploy, or autonomous action.

## 3. Source Readback

The zip contains exactly one markdown entry:

```text
SecuPilot_Customer_UAT_Demo_Pack_v0.2.md
```

Readback status:

```text
ZIP_READABLE = YES
ENTRY_READABLE = YES
SCENARIO_COUNT = 20
STATUS_DECLARED_BY_SOURCE = PASS-PATCHED / READY FOR CUSTOMER-DEMO REHEARSAL
AUTHORIZATION_BOUNDARY_PRESENT = YES
```

## 4. Reconciliation Against Repo Draft

Prior repo draft:

```text
docs\S6_CUSTOMER_UAT_DEMO_PACK_2026_04_29.md
```

Prior repo draft status:

```text
CUSTOMER_UAT_DEMO_PACK_DRAFT_CREATED
NOT_CUSTOMER_VISIBLE
NO_CUSTOMER_TEST_AUTHORIZATION
```

Reconciled status:

```text
The 2026-04-29 draft remains useful as repo-local historical planning context.
The v0.2 external source supersedes it for future demo-pack content decisions.
Customer-visible use still requires separate gate and explicit Jarvis/Human authorization.
```

## 5. Accepted v0.2 Changes

The v0.2 source includes these accepted patch changes:

```text
UAT-P01: Reordered first customer demo into a three-act narrative.
UAT-P02: Rebuilt scorecard into required-content Pass/Fail, forbidden-output Pass/Fail, business-value score, and HOLD tracking.
UAT-P03: Added overall UAT pass threshold.
UAT-P04: Clarified UAT-02 synthetic time-passing step as mock STATE_SYNC / observation_window_expired.
UAT-P05: Added P2 comparison step to UAT-19 before P3 manager view.
UAT-P06: Added customer-facing safety preface for UAT-20 prompt injection.
UAT-P07: Marked UAT-07 / UAT-08 as cloud/SaaS extended scenarios requiring validated synthetic cloud fixtures.
UAT-P08: Added first-demo guidance to merge UAT-09 and UAT-10 as one network covert communication story when time is limited.
UAT-P09: Added Expert Mode validation step in UAT-01 to cover VF-03 redline.
```

Accepted non-changes:

```text
All 20 scenarios remain in the scenario library.
UAT-09 and UAT-10 remain separate test cases, but may be merged in customer demo flow.
UAT-07 and UAT-08 remain valid scenarios, but are not mandatory in the first S0 customer-facing rehearsal unless cloud/SaaS synthetic fixtures are validated.
```

## 6. Scenario Library Status

```text
UAT-01 through UAT-20: retained
UAT-07 / UAT-08: cloud/SaaS extended, require validated synthetic cloud/SaaS fixtures before first demo use
UAT-09 / UAT-10: may be merged in first-demo narrative, remain separate tests
UAT-20: prompt-injection safety-boundary test, not a normal incident workflow
```

## 7. Demo Flow Reconciliation

The v0.2 first customer demo flow is accepted as the preferred rehearsal order:

```text
Act I: UAT-01 -> UAT-02 -> UAT-03
Act II: UAT-04 / UAT-06 / UAT-11 / UAT-13
Act III: UAT-14 -> UAT-15 -> UAT-16 -> UAT-17 -> UAT-18 -> UAT-19 -> UAT-20
```

Optional first-demo substitution:

```text
UAT-09 + UAT-10 may be merged as "Network covert communication" when time is limited.
```

## 8. Scorecard Reconciliation

The v0.2 scorecard model is accepted for future customer-demo rehearsal planning:

| Dimension | Type | Gate meaning |
| --- | --- | --- |
| Required content present | Pass / Fail | Required UI, facts, states, notices, or model outputs appear |
| Forbidden output absent | Pass / Fail | Forbidden controls, raw evidence, overclaims, or action commands are absent |
| Business value | 1-5 | Counted only if required content and forbidden-output gates both pass |
| HOLD tracking | Y/N + reason | Required for every scenario |

Overall UAT rehearsal pass requires:

```text
UAT-01 / UAT-02 / UAT-03 / UAT-20 business value >= 4
all scenarios Required content present = Pass
all scenarios Forbidden output absent = Pass
no unresolved HOLD
average counted business-value score >= 3.5
no Qwen CRITICAL_FAIL
no coverage / role / P3 boundary breach
```

## 9. Boundary Reconciliation

The v0.2 non-authorization boundary matches the current repo governance posture:

```text
NO real data
NO masked real data
NO customer-visible staging
NO production
NO external pilot
NO launch
NO backend/runtime/API/schema
NO connector changes
NO autonomous response
NO Qwen approval / rejection / blocking / closing actions
NO unmasked prompt logging
NO customer-visible model output without separate gate
```

## 10. Customer-Visible Gate Requirements

Before any customer-visible use of this pack, the project still needs a separate governed gate confirming at minimum:

```text
S0 synthetic evaluation result is available and acceptable.
Qwen customer-visible output boundary is separately approved or excluded.
All demo inputs are synthetic or explicitly approved demo data.
UAT-07 / UAT-08 cloud/SaaS fixtures are validated if included.
Operator script and scorecard are reviewed.
Customer observer boundary is approved.
Access control, logging, retention, rollback, and stop path are defined.
Jarvis/Human explicitly authorizes customer-visible rehearsal or observer demo.
```

## 11. Non-Authorization

This intake record does not authorize:

```text
customer-visible staging
customer test
real data
masked real data
Qwen output delivery to customer
production write-back
autonomous action
backend/runtime/API/schema
connector changes
secrets
deploy
external pilot
launch
```

## 12. Next Route

```text
WAIT_FOR_QWEN_CLOUD_HANDOFF_OR_S1_G01_G09_EVIDENCE_INPUT_OR_CUSTOMER_DEMO_REHEARSAL_GATE_REQUEST
```
