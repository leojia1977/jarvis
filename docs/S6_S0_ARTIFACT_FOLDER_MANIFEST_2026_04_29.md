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
WAIT_FOR_CLOUD_QWEN_OUTPUT_ARTIFACTS
```

