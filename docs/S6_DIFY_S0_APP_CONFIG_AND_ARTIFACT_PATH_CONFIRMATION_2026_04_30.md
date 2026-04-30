# S6 Dify S0 App Config and Artifact Path Confirmation 2026-04-30

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Dify S0 app configuration / artifact path confirmation |
| Date | 2026-04-30 |
| Applies to | S0 synthetic-only Qwen evaluation |
| Related topology record | `docs\S6_QWEN_CLOUD_HANDOFF_AND_DIFY_TOPOLOGY_RECONCILIATION_2026_04_30.md` |

## 2. Decision

```text
DIFY_S0_APP_CONFIG_CONFIRMED
S0_OUTPUT_ARTIFACT_PATH_LOCAL_CONFIRMED
S0_EXECUTION_READY_FOR_EXACT_RUN_AUTHORIZATION
S0_DECISION_NOT_YET_AVAILABLE
```

The Dify app-level generation parameters and local output artifact path are now confirmed for S0 planning. This closes the prior configuration/path gap but does not by itself run Qwen, import model outputs, score outputs, authorize real data, authorize customer-visible output, or produce an `S0_DECISION`.

Execution follow-up:

```text
docs\S6_S0_QWEN_SYNTHETIC_RUN_EXECUTION_REPORT_2026_04_30.md
```

S0 attempted execution after this confirmation, but the result is `HOLD_WITH_FAILURES`.

## 3. Confirmed Dify App Generation Parameters

| Parameter | Confirmed value |
| --- | --- |
| Max output tokens | `8192` |
| Temperature | `0.2` |
| top_p | `0.8` |

Interpretation:

```text
These values are Dify app / request-level generation settings.
They are distinct from the cloud vLLM --max-model-len 8192 context-length setting.
```

Execution finding:

```text
Direct vLLM execution rejected max_tokens=8192 because qwen-72b max_model_len is also 8192 and the first S0 request contained input tokens.
The actual S0 run used effective max_tokens=1024 and still held due to qwen-72b runtime connection failure after UAT-03.
```

## 4. Confirmed S0 Output Artifact Path

Local artifact path convention:

```text
D:\产品设计\New folder\artifacts\s0_qwen_runs\2026-04-30-001\
```

Recommended folder structure:

```text
outputs\
  UAT-01.json ... UAT-20.json
scoring\
  s0_scorecard.csv
  action_command_scan.csv
  prompt_injection_verdicts.csv
metrics\
  gpu_snapshot.txt
  latency_summary.csv
notes\
  operator_notes.md
  reviewer_notes.md
manifest.json
```

Artifact handling rule:

```text
Raw Qwen outputs and detailed Dify run logs may remain local/non-repo artifacts.
Repo closeout should import only safe manifests, scoring summaries, and governed reports unless separately authorized.
```

## 5. S0 Execution Inputs

Expected input source:

```text
mock_data\s0_synthetic\qwen_fact_bundle\*.json
```

Expected scenario range:

```text
UAT-01 through UAT-20
```

Expected model endpoint:

```text
qwen-72b LLM: http://192.168.10.139:8000/v1
```

Embedding endpoint, if needed:

```text
bge-m3: http://192.168.10.139:8001/v1
```

## 6. Remaining Before S0 Decision

S0 still requires actual execution artifacts:

```text
20 per-scenario Qwen outputs
per-scenario action-command scan results
prompt-injection verdicts
unsupported_claims transfer scoring
coverage / role / history clamp scoring
GPU runtime metrics
operator notes
reviewer notes
aggregate S0 scorecard
```

Allowed aggregate S0 decisions remain:

```text
PASS_FOR_SYNTHETIC_ONLY
CONDITIONAL_PASS_WITH_FIXES
HOLD_WITH_FAILURES
NO_GO
```

## 7. HOLD Conditions

HOLD if:

- artifact path contains real or masked-real data;
- Dify output includes secrets or credential-bearing text;
- model output is customer-visible before a separate gate;
- Qwen output is manually rewritten instead of preserved;
- fewer than 20 UAT outputs are produced without an explicit HOLD explanation;
- scoring artifacts are missing;
- GPU metrics are missing;
- reviewer assignment remains absent at S0 closeout;
- execution requires backend/runtime/API/schema or connector changes.

## 8. Non-Authorization

This confirmation does not authorize:

```text
Qwen execution without explicit run authorization
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

## 9. Next Route

```text
OPEN_QWEN_RUNTIME_STABILITY_FIX_AND_S0_RERUN
```
