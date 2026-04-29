# S6 R2 R1 Source Input Packet

## Document Control

- Document: `S6_R2_R1_SOURCE_INPUT_PACKET_2026_04_29`
- Date: 2026-04-29
- R2 item: `R2-02`
- Mode: docs-only source packet
- Implementation authorization: NO

## Decision

```text
R1_SOURCE_INPUT_PACKET_READY_NO_SOURCE_DELIVERED
```

## Purpose

This packet converts the three R1 source-blocked lanes into copy-ready source requests for product/design/governance input. It does not declare any source delivered.

## AP-T06 Source Request

Required input:

- governed state-sync authority for entering, staying in, and leaving `OBSERVATION_WINDOW`;
- explicit rule that frontend timer display is presentation-only and cannot migrate state;
- exact test hook semantics, including whether `emitStateSync` is allowed as test-only helper;
- exact allowed files and test command for future implementation.

Current status:

```text
HOLD_PENDING_STATE_SYNC_SOURCE_DELIVERY
```

## AP-T09 Source Request

Required input:

- `VF-15` or equivalent governed audit empty/unavailable source;
- distinction between audit empty and audit unavailable;
- governed copy source and required test anchors;
- forbidden CTA / mutation / fallback behavior;
- exact allowed files and test command for future implementation.

Current status:

```text
HOLD_PENDING_VF15_OR_EQUIVALENT_SOURCE
```

## CD-T06 Source Request

Required input:

- governed renderable CLOSED Case Detail context;
- source fields for closed-state header and readonly dialogue state;
- explicit `dialogue-input-readonly` implementation rule if disabled assertions are required;
- exact allowed files and test command for future implementation.

Current status:

```text
HOLD_PENDING_RENDERABLE_CLOSED_CONTEXT
```

## Non-Authorization

This packet does not authorize implementation, source invention, frontend source changes, fixture/context creation, Storybook, Playwright, backend/runtime/API/schema, Jira Done transition, or launch.

## Next Route

```text
WAIT_FOR_AP_T06_STATE_SYNC_SOURCE_OR_AP_T09_VF15_SOURCE_OR_CD_T06_CLOSED_CONTEXT_SOURCE
```
