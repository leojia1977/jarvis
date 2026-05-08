#!/usr/bin/env python3
"""Generate a local/offline internal trial KPI report from SecuPilot trial artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

SCHEMA_VERSION = "secupilot.internal_trial_kpi_report.v1"
DEFAULT_JSON_NAME = "internal_trial_kpi_report.json"
DEFAULT_MD_NAME = "internal_trial_kpi_report_中文.md"

FORBIDDEN_BOUNDARY_TRUE_FIELDS = (
    "real_data",
    "masked_real_data",
    "live_qwen_api",
    "live_connectors",
    "network_request",
    "api_key_required",
    "production_writeback",
    "customer_visible_output",
    "deploy_executed",
    "production_launch",
    "push",
    "autonomous_qwen_action",
)

FORBIDDEN_LITERAL_FRAGMENTS = (
    "Authorization:",
    "Bearer ",
    "refresh_token",
    "access_token",
    "api_key:",
    "api_key=",
    "private_key",
    "raw_payload",
    "raw_evidence",
    "writeback_action",
    "production_connector_output",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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


def scan_text(text: str, *, label: str) -> None:
    lowered = text.lower()
    for fragment in FORBIDDEN_LITERAL_FRAGMENTS:
        if fragment.lower() in lowered:
            raise ValueError(f"{label}: forbidden literal fragment {fragment}")


def normalize_feedback_records(payload: Any) -> list[dict[str, Any]]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("feedback", "responses", "items", "records"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    raise ValueError("feedback JSON must be a list or contain feedback/responses/items/records list")


def is_positive(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value > 0
    if isinstance(value, str):
        return value.strip().lower() in {"yes", "true", "pass", "understood", "useful", "准确", "有用", "看懂"}
    return False


def collect_feedback_metrics(feedback_path: Path | None) -> dict[str, Any]:
    if feedback_path is None:
        return {
            "feedback_source": None,
            "feedback_count": 0,
            "understanding_sample_count": 0,
            "understanding_positive_count": 0,
            "understanding_rate_percent": None,
            "usefulness_sample_count": 0,
            "usefulness_positive_count": 0,
            "usefulness_rate_percent": None,
            "missing_information_count": 0,
            "measurement_status": "PENDING_FEEDBACK",
        }

    feedback_records = normalize_feedback_records(read_json(feedback_path))
    understanding_values = [
        item.get("understood", item.get("can_understand", item.get("理解", None))) for item in feedback_records
    ]
    usefulness_values = [item.get("useful", item.get("is_useful", item.get("有用", None))) for item in feedback_records]
    understanding_values = [value for value in understanding_values if value is not None]
    usefulness_values = [value for value in usefulness_values if value is not None]
    missing_information_count = sum(
        1
        for item in feedback_records
        if item.get("missing_information") or item.get("缺失信息") or item.get("missing_info")
    )

    understanding_positive = sum(1 for value in understanding_values if is_positive(value))
    usefulness_positive = sum(1 for value in usefulness_values if is_positive(value))
    understanding_rate = (
        round(understanding_positive * 100 / len(understanding_values), 2) if understanding_values else None
    )
    usefulness_rate = round(usefulness_positive * 100 / len(usefulness_values), 2) if usefulness_values else None

    return {
        "feedback_source": feedback_path.as_posix(),
        "feedback_count": len(feedback_records),
        "understanding_sample_count": len(understanding_values),
        "understanding_positive_count": understanding_positive,
        "understanding_rate_percent": understanding_rate,
        "usefulness_sample_count": len(usefulness_values),
        "usefulness_positive_count": usefulness_positive,
        "usefulness_rate_percent": usefulness_rate,
        "missing_information_count": missing_information_count,
        "measurement_status": "MEASURED" if feedback_records else "PENDING_FEEDBACK",
    }


def collect_blockers(manifest: dict[str, Any], trial_status: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if manifest.get("status") != "STRUCTURE_ONLY_NOT_DEPLOYED":
        blockers.append({"id": "B01", "reason": "package manifest status is not structure-only"})
    if trial_status.get("status") != "LOCAL_TRIAL_ENTRY_READY":
        blockers.append({"id": "B02", "reason": "trial entry did not reach LOCAL_TRIAL_ENTRY_READY"})
    if trial_status.get("boundary_check", {}).get("status") != "PASS":
        blockers.append({"id": "B03", "reason": "boundary check did not pass"})

    boundaries = trial_status.get("boundaries") or manifest.get("boundaries") or {}
    for field in FORBIDDEN_BOUNDARY_TRUE_FIELDS:
        if boundaries.get(field) is not False:
            blockers.append({"id": f"B-{field}", "reason": f"{field} is not false"})
    return blockers


def completion_status(trial_status: dict[str, Any], blockers: list[dict[str, str]]) -> tuple[str, int]:
    if blockers:
        return "HOLD", 0
    if trial_status.get("status") == "LOCAL_TRIAL_ENTRY_READY":
        return "COMPLETE_LOCAL_DRY_RUN", 100
    return "INCOMPLETE", 0


def render_markdown(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    feedback = report["feedback"]
    blockers = report["blockers"]
    blocker_lines = "\n".join(f"- {item['id']}: {item['reason']}" for item in blockers) or "- none"
    understanding = (
        "PENDING_FEEDBACK"
        if feedback["understanding_rate_percent"] is None
        else f"{feedback['understanding_rate_percent']}%"
    )
    usefulness = (
        "PENDING_FEEDBACK"
        if feedback["usefulness_rate_percent"] is None
        else f"{feedback['usefulness_rate_percent']}%"
    )

    if feedback["measurement_status"] == "MEASURED":
        next_steps = """1. 将缺失信息反馈转入下一轮产品 backlog。
