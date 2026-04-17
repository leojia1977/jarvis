# L3 Customer Trial Launch Critical Path

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | L3 Customer Trial Launch Critical Path |
| Status | Docs-only draft for L3 customer trial launch critical path review |
| Snapshot | S5-AUTONOMOUS-VACATION-OPERATING-MODEL-2026-04-17-001 |
| Stage | s5-autonomous-vacation-operating-model |
| Baseline commit | `da15c383e14bc4cae6c97017f91549194c37487d` |

`L3 Customer Trial Launch` means a controlled customer-trial launch or private launch candidate. It is not unrestricted public GA and not multi-customer commercial GA unless separately governed.

This document defines what must become true before launch. It does not authorize external pilot execution, L3 launch execution, production deployment, credential handling, real-data handling, or customer sign-off.

## 2. Current Expected Posture

- External pilot/customer-trial inputs remain `NOT_READY` / `UNKNOWN` unless explicitly provided later.
- External pilot execution remains unauthorized by this stage.
- L3 launch execution remains unauthorized by this stage.

## 3. Status Vocabulary

Allowed status values:

- `PROVIDED`
- `ACCEPTED_BY_DELEGATED_APPROVER`
- `UNKNOWN`
- `MISSING`
- `NEEDS_DECISION`
- `HOLD`

## 4. Critical Path Table

| Area | Current status | Required input | Owner / approver | AI can do now | HOLD trigger | Evidence artifact | Target lane |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Customer trial scope | `UNKNOWN` | Named scope, customer/trial class, boundaries, exclusions. | Human or delegated approver. | Draft scope template. | Scope implies public GA or commercial commitment. | L3 launch decision package. | Conditional Red |
| Participating roles | `UNKNOWN` | Customer, operator, support, reviewer, approver roles. | Human or delegated approver. | Draft role matrix. | Real sign-off implied. | Role matrix. | Conditional Red |
| Environment/access boundary | `MISSING` | Environment type, access path, allowed systems, network boundary. | Human or delegated approver. | Draft access-boundary checklist. | Real access begins. | Environment/access decision. | Conditional Red |
| SIEM/EDR/source access plan | `UNKNOWN` | Read-only/read-write status, systems, data scope. | Human, delegated approver, external reviewer if required. | Draft access plan. | Real SIEM/EDR/source access starts. | Access plan. | Conditional Red |
| Credential handling path | `MISSING` | Vault/path, who handles credentials, no repo/chat disclosure. | Human/security owner. | Draft credential-handling checklist. | Credentials enter repo/chat. | Credential handling decision. | Red-3 |
| Evidence retention policy | `MISSING` | What may be retained, where, duration, deletion/expiry rules. | Human/legal/security or delegated if authorized. | Draft policy questions. | Retention activated without approval. | Evidence retention decision. | Conditional Red |
| Redaction policy for records | `MISSING` | Redaction rules for pilot/customer records. | Human/security/privacy or external reviewer. | Draft redaction policy candidate. | Raw customer records enter repo/chat. | Redaction policy decision. | Conditional Red |
| Go/no-go authority | `MISSING` | Named authority for launch and stop decisions. | Human or delegated approver. | Draft authority matrix. | AI claims readiness or signs off. | Go/no-go charter. | Red-2 |
| Rollback/HOLD authority | `MISSING` | Named stop authority and rollback criteria. | Human or delegated approver. | Draft rollback checklist. | Launch lacks stop authority. | Rollback/HOLD plan. | Red-2 |
| Deployment target | `UNKNOWN` | Target environment and deployment mechanism. | Human/delegated approver plus technical owner. | Draft target options. | Production deploy begins. | Deployment decision. | Conditional Red |
| Monitoring/logging | `NEEDS_DECISION` | What is monitored, logged, redacted, retained. | Human/security/support. | Draft monitoring checklist. | Raw logs retained without policy. | Monitoring/logging plan. | Conditional Red |
| Backup/restore | `NEEDS_DECISION` | Backup scope, restore test, rollback owner. | Technical owner/delegated approver. | Draft backup questions. | Irreversible action risk. | Backup/restore plan. | Yellow/Conditional Red |
| Support/escalation | `UNKNOWN` | Support owner, escalation path, response windows. | Human/delegated approver. | Draft support matrix. | Incident responsibility judgment required. | Support/escalation plan. | Conditional Red |
| Customer success metrics | `NEEDS_DECISION` | Metrics, allowed aggregation, no raw evidence leakage. | Product/governance. | Draft metric candidates. | Real customer metrics retained without approval. | Metrics decision. | Conditional Red |
| Public endpoint decision | `HOLD` | Separate public close-case endpoint route. | Human/governance/external reviewer if selected. | Document deferred state. | `KEEP_DEFERRED` weakened. | Endpoint route decision. | Red-2 |
| S5-B source/input reopen trigger | `HOLD` | Explicit source/input gap and reopen decision. | Human/governance. | Document trigger checklist. | S5-B reopens silently. | S5-B reopen decision. | Conditional Red |
| S5-D telemetry reopen trigger | `HOLD` | Explicit telemetry gap and reopen decision. | Human/governance. | Document trigger checklist. | S5-D reopens silently. | S5-D reopen decision. | Conditional Red |
| ORDIV report/CSV/L1B trigger | `HOLD` | Separate governed route and required review. | Human/governance/external reviewer. | Document parked state. | Report, CSV, or L1B work begins. | ORDIV route decision. | Red-2 |
| Security/privacy review | `MISSING` | Reviewer, scope, evidence handling, sign-off rules. | Security/privacy owner or delegated approver. | Draft review checklist. | Review bypassed. | Security/privacy review. | Conditional Red |
| Release artifact / verification baseline | `PROVIDED` | Current governed release artifact and manifest PASS. | Repo release process. | Cite current baseline. | Claim refreshed baseline without full gate. | Manifest/release verification. | Green |
| L3 launch decision package | `MISSING` | All above inputs resolved or explicitly accepted. | Human or delegated approver if policy permits. | Draft package skeleton. | Package claims readiness with missing inputs. | L3 launch package. | Red-2 |

## 5. Launch Rule

L3 launch execution remains HOLD until the launch decision package is governed, required reviews pass, all required approvals are recorded, full gate/release baseline is current, and human or delegated GO explicitly authorizes the exact launch action.

