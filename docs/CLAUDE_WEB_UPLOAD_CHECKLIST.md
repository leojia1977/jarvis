# Claude Web Upload Checklist

Preferred workflow:

1. Run `py -3 scripts/build_claude_review_pack.py`
2. Open `releases/claude_review_pack/<snapshot>/`
3. Upload the generated files from that folder to Claude Web

If you need to upload manually, include these files together whenever you ask Claude to review the current implementation:

1. `docs/HANDOFF.md`
2. `contracts/AI_COLLAB_CONTRACT.md`
3. `releases/release_manifest.json`
4. The exact `.py` files under review
5. Any relevant `.json` data files under review

Use this header in the prompt:

```text
Single source of truth: D:\产品设计\New folder
Snapshot ID: S3-A-2026-04-08-001
Manifest: D:\产品设计\New folder\releases\release_manifest.json
Do not use any file outside this root as latest code truth.
Any zip outside this root is input-only material unless the manifest says otherwise.
Please review based only on the uploaded files.
```

Do not upload:
- stale zip files from other folders
- duplicate copies of the same file from different roots
- screenshots alone without the matching manifest
- files that are not generated from the current manifest-backed review pack
