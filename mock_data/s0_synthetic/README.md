# S0 Synthetic Payloads

This directory contains fully artificial S0 synthetic-only payload artifacts generated from governed repo manifest records.

## Scope

- CaseView synthetic payloads: `caseview/*.json`
- QwenFactBundle synthetic payloads: `qwen_fact_bundle/*.json`
- Scenario range: UAT-01 through UAT-20

## Boundaries

These files contain no real data, no masked-real data, no customer data, no connector payloads, no credentials, no secrets, and no Qwen model outputs.

They do not authorize Qwen execution, real-data shadow, backend/runtime/API/schema changes, deployment, external pilot, launch, or customer-visible output.

## Required Use

Use these artifacts only as synthetic inputs for a later authorized S0 dry run. Qwen cloud runtime handoff is still required before model execution.
