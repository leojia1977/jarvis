# S6 Qwen Cloud Handoff and Dify Topology Reconciliation 2026-04-30

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Qwen cloud handoff / Dify topology reconciliation |
| Date | 2026-04-30 |
| Applies to | S0 synthetic-only Qwen evaluation |
| Repo root | `D:\产品设计\New folder` |
| Related handoff template | `docs\S6_S0_QWEN_CLOUD_HANDOFF_EVIDENCE_TEMPLATE_2026_04_29.md` |
| Related runtime precheck | `docs\S6_S0_QWEN_CLOUD_RUNTIME_PRECHECK_2026_04_29.md` |

## 2. Decision

```text
QWEN_CLOUD_ENVIRONMENT_HANDOFF_PARTIAL_PASS
DIFY_TOPOLOGY_RECONCILED_FOR_S0_SYNTHETIC_EVALUATION
DIFY_S0_APP_CONFIG_AND_ARTIFACT_PATH_CONFIRMED_BY_FOLLOWUP
S0_EXECUTION_READY_FOR_EXACT_RUN_AUTHORIZATION
NO_REAL_DATA_OR_CUSTOMER_VISIBLE_OUTPUT_AUTHORIZED
```

The cloud-team non-secret environment information is sufficient to establish the high-level Qwen cloud runtime topology. A follow-up record now confirms the Dify app-level generation parameters and local exportable S0 artifact path. S0 still requires explicit run authorization, model outputs, scoring artifacts, GPU metrics, and reviewer closeout before any `S0_DECISION` can be issued.

## 3. System Layers

### 3.1 SecuPilot Repo Layer

Role:

```text
Generate and govern S0 synthetic CaseView / QwenFactBundle payloads.
Define S0 scoring rubric, safety checks, and import expectations.
Hold source-of-truth records, gates, and closeout evidence.
```

Current S0 inputs:

```text
mock_data\s0_synthetic\caseview\*.json
mock_data\s0_synthetic\qwen_fact_bundle\*.json
```

Boundary:

```text
Synthetic only.
No real data.
No masked real data.
No Qwen execution from repo until cloud handoff and output artifact path are complete.
```

### 3.2 Company Dify Layer

Role:

```text
Host the S0 evaluation workflow / app.
Send S0 synthetic payloads to the Qwen runtime endpoint.
Control Dify-side generation settings such as max output tokens, temperature, and top_p.
Store S0 synthetic run logs / Dify workflow logs.
```

Important terminology:

```text
Use "S0 synthetic run logs" or "Dify workflow logs".
Do not call them "business logs" or "real alert logs" for S0.
```

Boundary:

```text
Dify must not receive real data or masked-real data for S0.
Dify must not expose S0 outputs to customers.
Dify must not trigger production write-back or autonomous action.
```

### 3.3 Cloud Qwen Runtime Layer

Role:

```text
Run Qwen inference on the cloud GPU environment.
Expose an OpenAI-compatible vLLM API to Dify through the approved network route.
Provide GPU runtime metrics for S0 evidence.
```

Environment evidence received:

```text
Cloud platform: 全向箔云平台
GPU: dual Iluvatar MR-V100 32GB
Model id: qwen-72b / Qwen2.5-72B-Instruct-Int4
Checkpoint path: /root/models/qwen2.5-72b-int4
Runtime: vLLM 0.11.2 OpenAI-compatible API
Embedding model: bge-m3 on port 8001
GPU metrics: ixsmi, Driver 4.4.0
Operator: jia
```

## 4. Network Topology

Current understood topology:

```text
SecuPilot repo synthetic payloads
  -> operator-approved transfer into Dify S0 workflow
  -> Dify app / workflow on company-local environment
  -> SSH local forwarding to cloud Qwen vLLM runtime
  -> Qwen model output
  -> Dify S0 synthetic run logs / exportable artifacts
  -> repo-side artifact manifest / scoring import
```

Known non-secret network facts:

```text
Cloud node: zibo.saas.iluvatar.com.cn
Company/local Dify host reference: 192.168.10.139
Qwen endpoint: OpenAI-compatible vLLM API through SSH tunnel
LLM model: qwen-72b at http://192.168.10.139:8000/v1
Embedding model: bge-m3 at http://192.168.10.139:8001/v1
```

Credentials, SSH keys, tokens, VPN details, API keys, and credential-bearing URLs must not be written into repo docs, source, fixtures, prompts, Jira, or logs.

## 5. Runtime Configuration Status

