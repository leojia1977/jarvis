# Autonomous Authorization Policy

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Authorization Policy |
| Status | Docs-only draft for autonomous authorization policy review |
| Snapshot | S5-AUTONOMOUS-VACATION-OPERATING-MODEL-2026-04-17-001 |
| Stage | s5-autonomous-vacation-operating-model |
| Baseline commit | `da15c383e14bc4cae6c97017f91549194c37487d` |

This policy defines standing authorization lanes for safe autonomous work while the human is unavailable. The policy is not active until the human names an approver/window or explicitly confirms activation.

## 2. Activation State

| Field | Value |
| --- | --- |
| Authorization status | NOT_ACTIVE |
| Delegated approver | TBD_DELEGATED_APPROVER |
| Authorization window | TBD_AUTHORIZATION_WINDOW |

Absent or ambiguous activation means HOLD.

## 3. Green Lane

Green lane work may proceed when the stage or standing policy explicitly allows it:

- docs-only governance artifacts
- route decisions
- rolling maps
- review packs
- manifest updates
- full gates
- release packaging
- commit/push after PASS only when the current stage prompt, activated standing policy, or explicit human/delegated instruction assigns Green lane authority and explicitly allows commit/push, and no HOLD remains

Green lane work does not authorize implementation or launch execution by itself.

## 4. Yellow Lane

Yellow lane work is scoped implementation or test work. It requires:

- exact files
- exact behavior
- exact tests
- review path
- rollback/HOLD conditions
- explicit confirmation that no Red trigger is present

If any item is missing, Yellow lane work is HOLD.

## 5. Conditional Red Lane

Conditional Red work may be drafted or prepared, but execution requires delegated or human GO.

Conditional Red includes:

- external pilot decision package
- customer-trial deployment prep
- read-only external access prep
- evidence/redaction policy drafting
- L3 launch package drafting

## 6. Red Items Not Allowed Without Separate GO

The following require separate delegated or human GO and cannot be inferred from this policy:

- external pilot execution
- real customer launch execution
- production deployment
- real credentials
- raw customer data
- evidence retention activation
- public endpoint activation
- schema/API contract freeze or change
- legal/commercial commitments

## 7. Red-3 Never AI-Self-Authorized

The following are never AI-self-authorized:

- legal/commercial commitments
- real customer sign-off
- raw secret handling
- deletion of real evidence
- incident responsibility judgments

## 8. Required Approval Format

Any delegated approval must use this format:

```text
DELEGATED_APPROVER_GO
Approver:
Date:
Stage/ticket:
Lane:
Approved action:
Allowed files/systems:
External access: yes/no
Real data: yes/no
Evidence retention: yes/no
Redaction reference:
Rollback/HOLD criteria:
Expiration:
Required review:
```

Any missing field means the approval is incomplete and the action is HOLD.

## 9. Commit And Push Rules

AI may stage, commit, and push only when:

- the current stage prompt, activated standing policy, or recorded human/delegated approval explicitly assigns lane authority
- the same authority explicitly allows staging, commit, and push
- review conditions are satisfied
- full gate passes where required
- release/package rules are satisfied
- no HOLD remains
- allowed files are exact and clean
- pre-existing unrelated files are not included

AI cannot self-assign lane authority or infer commit/push authority from Green lane status alone.

## 10. Standing Prohibitions

This policy does not authorize raw secret handling, external pilot execution, real customer launch execution, production deployment, public endpoint activation, evidence retention activation, S5-B/S5-D reopen, ORDIV report/CSV/L1B work, S4-A resolver change, or AI_COLLAB change.
