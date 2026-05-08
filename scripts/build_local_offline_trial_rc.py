#!/usr/bin/env python3
"""Build a self-contained SecuPilot local/offline trial RC package."""

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

EVIDENCE_FILES = (
    "artifact_manifest.json",
    "case_summary.json",
    "final_status.json",
    "safety_scan.json",
)

LEGACY_P3_CASE_TITLE = "P3 manager summary without host raw evidence"
PACKAGE_FACING_P3_CASE_TITLE = "P3 manager summary (metadata-only evidence scope)"

VALIDATION_RETENTION_CLASS = "S1_LOCAL_OFFLINE_VALIDATION_ARTIFACT"

SCREENSHOT_SPECS = (
    ("s1-run-desktop.png", "/s1-run", "1440x1100"),
    ("s1-run-mobile.png", "/s1-run", "390x1000"),
    ("s1-run-first-load-folded-desktop.png", "/s1-run", "1440x1100"),
    ("s1-trial-desktop.png", "/s1-trial", "1440x1100"),
    ("s1-trial-mobile.png", "/s1-trial", "390x1000"),
)
REQUIRED_ARCHIVE_SCREENSHOT_FILES = ("s1-run-first-load-folded-desktop.png",)

BOUNDARIES = {
    "real_data": False,
    "masked_real_data": False,
    "live_qwen_api": False,
    "live_connectors": False,
    "production_writeback": False,
    "customer_visible_output": False,
    "push": False,
}


def required_archive_evidence_payload(
    *,
    folded_state_primary_sha256: str | None = None,
    folded_state_screenshot_sha256: dict[str, str] | None = None,
) -> dict[str, Any]:
    payload = {
        "folded_state_screenshot_files": [f"screenshots/{name}" for name in REQUIRED_ARCHIVE_SCREENSHOT_FILES],
        "folded_state_screenshot_required": True,
        "folded_state_assertion_code": "AI_ADVICE_SOURCE_FIRST_LOAD_FOLDED",
        "folded_state_expected_state": "FOLDED",
        "folded_state_expected_section": "AI 建议来源",
        "folded_state_capture_phase": "FIRST_LOAD",
        "folded_state_capture_policy": "FIRST_LOAD_NO_INTERACTION",
        "folded_state_expected_interaction_count": 0,
        "folded_state_expected_route": "/s1-run",
        "folded_state_expected_viewport": "1440x1100",
        "folded_state_primary_screenshot": "screenshots/s1-run-first-load-folded-desktop.png",
    }
    if folded_state_primary_sha256:
        payload["folded_state_primary_sha256"] = folded_state_primary_sha256
        payload["folded_state_proof"] = {
            "screenshot_path": "screenshots/s1-run-first-load-folded-desktop.png",
            "route": "/s1-run",
            "viewport": "1440x1100",
            "expected_state": "FOLDED",
            "expected_section": "AI 建议来源",
            "interaction_count": 0,
            "interaction_policy": "FIRST_LOAD_NO_INTERACTION",
            "sha256": folded_state_primary_sha256,
        }
    if folded_state_screenshot_sha256:
        payload["folded_state_screenshot_sha256"] = {
            key: folded_state_screenshot_sha256[key] for key in sorted(folded_state_screenshot_sha256)
        }
    return payload

FORBIDDEN_TEXT_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"authorization\s*[:=]\s*\S+",
        r"bearer\s+[A-Za-z0-9._~+/=-]{12,}",
        r"api[_-]?key\s*[:=]\s*\S+",
        r"secret\s*[:=]\s*\S+",
        r"token\s*[:=]\s*\S+",
        r"private[_-]?key\s*[:=]\s*\S+",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"raw_payload\s*[:=]",
        r"raw_evidence\s*[:=]",
        r"host_raw_evidence\s*[:=]",
        r"customer_visible_message\s*[:=]",
        r"writeback_action\s*[:=]",
        r"production_connector_output\s*[:=]",
    )
)


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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def json_payload_sha256(payload: Any) -> str:
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def manifest_self_sha256(manifest: dict[str, Any]) -> str:
    manifest_for_hash = dict(manifest)
    manifest_for_hash["manifest_self_sha256"] = None
    return json_payload_sha256(manifest_for_hash)


