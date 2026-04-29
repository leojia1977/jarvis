# S6 Offline Synthetic Mapping Tooling Tickets 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Offline synthetic tooling ticket pack |
| Date | 2026-04-29 |
| Applies to | Pre-shadow synthetic safety tooling |
| Current lane | Docs-only ticket preparation |

## 2. Decision

```text
OFFLINE_SYNTHETIC_MAPPING_TOOLING_TICKETS_OPENED
MAP_T01_MASKING_VALIDATOR_CHECKLIST_READY
MAP_T02_REDACTION_HARD_STOP_SCANNER_CHECKLIST_READY
MAP_T03_QWEN_FACT_BUNDLE_SYNTHETIC_BUILDER_CHECK_READY
IMPLEMENTATION_GO_REQUIRED_FOR_CODE
```

These tickets are pre-shadow synthetic safety tooling. They do not connect to real data, masked-real data, customer data, connectors, backend/runtime/API/schema, deploy, external pilot, or launch.

## 3. Ticket Summary

| Ticket | Purpose | Current state |
| --- | --- | --- |
| `MAP-T01` | Masking Validator | `IMPLEMENTATION_GO_REQUIRED` |
| `MAP-T02` | Redaction Hard Stop Scanner | `IMPLEMENTATION_GO_REQUIRED` |
| `MAP-T03` | QwenFactBundle Synthetic Builder Check | `IMPLEMENTATION_GO_REQUIRED` |

## 4. MAP-T01 Masking Validator

### 4.1 Scope

Validate that governed masking rules can be mechanically applied to synthetic samples before any future S1 shadow gate.

### 4.2 Required Synthetic Cases

| Input pattern | Expected synthetic-safe result |
| --- | --- |
| `192.168.1.42` | `192.168.1.x` or equivalent governed masked IP |
| `jsmith@corp.example` | `user_[hash4]` or equivalent governed alias |
| `ws-finance-042` | `host_finance_ws_042` or `host_[hash]` |
| `-token abc123` | `-token [REDACTED]` |
| `Authorization: Bearer abc123` | `[REDACTED_AUTHORIZATION_HEADER]` |
| `-----BEGIN PRIVATE KEY-----` | `HOLD_REJECT_SECRET_BEARING_INPUT` |

### 4.3 Acceptance

MAP-T01 PASS requires:

- synthetic-only test inputs;
- deterministic expected outputs;
- explicit rejection of key/token/private-key patterns;
- no connector or real-data source;
- no backend/runtime/API/schema changes unless separately authorized.

## 5. MAP-T02 Redaction Hard Stop Scanner

### 5.1 Scope

Scan synthetic candidate payloads and block secret-bearing text before any future S1 pipeline consideration.

### 5.2 Required Hard Stop Patterns

```text
password=
passwd=
Authorization:
Bearer
api_key
secret
token=
private key
session cookie
-----BEGIN
```

### 5.3 Acceptance

MAP-T02 PASS requires:

- all hard-stop patterns detected in synthetic test strings;
- safe-list examples for documentation text that quotes forbidden patterns without becoming data;
- HOLD result when a payload resembles credentials;
- no output that preserves the secret value;
- no connector, backend, runtime, API, or schema changes.

## 6. MAP-T03 QwenFactBundle Synthetic Builder Check

### 6.1 Scope

Verify that QwenFactBundle input contains only deterministic synthetic facts, masked aliases, source limitations, unsupported claims, and forbidden-output instructions.

### 6.2 Forbidden Inputs

QwenFactBundle must not contain:

- raw event JSON;
- unmasked identity;
- raw command line with secrets;
- tokens;
- private keys;
- session cookies;
- P3-forbidden host raw evidence;
- connector payloads;
- real or masked-real records.

### 6.3 Acceptance

MAP-T03 PASS requires:

- synthetic-only builder or validation test;
- `fixture_meta.synthetic_only = true`;
- `fixture_meta.real_data_derived = false`;
- unsupported claims preserved;
- source limitations preserved;
- forbidden-output list preserved;
- no model output fabrication.

## 7. Shared Allowed Files For Future Implementation

Future implementation checklists may propose exact files only after GO. Candidate areas must remain synthetic/offline, for example:

```text
scripts/
backend/tests/ or dedicated test-only validator location
mock_data/s0_synthetic/
docs/
```

No file is authorized by this ticket pack yet.

## 8. Shared HOLD Conditions

HOLD if:

- implementation requires real or masked-real data;
- implementation requires connector access;
- implementation requires backend/runtime/API/schema changes not separately authorized;
- implementation needs secrets or credentials;
- implementation changes Qwen prompts, model runtime, output parser, fixture adapter, `ContextValidator`, or `ResolvedSurfaceContext`;
- exact allowed files or test command cannot be named.

## 9. Non-Authorization

This ticket pack does not authorize:

```text
code changes
real data
masked real data
connector changes
backend/runtime/API/schema
secrets
Qwen execution
deploy
external pilot
launch
```

## 10. Next Route

```text
WAIT_FOR_MAP_T01_T02_T03_IMPLEMENTATION_GO
```
