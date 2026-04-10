# S4-B-5 Telemetry Review Pass

## Goal
Record the Sprint 4 B-stream closeout decision after reviewing:
- `S4-B-1` EDR adapter contract freeze
- `S4-B-2` production EDR ingestion path
- `S4-B-3` EDR replay transport and fixtures
- `S4-B-4` T3 production parity tests

## Review Outcome
`SP4-B-5` closes the governed telemetry review with no open `P1` or `P2` blockers.

This follow-up resolves the remaining review gaps by:
- removing machine-local absolute paths from `backend/tests/test_edr_adapter_contract.py`
- removing machine-local absolute paths from `backend/tests/test_edr_replay.py`
- clarifying the `extra{}` boundary in `docs/S4B1_EDR_ADAPTER_CONTRACT.md`
- excluding common ECS-style vendor containers from `CanonicalProcessEvent.extra`

## Closeout Decision
`S4-B` is accepted as closed for Sprint 4.

Accepted baseline guarantees:
- T3 process-event ingestion is fully adapter-driven
- production-shaped EDR replay fixtures prove canonical normalization
- `partial / degraded` semantics remain explicit through orchestrator and case assembly
- vendor-shaped fields do not leak into T3 output or case contracts
- host identity resolution remains aligned with `S4-A-3`

## Deferred Notes
The `_determine_t3_hosts()` empty-cache branch remains an intentional runtime design choice for now.
It does not block `S4-C`, but should be revisited if later persistence or queue fan-out work increases host selection breadth.

## Acceptance
`S4-B-5` is complete when:
- the governed test suite passes
- the review pack passes verification
- no open `P1` or `P2` review findings remain for `S4-B`
- the snapshot is accepted as the handoff baseline for `S4-C`