def build_outer_zip_manifest_payload(
    *,
    candidate: str,
    source_candidate: str,
    package_dir: str,
    zip_path: Path,
    package_manifest_path: Path,
    manifest_self_hash: str,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "schema_version": "secupilot.s1.local_offline_outer_zip_manifest.v1",
        "generated_at_utc": utc_now(),
        "candidate": candidate,
        "source_candidate": source_candidate,
        "package_dir": package_dir,
        "zip_name": zip_path.name,
        "zip_path": portable_path(zip_path, repo_root),
        "zip_bytes": zip_path.stat().st_size,
        "zip_sha256": file_sha256(zip_path),
        "package_manifest_path": portable_path(package_manifest_path, repo_root),
        "package_manifest_sha256": file_sha256(package_manifest_path),
        "manifest_self_sha256": manifest_self_hash,
        "boundaries": BOUNDARIES,
    }


def portable_path(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def assert_inside_repo(path: Path, repo_root: Path) -> None:
    try:
        path.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"path is outside repo: {path}") from exc


def ensure_clean_output(output_dir: Path, zip_path: Path, repo_root: Path) -> None:
    assert_inside_repo(output_dir, repo_root)
    assert_inside_repo(zip_path, repo_root)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    if zip_path.exists():
        zip_path.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)


def validate_source_boundaries(source_package: Path) -> None:
    final_status = read_json(source_package / "evidence" / "final_status.json")
    safety_scan = read_json(source_package / "evidence" / "safety_scan.json")

    if final_status.get("can_deploy_to_customer_production") is not False:
        raise ValueError("final_status can_deploy_to_customer_production must be false")

    boundaries = final_status.get("boundaries_preserved", {})
    for key in (
        "customer_visible_output",
        "production_connectors",
        "qwen_autonomous_action",
        "raw_payload_retention",
        "secret_retention",
        "writeback",
    ):
        if boundaries.get(key) is not False:
            raise ValueError(f"final_status boundary must be false: {key}")

    summary = safety_scan.get("summary", {})
    if summary.get("finding_count") != 0:
        raise ValueError("safety_scan finding_count must be 0")
    if summary.get("no_go_count") != 0:
        raise ValueError("safety_scan no_go_count must be 0")


def scan_text_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for pattern in FORBIDDEN_TEXT_PATTERNS:
        if pattern.search(text):
            raise ValueError(f"{path.name}: forbidden text pattern {pattern.pattern}")


def rc_display_label(candidate: str) -> str:
    match = re.search(r"RC_(\d{3})", candidate)
    if not match:
        return candidate
    return f"RC-{match.group(1)}"


def copy_evidence(source_package: Path, output_dir: Path) -> list[dict[str, Any]]:
    evidence_output = output_dir / "evidence"
    evidence_output.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    for name in EVIDENCE_FILES:
        src = source_package / "evidence" / name
        if not src.exists():
            raise FileNotFoundError(f"missing evidence file: {src}")
        dst = evidence_output / name
        if name == "case_summary.json":
            payload = read_json(src)
            payload = sanitize_case_summary_for_package(payload)
            write_json(dst, payload)
        else:
            shutil.copy2(src, dst)
        entries.append(build_manifest_entry(dst, output_dir, "S1_LOCAL_OFFLINE_CHINESE_REVIEW_PACKAGE"))
    return entries


