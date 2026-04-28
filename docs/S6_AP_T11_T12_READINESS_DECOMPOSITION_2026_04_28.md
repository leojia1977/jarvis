# S6 AP-T11 / AP-T12 Readiness Decomposition 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 AP-T11 / AP-T12 Readiness Decomposition 2026-04-28 |
| Tickets | `AP-T11`, `AP-T12` |
| Scope | AP state-transition assertions and AP acceptance-suite readiness |
| Status | HOLD_DEPENDENCY_NOT_READY_WITH_STATIC_ASSERTION_SPLIT_CANDIDATE |
| Date | 2026-04-28 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Queue | `docs\S6_EXTENDED_BOUNDED_AUTOMATION_AUTHORIZATION_2026_04_28.md` |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Reviewer | Not required for readiness-only decomposition |
| Review surface | `not_required_no_implementation_diff` |
| External review | not required |
| SWE | disabled |

This record decomposes AP-T11 and AP-T12 after AP-T08 closeout.

It does not authorize implementation, new tests, backend/runtime/API/schema changes, Storybook, Playwright, fixture registry changes, Jira Done transition, real data, secrets, deploy, public endpoint, or external pilot.

## 2. Decision

Decision:

```text
AP_T11_FULL_HOLD_DEPENDENCY_NOT_READY
AP_T12_FULL_HOLD_DEPENDENCY_NOT_READY
AP_T11A_STATIC_NO_MUTATION_ASSERTION_SPLIT_CANDIDATE
```

Meaning:

- Full `AP-T11` cannot start because full AP state-transition behavior is not implemented.
- Full `AP-T12` cannot start because the AP acceptance suite depends on AP route, CTA, audit, state, observation-window, and audit-empty/unavailable behavior.
- A later narrow `AP-T11A` split may be considered for static no-mutation assertions only, because existing AP-T03 / AP-T04 / AP-T05 / AP-T06A / AP-T07 / AP-T08 surfaces already expose stable static boundaries.
- This record does not itself open or authorize `AP-T11A`.

## 3. Current AP Dependency State

| Dependency | Current state | Result |
| --- | --- | --- |
| `AP-T01` route shell / guard | Done | Satisfied for shell scope |
| `AP-T03` CTA boundary | Done | Satisfied for inert CTA boundary |
| `AP-T04` Strong Confirm shell | Done | Satisfied for disabled confirmation shell |
| `AP-T05` Delay / Observe configuration shell | Done | Satisfied for disabled configuration shell |
| `AP-T06A` static observation-window skeleton | Done split ticket | Helpful but not full `AP-T06` |
| Full `AP-T06` countdown / state-sync | HOLD | Blocking |
| `AP-T07` approved-pending locked skeleton | Done | Satisfied for locked display skeleton |
| `AP-T08` approval-audit source boundary | Done | Satisfied for display-only audit source boundary |
| `AP-T09` audit empty/unavailable state | HOLD | Blocking for full AP acceptance |

## 4. AP-T11 Readiness

Full `AP-T11` should remain HOLD because:

- full state-transition behavior is not implemented;
- full `AP-T06` countdown / state-sync remains HOLD pending exact state-sync input and test hook;
- `AP-T09` audit empty/unavailable behavior remains HOLD;
- implementing AP-T11 now would risk turning static semantic shells into implied state-transition behavior.

Potential later split:

```text
AP-T11A - static no-mutation AP assertion suite
```

Allowed only if a later exact checklist returns GO:

- assert AP-T03 CTA boundary is inert and scoped to P2;
- assert AP-T04 Strong Confirm shell keeps submit disabled;
- assert AP-T05 Delay / Observe shell keeps submit disabled and has no frontend timer authority;
- assert AP-T06A static observation-window skeleton has `data-state-sync="not-implemented"` and no mutation;
- assert AP-T07 approved-pending skeleton is locked and has no write controls;
- assert AP-T08 approval-audit source boundary is display-only;
- no AP state transition, no ActionMode creation, no backend/runtime/API/schema, no fixture/adapter/validator, and no `ResolvedSurfaceContext` changes.

## 5. AP-T12 Readiness

Full `AP-T12` should remain HOLD because:

- it is an AP acceptance suite, not an implementation shortcut;
- it requires the AP implementation chain to be complete or explicitly split into governed static and dynamic acceptance lanes;
- full `AP-T06`, `AP-T09`, and any true state-transition assertions are still unresolved;
- marking AP-T12 Done now would overstate Sprint 2 AP readiness.

## 6. Non-Goals Preserved

This decomposition does not implement:

- AP state transitions;
- observation-window countdown or state-sync;
- audit empty/unavailable rendering;
- Strong Confirm submission;
- Delay / Observe submission;
- approval mutation;
- `ActionMode` creation;
- backend/runtime/API/schema changes;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- real data, secrets, deploy, public endpoint, or external pilot.

## 7. Jira

Do not mark `AP-T11` or `AP-T12` Done.

Jira may receive readiness/HOLD comments later only when Jira environment variables are visible and safe.

## 8. Next Route

```text
OPEN_MV_T05_READINESS_CHECKLIST
```
