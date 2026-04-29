# S6 R2 Sprint Planning Candidate Board

## Document Control

- Document: `S6_R2_SPRINT_PLANNING_CANDIDATE_BOARD_2026_04_29`
- Date: 2026-04-29
- R2 item: `R2-05`
- Mode: docs-only planning board
- Implementation authorization: NO

## Decision

```text
SPRINT_PLANNING_CANDIDATE_BOARD_READY_NO_IMPLEMENTATION
```

## Candidate Groups

| Group | Tickets / lanes | Automation posture |
| --- | --- | --- |
| Source-needed | AP-T06, AP-T09, CD-T06 | wait for source input packet response |
| Authority-needed | CH-T04, IN-T03, MV-T02 | wait for authority review / governance decision |
| Dependent HOLD | AP-T11, AP-T12, CD-T07, IN-T06, MV-T05, AP-T02 | do not implement or close until parent resolves |
| Repo Done evidence | E0-01 through E0-04, E0-02B, AP-T08, SH-T08, MV-T04, CH-T02, Batch0 P1 | may be referenced, not relaunched |
| Low-risk docs-only | parity audits, source packs, authority packs, HOLD maps, idle reports | safe for runner while waiting |
| Implementation candidate | none from R1 at this moment | requires later exact GO |

## Planning Notes

- Next implementation should come only after at least one source-needed or authority-needed lane receives governed input.
- If no such input arrives, automation should continue docs-only hygiene and planning rather than invent product scope.
- Jira Done count should not be increased from R1/R2 HOLD rows.

## Non-Authorization

This board does not authorize implementation, Jira mutation, ticket closeout, backend/runtime/API/schema, real data, secrets, deploy, public endpoint, external pilot, or launch.

## Next Route

```text
WAIT_FOR_SOURCE_OR_AUTHORITY_INPUT_OR_CONTINUE_R2_DOCS_ONLY
```
