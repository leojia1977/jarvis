from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "releases" / "release_manifest.json"
UTC8 = timezone(timedelta(hours=8))

EXCLUDE_DIRS = {"__pycache__", "incoming", "releases", ".git"}
EXCLUDE_SUFFIXES = {".pyc"}
EXCLUDE_NAMES = {".DS_Store"}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def save_manifest(manifest: dict) -> None:
    with MANIFEST_PATH.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def should_include(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDE_DIRS for part in rel.parts[:-1]):
        return False
    if path.name in EXCLUDE_NAMES:
        return False
    if path.suffix in EXCLUDE_SUFFIXES:
        return False
    if path.name.endswith(".zip"):
        return False
    return path.is_file()


def sync_prompt_header(manifest: dict) -> None:
    snapshot_id = manifest.get("snapshot", {}).get("id", "")
    source_path = manifest.get("source_of_truth", {}).get("path", str(ROOT))
    manifest_path = str(MANIFEST_PATH)
    manifest["collaboration"]["required_prompt_header"] = [
        f"Single source of truth: {source_path}",
        f"Snapshot ID: {snapshot_id}",
        f"Manifest: {manifest_path}",
        "Do not use any file outside this root as latest code truth.",
    ]


def iter_release_files() -> list[Path]:
    files = [path for path in ROOT.rglob("*") if should_include(path)]
    return sorted(files, key=lambda item: str(item.relative_to(ROOT)).lower())


def update_key_hashes(manifest: dict) -> None:
    for item in manifest.get("key_files", []):
        rel = item["path"]
        target = ROOT / rel
        item["sha256"] = file_sha256(target) if target.exists() else None


def build_release_zip(manifest: dict) -> Path:
    snapshot_id = manifest["snapshot"]["id"]
    zip_name = f"secupilot-{snapshot_id}.zip"
    zip_path = ROOT / "releases" / zip_name

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in iter_release_files():
            archive.write(path, arcname=str(path.relative_to(ROOT)))
    return zip_path


def main() -> int:
    manifest = load_manifest()
    now = datetime.now(UTC8).isoformat()

    sync_prompt_header(manifest)
    update_key_hashes(manifest)
    zip_path = build_release_zip(manifest)

    manifest["snapshot"]["updated_at"] = now
    manifest["artifacts"]["current_release_zip"] = str(zip_path.relative_to(ROOT))
    manifest["artifacts"]["current_release_sha256"] = file_sha256(zip_path)

    save_manifest(manifest)

    print(f"[OK] Source root: {ROOT}")
    print(f"[OK] Release zip: {zip_path}")
    print(f"[OK] Release sha256: {manifest['artifacts']['current_release_sha256']}")
    print(f"[OK] Manifest updated: {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
