from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "releases" / "release_manifest.json"
PACK_ROOT = ROOT / "releases" / "claude_review_pack"


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def build_prompt_text(manifest: dict) -> str:
    header_lines = manifest.get("collaboration", {}).get("required_prompt_header", [])
    lines = header_lines + [
        "",
        "Please review only the uploaded files.",
        "Do not use any other folder, zip, or screenshot as latest code truth.",
        "Treat Claude as review-and-decision only; Codex remains implementation-and-release owner.",
    ]
    return "\n".join(lines) + "\n"


def pack_file(src_root: Path, dst_root: Path, rel_path: str) -> None:
    source = src_root / rel_path
    target = dst_root / rel_path
    ensure_parent(target)
    shutil.copy2(source, target)


def iter_review_files() -> list[str]:
    return [
        "docs/HANDOFF.md",
        "docs/PROJECT_STRUCTURE.md",
        "docs/GIT_WORKFLOW.md",
        "docs/GITHUB_PRIVATE_REMOTE_SETUP.md",
        "docs/PR_S3A_RUNTIME.md",
        "docs/MERGE_STRATEGY.md",
        "docs/CLAUDE_WEB_UPLOAD_CHECKLIST.md",
        "docs/CLAUDE_WEB_ALIGNMENT_GUIDE.md",
        "docs/SPRINT3_PRD.md",
        "docs/SPRINT3_JIRA_BACKLOG.md",
        "docs/S3A_RUNTIME_STARTUP.md",
        "docs/S3B_CASE_EXPERIENCE_PRD.md",
        "docs/S3B_JIRA_BACKLOG.md",
        "contracts/AI_COLLAB_CONTRACT.md",
        "releases/release_manifest.json",
        ".gitignore",
        ".gitattributes",
        ".gitmessage.txt",
        ".github/pull_request_template.md",
        "backend/app/agents/graph.py",
        "backend/app/agents/jarvis_hunt_engine.py",
        "backend/app/main.py",
        "backend/app/runtime_service.py",
        "backend/app/tools/process_tree_t3.py",
        "run_runtime.py",
        "backend/tests/test_t3_hunt.py",
        "backend/tests/test_secupilot_drafts.py",
        "backend/tests/test_runtime_service.py",
    ]


def build_zip(source_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, arcname=str(path.relative_to(source_dir)))


def main() -> int:
    manifest = load_manifest()
    snapshot_id = manifest["snapshot"]["id"]
    output_dir = PACK_ROOT / snapshot_id

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for rel_path in iter_review_files():
        pack_file(ROOT, output_dir, rel_path)

    prompt_path = output_dir / "CLAUDE_PROMPT.txt"
    prompt_path.write_text(build_prompt_text(manifest), encoding="utf-8")

    zip_path = ROOT / "releases" / f"claude-review-pack-{snapshot_id}.zip"
    if zip_path.exists():
        zip_path.unlink()
    build_zip(output_dir, zip_path)

    print(f"[OK] Review pack folder: {output_dir}")
    print(f"[OK] Review pack zip: {zip_path}")
    print(f"[OK] Prompt header: {prompt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
