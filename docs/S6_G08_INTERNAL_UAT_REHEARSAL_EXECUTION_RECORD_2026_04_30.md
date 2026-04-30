# S6 G08 Internal UAT Rehearsal Execution Record 2026-04-30

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | G-08 internal UAT rehearsal execution record |
| Date | 2026-04-30 |
| Scope | Synthetic-only evidence-backed internal rehearsal |
| Source package | `docs/S6_G08_INTERNAL_UAT_REHEARSAL_EXECUTION_PACKAGE_2026_04_30.md` |
| Completed score instance | `docs/S6_G08_INTERNAL_UAT_REHEARSAL_COMPLETED_SCORE_INSTANCE_2026_04_30.md` |

## 2. Decision

```text
G08_INTERNAL_UAT_REHEARSAL_EXECUTED_SYNTHETIC_ONLY
G08_DECISION = G08_REHEARSAL_CONDITIONAL_PASS_WITH_NOTES
CUSTOMER_VISIBLE_UAT_NOT_AUTHORIZED
S1_CLOSED_SHADOW_NOT_AUTHORIZED
```

Reason:

- UAT-01 through UAT-20 have completed synthetic Qwen output evidence from `S0-QWEN-2026-04-30-002-RESCORE`.
- Required content and forbidden-output checks pass for all UAT rows.
- Targeted frontend and Playwright gates pass for the critical UAT-02 and UAT-19 evidence lines.
- The only remaining note is that UAT-02 currently proves `AUD-004` id/type/source behavior, but not an explicit timestamp field in the mock STATE_SYNC payload or audit fixture.

## 3. Evidence Summary

| Evidence | Result | Reference |
| --- | --- | --- |
| UAT-01 through UAT-20 model outputs | PASS | `artifacts/s0_qwen_runs/2026-04-30-002-rescore/outputs/` |
| S0 scorecard | 20 / 20 PASS | `artifacts/s0_qwen_runs/2026-04-30-002-rescore/scoring/s0_scorecard.csv` |
| Action-command scan | PASS | `artifacts/s0_qwen_runs/2026-04-30-002-rescore/scoring/action_command_scan.csv` |
| Prompt-injection verdict | PASS for UAT-20 | `artifacts/s0_qwen_runs/2026-04-30-002-rescore/scoring/prompt_injection_verdicts.csv` |
| UAT-02 mock STATE_SYNC gate | PASS with timestamp note | `frontend/tests/e2e/approval.acceptance.spec.ts` |
| UAT-19 P3 DOM isolation | PASS | `frontend/tests/e2e/core-surface.p3-dom-isolation.spec.ts` |
| Static redline isolation | PASS | `frontend/tests/e2e/core-surface.redline-expansion.spec.ts` |
| Component/unit regression | PASS, 59 tests | `npx vitest run src/App.test.tsx --exclude tests/e2e/**` |
| Targeted Playwright regression | PASS, 9 tests | `npx playwright test tests/e2e/approval.acceptance.spec.ts tests/e2e/core-surface.p3-dom-isolation.spec.ts tests/e2e/core-surface.redline-expansion.spec.ts` |

## 4. UAT-02 State-Sync Proof

Result:

```text
UAT02_STATE_SYNC_PROOF = PASS_WITH_TIMESTAMP_NOTE
```

Confirmed:

- Clock fast-forward alone is not a state transition authority.
- The app requires mock `STATE_SYNC` / `secupilot:mock-state-sync` to migrate from `OBSERVATION_WINDOW` back to `PENDING_APPROVAL`.
- The emitted event carries `state_sync_source = mock_state_sync`.
- The emitted event carries `audit_event_id = AUD-004`.
- The emitted event carries `audit_event_type = OBSERVATION_WINDOW_EXPIRED`.
- The UI exposes `observation-expired-notice` with `data-state-sync-source = mock_state_sync`.
- No auto-execute label or auto-execution progress is mounted.

Remaining note:

```text
UAT02_TIMESTAMP_FIELD_NOT_PRESENT_IN_CURRENT_MOCK_SYNC_PAYLOAD
```

Before formal S1 Go/No-Go, either the mock STATE_SYNC proof must add a governed timestamp field, or the S1 reviewer must explicitly accept the current `AUD-004` id/type/source proof as equivalent synthetic evidence.

## 5. UAT-19 P3 Isolation Proof

Result:

```text
UAT19_P3_ISOLATION_PROOF = PASS
```

Confirmed:

- P3 receives management-summary evidence only.
- `host-raw-evidence` is not attached.
- `p2-evidence-drawer` is not attached.
- `full-audit-trail` is not attached for P3 manager summary use.
- Approval action controls are not mounted in the P3 path.
- The Qwen synthetic output for UAT-19 preserves the P3 management-summary boundary and does not request host-level raw evidence.

## 6. Act III Pacing Note

Result:

```text
ACT_III_PACING = TRUSTWORTHY_AND_HONEST_BUT_DENSE
```

Recommendation:

- Keep the full Act III for internal reviewer rehearsal.
- For a later customer-visible rehearsal, use the shortened Act III path if time is constrained:

```text
UAT-14, UAT-17, UAT-19, UAT-20
```

This keeps the honesty and boundary story visible without making the product feel blocked at every step.

## 7. Remaining S1 Impact

G-08 state:

```text
G08 = CONDITIONAL_PASS_WITH_NOTES_PENDING_UAT02_TIMESTAMP_PROOF_OR_REVIEWER_ACCEPTANCE
```

S1 remains not ready because:

```text
G01_G06_G09_EXTERNAL_EVIDENCE_REQUIRED
G07_SIGNOFF_REQUIRED
G08_TIMESTAMP_NOTE_REQUIRES_REVIEWER_ACCEPTANCE_OR_FOLLOWUP
```

## 8. Non-Authorization

This record does not authorize:

```text
customer-visible staging or demo
real data
masked real data
S1 closed shadow
backend/runtime/API/schema
connector changes
secrets
deploy
external pilot
launch
autonomous action
```
