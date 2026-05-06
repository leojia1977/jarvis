# S6 Fast MVP Qwen Cloud Adapter Spec 2026-05-06

## 1. Purpose

This document defines how SecuPilot should approach a future Qwen cloud adapter without blocking the current local/offline trial candidate.

Current decision:

```text
QWEN_CLOUD_NOT_REQUIRED_FOR_LOCAL_OFFLINE_TRIAL_RC_001
```

This document is design-only. It does not authorize live Qwen/API calls, credentials, secrets, connector work, real data, masked-real data, customer-visible output, deployment, or production write-back.

## 2. Why Qwen Cloud Is Not The First Blocker

The fastest product path is to prove the review loop first:

```text
artifact generated
artifact validated
workbench renders the run
reviewer can understand status and cases
local demo package can be shared for controlled review
feedback can be collected
```

That loop can be proven with `fixture` and `external-output` providers. Cloud Qwen should improve model realism later, but it should not delay RC-001.

## 3. Adapter Phases

| Phase | Name | Status | Allowed now |
| --- | --- | --- | --- |
| P0 | Fixture provider | `ACTIVE` | Yes |
| P1 | External-output metadata provider | `ACTIVE` | Yes |
| P2 | Qwen cloud synthetic-only dry run | `DESIGN_READY_ONLY` | No, needs later explicit GO |
| P3 | Qwen cloud masked/real-data pilot | `NOT_AUTHORIZED` | No |
| P4 | Production Qwen integration | `NOT_AUTHORIZED` | No |

## 4. Future Adapter Contract

A future Qwen cloud adapter should transform a validated S1 artifact into a model request and transform the model response back into SecuPilot artifact fields.

Expected adapter shape:

```text
input: validated S1 run artifact or approved synthetic package
request builder: whitelist-only prompt/request construction
model call: cloud Qwen call behind explicit runtime flag
response parser: structured JSON validation
artifact writer: metadata-only model output artifact
safety scanner: forbidden field and credential scan before retention
```

The adapter should never pass raw payloads through by default.

## 5. Allowed Request Fields For Synthetic-Only Dry Run

Allowed fields:

```text
run_id
case_id
title
summary
severity
risk_level
evidence_metadata_refs
synthetic_context_summary
detector_name
rule_id
timestamp_metadata
limitation_note
```

Forbidden fields:

```text
raw_payload
raw_evidence
raw_log
raw_event
customer_record
customer_visible_message
secret
token
auth_header
cookie
private_key
credential
action_command
writeback_action
production_connector_output
```

## 6. Expected Response Fields

Allowed response fields:

```text
case_id
model_summary
risk_explanation
reviewer_action
confidence
score
limitation_note
model_name
provider
generated_at_utc
```

The adapter must reject responses containing forbidden fields or unexpected top-level fields unless a later schema revision explicitly allows them.

## 7. Runtime Configuration Names

Future runtime configuration may use environment variable names like:

```text
SECUPILOT_QWEN_PROVIDER_ENABLED
SECUPILOT_QWEN_API_BASE
SECUPILOT_QWEN_MODEL
SECUPILOT_QWEN_TIMEOUT_SECONDS
SECUPILOT_QWEN_MAX_RETRIES
SECUPILOT_QWEN_SYNTHETIC_ONLY
```

Secret-bearing values must never be stored in repo docs, code comments, test fixtures, committed artifacts, or chat.

Any API key or token must be supplied only by a human-controlled local environment or a proper secret manager after a separate explicit GO.

## 8. Required Safety Controls Before First Cloud Dry Run

Before any synthetic-only Qwen cloud dry run, these controls must exist:

| Control | Required result |
| --- | --- |
| Explicit GO | Names Qwen cloud, data mode, run id, operator, and artifact root |
| Data mode | `SYNTHETIC_ONLY` |
| Runtime flag | Cloud provider disabled by default |
| Prompt builder | Whitelist-only fields |
| Response parser | Strict schema validation |
| Artifact scanner | Rejects secrets, tokens, raw payloads, auth headers, customer-visible messages, and write-back actions |
| No write-back | Adapter cannot invoke connector or action execution |
| No customer-visible output | Adapter output remains local artifact only |
| Cost/time guard | Timeout and retry bounds configured |

## 9. HOLD Conditions

Stop instead of running Qwen cloud if any condition is true:

```text
no explicit Qwen cloud dry-run GO
input contains real data or masked-real data
input contains raw payload or raw logs
API key or token appears in repo, docs, command line, logs, artifacts, or chat
provider flag defaults to enabled
request builder accepts non-whitelisted fields
response parser accepts unexpected fields
adapter attempts connector action or write-back
adapter produces customer-visible output
timeout/retry/cost guard is missing
```

## 10. Recommended Next Step

Do not implement the cloud adapter before RC-001 review readiness.

Recommended order:

```text
complete MVP-10 through MVP-13
run LOCAL_OFFLINE_TRIAL_RC_001 checks
collect reviewer feedback
then decide whether QWEN_CLOUD_SYNTHETIC_ONLY_DRY_RUN_GO is worth authorizing
```
