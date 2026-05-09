#!/usr/bin/env python3
"""Build a local/offline ECI/VFE review package from fixture-only artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

CANDIDATE = "ECI_VFE_LOCAL_OFFLINE_RC_001"
SOURCE_CANDIDATE = "ECI_VFE_FIXTURE_RC001"

BOUNDARY_FALSE_KEYS = (
    "real_data",
    "masked_real_data",
    "live_qwen_api",
    "live_connectors",
    "production_writeback",
    "customer_visible_output",
)

REQUIRED_JSON_INPUTS = (
    "output_guard_scan.json",
    "chain_assessment.json",
    "forecast_candidates.json",
    "correlation_result.json",
)

SCREENSHOT_SPECS = (
    ("eci-chain-indicator-desktop.png", "/eci-vfe-chain", "1440x1100"),
    ("eci-chain-indicator-mobile.png", "/eci-vfe-chain", "390x1000"),
    ("vfe-forecast-card-desktop.png", "/eci-vfe-forecast", "1440x1100"),
    ("vfe-forecast-card-mobile.png", "/eci-vfe-forecast", "390x1000"),
)


def utc_now() -> str:
  return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def file_sha256(path: Path) -> str:
  digest = hashlib.sha256()
  with path.open("rb") as handle:
    for chunk in iter(lambda: handle.read(65536), b""):
      digest.update(chunk)
  return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
  with path.open("r", encoding="utf-8") as handle:
    return json.load(handle)


def assert_inside_repo(path: Path, repo_root: Path) -> None:
  try:
    path.resolve().relative_to(repo_root.resolve())
  except ValueError as exc:
    raise ValueError(f"path is outside repo: {path}") from exc


def ensure_clean_output(output_dir: Path, zip_output: Path, repo_root: Path) -> None:
  assert_inside_repo(output_dir, repo_root)
  assert_inside_repo(zip_output, repo_root)
  if output_dir.exists():
    shutil.rmtree(output_dir)
  output_dir.mkdir(parents=True, exist_ok=True)
  if zip_output.exists():
    zip_output.unlink()


def validate_guard_payload(guard_payload: dict[str, Any]) -> None:
  if guard_payload.get("status") != "PASS":
    raise ValueError("output_guard_scan status must be PASS")
  if guard_payload.get("blocking_finding_count", 0) != 0:
    raise ValueError("output_guard_scan blocking_finding_count must be 0")
  boundaries = guard_payload.get("boundaries", {})
  for key in BOUNDARY_FALSE_KEYS:
    if boundaries.get(key) is not False:
      raise ValueError(f"output_guard_scan boundary must be false: {key}")


def load_screenshot_entries(run_dir: Path) -> list[dict[str, Any]]:
  entries: list[dict[str, Any]] = []
  screenshot_root = run_dir / "screenshots"
  for file_name, route, viewport in SCREENSHOT_SPECS:
    screenshot_path = screenshot_root / file_name
    if not screenshot_path.exists():
      raise FileNotFoundError(f"missing screenshot: {screenshot_path}")
    if screenshot_path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
      raise ValueError(f"invalid PNG header: {file_name}")
    entries.append(
      {
        "file_name": file_name,
        "source_path": screenshot_path.as_posix(),
        "route": route,
        "viewport": viewport,
        "bytes": screenshot_path.stat().st_size,
        "sha256": file_sha256(screenshot_path),
        "safety_class": "ECI_VFE_REVIEWER_SAFE_SCREENSHOT",
      }
    )
  return entries


def reviewer_start_here_text(package_dir: str, zip_name: str) -> str:
  return f"""# ECI/VFE 本地离线评审包（RC001）

## 评审边界

```text
Candidate: {CANDIDATE}
Source candidate: {SOURCE_CANDIDATE}
Package: {package_dir}
Zip: {zip_name}
real_data=false
masked_real_data=false
live_qwen_api=false
live_connectors=false
production_writeback=false
customer_visible_output=false
push=false
```

## 评审入口

1. 先看 `SCREENSHOT_INDEX_中文.json` 的 4 张截图条目，确认 route/viewport/sha256。
2. 再看 `output_guard_scan.json`，确认 `status=PASS` 且 `blocking_finding_count=0`。
3. 再看 `chain_assessment.json` / `forecast_candidates.json` / `correlation_result.json`。
4. 最后对照 `package_manifest.json` 的文件哈希与安全类别。

