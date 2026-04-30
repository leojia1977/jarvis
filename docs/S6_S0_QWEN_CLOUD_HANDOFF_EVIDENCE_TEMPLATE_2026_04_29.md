# S6 S0 Qwen Cloud Handoff Evidence Template 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Cloud handoff evidence template |
| Date | 2026-04-29 |
| Applies to | S0 synthetic-only Qwen evaluation |
| Related precheck | `docs/S6_S0_QWEN_CLOUD_RUNTIME_PRECHECK_2026_04_29.md` |

## 2. Decision

```text
QWEN_CLOUD_HANDOFF_EVIDENCE_TEMPLATE_CREATED
NO_QWEN_EXECUTION_AUTHORIZED
NO_SECRET_CAPTURE_AUTHORIZED
```

This template is for the cloud Qwen operator to fill in with non-secret evidence. It must not contain credentials, tokens, passwords, SSH keys, VPN details, customer-specific endpoints, real data, or masked-real data.

## 3. Required Handoff Fields

| Field | Required value | Status |
| --- | --- | --- |
| Cloud GPU environment identifier | Non-secret environment name or opaque id | `PENDING` |
| Qwen model id | Model family/name only | `PENDING` |
| Qwen model version/checkpoint | Version or checkpoint label | `PENDING` |
| Runtime invocation method | CLI/API/runbook name without secrets | `PENDING` |
| Prompt template version | Governed prompt/run template label | `PENDING` |
| Synthetic input transfer method | How `mock_data/s0_synthetic` will be provided to the cloud runner | `PENDING` |
| Output artifact export path | Non-secret repo-import or artifact-storage path | `PENDING` |
| GPU metrics capture method | Command/tool name and metric names only | `PENDING` |
| Evaluator runbook or script | Script/runbook name and version | `PENDING` |
| Named operator | Human/operator name or role | `PENDING` |
| Named reviewer | Reviewer name or role | `PENDING` |
| No real/masked-real data confirmation | `YES` required | `PENDING` |
| Credentials kept out of repo confirmation | `YES` required | `PENDING` |

## 4. Required Operator Assertions

The operator must confirm:

```text
SYNTHETIC_ONLY_INPUTS_USED = YES
REAL_DATA_USED = NO
MASKED_REAL_DATA_USED = NO
CUSTOMER_VISIBLE_OUTPUT = NO
PRODUCTION_WRITEBACK = NO
AUTONOMOUS_ACTION = NO
CREDENTIALS_WRITTEN_TO_REPO = NO
CONNECTOR_CHANGES = NO
BACKEND_RUNTIME_API_SCHEMA_CHANGES = NO
DEPLOY_OR_EXTERNAL_PILOT = NO
```

## 5. Expected Input Set

The cloud run must use:

```text
mock_data/s0_synthetic/caseview/*.json
mock_data/s0_synthetic/qwen_fact_bundle/*.json
```

Expected counts:

```text
CaseView payloads: 20
QwenFactBundle payloads: 20
Scenario range: UAT-01 through UAT-20
```

## 6. Expected Output Set

The operator should return or expose non-secret artifacts:

```text
S0_QWEN_OUTPUTS_MANIFEST
per-scenario model output files
per-scenario action-command scan results
per-scenario prompt-injection verdicts
aggregate scoring table
GPU latency and memory metrics
operator notes
reviewer notes
```

No credentials or real/masked-real data may be included in outputs.

## 7. HOLD Conditions

HOLD if:

- any input includes real or masked-real data;
- any credential would be written to repo, Jira, prompts, fixtures, or logs;
- model output contains customer identifiers or secrets;
- output artifact path cannot be exported without exposing secrets;
- invocation requires backend/runtime/API/schema or connector changes;
- operator cannot confirm synthetic-only boundary.

## 8. Non-Authorization

This template does not authorize:

```text
Qwen execution
real data
masked real data
closed shadow
customer-visible output
production write-back
autonomous action
backend/runtime/API/schema
connector changes
secrets
Jira mutation
deploy
external pilot
launch
```

## 9. Next Route

```text
WAIT_FOR_FILLED_CLOUD_QWEN_HANDOFF_EVIDENCE
```

## 10. 2026-04-30 Topology Reconciliation Note

Follow-up record:

```text
docs\S6_QWEN_CLOUD_HANDOFF_AND_DIFY_TOPOLOGY_RECONCILIATION_2026_04_30.md
```

Status update:

```text
QWEN_CLOUD_ENVIRONMENT_HANDOFF_PARTIAL_PASS
DIFY_TOPOLOGY_RECONCILED_FOR_S0_SYNTHETIC_EVALUATION
S0_EXECUTION_STILL_HOLD_PENDING_DIFY_APP_CONFIG_AND_ARTIFACT_EXPORT_PATH
```

Cloud runtime facts now received:

```text
Cloud GPU environment: 全向箔云平台, dual Iluvatar MR-V100 32GB
Model id: qwen-72b / Qwen2.5-72B-Instruct-Int4
Checkpoint: /root/models/qwen2.5-72b-int4
Runtime: vLLM 0.11.2 OpenAI-compatible API
LLM endpoint: http://192.168.10.139:8000/v1
Embedding endpoint: http://192.168.10.139:8001/v1
Context length: 8192
GPU metrics: ixsmi
Operator: jia
```

Remaining required before S0 execution / closeout:

```text
Actual Dify max output tokens / temperature / top_p
Exportable S0 output artifact path
Reviewer assignment before S0 closeout
```
