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
请全程仅使用简体中文回答。
代码标识、文件路径、字段名可以保留英文，但分析、结论、建议必须使用中文。
请只基于我上传的审查包 review，并将其视为当前完整且唯一的评审真相。
不要参考任何其它 zip、旧目录、截图或历史版本。
不要要求我再次同步本地目录；如果你发现缺文件，请直接列出缺失文件并继续完成当前审查。
```

Do not upload:
- stale zip files from other folders
- duplicate copies of the same file from different roots
- screenshots alone without the matching manifest
- files that are not generated from the current manifest-backed review pack
