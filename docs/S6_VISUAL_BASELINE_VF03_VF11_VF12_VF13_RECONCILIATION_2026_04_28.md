# S6 Visual Baseline VF-03 / VF-11 / VF-12 / VF-13 Reconciliation 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Status | `VISUAL_BASELINE_READY_FOR_STORYBOOK_PLAYWRIGHT_SPRINT_IMPLEMENTATION` |
| Date | 2026-04-28 |
| Scope | Docs-only visual baseline reconciliation |
| Source Folder | `D:\产品设计\secupilot0421\visual negative` |

## 2. Reviewed Inputs

Reviewed visual-negative inputs:

- `SecuPilot_VF-03_Expert_Mode_Entry_Frame_v0.2.md`
- `SecuPilot_VF-11_VF-12_Terminal_and_Observation_Frames_v0.2.md`
- `SecuPilot_VF-13_CLOSED_State_Frame_v0.2.md`

Decision:

```text
VF_03_PASS
VF_11_VF_12_V0_2_PASS
VF_13_CLOSED_STATE_FRAME_V0_2_PASS
```

The inputs are accepted as implementation references. They do not authorize launch,
deploy, real-data handling, backend/runtime/API/schema work, public endpoint activation,
or external pilot execution.

## 3. Current Route Correction

Older Sprint 0 sequencing notes that say to reopen E0-02B, E0-03, E0-04, or Sprint 0 Exit
Review are stale for the current repo state.

Current repo state is already beyond that sequence:

- `E0-01` closed and pushed;
- `E0-02` closed and pushed;
- `E0-02B` closed and pushed;
- `E0-03` / `E0-03B` closed and pushed;
- `E0-04` / `E0-04B` / `E0-04C` closed and pushed;
- Sprint 1-4 bounded implementation is already active.

Therefore the accepted visual inputs are applied forward into Sprint implementation,
regression selectors, and follow-up checklists instead of reopening Sprint 0.

## 4. Unlock Mapping

Accepted unlock mapping:

| Frame | Unlocks |
| --- | --- |
| `VF-03` | `GS-T04`, `CD-T01`, `CD-T02`, `CD-T04`, Storybook expert-mode selector baseline |
| `VF-12` | `AP-T07`, `CD-T06`, `LC-N02` |
| `VF-11` | `AP-T06`, `CD-T06`, `LC-P07`, `LC-B07`, `LC-B08`, `LC-N03`, `LC-N04` |
| `VF-13` | `CD-T06`, AP closed-state readonly behavior, SH history CLOSED case rendering, P1/P2 CLOSED full audit trail readonly, P3 CLOSED audit summary guardrail, Playwright CLOSED-state assertions |

## 5. Implementation Notes Carried Forward

### F-N01

```text
view-details-button is a secondary action for navigating case context.
It must be disabled during active OBSERVATION_WINDOW to prevent scope confusion.
```

Selector expectation:

```ts
await expect(page.getByTestId("view-details-button")).toBeDisabled();
```

### F13-N01

```text
dialogue-input-readonly must be implemented as input[disabled] or textarea[disabled]
if Playwright uses toBeDisabled().
Do not implement it as a div if disabled-state assertion is required.
```

Selector expectation:

```ts
await expect(page.getByTestId("dialogue-input-readonly")).toBeDisabled();
```

### D01C-N01

```text
missing-signal-notice must carry data-message-source="ui_messages".
```

Selector expectation:

```ts
await expect(page.getByTestId("missing-signal-notice"))
  .toHaveAttribute("data-message-source", "ui_messages");
```

## 6. Non-Authorization Boundary

This reconciliation does not authorize:

- final visual PASS for implementation screenshots;
- real-data or anonymized-real-data usage;
- secrets;
- backend/runtime/API/schema changes;
- launch or deploy;
- public endpoint activation;
- external pilot execution;
- coverage-level bypass;
- expert-mode access to OFF fields.

`coverage_level` remains a hard ceiling. Frontend implementation may only show,
collapse, weaken, or hide existing information; it must not create new information.
