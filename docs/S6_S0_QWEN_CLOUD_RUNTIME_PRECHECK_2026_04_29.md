# S6 S0 Qwen Cloud Runtime Precheck 2026-04-29

## 1. Document Control

- Date: 2026-04-29
- Record type: cloud Qwen runtime precheck
- Applies to: S0 Synthetic Dry Run only
- Related manifest: `docs/S6_S0_UAT_SYNTHETIC_FIXTURE_MANIFEST_2026_04_29.md`

## 2. Decision

```text
QWEN_RUNTIME_LOCATION_CORRECTED_TO_CLOUD_GPU_TEST_SERVER
LOCAL_QWEN_INSTALL_NOT_REQUIRED
CLOUD_RUNTIME_HANDOFF_REQUIRED_BEFORE_S0_RERUN
```

Qwen is expected to run in the cloud GPU test-server environment, not on the local workstation. This precheck does not authorize real data, masked real data, secrets, backend/runtime/API/schema, connector changes, deploy, external pilot, launch, or customer-visible output.

## 3. Required Cloud Runtime Handoff

Before rerunning S0, the model/runtime owner must provide:

- cloud GPU environment identifier;
- Qwen model id and version;
- runtime invocation method;
- synthetic-only input transfer method;
- output artifact export path;
- GPU metrics capture method;
- prompt template version;
- evaluator script or manual runbook;
- named operator / reviewer;
- confirmation that no real or masked-real data will be sent;
- confirmation that no secrets are committed to repo.

## 4. Secret Handling Rule

No cloud credentials, API keys, server passwords, tokens, SSH keys, VPN credentials, or customer-specific connection details may be written into repo docs, source, fixtures, prompts, Jira, or logs.

If credentials are needed for execution, they must be handled outside repo through the approved secure channel and referenced only as:

```text
CREDENTIAL_HANDLED_OUT_OF_REPO
```

## 5. Runtime Boundary

Allowed:

```text
synthetic CaseView inputs
synthetic QwenFactBundle inputs
UAT-01 through UAT-20
offline Qwen evaluation
prompt injection tests
action-command keyword scan
GPU runtime metrics
S0 report completion
```

Forbidden:

```text
real data
masked real data
customer-visible output
production write-back
autonomous action
backend/runtime/API/schema changes
connector changes
secrets
deploy
external pilot
launch
```

## 6. Precheck Status Table

| Item | Status | Required before S0 rerun |
|---|---|---|
| Cloud GPU environment id | Pending | Yes |
| Qwen model id/version | Partial received: `qwen-72b` / Qwen2.5-72B-Instruct-Int4 / `/root/models/qwen2.5-72b-int4` | Yes |
| Invocation method | Received: vLLM 0.11.2 OpenAI-compatible API; qwen-72b at `http://192.168.10.139:8000/v1`; bge-m3 at `http://192.168.10.139:8001/v1` | Yes |
| Synthetic-only input transfer | Pending | Yes |
| Output artifact path | Pending export path; Dify PostgreSQL alone is not enough for repo intake | Yes |
| GPU metrics capture | Received: `ixsmi`, `~/gpu_snapshot.txt` | Yes |
| Prompt template version | Product-defined pending | Yes |
| Evaluator runbook/script | Pending | Yes |
| Credentials kept out of repo | Required | Yes |
| Real/masked-real data exclusion | Required | Yes |

## 7. S0 Rerun Gate

S0 may rerun only when:

```text
S0_UAT_SYNTHETIC_FIXTURE_MANIFEST_READY
CLOUD_QWEN_RUNTIME_HANDOFF_READY
CREDENTIALS_NOT_IN_REPO
SYNTHETIC_ONLY_BOUNDARY_CONFIRMED
```

## 8. Current Decision

```text
CURRENT_DECISION: HOLD_PENDING_CLOUD_QWEN_RUNTIME_HANDOFF
```

## 9. 2026-04-30 Dify Topology Reconciliation

Follow-up record:

```text
docs\S6_QWEN_CLOUD_HANDOFF_AND_DIFY_TOPOLOGY_RECONCILIATION_2026_04_30.md
```

Current updated decision:

```text
QWEN_CLOUD_ENVIRONMENT_HANDOFF_PARTIAL_PASS
DIFY_TOPOLOGY_RECONCILED_FOR_S0_SYNTHETIC_EVALUATION
S0_EXECUTION_STILL_HOLD_PENDING_DIFY_APP_CONFIG_AND_ARTIFACT_EXPORT_PATH
```
