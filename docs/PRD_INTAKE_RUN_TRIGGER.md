# PRD Intake Run Trigger

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | PRD Intake Run Trigger |
| Status | Green docs-only run trigger baseline |
| Scope | Define the exact autonomous run packet after PRD intake trigger rules detect a governed product source |
| Snapshot | S5-PRD-INTAKE-AUTOMATION-TRIGGER-2026-04-22-001 |
| Stage | s5-prd-intake-automation-trigger |
| Baseline commit | `47f86dc4249155a30bc617eb26f522f9caf4b739` |
| Baseline snapshot | S5-LIVE-PRD-INTAKE-RUNBOOK-METRICS-2026-04-22-001 |
| Baseline manifest status | PASS |
| Route | `OPEN_PRD_INTAKE_AUTOMATION_TRIGGER_STAGE` |
| Lane | Green docs-only |

This run trigger defines the exact packet the autonomous ops loop should execute after `docs\PRD_INTAKE_AUTOMATION_TRIGGER_RULES.md` confirms a positive PRD/product-source trigger.

It does not authorize implementation, code/test changes, SWE product execution, launch, deployment, external pilot execution, real-data handling, credential handling, public endpoint work, parked-stream reopen, Red execution, AI_COLLAB changes, staging, commit, or push outside governed closeout rules.

## 2. Trigger Packet

Use this packet after a positive trigger:

```text
PRD_INTAKE_RUN_TRIGGER
Trigger source:
Trigger evidence:
Source id:
Source timestamp:
Baseline snapshot:
Baseline commit:
Manifest path:
Git status:
Delegation check:
Safety screen:
Claude Web state:
Runbook:
Metrics record:
Decision:
Next artifact:
```

Allowed `Decision` values:

- `START_LIVE_PRD_INTAKE`
- `READY_FOR_ROUTE_SELECTION`
- `NEEDS_CLAUDE_WEB_REVIEW`
- `NEEDS_HUMAN_OR_JARVIS_GO`
- `HOLD`
- `WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION`

## 3. Required Read Set

Every run trigger must read:

- `docs\DELEGATED_APPROVER_CHARTER.md`
- `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
- `docs\AUTONOMOUS_DELIVERY_PIPELINE.md`
- `docs\AUTONOMOUS_HOLD_QUEUE.md`
- `docs\PRODUCT_STATE.md`
- `docs\ROADMAP_AND_PARKED_ITEMS.md`
- `docs\GOVERNANCE_DECISION_LOG.md`
- `docs\HANDOFF.md`
- `docs\WAIT_FOR_PRD_AND_ROUTE_SELECTION_READINESS.md`
- `docs\SWE_AUTONOMOUS_DELIVERY_ACCELERATION_PLAYBOOK.md`
- `docs\AUTONOMOUS_DELIVERY_PROMPT_PACK.md`
- `docs\TICKET_READINESS_CHECKLIST.md`
- `docs\AUTONOMOUS_DELIVERY_DRY_RUN_REHEARSAL.md`
- `docs\LIVE_PRD_INTAKE_RUNBOOK.md`
- `docs\LIVE_PRD_INTAKE_METRICS_RECORD.md`
- `docs\PRD_INTAKE_AUTOMATION_TRIGGER_RULES.md`
- `releases\release_manifest.json`

If any required read fails, return:

```text
HOLD_REQUIRED_CONTEXT_UNREADABLE
```

## 4. Execution Steps

```text
1. Record run_trigger_started_at.
2. Confirm current repo root is D:\产品设计\New folder.
3. Confirm current branch and git status.
4. Verify delegation_expires when autonomous policy applies.
5. Confirm manifest verification status is PASS.
6. Apply PRD_INTAKE_AUTOMATION_TRIGGER_RULES.
7. If no positive trigger exists, report WAIT and stop without editing metrics.
8. If positive trigger exists, record source id, source timestamp, and source authority.
9. Run safety screen.
10. If unsafe material exists, HOLD and request redacted/governed source.
11. Start LIVE_PRD_INTAKE_RUNBOOK.
12. Create or update LIVE_PRD_INTAKE_METRICS_RECORD only after positive trigger and safety screen pass.
13. Record Claude Web state.
14. Copy prompt material only if needed; prompt copy is not review verdict.
15. Produce LIVE_PRD_INTAKE_SUMMARY.
16. Decide READY_FOR_ROUTE_SELECTION, review needed, human/Jarvis needed, or HOLD.
17. Open OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE only when the intake decision is READY_FOR_ROUTE_SELECTION.
```

## 5. Output Contract

Every triggered run must output:

```text
PRD_INTAKE_TRIGGER_OUTPUT
Trigger state:
Source id:
Source timestamp:
Baseline snapshot:
Baseline commit:
Safety screen:
Metrics record status:
Claude Web state:
Claude Code state:
SWE state:
Ticket readiness precheck:
HOLDs:
Decision:
Next governed artifact:
```

No triggered run may output:

- implementation started
- SWE started
- code changed
- launch ready
- external pilot ready
- Claude Web PASS without an actual verdict
- product route selected from missing PRD

## 6. Claude Web Queue Rule

If Claude Web review is required and unavailable:

```text
Decision: NEEDS_CLAUDE_WEB_REVIEW
Claude Web state: REVIEW_QUEUED or BLOCKED_BY_USAGE_LIMIT
Next governed artifact: Claude Web route/governance review prompt
```

Do not substitute Claude Code, SWE, VS Code, or Codex as a Claude Web architecture/governance reviewer.

## 7. SWE Rule

During PRD intake, SWE state is:

```text
SWE agent use: not authorized for this item
```

SWE may change only after:

- route selection exists
- ticket readiness passes
- exact Yellow item exists
- exact Yellow item explicitly names SWE as `bounded implementation accelerator`

## 8. Inbox Report Template

When the autonomous ops loop runs this trigger, open an inbox item using:

```text
PRD_INTAKE_TRIGGER_INBOX_REPORT
Snapshot:
Branch:
Trigger checked:
Positive trigger:
Source id:
Source timestamp:
Decision:
Metrics record:
Claude Web state:
SWE state:
HOLDs:
Files touched:
Gate status:
Next step:
```

If no positive trigger exists, `Files touched` should be:

```text
none
```

## 9. Non-Authorization

This run trigger does not authorize:

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

## 10. Next Use

Use this run trigger only after `docs\PRD_INTAKE_AUTOMATION_TRIGGER_RULES.md` returns a positive trigger.

If no trigger exists, keep waiting without editing the metrics record.
