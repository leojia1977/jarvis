# Delegated Approver Charter

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Delegated Approver Charter |
| Status | Docs-only draft for delegated approver charter review |
| Snapshot | S5-AUTONOMOUS-VACATION-OPERATING-MODEL-2026-04-17-001 |
| Stage | s5-autonomous-vacation-operating-model |
| Delegated approver | TBD_DELEGATED_APPROVER |

This charter defines the purpose and limits of delegated approver authority during human absence. It is inactive until the human names the delegated approver and authorization window.

## 2. Purpose

The delegated approver exists to unblock safe autonomous progress while preserving human-governed product authority. The delegated approver may approve bounded Red-lane actions only where this charter and `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md` allow it.

## 3. May Approve

The delegated approver may approve:

- Red-1 items
- selected Red-2 execution only if explicitly allowed by policy
- L3 launch readiness package review
- bounded customer-trial prep artifacts that do not execute launch
- review escalation paths when evidence is complete

## 4. May Not Approve Without Human Pre-Authorization

The delegated approver may not approve:

- legal/commercial commitments
- public GA
- unredacted customer data retention
- credential disclosure into repo/chat
- destructive response
- irreversible production/customer actions
- raw secret handling
- deletion of real evidence
- incident responsibility judgments

## 5. Approval SLA

Approval SLA: `TBD_APPROVAL_SLA`.

If no SLA is named, AI must assume no response deadline and hold blocked Red-lane execution.

## 6. Required Evidence Before Approval

Before approving, the delegated approver should receive:

- stage/ticket and lane
- exact action requested
- exact files/systems in scope
- external access yes/no
- real data yes/no
- evidence retention yes/no
- redaction reference
- rollback/HOLD criteria
- gate/review status
- expiration of approval

## 7. Approval Record

Approvals must use the `DELEGATED_APPROVER_GO` format in `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`.

Absent or ambiguous delegated approval means HOLD.

## 8. Escalation

Escalate to the human or designated external reviewer if:

- the requested action touches Red-3
- real customer readiness or sign-off is implied
- legal/commercial commitment is possible
- raw secrets or unredacted customer data are involved
- the approval request is ambiguous
- rollback/HOLD authority is unclear

## 9. Expiration And Revocation

- Every approval must include an expiration.
- Expired approval cannot be reused.
- Revocation immediately returns the action to HOLD.
- Approval for one action does not authorize adjacent actions.

