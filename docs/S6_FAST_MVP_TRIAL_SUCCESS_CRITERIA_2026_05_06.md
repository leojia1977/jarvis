# S6 Fast MVP Trial Success Criteria 2026-05-06

## 1. Purpose

This document defines what success means for the first Fast MVP local/offline trial candidate.

Candidate:

```text
LOCAL_OFFLINE_TRIAL_RC_001
```

The goal is to decide whether the product loop is useful enough to keep iterating toward a controlled customer trial.

## 2. Trial Hypothesis

SecuPilot is worth advancing if a reviewer can use the local/offline workbench and package to understand:

```text
what happened
why it matters
what evidence exists
what action a reviewer should take next
whether the run is safe to retain and review
```

This must be true without real data, masked-real data, live Qwen/API, live connectors, production write-back, or customer-visible publishing.

## 3. Minimum Success Metrics

| Metric | PASS target | Collection method |
| --- | --- | --- |
| First understanding | Reviewer understands run status within 2 minutes | Feedback form |
| Case comprehension | Reviewer can explain at least 3 displayed cases | Feedback form |
| Evidence trust | Reviewer can identify evidence references without raw payload exposure | Feedback form and package review |
| Reviewer action | Reviewer knows the next action for each case | Workbench review |
| Safety confidence | Reviewer sees no raw payload, secret, token, auth header, or write-back implication | Safety review |
| Package portability | Local package can be inspected without repo-specific absolute paths | Package manifest review |

## 4. Product Quality Threshold

The candidate may proceed to the next iteration if:

```text
no P0 finding
no P1 safety or data-boundary finding
at most two P1 usability findings with clear fixes
artifact validator passes
local demo package builds
frontend tests and build pass
reviewer decision is PASS or PASS_WITH_NOTES
```

The candidate must hold if:

```text
any forbidden data appears
any write-back or connector action is attempted
any customer-visible publish/deploy is implied
reviewer cannot understand the core run status
artifact validator fails
package manifest cannot be trusted
```

## 5. Feedback Severity

Use this severity scale:

| Severity | Meaning | Required response |
| --- | --- | --- |
| P0 | Safety boundary breach or trial cannot proceed | Stop and fix before any further review |
| P1 | Core workflow blocked or reviewer cannot trust result | Fix before next RC |
| P2 | Workflow understandable but slower or confusing | Prioritize in next iteration |
| P3 | Polish, wording, or layout issue | Batch into normal iteration |

## 6. Decision Outcomes

Allowed outcomes:

```text
PASS_TO_NEXT_LOCAL_RC
PASS_WITH_NOTES_TO_NEXT_LOCAL_RC
HOLD_FOR_FIXES
NO_GO_FOR_CURRENT_PRODUCT_PATH
```

Forbidden interpretations:

```text
production ready
customer-visible ready
external pilot authorized
real-data ready
live Qwen/API authorized
production connector authorized
write-back authorized
```

## 7. Next Iteration Choices

After RC-001 feedback, choose exactly one primary next step:

| Choice | When to choose |
| --- | --- |
| Improve workbench UX | Reviewer can understand artifacts but screen flow is slow or unclear |
| Improve artifact quality | Reviewer wants different case fields, evidence summaries, or action fields |
| Improve package portability | Reviewer needs easier offline review and handoff |
| Prepare Qwen cloud synthetic-only dry run | Fixture/external-output loop is useful and model realism is the next bottleneck |
| Hold product path | Feedback shows the current value proposition is not landing |

## 8. Recommended Decision Rule

Do not move to cloud Qwen or real customer trial just because the local package exists.

Move only when the reviewer feedback proves that the local product loop is useful and the next bottleneck is model realism or external review, not basic usability, evidence trust, or safety.
