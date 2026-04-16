# ORDIV-L1A OpenPyXL Dependency Decision

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | ORDIV-L1A OpenPyXL Dependency Decision |
| Status | Closed as governed ORDIV-L1A OpenPyXL dependency decision baseline; docs-only dependency decision; not implementation authorization |
| Baseline | ORDIV-L1A01-TICKET-DEF-2026-04-16-001 / commit `6252259d0b9370d95e0ba6623a22dff7e4a100d8` |
| Predecessor | docs/ORDIV_L1A_01_SIEM_ALERT_XLSX_MAPPING_TICKET.md |
| Route | OPEN_ORDIV_L1A_DEPENDENCY_APPROVAL_DECISION |
| Primary implementor for this docs-only draft | VS Code / human-supervised workspace |
| Codex role | planning only |
| Reviewer | Claude Code review-only |
| requires_external_review | Trigger-based: false for `PARK_L1A_UNTIL_OPENPYXL_AVAILABLE` or `APPROVE_LOCAL_ENV_OPENPYXL_ONLY` with no repo dependency changes; true if the decision selects a tracked dependency addition, dependency governance change, release-process change, frozen contract change, parser contract freeze, real-data/evidence-retention/redaction policy freeze, or stream/milestone closeout. |

This draft does not install `openpyxl`, does not modify dependency files, and does not authorize ORDIV-L1A implementation. If the route later changes from local-only/park to tracked dependency governance, the work must HOLD and set `requires_external_review=true` before proceeding.

Review closeout note: Claude Code review-only returned GO. No HIGH, MEDIUM, LOW, or INFO findings remain. Claude Web escalation is not required for this docs-only dependency decision because it selects local-only / park behavior and does not add tracked dependencies, modify frozen contracts, change dependency governance, create dependency manifests, change release process, freeze parser contracts, touch real data, or perform stream/milestone closeout.

## 2. Goal

Draft a docs-only dependency approval decision for ORDIV-L1A-01 after preflight found `openpyxl_available=False`.

This decision must decide the safe route for handling the missing `.xlsx` parser dependency before ORDIV-L1A implementation can begin.

This decision must not:

- implement the SIEM alert `.xlsx` adapter
- install `openpyxl`
- modify dependency files
- modify code or tests
- create fixtures
- run local real-data validation

## 3. Baseline Summary

- Current governed baseline is `ORDIV-L1A01-TICKET-DEF-2026-04-16-001`.
- Current baseline commit is `6252259d0b9370d95e0ba6623a22dff7e4a100d8`.
- Predecessor artifact is `docs/ORDIV_L1A_01_SIEM_ALERT_XLSX_MAPPING_TICKET.md`.
- ORDIV-L1A-01 is a governed docs-only ticket-definition baseline for a later narrow SIEM alert `.xlsx` mapping adapter.
- ORDIV-L1A-01 permits only a later separate implementation ticket draft; it does not authorize implementation now.
- The governed L1A ticket definition allows `openpyxl` only if already available and no dependency file changes are needed.
- If `openpyxl` is unavailable or dependency files must change, L1A must HOLD for dependency approval and external-review evaluation.
- S5-B and S5-D remain `PASS_AND_PARK`.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- External pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- AI_COLLAB files and contracts remain unchanged.

## 4. Preflight Finding

- `openpyxl_available=False`.
- Therefore ORDIV-L1A implementation is currently HOLD under the governed L1A ticket definition.
- No adapter implementation may begin until dependency handling is resolved.
- This finding does not authorize installation, dependency file edits, adapter code, tests, fixtures, validation reports, or local real-data execution.

## 5. Role Boundary

- VS Code / human-supervised workspace is primary implementor for this docs-only draft.
- Codex role is planning and prompt orchestration only.
- Claude Code reviews this draft in review-only mode after creation.
- Claude Web is not required for a local-only or park decision with no repo dependency changes.
- Claude Web should be required if this decision approves a new tracked runtime/build dependency, dependency governance/release-process changes, frozen contract changes, parser contract freeze, real-data/evidence-retention/redaction policy freeze, or stream/milestone closeout.
- Human go/no-go remains required before any future implementation route.

## 6. Candidate Routes

| Candidate route | Meaning | Current posture | Recommendation |
| --- | --- | --- | --- |
| `PARK_L1A_UNTIL_OPENPYXL_AVAILABLE` | Do not change repo or dependencies. Wait until `openpyxl` is present in the environment, then rerun preflight. | Safe fallback; no repo changes. | Recommended fallback. |
| `APPROVE_LOCAL_ENV_OPENPYXL_ONLY` | Human may install/provide `openpyxl` outside repo without modifying tracked dependency files; implementation can proceed only after preflight confirms `openpyxl_available=True`. | Preferred if human accepts local environment preparation outside repo. | Preferred route. |
| `APPROVE_TRACKED_DEPENDENCY_ADDITION` | Add `openpyxl` to a tracked dependency manifest if the repo has or chooses one. This route cannot be activated by chat instruction alone; it requires a new separate governed tracked-dependency decision ticket or equivalent governed route selection, with `requires_external_review=true` and Claude Web or a human-designated qualified external review path before any tracked dependency file work begins. | High governance impact because it creates a new runtime/build dependency. | Not recommended in this draft unless human explicitly requests formal dependency governance. |
| `HAND_ROLL_XLSX_READER` | Implement `.xlsx` parsing without `openpyxl`. | High parser-risk and security-risk path. | Not recommended / HOLD. |
| `CHANGE_INPUT_FORMAT_TO_CSV` | Change ORDIV-L1A input from `.xlsx` to `.csv`. | Changes the governed L1A input boundary. | Not recommended / out of scope. |

## 7. Route Risk Matrix

| Route | Main risk | External-review implication | HOLD trigger | Non-authorization note |
| --- | --- | --- | --- | --- |
| `PARK_L1A_UNTIL_OPENPYXL_AVAILABLE` | Work stalls until the environment has the dependency. | Claude Web not required if no repo dependency change occurs. | Any attempt to implement before `openpyxl_available=True`. | Does not authorize adapter work. |
| `APPROVE_LOCAL_ENV_OPENPYXL_ONLY` | Local environment may drift from tracked dependency state. | Claude Web not required if no repo dependency change occurs and no contract is frozen. | Any tracked dependency file change, dependency pin, or repo metadata change. | Allows only human-provided local environment preparation outside repo. |
| `APPROVE_TRACKED_DEPENDENCY_ADDITION` | Adds a new runtime/build dependency and may alter release/build expectations. | `requires_external_review=true`; Claude Web should be required unless human governance selects another qualified external review path. | Missing dependency strategy; missing dependency manifest / package-file policy; any attempt to combine tracked dependency addition with adapter implementation. | Does not authorize adapter work in the same ticket. |
| `HAND_ROLL_XLSX_READER` | Reimplements complex file parsing and may mishandle malicious or malformed files. | Would require external review if selected, but should HOLD. | Hand-rolled parser proposal appears in implementation scope. | Not a safe route for ORDIV-L1A. |
| `CHANGE_INPUT_FORMAT_TO_CSV` | Changes the governed ORDIV-L1A input contract from `.xlsx` to `.csv`. | Would require external review and likely route redefinition. | CSV route is treated as replacement for `.xlsx` without new scoped decision. | Out of scope for this dependency decision. |

## 8. Recommended Route

Recommended route: `APPROVE_LOCAL_ENV_OPENPYXL_ONLY`, with fallback `PARK_L1A_UNTIL_OPENPYXL_AVAILABLE`.

Meaning:

- Prefer human-provided local `openpyxl` outside repo.
- No repository files change for dependency handling.
- No dependency files change.
- No dependency pin is committed.
- ORDIV-L1A implementation remains HOLD until preflight confirms `openpyxl_available=True`.
- If local environment preparation is not accepted, park ORDIV-L1A until `openpyxl` is available.

Non-meaning:

- Does not authorize installation by this draft.
- Does not authorize dependency file edits.
- Does not authorize adapter implementation.
- Does not authorize tests or fixtures.
- Does not authorize tracked dependency addition.
- Does not authorize changing input format to `.csv`.
- Does not authorize hand-rolled `.xlsx` parsing.

## 9. Dependency Governance Boundary

This draft may approve only the dependency-handling route, not installation.

If the local-only route is selected:

- no repo files change
- no dependency files change
- no dependency pin is committed
- no implementation begins until preflight confirms `openpyxl_available=True`
- no Claude Web escalation is required solely for the local-only decision

If the tracked dependency route is selected:

- a chat instruction alone is not sufficient to activate tracked dependency work
- a new separate governed tracked-dependency decision ticket or equivalent governed route selection is required
- HOLD for external review
- set `requires_external_review=true`
- use Claude Web or a human-designated qualified external review path before any tracked dependency file work begins
- identify dependency file strategy separately
- identify dependency manifest / package-file policy separately
- do not implement adapter in the same ticket
- do not modify release scripts in this decision
- do not modify AI_COLLAB files/contracts in this decision
- do not invent a dependency manifest if none exists

If no dependency manifest exists, this draft must not create one, name one as mandatory, or imply that dependency governance has been frozen.

## 10. Non-Authorization

This draft does not authorize:

- adapter implementation
- code changes
- tests
- dependency installation
- dependency file changes
- lockfile/package metadata changes
- fixture creation
- local real-data execution
- evidence retention
- validation report creation
- runtime integration
- `SIEMAdapterProtocol` changes
- tracked dependency addition
- dependency manifest creation
- release-process changes
- S5-B reopen
- S5-D reopen
- S4-A resolver changes
- public close-case endpoint work
- AI_COLLAB changes
- external pilot readiness
- external pilot execution
- real customer/operator sign-off
- staging
- commit
- push

## 11. HOLD Conditions

This decision or any follow-up work must HOLD if:

- `openpyxl` remains unavailable.
- Any tracked dependency file must change.
- No clear dependency governance route is selected.
- Implementation starts before dependency handling is resolved.
- A hand-rolled parser is proposed.
- Input format changes from `.xlsx`.
- Real `.xlsx` data enters repo or review material.
- Tests, fixtures, or code appear in this decision.
- External review is required but not completed.
- Dependency installation is attempted from this draft.
- A dependency manifest is created or changed by this draft.
- Release scripts are changed.
- AI_COLLAB files or contracts are changed.
- S5-B or S5-D reopen is implied.
- S4-A resolver behavior changes.
- Public close-case endpoint work appears.
- External pilot readiness or execution is implied.
- Evidence retention or redaction policy freeze appears.

## 12. Claude Web Escalation Criteria

Claude Web is not required if the decision only selects:

- `PARK_L1A_UNTIL_OPENPYXL_AVAILABLE`
- `APPROVE_LOCAL_ENV_OPENPYXL_ONLY` with no repo dependency changes

Claude Web should be required if the decision approves or requires:

- new tracked runtime/build dependency
- dependency manifest or release-process change
- frozen contract change
- new parser contract freeze
- real data/evidence retention/redaction policy freeze
- stream/milestone closeout

If Claude Web is required and unavailable, the work must HOLD unless human product/governance explicitly designates an alternative qualified external review path.

## 13. Acceptance Criteria

This draft is acceptable if:

- exactly one new docs-only file is created
- status is closed as governed ORDIV-L1A OpenPyXL dependency decision baseline and remains explicitly non-authorizing
- `openpyxl_available=False` is recorded
- ORDIV-L1A implementation is marked HOLD until dependency handling is resolved
- all five candidate routes are compared
- recommended route is `APPROVE_LOCAL_ENV_OPENPYXL_ONLY` with fallback `PARK_L1A_UNTIL_OPENPYXL_AVAILABLE`
- tracked dependency addition is not recommended unless human explicitly requests formal dependency governance
- hand-rolled `.xlsx` parsing is not recommended
- changing input format to `.csv` is out of scope
- dependency governance boundary is explicit
- Claude Web escalation criteria are explicit
- no adapter implementation, code, tests, dependency installation, dependency file changes, lockfile/package metadata changes, fixture creation, local real-data execution, validation reports, evidence retention, runtime integration, `SIEMAdapterProtocol` changes, S5-B/S5-D reopen, S4-A resolver changes, public close-case endpoint work, AI_COLLAB changes, external pilot readiness/execution, staging, commit, or push is authorized
- HANDOFF and manifest are modified only for governed closeout metadata; verify report, code, tests, fixtures, config, dependencies, AI_COLLAB files, and contracts are not manually modified

## 14. Preliminary Recommendation

`PRELIMINARY_RECOMMENDATION_APPROVE_LOCAL_ENV_OPENPYXL_ONLY_OR_PARK`

Meaning:

- Prefer human-provided local `openpyxl` outside repo.
- Rerun preflight after local environment preparation.
- If local environment preparation is not accepted, park ORDIV-L1A implementation.
- Do not implement the adapter until `openpyxl_available=True`.

Non-meaning:

- Does not install `openpyxl`.
- Does not change dependency files.
- Does not approve a tracked dependency addition.
- Does not implement adapter code.
- Does not add tests.
- Does not create fixtures.
- Does not run local real-data validation.
- Does not authorize evidence retention.
- Does not change release process, AI_COLLAB, S5-B, S5-D, S4-A, or public close-case endpoint boundaries.
