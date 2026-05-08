#!/usr/bin/env python3
"""Generate a local/offline private deployment prerequisite and sizing draft."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

SCHEMA_VERSION = "secupilot.private_deployment_prereq_sizing_draft.v1"
DEFAULT_JSON_NAME = "private_deployment_prereq_sizing_draft.json"
DEFAULT_MD_NAME = "private_deployment_prereq_sizing_draft_中文.md"

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
    "cookie:",
    "set-cookie",
    "writeback_action",
    "production_connector_output",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


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


def scan_value(value: Any, *, label: str) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            scan_value(nested, label=f"{label}.{key}")
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            scan_value(nested, label=f"{label}[{index}]")
        return
    if not isinstance(value, str):
        return

    lowered = value.lower()
    for fragment in FORBIDDEN_LITERAL_FRAGMENTS:
        if fragment.lower() in lowered:
            raise ValueError(f"{label}: forbidden literal fragment {fragment}")


def feedback_records(feedback_payload: dict[str, Any]) -> list[dict[str, Any]]:
    feedback = feedback_payload.get("feedback")
    if not isinstance(feedback, list) or not feedback:
        raise ValueError("feedback sample must contain a non-empty feedback list")
    return [item for item in feedback if isinstance(item, dict)]


def text_blob(item: dict[str, Any]) -> str:
    return " ".join(str(item.get(field, "")) for field in ("missing_information", "blocker", "notes"))


def source_ids_for(records: list[dict[str, Any]], keywords: tuple[str, ...]) -> list[str]:
    result: list[str] = []
    lowered_keywords = tuple(keyword.lower() for keyword in keywords)
    for item in records:
        lowered = text_blob(item).lower()
        if any(keyword in lowered for keyword in lowered_keywords):
            response_id = str(item.get("response_id", "")).strip()
            if response_id:
                result.append(response_id)
    return result


def missing_information_items(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for record in records:
        missing = str(record.get("missing_information", "")).strip()
        if missing:
            items.append(
                {
                    "response_id": str(record.get("response_id", "")),
                    "reviewer_role": str(record.get("reviewer_role", "")),
                    "missing_information": missing,
                }
            )
    return items


def build_windows_prerequisites(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "status": "DRAFT_FROM_FEEDBACK",
        "source_feedback_ids": source_ids_for(records, ("windows", "前置依赖", "依赖")),
        "checks_to_turn_into_precheck_script": [
            {
                "id": "WIN-PREQ-01",
                "name": "Windows local execution environment",
                "name_zh": "Windows 本地执行环境",
                "draft_requirement": "Windows workstation or Windows Server host that can run local PowerShell scripts.",
                "draft_requirement_zh": "可运行本地 PowerShell 脚本的 Windows 工作站或 Windows Server 主机。",
                "verification_hint": "Check OS family and script execution ability in a future local precheck script.",
                "verification_hint_zh": "后续本地 precheck 脚本检查操作系统类型和脚本执行能力。",
            },
            {
                "id": "WIN-PREQ-02",
                "name": "PowerShell execution",
                "name_zh": "PowerShell 执行能力",
                "draft_requirement": "PowerShell can run local signed or explicitly bypassed dry-run scripts for this package.",
                "draft_requirement_zh": "PowerShell 可运行本包内的本地 dry-run 脚本。",
                "verification_hint": "Run scripts/VERIFY_BOUNDARIES.ps1 and scripts/START_CUSTOMER_TRIAL.ps1 locally.",
                "verification_hint_zh": "本地运行 scripts/VERIFY_BOUNDARIES.ps1 和 scripts/START_CUSTOMER_TRIAL.ps1。",
            },
            {
                "id": "WIN-PREQ-03",
                "name": "Python launcher",
                "name_zh": "Python 启动器",
                "draft_requirement": "Python launcher can execute local SecuPilot package/report commands.",
                "draft_requirement_zh": "Python 启动器可执行本地 SecuPilot 包与报告生成命令。",
                "verification_hint": "Run py -3 --version and local report generation commands.",
                "verification_hint_zh": "运行 py -3 --version 以及本地报告生成命令。",
            },
            {
                "id": "WIN-PREQ-04",
                "name": "Local file permissions",
                "name_zh": "本地文件权限",
                "draft_requirement": "Current user can read package files and write trial_output artifacts.",
                "draft_requirement_zh": "当前用户可读取包文件，并可写入 trial_output 产物目录。",
                "verification_hint": "Create and delete a local test file under trial_output in a future precheck.",
                "verification_hint_zh": "后续 precheck 在 trial_output 下创建并删除本地测试文件。",
            },
        ],
    }


def build_sizing_profiles(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "status": "DRAFT_NOT_BENCHMARKED",
        "source_feedback_ids": source_ids_for(records, ("资源", "sizing", "部署 sizing", "需求")),
        "profiles": [
            {
                "id": "SIZE-LOCAL-TRIAL",
                "purpose": "Local/offline reviewer trial for package, reports, and screenshots",
                "purpose_zh": "本地离线评审试用，用于打开包、报告和截图",
                "cpu": "2 vCPU draft",
                "memory": "4 GB RAM draft",
                "disk": "2 GB free local workspace draft",
                "notes": "For dry-run package and local reports only; not a production benchmark.",
                "notes_zh": "仅用于 dry-run 包和本地报告，不是生产 benchmark。",
            },
            {
                "id": "SIZE-LAB-PILOT-DRAFT",
                "purpose": "Private lab dry-run with larger synthetic packages",
                "purpose_zh": "私有化实验室 dry-run，用于更大的 synthetic 包",
                "cpu": "4 vCPU draft",
                "memory": "8 GB RAM draft",
                "disk": "10 GB free local workspace draft",
                "notes": "Requires future benchmark before any customer pilot or production sizing claim.",
                "notes_zh": "任何客户试点或生产 sizing 结论前都需要后续 benchmark。",
            },
            {
                "id": "SIZE-PRODUCTION-TBD",
                "purpose": "Future private production deployment",
                "purpose_zh": "未来私有化生产部署",
                "cpu": "TBD",
                "memory": "TBD",
                "disk": "TBD",
                "notes": "Not authorized and not benchmarked in this Goal.",
                "notes_zh": "本 Goal 不授权、不 benchmark、不声明生产规格。",
            },
        ],
    }


def build_model_provider_path(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "status": "DRY_RUN_PATH_ONLY",
        "source_feedback_ids": source_ids_for(records, ("模型", "qwen", "provider", "接入路径")),
        "stages": [
            {
                "id": "MODEL-01",
                "name": "Current dry-run provider",
                "name_zh": "当前 dry-run provider",
                "description": "Use local fixture/provider dry-run outputs only.",
                "description_zh": "仅使用本地 fixture/provider dry-run 输出。",
                "live_call": False,
            },
            {
                "id": "MODEL-02",
                "name": "Cloud Qwen contract simulation",
                "name_zh": "云端 Qwen contract 模拟",
                "description": "Validate request/response shape, latency states, error states, and fallback UI without API keys.",
                "description_zh": "在无 API key 条件下验证请求/响应形态、延迟状态、错误状态和回退 UI。",
                "live_call": False,
            },
            {
                "id": "MODEL-03",
                "name": "Private deployment model connector design",
                "name_zh": "私有化模型 connector 设计",
                "description": "Define where model endpoint config would live, with secret handling excluded from this draft.",
                "description_zh": "定义模型 endpoint 配置未来放在哪里；secret 处理不在本草案内。",
                "live_call": False,
            },
            {
                "id": "MODEL-04",
                "name": "Future live model authorization",
                "name_zh": "未来 live 模型授权",
                "description": "Requires a separate Goal with explicit API, data, secret, network, and rollback boundaries.",
                "description_zh": "需要单独 Goal 明确 API、数据、secret、网络和回滚边界。",
                "live_call": False,
            },
        ],
    }


def collect_follow_up_actions(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": "ACTION-01",
            "title": "Build Windows local prerequisite precheck script",
            "title_zh": "制作 Windows 本地前置依赖 precheck 脚本",
            "source_feedback_ids": source_ids_for(records, ("windows", "前置依赖", "依赖")),
            "suggested_goal": "GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT",
        },
        {
            "id": "ACTION-02",
            "title": "Convert sizing draft into benchmark-ready sizing report",
            "title_zh": "把 sizing 草案推进为可 benchmark 的资源报告",
            "source_feedback_ids": source_ids_for(records, ("资源", "sizing", "需求")),
            "suggested_goal": "GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT",
        },
        {
            "id": "ACTION-03",
            "title": "Map dry-run model provider path to customer-facing setup flow",
            "title_zh": "把 dry-run 模型接入路径映射到客户可理解的配置流程",
            "source_feedback_ids": source_ids_for(records, ("模型", "qwen", "provider", "接入路径")),
            "suggested_goal": "GOAL-MVP-80_MODEL_PROVIDER_SETUP_FLOW_DRY_RUN",
        },
    ]


def collect_blockers(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    for record in records:
        blocker = str(record.get("blocker", "")).strip()
        if blocker:
            blockers.append(
                {
                    "response_id": str(record.get("response_id", "")),
                    "reviewer_role": str(record.get("reviewer_role", "")),
                    "blocker": blocker,
                }
            )
    return blockers


def render_markdown(draft: dict[str, Any]) -> str:
    missing_lines = "\n".join(
        f"- {item['response_id']} / {item['reviewer_role']}: {item['missing_information']}"
        for item in draft["source_feedback"]["missing_information_items"]
    ) or "- none"
    prereq_lines = "\n".join(
        f"- {item['id']}: {item.get('name_zh', item['name'])} - {item.get('draft_requirement_zh', item['draft_requirement'])}"
        for item in draft["windows_prerequisites"]["checks_to_turn_into_precheck_script"]
    )
    sizing_lines = "\n".join(
        f"- {item['id']}: {item.get('purpose_zh', item['purpose'])} / CPU {item['cpu']} / 内存 {item['memory']} / 磁盘 {item['disk']} / 说明：{item.get('notes_zh', item['notes'])}"
        for item in draft["resource_sizing"]["profiles"]
    )
    model_lines = "\n".join(
        f"- {item['id']}: {item.get('name_zh', item['name'])} - {item.get('description_zh', item['description'])}"
        for item in draft["model_provider_path"]["stages"]
    )
    action_lines = "\n".join(
        f"- {item['id']}: {item.get('title_zh', item['title'])} -> {item['suggested_goal']}"
        for item in draft["follow_up_actions"]
    )
    blocker_lines = "\n".join(
        f"- {item['response_id']} / {item['reviewer_role']}: {item['blocker']}"
        for item in draft["blockers"]
    ) or "- none"

    return f"""# SecuPilot 私有化部署前置条件与 Sizing 草案

