#!/usr/bin/env python3
"""Generate a local/offline private deployment sizing report."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

SCHEMA_VERSION = "secupilot.private_deployment_sizing_report.v1"
DEFAULT_JSON_NAME = "private_deployment_sizing_report.json"
DEFAULT_MD_NAME = "private_deployment_sizing_report_中文.md"

FORBIDDEN_BOUNDARY_TRUE_FIELDS = (
    "deploy_executed",
    "network_request",
    "live_qwen_api",
    "live_connectors",
    "production_writeback",
    "customer_visible_output",
    "real_data",
    "masked_real_data",
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


def check_boundaries(boundaries: dict[str, Any]) -> None:
    for field in FORBIDDEN_BOUNDARY_TRUE_FIELDS:
        if boundaries.get(field) is not False:
            raise ValueError(f"{field} is not false")


def validate_inputs(draft: dict[str, Any], precheck: dict[str, Any]) -> None:
    if draft.get("status") != "DRAFT_READY_FOR_INTERNAL_PRODUCT_REVIEW":
        raise ValueError("prereq/sizing draft status is not ready")
    if draft.get("resource_sizing", {}).get("status") != "DRAFT_NOT_BENCHMARKED":
        raise ValueError("resource sizing source must remain DRAFT_NOT_BENCHMARKED")
    profiles = draft.get("resource_sizing", {}).get("profiles")
    if not isinstance(profiles, list) or len(profiles) < 3:
        raise ValueError("resource sizing source must include at least three profiles")
    if precheck.get("status") != "PRIVATE_DEPLOYMENT_PRECHECK_PASS":
        raise ValueError("private deployment precheck did not pass")
    checks = precheck.get("checks")
    if not isinstance(checks, list) or len(checks) < 4:
        raise ValueError("precheck result must include four checks")
    failed = [item for item in checks if not item.get("passed")]
    if failed:
        raise ValueError("private deployment precheck contains failed checks")
    check_boundaries(precheck.get("boundaries", {}))


def normalize_profiles(profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for profile in profiles:
        profile_id = str(profile.get("id", ""))
        if not profile_id:
            raise ValueError("sizing profile missing id")
        normalized.append(
            {
                "id": profile_id,
                "purpose": profile.get("purpose", ""),
                "purpose_zh": profile.get("purpose_zh", profile.get("purpose", "")),
                "cpu": profile.get("cpu", "TBD"),
                "memory": profile.get("memory", "TBD"),
                "disk": profile.get("disk", "TBD"),
                "source_notes": profile.get("notes", ""),
                "source_notes_zh": profile.get("notes_zh", profile.get("notes", "")),
                "measurement_status": "NOT_BENCHMARKED_DRAFT_ONLY",
                "production_claim": False,
                "customer_pilot_claim": False,
                "benchmark_required_before_use": profile_id != "SIZE-LOCAL-TRIAL",
            }
        )
    return normalized


def observed_precheck(precheck: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": precheck["status"],
        "passed_count": sum(1 for item in precheck["checks"] if item.get("passed") is True),
        "required_count": len(precheck["checks"]),
        "checks": [
            {
                "id": item["id"],
                "name": item.get("name", ""),
                "passed": item.get("passed") is True,
                "observed": item.get("observed", ""),
            }
            for item in precheck["checks"]
        ],
        "boundaries": precheck.get("boundaries", {}),
    }


def render_markdown(report: dict[str, Any]) -> str:
    profile_lines = "\n".join(
        (
            f"- {item['id']}: {item['purpose_zh']} / CPU {item['cpu']} / 内存 {item['memory']} / "
            f"磁盘 {item['disk']} / 状态：{item['measurement_status']} / 说明：{item['source_notes_zh']}"
        )
        for item in report["sizing_profiles"]
    )
    precheck_lines = "\n".join(
        f"- {item['id']}: {item['name']} = {'PASS' if item['passed'] else 'HOLD'} ({item['observed']})"
        for item in report["observed_precheck"]["checks"]
    )
    assumption_lines = "\n".join(f"- {item}" for item in report["assumptions"])
    caveat_lines = "\n".join(f"- {item}" for item in report["non_production_caveats"])
    action_lines = "\n".join(
        f"- {item['id']}: {item['title_zh']} -> {item['suggested_goal']}" for item in report["follow_up_actions"]
    )

    return f"""# SecuPilot 私有化部署 Sizing 报告

Report ID: `{report['report_id']}`

Package ID: `{report['package_id']}`

Status: `{report['status']}`

## 一句话结论

{report['summary']}

## 本机 Precheck 结果

{precheck_lines}

## Sizing 档位

{profile_lines}

## 假设条件

{assumption_lines}

## 非生产 Caveat

{caveat_lines}

## 后续动作

{action_lines}

## 边界

