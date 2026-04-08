# S3-B Case And Jarvis Experience PRD

## Objective
Turn the current investigation output into an analyst-ready case artifact that is:
- readable on first load
- operationally actionable
- safe under degraded conditions
- consistent between backend payload and future UI rendering

## User Problem
The backend can already produce T1, T3, T4, T5, and Jarvis data, but the result is still too tool-centric. Analysts need one case experience, not five tool outputs.

## Sprint 3-B Goal
Freeze and implement a case view contract that answers:
1. what happened
2. why it matters
3. what the analyst should do now
4. what evidence supports the conclusion
5. what the system could not verify

## In Scope
- case summary contract
- evidence grouping contract
- Jarvis hunt plan placement and wording
- degraded-state banner and action suppression rules
- approval-ready action block
- backend shaping layer for frontend consumption

## Out Of Scope
- pixel-perfect final UI design system
- raw process tree explorer
- automatic containment

## Proposed Case Sections

### 1. Executive Summary
- verdict status
- investigation status
- risk score
- confidence label
- one-sentence analyst brief

### 2. What Happened
- scenario name if known
- suspected attack stages
- affected hosts
- most important suspicious chain

### 3. Why It Matters
- IOC matches
- persistence findings
- blast impact summary
- business risk summary

### 4. Jarvis Plan
- hypothesis
- next steps
- scope
- stop conditions

### 5. Recommended Action
- suggested action block
- approval requirement
- action disabled reason if degraded

### 6. Evidence
- top chains
- IOC table
- persistence mechanisms
- evidence gaps

### 7. Limits And Gaps
- degraded banner
- missing telemetry
- unavailable tools
- unresolved pivots

## Backend Contract Direction
Add a case-facing view model on top of the current case payload, for example:
- `case_summary`
- `what_happened`
- `why_it_matters`
- `jarvis_plan`
- `recommended_action`
- `evidence_panels`
- `analysis_limits`

This should be derived from canonical tool results, not replace them.

## UX Rules
- first screen must fit an L1 workflow
- use plain language before deep technical detail
- never hide degraded status
- never show action buttons as active if the case is degraded and the action is unsafe

## Acceptance Criteria
- one frozen case-facing contract exists in backend docs and tests
- `hunt_plan` is visible and understandable as part of the case
- degraded cases suppress unsafe action guidance
- T1/T3/T4/T5 remain available for drilldown without overwhelming the first screen

## Risks
- schema drift between backend and future frontend
- duplicating information across summary and evidence panels
- Jarvis prose becoming detached from evidence

## Recommended Implementation Slice
1. freeze case-facing contract
2. add backend shaping function
3. add tests for summary and degraded behavior
4. then build or mock the frontend consumer