Draft ID: `{draft['draft_id']}`

Package ID: `{draft['package_id']}`

Status: `{draft['status']}`

## 一句话结论

{draft['summary']}

## 来源反馈

{missing_lines}

## Windows 前置依赖草案

{prereq_lines}

## 资源需求 / Sizing 草案

{sizing_lines}

## 模型接入路径草案

{model_lines}

## 阻塞点

{blocker_lines}

## 建议后续 Goal

{action_lines}

## 边界

- 本草案不执行部署。
- 本草案不调用 live Qwen/API。
- 本草案不连接 live connector。
- 本草案不读取、保存或要求 secret/token/auth header。
- 本草案不使用真实数据或脱敏真实数据。
- 本草案不授权客户可见发布、外部试点或生产上线。
"""


def build_draft(
    *,
    package_dir: Path,
    feedback_json: Path,
    output_dir: Path,
    repo_root: Path,
) -> dict[str, Any]:
    assert_inside_repo(package_dir, repo_root)
    assert_inside_repo(feedback_json, repo_root)
    assert_inside_repo(output_dir, repo_root)

    manifest_path = package_dir / "package_manifest.json"
    status_path = package_dir / "trial_output" / "customer_trial_status.json"
    if not manifest_path.exists():
        raise ValueError(f"package manifest not found: {manifest_path}")
    if not status_path.exists():
        raise ValueError(f"trial status not found: {status_path}")
    if not feedback_json.exists():
        raise ValueError(f"feedback sample not found: {feedback_json}")

    manifest = read_json(manifest_path)
    trial_status = read_json(status_path)
    feedback_payload = read_json(feedback_json)
    package_id = str(manifest.get("package_id", ""))
    if not package_id:
        raise ValueError("package_id missing from manifest")
    if trial_status.get("package_id") != package_id or feedback_payload.get("package_id") != package_id:
        raise ValueError("package_id mismatch between manifest, trial status, and feedback sample")

    boundaries = trial_status.get("boundaries") or manifest.get("boundaries") or {}
    for field in FORBIDDEN_BOUNDARY_TRUE_FIELDS:
        if boundaries.get(field) is not False:
            raise ValueError(f"{field} is not false")

    records = feedback_records(feedback_payload)
    scan_value(feedback_payload, label="feedback_payload")
    blockers = collect_blockers(records)
    draft_status = "DRAFT_READY_FOR_INTERNAL_PRODUCT_REVIEW" if not blockers else "HOLD_FOR_BLOCKER_REVIEW"
    draft_id = f"{package_id}-private-deployment-prereq-sizing-draft"
    json_path = output_dir / DEFAULT_JSON_NAME
    md_path = output_dir / DEFAULT_MD_NAME
    draft = {
        "schema_version": SCHEMA_VERSION,
        "draft_id": draft_id,
        "generated_at_utc": utc_now(),
        "package_id": package_id,
        "package_dir": portable_path(package_dir, repo_root),
        "status": draft_status,
        "summary": "已将反馈样本转成 Windows 前置依赖、资源 sizing 和模型接入路径草案，下一步可做本地 precheck 脚本。",
        "inputs": {
            "package_manifest": portable_path(manifest_path, repo_root),
            "customer_trial_status": portable_path(status_path, repo_root),
            "feedback_json": portable_path(feedback_json, repo_root),
        },
        "source_feedback": {
            "feedback_count": len(records),
            "missing_information_items": missing_information_items(records),
        },
        "windows_prerequisites": build_windows_prerequisites(records),
        "resource_sizing": build_sizing_profiles(records),
        "model_provider_path": build_model_provider_path(records),
        "blockers": blockers,
        "follow_up_actions": collect_follow_up_actions(records),
        "non_authorization": [
            "No deployment executed",
            "No live Qwen/API/connectors",
            "No network request",
            "No production write-back",
            "No customer-visible publish/deploy",
            "No real or masked-real data",
            "No secrets, tokens, auth headers, or raw customer logs",
        ],
        "next_unlock": "GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT" if not blockers else None,
    }
    draft["outputs"] = {
        "json": portable_path(json_path, repo_root),
        "markdown": portable_path(md_path, repo_root),
    }
    scan_value(draft, label="draft")
    md_text = render_markdown(draft)
    scan_value(md_text, label=DEFAULT_MD_NAME)
    write_json(json_path, draft)
    write_text(md_path, md_text)
    return draft


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", required=True, type=Path)
    parser.add_argument("--feedback-json", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    args = parser.parse_args(argv)

    output_dir = args.output_dir or args.package_dir / "trial_output"
    try:
        draft = build_draft(
            package_dir=args.package_dir,
            feedback_json=args.feedback_json,
            output_dir=output_dir,
            repo_root=args.repo_root,
        )
    except Exception as exc:  # noqa: BLE001 - CLI converts draft violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    cli_status = "HOLD" if draft["status"].startswith("HOLD") else "PASS"
    print(
        json.dumps(
            {
                "status": cli_status,
                "draft": draft,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return HOLD if cli_status == "HOLD" else PASS


if __name__ == "__main__":
    sys.exit(run())
