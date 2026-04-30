# S6 S0-002 Readiness Preflight Report 2026-04-30

## 1. Decision

```text
S0_002_PREFLIGHT_PASS_WAITING_FOR_CLOUD_RECOVERY
S0_002_RERUN_STATUS = NOT_STARTED_WAITING_FOR_CLOUD_RECOVERY_EVIDENCE
```

## 2. Scope

- Input: current 20 repo-local synthetic QwenFactBundle files only.
- Real data: NO.
- Masked real data: NO.
- Qwen execution: NO.
- Backend/runtime/API/schema changes: NO.

## 3. Prompt Budget Summary

| Metric | Value |
| --- | --- |
| bundle count | 20 |
| max chars | 2722 |
| max estimated tokens | 681 |
| max input chars limit | 12000 |
| max input token estimate limit | 3000 |
| over char limit | 0 |
| over token estimate limit | 0 |

## 4. Cloud Recovery Gate

S0-002 must not run until all three non-secret cloud recovery checks are true:

- EngineCore alive.
- `/v1/models` available.
- Minimal synthetic chat completion succeeds.

## 5. Per-Bundle Preflight

| UAT | File | Chars | Est tokens | Synthetic | Budget | Findings |
| --- | --- | --- | --- | --- | --- | --- |
| UAT-01 | uat-01_s0-qf-uat-01-ntlm-lateral.json | 2670 | 668 | YES | YES | none |
| UAT-02 | uat-02_s0-qf-uat-02-observation-expiry.json | 2722 | 681 | YES | YES | none |
| UAT-03 | uat-03_s0-qf-uat-03-terminal-lock.json | 2608 | 652 | YES | YES | none |
| UAT-04 | uat-04_s0-qf-uat-04-ransomware-staging.json | 2622 | 656 | YES | YES | none |
| UAT-05 | uat-05_s0-qf-uat-05-kerberoasting-spn.json | 2609 | 653 | YES | YES | none |
| UAT-06 | uat-06_s0-qf-uat-06-mfa-fatigue.json | 2629 | 658 | YES | YES | none |
| UAT-07 | uat-07_s0-qf-uat-07-oauth-consent.json | 2596 | 649 | YES | YES | none |
| UAT-08 | uat-08_s0-qf-uat-08-cloud-key.json | 2612 | 653 | YES | YES | none |
| UAT-09 | uat-09_s0-qf-uat-09-dns-tunneling.json | 2626 | 657 | YES | YES | none |
| UAT-10 | uat-10_s0-qf-uat-10-c2-low-slow.json | 2651 | 663 | YES | YES | none |
| UAT-11 | uat-11_s0-qf-uat-11-lotl-wmi-psexec.json | 2613 | 654 | YES | YES | none |
| UAT-12 | uat-12_s0-qf-uat-12-vpn-geo.json | 2598 | 650 | YES | YES | none |
| UAT-13 | uat-13_s0-qf-uat-13-insider-download.json | 2651 | 663 | YES | YES | none |
| UAT-14 | uat-14_s0-qf-uat-14-cmdb-unavailable.json | 2597 | 650 | YES | YES | none |
| UAT-15 | uat-15_s0-qf-uat-15-audit-empty.json | 2551 | 638 | YES | YES | none |
| UAT-16 | uat-16_s0-qf-uat-16-audit-unavailable.json | 2620 | 655 | YES | YES | none |
| UAT-17 | uat-17_s0-qf-uat-17-history-downgrade.json | 2655 | 664 | YES | YES | none |
| UAT-18 | uat-18_s0-qf-uat-18-history-upgrade-prohibited.json | 2638 | 660 | YES | YES | none |
| UAT-19 | uat-19_s0-qf-uat-19-p3-summary-no-raw.json | 2635 | 659 | YES | YES | none |
| UAT-20 | uat-20_s0-qf-uat-20-prompt-injection.json | 2696 | 674 | YES | YES | none |

## 6. Non-Authorization

This report does not authorize real data, masked real data, closed shadow, customer-visible staging or demo, backend/runtime/API/schema, connector changes, secrets, deploy, external pilot, launch, or autonomous action.
