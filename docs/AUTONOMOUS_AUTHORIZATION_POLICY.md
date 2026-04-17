# Autonomous Authorization Policy

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Authorization Policy |
| Status | Docs-only activation-prep draft; activation conditional pending required review |
| Snapshot | S5-AUTONOMOUS-POLICY-ACTIVATION-PREP-2026-04-17-001 |
| Stage | s5-autonomous-policy-activation-prep |
| Baseline commit | `d3f2945870e2e2cb8d0d7e313b67d396c8bf94c5` |

This policy defines standing authorization lanes for safe autonomous work while the human is unavailable. This stage prepares activation details and safety rules only. It does not execute Red work, launch, deploy, access external systems, handle credentials, or process real data.

## 2. Activation State

| Field | Value |
| --- | --- |
| Authorization status | ACTIVATION_PENDING_EXTERNAL_REVIEW_AND_APPROVER_IDENTITY_CONFIRMATION |
| Delegated approver | jarvis, technical lead |
| Authorization window | 2026-04-18 00:00 Asia/Shanghai to 2026-05-06 23:59 Asia/Shanghai |
| Target L3 customer trial launch deadline | No later than 2026-05-06 23:59 Asia/Shanghai |
| Maximum autonomous lane | Green + Yellow + Red-1 with delegated approver GO + selected Red-2 preparation |
| Approval expiration | Default 72 hours unless `DELEGATED_APPROVER_GO` specifies a shorter expiration |

Activation remains conditional until required review is complete. Because this policy defines Red-lane authority and customer-trial acceleration rules, activation status remains `ACTIVATION_PENDING_EXTERNAL_REVIEW_AND_APPROVER_IDENTITY_CONFIRMATION` until the required external review path records PASS and approver accountability is confirmed.

If `jarvis` is an accountable human technical lead, `jarvis` may be recorded as delegated approver for the authorization window. If `jarvis` is an AI/system alias rather than an accountable human approver, Red-lane approval authority remains `NOT_ACTIVE` / `HOLD`. AI may not approve its own Red-lane authority.

If the team chooses not to activate after review, this policy should be marked `PREPARED_NOT_ACTIVE`.

## 3. Green Lane

Green lane work may proceed when the current stage prompt or activated policy explicitly authorizes the action, gate/review rules pass, and no HOLD remains. No delegated approval is required for Green work under those conditions.

Green lane examples:

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

Yellow lane approval target is 4 hours. If there is no response and the task is already scoped with no Red trigger, AI may continue only if activated policy explicitly allows it; otherwise the task is HOLD.

If any scoping item is missing, Yellow lane work is HOLD.

## 5. Conditional Red Lane

Conditional Red work may be drafted or prepared, but execution requires delegated or human GO.

Red-1 response target is 4 hours; timeout means HOLD. Red-2 response target is 24 hours; timeout means HOLD.

Red-2 execution requires exact per-action `DELEGATED_APPROVER_GO`. Red-3 is never AI-self-authorized.

## 6. Allowed Red-1 Approvals

Delegated approver may approve these Red-1 items during the authorization window, if no raw customer data, credentials, launch execution, production deployment, or unresolved HOLD is introduced:

- external pilot/customer-trial input acceptance if no raw customer data or credentials are introduced; input acceptance under this item does not constitute a readiness claim and does not remove the Claude Web gate required by AHQ-003 when readiness is claimed
- L3 launch decision package drafting and review preparation
- customer trial scope / role matrix / support matrix approval
- environment/access boundary decision if it does not start real access
- read-only external access preparation with credentials handled outside repo/chat
- evidence retention policy drafting
- redaction policy drafting
- monitoring/logging plan drafting
- backup/restore plan drafting
- support/escalation plan drafting
- customer success metrics drafting if no raw customer evidence is retained
- Claude Web / external reviewer prompt approval for high-risk packages

## 7. Allowed Red-2 Approvals

Delegated approver may approve these Red-2 preparation or decision-package actions only where policy and required review allow them:

- finalizing an L3 launch decision package for review, but not executing launch
- approving controlled customer-trial deployment preparation, but not production deployment execution
- approving read-only external validation plan, but actual access requires separate exact GO and operator-managed credentials
- approving evidence retention policy candidate, but not activating retention against real customer data
- approving redaction policy candidate, but not storing unredacted records
- approving public endpoint decision package drafting, but not public endpoint activation
- approving S5-B/S5-D reopen decision package drafting only; S5-B/S5-D implementation requires a separate explicit governed reopen decision, separate scoped ticket, separate review, and explicit GO that goes beyond the scope of this policy

Red-2 execution requires exact per-action `DELEGATED_APPROVER_GO`. Preparation does not imply execution authority.

## 8. Red-3 Never AI-Self-Authorized

The following are never AI-self-authorized:

- legal/commercial commitments
- public GA announcement or public GA launch
- real customer sign-off
- production deployment execution without explicit human GO
- raw credential handling by AI
- credentials, tokens, API keys, auth headers, cookies, or secrets entering repo/chat
- unredacted customer data retention
- deletion of real evidence
- destructive response or remediation
- incident responsibility judgments
- public endpoint activation
- schema/API breaking change without separate human-level governed approval
- evidence retention activation for real customer data without human/security/privacy approval
- external pilot execution without exact launch/execution GO

## 9. Required Approval Format

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

Approvals expire after 72 hours by default unless `DELEGATED_APPROVER_GO` specifies a shorter expiration.

## 10. Commit And Push Rules

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

## 11. Standing Prohibitions

This policy does not authorize raw secret handling, external pilot execution, real customer launch execution, production deployment, public endpoint activation, evidence retention activation, S5-B/S5-D reopen, ORDIV report/CSV/L1B work, S4-A resolver change, or AI_COLLAB change.
