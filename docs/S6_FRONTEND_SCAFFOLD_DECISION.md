# S6 Frontend Scaffold Decision

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Frontend Scaffold Decision |
| Status | Approved scaffold baseline for bounded implementation |
| Date | 2026-04-24 |
| Repo root | `D:\产品设计\New folder` |
| Decision | `vite-react-typescript` |
| Execution surface adjustment | First-batch `swe` tickets temporarily move to `codex` |

This record imports the human decision to use a Vite React TypeScript frontend scaffold for the first bounded Web workbench implementation slice.

It does not authorize launch, deploy, public endpoint work, real data, credentials, external pilot, parked-stream reopen, schema/API breaking change, broad platforming, or implementation outside first-batch ticket scope.

## 2. Decision

The approved frontend scaffold is:

```text
vite-react-typescript
```

Rationale:

- the frozen PRD defines SecuPilot Web as the primary workbench surface;
- the first batch is route/navigation/UI-shell heavy;
- React TypeScript fits componentized route/nav/case-detail work without inventing backend scope;
- Vite keeps the scaffold small and directly testable.

Rejected for this stage:

- `static-no-dependency`, because it is too weak for routed case workbench evolution;
- any Next.js/server-rendering scaffold, because no route requires server-side rendering yet;
- any broad design-system/platform foundation beyond first-batch needs.

## 3. Execution Surface Change

The first-batch tracker originally planned these tickets as `swe`:

- `GS-T01`
- `GS-T03`
- `CD-T03`

Local SWE command discovery did not find a usable `mini`, `mini-extra`, `mini-swe-agent`, or `swe` command.

Human decision:

```text
Temporarily change GS-T01 / GS-T03 / CD-T03 execution surface from swe to codex.
SWE can rejoin after toolchain unblock and bounded execution verification.
```

This does not change the reviewer floor. Routine ticket review remains `claude-code` / governed `claude-cmd` where available, with human go/no-go still required for batch closeout or any HOLD/external-review trigger.

## 4. Exact Allowed Files For Scaffold Slice

Allowed files for the scaffold and first-batch slice:

- `.gitignore`
- `docs/S6_FRONTEND_SCAFFOLD_DECISION.md`
- `docs/S6_FIRST_BATCH_TICKET_LAUNCH_CHECKLIST.md`
- `docs/S6_FIRST_BATCH_IMPLEMENTATION_LAUNCH_PREP.md`
- `docs/PROJECT_STRUCTURE.md`
- `frontend/index.html`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.json`
- `frontend/tsconfig.node.json`
- `frontend/vite.config.ts`
- `frontend/src/main.tsx`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/test/setup.ts`
- `frontend/src/App.test.tsx`

No backend files are in scope for this first scaffold slice.

## 5. Test Commands

Required frontend commands:

```powershell
cd frontend
npm install
npm run test
npm run build
```

Required backend guard command:

```powershell
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
```

## 6. HOLD Conditions

HOLD if implementation requires:

- backend API change;
- schema/API breaking change;
- real data or credentials;
- public endpoint work;
- additional routes beyond `/`, `/inbox`, and `/case/:caseId` for this slice;
- approval queue, manager view, search/history, coverage-health, or expert-mode implementation beyond visible placeholders required by nav semantics;
- broad component library or reusable framework work;
- SWE execution before SWE toolchain is reverified;
- dependencies beyond Vite, React, TypeScript, Vitest test tooling, and `lucide-react` icons;
- files outside the exact allowed list.
