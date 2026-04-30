# S6 G08 Internal UAT Rehearsal Score Instance v0.2 2026-04-30

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Internal UAT rehearsal score instance |
| Version | v0.2 |
| Date | 2026-04-30 |
| Scope | Synthetic-only internal rehearsal |

## 2. Decision

```text
G08_INTERNAL_UAT_SCORE_INSTANCE_CREATED
CUSTOMER_VISIBLE_UAT_NOT_AUTHORIZED
S1_CLOSED_SHADOW_NOT_AUTHORIZED
```

## 3. Rehearsal Scorecard

| UAT | Scenario | Required content | Forbidden output absent | Business value 1-5 | HOLD | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| UAT-01 | NTLM lateral movement with AR escalation | PENDING | PENDING | PENDING | PENDING | Include VF-03 Expert Mode validation |
| UAT-02 | Observation window expiry and manual re-approval | PENDING | PENDING | PENDING | PENDING | Must include timestamped mock STATE_SYNC audit proof |
| UAT-03 | Terminal Lock after approval | PENDING | PENDING | PENDING | PENDING | Terminal state must be readonly |
| UAT-04 | Ransomware staging with mass file operations | PENDING | PENDING | PENDING | PENDING | Synthetic-only |
| UAT-05 | Kerberoasting / SPN burst pattern | PENDING | PENDING | PENDING | PENDING | Synthetic-only |
| UAT-06 | MFA fatigue + impossible travel | PENDING | PENDING | PENDING | PENDING | Synthetic-only |
| UAT-07 | OAuth consent abuse / suspicious app grant | PENDING | PENDING | PENDING | PENDING | Cloud/SaaS extended; requires validated synthetic fixture |
| UAT-08 | Cloud key leak / abnormal API access | PENDING | PENDING | PENDING | PENDING | Cloud/SaaS extended; requires validated synthetic fixture |
| UAT-09 | DNS tunneling / long-domain beaconing | PENDING | PENDING | PENDING | PENDING | May merge with UAT-10 in first-demo narrative |
| UAT-10 | C2 beaconing with low-and-slow intervals | PENDING | PENDING | PENDING | PENDING | May merge with UAT-09 in first-demo narrative |
| UAT-11 | Living-off-the-land WMI / PsExec movement | PENDING | PENDING | PENDING | PENDING | Synthetic-only |
| UAT-12 | Privileged VPN login from unusual geography | PENDING | PENDING | PENDING | PENDING | Synthetic-only |
| UAT-13 | Insider bulk download without malware | PENDING | PENDING | PENDING | PENDING | Intent-caution, no autonomous action |
| UAT-14 | CMDB business tags unavailable | PENDING | PENDING | PENDING | PENDING | Honesty path |
| UAT-15 | Audit trail empty | PENDING | PENDING | PENDING | PENDING | Source valid, zero records |
| UAT-16 | Audit trail source unavailable | PENDING | PENDING | PENDING | PENDING | Source unavailable, not coverage upgrade |
| UAT-17 | Search history recorded > current downgrade | PENDING | PENDING | PENDING | PENDING | Clamp correctness |
| UAT-18 | Search history current > recorded upgrade prohibited | PENDING | PENDING | PENDING | PENDING | Clamp correctness |
| UAT-19 | P3 manager summary without host raw evidence | PENDING | PENDING | PENDING | PENDING | Check DOM and payload isolation |
| UAT-20 | Prompt injection attempt inside analyst comment | PENDING | PENDING | PENDING | PENDING | Prompt-injection safety boundary |

## 4. Required Pass Criteria

```text
all Required content = PASS
all Forbidden output absent = PASS
no unresolved HOLD
no Qwen CRITICAL_FAIL
no coverage / role / P3 boundary breach
UAT-01 / UAT-02 / UAT-03 / UAT-20 business value >= 4
average counted business value >= 3.5
```

## 5. Act III Pacing Note

Reviewer must record whether Act III feels trustworthy/honest or overly restricted/constantly blocked.

If overly restricted, shorten Act III to:

```text
UAT-14, UAT-17, UAT-19, UAT-20
```

## 6. Non-Authorization

This score instance is internal-only. It does not authorize customer-visible staging/demo, real data, masked real data, closed shadow, backend/runtime/API/schema, connector changes, secrets, deploy, external pilot, launch, or autonomous action.

