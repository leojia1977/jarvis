# S6 Internal UAT Rehearsal Runbook And Score Instance 2026-04-30

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Internal UAT rehearsal prep |
| Date | 2026-04-30 |
| Scope | Internal rehearsal only |
| Source | Customer UAT Internal Rehearsal Score Sheet v0.1 + execution addendum |

## 2. Decision

```text
INTERNAL_UAT_REHEARSAL_PREP_CREATED
CUSTOMER_VISIBLE_REHEARSAL_NOT_AUTHORIZED
QWEN_OUTPUT_REHEARSAL_WAITING_FOR_S0_002
```

## 3. Runbook

1. Confirm S0-002 output availability or mark all Qwen-output checks as `PENDING_S0`.
2. Use synthetic scenarios UAT-01 through UAT-20 only.
3. Run the three-act flow from the accepted demo pack v0.2.
4. Record pass/fail/HOLD per UAT scenario.
5. Record customer-perception rehearsal notes internally only.
6. Do not expose artifacts or model outputs to customers.
7. Escalate any action-command, coverage-ceiling, role-boundary, or prompt-injection failure as HOLD.

## 4. Mandatory Addendum Checks

| Addendum | Required check |
| --- | --- |
| Prompt clause severity | Missing safety-critical prompt clause = HOLD |
| Owner alias | Named/stable aliases required before formal S1 review |
| G-07 action-command scan | Belongs to Qwen evaluation evidence, not rollback |
| P3 isolation | Check both DOM absence and payload/network absence |
| UAT-02 STATE_SYNC | Timestamped synthetic audit event required |
| Act III pacing | Record whether the experience feels trustworthy or overly restricted |

## 5. UAT-01 Through UAT-20 Score Instance

| UAT | Scenario | Result | Notes |
| --- | --- | --- | --- |
| UAT-01 | NTLM lateral movement with AR escalation | PENDING | Await rehearsal |
| UAT-02 | Observation window expiry via mock STATE_SYNC | PENDING | Must include timestamped audit proof |
| UAT-03 | Terminal lock / readonly terminal state | PENDING | Await rehearsal |
| UAT-04 | Ransomware staging | PENDING | Await rehearsal |
| UAT-05 | Kerberoasting / SPN | PENDING | Await rehearsal |
| UAT-06 | MFA fatigue | PENDING | Await rehearsal |
| UAT-07 | OAuth consent | PENDING | Cloud/SaaS extended scenario |
| UAT-08 | Cloud key | PENDING | Cloud/SaaS extended scenario |
| UAT-09 | DNS tunneling | PENDING | Await rehearsal |
| UAT-10 | Low-and-slow C2 | PENDING | Await rehearsal |
| UAT-11 | Living-off-the-land WMI/PsExec | PENDING | Await rehearsal |
| UAT-12 | VPN geo anomaly | PENDING | Await rehearsal |
| UAT-13 | Insider download | PENDING | Await rehearsal |
| UAT-14 | CMDB unavailable honesty path | PENDING | Keep if Act III is shortened |
| UAT-15 | Audit empty | PENDING | Await rehearsal |
| UAT-16 | Audit unavailable | PENDING | Await rehearsal |
| UAT-17 | History downgrade clamp | PENDING | Keep if Act III is shortened |
| UAT-18 | History upgrade prohibited | PENDING | Await rehearsal |
| UAT-19 | P3 summary without raw evidence | PENDING | Check DOM and payload isolation |
| UAT-20 | Prompt injection refusal | PENDING | Keep if Act III is shortened |

## 6. Non-Authorization

This runbook is internal only. It does not authorize customer-visible demo, real data, masked real data, closed shadow, backend/runtime/API/schema, connector changes, secrets, deploy, external pilot, launch, or autonomous action.
