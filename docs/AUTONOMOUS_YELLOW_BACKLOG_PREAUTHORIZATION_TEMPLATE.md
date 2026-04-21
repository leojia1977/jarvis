# Autonomous Yellow Backlog Preauthorization Template

## 1. Template Purpose

Use this template when preparing the next governed Yellow backlog preauthorization package for autonomous implementation work.

This template is not implementation authority by itself. A future backlog package must name the governed baseline, exact items, exact files, exact tests, required review path, full gate, release verification, staging scope, commit/push rules, and HOLD conditions before any Yellow item may run.

## 2. Required Package Header

Every Yellow backlog preauthorization package must include:

- snapshot and stage
- baseline commit, baseline snapshot, baseline manifest status, and baseline release sha256
- requested route and lane
- one-item-at-a-time rule
- exact file scope rule
- review, targeted-test, full-gate, release-verification, manifest PASS, exact-staging, commit, and push sequence
- inherited non-authorizations and HOLD boundaries

## 3. Anti-Overengineering Rules

Every future Yellow backlog package and every item inside it must include these rules:

1. Implement the smallest change that satisfies the exact ticket behavior and required tests.
2. Do not introduce a new abstraction, helper, registry, vocabulary, adapter, service, module, or generalized framework unless the item explicitly names it.
3. Do not generalize for future routes, states, statuses, formats, roles, backends, transports, or workflows.
4. Do not perform unrelated renames, reorganizations, cleanup refactors, or while-we-are-here improvements.
5. Prefer local assertions and narrowly scoped tests over framework-level changes.
6. Every changed line must map to an explicit item sentence, exact allowed behavior, or required test.
7. If a broader abstraction seems desirable, HOLD and record a scoped design note instead of implementing it.
8. Reviews must flag unnecessary abstraction, speculative generalization, and hidden scope expansion.
9. Any scope expansion means HOLD.

## 4. Per-Item Max-Change Budget

Each Yellow backlog item must include:

| Field | Required content |
| --- | --- |
| Item ID | Stable item identifier. |
| Route name | Exact route to open. |
| Lane | Yellow implementation or Yellow test-only. |
| Purpose | One sentence. |
| Allowed files | Exact file list. No glob-only scopes. |
| Exact allowed behavior | Bullet list of what may change. |
| Required tests | Exact commands. |
| Required assertions | Exact assertions or observable outcomes. |
| Max new helpers | `0`, unless explicitly listed; otherwise `1`. |
| Max new concept names | Only names listed in the item. |
| Explicit non-goals | Behaviors and files that must not change. |
| HOLD if | Exact stop conditions. |

If the item cannot be described this tightly, it is not ready for autonomous Yellow implementation and must become a Green docs-only ticket-prep or design-note route instead.

## 4.1 Optional SWE Agent Accelerator Block

SWE agent / mini-swe-agent is optional and disabled by default. Every future Yellow backlog item must explicitly state one of:

```text
SWE agent use: not authorized for this item
```

or:

```text
SWE agent use: authorized only as bounded implementation accelerator for this item
```

The authorized form may be used only after `S5-SWE-AGENT-YELLOW-BACKLOG-TEMPLATE-INTEGRATION-2026-04-21-001` closes with review PASS, full gate PASS, release verification PASS, manifest PASS, closeout commit, and push.

If an item authorizes SWE agent use, the item must include:

| Field | Required content |
| --- | --- |
| SWE agent role | Exactly `bounded implementation accelerator`. |
| Exact repo root | The repo path visible to the runner. |
| Exact command path | Absolute WSL command path and version check. |
| Exact allowed files | Same exact file list as the Yellow item; no extra files. |
| Exact allowed behavior | Same item behavior; no scope expansion. |
| Required tests | Exact commands the item already requires. |
| Max-change budget | Explicit maximum changed files, helpers, and concept names. |
| Model/credential path | `not used` or governed non-secret path; values must not be printed. |
| Output location | Prefer outside repo unless the item names an in-repo artifact. |
| Before/after checks | `git status --short`, no staged files, exact diff scope. |
| Review path | Independent review of generated output; SWE agent cannot review itself. |
| Closeout ownership | Codex owns manifest, gate, release, staging plan, commit, and push under policy. |
| HOLD if | Unlisted file, unexpected mutation, staged file, secret/real-data/browser/session access, network/model ambiguity, Red trigger, or out-of-scope test failure. |

SWE agent must not select route, define acceptance criteria, expand scope, replace review, own closeout, update manifest, run release packaging, stage, commit, push, or perform remote actions.

Existing Yellow backlog packages and closed/current items do not inherit SWE agent authority retroactively. A later item must explicitly name SWE agent to use it.

## 5. Review Checklist

Review must check:

- allowed files match the item
- tests match the item
- SWE agent is either explicitly `not authorized for this item` or is tightly bounded by the optional accelerator block
- no unrelated file, helper, abstraction, cleanup, rename, or reorganizing is included
- no future-facing generalization is introduced
- no new status, event, vocabulary, panel, schema, route, adapter, service, or workflow is introduced unless explicitly named
- no runtime/API/schema, public endpoint, launch, deploy, real data, credential, parked-stream reopen, Red-3, S4-A resolver, or AI_COLLAB boundary is crossed
- Claude Code review-only or Claude Web fallback is review evidence only and not authority

## 6. Closeout Sequence

Each item may close only after this exact order:

1. Review PASS or PASS_WITH_FINDINGS with no blocking finding.
2. Targeted tests PASS.
3. Full gate PASS.
4. Release package produced.
5. Release verification PASS.
6. Manifest updated from PENDING to PASS by verification.
7. Exact files staged.
8. Commit.
9. Push.

No gate may be skipped, reordered, inferred, or satisfied retroactively.

## 7. Standing Non-Authorization

This template does not authorize:

- implementation by itself
- unlisted files
- broad refactors
- reusable framework work not named by an item
- runtime/API/schema behavior
- public endpoint work
- dependency or fixture changes unless explicitly listed
- release-script or contract changes unless explicitly listed
- AI_COLLAB changes
- launch or deployment
- external pilot execution or readiness
- credential handling
- real-data handling
- evidence retention or redaction policy freeze
- S5-B/S5-D reopen
- ORDIV work
- Red-3 action
- AdsPower profile creation/switching or Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection
