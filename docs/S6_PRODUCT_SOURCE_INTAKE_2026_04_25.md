# S6 Product Source Intake 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Product Source Intake 2026-04-25 |
| Status | READY_FOR_ROUTE_SELECTION_DRAFT_UPDATED |
| Date | 2026-04-25 |
| Intake started | 2026-04-25 14:15 Asia/Shanghai |
| Intake recorded | 2026-04-25 14:25 Asia/Shanghai |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `4d6b380` |
| Source package root | `D:\产品设计\secupilot0421\incoming_pending` |
| Source authority | Human declared package complete and authorized intake |
| Update | P2 Model Contract supplied after initial intake |

This record organizes the incoming product-source package and decides whether route selection may proceed.

It does not authorize implementation, code/test changes, dependency changes, schema/API changes, launch, deploy, public endpoint work, real-data handling, credential handling, external pilot execution, parked-stream reopen, AI_COLLAB changes, staging, commit, or push.

## 2. Human Intake Constraint

Human instruction for this intake:

```text
HTML 是视觉与交互原型，Model Contract 与 PRD 是实现依据；不得直接把静态 HTML 当作最终前端代码照抄上线。
```

This instruction is binding for route selection and ticket readiness.

## 3. Safety Screen

Result:

```text
PASS_WITH_NOTES
```

Notes:

- No actual API keys, tokens, cookies, auth headers, private keys, credentials, browser session material, or unredacted customer evidence were found in the readable product-source files.
- Matches for `token`, `secrets`, `credentials`, and related terms are governance prohibitions or non-goal statements.
- HTML files contain static prototype sample host/user/business text and a Google Fonts link. Treat all HTML content as visual and interaction reference only.
- Data mode for implementation planning remains `synthetic/local only`.

## 4. Source Package Triage

### 4.1 Canonical Implementation Basis

Use these as the primary semantic sources for implementation planning:

| Source | Role | SHA256 |
| --- | --- | --- |
| `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版 (2).md` | Frozen engineering PRD and requirement baseline | `6C7445D38E57DE3FE0CA2E4BC86FC87F0302BEF315B2F8C0725F45185EF50C17` |
| `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2 (1).md` | Bounded implementation GO / NO-GO boundary | `67EA5DACB40DD9725B8B7AC2E6C19B93C011294BF44F94B7EAE75ABDB8C77800` |
| `SecuPilot_P1_L2_Case_Detail_Page_Model_Contract_v0.2 (1).md` | P1/L2 Case Detail page model contract | `DFAD417E1011444A98C6FA384ED4D18AA2475BF14C6C5C89A6DB94FD7389D4EF` |
| `SecuPilot_P2_Approval_Surface_Model_Contract_v0.1 (1).md` | P2 Approval Surface page model contract | `24A4254F9057A9C59090251D9655D00AFBB2C2D1A43B5CCFC92C602DA62DC365` |
| `SecuPilot_P3_Manager_View_Model_Contract_v0.1.md` | P3 Manager View page model contract | `0415534035600365535C6100976E2E280EA7268F8B3FB357EC9D65C4BAE2428C` |
| `SecuPilot_High_Fidelity_UI_and_Visual_Interaction_Spec_v0.1 (1).md` | Visual and interaction constraints | `9156CE7FF4F8C16FAA3000717127F2DB00EFEB158824539F75877371933EBA2C` |

### 4.2 Visual / Interaction Prototype References

Use these as visual and interaction references only:

| Source | Role | SHA256 |
| --- | --- | --- |
| `SecuPilot_P1_L2_Case_Detail_Prototype_v2.1_Formal.md` | P1/L2 Case Detail formal prototype record | `1E679E2335F26B4ABC1B8089ABB5892305607750F0F6C05F8AB10CC409D5E73D` |
| `secupilot_v2_1_final.html` | P1/L2 visual and interaction prototype | `F4B7F085BD33E08A2FE47026BC25F5E1B9F44095A4068A1428ABDA080F5CC84C` |
| `SecuPilot_P2_Approval_Surface_Prototype_v0.3.md` | P2 Approval Surface prototype display patch | `1676A77C7F309E3A9E646BFF5155AA7BC9948E198DB06AFF61D138F942F11FA1` |
| `secupilot_p2_approval_surface_v0.3.html` | P2 visual and interaction prototype | `ACA76791D3EA74814C4CD4B6558324AA62CC369EAA6BEF274A1AE4270668DCB8` |
| `SecuPilot_P3_Manager_View_Prototype_v0.2.md` | P3 Manager View prototype record | `41DA5ACBA6B616668A8A8CF4157F617F3DCA928E7995168CDDA75BBD809F43B0` |
| `secupilot_p3_manager_view_v0.2.html` | P3 visual and interaction prototype | `226A12BAFDBB473E09A88015C2B01329EF4BBCD4FDA75281A74AF0F6FC903D26` |

### 4.3 Tooling / Planning Packs

| Source | Role | Intake handling |
| --- | --- | --- |
| `SecuPilot_Core_Surface_Prototype_Update_Pack_v0.1.zip` | Bundled P2/P3 prototype update pack | Duplicate packaging of files already present in the directory |
| `SecuPilot_Jira_Linear_CSV_Import_Pack_v0.2 (1).zip` | Jira/Linear import seed pack | Planning/tracker support only; not product semantic authority |

The Jira/Linear zip contains:

- `SecuPilot_Jira_Import_Backlog_v0.1.csv`: 63 logical rows according to notes, with epics and tasks.
- `SecuPilot_Linear_Import_Backlog_v0.1.csv`: 54 task rows according to notes.
- `SecuPilot_Jira_Linear_CSV_Import_Notes_v0.2.md`: import guidance.

PowerShell line splitting reports more physical lines because CSV descriptions contain embedded newlines.

## 5. Duplicate And Supersession Handling

### 5.1 Exact Duplicates

The following are exact hash duplicates. Use the clean filename where present and ignore the duplicate suffix copy:

| Canonical | Duplicate |
| --- | --- |
| `SecuPilot_P1_L2_Case_Detail_Prototype_v2.1_Formal.md` | `SecuPilot_P1_L2_Case_Detail_Prototype_v2.1_Formal (1).md` |
| `SecuPilot_P2_Approval_Surface_Prototype_v0.3.md` | `SecuPilot_P2_Approval_Surface_Prototype_v0.3 (1).md` |
| `secupilot_p2_approval_surface_v0.3.html` | `secupilot_p2_approval_surface_v0.3 (1).html` |
| `SecuPilot_P3_Manager_View_Model_Contract_v0.1.md` | `SecuPilot_P3_Manager_View_Model_Contract_v0.1 (1).md` |
| `SecuPilot_P3_Manager_View_Prototype_v0.2.md` | `SecuPilot_P3_Manager_View_Prototype_v0.2 (1).md` |
| `secupilot_p3_manager_view_v0.2.html` | `secupilot_p3_manager_view_v0.2 (1).html` |

### 5.2 Superseded Prototype Versions

- P2 `v0.3` supersedes P2 `v0.2` only for the APC-N01 display patch.
- P2 `v0.2` remains useful as context for the full P2 prototype behavior.
- P2 `v0.3` states it does not change substantive semantics and should rely on `P2 Approval Surface Model Contract v0.1`.

## 6. Intake Findings

### 6.1 Product Goals

- Advance from minimal S6 scaffold to contract-driven core workbench surfaces.
- Keep `conversation first`, `case first`, and `Web first` as dominant UX principles.
- Implement P1/L2 Case Detail around a five-part narrative spine: WHAT, WHY, INTENT, HONESTY, DECISION.
- Keep `coverage_level` as a hard ceiling and render degradation honestly.
- Keep P2 as the only approval workflow owner.
- Keep P3 as management read-only, using independent summary components rather than masked P2 technical components.
- Use visual prototypes to inform interaction and layout, not as source code.

### 6.2 Non-Goals

- No launch, deploy, public endpoint, external pilot, real data, or credential work.
- No backend API or schema-breaking implementation from this intake alone.
- No static HTML copy/paste into production frontend.
- No P1 approval decision authority or P3 approval workflow access.
- No expert-mode field expansion beyond the current role/coverage field set.
- No frontend-hardcoded business follow-up chips, unlock text, queue windows, ROI values, or CMDB business tags.

### 6.3 Changed Assumptions Versus Current Repo Baseline

- Current repo baseline has a minimal first-batch workbench slice; this package introduces full contract candidates for P1 Case Detail and P3 Manager View.
- P2 approval surface now has both mature prototypes and the referenced `P2 Approval Surface Model Contract v0.1`.
- HTML prototypes are now explicitly demoted to visual/interaction references.
- Route selection should move from generic waiting posture to package-driven route selection.

### 6.4 Affected Areas

- `frontend/src/App.tsx` and related frontend styling/tests after exact ticket prep.
- Case Detail layout, narrative spine, honesty layer, right contextual evidence panel, Auto/Manual/Pin behavior, P1 AR modal, and Dialogue Dock.
- Manager View layout, independent P3 summary component, approval-audit read-only summary, coverage/ROI summary, attention queue source constraints, and P3 dialogue boundaries.
- Approval Surface route can be planned from the supplied P2 Model Contract, but implementation still requires exact ticket readiness before code changes.
- Jira/Linear planning artifacts may need reconciliation with current cloud issue state before bulk import.

## 7. Candidate Routes

| Route | Lane | Intake decision | Notes |
| --- | --- | --- | --- |
| `OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE` | Green docs-only | READY | Use this as the next governed artifact. |
| `OPEN_P1_L2_CASE_DETAIL_CONTRACT_IMPLEMENTATION_PREP` | Yellow prep after route selection | CANDIDATE | Strong candidate because PRD and P1 Model Contract exist. |
| `OPEN_P2_APPROVAL_SURFACE_CONTRACT_IMPLEMENTATION_PREP` | Yellow prep after route selection | CANDIDATE | Strong candidate because P2 Model Contract now exists. |
| `OPEN_P3_MANAGER_VIEW_CONTRACT_IMPLEMENTATION_PREP` | Yellow prep after route selection | CANDIDATE | Strong candidate because P3 Model Contract exists. |
| `OPEN_JIRA_LINEAR_IMPORT_RECONCILIATION` | Green docs-only / tooling | OPTIONAL | Use only if tracker sync is needed before implementation. |

## 8. Review And HOLD Conditions

Claude Web state:

```text
UNKNOWN_AVAILABILITY
```

Review requirement:

- Claude Web or equivalent product/architecture/governance review is required before claiming route-selection review PASS for a broad P1/P2/P3 core-surface batch.
- Claude Code review is not required during intake because no implementation diff exists.
- SWE agent use is not authorized during intake.

HOLD if:

- route selection tries to implement directly from static HTML;
- implementation requires backend/API/schema changes not named in an exact ticket;
- follow-up chips, unlock messages, attention queue numbers, CMDB tags, or ROI values are hardcoded in frontend runtime;
- P1/P3 gain approval workflow authority;
- P3 reuses P2 technical component DOM with masking/hiding instead of independent summary components;
- real data, credentials, launch, deployment, public endpoint, external pilot, parked streams, or AI_COLLAB changes appear.

## 9. Ticket Readiness Precheck

Current outcome:

```text
NEEDS_GREEN_DOCS_ONLY_TICKET_PREP
```

Reason:

- Product source is now available.
- Route selection can proceed.
- Exact implementation tickets still need exact allowed files, exact behavior, exact tests, review path, rollback, and HOLD conditions.
- P1, P2, and P3 all still need per-ticket allowed files, exact tests, review path, rollback, and HOLD conditions before implementation.

## 10. Decision

Intake decision:

```text
READY_FOR_ROUTE_SELECTION_DRAFT
```

Next governed artifact:

```text
OPEN_NEXT_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_STAGE
```

Recommended first route-selection focus:

1. P1/L2 Case Detail contract-driven implementation prep.
2. P2 Approval Surface contract-driven implementation prep.
3. P3 Manager View contract-driven implementation prep.

## 11. Update 2026-04-25 14:26 Asia/Shanghai

Human supplied the previously missing P2 Model Contract:

```text
D:\产品设计\secupilot0421\incoming_pending\SecuPilot_P2_Approval_Surface_Model_Contract_v0.1 (1).md
```

Hash:

```text
24A4254F9057A9C59090251D9655D00AFBB2C2D1A43B5CCFC92C602DA62DC365
```

P2 intake update:

- P2 is no longer blocked by missing model contract.
- P2 implementation planning may proceed to route selection and exact ticket prep.
- P2 remains not authorized for direct implementation until exact ticket readiness names exact files, exact behaviors, exact tests, review path, rollback, and HOLD conditions.
- P2 contract-specific implementation constraints include Decision Composer as the only action entry, Strong Confirm for Approve, observation windows returning only to `PENDING_APPROVAL`, no independent Reject CTA, no frontend-hardcoded dialogue chips, no frontend-inferred queue window, no frontend-inferred CMDB tags, and no L2 synthesis of L3 impact chain.
