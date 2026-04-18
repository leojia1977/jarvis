# Autonomous Policy Final Activation

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Policy Final Activation |
| Status | Docs-only final activation draft |
| Snapshot | S5-AUTONOMOUS-POLICY-FINAL-ACTIVATION-2026-04-18-001 |
| Stage | s5-autonomous-policy-final-activation |
| Route | OPEN_AUTONOMOUS_POLICY_FINAL_ACTIVATION_DOCS_ONLY_STAGE |
| Baseline commit | `5981e478f0d47b4d2476556689d31c0429b7b88e` |
| Baseline snapshot | S5-AUTONOMOUS-POLICY-EXTERNAL-REVIEW-APPROVER-CONFIRMATION-2026-04-17-001 |
| Baseline stage | s5-autonomous-policy-external-review-approver-confirmation |

This document records the docs-only final activation of the autonomous authorization policy. It does not authorize launch execution, production deployment, external pilot execution, credential handling, real-data handling, public endpoint activation, S5-B/S5-D reopen, ORDIV reopen, or any Red-3 action.

## 2. Activation Input

| Field | Value |
| --- | --- |
| Activation input source | Human product/governance `FINAL_HUMAN_GO` |
| Activation date/time | 2026-04-18 08:21 Asia/Shanghai |
| Charter reread check | `docs\DELEGATED_APPROVER_CHARTER.md` was readable before this draft edit |
| delegation_expires check | 2026-05-06 23:59 Asia/Shanghai; not passed at activation draft time |
| Policy status after this stage | ACTIVE |

Human activation input includes the required MEDIUM-1 guardrail:

```text
At the start of every autonomous session, Codex must re-read docs/DELEGATED_APPROVER_CHARTER.md and verify that delegation_expires has not passed. If the charter cannot be read or the timestamp has passed, all Red authority reverts to HOLD and the AI must not proceed with any Red-lane action.
```

## 3. Core Governance Docs Loaded

Before activation drafting, Codex loaded the required core governance docs:

- `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
- `docs\DELEGATED_APPROVER_CHARTER.md`
- `docs\AUTONOMOUS_DELIVERY_PIPELINE.md`
- `docs\AUTONOMOUS_HOLD_QUEUE.md`
- `docs\L3_CUSTOMER_TRIAL_LAUNCH_CRITICAL_PATH.md`
- `docs\PRODUCT_STATE.md`
- `docs\ROADMAP_AND_PARKED_ITEMS.md`
- `docs\GOVERNANCE_DECISION_LOG.md`

Future autonomous sessions must load these core governance docs before autonomous action.

## 4. Authorization Window

| Field | Value |
| --- | --- |
| Authorization window start | 2026-04-18 00:00 Asia/Shanghai |
| Authorization window end | 2026-05-06 23:59 Asia/Shanghai |
| delegation_expires | 2026-05-06 23:59 Asia/Shanghai |
| Delegated approver | jarvis, technical lead |

`ACTIVE` applies only during this authorization window. If `delegation_expires` has passed, the charter cannot be read, or the timestamp is missing, all Red authority is HOLD.

Jarvis is delegated approver only within the limits of `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md` and `docs\DELEGATED_APPROVER_CHARTER.md`.

## 5. AHQ Status Effects

| Hold ID | Status after this stage | Rationale |
| --- | --- | --- |
| AHQ-015 | CLOSED_BY_EXTERNAL_REVIEW_CONDITIONALLY | Previously closed by external review `PASS_WITH_CONDITIONS` and incorporated MEDIUM-1 guardrail. |
| AHQ-016 | CLOSED_BY_HUMAN_CONFIRMATION | Previously closed by human confirmation that jarvis is an accountable human technical lead. |
| AHQ-018 | CLOSED_BY_FINAL_HUMAN_GO | Human supplied `FINAL_HUMAN_GO` and required session-start/core-governance guardrails. |

Closing AHQ-018 activates the policy only within the authorization window and only under the policy limits. It does not close launch, deployment, external access, credential, real-data, evidence, public endpoint, S5-B/S5-D, ORDIV, network ambiguity, or Red-3 blockers.

## 6. Remaining HOLDs

The following remain HOLD unless later governed otherwise:

- AHQ-003 external pilot seven input categories
- AHQ-004 environment/access boundary
- AHQ-005 evidence retention policy
- AHQ-006 real-record redaction approval
- AHQ-007 go/no-go authority
- AHQ-008 rollback/HOLD authority
- AHQ-009 deployment target
- AHQ-010 credential handling path
- AHQ-011 L3 launch decision package
- AHQ-012 S5-B/S5-D parked streams
- AHQ-013 public close-case endpoint
- AHQ-014 ORDIV report/CSV/L1B
- AHQ-017 network retry ambiguity / non-idempotent remote request uncertainty when ambiguity exists

## 7. Red-3 Never-Authorized List

Red-3 remains never AI-self-authorized and is not delegable by normal Red-1/Red-2 approval. Jarvis may not approve Red-3.

Red-3 includes:

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

Any Red-3 action requires separate explicit human-level governed approval, and some Red-3 actions may remain never authorized by this policy.

## 8. Per-Action Red Rules

- ACTIVE policy does not create blanket Red execution.
- Red-1/Red-2 still require exact per-action `DELEGATED_APPROVER_GO` where policy requires it.
- Any missing `DELEGATED_APPROVER_GO` field means HOLD.
- Any expired approval means HOLD.
- Any lane ambiguity defaults to the higher-restriction lane; if still unclear, HOLD.
- Any unresolved HOLD blocks the action.

## 9. L3 And Launch Boundary

- L3 deadline remains a planning target only.
- L3 launch execution remains HOLD until a separate governed launch decision package exists, required reviews pass, all required approvals are recorded, full gate/release baseline is current, and exact human/delegated GO authorizes the launch action.
- External pilot inputs remain `NOT_READY` / `UNKNOWN` unless separately governed.
- External pilot execution remains unauthorized.

## 10. Non-Authorization

This activation does not authorize:

- launch execution
- production deployment
- external pilot execution
- credential handling by AI
- real-data handling
- public endpoint activation
- S5-B reopen
- S5-D reopen
- ORDIV reopen/report/CSV/L1B work
- Red-3 actions
- legal/commercial commitments
- public GA
- customer/operator sign-off
- evidence deletion
- schema/API breaking changes without separate human-level governed approval
- S4-A resolver order changes
- AI_COLLAB changes

## 11. Future Autonomous Session Operating Rules

Every future autonomous session must:

- load the core governance docs before autonomous action
- re-read `docs\DELEGATED_APPROVER_CHARTER.md`
- verify `delegation_expires` has not passed
- treat unreadable charter, missing timestamp, or expired window as Red authority HOLD
- preserve all Red-3 prohibitions
- apply lane ambiguity to the higher-restriction lane; if still unclear, HOLD
- honor all remaining HOLD queue entries
- record required governed decisions and review/gate status before any closeout

## 12. Expiration And Deactivation

The active authorization window ends at 2026-05-06 23:59 Asia/Shanghai.

At expiration, Red authority reverts to HOLD unless a later governed stage explicitly extends or replaces the policy.

Future deactivation or expiration closeout must add an `AUTONOMOUS_PERIOD_END` marker to `docs\GOVERNANCE_DECISION_LOG.md`.
