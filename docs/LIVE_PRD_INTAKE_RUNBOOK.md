# Live PRD Intake Runbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Live PRD Intake Runbook |
| Status | Green docs-only live-intake runbook baseline |
| Scope | Convert the autonomous delivery rehearsal into an executable checklist for the first real PRD or explicit product direction |
| Snapshot | S5-LIVE-PRD-INTAKE-RUNBOOK-METRICS-2026-04-22-001 |
| Stage | s5-live-prd-intake-runbook-metrics |
| Baseline commit | `6eb2cd809c89d989b1c8f91d2b5328212b1ea18d` |
| Baseline snapshot | S5-AUTONOMOUS-DELIVERY-DRY-RUN-REHEARSAL-2026-04-22-001 |
| Baseline manifest status | PASS |
| Route | `OPEN_LIVE_PRD_INTAKE_RUNBOOK_METRICS_STAGE` |
| Lane | Green docs-only |

This runbook is the first-response checklist for the next real PRD or explicit product direction. It turns rehearsal controls into a live intake path, while preserving the current waiting posture until product input exists.

It does not authorize implementation, code/test changes, SWE product execution, launch, deployment, real-data handling, credential handling, public endpoint work, parked-stream reopen, Red execution, AI_COLLAB changes, staging, commit, or push outside governed closeout rules.

## 2. Start Trigger

Start this runbook only when at least one governed product input exists:

- latest PRD supplied in the current thread
- explicit product direction supplied by Human/Jarvis
- governed PRD file added or identified inside the source root
- governed product decision that replaces or amends a PRD

For autonomous ops-loop use, the product input must first pass:

```text
docs\PRD_INTAKE_AUTOMATION_TRIGGER_RULES.md
docs\PRD_INTAKE_RUN_TRIGGER.md
```

If none exists, stop with:

```text
WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION
```

Do not infer product goals from roadmap history, parked items, earlier backlog, model suggestions, or convenience.

## 3. Required Intake Inputs

Before route selection, collect and record:

| Input | Required evidence | Missing result |
| --- | --- | --- |
| PRD/source identifier | filename, thread reference, or explicit product direction text | `HOLD_NO_PRODUCT_SOURCE` |
| PRD/source timestamp | date/time or supplied version marker | `NEEDS_GREEN_DOCS_ONLY_INTAKE_PREP` |
| Current baseline | manifest snapshot, release PASS, commit | `HOLD_BASELINE_UNKNOWN` |
| Authority source | Human/Jarvis/product/governance source | `HOLD_AUTHORITY_UNKNOWN` |
| Data mode | synthetic/local, external, real-data, or unknown | `HOLD_IF_UNKNOWN` |
| Review need | Claude Web, Claude Code, Human/Jarvis, external/security/privacy | `NEEDS_REVIEW_ROUTE` |
| Claude Web availability | available, usage-limited until timestamp, or unknown | `NEEDS_CLAUDE_WEB_REVIEW` or `HOLD_PENDING_CLAUDE_WEB_RESET` |

## 4. Live Intake Checklist

Use this sequence for the first real PRD:

```text
1. Record intake_start_at.
2. Confirm source root is D:\产品设计\New folder.
3. Read DELEGATED_APPROVER_CHARTER and verify delegation_expires when autonomous policy applies.
4. Load current manifest, HANDOFF, PRODUCT_STATE, ROADMAP_AND_PARKED_ITEMS, GOVERNANCE_DECISION_LOG, AUTONOMOUS_HOLD_QUEUE, AUTONOMOUS_AUTHORIZATION_POLICY, AUTONOMOUS_DELIVERY_PIPELINE, SWE_AUTONOMOUS_DELIVERY_ACCELERATION_PLAYBOOK, TICKET_READINESS_CHECKLIST, and this runbook.
5. Record current git status.
6. Register PRD/source identifier and timestamp.
7. Check for secrets, raw customer data, credentials, cookies, tokens, auth headers, browser sessions, or unredacted evidence.
8. If unsafe material is present, stop and request redacted/governed input.
9. Summarize product goals in 3-7 bullets.
10. Summarize non-goals in 3-7 bullets.
11. List changed assumptions versus the current baseline.
12. List affected product areas and parked boundaries.
13. Identify candidate routes.
14. Classify each route by lane.
15. Identify required review path.
16. Identify likely HOLD triggers.
17. Create or update LIVE_PRD_INTAKE_METRICS_RECORD.md as the timing and evidence ledger.
18. Decide whether route selection can proceed.
19. If route selection proceeds, open OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE.
20. If route selection cannot proceed, record HOLD and missing input.
```

## 5. Timebox

The target first-pass timebox is:

| Window | Target output |
| --- | --- |
| T+0 to T+5 min | intake source registered, baseline confirmed |
| T+5 to T+15 min | safety/data/credential screen complete |
| T+15 to T+30 min | goals, non-goals, changed assumptions drafted |
| T+30 to T+45 min | affected areas, parked boundaries, candidate routes drafted |
| T+45 to T+60 min | lane classification, review path, HOLD triggers drafted |
| T+60 to T+75 min | ticket-readiness precheck and metrics record updated |
| T+75 to T+90 min | route-selection recommendation or HOLD reported |

Exceeding the timebox is allowed only if the metrics record captures why.

## 6. Claude Web Handling

Claude Web handles product, architecture, governance, high-risk, Red, and HOLD review when required.

