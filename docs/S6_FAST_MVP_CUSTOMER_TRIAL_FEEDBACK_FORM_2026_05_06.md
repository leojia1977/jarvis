# S6 Fast MVP Customer Trial Feedback Form 2026-05-06

## 1. Purpose

This form captures reviewer feedback for the Fast MVP local/offline trial candidate.

Use it for:

```text
synthetic artifact review
approved metadata-only external-output review
local workbench review
local demo package review
```

Do not paste real customer data, masked-real data, credentials, tokens, auth headers, cookies, raw logs, raw payloads, screenshots containing customer records, or production connector output into this form.

## 2. Review Context

| Field | Value |
| --- | --- |
| Review date | `YYYY-MM-DD` |
| Reviewer | `PENDING` |
| Role | `PENDING` |
| Candidate | `LOCAL_OFFLINE_TRIAL_RC_001` |
| Artifact run | `artifacts/s1_closed_shadow_runs/2026-04-30-001` |
| Demo package | `artifacts/local_demo_packages/s1-closed-shadow-2026-04-30-001` |
| Data mode | `SYNTHETIC_OR_METADATA_ONLY_EXTERNAL_OUTPUT` |
| Customer-visible output | `NOT_AUTHORIZED` |
| Write-back | `DISABLED` |

## 3. Product Usefulness

| Question | Answer |
| --- | --- |
| Does the `/s1-run` view make the run status understandable within 2 minutes? | `YES / NO / PARTIAL` |
| Does the case summary expose the right fields for review? | `YES / NO / PARTIAL` |
| Are evidence references clear without showing raw payloads? | `YES / NO / PARTIAL` |
| Is the reviewer action obvious enough to continue the workflow? | `YES / NO / PARTIAL` |
| What is the single most confusing part? | `PENDING` |

## 4. Trust And Safety

| Question | Answer |
| --- | --- |
| Did you see any raw payload, secret, token, auth header, cookie, private key, customer log, or credential-like text? | `YES / NO` |
| Did any screen or package imply customer-visible publication or production deployment? | `YES / NO` |
| Did any artifact imply write-back or connector execution? | `YES / NO` |
| Would you allow this exact package for local/offline internal review? | `YES / NO / WITH_NOTES` |

If any answer is `YES` for an exposure or write-back concern, mark severity `P0` or `P1` and stop the trial review.

## 5. Usability Findings

| Finding ID | Severity | Screen/artifact | Finding | Suggested fix |
| --- | --- | --- | --- | --- |
| `F-001` | `P0/P1/P2/P3` | `PENDING` | `PENDING` | `PENDING` |

Severity guide:

```text
P0 blocks trial review or leaks forbidden material
P1 blocks core review workflow
P2 slows reviewer confidence or comprehension
P3 polish or wording issue
```

## 6. Trial Decision

| Field | Value |
| --- | --- |
| Reviewer decision | `PASS / PASS_WITH_NOTES / HOLD / NO_GO` |
| Required fix before next review | `PENDING` |
| Nice-to-have follow-up | `PENDING` |
| Can proceed to local/offline RC review package? | `YES / NO / WITH_NOTES` |

## 7. Non-Authorization Reminder

Completing this form does not authorize:

```text
real data
masked-real data
live Qwen/API
live connectors
production write-back
customer-visible publish/deploy
external pilot
production launch
push
```
