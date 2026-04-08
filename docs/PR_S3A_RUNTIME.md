# PR: S3-A Runtime Productization Baseline

## Branch
- Source branch: `codex/s3-a-runtime`
- Target branch: `main`

## Recommended PR Title
`feat: add S3-A runtime productization baseline`

## Change Summary
- adds a local runtime service boundary
- adds health and readiness endpoints
- adds a POST investigation endpoint
- makes mock runtime mode explicit
- makes production mode explicitly not-ready instead of silently pretending support
- adds runtime tests and startup docs
- extends Git and release workflow docs for private remote usage

## Key Files
- `backend/app/main.py`
- `backend/app/runtime_service.py`
- `backend/app/config.py`
- `backend/app/tools/siem_adapter.py`
- `backend/app/agents/graph.py`
- `backend/tests/test_runtime_service.py`
- `run_runtime.py`
- `docs/S3A_RUNTIME_STARTUP.md`

## Validation Performed
- `py -3 scripts/git_preflight.py --mode all`
- service smoke check for:
  - `GET /health`
  - `GET /ready`
- governed release packaging and verification

## Review Focus
1. Runtime boundary correctness
2. Mock versus production mode semantics
3. Whether the current entrypoint and readiness payload are sufficient for Sprint 3
4. Whether any case-output changes should be frozen before S3-B starts

## Known Limits
- production adapters are not implemented yet
- this runtime uses the lightweight built-in HTTP server, not FastAPI
- API shape is intentionally minimal for Sprint 3A

## Suggested Claude Review Prompt
Use the manifest-backed Claude review pack for snapshot `S3-A-2026-04-08-001` and focus on:
- runtime boundary quality
- degraded semantics
- product readiness of the current API surface
