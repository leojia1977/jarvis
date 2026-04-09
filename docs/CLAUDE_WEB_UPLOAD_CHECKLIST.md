# Claude Web Upload Checklist

## Preferred Workflow
1. Run `py -3 scripts/build_claude_review_pack.py`
2. Upload `releases/claude-review-pack-<snapshot>.zip`
3. Paste the generated header from `releases/claude_review_pack/<snapshot>/CLAUDE_PROMPT.txt`

The generated review-pack zip is authoritative. Prefer it over manual file picking.

## If Manual Upload Is Unavoidable
Upload these together:
1. `docs/HANDOFF.md`
2. `contracts/AI_COLLAB_CONTRACT.md`
3. `releases/release_manifest.json`
4. the exact `.py` files under review
5. the exact `.json` fixtures or datasets under review
6. any stage contract doc added in the current snapshot

## Prompt Header Rule
Do not hand-write or reuse an old snapshot header.

Always copy the header from:
- `releases/claude_review_pack/<snapshot>/CLAUDE_PROMPT.txt`

The generated header is the only authoritative prompt header for the current snapshot.

## Minimum Review Discipline
- review only the current manifest-backed pack
- do not mix files from other folders
- do not use screenshots as a substitute for governed files
- do not ask Claude to become the code source of truth
- if the pack is incomplete, rebuild it before review instead of patching the upload ad hoc

## Never Upload
- stale zip files from other folders
- duplicate copies of the same file from different roots
- screenshots alone without the matching manifest
- files not generated from the current manifest-backed review pack
