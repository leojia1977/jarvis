# Project Structure

## Canonical Layout
- `backend/app/agents/`: canonical agent implementations
- `backend/app/tools/`: canonical tool implementations
- `backend/tests/`: structured test entrypoints
- `scripts/`: canonical data/build utilities
- `mock_data/`: canonical generated datasets
- `.githooks/`: repository hook entrypoints
- `.gitignore`, `.gitattributes`, `.gitmessage.txt`: Git workflow controls

## Compatibility Layer
- Root-level `.py` files remain as thin wrappers.
- Their only purpose is to preserve the current runnable snapshot and commands.
- New feature work should target canonical files in `backend/` and `scripts/`.

## Current Rule
- Canonical code lives under `backend/` and `scripts/`.
- Root files are compatibility shims only.
- Git workflow and release governance are part of the controlled project structure.
