# AI Collaboration Contract

## Objective
Keep Claude and Codex aligned on one source of truth, one snapshot, and one release flow.

## Single Source Of Truth
- Active root: `D:\产品设计\New folder`
- Active snapshot: read from `releases/release_manifest.json`

## Role Split
### Claude
- product review
- architecture review
- UX review
- risk review
- PRD and decision writing

### Codex
- code changes
- test updates
- mock data updates
- packaging
- verification
- manifest updates

## Non-Negotiable Rules
1. Claude must not assume any zip outside the source root is latest.
2. Codex must not change runnable truth outside the source root.
3. No manual release zip may be treated as official.
4. No code review may be considered current unless the manifest snapshot matches the reviewed files.
5. If duplicate files exist in multiple folders, the source root wins.

## Required Prompt Header
```text
Single source of truth: D:\产品设计\New folder
Snapshot ID: <read from releases/release_manifest.json>
Manifest: D:\产品设计\New folder\releases\release_manifest.json
Do not use any file outside this root as latest code truth.
If you find duplicates, treat files outside this root as stale unless they are explicitly imported into the manifest.
```

## Required Review Output
When Claude reviews code, the preferred format is:
- `P1 / P2 / P3 findings`
- `why`
- `modification advice`
- `does this block acceptance`

## Required Codex Output
When Codex changes code, the preferred close-out format is:
- files changed
- what changed
- tests run
- current acceptance status

## Import Rule
External zips or copied folders are not code truth.
They are only candidate input material until:
1. they are placed under `incoming/`
2. the required files are copied into the source root
3. the manifest is updated
4. verification passes
