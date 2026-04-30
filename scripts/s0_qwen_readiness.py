#!/usr/bin/env python3
"""S0-002 local readiness and artifact validation utilities.

This script is deliberately split from the S0 Qwen runner:
- `preflight` is local-only and inspects synthetic QwenFactBundle inputs.
- `artifact-validate` is local-only and checks a run folder shape.
- `healthcheck` only checks the cloud endpoint when explicitly invoked.

It must not connect to real data, connectors, runtime APIs, or production systems.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import s0_qwen_synthetic_run as qwen_runner
from scripts.synthetic_safety_tooling import scan_text_for_hard_stops, validate_qwen_fact_bundle_file


EXPECTED_UAT_IDS = tuple(f"UAT-{index:02d}" for index in range(1, 21))
DEFAULT_PREFLIGHT_JSON = Path("artifacts/s0_qwen_runs/2026-04-30-002/preflight/s0_002_preflight.json")
DEFAULT_PREFLIGHT_MD = Path("docs/S6_S0_002_READINESS_PREFLIGHT_REPORT_2026_04_30.md")
DEFAULT_ARTIFACT_CHECKLIST_MD = Path("docs/S6_S0_ARTIFACT_COMPLETENESS_VALIDATOR_CHECKLIST_2026_04_30.md")
DEFAULT_ENDPOINT = qwen_runner.DEFAULT_ENDPOINT
DEFAULT_MODEL = qwen_runner.DEFAULT_MODEL


@dataclass(frozen=True)
class BundlePreflightRow:
    uat_id: str
    filename: str
    chars: int
    estimated_tokens: int
    synthetic_valid: bool
    budget_valid: bool
    findings: tuple[str, ...]


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} root is not an object")
    return data


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, rows: list[BundlePreflightRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "uat_id",
                "filename",
                "chars",
                "estimated_tokens",
                "synthetic_valid",
                "budget_valid",
                "findings",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "uat_id": row.uat_id,
                    "filename": row.filename,
                    "chars": row.chars,
                    "estimated_tokens": row.estimated_tokens,
                    "synthetic_valid": row.synthetic_valid,
                    "budget_valid": row.budget_valid,
                    "findings": "; ".join(row.findings),
                }
            )


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    table = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        table.append("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |")
    return "\n".join(table)


def _preflight_rows(bundle_dir: Path, *, max_input_chars: int, max_input_tokens_estimate: int) -> tuple[list[BundlePreflightRow], list[str]]:
    rows: list[BundlePreflightRow] = []
    global_findings: list[str] = []
    paths = sorted(bundle_dir.glob("*.json"))
    if len(paths) != 20:
        global_findings.append(f"bundle_count_expected_20_actual_{len(paths)}")

    seen_ids: set[str] = set()
    for path in paths:
        findings: list[str] = []
        try:
            bundle = _read_json(path)
            uat_id = str(bundle.get("uat_id", "UNKNOWN"))
        except Exception as exc:  # noqa: BLE001 - convert malformed local input to HOLD evidence.
            rows.append(
                BundlePreflightRow(
                    uat_id="UNKNOWN",
                    filename=path.name,
                    chars=0,
                    estimated_tokens=0,
                    synthetic_valid=False,
                    budget_valid=False,
                    findings=(f"json_read_failed:{type(exc).__name__}:{exc}",),
                )
            )
            continue

        if uat_id in seen_ids:
            findings.append(f"duplicate_uat_id:{uat_id}")
        seen_ids.add(uat_id)

        validation = validate_qwen_fact_bundle_file(path)
        synthetic_valid = validation.valid
        findings.extend(validation.errors)

        messages = qwen_runner._build_messages(bundle)
        prompt_text = "\n".join(message["content"] for message in messages)
        chars = len(prompt_text)
        estimated_tokens = qwen_runner._estimate_tokens(prompt_text)
        budget_valid = True
        try:
            qwen_runner._validate_prompt_budget(
                messages,
                max_input_chars=max_input_chars,
                max_input_tokens_estimate=max_input_tokens_estimate,
            )
        except ValueError as exc:
            budget_valid = False
            findings.append(str(exc))

        rows.append(
            BundlePreflightRow(
                uat_id=uat_id,
                filename=path.name,
                chars=chars,
                estimated_tokens=estimated_tokens,
                synthetic_valid=synthetic_valid,
                budget_valid=budget_valid,
                findings=tuple(findings),
            )
        )

    missing_ids = sorted(set(EXPECTED_UAT_IDS) - seen_ids)
    extra_ids = sorted(seen_ids - set(EXPECTED_UAT_IDS))
    for uat_id in missing_ids:
        global_findings.append(f"missing_uat_id:{uat_id}")
    for uat_id in extra_ids:
        global_findings.append(f"unexpected_uat_id:{uat_id}")
    return rows, global_findings


def run_preflight(args: argparse.Namespace) -> int:
    rows, global_findings = _preflight_rows(
        args.bundle_dir,
        max_input_chars=args.max_input_chars,
        max_input_tokens_estimate=args.max_input_tokens_estimate,
    )
    all_rows_valid = all(row.synthetic_valid and row.budget_valid and not row.findings for row in rows)
    decision = "S0_002_PREFLIGHT_PASS_WAITING_FOR_CLOUD_RECOVERY" if all_rows_valid and not global_findings else "HOLD_PREFLIGHT_FAILURE"

    prompt_stats = {
        "count": len(rows),
        "max_chars": max((row.chars for row in rows), default=0),
        "max_estimated_tokens": max((row.estimated_tokens for row in rows), default=0),
        "over_max_input_chars": sum(1 for row in rows if row.chars > args.max_input_chars),
        "over_max_input_tokens_estimate": sum(1 for row in rows if row.estimated_tokens > args.max_input_tokens_estimate),
    }
    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "bundle_dir": str(args.bundle_dir),
        "expected_uat_ids": list(EXPECTED_UAT_IDS),
        "prompt_budget": {
            "max_input_chars": args.max_input_chars,
            "max_input_tokens_estimate": args.max_input_tokens_estimate,
        },
        "prompt_stats": prompt_stats,
        "global_findings": global_findings,
        "rows": [
            {
                "uat_id": row.uat_id,
                "filename": row.filename,
                "chars": row.chars,
                "estimated_tokens": row.estimated_tokens,
                "synthetic_valid": row.synthetic_valid,
                "budget_valid": row.budget_valid,
                "findings": list(row.findings),
            }
            for row in rows
        ],
        "s0_002_rerun_status": "NOT_STARTED_WAITING_FOR_CLOUD_RECOVERY_EVIDENCE",
        "required_cloud_recovery_evidence": [
            "EngineCore alive",
            "/v1/models available",
            "minimal synthetic chat completion succeeds",
        ],
    }

    _write_json(args.output_json, payload)
    _write_csv(args.output_json.with_suffix(".csv"), rows)
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(_preflight_markdown(payload), encoding="utf-8")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if decision.startswith("S0_002_PREFLIGHT_PASS") else 1


def _preflight_markdown(payload: dict[str, Any]) -> str:
    rows = payload["rows"]
    table_rows = [
        [
            row["uat_id"],
            row["filename"],
            str(row["chars"]),
            str(row["estimated_tokens"]),
            "YES" if row["synthetic_valid"] else "NO",
            "YES" if row["budget_valid"] else "NO",
            "; ".join(row["findings"]) if row["findings"] else "none",
        ]
        for row in rows
    ]
    return (
        "# S6 S0-002 Readiness Preflight Report 2026-04-30\n\n"
        "## 1. Decision\n\n"
        "```text\n"
        f"{payload['decision']}\n"
        "S0_002_RERUN_STATUS = NOT_STARTED_WAITING_FOR_CLOUD_RECOVERY_EVIDENCE\n"
        "```\n\n"
        "## 2. Scope\n\n"
        "- Input: current 20 repo-local synthetic QwenFactBundle files only.\n"
        "- Real data: NO.\n"
        "- Masked real data: NO.\n"
        "- Qwen execution: NO.\n"
        "- Backend/runtime/API/schema changes: NO.\n\n"
        "## 3. Prompt Budget Summary\n\n"
        + _markdown_table(
            ["Metric", "Value"],
            [
                ["bundle count", str(payload["prompt_stats"]["count"])],
                ["max chars", str(payload["prompt_stats"]["max_chars"])],
                ["max estimated tokens", str(payload["prompt_stats"]["max_estimated_tokens"])],
                ["max input chars limit", str(payload["prompt_budget"]["max_input_chars"])],
                ["max input token estimate limit", str(payload["prompt_budget"]["max_input_tokens_estimate"])],
                ["over char limit", str(payload["prompt_stats"]["over_max_input_chars"])],
                ["over token estimate limit", str(payload["prompt_stats"]["over_max_input_tokens_estimate"])],
            ],
        )
        + "\n\n"
        "## 4. Cloud Recovery Gate\n\n"
        "S0-002 must not run until all three non-secret cloud recovery checks are true:\n\n"
        "- EngineCore alive.\n"
        "- `/v1/models` available.\n"
        "- Minimal synthetic chat completion succeeds.\n\n"
        "## 5. Per-Bundle Preflight\n\n"
        + _markdown_table(
            ["UAT", "File", "Chars", "Est tokens", "Synthetic", "Budget", "Findings"],
            table_rows,
        )
        + "\n\n"
        "## 6. Non-Authorization\n\n"
        "This report does not authorize real data, masked real data, closed shadow, customer-visible staging or demo, "
        "backend/runtime/API/schema, connector changes, secrets, deploy, external pilot, launch, or autonomous action.\n"
    )


def _required_artifact_paths(run_dir: Path) -> list[Path]:
    paths = [
        run_dir / "manifest.json",
        run_dir / "scoring" / "s0_scorecard.csv",
        run_dir / "scoring" / "action_command_scan.csv",
        run_dir / "scoring" / "prompt_injection_verdicts.csv",
        run_dir / "metrics" / "latency_summary.json",
        run_dir / "notes" / "operator_notes.md",
        run_dir / "notes" / "reviewer_notes.md",
    ]
    paths.extend(run_dir / "outputs" / f"{uat_id}.json" for uat_id in EXPECTED_UAT_IDS)
    return paths


def run_artifact_validate(args: argparse.Namespace) -> int:
    missing = [str(path) for path in _required_artifact_paths(args.run_dir) if not path.exists()]
    hard_stop_findings: list[dict[str, str]] = []
    scanned_files = 0
    for path in sorted(args.run_dir.rglob("*")) if args.run_dir.exists() else []:
        if path.is_file() and path.suffix.lower() in {".json", ".csv", ".md", ".txt"}:
            scanned_files += 1
            scan = scan_text_for_hard_stops(path.read_text(encoding="utf-8", errors="replace"))
            for finding in scan.findings:
                if not finding.safe_listed:
                    hard_stop_findings.append({"file": str(path), "label": finding.label})

    decision = "S0_ARTIFACT_COMPLETENESS_PASS" if not missing and not hard_stop_findings else "HOLD_ARTIFACT_COMPLETENESS_FAILURE"
    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "run_dir": str(args.run_dir),
        "missing": missing,
        "scanned_files": scanned_files,
        "hard_stop_findings": hard_stop_findings,
        "required_paths": [str(path) for path in _required_artifact_paths(args.run_dir)],
    }
    if args.output_json:
        _write_json(args.output_json, payload)
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(_artifact_markdown(payload), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if decision.endswith("_PASS") else 1


def _artifact_markdown(payload: dict[str, Any]) -> str:
    missing_rows = [[item] for item in payload["missing"]] or [["none"]]
    finding_rows = [[finding["file"], finding["label"]] for finding in payload["hard_stop_findings"]] or [["none", "none"]]
    return (
        "# S6 S0 Artifact Completeness Validator Checklist 2026-04-30\n\n"
        "## 1. Decision\n\n"
        "```text\n"
        f"{payload['decision']}\n"
        "```\n\n"
        "## 2. Required Artifact Shape\n\n"
        "A completed S0 run folder must include manifest, output, scoring, metrics, operator notes, and reviewer notes.\n"
        "For S0-002, the expected root is `artifacts/s0_qwen_runs/2026-04-30-002/`.\n\n"
        "## 3. Current Validation Target\n\n"
        f"- Run dir: `{payload['run_dir']}`\n"
        f"- Scanned files: `{payload['scanned_files']}`\n\n"
        "## 4. Missing Paths\n\n"
        + _markdown_table(["Missing path"], missing_rows)
        + "\n\n"
        "## 5. Hard-Stop Findings\n\n"
        + _markdown_table(["File", "Finding"], finding_rows)
        + "\n\n"
        "## 6. Non-Authorization\n\n"
        "This checklist does not authorize Qwen execution, real data, masked real data, customer-visible staging, "
        "backend/runtime/API/schema, connector changes, secrets, deploy, external pilot, launch, or autonomous action.\n"
    )


def _get_json(url: str, *, timeout: int) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{url} did not return a JSON object")
    return data


def _post_json(url: str, payload: dict[str, Any], *, timeout: int) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{url} did not return a JSON object")
    return data


def run_healthcheck(args: argparse.Namespace) -> int:
    endpoint = args.endpoint.rstrip("/")
    checks: list[dict[str, Any]] = []
    started = time.perf_counter()
    try:
        models = _get_json(f"{endpoint}/models", timeout=args.timeout)
        checks.append({"name": "models", "pass": True, "detail": f"models_count={len(models.get('data', [])) if isinstance(models.get('data'), list) else 'unknown'}"})
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        checks.append({"name": "models", "pass": False, "detail": f"{type(exc).__name__}:{exc}"})

    if args.run_chat_check:
        payload = {
            "model": args.model,
            "messages": [
                {"role": "system", "content": "Synthetic healthcheck only. Return JSON only."},
                {"role": "user", "content": "{\"task\":\"healthcheck\",\"synthetic_only\":true}"},
            ],
            "max_tokens": 64,
            "temperature": 0.0,
            "top_p": 1.0,
        }
        try:
            response = _post_json(f"{endpoint}/chat/completions", payload, timeout=args.request_timeout)
            checks.append({"name": "minimal_chat_completion", "pass": True, "detail": "choices_present" if response.get("choices") else "choices_missing"})
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
            checks.append({"name": "minimal_chat_completion", "pass": False, "detail": f"{type(exc).__name__}:{exc}"})

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    decision = "QWEN_RUNTIME_HEALTHCHECK_PASS" if checks and all(check["pass"] for check in checks) else "HOLD_QWEN_RUNTIME_HEALTHCHECK_FAILURE"
    payload = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "endpoint": endpoint,
        "model": args.model,
        "elapsed_ms": elapsed_ms,
        "checks": checks,
        "real_data_used": False,
        "masked_real_data_used": False,
        "customer_visible_output": False,
    }
    if args.output_json:
        _write_json(args.output_json, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if decision.endswith("_PASS") else 1


def _main() -> int:
    parser = argparse.ArgumentParser(description="S0 Qwen readiness helpers")
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight", help="local-only synthetic bundle preflight")
    preflight.add_argument("--bundle-dir", type=Path, default=qwen_runner.DEFAULT_BUNDLE_DIR)
    preflight.add_argument("--max-input-chars", type=int, default=qwen_runner.DEFAULT_MAX_INPUT_CHARS)
    preflight.add_argument("--max-input-tokens-estimate", type=int, default=qwen_runner.DEFAULT_MAX_INPUT_TOKENS_ESTIMATE)
    preflight.add_argument("--output-json", type=Path, default=DEFAULT_PREFLIGHT_JSON)
    preflight.add_argument("--output-md", type=Path, default=DEFAULT_PREFLIGHT_MD)
    preflight.set_defaults(func=run_preflight)

    artifact = subparsers.add_parser("artifact-validate", help="local-only S0 run artifact completeness validation")
    artifact.add_argument("--run-dir", type=Path, required=True)
    artifact.add_argument("--output-json", type=Path)
    artifact.add_argument("--output-md", type=Path, default=DEFAULT_ARTIFACT_CHECKLIST_MD)
    artifact.set_defaults(func=run_artifact_validate)

    healthcheck = subparsers.add_parser("healthcheck", help="explicit cloud Qwen runtime healthcheck")
    healthcheck.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    healthcheck.add_argument("--model", default=DEFAULT_MODEL)
    healthcheck.add_argument("--timeout", type=int, default=10)
    healthcheck.add_argument("--request-timeout", type=int, default=60)
    healthcheck.add_argument("--run-chat-check", action="store_true")
    healthcheck.add_argument("--output-json", type=Path)
    healthcheck.set_defaults(func=run_healthcheck)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(_main())
