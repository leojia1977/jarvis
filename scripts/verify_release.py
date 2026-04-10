from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

from build_claude_review_pack import PACK_ROOT, expected_review_pack_entries


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "releases" / "release_manifest.json"
REPORT_PATH = ROOT / "releases" / "verify_report.json"
UTC8 = timezone(timedelta(hours=8))

PILOT_GATE_ENTRY = ["py", "-3", "scripts/git_preflight.py", "--mode", "pilot"]
PILOT_REQUIRED_ARTIFACTS = [
    {
        "path": "docs\\S4D2_PILOT_SMOKE_PATH.md",
        "role": "s4d2-pilot-smoke-path",
    },
    {
        "path": "docs\\S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md",
        "role": "s4d3-operator-runbooks-and-failure-triage",
    },
    {
        "path": "docs\\S4D4_PILOT_VALIDATION_GATE.md",
        "role": "s4d4-pilot-validation-gate",
    },
]


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


def verify_key_files(manifest: dict) -> list[dict]:
    results = []
    for item in manifest.get("key_files", []):
        rel = item["path"]
        target = ROOT / rel
        exists = target.exists()
        actual = file_sha256(target) if exists else None
        expected = item.get("sha256")
        ok = exists and (expected in (None, actual))
        results.append(
            {
                "path": rel,
                "exists": exists,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "ok": ok,
            }
        )
    return results


def verify_release_zip(manifest: dict) -> dict:
    rel_zip = manifest.get("artifacts", {}).get("current_release_zip")
    expected_sha = manifest.get("artifacts", {}).get("current_release_sha256")
    if not rel_zip:
        return {"exists": False, "ok": False, "reason": "no_release_zip_recorded"}

    zip_path = ROOT / rel_zip
    if not zip_path.exists():
        return {"exists": False, "ok": False, "reason": "release_zip_missing", "path": rel_zip}

    actual_sha = file_sha256(zip_path)
    names = []
    with zipfile.ZipFile(zip_path, "r") as archive:
        names = archive.namelist()

    ok = expected_sha == actual_sha
    return {
        "exists": True,
        "path": rel_zip,
        "expected_sha256": expected_sha,
        "actual_sha256": actual_sha,
        "file_count": len(names),
        "ok": ok,
    }


def verify_review_pack(manifest: dict) -> dict:
    snapshot_id = manifest.get("snapshot", {}).get("id")
    expected_entries = expected_review_pack_entries(manifest)
    pack_dir = PACK_ROOT / snapshot_id
    zip_path = ROOT / "releases" / f"claude-review-pack-{snapshot_id}.zip"

    folder_exists = pack_dir.exists()
    zip_exists = zip_path.exists()
    folder_files = {
        path.relative_to(pack_dir).as_posix()
        for path in pack_dir.rglob("*")
        if path.is_file()
    } if folder_exists else set()
    zip_files: set[str] = set()
    if zip_exists:
        with zipfile.ZipFile(zip_path, "r") as archive:
            zip_files = set(archive.namelist())

    missing_from_folder = sorted(entry for entry in expected_entries if entry not in folder_files)
    missing_from_zip = sorted(entry for entry in expected_entries if entry not in zip_files)
    ok = folder_exists and zip_exists and not missing_from_folder and not missing_from_zip

    return {
        "snapshot_id": snapshot_id,
        "folder_exists": folder_exists,
        "zip_exists": zip_exists,
        "folder_path": str(pack_dir.relative_to(ROOT)) if folder_exists else str(pack_dir),
        "zip_path": str(zip_path.relative_to(ROOT)) if zip_exists else str(zip_path),
        "expected_count": len(expected_entries),
        "folder_file_count": len(folder_files),
        "zip_file_count": len(zip_files),
        "missing_from_folder": missing_from_folder,
        "missing_from_zip": missing_from_zip,
        "ok": ok,
    }


