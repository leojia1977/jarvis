# SecuPilot Surface Fixture Layer

This directory owns mock-only bounded frontend fixtures for Sprint 0 surface work.

The fixture layer has one authority rule: renderable fixtures must resolve through
`ResolvedSurfaceContext` and pass `ContextValidator`. Browser URL, localStorage,
sessionStorage, Storybook args, and Playwright route params are not authority
sources for role, coverage, surface, case state, AR status, or action mode.

## Fixture Groups

- `phase`: validated phase-state fixtures used by P1/P2/P3 surface stories and tests.
- `boundary_case`: validated missing-signal, readonly, disabled, or inline-warning states.
- `resolver_degradation`: validated contexts where unavailable or lower-coverage signals degrade honestly without triggering SH-08.
- `poison_pill`: intentionally invalid contexts used only to prove fail-closed SH-08 behavior.

## Validation Rule

`validate=true` is the default and is required for production-like, Storybook, and
Playwright fixture usage. `validate=false` is allowed only for poison-pill rejection
tests so tests can feed invalid contexts into `ContextValidator`.

Never set `validate=false` to work around context issues in page rendering.

## Non-Goals

This directory must not contain page implementation, Storybook stories, Playwright
E2E tests, backend/runtime/API/schema code, secrets, real data, anonymized real data,
or deploy/public endpoint behavior.