Availability states:

- `AVAILABLE_FOR_REVIEW`
- `USAGE_LIMITED_UNTIL_<timestamp>`
- `UNKNOWN_AVAILABILITY`
- `REVIEW_QUEUED`
- `REVIEW_PASS`
- `REVIEW_PASS_WITH_FINDINGS`
- `REVIEW_HOLD`

Rules:

- If Claude Web is usage-limited, record `REVIEW_QUEUED` or `HOLD_PENDING_CLAUDE_WEB_RESET`.
- Claude Code cannot replace Claude Web architecture/governance review.
- Codex may copy the Claude Web prompt into the prompt ledger, but copied prompt text is not a verdict.
- No AdsPower profile creation/switching, Claude Web login automation, cookie/session/token/auth-header/browser-storage/profile-file inspection, or conversation-history reading is authorized.

The current known limit from the rehearsal baseline is:

```text
USAGE_LIMITED_UNTIL_2026-04-23_01:00_ASIA_SHANGHAI
```

For any later live run, verify current availability instead of assuming the limit is still active or cleared.

## 7. Prompt Routing Order

Codex owns prompt copying and routing records.

Default order:

```text
1. Human/Jarvis clarification prompt if product source or authority is missing.
2. Claude Web route/governance prompt if product, architecture, governance, high-risk, Red, or HOLD boundaries are touched.
3. Ticket Readiness Record prompt after route candidate exists.
4. SWE prompt only after exact Yellow item explicitly authorizes bounded implementation accelerator use.
5. Claude Code focused review prompt only after Codex has a bounded implementation diff.
```

Do not send SWE or Claude Code prompts during PRD intake unless the later exact route and ticket permit it.

## 8. Route Selection Admission

Route selection may proceed only when the intake record names:

- product source
- baseline snapshot and commit
- product goals
- non-goals
- changed assumptions
- affected areas
- candidate routes
- lane for each route
- review requirements
- HOLD triggers
- next governed artifact

If the PRD touches product/architecture/governance/high-risk boundaries and Claude Web is unavailable, route selection may draft a package but must not claim review PASS.

## 9. Ticket Readiness Precheck

Before opening an exact ticket, run `docs\TICKET_READINESS_CHECKLIST.md`.

The intake stage may produce:

- `READY_FOR_ROUTE_SELECTION`
- `NEEDS_CLAUDE_WEB_REVIEW`
- `NEEDS_HUMAN_OR_JARVIS_GO`
- `NEEDS_GREEN_DOCS_ONLY_INTAKE_PREP`
- `HOLD`

The intake stage cannot produce:

- implementation authority
- SWE execution authority
- release authority for product changes
- launch/deployment authority
- external pilot execution authority

## 10. Metrics Record Requirement

Every live PRD intake must create or update:

```text
docs\LIVE_PRD_INTAKE_METRICS_RECORD.md
```

The record must capture:

- timestamps
- elapsed time
- review queue time
- route decision time
- HOLD causes
- prompt routing state
- SWE eligibility state
- anti-generalization findings
- scope change count
- next artifact

## 11. Stop Conditions

Stop and record HOLD if:

- PRD/source is missing
- PRD contains secrets, raw customer data, credentials, cookies, tokens, auth headers, browser sessions, or unredacted evidence
- product authority is unclear
- route touches Red-3
- real-data handling is required but not governed
- external pilot execution or readiness claim is implied
- public endpoint work is implied
- S5-B/S5-D/ORDIV reopen is implied without explicit governed reopen
- AI_COLLAB changes are requested without separate AI_COLLAB governance route
- Claude Web is required but unavailable and no alternate authorized reviewer is named
- a model proposes speculative helper/module/registry/framework/service/reusable abstraction/future-proofing beyond the PRD

## 12. Output Template

```text
LIVE_PRD_INTAKE_SUMMARY
Snapshot:
Baseline commit:
PRD/source:
Intake started:
Intake completed:
Goals:
Non-goals:
Changed assumptions:
Affected areas:
Parked boundary impact:
Candidate routes:
Lane classification:
Required review:
Claude Web state:
Ticket readiness precheck:
SWE eligibility:
HOLDs:
Anti-generalization findings:
Metrics record:
Decision:
Next governed artifact:
```

Allowed `Decision` values:

- `READY_FOR_ROUTE_SELECTION`
- `NEEDS_CLAUDE_WEB_REVIEW`
- `NEEDS_HUMAN_OR_JARVIS_GO`
- `NEEDS_GREEN_DOCS_ONLY_INTAKE_PREP`
- `HOLD`

## 13. Non-Authorization

This runbook does not authorize:

- implementation
- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime/API/schema behavior changes
- release script changes
- contract changes
- AI_COLLAB changes
- Yellow implementation
- SWE product execution
- direct SWE repo writes
- Red execution
- launch execution
- production deployment
- external pilot execution or readiness claims
- credential handling
- real-data handling
- evidence retention or redaction policy freeze
- public endpoint work
- S5-B/S5-D reopen
- ORDIV work
- S4-A resolver change
- Red-3 action
- AdsPower profile creation/switching
- Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection
- staging, commit, or push outside governed closeout rules

## 14. Next Use

When the latest PRD or explicit product direction arrives, use this runbook first, then open:

```text
OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE
```

If no PRD or explicit product direction exists, remain in:

```text
WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION
```
