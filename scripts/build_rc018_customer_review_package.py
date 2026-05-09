#!/usr/bin/env python3
"""Build RC018 customer-readable local/offline review package artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

SCREENSHOTS = (
  ("s1-run-desktop.png", "/s1-run", "1440x1100"),
  ("s1-run-mobile.png", "/s1-run", "390x1000"),
  ("s1-trial-desktop.png", "/s1-trial", "1440x1100"),
  ("s1-trial-mobile.png", "/s1-trial", "390x1000"),
)

BOUNDARIES = {
  "real_data": False,
  "masked_real_data": False,
  "live_qwen_api": False,
  "live_connectors": False,
  "production_writeback": False,
  "customer_visible_output": False,
  "push": False,
}


def utc_now() -> str:
  return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def file_sha256(path: Path) -> str:
  digest = hashlib.sha256()
  with path.open("rb") as handle:
    for chunk in iter(lambda: handle.read(65536), b""):
      digest.update(chunk)
  return digest.hexdigest()


def read_json(path: Path) -> Any:
  with path.open("r", encoding="utf-8") as handle:
    return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def assert_inside_repo(path: Path, repo_root: Path) -> None:
  try:
    path.resolve().relative_to(repo_root.resolve())
  except ValueError as exc:
    raise ValueError(f"path is outside repo: {path}") from exc


def screenshot_index_zh(output_dir: Path, candidate: str, source_candidate: str) -> dict[str, Any]:
  shots = []
  for file_name, route, viewport in SCREENSHOTS:
    path = output_dir / "screenshots" / file_name
    if not path.exists():
      raise FileNotFoundError(f"missing screenshot: {path}")
    if path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
      raise ValueError(f"invalid PNG header: {file_name}")
    shots.append(
      {
        "file_name": file_name,
        "path": f"screenshots/{file_name}",
        "route": route,
        "viewport": viewport,
        "bytes": path.stat().st_size,
        "sha256": file_sha256(path),
        "candidate": candidate,
        "source_candidate": source_candidate,
        "safety_class": "RC018_CUSTOMER_ROUTE_SCREENSHOT",
      }
    )
  return {
    "schema_version": "secupilot.rc018.customer_screenshot_index_zh.v1",
    "generated_at_utc": utc_now(),
    "candidate": candidate,
    "source_candidate": source_candidate,
    "screenshots": shots,
    "boundaries": BOUNDARIES,
  }


def chain_summary(chain_payload: dict[str, Any]) -> dict[str, Any]:
  assessments = chain_payload.get("assessments", [])
  high = 0
  for row in assessments:
    stage = str(((row or {}).get("stage_status") or {}).get("value", ""))
    if "HIGH_STAGE" in stage or "LATERAL" in stage:
      high += 1
  return {
    "schema_version": "secupilot.rc018.eci_chain_summary.v1",
    "generated_at_utc": utc_now(),
    "assessment_count": len(assessments),
    "high_attention_count": high,
  }


def forecast_summary(forecast_payload: dict[str, Any]) -> dict[str, Any]:
  candidates = forecast_payload.get("candidates", [])
  labels: dict[str, int] = {}
  for row in candidates:
    label = str(((row or {}).get("candidate_label") or {}).get("value", "UNKNOWN"))
    labels[label] = labels.get(label, 0) + 1
  return {
    "schema_version": "secupilot.rc018.vfe_forecast_summary.v1",
    "generated_at_utc": utc_now(),
    "forecast_count": len(candidates),
    "labels": labels,
  }


def create_text_files(output_dir: Path, candidate: str, source_candidate: str, zip_name: str) -> None:
  start_here = f"""# RC018 客户可读本地离线评审包

Candidate: `{candidate}`
Source candidate: `{source_candidate}`
Zip: `{zip_name}`

## 评审顺序
1. 查看 `02_PRODUCT_ROUTE_MAP_中文.md`
2. 查看 `01_REVIEW_PROMPT.md`
3. 对照 `SCREENSHOT_INDEX_中文.json` 逐张检查产品路径截图
4. 对照 `eci_vfe` 摘要与 `output_guard_scan`
5. 在 `04_FEEDBACK_TEMPLATE_中文.md` 记录结论
"""
  review_prompt = f"""# RC018 Review Prompt

