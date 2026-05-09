# S6 RC-018 Customer Path Review Decision

Date: 2026-05-09

Candidate:

```text
LOCAL_OFFLINE_TRIAL_RC_018_CN
```

Review package:

```text
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review
```

Zip:

```text
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
```

Zip SHA256:

```text
d623f83657a0cf54cca99a2cedec30c59734ceed8d7b234455fedf88d96a9456
```

Decision:

```text
PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
```

Human confirmation:

```text
2026-05-09: Human confirmed RC-018 may enter the next internal/local trial;
N1-N5 do not block current RC-018; GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH
will carry the next small follow-up.
```

## Reconciliation

Two review readings were received for RC-018:

- Team 1 product-path review: `PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL`.
- Team 2 package-hygiene review: initial `HOLD_FOR_UI_OR_PACKAGE_FIXES`, then re-review `PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL` after `GOAL-RC018-01_CUSTOMER_ROUTE_PACKAGE_HYGIENE_FIX`.

Repo decision:

```text
ACCEPT_PASS_WITH_NOTES_AND_OPEN_RC018_02_FOLLOW_UP
```

Rationale:

- The customer product path is understandable from product home through incident workbench, AI advice source, ECI/VFE summary, missing evidence, collection window, and local feedback.
- Team 2's package-hygiene blockers were fixed in commit `4388e0b`; the new package zip excludes stale root indexes, old four-screenshot scan evidence, and engineering validation annex files from the customer-facing zip.
- Remaining notes N1-N5 are next-round product/package polish and regression evidence items. They do not block the current RC-018 internal/local trial decision.

## Closure Checks

| Check | Result |
| --- | --- |
| Product home first impression | PASS |
| Incident workbench first screen | PASS |
| AI advice source folded by default | PASS |
| AI advice source expanded copy | PASS_WITH_NOTES |
| ECI/VFE product explanation | PASS |
| Missing evidence and collection window | PASS |
| Local feedback preview | PASS |
| Package root hygiene | PASS |
| Current seven-screenshot package safety scan | PASS |
| Customer-facing zip excludes stale provider/stub/live-Qwen annex | PASS |
| Safety / boundary review | PASS |

## Open Notes For Next Round

### N1 Annex Language Polish

The package can enter the next internal/local trial, but annex evidence still contains engineering terms such as `qwen_fact_bundle`, `source_payload`, `provider_decision_hint`, `provider = fixture`, `provider_output_scan`, and `qwen_fact_bundle_directory`.

Next round should move these to `internal_validation/` or rewrite them as customer-readable local/offline synthetic metadata validation.

### N2 Conservative UI Action Copy

Two UI phrases should become more conservative:

- `查看部署准备` -> `查看本地接入准备`
- `隔离 finance-042 并锁定凭据` -> `待复核：finance-042 隔离与凭据锁定建议`

### N3 Mobile Incident Scroll Evidence

`04_incident_first_load_mobile.png` proves the mobile entry and folded AI source state, but it does not show the full conclusion cards, trusted boundary, and recommended action. Add a mobile scrolled-state screenshot in the next package.

### N4 AI Advice Source Folded State

AI advice source default folded behavior is accepted for RC-018. Preserve this as a regression check in the next package.

### N5 ECI/VFE Product Framing

ECI/VFE product framing is accepted for RC-018. Preserve the defensive framing and do not expose reusable attack path, payload, PoC, exploit steps, or topology reachability.

## Next Suggested Goal

```text
GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH
```

Scope:

- conservative UI copy polish for deployment/action wording
- annex language downshift into customer-readable local/offline metadata validation or `internal_validation/`
- mobile incident scrolled-state screenshot
- regression checks for folded AI source and ECI/VFE defensive framing

## Boundary

This decision does not authorize:

- real data
- masked-real data
- live Qwen/API/connectors
- production write-back
- customer-visible publish, deploy, or output
- external pilot
- production launch
- autonomous containment, remediation, isolation, blocking, approval, rejection, or action-mode choice

## Trial Unlock

RC-018 may enter the next internal/local trial using the hygiene-fixed package from commit `4388e0b`.

This is not a customer-visible release, external pilot, production launch, or live integration approval.