## HOLD 条件

- 任何 boundary 字段不是 false
- output guard 不是 PASS
- 出现 raw payload/token/auth header/attacker-readable attack path
- manifest 缺失 sha256 / bytes / safety_class
"""


def package_files_manifest(output_dir: Path) -> list[dict[str, Any]]:
  entries: list[dict[str, Any]] = []
  for path in sorted(output_dir.glob("*")):
    if not path.is_file():
      continue
    if path.name.endswith(".zip"):
      continue
    entries.append(
      {
        "file_name": path.name,
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": file_sha256(path),
        "safety_class": "ECI_VFE_LOCAL_OFFLINE_REVIEW_ARTIFACT",
      }
    )
  return entries


def build_package(args: argparse.Namespace) -> dict[str, Any]:
  repo_root = Path(args.repo_root).resolve()
  run_dir = (repo_root / args.run_dir).resolve()
  output_dir = (repo_root / args.output_dir).resolve()
  zip_output = (repo_root / args.zip_output).resolve()

  ensure_clean_output(output_dir, zip_output, repo_root)

  loaded_payloads: dict[str, dict[str, Any]] = {}
  for name in REQUIRED_JSON_INPUTS:
    src = run_dir / name
    if not src.exists():
      raise FileNotFoundError(f"missing input: {src}")
    payload = read_json(src)
    if not isinstance(payload, dict):
      raise ValueError(f"input must be JSON object: {name}")
    loaded_payloads[name] = payload
    write_json(output_dir / name, payload)

  validate_guard_payload(loaded_payloads["output_guard_scan.json"])
  screenshot_entries = load_screenshot_entries(run_dir)

  screenshot_index = {
    "schema_version": "secupilot.eci_vfe.local_offline_screenshot_index_zh.v1",
    "generated_at_utc": utc_now(),
    "candidate": CANDIDATE,
    "source_candidate": SOURCE_CANDIDATE,
    "screenshots": screenshot_entries,
    "boundaries": {
      key: False for key in ("real_data", "masked_real_data", "live_qwen_api", "live_connectors", "production_writeback", "customer_visible_output", "push")
    },
  }
  write_json(output_dir / "SCREENSHOT_INDEX_中文.json", screenshot_index)

  package_dir_ref = output_dir.as_posix()
  reviewer_start_here = reviewer_start_here_text(package_dir_ref, zip_output.name)
  (output_dir / "REVIEWER_START_HERE_中文.md").write_text(reviewer_start_here, encoding="utf-8")

  manifest_payload = {
    "schema_version": "secupilot.eci_vfe.local_offline_review_manifest.v1",
    "generated_at_utc": utc_now(),
    "candidate": CANDIDATE,
    "source_candidate": SOURCE_CANDIDATE,
    "package_dir": package_dir_ref,
    "zip_name": zip_output.name,
    "boundaries": {
      key: False for key in ("real_data", "masked_real_data", "live_qwen_api", "live_connectors", "production_writeback", "customer_visible_output", "push")
    },
    "package_files": [],
  }

  write_json(output_dir / "package_manifest.json", manifest_payload)
  manifest_payload["package_files"] = package_files_manifest(output_dir)
  write_json(output_dir / "package_manifest.json", manifest_payload)

  with zipfile.ZipFile(zip_output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(output_dir.glob("*")):
      if path.is_file():
        archive.write(path, path.name)
    for screenshot in screenshot_entries:
      source = Path(screenshot["source_path"])
      archive.write(source, f"screenshots/{source.name}")

  return {
    "status": "PASS",
    "candidate": CANDIDATE,
    "source_candidate": SOURCE_CANDIDATE,
    "package_dir": package_dir_ref,
    "zip_output": zip_output.as_posix(),
    "zip_sha256": file_sha256(zip_output),
    "file_count": len(manifest_payload["package_files"]),
  }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--run-dir", required=True)
  parser.add_argument("--output-dir", required=True)
  parser.add_argument("--zip-output", required=True)
  parser.add_argument("--repo-root", default=".")
  return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
  args = parse_args(argv)
  try:
    result = build_package(args)
  except Exception as exc:
    print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
    return HOLD
  print(json.dumps(result, ensure_ascii=False, indent=2))
  return PASS


if __name__ == "__main__":
  sys.exit(run())
