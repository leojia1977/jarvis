from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "releases" / "release_manifest.json"
REPORT_PATH = ROOT / "releases" / "verify_report.json"
UTC8 = timezone(timedelta(hours=8))


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
    test_results = run_tests(manifest)

    report = {
        "verified_at": now,
        "root": str(ROOT),
        "snapshot_id": manifest.get("snapshot", {}).get("id"),
        "key_files": key_results,
        "release_zip": zip_result,
        "tests": test_results,
    }

    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    key_ok = all(item["ok"] for item in key_results)
    zip_ok = zip_result.get("ok", False)
    tests_ok = all(item["ok"] for item in test_results)
    all_ok = key_ok and zip_ok and tests_ok

    test_status_map = {item["name"]: ("PASS" if item["ok"] else "FAIL") for item in test_results}
    for test in manifest.get("tests", []):
        test["status"] = test_status_map.get(test.get("name"), "UNKNOWN")

    manifest["verification"] = {
        "last_verified_at": now,
        "key_files": "PASS" if key_ok else "FAIL",
        "release_zip": "PASS" if zip_ok else "FAIL",
        "tests": "PASS" if tests_ok else "FAIL",
        "overall_status": "PASS" if all_ok else "FAIL",
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
    }
    save_manifest(manifest)

    print(f"[VERIFY] Root: {ROOT}")
    print(f"[VERIFY] Snapshot: {manifest.get('snapshot', {}).get('id')}")
    print(f"[VERIFY] Key files: {'PASS' if key_ok else 'FAIL'}")
    print(f"[VERIFY] Release zip: {'PASS' if zip_ok else 'FAIL'}")
    print(f"[VERIFY] Tests: {'PASS' if tests_ok else 'FAIL'}")
    print(f"[VERIFY] Report: {REPORT_PATH}")

    if not all_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
