#!/usr/bin/env python3
"""Check private-preview local/offline readiness before internal trial review."""

from __future__ import annotations

import argparse
import json
import re
import sys
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

FINAL_STATUS_FALSE_KEYS = (
    "customer_visible_output",
    "production_connectors",
    "qwen_autonomous_action",
    "raw_payload_retention",
    "secret_retention",
    "writeback",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_path(value: str | Path) -> str:
    return str(value).replace("\\", "/").strip().rstrip("/")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def add_finding(findings: list[dict[str, str]], label: str, detail: str) -> None:
    findings.append({"label": label, "detail": detail})


def check_false_keys(
    findings: list[dict[str, str]],
    source_name: str,
    payload: dict[str, Any],
    *,
    key: str,
    expected_false_keys: tuple[str, ...],
) -> None:
    boundaries = payload.get(key)
    if not isinstance(boundaries, dict):
        add_finding(findings, "missing_boundary_block", f"{source_name}:{key}")
        return
    for boundary_key in expected_false_keys:
        if boundaries.get(boundary_key) is not False:
            add_finding(
                findings,
                "boundary_not_false",
                f"{source_name}:{boundary_key}={boundaries.get(boundary_key)!r}",
            )


def extract_rc_triplet(package_slug: str) -> str | None:
    match = re.search(r"rc-(\d{3})", package_slug, flags=re.IGNORECASE)
    if not match:
        return None
    return match.group(1)


def resolve_launch_info_path(package_dir: Path, launch_info_arg: str | None) -> Path:
    if launch_info_arg:
        return Path(launch_info_arg)
    rc_triplet = extract_rc_triplet(package_dir.name)
    if not rc_triplet:
        return Path("artifacts/local_trial_launches/UNKNOWN/launch_info.json")
    return Path("artifacts") / "local_trial_launches" / f"local-offline-trial-rc-{rc_triplet}" / "launch_info.json"


def check_local_offline_text(findings: list[dict[str, str]], source_name: str, text: str) -> None:
    normalized = text.lower()
    if ("local/offline" not in normalized) and ("本地" not in text or "离线" not in text):
        add_finding(findings, "local_offline_text_missing", source_name)


def validate(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    package_dir = (repo_root / args.package_dir).resolve() if not Path(args.package_dir).is_absolute() else Path(args.package_dir).resolve()
    route_map_path = (repo_root / args.route_map).resolve() if not Path(args.route_map).is_absolute() else Path(args.route_map).resolve()
    launch_info_path = resolve_launch_info_path(package_dir, args.launch_info)
    if not launch_info_path.is_absolute():
        launch_info_path = (repo_root / launch_info_path).resolve()

    findings: list[dict[str, str]] = []
    package_manifest: dict[str, Any] | None = None
    final_status: dict[str, Any] | None = None
    route_map: dict[str, Any] | None = None
    launch_info: dict[str, Any] | None = None

    if not package_dir.exists():
        add_finding(findings, "package_dir_missing", normalize_path(args.package_dir))

    manifest_path = package_dir / "package_manifest.json"
    if not manifest_path.exists():
        add_finding(findings, "package_manifest_missing", normalize_path(manifest_path))
    else:
        try:
            payload = read_json(manifest_path)
            if not isinstance(payload, dict):
                add_finding(findings, "package_manifest_not_object", normalize_path(manifest_path))
            else:
                package_manifest = payload
        except Exception as exc:  # noqa: BLE001
            add_finding(findings, "package_manifest_invalid_json", str(exc))

    final_status_path = package_dir / "evidence" / "final_status.json"
    if not final_status_path.exists():
        add_finding(findings, "final_status_missing", normalize_path(final_status_path))
    else:
        try:
            payload = read_json(final_status_path)
            if not isinstance(payload, dict):
                add_finding(findings, "final_status_not_object", normalize_path(final_status_path))
            else:
                final_status = payload
        except Exception as exc:  # noqa: BLE001
            add_finding(findings, "final_status_invalid_json", str(exc))

    start_here_path = package_dir / "REVIEWER_START_HERE_中文.md"
    if not start_here_path.exists():
        add_finding(findings, "reviewer_start_here_missing", normalize_path(start_here_path))
    else:
        text = start_here_path.read_text(encoding="utf-8")
        check_local_offline_text(findings, "REVIEWER_START_HERE_中文.md", text)

    if not route_map_path.exists():
        add_finding(findings, "route_map_missing", normalize_path(args.route_map))
    else:
        try:
            payload = read_json(route_map_path)
            if not isinstance(payload, dict):
                add_finding(findings, "route_map_not_object", normalize_path(route_map_path))
            else:
                route_map = payload
        except Exception as exc:  # noqa: BLE001
            add_finding(findings, "route_map_invalid_json", str(exc))

    if not launch_info_path.exists():
        add_finding(findings, "launch_info_missing", normalize_path(launch_info_path))
    else:
        try:
            payload = read_json(launch_info_path)
            if not isinstance(payload, dict):
                add_finding(findings, "launch_info_not_object", normalize_path(launch_info_path))
            else:
                launch_info = payload
        except Exception as exc:  # noqa: BLE001
            add_finding(findings, "launch_info_invalid_json", str(exc))

    if package_manifest:
        expected_package_dir = normalize_path(args.package_dir)
        actual_package_dir = normalize_path(package_manifest.get("package_dir", ""))
        if actual_package_dir != expected_package_dir:
            add_finding(
                findings,
                "package_manifest_package_dir_mismatch",
                f"actual={actual_package_dir!r}; expected={expected_package_dir!r}",
            )
        check_false_keys(
            findings,
            "package_manifest.json",
            package_manifest,
            key="boundaries",
            expected_false_keys=BOUNDARY_FALSE_KEYS,
        )

    if final_status:
        if final_status.get("can_deploy_to_customer_production") is not False:
            add_finding(
                findings,
                "final_status_deploy_gate_not_false",
                f"value={final_status.get('can_deploy_to_customer_production')!r}",
            )
        check_false_keys(
            findings,
            "evidence/final_status.json",
            final_status,
            key="boundaries_preserved",
            expected_false_keys=FINAL_STATUS_FALSE_KEYS,
        )

    if route_map:
        route_entries = route_map.get("route_entries")
        if not isinstance(route_entries, list) or not route_entries:
            add_finding(findings, "route_map_entries_missing", normalize_path(route_map_path))
        check_false_keys(
            findings,
            "route_map_index.json",
            route_map,
            key="boundaries",
            expected_false_keys=BOUNDARY_FALSE_KEYS,
        )
        non_auth = route_map.get("non_authorization")
        if not isinstance(non_auth, dict):
            add_finding(findings, "route_map_non_authorization_missing", normalize_path(route_map_path))
        else:
            for key in ("customer_visible_or_deploy_go", "live_qwen_api", "production_writeback"):
                if non_auth.get(key) is not False:
                    add_finding(findings, "route_map_non_authorization_not_false", f"{key}={non_auth.get(key)!r}")

    if launch_info:
        check_false_keys(
            findings,
            "launch_info.json",
            launch_info,
            key="boundaries",
            expected_false_keys=BOUNDARY_FALSE_KEYS,
        )
        operator_notice = str(launch_info.get("operator_notice", ""))
        check_local_offline_text(findings, "launch_info.operator_notice", operator_notice)
        if launch_info.get("server_started") not in (False, None):
            add_finding(findings, "launch_info_server_started_true", f"value={launch_info.get('server_started')!r}")

    status = "PASS" if not findings else "HOLD"
    payload = {
        "schema_version": "secupilot.private_preview.healthcheck.v1",
        "generated_at_utc": utc_now(),
        "status": status,
        "package_dir": normalize_path(args.package_dir),
        "route_map": normalize_path(args.route_map),
        "launch_info": normalize_path(args.launch_info) if args.launch_info else normalize_path(launch_info_path),
        "blocking_finding_count": len(findings),
        "blocking_findings": findings,
        "hard_boundaries": {key: False for key in BOUNDARY_FALSE_KEYS},
    }
    return payload


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate private-preview local/offline package + route map + launch metadata readiness."
    )
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--route-map", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--launch-info")
    args = parser.parse_args(argv)

    payload = validate(args)
    output_path = Path(args.output_json)
    if not output_path.is_absolute():
        output_path = (Path(args.repo_root).resolve() / output_path).resolve()
    write_json(output_path, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return PASS if payload["status"] == "PASS" else HOLD


if __name__ == "__main__":
    sys.exit(run())
