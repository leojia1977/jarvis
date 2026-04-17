# Delegated Approver Charter

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Delegated Approver Charter |
| Status | Docs-only activation-prep draft; authority conditional pending required review |
| Snapshot | S5-AUTONOMOUS-POLICY-ACTIVATION-PREP-2026-04-17-001 |
| Stage | s5-autonomous-policy-activation-prep |
| Baseline commit | `d3f2945870e2e2cb8d0d7e313b67d396c8bf94c5` |
| Delegated approver | jarvis, technical lead |
| Authorization window | 2026-04-18 00:00 Asia/Shanghai to 2026-05-06 23:59 Asia/Shanghai |

This charter defines the purpose and limits of delegated approver authority during human absence. It is activation-prep only until required review is complete and approver accountability is confirmed.

If `jarvis` is an accountable human technical lead, `jarvis` may serve as delegated approver during the authorization window. If `jarvis` is an AI/system alias rather than an accountable human approver, Red-lane approval authority remains `NOT_ACTIVE` / `HOLD`. AI may not approve its own Red-lane authority.

## 2. Purpose

The delegated approver exists to unblock safe autonomous progress while preserving human-governed product authority. The delegated approver may approve bounded Red-lane actions only where this charter and `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md` allow it.

Delegated approver authority applies only during the authorization window and only for actions with complete approval records.

## 3. May Approve

The delegated approver may approve:

- Red-1 items listed in `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
- selected Red-2 execution only if explicitly allowed by policy and exact per-action `DELEGATED_APPROVER_GO`
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
- external pilot execution without exact launch/execution GO
- production deployment execution without explicit human GO

## 5. Approval SLA

Approval targets:

- Green: no delegated approval required if the current stage prompt or activated policy explicitly authorizes the action, gate/review rules pass, and no HOLD remains.
- Yellow: 4-hour review/approval target; if no response and the task is already scoped with no Red trigger, AI may continue only if activated policy explicitly allows it; otherwise HOLD.
- Red-1: 4-hour response target; timeout means HOLD.
- Red-2: 24-hour response target; timeout means HOLD.
- Approval expiration: default 72 hours unless `DELEGATED_APPROVER_GO` specifies a shorter expiration.

Timeout never permits bypassing required review, full gate, release verification, external review, or HOLD conditions.

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

Absent or ambiguous delegated approval means HOLD. Missing `DELEGATED_APPROVER_GO` fields mean HOLD.

Approvals expire after 72 hours by default unless a shorter expiration is specified.

## 8. Escalation

Escalate to the human or designated external reviewer if:

- the requested action touches Red-3
- real customer readiness or sign-off is implied
- legal/commercial commitment is possible
- raw secrets or unredacted customer data are involved
- the approval request is ambiguous
- rollback/HOLD authority is unclear
- approver accountability is unclear

## 9. Expiration And Revocation

- Every approval must include an expiration.
- Expired approval cannot be reused.
- Revocation immediately returns the action to HOLD.
- Approval for one action does not authorize adjacent actions.
- Authority ends at 2026-05-06 23:59 Asia/Shanghai unless separately governed.