- 本报告不执行部署。
- 本报告不做生产 benchmark。
- 本报告不声明客户试点或生产规格。
- 本报告不调用 live Qwen/API。
- 本报告不连接 live connector。
- 本报告不读取、保存或要求 secret/token/auth header。
- 本报告不使用真实数据或脱敏真实数据。
"""


def build_report(
    *,
    package_dir: Path,
    draft_json: Path,
    precheck_json: Path,
    output_dir: Path,
    repo_root: Path,
) -> dict[str, Any]:
    assert_inside_repo(package_dir, repo_root)
    assert_inside_repo(draft_json, repo_root)
    assert_inside_repo(precheck_json, repo_root)
    assert_inside_repo(output_dir, repo_root)
    if not draft_json.exists():
        raise ValueError(f"prereq/sizing draft not found: {draft_json}")
    if not precheck_json.exists():
        raise ValueError(f"precheck result not found: {precheck_json}")

    draft = read_json(draft_json)
    precheck = read_json(precheck_json)
    validate_inputs(draft, precheck)
    package_id = str(draft.get("package_id", ""))
    if not package_id:
        raise ValueError("package_id missing from draft")
    report_id = f"{package_id}-private-deployment-sizing-report"
    json_path = output_dir / DEFAULT_JSON_NAME
    md_path = output_dir / DEFAULT_MD_NAME
    report = {
        "schema_version": SCHEMA_VERSION,
        "report_id": report_id,
        "generated_at_utc": utc_now(),
        "package_id": package_id,
        "package_dir": portable_path(package_dir, repo_root),
        "status": "SIZING_DRAFT_READY_NOT_BENCHMARKED",
        "summary": "本地 precheck 已通过；当前 sizing 仅为私有化试用与实验室 dry-run 草案，不是生产 benchmark 或客户试点规格。",
        "inputs": {
            "prereq_sizing_draft": portable_path(draft_json, repo_root),
            "precheck_result": portable_path(precheck_json, repo_root),
        },
        "observed_precheck": observed_precheck(precheck),
        "sizing_profiles": normalize_profiles(draft["resource_sizing"]["profiles"]),
        "assumptions": [
            "当前仅覆盖 local/offline private deployment package 与报告生成链路。",
            "local trial 档位只用于打开包、运行本地脚本、查看报告和截图。",
            "lab dry-run 档位仍需后续 benchmark 才能用于客户试点或生产 sizing 判断。",
            "production 档位保持 TBD，不在本 Goal 内授权或声明。",
        ],
        "non_production_caveats": [
            "Not a production benchmark.",
            "Not a customer pilot sizing claim.",
            "Not a deployment authorization.",
            "No live Qwen/API/connectors were used.",
            "No real or masked-real data was used.",
        ],
        "follow_up_actions": [
            {
                "id": "ACTION-01",
                "title": "Build benchmark dry-run harness for lab profile",
                "title_zh": "为实验室档位制作 benchmark dry-run harness",
                "suggested_goal": "GOAL-MVP-80_MODEL_PROVIDER_SETUP_FLOW_DRY_RUN",
            },
            {
                "id": "ACTION-02",
                "title": "Refresh private package readme with precheck and sizing report",
                "title_zh": "把 precheck 与 sizing report 汇入私有化包入口说明",
                "suggested_goal": "GOAL-MVP-81_PRIVATE_DEPLOYMENT_PACKAGE_REFRESH_WITH_PRECHECK",
            },
        ],
        "non_authorization": [
            "No deployment executed",
            "No production benchmark",
            "No customer pilot sizing claim",
            "No live Qwen/API/connectors",
            "No network request",
            "No production write-back",
            "No customer-visible publish/deploy",
            "No real or masked-real data",
            "No secrets, tokens, auth headers, or raw customer logs",
        ],
        "next_unlock": "GOAL-MVP-80_MODEL_PROVIDER_SETUP_FLOW_DRY_RUN",
    }
    report["outputs"] = {
        "json": portable_path(json_path, repo_root),
        "markdown": portable_path(md_path, repo_root),
    }
    scan_value(report, label="sizing_report")
    md_text = render_markdown(report)
    scan_value(md_text, label=DEFAULT_MD_NAME)
    write_json(json_path, report)
    write_text(md_path, md_text)
    return report


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", required=True, type=Path)
    parser.add_argument("--draft-json", required=True, type=Path)
    parser.add_argument("--precheck-json", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    args = parser.parse_args(argv)

    output_dir = args.output_dir or args.package_dir / "trial_output"
    try:
        report = build_report(
            package_dir=args.package_dir,
            draft_json=args.draft_json,
            precheck_json=args.precheck_json,
            output_dir=output_dir,
            repo_root=args.repo_root,
        )
    except Exception as exc:  # noqa: BLE001 - CLI converts sizing violations to HOLD.
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    print(json.dumps({"status": "PASS", "report": report}, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