| Item | Value | Status | Owner |
| --- | --- | --- | --- |
| Cloud GPU environment | 全向箔云平台 / Iluvatar MR-V100 32GB x2 | `RECEIVED` | Cloud team |
| Model id | `qwen-72b` / Qwen2.5-72B-Instruct-Int4 | `RECEIVED` | Cloud team |
| Checkpoint | `/root/models/qwen2.5-72b-int4` | `RECEIVED` | Cloud team |
| Runtime framework | vLLM `0.11.2` OpenAI-compatible API | `RECEIVED` | Cloud team |
| IX-ML / driver | IX-ML / Driver `4.4.0` | `RECEIVED` | Cloud team |
| Context length | `8192` via `--max-model-len 8192` | `RECEIVED` | Cloud team |
| Tensor parallel | `2` | `RECEIVED` | Cloud team |
| Max output tokens | `8192` | `CONFIRMED_BY_DIFY_S0_CONFIG_RECORD` | Product / Dify operator |
| Temperature | `0.2` | `CONFIRMED_BY_DIFY_S0_CONFIG_RECORD` | Product / Dify operator |
| top_p | `0.8` | `CONFIRMED_BY_DIFY_S0_CONFIG_RECORD` | Product / Dify operator |
| GPU metrics | `ixsmi`, `~/gpu_snapshot.txt` | `RECEIVED_WITH_EXPORT_PATH` | Cloud team |
| Output artifact export path | `D:\产品设计\New folder\artifacts\s0_qwen_runs\2026-04-30-001\` | `LOCAL_PATH_CONFIRMED_BY_DIFY_S0_CONFIG_RECORD` | Product / Dify operator |
| Reviewer | `Jarvis/product-governance reviewer pending` | `PENDING_REVIEWER_ASSIGNMENT_BEFORE_S0_CLOSEOUT` | Product / governance |

## 6. S0 Log Definition

For S0, the acceptable log class is:

```text
S0 synthetic run logs / Dify workflow logs
```

Allowed contents:

```text
synthetic input payload id
synthetic QwenFactBundle id
Qwen synthetic output
Dify workflow execution metadata
GPU runtime metrics
scoring/evaluator notes
operator notes
reviewer notes
```

Forbidden contents:

```text
real alert logs
masked-real alert logs
customer data
production SIEM / EDR logs
secrets
tokens
SSH keys
API keys
credential-bearing URLs
unredacted prompt logs containing secrets
```

## 7. Dify S0 App Configuration Gate

Before S0 Qwen execution may proceed, create or confirm one S0-specific Dify app/workflow:

```text
Suggested Dify app/workflow name:
S0-SecuPilot-Qwen-Synthetic-Eval
```

Required confirmation:

```text
Input source = mock_data/s0_synthetic/qwen_fact_bundle/*.json
Model endpoint = Qwen vLLM OpenAI-compatible API via approved SSH tunnel
Max output tokens = actual configured value
Temperature = actual configured value
top_p = actual configured value
Output export method = JSON/CSV/files/screenshots/artifact bundle path
Customer-visible output = NO
Real data = NO
Masked-real data = NO
Production write-back = NO
Autonomous action = NO
```

Recommended starting values for deterministic S0 evaluation:

```text
max output tokens = 4096
temperature = 0.2
top_p = 0.8
```

Follow-up record:

```text
docs\S6_DIFY_S0_APP_CONFIG_AND_ARTIFACT_PATH_CONFIRMATION_2026_04_30.md
```

Confirmed values:

```text
max output tokens = 8192
temperature = 0.2
top_p = 0.8
output artifact path = D:\产品设计\New folder\artifacts\s0_qwen_runs\2026-04-30-001\
```

## 8. Safety Assertions

Jarvis supplied:

```text
Operator = jia
Safety confirmation = YES
```

Interpreted required assertions:

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

## 9. Current Gaps

Remaining before S0 execution / closeout:

```text
GAP-01: final reviewer assignment before S0 closeout
GAP-02: explicit S0 Qwen synthetic run authorization
GAP-03: S0 output import/scoring execution still not run
```

## 10. HOLD Conditions

HOLD S0 if:

- Dify app configuration cannot name actual generation parameters;
- output artifacts remain only inside an internal database with no governed export path;
- any input includes real or masked-real data;
- any output is customer-visible before a separate gate;
- model output contains secrets or customer identifiers;
- invocation requires backend/runtime/API/schema or connector changes;
- credentials would be written to repo, Jira, prompts, fixtures, docs, or logs;
- reviewer assignment remains absent at S0 closeout.

## 11. Non-Authorization

This reconciliation does not authorize:

```text
Qwen execution
Qwen output import
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

## 12. Next Route

```text
OPEN_S0_QWEN_SYNTHETIC_RUN_AUTHORIZATION_OR_WAIT_FOR_REVIEWER_ASSIGNMENT
```
