#!/usr/bin/env python3
"""Validate ECI/VFE analyzer outputs for schema and safety boundaries."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PASS = 0
HOLD = 20

FORBIDDEN_CONTENT_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"authorization\s*:",
        r"bearer\s+[A-Za-z0-9._~+/=-]{8,}",
        r"api[_-]?key\s*[:=]",
        r"access[_-]?token\s*[:=]",
        r"private[_-]?key",
        r"raw[_-]?payload",
        r"raw[_-]?evidence",
        r"exploit\s+step",
        r"\bpoc\b",
        r"attacker-readable",
    )
)

PROMPT_INJECTION_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"ignore\s+previous\s+instructions",
        r"disregard\s+security\s+policy",
        r"drop\s+table",
        r"rm\s+-rf",
        r"<script",
    )
)

TOPOLOGY_TERMS = (
    "reachability",
    "reachable",
    "open port",
    "lateral path",
    "pivot path",
    "control channel",
)

REQUIRED_GAP_FIELDS = (
    "gap",
    "why_it_matters",
    "recommended_query_type",
    "allowed_scope",
    "urgency",
    "window_closes_in",
    "deadline_basis",
    "fallback_if_missed",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def flatten_strings(payload: Any) -> list[str]:
    values: list[str] = []
    if isinstance(payload, str):
        values.append(payload)
    elif isinstance(payload, dict):
        for value in payload.values():
            values.extend(flatten_strings(value))
    elif isinstance(payload, list):
        for item in payload:
            values.extend(flatten_strings(item))
    return values


def find_private_ip(text: str) -> bool:
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    for token in ip_pattern.findall(text):
        try:
            addr = ipaddress.ip_address(token)
        except ValueError:
            continue
        if addr.is_private:
            return True
    return False


def check_required_files(input_dir: Path) -> dict[str, Path]:
    files = {
        "chain_assessment": input_dir / "chain_assessment.json",
        "forecast_candidates": input_dir / "forecast_candidates.json",
        "correlation_result": input_dir / "correlation_result.json",
        "run_record": input_dir / "run_record.json",
    }
    missing = [name for name, path in files.items() if not path.exists()]
    if missing:
        raise ValueError(f"missing required analyzer outputs: {', '.join(missing)}")
    return files


def validate_chain(chain: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    if chain.get("schema_version") != "eci_vfe.v0.2":
        findings.append({"severity": "P1", "type": "schema", "message": "chain_assessment schema_version mismatch"})

    assessments = chain.get("assessments")
    if not isinstance(assessments, list) or not assessments:
        findings.append({"severity": "P1", "type": "schema", "message": "chain_assessment assessments missing"})
        return

    high_stage_labels = {
        "LATERAL_MOVEMENT_SUSPECTED",
        "HIGH_STAGE_SUSPECTED_SHORT_OBSERVATION",
        "IMMEDIATE_HUMAN_CONFIRMATION_REQUIRED",
    }

    for index, assessment in enumerate(assessments):
        case_ref = f"assessment[{index}]"
        for key in ("stage_label", "stage_number", "stage_status", "confidence", "evidence_gaps"):
            if key not in assessment:
                findings.append({"severity": "P1", "type": "schema", "message": f"{case_ref} missing {key}"})

        stage_number = assessment.get("stage_number", {}).get("value")
        stage_status = assessment.get("stage_status", {}).get("value")
        confidence = assessment.get("confidence", {}).get("value")
        if isinstance(stage_number, (int, float)) and stage_number >= 4 and isinstance(confidence, (int, float)):
            if confidence < 0.8 and stage_status not in {
                "HIGH_STAGE_SUSPECTED_SHORT_OBSERVATION",
                "INSUFFICIENT_EVIDENCE_WITH_PRIORITY_GAPS",
            }:
                findings.append(
                    {
                        "severity": "P1",
                        "type": "high_stage_guard",
                        "message": f"{case_ref} high-stage label below threshold without suspected-state downgrade",
                    }
                )
        if stage_status in high_stage_labels and stage_number in {1, 2}:
            findings.append(
                {
                    "severity": "P2",
                    "type": "stage_consistency",
                    "message": f"{case_ref} high-stage status with low stage number",
                }
            )

        gaps = assessment.get("evidence_gaps")
        if not isinstance(gaps, list) or not gaps:
            findings.append({"severity": "P1", "type": "evidence_gap", "message": f"{case_ref} evidence_gaps missing"})
            continue
        for gap_index, gap in enumerate(gaps):
            if not isinstance(gap, dict):
                findings.append(
                    {
                        "severity": "P1",
                        "type": "evidence_gap",
                        "message": f"{case_ref}.evidence_gaps[{gap_index}] not an object",
                    }
                )
                continue
            for field in REQUIRED_GAP_FIELDS:
                if field not in gap or gap.get(field) in (None, ""):
                    findings.append(
                        {
                            "severity": "P1",
                            "type": "evidence_gap",
                            "message": f"{case_ref}.evidence_gaps[{gap_index}] missing {field}",
                        }
                    )
            if gap.get("allowed_scope") != "metadata_only":
                findings.append(
                    {
                        "severity": "P1",
                        "type": "evidence_gap",
                        "message": f"{case_ref}.evidence_gaps[{gap_index}] allowed_scope must be metadata_only",
                    }
                )


def validate_forecast(forecast_payload: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    if forecast_payload.get("schema_version") != "eci_vfe.v0.2":
        findings.append({"severity": "P1", "type": "schema", "message": "forecast_candidates schema_version mismatch"})

    candidates = forecast_payload.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        findings.append({"severity": "P1", "type": "schema", "message": "forecast_candidates candidates missing"})
        return

    for index, candidate in enumerate(candidates):
        ref = f"candidate[{index}]"
        context = candidate.get("query_context")
        if not isinstance(context, dict):
            findings.append({"severity": "P1", "type": "query_context", "message": f"{ref} query_context missing"})
            continue

        if context.get("bulk_export") is not False:
            findings.append({"severity": "P1", "type": "query_context", "message": f"{ref} bulk_export=true passes"})
        if context.get("audit_required") is not True:
            findings.append({"severity": "P1", "type": "query_context", "message": f"{ref} audit_required not true"})
        if context.get("asset_scope") == "bulk":
            findings.append({"severity": "P1", "type": "query_context", "message": f"{ref} asset_scope bulk is forbidden"})

        gaps = candidate.get("evidence_gaps")
        if not isinstance(gaps, list) or not gaps:
            findings.append({"severity": "P1", "type": "evidence_gap", "message": f"{ref} evidence_gaps missing"})


def validate_correlation(correlation_payload: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    if correlation_payload.get("schema_version") != "eci_vfe.v0.2":
        findings.append({"severity": "P1", "type": "schema", "message": "correlation_result schema_version mismatch"})

    correlations = correlation_payload.get("correlations")
    if not isinstance(correlations, list) or not correlations:
        findings.append({"severity": "P1", "type": "schema", "message": "correlation_result correlations missing"})
        return

    for index, correlation in enumerate(correlations):
        ref = f"correlation[{index}]"
        hard_match = bool(correlation.get("hard_match"))
        fuzzy_match = bool(correlation.get("bounded_fuzzy_match"))
        semantic = bool(correlation.get("semantic_supporting_signal"))
        upgrade = correlation.get("case_upgrade_allowed")

        if semantic and not hard_match and not fuzzy_match and upgrade is not False:
            findings.append(
                {
                    "severity": "P1",
                    "type": "correlation_guard",
                    "message": f"{ref} semantic similarity alone upgrades a case",
                }
            )
        if correlation.get("case_upgrade_allowed") is not False:
            findings.append(
                {
                    "severity": "P1",
                    "type": "correlation_guard",
                    "message": f"{ref} case_upgrade_allowed must be false",
                }
            )


def scan_forbidden_content(payloads: list[dict[str, Any]], findings: list[dict[str, Any]]) -> None:
    for payload in payloads:
        for text in flatten_strings(payload):
            lowered = text.lower()
            for pattern in FORBIDDEN_CONTENT_PATTERNS:
                if pattern.search(text):
                    findings.append(
                        {
                            "severity": "P1",
                            "type": "forbidden_content",
                            "message": f"forbidden content passes: pattern={pattern.pattern}",
                        }
                    )
                    break
            for pattern in PROMPT_INJECTION_PATTERNS:
                if pattern.search(text):
                    findings.append(
                        {
                            "severity": "P1",
                            "type": "prompt_injection",
                            "message": "prompt injection text propagates into narrative, watch_for, or remediation",
                        }
                    )
                    break
            if find_private_ip(lowered) and any(term in lowered for term in TOPOLOGY_TERMS):
                findings.append(
                    {
                        "severity": "P1",
                        "type": "topology_disclosure",
                        "message": "private CIDR plus reachability plus port/control semantics passes",
                    }
                )


def build_report(input_dir: Path, findings: list[dict[str, Any]], file_hashes: dict[str, str]) -> dict[str, Any]:
    blocking = [item for item in findings if item.get("severity") in {"P1", "P2"}]
    status = "PASS" if not blocking else "HOLD"
    return {
        "schema_version": "secupilot.eci_vfe.output_guard_scan.v1",
        "generated_at_utc": utc_now(),
        "input_dir": input_dir.as_posix(),
        "status": status,
        "blocking_finding_count": len(blocking),
        "finding_count": len(findings),
        "findings": findings,
        "validated_files": file_hashes,
        "boundaries": {
            "real_data": False,
            "masked_real_data": False,
            "live_qwen_api": False,
            "live_connectors": False,
            "production_writeback": False,
            "customer_visible_output": False,
            "push": False,
        },
    }


def stable_sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_output(input_dir: Path) -> dict[str, Any]:
    files = check_required_files(input_dir)
    payloads = {name: read_json(path) for name, path in files.items()}

    findings: list[dict[str, Any]] = []
    validate_chain(payloads["chain_assessment"], findings)
    validate_forecast(payloads["forecast_candidates"], findings)
    validate_correlation(payloads["correlation_result"], findings)
    scan_forbidden_content(
        [
            payloads["chain_assessment"],
            payloads["forecast_candidates"],
            payloads["correlation_result"],
            payloads["run_record"],
        ],
        findings,
    )

    hashes = {name: stable_sha256(path) for name, path in files.items()}
    report = build_report(input_dir, findings, hashes)
    write_json(input_dir / "output_guard_scan.json", report)
    return report


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = validate_output(args.input.resolve())
    except Exception as exc:
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return PASS if report.get("status") == "PASS" else HOLD


if __name__ == "__main__":
    sys.exit(run())
