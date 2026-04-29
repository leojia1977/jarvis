# S6 AP-T02 P0 Readonly Approval Test Harness Closeout 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T02` |
| Jira issue | `SCRUM-54` |
| Scope | P0 readonly approval context source via approved test harness only |
| Status | `AP_T02_TEST_HARNESS_SOURCE_IMPLEMENTED_GATE_PASS_CLAUDE_CODE_FINDINGS_FIXED_JIRA_DONE_SYNCED` |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |

## 2. Decision

```text
AP_T02_TEST_HARNESS_SOURCE_IMPLEMENTED_GATE_PASS_CLAUDE_CODE_FINDINGS_FIXED_JIRA_DONE_SYNCED
PRODUCT_ROUTE_IMPLEMENTATION_NOT_AUTHORIZED
```

Jarvis provided the governed AP-T02 input and authorized the Option B
test-harness-only path. The implementation creates a P0 readonly approval
context only inside test scope, validates it through `ContextValidator`, and
uses it to prove the existing approval shell remains read-only for P0.

## 3. Changed Files

```text
frontend/src/App.test.tsx
docs/S6_AP_T02_P0_READONLY_APPROVAL_CONTEXT_SOURCE_CHECKLIST_2026_04_29.md
docs/S6_AP_T02_P0_READONLY_APPROVAL_TEST_HARNESS_CLOSEOUT_2026_04_29.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
releases/release_manifest.json
```

`releases/release_manifest.json` may be refreshed by the pilot preflight gate.

## 4. Implementation Evidence

`frontend/src/App.test.tsx` now includes
`buildP0ReadonlyApprovalTestHarnessContext()`.

The helper:

- starts from the existing artificial phase-2 P2 approval fixture;
- sets `session.role = "P0"`;
- uses `surface = "CROSS_SURFACE"` because this path is test-harness-only;
- keeps `action_mode = null`;
- downgrades every inherited `action_permissions` key to `READONLY`;
- downgrades every inherited `resolved_visibility.allowed_actions` key to
  `READONLY`;
- marks the approval page as `READONLY`;
- validates the resulting context through `validateResolvedSurfaceContext()`;
- is not exported to product route, Storybook, Playwright, fixture, adapter, or
  runtime code.

## 5. Test Evidence

Added test:

```text
renders AP-T02 P0 approval as readonly from the governed test harness only
```

Assertions confirm:

- `data-role="P0"`;
- `data-approval-mode="readonly-container"`;
- `data-authority-source="resolved-surface-context"`;
- `data-route-authority="resolved-surface-context"`;
- status display is `PENDING_APPROVAL` with `display-only` authority;
- mapping source remains `D-02`;
- state migration is `none`;
- audit boundary is display-only and sourced from `activeContext.audit_trail`;
- no approval CTA boundary is mounted;
- no approve/reject/delay/observe controls are mounted;
- every `action_permissions` and `resolved_visibility.allowed_actions` value is
  `READONLY`;
- no dialog is mounted;
- URL search, `localStorage`, and `sessionStorage` do not become authority;
- `IMMEDIATE`, `DELAYED`, and `OBSERVE_ONLY` do not appear.

Targeted frontend gate:

```text
npm test -- --run App.test.tsx
1 passed / 59 tests passed
```

Full gate:

```text
npm test
5 files passed / 96 tests passed

npm run build
PASS

git diff --check
PASS with Windows line-ending warnings only

py -3 scripts/git_preflight.py --mode pilot
PASS / backend guard 164 tests / release verification PASS
```

Claude Code focused review:

```text
Initial verdict: PASS_WITH_FINDINGS
Finding 1 fixed: P0 harness no longer inherits P2 action permissions; every inherited action_permissions and allowed_actions key is downgraded to READONLY.
Finding 2 fixed: status / next-route tokens aligned.
Re-review verdict: PASS_WITH_FINDINGS with P3 doc-token note only; note fixed before closeout.
```

## 6. Non-Authorization

This closeout does not authorize:

- production P0 `/approval` route entry;
- new fixture phase;
- Storybook or Playwright source;
- fixture/adapter/validator file changes;
- `ResolvedSurfaceContext` model changes;
- backend/runtime/API/schema;
- real data or anonymized real data;
- secrets;
- deploy;
- public endpoint;
- external pilot;
- launch.

## 7. Jira

`SCRUM-54` was verified as `[AP-T02] P0 readonly approval container`, received
repo closeout evidence, and is now `已完成`.

## 8. Next Route

```text
OPEN_AP_T12_FULL_AP_ACCEPTANCE_RECHECK_OR_PARENT_EPIC_CLOSURE_REVIEW
```
