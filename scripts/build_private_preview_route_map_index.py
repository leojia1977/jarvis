#!/usr/bin/env python3
"""Build a product-first route map index for private preview review packages."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

REQUIRED_FALSE_BOUNDARIES = (
    "real_data",
    "masked_real_data",
    "live_qwen_api",
    "live_connectors",
    "production_writeback",
    "customer_visible_output",
    "push",
)

ROUTE_TITLES = {
    "/s1-trial": "试用入口页",
    "/s1-run": "试用结果页",
}

ROUTE_OBJECTIVES = {
    "/s1-trial": "确认试用入口、评审范围和边界说明是否清晰。",
    "/s1-run": "确认结果页呈现产品结论，而不是证据目录。",
}

PERSONA_ROUTE_PLANS = (
    {
        "persona_key": "ENGINEER_REVIEWER",
        "persona_name": "工程师评审路径",
        "focus": "核验候选口径、路径一致性与截图可对账性。",
    },
    {
        "persona_key": "MANAGER_REVIEWER",
        "persona_name": "经理评审路径",
        "focus": "核验结果页表达与边界合规是否支持下一轮内部试用决策。",
    },
    {
        "persona_key": "CTO_REVIEWER",
        "persona_name": "CTO评审路径",
        "focus": "核验路线完整性、离线边界和风险控制声明是否满足私有预览门槛。",
    },
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def assert_inside_repo(path: Path, repo_root: Path) -> None:
    try:
        path.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"path is outside repo: {path}") from exc


def require_false_boundaries(label: str, payload: dict[str, Any]) -> None:
    boundaries = payload.get("boundaries")
    if not isinstance(boundaries, dict):
        raise ValueError(f"{label}: missing boundaries map")
    for key in REQUIRED_FALSE_BOUNDARIES:
        if boundaries.get(key) is not False:
            raise ValueError(f"{label}: boundary must be false: {key}")


def route_screenshot_map(screenshot_index: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    rows = screenshot_index.get("screenshots")
    if not isinstance(rows, list) or not rows:
        raise ValueError("SCREENSHOT_INDEX.json: screenshots must be a non-empty list")
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        route = str(row.get("route", "")).strip()
        if not route:
            continue
        grouped.setdefault(route, []).append(row)
    return grouped


def build_persona_routes(routes: list[str]) -> list[dict[str, Any]]:
    coverage = []
    for plan in PERSONA_ROUTE_PLANS:
        coverage.append(
            {
                "persona_key": plan["persona_key"],
                "persona_name": plan["persona_name"],
                "focus": plan["focus"],
                "ordered_routes": routes,
            }
        )
    return coverage


def markdown_table_rows(routes: list[str], screenshot_map: dict[str, list[dict[str, Any]]]) -> list[str]:
    rows = []
    for index, route in enumerate(routes, start=1):
        title = ROUTE_TITLES.get(route, f"页面 {route}")
        objective = ROUTE_OBJECTIVES.get(route, "核验页面是否符合产品评审定位。")
        shots = screenshot_map.get(route, [])
        shot_paths = " / ".join(sorted(str(item.get("path", "")) for item in shots if item.get("path")))
        rows.append(f"| {index} | `{route}` | {title} | {objective} | {shot_paths} |")
    return rows


def markdown_persona_blocks(persona_routes: list[dict[str, Any]]) -> list[str]:
    blocks = []
    for row in persona_routes:
        route_lines = "\n".join(f"{idx}. `{route}`" for idx, route in enumerate(row["ordered_routes"], start=1))
        blocks.append(
            "\n".join(
                (
                    f"### {row['persona_name']}",
                    "",
                    f"- 关注点：{row['focus']}",
                    "- 路线：",
                    route_lines,
                )
            )
        )
    return blocks


def build(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    package_dir = (repo_root / args.package_dir).resolve()
    output_md = (repo_root / args.output_md).resolve()
    output_json = (repo_root / args.output_json).resolve()
    for path in (package_dir, output_md, output_json):
        assert_inside_repo(path, repo_root)

    if not package_dir.is_dir():
        raise FileNotFoundError(f"missing package_dir: {package_dir}")

    package_index = read_json(package_dir / "PACKAGE_INDEX_中文.json")
    screenshot_index = read_json(package_dir / "SCREENSHOT_INDEX.json")
    package_manifest = read_json(package_dir / "package_manifest.json")

    require_false_boundaries("PACKAGE_INDEX_中文.json", package_index)
    require_false_boundaries("SCREENSHOT_INDEX.json", screenshot_index)
    require_false_boundaries("package_manifest.json", package_manifest)

    routes = package_index.get("route")
    if not isinstance(routes, list) or not routes:
        raise ValueError("PACKAGE_INDEX_中文.json: route must be a non-empty list")
    normalized_routes = [str(route).strip() for route in routes if str(route).strip()]
    if not normalized_routes:
        raise ValueError("PACKAGE_INDEX_中文.json: route list is empty after normalization")

    screenshot_map = route_screenshot_map(screenshot_index)
    for route in normalized_routes:
        if route not in screenshot_map:
            raise ValueError(f"missing screenshot coverage for route: {route}")

    persona_routes = build_persona_routes(normalized_routes)
    if len(persona_routes) != 3:
        raise ValueError("persona route coverage must include engineer, manager, and CTO")

    route_entries = []
    for route in normalized_routes:
        screenshots = screenshot_map.get(route, [])
        route_entries.append(
            {
                "route": route,
                "title": ROUTE_TITLES.get(route, f"页面 {route}"),
                "objective": ROUTE_OBJECTIVES.get(route, "核验页面是否符合产品评审定位。"),
                "screenshot_count": len(screenshots),
                "screenshot_paths": sorted(str(item.get("path", "")) for item in screenshots if item.get("path")),
            }
        )

    artifact_counts = {
        "package_file_count": len(package_manifest.get("package_files", [])),
        "evidence_file_count": len(package_index.get("evidence_files", [])),
        "validation_file_count": len(package_index.get("validation_files", [])),
    }

    payload = {
        "schema_version": "secupilot.private_preview.route_map_index.v1",
        "generated_at_utc": utc_now(),
        "candidate": package_index.get("candidate"),
        "source_candidate": package_index.get("source_candidate"),
        "package_dir": package_index.get("package_dir"),
        "zip_name": package_index.get("zip_name"),
        "route_entries": route_entries,
        "persona_route_coverage": persona_routes,
        "review_entry_files": {
            "start_here": package_index.get("start_here"),
            "checklist": package_index.get("checklist"),
            "feedback_template": package_index.get("feedback_template"),
        },
        "artifact_counts": artifact_counts,
        "boundaries": package_index.get("boundaries", {}),
        "non_authorization": {
            "customer_visible_or_deploy_go": False,
            "live_qwen_api": False,
            "production_writeback": False,
        },
    }
    write_json(output_json, payload)

    table_rows = markdown_table_rows(normalized_routes, screenshot_map)
    persona_blocks = markdown_persona_blocks(persona_routes)
    md = "\n".join(
        (
            f"# {payload['candidate']} 私有预览产品路径索引",
            "",
            f"生成时间（UTC）：{payload['generated_at_utc']}",
            f"Source candidate：`{payload['source_candidate']}`",
            f"Package：`{payload['package_dir']}`",
            "",
            "## 产品旅程总览",
            "",
            "| 步骤 | 路径 | 页面 | 评审目标 | 截图覆盖 |",
            "| --- | --- | --- | --- | --- |",
            *table_rows,
            "",
            "## 角色路径覆盖",
            "",
            *persona_blocks,
            "",
            "## 评审入口文件",
            "",
            f"- start_here: `{payload['review_entry_files']['start_here']}`",
            f"- checklist: `{payload['review_entry_files']['checklist']}`",
            f"- feedback_template: `{payload['review_entry_files']['feedback_template']}`",
            "",
            "## 边界与非授权",
            "",
            "```text",
            "real_data=false",
            "masked_real_data=false",
            "live_qwen_api=false",
            "live_connectors=false",
            "production_writeback=false",
            "customer_visible_output=false",
            "push=false",
            "customer_visible_or_deploy_go=false",
            "```",
            "",
            "## 补充统计",
            "",
            f"- package_file_count: {artifact_counts['package_file_count']}",
            f"- evidence_file_count: {artifact_counts['evidence_file_count']}",
            f"- validation_file_count: {artifact_counts['validation_file_count']}",
        )
    )
    write_text(output_md, md + "\n")
    return payload


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build private preview route-map index artifacts.")
    parser.add_argument("--package-dir", required=True, help="Package directory path relative to repo root.")
    parser.add_argument("--output-md", required=True, help="Output markdown path relative to repo root.")
    parser.add_argument("--output-json", required=True, help="Output JSON path relative to repo root.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        payload = build(args)
    except Exception as exc:  # pragma: no cover - top-level CLI guard
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False))
        return HOLD
    print(
        json.dumps(
            {
                "status": "PASS",
                "candidate": payload.get("candidate"),
                "route_count": len(payload.get("route_entries", [])),
                "output_md": args.output_md,
                "output_json": args.output_json,
            },
            ensure_ascii=False,
        )
    )
    return PASS


if __name__ == "__main__":
    raise SystemExit(run())