def verify_pilot_validation(manifest: dict, key_results: list[dict]) -> dict:
    manifest_key_files = {item.get("path"): item for item in manifest.get("key_files", [])}
    key_results_by_path = {item["path"]: item for item in key_results}
    snapshot_id = manifest.get("snapshot", {}).get("id")

    pack_dir = PACK_ROOT / snapshot_id
    review_pack_entries = {
        path.relative_to(pack_dir).as_posix()
        for path in pack_dir.rglob("*")
        if path.is_file()
    } if pack_dir.exists() else set()

    review_pack_zip_entries: set[str] = set()
    review_pack_zip_path = ROOT / "releases" / f"claude-review-pack-{snapshot_id}.zip"
    if review_pack_zip_path.exists():
        with zipfile.ZipFile(review_pack_zip_path, "r") as archive:
            review_pack_zip_entries = set(archive.namelist())

    release_zip_entries: set[str] = set()
    rel_release_zip = manifest.get("artifacts", {}).get("current_release_zip")
    if rel_release_zip:
        release_zip_path = ROOT / rel_release_zip
        if release_zip_path.exists():
            with zipfile.ZipFile(release_zip_path, "r") as archive:
                release_zip_entries = set(archive.namelist())

    artifact_results = []
    for artifact in PILOT_REQUIRED_ARTIFACTS:
        rel_path = artifact["path"]
        normalized = rel_path.replace("\\", "/")
        manifest_item = manifest_key_files.get(rel_path, {})
        key_item = key_results_by_path.get(rel_path, {})
        role_matches = manifest_item.get("role") == artifact["role"]
        item_ok = (
            bool(manifest_item)
            and role_matches
            and key_item.get("ok", False)
            and normalized in review_pack_entries
            and normalized in review_pack_zip_entries
            and normalized in release_zip_entries
        )
        artifact_results.append(
            {
                "path": rel_path,
                "expected_role": artifact["role"],
                "manifest_listed": bool(manifest_item),
                "role_matches": role_matches,
                "key_file_ok": key_item.get("ok", False),
                "in_review_pack_folder": normalized in review_pack_entries,
                "in_review_pack_zip": normalized in review_pack_zip_entries,
                "in_release_zip": normalized in release_zip_entries,
                "ok": item_ok,
            }
        )

    overall_ok = all(item["ok"] for item in artifact_results)
    return {
        "deterministic_gate_entry": PILOT_GATE_ENTRY,
        "required_artifacts": artifact_results,
        "ok": overall_ok,
    }


def run_tests(manifest: dict) -> list[dict]:
    results = []
    for test in manifest.get("tests", []):
        argv = test.get("argv", [])
        if not argv:
            results.append({"name": test.get("name", "unnamed"), "ok": False, "reason": "missing_argv"})
            continue

        proc = subprocess.run(
            argv,
            cwd=ROOT,
            capture_output=True,
            text=True,
            shell=False,
        )
        ok = proc.returncode == 0
        results.append(
            {
                "name": test.get("name", "unnamed"),
                "argv": argv,
                "returncode": proc.returncode,
                "ok": ok,
                "stdout_tail": proc.stdout[-1200:],
                "stderr_tail": proc.stderr[-1200:],
            }
        )
    return results


def main() -> int:
    manifest = load_manifest()
    now = datetime.now(UTC8).isoformat()

    key_results = verify_key_files(manifest)
    zip_result = verify_release_zip(manifest)
    review_pack_result = verify_review_pack(manifest)
    pilot_validation_result = verify_pilot_validation(manifest, key_results)
    test_results = run_tests(manifest)

    report = {
        "verified_at": now,
        "root": str(ROOT),
        "snapshot_id": manifest.get("snapshot", {}).get("id"),
        "key_files": key_results,
        "release_zip": zip_result,
        "review_pack": review_pack_result,
        "pilot_validation": pilot_validation_result,
        "tests": test_results,
    }

    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    key_ok = all(item["ok"] for item in key_results)
    zip_ok = zip_result.get("ok", False)
    review_pack_ok = review_pack_result.get("ok", False)
    pilot_ok = pilot_validation_result.get("ok", False)
    tests_ok = all(item["ok"] for item in test_results)
    all_ok = key_ok and zip_ok and review_pack_ok and pilot_ok and tests_ok

    test_status_map = {item["name"]: ("PASS" if item["ok"] else "FAIL") for item in test_results}
    for test in manifest.get("tests", []):
        test["status"] = test_status_map.get(test.get("name"), "UNKNOWN")

    manifest["verification"] = {
        "last_verified_at": now,
        "key_files": "PASS" if key_ok else "FAIL",
        "release_zip": "PASS" if zip_ok else "FAIL",
        "review_pack": "PASS" if review_pack_ok else "FAIL",
        "pilot_validation": "PASS" if pilot_ok else "FAIL",
        "tests": "PASS" if tests_ok else "FAIL",
        "overall_status": "PASS" if all_ok else "FAIL",
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
    }
    save_manifest(manifest)

    print(f"[VERIFY] Root: {ROOT}")
    print(f"[VERIFY] Snapshot: {manifest.get('snapshot', {}).get('id')}")
    print(f"[VERIFY] Key files: {'PASS' if key_ok else 'FAIL'}")
    print(f"[VERIFY] Release zip: {'PASS' if zip_ok else 'FAIL'}")
    print(f"[VERIFY] Review pack: {'PASS' if review_pack_ok else 'FAIL'}")
    print(f"[VERIFY] Pilot validation: {'PASS' if pilot_ok else 'FAIL'}")
    print(f"[VERIFY] Tests: {'PASS' if tests_ok else 'FAIL'}")
    print(f"[VERIFY] Report: {REPORT_PATH}")

    if not all_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
