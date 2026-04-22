# PRD Intake Automation Trigger Rules

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | PRD Intake Automation Trigger Rules |
| Status | Green docs-only automation trigger rules baseline |
| Scope | Define when autonomous ops may open live PRD intake and when it must keep waiting |
| Snapshot | S5-PRD-INTAKE-AUTOMATION-TRIGGER-2026-04-22-001 |
| Stage | s5-prd-intake-automation-trigger |
| Baseline commit | `47f86dc4249155a30bc617eb26f522f9caf4b739` |
| Baseline snapshot | S5-LIVE-PRD-INTAKE-RUNBOOK-METRICS-2026-04-22-001 |
| Baseline manifest status | PASS |
| Route | `OPEN_PRD_INTAKE_AUTOMATION_TRIGGER_STAGE` |
| Lane | Green docs-only |

These rules connect the live PRD intake runbook to the autonomous ops loop. They define when the loop may start intake, what evidence must exist, and which cases remain waiting or HOLD.

They do not authorize implementation, code/test changes, SWE product execution, launch, deployment, external pilot execution, real-data handling, credential handling, public endpoint work, parked-stream reopen, Red execution, AI_COLLAB changes, staging, commit, or push outside governed closeout rules.

## 2. Trigger Objective

The objective is to reduce time from PRD arrival to route-selection readiness without inventing product scope.

Automation may only trigger:

```text
LIVE_PRD_INTAKE_RUNBOOK
```

and may only produce:

- intake started
- route-selection readiness
- review needed
- human/Jarvis input needed
- HOLD
- wait state

It may not produce implementation authority, SWE execution authority, launch authority, or external pilot readiness.

## 3. Positive Trigger Conditions

The autonomous ops loop may open live PRD intake when one of these exists in the current governed context:

| Trigger | Required evidence | Intake action |
| --- | --- | --- |
| Latest PRD pasted or attached in the current thread | Human/product source says it is the latest PRD, or clearly provides a complete PRD-like product source | Start `docs\LIVE_PRD_INTAKE_RUNBOOK.md` |
| Explicit product direction | Human/Jarvis gives a direct product direction with enough source authority to start intake | Start runbook; mark source type `explicit_product_direction` |
| Governed PRD file identified inside source root | File path under `D:\产品设计\New folder` is named as current PRD or product source | Start runbook after reading only that governed file and baseline docs |
| Governed replacement or amendment | Human/Jarvis states that a product decision replaces or amends prior PRD scope | Start runbook; record amendment source |
| Existing ops-loop wakeup includes product source | The wakeup prompt carries a concrete PRD/source, not a generic reminder | Start runbook |

If multiple candidate PRDs appear, use the most recent human/product-declared source. If recency or authority is ambiguous, do not choose; return `HOLD_MULTIPLE_PRODUCT_SOURCES`.

## 4. Non-Trigger Conditions

Do not open live intake for:

- discussion about how to use PRDs
- expectation that a PRD will arrive later
- placeholder titles without content
- old PRD references without a current authority statement
- roadmap or parked-item history alone
- model-generated feature ideas
- product brainstorms that are not explicit direction
- files outside `D:\产品设计\New folder`
- untracked files unless the user explicitly identifies them as governed input for intake
- screenshots, images, spreadsheets, or external links that contain secrets, raw customer data, credentials, cookies, tokens, auth headers, browser sessions, or unredacted evidence
- Claude Web availability changes alone
- SWE availability changes alone
- gate or release status changes alone

Non-trigger result:

```text
WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION
```

## 5. Safety Screen Before Intake

Before live intake starts, Codex must screen the source for:

- secrets
- credentials
- API keys
- tokens
- cookies
- auth headers
- browser/session material
- raw customer data
- unredacted customer/operator evidence
- external-system payloads
- legal/commercial commitments
- launch or deployment instructions
- public endpoint activation
- Red-3 actions

If present, stop with:

```text
HOLD_UNSAFE_PRODUCT_SOURCE_REDACTION_REQUIRED
```

Do not paste unsafe content into Claude Web, Claude Code, SWE, prompts, metrics records, or release artifacts.

## 6. Trigger State Machine

```text
WAITING_FOR_PRD
-> CANDIDATE_PRODUCT_SOURCE_DETECTED
-> PRODUCT_SOURCE_AUTHORITY_CHECK
-> PRODUCT_SOURCE_SAFETY_SCREEN
-> LIVE_PRD_INTAKE_STARTED
-> METRICS_RECORD_STARTED
-> ROUTE_SELECTION_READY
```

Alternate outcomes:

```text
WAITING_FOR_PRD
HOLD_NO_PRODUCT_SOURCE
HOLD_MULTIPLE_PRODUCT_SOURCES
HOLD_AUTHORITY_UNKNOWN
HOLD_UNSAFE_PRODUCT_SOURCE_REDACTION_REQUIRED
NEEDS_HUMAN_OR_JARVIS_GO
NEEDS_CLAUDE_WEB_REVIEW
HOLD_PENDING_CLAUDE_WEB_RESET
```

## 7. Debounce And Idempotency

To avoid duplicate intake runs:

- Use the tuple `source_id + source_timestamp + baseline_snapshot` as the intake key.
- If an intake record already exists for the same tuple and remains in progress, do not start a second intake.
- If a newer PRD/source arrives, close the old intake as superseded only through a governed note.
- If route selection has already started for the tuple, do not reopen intake unless the product source changes.
- If the ops loop wakes repeatedly while waiting, report waiting state without editing metrics.

Do not modify `docs\LIVE_PRD_INTAKE_METRICS_RECORD.md` during a no-PRD wait run.

## 8. Automation Input Boundary

Allowed trigger inputs:

- current thread user message
- repo-governed files under `D:\产品设计\New folder`
- existing manifest, handoff, rolling maps, governance docs
- current git status
- explicit Human/Jarvis product direction

Not allowed as trigger truth:

- files outside the source root
- old release zips
- old copied folders
- browser history or Claude conversation history
- AdsPower profile data
- cookies, tokens, auth headers, local/session storage, profile files
- model memory not present in governed docs or current user input

## 9. Run Trigger Link

When a positive trigger is confirmed, execute:

```text
docs\PRD_INTAKE_RUN_TRIGGER.md
```

The run trigger must call:

```text
docs\LIVE_PRD_INTAKE_RUNBOOK.md
docs\LIVE_PRD_INTAKE_METRICS_RECORD.md
```

and then decide whether to open:

```text
OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE
```

## 10. Non-Authorization

These trigger rules do not authorize:

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

## 11. Next Use

The autonomous ops loop should apply these trigger rules on every run before selecting speculative product work.

If no positive trigger exists, the loop must keep:

```text
WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION
```