def sanitize_case_summary_for_package(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    cases = payload.get("cases")
    if not isinstance(cases, list):
        return payload
    next_cases: list[Any] = []
    for case in cases:
        if not isinstance(case, dict):
            next_cases.append(case)
            continue
        next_case = dict(case)
        title = next_case.get("title")
        if isinstance(title, str) and title.strip() == LEGACY_P3_CASE_TITLE:
            next_case["title"] = PACKAGE_FACING_P3_CASE_TITLE
        summary = next_case.get("summary")
        if isinstance(summary, str):
            next_case["summary"] = summary.replace(LEGACY_P3_CASE_TITLE, PACKAGE_FACING_P3_CASE_TITLE)
        next_cases.append(next_case)
    next_payload = dict(payload)
    next_payload["cases"] = next_cases
    return next_payload


def copy_screenshots(
    screenshot_dir: Path, output_dir: Path
) -> tuple[list[dict[str, Any]], list[tuple[str, str, str]]]:
    screenshot_output = output_dir / "screenshots"
    screenshot_output.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    included_specs: list[tuple[str, str, str]] = []
    for file_name, route, viewport in SCREENSHOT_SPECS:
        src = screenshot_dir / file_name
        if not src.exists():
            raise FileNotFoundError(f"missing screenshot: {src}")
        dst = screenshot_output / file_name
        shutil.copy2(src, dst)
        entries.append(build_manifest_entry(dst, output_dir, "S1_LOCAL_OFFLINE_CHINESE_REVIEW_PACKAGE"))
        included_specs.append((file_name, route, viewport))
    return entries, included_specs


def copy_validation_artifacts(
    validation_paths: list[Path],
    output_dir: Path,
) -> list[dict[str, Any]]:
    if not validation_paths:
        return []
    validation_output = output_dir / "validation"
    validation_output.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    for src in validation_paths:
        if not src.exists():
            raise FileNotFoundError(f"missing validation artifact: {src}")
        dst = validation_output / src.name
        shutil.copy2(src, dst)
        entries.append(build_manifest_entry(dst, output_dir, VALIDATION_RETENTION_CLASS))
    return entries


def build_manifest_entry(path: Path, package_dir: Path, retention_class: str) -> dict[str, Any]:
    return {
        "file_name": path.name,
        "path": portable_path(path, package_dir),
        "bytes": path.stat().st_size,
        "sha256": file_sha256(path),
        "contains_raw_payload": False,
        "contains_secret_or_token": False,
        "contains_customer_visible_artifact": False,
        "retention_class": retention_class,
    }


def reviewer_start_here(candidate: str, source_candidate: str, package_dir: str, zip_name: str) -> str:
    rc_label = rc_display_label(candidate)
    return f"""# SecuPilot 本地离线中文评审包 {rc_label}

## 本轮目标

{rc_label} 用于验证本地离线试用包、产品化结果页和机器验证证据是否保持一致。

本轮所有 reviewer-facing 口径统一为：

```text
Candidate: {candidate}
Source candidate: {source_candidate}
Package: {package_dir}
Zip: {zip_name}
```

## 评审范围

本包只用于内部本地/离线中文评审。

允许查看：

```text
中文优先的 S1 本地试用页面
中文优先的 S1 试用结果页面
metadata-only case summary
artifact manifest
safety scan summary
本地评审结论预览
离线评审交接材料
```

不允许：

```text
真实数据
脱敏真实数据
live Qwen/API 调用
live connector
生产写回
客户可见发布/部署/输出
外部试点
生产上线
push
```

## 建议评审顺序

1. 查看 `screenshots/s1-trial-desktop.png` 和 `screenshots/s1-trial-mobile.png`。
2. 查看 `screenshots/s1-run-desktop.png` 和 `screenshots/s1-run-mobile.png`，重点判断它是否像产品结果页，而不是证据台。
3. 查看 `screenshots/s1-run-first-load-folded-desktop.png`，确认 AI 建议来源在首屏未交互状态下保持折叠态证据。
4. 核验 `evidence/final_status.json`、`evidence/case_summary.json`、`evidence/artifact_manifest.json`、`evidence/safety_scan.json`。
5. 对照 `REVIEWER_CHECKLIST_中文.md` 判断是否可进入下一轮内部本地试用。
6. 使用 `FEEDBACK_TEMPLATE_中文.md` 输出结论。
"""


def reviewer_checklist(candidate: str, source_candidate: str, package_slug: str) -> str:
    rc_label = rc_display_label(candidate)
    return f"""# {rc_label} 中文本地离线评审检查清单

## 必查项

| 检查项 | 期望 |
| --- | --- |
| `/s1-trial` 截图为中文优先 | PASS |
| `/s1-run` 截图为产品化结果页，不是证据台 | PASS |
| `s1-run-first-load-folded-desktop.png` 存在且可打开 | PASS |
| 截图中 candidate 为 `{candidate}` | PASS |
| 截图中 source candidate 为 `{source_candidate}` | PASS |
| 截图中 package path 指向 `{package_slug}` | PASS |
| 截图中不再出现上一轮旧版本 reviewer package 口径 | PASS |
| 桌面截图不显示 P1/P2/P3 / Mock Fixture / Expert Mode 调试控件 | PASS |
| 手机截图不显示 P1/P2/P3 / Mock Fixture / Expert Mode 调试控件 | PASS |
| 证据 ID / artifact path / decision code 保持可对账 | PASS |
| 本地评审结论预览不写后端或 artifact | PASS |
| `customer_visible_output` | false |
| `production_writeback` | false |
| `live_qwen_api` | false |
| `live_connectors` | false |
| `safety_scan.summary.finding_count` | 0 |
| `validation/screenshot_safety_scan.json` 阻塞项 | 0 |

## HOLD 条件

```text
截图无法打开
页面入口仍主要依赖英文说明才能理解
/s1-run 仍像证据台而不是产品结果页
页面仍显示上一轮旧版本 reviewer package 口径
路径指向不存在的 artifact
反馈入口声称会写后端或提交外部系统
出现真实/脱敏真实数据
出现 secret/token/auth header
出现 live Qwen/API/connector 调用
出现客户可见发布、部署、外部试点或生产上线暗示
```
"""


def feedback_template(candidate: str, source_candidate: str, package_dir: str, zip_name: str) -> str:
    rc_label = rc_display_label(candidate)
    return f"""# {rc_label} 中文本地离线评审反馈模板

## 基本信息

```text
Reviewer:
Review timestamp:
Candidate: {candidate}
Source candidate: {source_candidate}
Route: /s1-trial, /s1-run
Package: {package_dir}
Zip: {zip_name}
```

## 结论

选择一项：

```text
PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL
PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
HOLD_FOR_UI_OR_PACKAGE_FIXES
```

## 反馈

```text
1. 中文页面是否能看懂：
2. /s1-run 是否已经像产品结果页，而不是证据台：
3. 是否仍看到上一轮旧版本口径：
4. 是否仍看到 P1/P2/P3、Mock Fixture、Expert Mode 调试控件：
5. 截图是否足够 reviewer 离线判断：
6. 是否看到越界内容：
7. 是否需要补截图/说明/路径：
8. 下一轮建议：
```

## 边界确认

```text
real_data = false
masked_real_data = false
live_qwen_api = false
live_connectors = false
production_writeback = false
customer_visible_output = false
push = false
```
"""


def package_index(
    candidate: str,
    source_candidate: str,
    package_dir: str,
    zip_name: str,
    screenshot_files: list[str],
    validation_files: list[str],
    required_archive_evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "secupilot.s1.local_offline_chinese_package_index.v1",
        "candidate": candidate,
        "source_candidate": source_candidate,
        "route": ["/s1-trial", "/s1-run"],
        "package_dir": package_dir,
        "zip_name": zip_name,
        "start_here": "REVIEWER_START_HERE_中文.md",
        "checklist": "REVIEWER_CHECKLIST_中文.md",
        "feedback_template": "FEEDBACK_TEMPLATE_中文.md",
        "evidence_files": [f"evidence/{name}" for name in EVIDENCE_FILES],
        "screenshot_files": screenshot_files,
        "required_archive_evidence": required_archive_evidence,
        "validation_files": validation_files,
        "boundaries": BOUNDARIES,
    }


def screenshot_index(
    candidate: str,
    source_candidate: str,
    source_commit: str,
    output_dir: Path,
    screenshot_specs: list[tuple[str, str, str]],
) -> dict[str, Any]:
    screenshots = []
    folded_name = REQUIRED_ARCHIVE_SCREENSHOT_FILES[0]
    for file_name, route, viewport in screenshot_specs:
        path = output_dir / "screenshots" / file_name
        item: dict[str, Any] = {
            "file_name": file_name,
            "path": portable_path(path, output_dir),
            "bytes": path.stat().st_size,
            "sha256": file_sha256(path),
            "route": route,
            "viewport": viewport,
        }
        if file_name == folded_name:
            item["archive_evidence"] = {
                "assertion_code": "AI_ADVICE_SOURCE_FIRST_LOAD_FOLDED",
                "evidence_role": "AI_ADVICE_SOURCE_FOLDED_STATE",
                "capture_phase": "FIRST_LOAD",
                "capture_policy": "FIRST_LOAD_NO_INTERACTION",
                "interaction_count": 0,
                "expected_interaction_count": 0,
                "expected_state": "FOLDED",
                "expected_section": "AI 建议来源",
                "expected_route": "/s1-run",
                "expected_viewport": "1440x1100",
            }
        screenshots.append(item)
    return {
        "schema_version": "secupilot.s1.local_offline_chinese_screenshot_index.v1",
        "candidate": candidate,
        "source_candidate": source_candidate,
        "source_commit": source_commit,
        "generated_at_utc": utc_now(),
        "screenshots": screenshots,
        "boundaries": BOUNDARIES,
    }


def write_reviewer_docs(
    output_dir: Path,
    candidate: str,
    source_candidate: str,
    package_dir: str,
    zip_name: str,
) -> list[dict[str, Any]]:
    docs = {
        "REVIEWER_START_HERE_中文.md": reviewer_start_here(
            candidate, source_candidate, package_dir, zip_name
        ),
        "REVIEWER_CHECKLIST_中文.md": reviewer_checklist(
            candidate, source_candidate, Path(package_dir).name
        ),
        "FEEDBACK_TEMPLATE_中文.md": feedback_template(
            candidate, source_candidate, package_dir, zip_name
        ),
    }
    entries = []
    for name, text in docs.items():
        path = output_dir / name
        path.write_text(text, encoding="utf-8")
        scan_text_file(path)
        entries.append(build_manifest_entry(path, output_dir, "S1_LOCAL_OFFLINE_CHINESE_REVIEW_PACKAGE"))
    return entries


def create_zip(output_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output_dir.rglob("*")):
            if path.is_file():
                archive.write(path, portable_path(path, output_dir))


def resolve_outer_zip_manifest_path(
    repo_root: Path,
    zip_path: Path,
    explicit_path: str | None,
) -> Path:
    if explicit_path:
        target = (repo_root / explicit_path).resolve()
    else:
        target = Path(str(zip_path) + ".outer_zip_manifest.json")
    assert_inside_repo(target, repo_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def build_package(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    source_package = (repo_root / args.source_package).resolve()
    screenshot_dir = (repo_root / args.screenshot_dir).resolve()
    output_dir = (repo_root / args.output_dir).resolve()
    zip_path = (repo_root / args.zip_path).resolve()
    package_dir_ref = portable_path(output_dir, repo_root)
    zip_name = zip_path.name

    validate_source_boundaries(source_package)
    ensure_clean_output(output_dir, zip_path, repo_root)

    entries = []
    entries.extend(copy_evidence(source_package, output_dir))
    entries.extend(write_reviewer_docs(output_dir, args.candidate, args.source_candidate, package_dir_ref, zip_name))
    screenshot_entries, included_screenshot_specs = copy_screenshots(screenshot_dir, output_dir)
    entries.extend(screenshot_entries)
    screenshot_files = [f"screenshots/{name}" for name, _, _ in included_screenshot_specs]
    folded_state_primary_relpath = f"screenshots/{REQUIRED_ARCHIVE_SCREENSHOT_FILES[0]}".replace("\\", "/")
    folded_state_screenshot_hashes = {
        f"screenshots/{name}".replace("\\", "/"): file_sha256(output_dir / "screenshots" / name)
        for name in REQUIRED_ARCHIVE_SCREENSHOT_FILES
    }
    required_archive_evidence = required_archive_evidence_payload(
        folded_state_primary_sha256=folded_state_screenshot_hashes[folded_state_primary_relpath],
        folded_state_screenshot_sha256=folded_state_screenshot_hashes,
    )
    validation_sources = []
    if args.screenshot_safety_scan:
        validation_sources.append((repo_root / args.screenshot_safety_scan).resolve())
    for validation_artifact in args.validation_artifact:
        validation_sources.append((repo_root / validation_artifact).resolve())
    validation_entries = copy_validation_artifacts(validation_sources, output_dir)
    entries.extend(validation_entries)
    validation_files = [entry["path"] for entry in validation_entries]

    package_index_path = output_dir / "PACKAGE_INDEX_中文.json"
    write_json(
        package_index_path,
        package_index(
            args.candidate,
            args.source_candidate,
            package_dir_ref,
            zip_name,
            screenshot_files,
            validation_files,
            required_archive_evidence,
        ),
    )
    entries.append(build_manifest_entry(package_index_path, output_dir, "S1_LOCAL_OFFLINE_CHINESE_REVIEW_PACKAGE"))

    screenshot_index_path = output_dir / "SCREENSHOT_INDEX.json"
    write_json(
        screenshot_index_path,
        screenshot_index(
            args.candidate,
            args.source_candidate,
            args.source_commit,
            output_dir,
            included_screenshot_specs,
        ),
    )
    entries.append(build_manifest_entry(screenshot_index_path, output_dir, "S1_LOCAL_OFFLINE_CHINESE_REVIEW_PACKAGE"))

    entries = sorted(entries, key=lambda item: item["path"])
    package_manifest = {
        "schema_version": "secupilot.s1.local_offline_chinese_review_package_manifest.v1",
        "candidate": args.candidate,
        "source_candidate": args.source_candidate,
        "source_commit": args.source_commit,
        "generated_at_utc": utc_now(),
        "package_dir": package_dir_ref,
        "zip_name": zip_name,
        "required_archive_evidence": required_archive_evidence,
        "package_files": entries,
        "boundaries": BOUNDARIES,
    }
    package_manifest["manifest_self_sha256"] = manifest_self_sha256(package_manifest)
    package_manifest_path = output_dir / "package_manifest.json"
    write_json(package_manifest_path, package_manifest)

    outer_zip_manifest_path = resolve_outer_zip_manifest_path(
        repo_root=repo_root,
        zip_path=zip_path,
        explicit_path=args.outer_zip_manifest,
    )
    create_zip(output_dir, zip_path)
    outer_zip_manifest = build_outer_zip_manifest_payload(
        candidate=args.candidate,
        source_candidate=args.source_candidate,
        package_dir=package_dir_ref,
        zip_path=zip_path,
        package_manifest_path=package_manifest_path,
        manifest_self_hash=package_manifest["manifest_self_sha256"],
        repo_root=repo_root,
    )
    write_json(outer_zip_manifest_path, outer_zip_manifest)
    zip_sha256 = outer_zip_manifest["zip_sha256"]
    return {
        "status": "PASS",
        "candidate": args.candidate,
        "package_dir": package_dir_ref,
        "zip_path": portable_path(zip_path, repo_root),
        "zip_sha256": zip_sha256,
        "manifest_self_sha256": package_manifest["manifest_self_sha256"],
        "outer_zip_manifest_path": portable_path(outer_zip_manifest_path, repo_root),
        "outer_zip_manifest_sha256": file_sha256(outer_zip_manifest_path),
        "file_count": len(entries) + 1,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--source-candidate", required=True)
    parser.add_argument("--source-package", required=True)
    parser.add_argument("--screenshot-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--zip-path", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--screenshot-safety-scan")
    parser.add_argument("--validation-artifact", action="append", default=[])
    parser.add_argument("--outer-zip-manifest")
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