2. 继续补齐私有化部署前置依赖和资源需求说明。
3. 下一轮试用继续追加反馈样本并重新生成 KPI 报告。"""
    else:
        next_steps = """1. 继续收集内部试用反馈。
2. 若反馈样本存在，重新运行本报告生成器并计算理解率/可用性正向率。
3. 若无阻塞，可进入客户试用 README 与一键启动体验继续打磨。"""

    return f"""# SecuPilot 内部试用 KPI 报告

Report ID: `{report['report_id']}`

Package ID: `{report['package_id']}`

Status: `{report['status']}`

## 一句话结论

{report['summary']}

## 核心指标

| 指标 | 结果 |
| --- | --- |
| 本地试用启动完成率 | {metrics['trial_completion_rate_percent']}% |
| 边界检查 | {metrics['boundary_check_status']} |
| 理解率 | {understanding} |
| 可用性正向率 | {usefulness} |
| 反馈数 | {feedback['feedback_count']} |
| 缺失信息反馈数 | {feedback['missing_information_count']} |
| 阻塞点数量 | {len(blockers)} |

## 阻塞点

{blocker_lines}

## 当前边界

- 真实数据：false
- 脱敏真实数据：false
- live Qwen/API：false
- live connector：false
- 网络请求：false
- 生产写回：false
- 客户可见发布：false
- 实际部署执行：false

## 下一步

{next_steps}

## 非授权声明

