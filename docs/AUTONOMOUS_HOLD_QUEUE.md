# Autonomous HOLD Queue

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous HOLD Queue |
| Status | Live governed HOLD queue draft |
| Snapshot | S5-AUTONOMOUS-VACATION-OPERATING-MODEL-2026-04-17-001 |
| Stage | s5-autonomous-vacation-operating-model |
| Baseline commit | `da15c383e14bc4cae6c97017f91549194c37487d` |

This HOLD queue tracks blockers for autonomous vacation mode and L3 customer-trial launch acceleration. It does not authorize implementation or launch execution.

## 2. HOLD Queue

| Hold ID | Area | Blocked item | Why blocked | Required input | Who can unblock | AI can prepare while waiting | Required review | Lane | Status | Last update |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AHQ-001 | Authorization | Named delegated approver | Approver is `TBD_DELEGATED_APPROVER`. | Named approver and authority scope. | Human. | Draft approval templates. | Human review. | Conditional Red | HOLD | 2026-04-17 |
| AHQ-002 | Authorization | Authorization window | Window is `TBD_AUTHORIZATION_WINDOW`. | Start/end window and allowed lanes. | Human. | Draft schedule checklist. | Human review. | Conditional Red | HOLD | 2026-04-17 |
| AHQ-003 | External pilot | Seven input categories | Inputs remain `NOT_READY` / `UNKNOWN`. | Governed input package or explicit acceptance. | Human/product governance. | Maintain checklist. | Claude Web if readiness claimed. | Red-2 | HOLD | 2026-04-17 |
| AHQ-004 | Access | Environment/access boundary | Boundary is missing. | Environment/access decision. | Human/delegated approver. | Draft boundary template. | External review if real access. | Conditional Red | HOLD | 2026-04-17 |
| AHQ-005 | Evidence | Evidence retention policy | Policy is missing. | Retention decision. | Human/security/privacy. | Draft questions. | Claude Web/external review. | Red-2 | HOLD | 2026-04-17 |
| AHQ-006 | Redaction | Real-record redaction approval | Approval is missing. | Redaction policy reference. | Human/security/privacy. | Draft redaction candidate. | Claude Web/external review. | Conditional Red | HOLD | 2026-04-17 |
| AHQ-007 | Authority | Go/no-go authority | Named authority is missing. | Named launch authority. | Human/delegated approver. | Draft authority matrix. | Human/delegated review. | Red-2 | HOLD | 2026-04-17 |
| AHQ-008 | Authority | Rollback/HOLD authority | Stop authority is missing. | Named stop owner and criteria. | Human/delegated approver. | Draft rollback checklist. | Human/delegated review. | Red-2 | HOLD | 2026-04-17 |
| AHQ-009 | Deployment | Deployment target | Target is missing. | Target environment and deployment path. | Human/delegated approver. | Draft options. | External review if production. | Conditional Red | HOLD | 2026-04-17 |
| AHQ-010 | Secrets | Credential handling path | Path is missing. | Vault/credential handling decision. | Human/security owner. | Draft checklist only. | Security review. | Red-3 | HOLD | 2026-04-17 |
| AHQ-011 | L3 launch | Launch decision package | Package is not opened. | Governed L3 package route. | Human/delegated approver. | Draft skeleton only. | Claude Web/external review. | Red-2 | HOLD | 2026-04-17 |
| AHQ-012 | S5-B/S5-D | Parked streams | S5-B and S5-D remain parked. | Explicit reopen decision. | Human/governance. | Draft trigger checklist. | Review per route. | Conditional Red | HOLD | 2026-04-17 |
| AHQ-013 | Public endpoint | Close-case endpoint | Endpoint remains `KEEP_DEFERRED`. | Separate endpoint route. | Human/governance. | Document deferred state. | Claude Web required if selected. | Red-2 | HOLD | 2026-04-17 |
| AHQ-014 | ORDIV | Report/CSV/L1B | ORDIV-L1A remains parked. | Separate ORDIV route. | Human/governance. | Document parked state. | Claude Web required. | Red-2 | HOLD | 2026-04-17 |

## 3. Queue Rules

- HOLD entries remain blocked until the named unblocking input is governed.
- AI may prepare only the listed safe drafting work.
- Any ambiguity keeps the item in HOLD.
- No HOLD queue item authorizes real access, credentials, launch execution, public endpoint work, or parked-stream reopen.

