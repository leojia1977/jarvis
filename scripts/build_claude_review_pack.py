from __future__ import annotations

import json
import os
import stat
import shutil
import time
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
        "请全程仅使用简体中文回答。",
        "代码标识、文件路径、字段名可以保留英文，但分析、结论、建议必须使用中文。",
        "请只基于已上传的审查包进行 review，并将其视为当前完整且唯一的评审真相。",
        "不要参考任何其它 zip、旧目录、截图或你之前环境中的缓存文件。",
        "不要要求我再次同步本地目录；如果你发现缺文件，请直接列出缺失文件并继续完成当前审查。",
        "Claude 只负责 review-and-decision；Codex 仍然是 implementation-and-release owner。",
    ]
    return "\n".join(lines) + "\n"


def pack_file(src_root: Path, dst_root: Path, rel_path: str) -> None:
    source = src_root / rel_path
    target = dst_root / rel_path
    ensure_parent(target)
    shutil.copyfile(source, target)


def iter_review_files(manifest: dict) -> list[str]:
    files: list[str] = [
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
        "docs/SP3_B1_Case_View_Contract.md",
        "docs/SP3_B4_Degraded_UX_Contract.md",
        "docs/S3B_JIRA_BACKLOG.md",
        "docs/S3C0_ADAPTER_CONTRACT.md",
        "docs/S3C1_SIEM_ADAPTER_BOUNDARY.md",
        "docs/S3C2_VENDOR_PROFILE_HARDENING.md",
        "docs/S3C3_VENDOR_REPLAY_SPEC.md",
        "docs/S3D_ENGINEERING_HARDENING_PRD.md",
        "docs/S3D2_WRAPPER_RETIREMENT_PLAN.md",
        "docs/S3D3_RUNTIME_OPERABILITY_CONTRACT.md",
        "docs/S3D4_SNAPSHOT_TRANSITION_CHECKLIST.md",
        "docs/S3D13_GOVERNANCE_REVIEW_PASS.md",
        "docs/S3D_JIRA_BACKLOG.md",
        "docs/SPRINT4_PRD.md",
        "docs/SPRINT4_JIRA_BACKLOG.md",
        "docs/S4A1_STATIC_DATA_SOURCE_CONTRACT.md",
        "contracts/AI_COLLAB_CONTRACT.md",
        "releases/release_manifest.json",
        ".gitignore",
        ".gitattributes",
        ".gitmessage.txt",
        ".github/pull_request_template.md",
        "backend/app/config.py",
        "backend/app/agents/case_view.py",
        "backend/app/agents/graph.py",
        "backend/app/agents/jarvis_hunt_engine.py",
        "backend/app/main.py",
        "backend/app/runtime_service.py",
        "backend/app/tools/process_tree_t3.py",
        "backend/app/tools/siem_adapter.py",
        "run_runtime.py",
        "backend/tests/test_t3_hunt.py",
        "backend/tests/test_case_view.py",
        "backend/tests/test_secupilot_drafts.py",
        "backend/tests/test_runtime_service.py",
        "backend/tests/test_static_data_contracts.py",
    ]

    # Always include manifest-declared key files so new stage artifacts are not
    # accidentally omitted from the review pack when the static list lags behind.
    for item in manifest.get("key_files", []):
        rel_path = item.get("path")
        if not rel_path:
            continue
        normalized = rel_path.replace("\\", "/")
        if (ROOT / normalized).is_file() and normalized not in files:
            files.append(normalized)

    fixtures_root = ROOT / "backend" / "tests" / "fixtures"
    if fixtures_root.exists():
        for fixture in sorted(fixtures_root.rglob("*.json")):
            rel_path = fixture.relative_to(ROOT).as_posix()
            if rel_path not in files:
                files.append(rel_path)

    return sorted(set(files))


def validate_review_files(files: list[str]) -> list[str]:
    missing: list[str] = []
    for rel_path in files:
        if not (ROOT / rel_path).is_file():
            missing.append(rel_path)
    return missing


def expected_review_pack_entries(manifest: dict) -> list[str]:
    return iter_review_files(manifest) + ["CLAUDE_PROMPT.txt"]


def build_zip(source_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, arcname=str(path.relative_to(source_dir)))


def retry_permission_error(operation, *, attempts: int = 10, delay_seconds: float = 0.2):
    last_exc = None
    for _ in range(attempts):
        try:
            return operation()
        except PermissionError as exc:
            last_exc = exc
            time.sleep(delay_seconds)
    if last_exc:
        raise last_exc


def _handle_rmtree_error(func, path, exc_info) -> None:
    target = Path(path)
    try:
        if target.exists():
            os.chmod(target, stat.S_IWRITE | stat.S_IREAD)
        if target.parent.exists():
            os.chmod(target.parent, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
    except OSError:
        pass

    if target.is_file():
        target.unlink(missing_ok=True)
        return

    func(path)


def rotate_existing_output_dir(output_dir: Path) -> bool:
    if not output_dir.exists():
        return True

    stale_dir = output_dir.with_name(f"{output_dir.name}__stale__{int(time.time())}")
    try:
        retry_permission_error(lambda: output_dir.rename(stale_dir))
        shutil.rmtree(stale_dir, onerror=_handle_rmtree_error)
        return True
    except OSError as exc:
        print(f"[WARN] Could not rotate existing review pack folder: {exc}")
        return False


def main() -> int:
    manifest = load_manifest()
    snapshot_id = manifest["snapshot"]["id"]
    output_dir = PACK_ROOT / snapshot_id
    review_files = iter_review_files(manifest)
    missing = validate_review_files(review_files)

    if missing:
        print("[FAIL] Review pack source files missing:")
        for rel_path in missing:
            print(f" - {rel_path}")
        return 1

    if output_dir.exists():
        rotate_existing_output_dir(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for rel_path in review_files:
        pack_file(ROOT, output_dir, rel_path)

    prompt_path = output_dir / "CLAUDE_PROMPT.txt"
    prompt_path.write_text(build_prompt_text(manifest), encoding="utf-8")

    zip_path = ROOT / "releases" / f"claude-review-pack-{snapshot_id}.zip"
    if zip_path.exists():
        try:
            retry_permission_error(lambda: zip_path.unlink())
        except PermissionError as exc:
            print(f"[FAIL] Could not replace existing review pack zip: {exc}")
            print("[FAIL] Review pack folder and zip would diverge. Resolve the file lock and rerun.")
            return 1
    build_zip(output_dir, zip_path)

    print(f"[OK] Review pack folder: {output_dir}")
    print(f"[OK] Review pack zip: {zip_path}")
    print(f"[OK] Prompt header: {prompt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