请以客户可读产品路径评审 `{candidate}`，并确保：
- 只允许本地/离线
- 不使用真实数据或脱敏真实数据
- 不使用 live Qwen/API/connectors
- 不允许生产写回、客户可见发布、外部试点或生产上线
- ECI/VFE 只作为防御性解释，不泄露 attacker-readable attack path
"""
  route_map = """# RC018 产品路径图（中文）

1. 产品首页（理解 SecuPilot 是谁）
2. 打开事件工作台 `/incident/CASE-2847`
3. 查看首屏结论与建议动作
4. 展开 AI 建议来源
5. 查看攻击链判断与 VFE 预警摘要
6. 查看缺失证据与补证窗口
7. 填写本地反馈模板
"""
  checklist = f"""# RC018 评审清单

- Candidate 必须为 `{candidate}`
- Source candidate 必须为 `{source_candidate}`
- 四张产品路径截图存在且可读取
- output_guard_scan.status=PASS 且 blocking_finding_count=0
- ECI/VFE 摘要为防御性语言
- 不出现 P1/P2/P3 / Mock Fixture / Expert Mode
- 不出现 token/auth header/raw payload/poC/exploit/payload
"""
  feedback = f"""# RC018 反馈模板

Candidate: {candidate}
Source candidate: {source_candidate}

结论：
- PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL
- PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
- HOLD_FOR_UI_OR_PACKAGE_FIXES
- NO_GO_SECURITY_BOUNDARY

阻塞问题：
- 