本报告不授权真实数据、脱敏真实数据、live Qwen/API/connectors、生产写回、客户可见发布、外部试点或生产上线。
"""


def build_report(
    *,
    package_dir: Path,
    output_dir: Path,
    repo_root: Path,
    feedback_json: Path | None = None,
) -> dict[str, Any]:
    assert_inside_repo(package_dir, repo_root)
    assert_inside_repo(output_dir, repo_root)
    if feedback_json is not None:
        assert_inside_repo(feedback_json, repo_root)

    manifest_path = package_dir / "package_manifest.json"
    status_path = package_dir / "trial_output" / "customer_trial_status.json"
    if not manifest_path.exists():
        raise ValueError(f"package manifest not found: {manifest_path}")
    if not status_path.exists():
        raise ValueError(f"trial status not found: {status_path}")

    manifest = read_json(manifest_path)
    trial_status = read_json(status_path)
    if manifest.get("package_id") != trial_status.get("package_id"):
        raise ValueError("package_id mismatch between manifest and trial status")

    blockers = collect_blockers(manifest, trial_status)
    status, completion_rate = completion_status(trial_status, blockers)
    feedback = collect_feedback_metrics(feedback_json)
    boundary_check_status = trial_status.get("boundary_check", {}).get("status", "UNKNOWN")
    package_id = str(manifest["package_id"])
    report_id = f"{package_id}-internal-trial-kpi"
    measured_feedback = feedback["measurement_status"] == "MEASURED"
    if status == "COMPLETE_LOCAL_DRY_RUN" and measured_feedback:
        summary = "本地离线试用入口已完成 dry-run 启动，反馈样本已计入 KPI，缺失信息可进入下一轮产品 backlog。"
    elif status == "COMPLETE_LOCAL_DRY_RUN":
        summary = "本地离线试用入口已完成 dry-run 启动且边界检查通过，等待内部试用反馈样本。"
    else:
        summary = "本地离线试用入口存在阻塞，需要先修复 HOLD 项。"

    next_unlock = (
        "GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT"
        if status == "COMPLETE_LOCAL_DRY_RUN" and feedback["measurement_status"] == "MEASURED"
        else "GOAL-MVP-76_CUSTOMER_TRIAL_FEEDBACK_SAMPLE_CAPTURE"
        if status == "COMPLETE_LOCAL_DRY_RUN"
        else None
    )

    report = {
        "schema_version": SCHEMA_VERSION,
        "report_id": report_id,
        "generated_at_utc": utc_now(),
        "package_id": package_id,
        "package_dir": portable_path(package_dir, repo_root),
        "status": (
            "INTERNAL_TRIAL_FEEDBACK_MEASURED"
            if status == "COMPLETE_LOCAL_DRY_RUN" and measured_feedback
            else "READY_FOR_INTERNAL_TRIAL_FEEDBACK_COLLECTION"
            if status == "COMPLETE_LOCAL_DRY_RUN"
            else "HOLD"
        ),
        "summary": summary,
        "inputs": {
            "package_manifest": portable_path(manifest_path, repo_root),
            "customer_trial_status": portable_path(status_path, repo_root),
            "feedback_json": portable_path(feedback_json, repo_root) if feedback_json else None,
        },
        "metrics": {
            "completion_status": status,
            "trial_completion_rate_percent": completion_rate,
            "boundary_check_status": boundary_check_status,
            "boundary_false_count": sum(
                1 for field in FORBIDDEN_BOUNDARY_TRUE_FIELDS if trial_status.get("boundaries", {}).get(field) is False
            ),
            "boundary_required_count": len(FORBIDDEN_BOUNDARY_TRUE_FIELDS),
        },
        "feedback": feedback,
        "blockers": blockers,
        "non_authorization": [
            "No real data",
            "No masked-real data",
            "No live Qwen/API/connectors",
            "No production write-back",
            "No customer-visible publish/deploy",
            "No external pilot",
            "No production launch",
        ],
        "next_unlock": next_unlock,
    }

    json_path = output_dir / DEFAULT_JSON_NAME
    md_path = output_dir / DEFAULT_MD_NAME
    report["outputs"] = {
        "json": portable_path(json_path, repo_root),
        "markdown": portable_path(md_path, repo_root),
    }
    json_text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    md_text = render_markdown(report)
    scan_text(json_text, label=DEFAULT_JSON_NAME)
    scan_text(md_text, label=DEFAULT_MD_NAME)
    write_text(md_path, md_text)
    write_text(json_path, json_text)
    return report


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    parser.add_argument("--feedback-json", type=Path)
    args = parser.parse_args(argv)

    output_dir = args.output_dir or args.package_dir / "trial_output"
    try:
        report = build_report(
            package_dir=args.package_dir,
            output_dir=output_dir,
            repo_root=args.repo_root,
            feedback_json=args.feedback_json,
        )
    except Exception as exc:  # noqa: BLE001 - CLI converts report violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    cli_status = "HOLD" if report["status"] == "HOLD" else "PASS"
    print(json.dumps({"status": cli_status, "report": report}, ensure_ascii=False, indent=2))
    return HOLD if cli_status == "HOLD" else PASS


if __name__ == "__main__":
    sys.exit(run())
