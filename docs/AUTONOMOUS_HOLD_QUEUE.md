# Autonomous HOLD Queue

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous HOLD Queue |
| Status | Live governed HOLD queue activation-prep draft |
| Snapshot | S5-AUTONOMOUS-POLICY-ACTIVATION-PREP-2026-04-17-001 |
| Stage | s5-autonomous-policy-activation-prep |
| Baseline commit | `d3f2945870e2e2cb8d0d7e313b67d396c8bf94c5` |

This HOLD queue tracks blockers for autonomous vacation mode and L3 customer-trial launch acceleration. It does not authorize implementation or launch execution.

## 2. HOLD Queue

| Hold ID | Area | Blocked item | Why blocked | Required input | Who can unblock | AI can prepare while waiting | Required review | Lane | Status | Last update |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AHQ-001 | Authorization | Named delegated approver | `jarvis, technical lead` is supplied for activation prep, but accountable-human identity must remain explicit. | Confirm `jarvis` is an accountable human technical lead, not an AI/system alias. | Human/product governance. | Draft approval templates. | Human or external review. | Conditional Red | PREPARED_CONDITIONAL | 2026-04-17 |
| AHQ-002 | Authorization | Authorization window | Window is supplied for activation prep. | Confirm scope applies only from 2026-04-18 00:00 Asia/Shanghai to 2026-05-06 23:59 Asia/Shanghai. | Human/product governance. | Draft schedule checklist. | Human or external review. | Conditional Red | PREPARED_CONDITIONAL | 2026-04-17 |
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
| AHQ-015 | Review | External review before policy activation | Activation-prep policy introduces delegated Red-lane authority and L3 acceleration rules. | Claude Web or designated external reviewer PASS before marking policy ACTIVE. | Human/product governance or external reviewer. | Prepare review packet. | Claude Web/external review. | Conditional Red | HOLD | 2026-04-17 |
| AHQ-016 | Authorization | Jarvis approver identity/accountability | `jarvis` must be an accountable human technical lead for Red authority. | Confirmation that `jarvis` is human/accountable and authorized for this window. | Human/product governance. | Keep Red authority conditional. | Human or external review. | Conditional Red | HOLD | 2026-04-17 |
| AHQ-017 | Network | Retry ambiguity / non-idempotent remote request uncertainty | Slow or ambiguous remote/network status can duplicate approval, push, deploy, launch, upload, or access actions. | Confirm previous request failed, expired, or is void before retrying non-idempotent work. | Human/delegated approver for Red actions; operator for remote status. | Retry idempotent/read-only once; document ambiguity. | Review by lane. | Green/Yellow/Conditional Red | HOLD_IF_AMBIGUOUS | 2026-04-17 |

## 3. Queue Rules

- HOLD entries remain blocked until the named unblocking input is governed.
- AI may prepare only the listed safe drafting work.
- Any ambiguity keeps the item in HOLD.
- No HOLD queue item authorizes real access, credentials, launch execution, public endpoint work, or parked-stream reopen.
