#!/usr/bin/env python3
"""Build a self-contained local/offline reviewer handoff package for an RC."""

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

BOUNDARY_FALSE_KEYS = (
    "real_data",
    "masked_real_data",
    "live_qwen_api",
    "live_connectors",
    "production_writeback",
    "customer_visible_output",
    "push",
)

FORBIDDEN_TEXT_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"authorization\s*[:=]\s*\S+",
        r"bearer\s+[A-Za-z0-9._~+/=-]{12,}",
        r"api[_-]?key\s*[:=]\s*\S+",
        r"secret\s*[:=]\s*\S+",
        r"token\s*[:=]\s*\S+",
        r"private[_-]?key\s*[:=]\s*\S+",
        r"raw_payload\s*[:=]",
        r"raw_evidence\s*[:=]",
        r"writeback_action\s*[:=]",
        r"customer_visible_message\s*[:=]",
    )
)


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


def portable_path(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


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


def scan_text(text: str, label: str) -> None:
    for pattern in FORBIDDEN_TEXT_PATTERNS:
        if pattern.search(text):
            raise ValueError(f"{label}: forbidden text pattern {pattern.pattern}")


def require_false_boundaries(boundaries: dict[str, Any], source: str) -> None:
    for key in BOUNDARY_FALSE_KEYS:
        if boundaries.get(key) is not False:
            raise ValueError(f"{source} boundary must be false: {key}")


def validate_inputs(args: argparse.Namespace, repo_root: Path) -> dict[str, Any]:
    package_dir = (repo_root / args.package_dir).resolve()
    package_zip = (repo_root / args.package_zip).resolve()
    screenshot_scan_path = (repo_root / args.screenshot_safety_scan).resolve()
    rc_consistency_path = (repo_root / args.rc_consistency_check).resolve()
    qwen_validation_path = (repo_root / args.qwen_preview_validation).resolve()
    qwen_screenshot_path = (repo_root / args.qwen_preview_screenshot).resolve()
    qwen_text_path = (repo_root / args.qwen_preview_text).resolve()

    for path in (
        package_dir,
        package_zip,
        screenshot_scan_path,
        rc_consistency_path,
        qwen_validation_path,
        qwen_screenshot_path,
        qwen_text_path,
    ):
        if not path.exists():
            raise FileNotFoundError(f"missing handoff input: {path}")

    package_index = read_json(package_dir / "PACKAGE_INDEX_中文.json")
    package_manifest = read_json(package_dir / "package_manifest.json")
    screenshot_scan = read_json(screenshot_scan_path)
    rc_consistency = read_json(rc_consistency_path)
    qwen_validation = read_json(qwen_validation_path)

    candidate = package_index.get("candidate")
    source_candidate = package_index.get("source_candidate")
    if not candidate:
        raise ValueError("package index candidate is required")
    if package_manifest.get("candidate") != candidate:
        raise ValueError("package manifest candidate must match package index")
    if package_manifest.get("source_candidate") != source_candidate:
        raise ValueError("package manifest source_candidate must match package index")
    require_false_boundaries(package_index.get("boundaries", {}), "package_index")
    require_false_boundaries(package_manifest.get("boundaries", {}), "package_manifest")

    if screenshot_scan.get("status") != "PASS":
        raise ValueError("screenshot safety scan must be PASS")
    if screenshot_scan.get("blocking_finding_count") != 0:
        raise ValueError("screenshot safety scan blocking findings must be 0")
    if rc_consistency.get("status") != "PASS":
        raise ValueError("RC consistency check must be PASS")
    if rc_consistency.get("blocking_finding_count") != 0:
        raise ValueError("RC consistency blocking findings must be 0")
    if qwen_validation.get("status") != "PASS":
        raise ValueError("Qwen dry UI preview validation must be PASS")
    if qwen_validation.get("network_call") is not False:
        raise ValueError("Qwen validation network_call must be false")
    if qwen_validation.get("live_qwen_api") is not False:
        raise ValueError("Qwen validation live_qwen_api must be false")

    qwen_text = qwen_text_path.read_text(encoding="utf-8")
    scan_text(qwen_text, qwen_text_path.name)

    return {
        "candidate": candidate,
        "source_candidate": source_candidate,
        "package_index": package_index,
        "package_manifest": package_manifest,
        "screenshot_scan": screenshot_scan,
        "rc_consistency": rc_consistency,
        "qwen_validation": qwen_validation,
        "paths": {
            "package_dir": package_dir,
            "package_zip": package_zip,
            "screenshot_scan": screenshot_scan_path,
            "rc_consistency": rc_consistency_path,
            "qwen_validation": qwen_validation_path,
            "qwen_screenshot": qwen_screenshot_path,
            "qwen_text": qwen_text_path,
        },
    }


def copy_file(src: Path, dst: Path, output_dir: Path, entries: list[dict[str, Any]], label: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    entries.append(
        {
            "label": label,
            "path": portable_path(dst, output_dir),
            "bytes": dst.stat().st_size,
            "sha256": file_sha256(dst),
        }
    )


def handoff_start_here(candidate: str, source_candidate: str, package_zip_name: str) -> str:
    return f"""# SecuPilot RC-010 中文本地离线评审交接包

## 先读这个

本交接包用于把 RC-010 本地离线评审材料一次性交给 reviewer。

```text
candidate = {candidate}
source_candidate = {source_candidate}
rc_package_zip = {package_zip_name}
review_mode = LOCAL_OFFLINE_REVIEW_ONLY
customer_visible_or_deploy_go = false
```

## 推荐评审顺序

1. 打开 `reviewer_entry/RC010_REVIEWER_START_HERE_中文.md`。
2. 打开 `reviewer_entry/RC010_REVIEWER_CHECKLIST_中文.md`。
3. 核对 `validation/screenshot_safety_scan.json` 和 `validation/rc_consistency_check.json`。
4. 查看 `qwen_preview/s1-qwen-dry-provider-preview.png`，确认 dry provider 只是本地 UI 预览。
5. 如需完整 RC 包，解压 `rc_package/{package_zip_name}`。

## 明确不授权

```text
real_data = false
masked_real_data = false
live_qwen_api = false
live_connectors = false
production_writeback = false
customer_visible_output = false
external_pilot = false
production_launch = false
push = false
```
"""


def reviewer_prompt(candidate: str) -> str:
    return f"""# 给 reviewer 的中文提示词

请对 SecuPilot `{candidate}` 本地离线评审交接包做一次离线审查。

请按以下顺序检查：

1. 先读 `REVIEWER_START_HERE_中文.md` 和 `RC010_REVIEWER_START_HERE_中文.md`。
2. 核验 RC package manifest、screenshot safety scan、RC consistency check。
3. 打开四张 `/s1-trial` 和 `/s1-run` 截图，确认页面没有 P1/P2/P3、Mock Fixture、Expert Mode 或旧 RC 口径。
4. 打开 Qwen dry provider UI preview 截图，确认它只是 dry contract 预览，没有 live Qwen/API、connector、写回、自主动作或 API key。
5. 输出结论：

```text
PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL
PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
HOLD_FOR_UI_OR_PACKAGE_FIXES
NO_GO_FOR_CURRENT_PRODUCT_PATH
```

本评审不授权客户可见发布、部署、真实数据、live Qwen/API、connector、生产写回、外部试点或生产上线。
"""


def create_zip(output_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output_dir.rglob("*")):
            if path.is_file():
                archive.write(path, portable_path(path, output_dir))


def build_handoff(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    output_dir = (repo_root / args.output_dir).resolve()
    zip_path = (repo_root / args.zip_path).resolve()
    context = validate_inputs(args, repo_root)
    paths = context["paths"]
    ensure_clean_output(output_dir, zip_path, repo_root)

    entries: list[dict[str, Any]] = []
    package_zip_name = paths["package_zip"].name

    start_here = handoff_start_here(context["candidate"], context["source_candidate"], package_zip_name)
    prompt = reviewer_prompt(context["candidate"])
    (output_dir / "REVIEWER_HANDOFF_START_HERE_中文.md").write_text(start_here, encoding="utf-8")
    (output_dir / "REVIEWER_PROMPT_中文.md").write_text(prompt, encoding="utf-8")
    scan_text(start_here, "REVIEWER_HANDOFF_START_HERE_中文.md")
    scan_text(prompt, "REVIEWER_PROMPT_中文.md")

    for name, label in (
        ("REVIEWER_START_HERE_中文.md", "rc_start_here"),
        ("REVIEWER_CHECKLIST_中文.md", "rc_checklist"),
        ("FEEDBACK_TEMPLATE_中文.md", "rc_feedback_template"),
        ("package_manifest.json", "rc_package_manifest"),
        ("PACKAGE_INDEX_中文.json", "rc_package_index"),
    ):
        copy_file(paths["package_dir"] / name, output_dir / "reviewer_entry" / f"RC010_{name}", output_dir, entries, label)

    copy_file(paths["package_zip"], output_dir / "rc_package" / package_zip_name, output_dir, entries, "rc_package_zip")
    copy_file(paths["screenshot_scan"], output_dir / "validation" / "screenshot_safety_scan.json", output_dir, entries, "screenshot_safety_scan")
    copy_file(paths["rc_consistency"], output_dir / "validation" / "rc_consistency_check.json", output_dir, entries, "rc_consistency_check")
    copy_file(paths["qwen_validation"], output_dir / "qwen_preview" / "qwen_dry_ui_preview_validation.json", output_dir, entries, "qwen_validation")
    copy_file(paths["qwen_screenshot"], output_dir / "qwen_preview" / paths["qwen_screenshot"].name, output_dir, entries, "qwen_preview_screenshot")
    copy_file(paths["qwen_text"], output_dir / "qwen_preview" / paths["qwen_text"].name, output_dir, entries, "qwen_preview_text")

    entries.extend(
        [
            {
                "label": "handoff_start_here",
                "path": "REVIEWER_HANDOFF_START_HERE_中文.md",
                "bytes": (output_dir / "REVIEWER_HANDOFF_START_HERE_中文.md").stat().st_size,
                "sha256": file_sha256(output_dir / "REVIEWER_HANDOFF_START_HERE_中文.md"),
            },
            {
                "label": "reviewer_prompt",
                "path": "REVIEWER_PROMPT_中文.md",
                "bytes": (output_dir / "REVIEWER_PROMPT_中文.md").stat().st_size,
                "sha256": file_sha256(output_dir / "REVIEWER_PROMPT_中文.md"),
            },
        ]
    )

    manifest = {
        "schema_version": "secupilot.rc_review_handoff_manifest.v1",
        "generated_at_utc": utc_now(),
        "candidate": context["candidate"],
        "source_candidate": context["source_candidate"],
        "package_zip": f"rc_package/{package_zip_name}",
        "screenshot_safety_status": context["screenshot_scan"].get("status"),
        "rc_consistency_status": context["rc_consistency"].get("status"),
        "qwen_preview_validation_status": context["qwen_validation"].get("status"),
        "entries": sorted(entries, key=lambda item: item["path"]),
        "boundaries": {key: False for key in BOUNDARY_FALSE_KEYS},
        "customer_visible_or_deploy_go": False,
    }
    write_json(output_dir / "HANDOFF_MANIFEST.json", manifest)

    create_zip(output_dir, zip_path)
    return {
        "status": "PASS",
        "candidate": context["candidate"],
        "handoff_dir": portable_path(output_dir, repo_root),
        "handoff_zip": portable_path(zip_path, repo_root),
        "handoff_zip_sha256": file_sha256(zip_path),
        "entry_count": len(entries) + 1,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--package-zip", required=True)
    parser.add_argument("--screenshot-safety-scan", required=True)
    parser.add_argument("--rc-consistency-check", required=True)
    parser.add_argument("--qwen-preview-validation", required=True)
    parser.add_argument("--qwen-preview-screenshot", required=True)
    parser.add_argument("--qwen-preview-text", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--zip-path", required=True)
    parser.add_argument("--repo-root", default=".")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = build_handoff(args)
    except Exception as exc:
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