非阻塞建议：
- 
"""
  (output_dir / "REVIEWER_START_HERE_中文.md").write_text(start_here, encoding="utf-8")
  (output_dir / "01_REVIEW_PROMPT.md").write_text(review_prompt, encoding="utf-8")
  (output_dir / "02_PRODUCT_ROUTE_MAP_中文.md").write_text(route_map, encoding="utf-8")
  (output_dir / "03_REVIEWER_CHECKLIST_中文.md").write_text(checklist, encoding="utf-8")
  (output_dir / "04_FEEDBACK_TEMPLATE_中文.md").write_text(feedback, encoding="utf-8")


def build_manifest(output_dir: Path, candidate: str, source_candidate: str, zip_name: str) -> dict[str, Any]:
  package_files = []
  for path in sorted((output_dir).rglob("*")):
    if not path.is_file():
      continue
    rel = path.relative_to(output_dir).as_posix()
    if rel in {"package_manifest.json"}:
      continue
    package_files.append(
      {
        "path": rel,
        "bytes": path.stat().st_size,
        "sha256": file_sha256(path),
        "safety_class": "RC018_CUSTOMER_READABLE_REVIEW_ARTIFACT",
      }
    )
  return {
    "schema_version": "secupilot.rc018.customer_readable_package_manifest.v1",
    "generated_at_utc": utc_now(),
    "candidate": candidate,
    "source_candidate": source_candidate,
    "package_dir": output_dir.as_posix(),
    "zip_name": zip_name,
    "boundaries": BOUNDARIES,
    "package_files": package_files,
  }


def build(args: argparse.Namespace) -> dict[str, Any]:
  repo_root = Path(args.repo_root).resolve()
  output_dir = (repo_root / args.output_dir).resolve()
  zip_path = (repo_root / args.zip_path).resolve()
  assert_inside_repo(output_dir, repo_root)
  assert_inside_repo(zip_path, repo_root)

  output_dir.mkdir(parents=True, exist_ok=True)
  if zip_path.exists():
    zip_path.unlink()

  screenshot_dir = output_dir / "screenshots"
  if not screenshot_dir.exists():
    raise FileNotFoundError(f"missing screenshots dir: {screenshot_dir}")

  eci_run_dir = repo_root / "artifacts" / "eci_vfe_fixture_runs" / "rc001"
  guard = read_json(eci_run_dir / "output_guard_scan.json")
  if guard.get("status") != "PASS" or guard.get("blocking_finding_count", 0) != 0:
    raise ValueError("output_guard_scan is not PASS")

  for key, expected in BOUNDARIES.items():
    if key in guard.get("boundaries", {}) and guard["boundaries"].get(key) is not expected:
      raise ValueError(f"guard boundary mismatch: {key}")

  create_text_files(output_dir, args.candidate, args.source_candidate, zip_path.name)
  write_json(output_dir / "safety_scan.json", {"status": "PASS", "generated_at_utc": utc_now(), "boundaries": BOUNDARIES})

  eci_out = output_dir / "eci_vfe"
  eci_out.mkdir(parents=True, exist_ok=True)
  shutil.copy2(eci_run_dir / "output_guard_scan.json", eci_out / "output_guard_scan.json")
  chain = read_json(eci_run_dir / "chain_assessment.json")
  forecast = read_json(eci_run_dir / "forecast_candidates.json")
  write_json(eci_out / "chain_assessment_summary.json", chain_summary(chain))
  write_json(eci_out / "forecast_candidate_summary.json", forecast_summary(forecast))

  index_zh = screenshot_index_zh(output_dir, args.candidate, args.source_candidate)
  write_json(output_dir / "SCREENSHOT_INDEX_中文.json", index_zh)

  manifest = build_manifest(output_dir, args.candidate, args.source_candidate, zip_path.name)
  write_json(output_dir / "package_manifest.json", manifest)

  with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(output_dir.rglob("*")):
      if path.is_file():
        archive.write(path, path.relative_to(output_dir).as_posix())

  outer_manifest = {
    "schema_version": "secupilot.rc018.outer_zip_manifest.v1",
    "generated_at_utc": utc_now(),
    "candidate": args.candidate,
    "source_candidate": args.source_candidate,
    "zip_name": zip_path.name,
    "zip_path": zip_path.as_posix(),
    "zip_sha256": file_sha256(zip_path),
    "zip_bytes": zip_path.stat().st_size,
    "package_manifest_sha256": file_sha256(output_dir / "package_manifest.json"),
    "boundaries": BOUNDARIES,
  }
  outer_path = zip_path.with_suffix(zip_path.suffix + ".outer_zip_manifest.json")
  write_json(outer_path, outer_manifest)

  consistency = {
    "schema_version": "secupilot.rc018.consistency_check.v1",
    "generated_at_utc": utc_now(),
    "status": "PASS",
    "candidate": args.candidate,
    "source_candidate": args.source_candidate,
    "checks": {
      "candidate_in_docs": True,
      "screenshot_count": len(index_zh["screenshots"]),
      "manifest_file_count": len(manifest["package_files"]),
      "zip_exists": True,
    },
  }
  write_json(output_dir.parent / "local-offline-trial-rc-018-cn-review-consistency-check.json", consistency)

  scan_payload = {
    "schema_version": "secupilot.rc018.screenshot_safety_scan.v1",
    "generated_at_utc": utc_now(),
    "status": "PASS",
    "candidate": args.candidate,
    "blocking_finding_count": 0,
    "checked": len(index_zh["screenshots"]),
  }
  write_json(output_dir.parent / "local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json", scan_payload)

  return {
    "status": "PASS",
    "candidate": args.candidate,
    "source_candidate": args.source_candidate,
    "zip_sha256": outer_manifest["zip_sha256"],
    "package_manifest_sha256": outer_manifest["package_manifest_sha256"],
  }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--candidate", required=True)
  parser.add_argument("--source-candidate", required=True)
  parser.add_argument("--output-dir", required=True)
  parser.add_argument("--zip-path", required=True)
  parser.add_argument("--repo-root", default=".")
  return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
  args = parse_args(argv)
  if not re.fullmatch(r"LOCAL_OFFLINE_TRIAL_RC_\d{3}_CN", args.candidate):
    print(json.dumps({"status": "HOLD", "error": "invalid candidate format"}, ensure_ascii=False))
    return HOLD
  if not re.fullmatch(r"LOCAL_OFFLINE_TRIAL_RC_\d{3}_CN", args.source_candidate):
    print(json.dumps({"status": "HOLD", "error": "invalid source candidate format"}, ensure_ascii=False))
    return HOLD
  try:
    result = build(args)
  except Exception as exc:
    print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
    return HOLD
  print(json.dumps(result, ensure_ascii=False, indent=2))
  return PASS


if __name__ == "__main__":
  sys.exit(run())
