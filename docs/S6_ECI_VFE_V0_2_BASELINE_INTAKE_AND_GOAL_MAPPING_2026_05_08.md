# S6 ECI/VFE v0.2 Baseline Intake And Goal Mapping

Date: 2026-05-08

Source file:

```text
D:/downloads/ECI_VFE_V0_2_BASELINE_AND_GOAL_QUEUE_2026_05_08.md
```

Intake decision:

```text
ACCEPT_AS_ECI_VFE_V0_2_BASELINE
```

Execution posture:

```text
NOW_INSERT_AS_PARALLEL_AUTOMATION_LANE
```

## Scope

This intake establishes ECI/VFE as an independent SecuPilot product capability lane. It must not be mixed into the RC-017 UX03 review surface.

ECI/VFE remains local/offline, metadata-only, fixture-first, and human-in-the-loop only until separately authorized.

## Product Split

```text
VFE = pre-attack vulnerability / weakness forecast candidate layer.
ECI = during-attack exploit-chain reasoning layer.
ECI x VFE = correlation between a forecast weakness and current exploit-chain evidence.
```

This lane is allowed to produce executable objects:

- TypeScript interfaces
- JSON schemas
- metadata-only synthetic fixtures
- local deterministic rule engine
- output guard
- guard-passed UI components
- local/offline review package
- local tests and screenshots

## Repo Goal ID Mapping

The source baseline uses `GOAL-MVP-30` through `GOAL-MVP-35`, but this repo already contains historical `GOAL-MVP-30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG`.

To avoid ID collision, repo execution uses ECI/VFE-prefixed goal IDs while preserving the external aliases:

| Execution order | Repo executable goal ID | Human-readable lane alias | External baseline alias |
| --- | --- | --- | --- |
| 1 | `GOAL-ECIVFE-30_FIXTURE_MODEL` | `GOAL-ECI-VFE-30_FIXTURE_MODEL` | `GOAL-MVP-30_ECI_VFE_FIXTURE_MODEL` |
| 2 | `GOAL-ECIVFE-33_LOCAL_RULE_ENGINE` | `GOAL-ECI-VFE-33_LOCAL_RULE_ENGINE` | `GOAL-MVP-33_ECI_VFE_LOCAL_RULE_ENGINE` |
| 3 | `GOAL-ECIVFE-34_OUTPUT_GUARD` | `GOAL-ECI-VFE-34_OUTPUT_GUARD` | `GOAL-MVP-34_ECI_VFE_OUTPUT_GUARD` |
| 4 | `GOAL-ECIVFE-31_CHAIN_INDICATOR_UI` | `GOAL-ECI-VFE-31_CHAIN_INDICATOR_UI` | `GOAL-MVP-31_ECI_CHAIN_INDICATOR_UI` |
| 5 | `GOAL-ECIVFE-32_FORECAST_CARD_UI` | `GOAL-ECI-VFE-32_FORECAST_CARD_UI` | `GOAL-MVP-32_VFE_FORECAST_CARD_UI` |
| 6 | `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE` | `GOAL-ECI-VFE-35_LOCAL_REVIEW_PACKAGE` | `GOAL-MVP-35_ECI_VFE_LOCAL_REVIEW_PACKAGE` |

Required order:

```text
GOAL-ECIVFE-30 -> GOAL-ECIVFE-33 -> GOAL-ECIVFE-34 -> GOAL-ECIVFE-31 -> GOAL-ECIVFE-32 -> GOAL-ECIVFE-35
```

## Non-Authorization Boundary

This intake does not authorize:

- real data
- masked-real data
- live Qwen/API calls
- live connectors
- production connectors
- production write-back
- customer-visible publish, deploy, or output
- external pilot
- production launch
- secrets, tokens, auth headers, raw customer logs, raw payloads, or host raw evidence
- autonomous approval, rejection, blocking, containment, isolation, remediation, or action-mode choice
- PoC, exploit steps, payload generation, or attacker-readable attack path
- bulk VFE export

## Hard Rules Carried Forward

1. LLM output is never authoritative by default.
2. Every LLM-derived field must carry source/authority metadata and defaults to `is_authoritative=false`.
3. Semantic correlation cannot independently upgrade a case.
4. Correlation order must be hard match, bounded fuzzy match, then semantic supporting signal.
5. UI cannot render ECI/VFE output unless schema validation and output guard pass.
6. VFE output must use `attack_path_defensive_summary`, not attacker-readable `attack_path`.
7. VFE must not expose internal topology reachability details.
8. High-stage ECI labels require stricter confidence thresholds.
9. High-stage suspicion shortens observation windows but does not authorize automatic containment.
10. `evidence_gaps` must include urgency and collection-window guidance.
11. VFE query patterns are an attack surface and must be audit-controlled.
12. Prompt injection fixtures are mandatory in the first fixture set.
13. Forbidden output is HOLD/NO_GO.
14. All ECI/VFE MVP work remains fixture-only, metadata-only, local/offline until separately authorized.

## Insertion Decision

`GOAL-ECIVFE-30`, `GOAL-ECIVFE-33`, and `GOAL-ECIVFE-34` are low-conflict automation-friendly work because they only create schemas, fixtures, local scripts, validators, and tests.

`GOAL-ECIVFE-31` and `GOAL-ECIVFE-32` must wait until `GOAL-ECIVFE-34` output guard passes.

`GOAL-ECIVFE-35` must wait until both UI goals pass.

## Next Unlock

Begin:

```text
GOAL-ECIVFE-30_FIXTURE_MODEL
```

Keep RC-017 UX03 review and ECI/VFE implementation separate.
