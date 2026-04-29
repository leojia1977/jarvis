# S6 R2 Low-Risk Burn Pool

## Document Control

- Document: `S6_R2_LOW_RISK_BURN_POOL_2026_04_29`
- Date: 2026-04-29
- Trigger: `NEXT_EXACT_LOW_RISK_BURN_POOL`
- Mode: docs-only / checklist / reconciliation / source-pack / authority-pack
- Implementation authorization: NO

## Purpose

Keep bounded automation productive while Batch R1 waits for product/source/authority input. This pool must not bypass R1 blockers. It may only prepare evidence, prompts, parity tables, source requests, authority packs, and future launch readiness records.

## Decision

```text
R2_LOW_RISK_BURN_POOL_OPEN
DOCS_ONLY_NO_IMPLEMENTATION
```

## Queue

| Item | Lane | Allowed output | Stop condition |
| --- | --- | --- | --- |
| R2-01 | Jira parity audit refresh | repo Done vs Jira Done diff table; no cloud mutation unless explicitly authorized later | stop before Jira transition/create |
| R2-02 | R1 source input packet | consolidated source request pack for `AP-T06`, `AP-T09`, and `CD-T06` | stop before declaring any source delivered |
| R2-03 | R1 authority review prompt pack | Claude Web / governance prompt pack for `CH-T04`, `IN-T03`, and `MV-T02` | stop before implementation or authority conclusion fabrication |
| R2-04 | Dependent ticket HOLD map | dependency map for `AP-T11`, `AP-T12`, `CD-T07`, `IN-T06`, `MV-T05`, `AP-T02` | stop before closing dependent tickets |
| R2-05 | Sprint planning candidate board | candidate grouping: auto-ready, source-needed, authority-needed, blocked, no-code-only | stop before implementation GO |
| R2-06 | Runner heartbeat prompt | copy-ready heartbeat for docs-only low-risk runner execution | stop before code or Jira Done mutation |
| R2-07 | Backlog tracker parity note | note listing tracker/Jira/repo rows that need later exact mapping | stop before workbook or cloud edits unless later authorized |
| R2-08 | Idle fallback report | report explaining why no safe implementation exists and what unlocks next work | stop before product-scope expansion |

## Allowed Files

R2 may create or update only docs with one of these names:

```text
docs/S6_R2_*.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
releases/release_manifest.json
```

## Forbidden

- no implementation;
- no frontend source changes;
- no Storybook changes;
- no Playwright changes;
- no fixture / adapter / validator / `ResolvedSurfaceContext` changes;
- no backend / runtime / API / schema changes;
- no real data or anonymized real data;
- no secrets;
- no deploy, public endpoint, launch, or external pilot;
- no Jira Done transition, issue creation, or status mutation without later exact Jira sync authorization;
- no declaration that any R1 blocker is resolved unless the governed source/authority input has actually arrived.

## Required Gates

- `git diff --check`
- `py -3 scripts/git_preflight.py --mode pilot` before any docs-only closeout commit, if stage/commit/push is authorized.

## Next Route

```text
OPEN_R2_LOW_RISK_BURN_POOL_DOCS_ONLY_QUEUE
```
