# S6 S0 Artifact Folder Manifest 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | S0 artifact folder manifest |
| Date | 2026-04-29 |
| Current repo artifacts | Synthetic input artifacts only |

## 2. Decision

```text
S0_ARTIFACT_FOLDER_MANIFEST_CREATED
INPUT_ARTIFACTS_READY
OUTPUT_ARTIFACTS_PENDING_QWEN_HANDOFF
```

## 3. Current Repo Artifact Folders

| Folder | Status | Contents |
| --- | --- | --- |
| `mock_data/s0_synthetic/caseview/` | Ready | 20 synthetic CaseView input JSON files. |
| `mock_data/s0_synthetic/qwen_fact_bundle/` | Ready | 20 synthetic QwenFactBundle input JSON files. |
| `mock_data/s0_synthetic/README.md` | Ready | Boundary and usage notes. |

## 4. Future Non-Repo Or Import Candidate Folders

These are conventions only. They are not created or authorized by this record.

| Candidate folder | Purpose | Status |
| --- | --- | --- |
| `s0/output/qwen/` | Cloud Qwen model outputs | Pending cloud handoff. |
| `s0/output/scans/` | Action-command scan results | Pending model outputs. |
| `s0/output/metrics/` | GPU runtime metrics | Pending cloud handoff. |
| `s0/report/` | Final S0 evaluation report | Pending scoring. |

## 4A. 2026-04-30 Local S0 Output Path Confirmation

Follow-up record:

```text
docs\S6_DIFY_S0_APP_CONFIG_AND_ARTIFACT_PATH_CONFIRMATION_2026_04_30.md
```

Confirmed local artifact path convention:

```text
D:\产品设计\New folder\artifacts\s0_qwen_runs\2026-04-30-001\
```

Recommended folder structure:

```text
outputs\
scoring\
metrics\
notes\
manifest.json
```

This path is a local artifact convention. Raw Qwen outputs and detailed Dify run logs do not need to be committed to Git. Repo closeout should import only safe manifests, scoring summaries, and governed reports unless separately authorized.

## 4B. 2026-04-30 S0 Run Artifact Creation

Execution report:

```text
docs\S6_S0_QWEN_SYNTHETIC_RUN_EXECUTION_REPORT_2026_04_30.md
```

Created artifact root:

```text
artifacts\s0_qwen_runs\2026-04-30-001\
```

Artifact decision:

```text
S0_DECISION = HOLD_WITH_FAILURES
PASS = UAT-01 / UAT-02 / UAT-03
FAIL_NEEDS_FIX = UAT-04 through UAT-20 due qwen-72b runtime connection failure
```

## 5. Import Rules

Any future output import must:

- include an output manifest;
- map each output to `UAT-01` through `UAT-20`;
- include hashes or equivalent integrity identifiers;
- exclude credentials and secrets;
- exclude real and masked-real data;
- preserve raw model output without manual rewriting;
- clearly separate model output from evaluator judgment.

## 6. Non-Authorization

This manifest does not authorize:

```text
Qwen execution
output import
real data
masked real data
backend/runtime/API/schema
connector changes
secrets
Jira mutation
deploy
external pilot
launch
```

## 7. Next Route

```text
OPEN_QWEN_RUNTIME_STABILITY_FIX_AND_S0_RERUN
```
