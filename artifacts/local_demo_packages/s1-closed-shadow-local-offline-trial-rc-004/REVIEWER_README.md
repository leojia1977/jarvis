# SecuPilot S1 Local Demo Package

## Scope

This package is for local/offline reviewer inspection only.

Allowed review:

```text
synthetic S1 run status
metadata-only case summary
artifact manifest and SHA256 values
safety scan summary
reviewer notes and follow-up decisions
local browser review decision preview
```

Not allowed from this package:

```text
real data
masked-real data
live Qwen/API calls
live connector setup
production credentials
production write-back
customer-visible publish/deploy
external pilot execution
```

## Files

Start with `package_manifest.json`, then inspect `final_status.json`, `case_summary.json`, `artifact_manifest.json`, and `safety_scan.json`.

Visual screenshots are packaged under `playwright/`.

Source artifact root:

```text
artifacts/s1_closed_shadow_runs/2026-04-30-001
```

Package root:

```text
artifacts/local_demo_packages/s1-closed-shadow-local-offline-trial-rc-004
```

## Reviewer Checks

```text
run status is understandable
case count matches expected synthetic bundle
evidence references are metadata-only
no raw payloads, credentials, tokens, auth headers, or customer logs appear
no write-back or deployment path appears
local review decision preview does not write artifacts or call external systems
reviewer action is clear
```

Record feedback in the repo feedback form or a governed review note without pasting raw customer data or secrets.
