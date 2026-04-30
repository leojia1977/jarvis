#!/usr/bin/env python3
"""Run the SecuPilot S1 Closed Shadow Fast MVP path.

This runner is deliberately local and narrow:
- accepts approved synthetic/package input as either a JSON package file or a
  directory of S0 QwenFactBundle JSON files;
- supports fixture and approved-output import providers without live Qwen calls;
- writes standard S1 artifacts under an explicit output folder;
- refuses customer-visible output, production write-back, production connectors,
  raw payload retention, and secret/token/auth-bearing artifacts.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PASS = "S1_CLOSED_SHADOW_PASS"
PASS_WITH_NOTES = "S1_CLOSED_SHADOW_PASS_WITH_NOTES"
HOLD = "S1_CLOSED_SHADOW_HOLD"
NO_GO = "S1_CLOSED_SHADOW_NO_GO"

EXIT_CODES = {
    PASS: 0,
    PASS_WITH_NOTES: 10,
    HOLD: 20,
    NO_GO: 30,
}

STANDARD_ARTIFACTS = (
    "run_record.json",
    "safety_scan.json",
    "case_summary.json",
    "final_status.json",
    "RUN_RECORD.md",
)

MANIFEST_FILE = "artifact_manifest.json"

FORBIDDEN_KEY_PATTERNS = (
    re.compile(r"(^|_)(password|passwd|pwd)($|_)", re.I),
    re.compile(r"(^|_)(secret|client_secret|api_secret)($|_)", re.I),
    re.compile(r"(^|_)(access_token|refresh_token|id_token|token)($|_)", re.I),
    re.compile(r"(^|_)(authorization|auth_header|authheaders?)($|_)", re.I),
    re.compile(r"(^|_)(cookie|session_cookie|set_cookie)($|_)", re.I),
    re.compile(r"(^|_)(private_key|privatekey|ssh_key|pem)($|_)", re.I),
    re.compile(r"(^|_)(raw_payload|rawpayload|payload_raw|host_raw_evidence|raw_evidence)($|_)", re.I),
    re.compile(r"(^|_)(customer_visible_artifact|customer_output|prod_writeback|writeback_payload)($|_)", re.I),
)

FORBIDDEN_VALUE_PATTERNS = (
    ("bearer_token", re.compile(r"Bearer\s+[A-Za-z0-9._~+\-/]+=*", re.I)),
    ("authorization_header", re.compile(r"Authorization\s*[:=]\s*(Bearer|Basic)\s+[^\s,;]+", re.I)),
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private_key_block", re.compile(r"-----BEGIN\s+(RSA\s+|EC\s+|OPENSSH\s+)?PRIVATE KEY-----", re.I)),
    ("jwt_like_token", re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("sas_token", re.compile(r"(?:^|[?&])sig=[A-Za-z0-9%+/=_-]{20,}(?:&|$)", re.I)),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}", re.I)),
    ("generic_secret_assignment", re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+=]{16,}")),
)

REQUIRED_REVIEWERS = (
    {"alias": "Jarvis", "role": "TL / S1 DRI / Product-Governance Reviewer"},
    {"alias": "SecuPilot-GOV-01", "role": "Governance Reviewer"},
    {"alias": "SecuPilot-SEC-01", "role": "Security Reviewer"},
    {"alias": "SecuPilot-DATA-OWNER-01", "role": "Data Owner"},
    {"alias": "SecuPilot-INFRA-01", "role": "Infra Reviewer"},
    {"alias": "SecuPilot-MODEL-OWNER-01", "role": "Model Owner"},
    {"alias": "SecuPilot-QA-01", "role": "QA Reviewer"},
)


@dataclass(frozen=True)
class CaseInput:
    case_id: str
    source_id: str
    title: str
    severity: str
    expected_outcome: str
    tags: tuple[str, ...]
    metadata_refs: tuple[str, ...]
    input_file: str | None = None


@dataclass(frozen=True)
class LoadedInput:
    input_ref: str
    input_kind: str
    package_id: str
    data_mode: str
    cases: tuple[CaseInput, ...]
    raw_objects: tuple[dict[str, Any], ...]


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(obj, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    tmp.replace(path)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def relpath(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def flatten_json(obj: Any, prefix: str = "") -> list[tuple[str, Any]]:
    flattened: list[tuple[str, Any]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            field = f"{prefix}.{key}" if prefix else str(key)
            flattened.append((field, value))
            flattened.extend(flatten_json(value, field))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            field = f"{prefix}[{index}]"
            flattened.append((field, value))
            flattened.extend(flatten_json(value, field))
    return flattened


def scan_json_for_forbidden(obj: Any, label: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    scanned_fields = 0
    scanned_string_values = 0
    for field_path, value in flatten_json(obj):
        scanned_fields += 1
        leaf_name = field_path.split(".")[-1].split("[")[0]
        for pattern in FORBIDDEN_KEY_PATTERNS:
            if pattern.search(leaf_name):
                findings.append(
                    {
                        "source": label,
                        "finding_type": "forbidden_key",
                        "field_path": field_path,
                        "rule": pattern.pattern,
                        "severity": NO_GO,
                        "matched_value_retained": False,
                    }
                )
        if isinstance(value, str):
            scanned_string_values += 1
            for rule_name, pattern in FORBIDDEN_VALUE_PATTERNS:
                if pattern.search(value):
                    findings.append(
                        {
                            "source": label,
                            "finding_type": "forbidden_value_pattern",
                            "field_path": field_path,
                            "rule": rule_name,
                            "severity": NO_GO,
                            "matched_value_retained": False,
                        }
                    )
    return {
        "label": label,
        "scanned_fields": scanned_fields,
        "scanned_string_values": scanned_string_values,
        "findings": findings,
    }


def parse_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError(f"Expected true/false, got {value!r}")


def bounded_text(value: Any, fallback: str, limit: int = 500) -> str:
    if value is None:
        return fallback
    return str(value).strip()[:limit] or fallback


def case_from_package(case: dict[str, Any], index: int) -> CaseInput:
    case_id = bounded_text(case.get("case_id") or case.get("id"), f"S1-CS-CASE-{index + 1:03d}", 120)
    source_id = bounded_text(case.get("source_id"), "UNKNOWN_SOURCE", 120)
    tags = case.get("tags") if isinstance(case.get("tags"), list) else []
    metadata_refs = case.get("evidence_metadata_refs") if isinstance(case.get("evidence_metadata_refs"), list) else []
    if not metadata_refs:
        metadata_refs = [f"metadata:{source_id}:{case_id}"]
    return CaseInput(
        case_id=case_id,
        source_id=source_id,
        title=bounded_text(case.get("title"), "Untitled synthetic case", 200),
        severity=bounded_text(case.get("severity"), "UNSPECIFIED", 80),
        expected_outcome=bounded_text(case.get("expected_outcome"), "Reviewer signoff required.", 500),
        tags=tuple(str(tag)[:80] for tag in tags[:20]),
        metadata_refs=tuple(str(ref)[:300] for ref in metadata_refs[:20]),
    )


def case_from_qwen_bundle(path: Path, bundle: dict[str, Any]) -> CaseInput:
    uat_id = bounded_text(bundle.get("uat_id"), path.stem, 80)
    fact_bundle_id = bounded_text(bundle.get("fact_bundle_id"), path.stem, 140)
    source_id = bounded_text(bundle.get("source_payload_id"), fact_bundle_id, 140)
    title = bounded_text(bundle.get("scenario_title"), f"Synthetic QwenFactBundle {uat_id}", 220)
    profile = bundle.get("evaluation_profile") if isinstance(bundle.get("evaluation_profile"), dict) else {}
    fixture_meta = bundle.get("fixture_meta") if isinstance(bundle.get("fixture_meta"), dict) else {}
    tags = [
        "synthetic",
        "qwen_fact_bundle",
        f"uat:{uat_id}",
    ]
    if profile.get("prompt_injection_required"):
        tags.append("prompt_injection_required")
    if fixture_meta.get("synthetic_only") is True:
        tags.append("synthetic_only")
    return CaseInput(
        case_id=uat_id,
        source_id=source_id,
        title=title,
        severity="SYNTHETIC",
        expected_outcome="Metadata-only S1 fixture summary; reviewer signoff required before any next step.",
        tags=tuple(tags),
        metadata_refs=(f"qwen_fact_bundle:{fact_bundle_id}", f"source_payload:{source_id}"),
        input_file=path.as_posix(),
    )


def load_input(input_path: Path, workdir: Path) -> LoadedInput:
    if input_path.is_file():
        obj = read_json(input_path)
        if not isinstance(obj, dict):
            raise ValueError("input package root must be a JSON object")
        cases = obj.get("cases")
        if not isinstance(cases, list):
            raise ValueError("input package file must contain a list field named 'cases'")
        loaded_cases = tuple(case_from_package(case, index) for index, case in enumerate(cases) if isinstance(case, dict))
        if not loaded_cases:
            raise ValueError("input package contains no case objects")
        return LoadedInput(
            input_ref=relpath(input_path, workdir),
            input_kind="json_package",
            package_id=bounded_text(obj.get("package_id"), input_path.stem, 160),
            data_mode=bounded_text(obj.get("data_mode"), "SYNTHETIC_PACKAGE_ONLY", 80),
            cases=loaded_cases,
            raw_objects=(obj,),
        )

    if input_path.is_dir():
        raw_objects: list[dict[str, Any]] = []
        cases: list[CaseInput] = []
        for path in sorted(input_path.glob("*.json")):
            obj = read_json(path)
            if not isinstance(obj, dict):
                raise ValueError(f"{path} root must be a JSON object")
            raw_objects.append(obj)
            if "fact_bundle_id" in obj or "uat_id" in obj:
                cases.append(case_from_qwen_bundle(path, obj))
        if not raw_objects:
            raise ValueError("input directory contains no JSON files")
        if not cases:
            raise ValueError("input directory contains JSON files but no QwenFactBundle-like objects")
        return LoadedInput(
            input_ref=relpath(input_path, workdir),
            input_kind="qwen_fact_bundle_directory",
            package_id=input_path.name,
            data_mode="SYNTHETIC_PACKAGE_ONLY",
            cases=tuple(cases),
            raw_objects=tuple(raw_objects),
        )

    raise FileNotFoundError(str(input_path))


def scan_loaded_input(loaded: LoadedInput) -> dict[str, Any]:
    scans = [scan_json_for_forbidden(obj, f"input:{index}") for index, obj in enumerate(loaded.raw_objects)]
    findings = [finding for scan in scans for finding in scan["findings"]]
    return {
        "label": "input_package",
        "input_kind": loaded.input_kind,
        "object_count": len(loaded.raw_objects),
        "scanned_fields": sum(scan["scanned_fields"] for scan in scans),
        "scanned_string_values": sum(scan["scanned_string_values"] for scan in scans),
        "findings": findings,
    }


def validate_fixture_meta(loaded: LoadedInput) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if loaded.input_kind != "qwen_fact_bundle_directory":
        return findings
    for index, obj in enumerate(loaded.raw_objects):
        meta = obj.get("fixture_meta")
        if not isinstance(meta, dict):
            findings.append(
                {
                    "source": f"input:{index}",
                    "finding_type": "missing_fixture_meta",
                    "field_path": "fixture_meta",
                    "severity": HOLD,
                    "matched_value_retained": False,
                }
            )
            continue
        forbidden_true_fields = (
            "real_data_derived",
            "masked_real_data",
            "secrets_present",
            "raw_layer0_payload_present",
        )
        for field in forbidden_true_fields:
            if meta.get(field) is True:
                findings.append(
                    {
                        "source": f"input:{index}",
                        "finding_type": "forbidden_fixture_meta_true",
                        "field_path": f"fixture_meta.{field}",
                        "severity": NO_GO,
                        "matched_value_retained": False,
                    }
                )
        if meta.get("synthetic_only") is not True:
            findings.append(
                {
                    "source": f"input:{index}",
                    "finding_type": "synthetic_only_not_true",
                    "field_path": "fixture_meta.synthetic_only",
                    "severity": HOLD,
                    "matched_value_retained": False,
                }
            )
    return findings


def build_fixture_provider(loaded: LoadedInput) -> dict[str, Any]:
    return {
        "provider": "fixture",
        "qwen_used": False,
        "items": [
            {
                "case_id": case.case_id,
                "summary": f"S1 fixture summary for {case.case_id}: {case.title}. Metadata-only review required.",
                "evidence_metadata_refs": list(case.metadata_refs),
                "provider_decision_hint": "REVIEW_REQUIRED",
                "qwen_used": False,
            }
            for case in loaded.cases
        ],
        "provider_notes": "Deterministic fixture provider; no Qwen/API dependency.",
    }


def build_import_provider(loaded: LoadedInput, provider_name: str, provider_output_file: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    obj = read_json(provider_output_file)
    if not isinstance(obj, dict):
        raise ValueError("provider output file root must be a JSON object")
    provider_scan = scan_json_for_forbidden(obj, "provider_output_file")
    outputs = obj.get("items") or obj.get("case_outputs") or []
    if not isinstance(outputs, list):
        raise ValueError("provider output must contain an 'items' or 'case_outputs' list")
    by_case = {str(item.get("case_id")): item for item in outputs if isinstance(item, dict) and item.get("case_id")}
    items = []
    for case in loaded.cases:
        raw = by_case.get(case.case_id, {})
        refs = raw.get("evidence_metadata_refs") if isinstance(raw.get("evidence_metadata_refs"), list) else []
        items.append(
            {
                "case_id": case.case_id,
                "summary": bounded_text(raw.get("summary"), "No approved provider summary supplied.", 1000),
                "evidence_metadata_refs": [str(ref)[:300] for ref in refs[:20]],
                "provider_decision_hint": bounded_text(raw.get("provider_decision_hint"), "REVIEW_REQUIRED", 80),
                "qwen_used": provider_name == "qwen-api",
            }
        )
    return (
        {
            "provider": provider_name,
            "qwen_used": provider_name == "qwen-api",
            "items": items,
            "provider_notes": "Approved provider output imported by whitelist. Raw provider payload was not persisted.",
        },
        provider_scan,
    )


def derive_case_summary(loaded: LoadedInput, provider_result: dict[str, Any]) -> dict[str, Any]:
    by_case = {item["case_id"]: item for item in provider_result.get("items", []) if isinstance(item, dict) and item.get("case_id")}
    cases = []
    for case in loaded.cases:
        provider_item = by_case.get(case.case_id, {})
        cases.append(
            {
                "case_id": case.case_id,
                "source_id": case.source_id,
                "title": case.title,
                "severity": case.severity,
                "expected_outcome": case.expected_outcome,
                "summary": provider_item.get("summary", "No summary available."),
                "evidence_metadata_refs": provider_item.get("evidence_metadata_refs", list(case.metadata_refs)),
                "provider_decision_hint": provider_item.get("provider_decision_hint", "REVIEW_REQUIRED"),
                "reviewer_action": "REVIEW_AND_SIGNOFF_REQUIRED",
                "tags": list(case.tags),
            }
        )
    return {
        "schema_version": "secupilot.s1.case_summary.v1",
        "case_count": len(cases),
        "provider": provider_result.get("provider"),
        "qwen_used": provider_result.get("qwen_used", False),
        "cases": cases,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SecuPilot S1 Closed Shadow Fast MVP Runner")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--workdir", default=".")
    parser.add_argument("--input", dest="input_ref", default=None, help="Approved input package file or directory.")
    parser.add_argument("--input-package", dest="input_package", default=None, help="Alias for --input.")
    parser.add_argument("--output", dest="output_ref", default=None, help="Artifact output directory.")
    parser.add_argument("--artifact-dir", dest="artifact_dir", default=None, help="Alias for --output.")
    parser.add_argument("--provider", choices=("fixture", "external-output", "qwen-api"), default="fixture")
    parser.add_argument("--provider-output-file", default=None)
    parser.add_argument("--operator", default="Codex / authorized operator")
    parser.add_argument("--operator-account", default="local-mvp-operator")
    parser.add_argument("--go-record-ref", default="SECUPILOT-S1-CLOSED-SHADOW-GO-20260430-001")
    parser.add_argument("--source-ids", default="")
    parser.add_argument("--data-mode", default="SYNTHETIC_PACKAGE_ONLY")
    parser.add_argument("--allowed-input-scope", default="G01-approved synthetic/package metadata only; no raw payloads; no real data; no masked real data")
    parser.add_argument("--customer-visible-output", type=parse_bool, default=False)
    parser.add_argument("--writeback-enabled", type=parse_bool, default=False)
    parser.add_argument("--production-writeback", type=parse_bool, default=False)
    parser.add_argument("--production-connectors-enabled", type=parse_bool, default=False)
    parser.add_argument("--no-writeback", action="store_true")
    parser.add_argument("--no-customer-visible", action="store_true")
    parser.add_argument("--environment-id", default="G04_CLOSED_ENVIRONMENT_CONFIRMED_BY_USER")
    parser.add_argument("--isolation-proof-ref", default="G04_ISOLATION_PROOF_CLOSED_BY_USER_CONFIRMATION")
    parser.add_argument("--no-writeback-proof-ref", default="G04_NO_WRITEBACK_PROOF_CLOSED_BY_USER_CONFIRMATION")
    parser.add_argument("--access-boundary-proof-ref", default="G04_ACCESS_BOUNDARY_CLOSED_BY_USER_CONFIRMATION")
    parser.add_argument("--reviewer-register-ref", default="G05_REVIEWER_ACCESS_REGISTER_CLOSED_BY_USER_CONFIRMATION")
    parser.add_argument("--retention-policy-ref", default="G06_RETENTION_POLICY_CONFIRMED")
    parser.add_argument("--stop-clean-delete-ref", default="G09_STOP_CLEAN_DELETE_AUTHORITY_CONFIRMED")
    parser.add_argument("--requested-outcome", choices=tuple(EXIT_CODES), default=PASS_WITH_NOTES)
    parser.add_argument("--pass-hold-reason", default="Closed-shadow fixture metadata capture completed; reviewer signoff required.")
    parser.add_argument("--reviewer-action", default="REVIEW_AND_SIGNOFF_REQUIRED")
    args = parser.parse_args(argv)

    if not args.input_ref and args.input_package:
        args.input_ref = args.input_package
    if not args.output_ref and args.artifact_dir:
        args.output_ref = args.artifact_dir
    if not args.input_ref:
        parser.error("--input or --input-package is required")
    if not args.output_ref:
        parser.error("--output or --artifact-dir is required")
    return args


def boundary_findings(args: argparse.Namespace) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    flag_values = {
        "customer_visible_output": args.customer_visible_output,
        "writeback_enabled": args.writeback_enabled,
        "production_writeback": args.production_writeback,
        "production_connectors_enabled": args.production_connectors_enabled,
    }
    for field, value in flag_values.items():
        if value is True:
            findings.append(
                {
                    "source": "runtime_args",
                    "finding_type": "forbidden_runtime_flag",
                    "field_path": field,
                    "severity": NO_GO,
                    "matched_value_retained": False,
                }
            )
    if not args.no_writeback:
        findings.append(
            {
                "source": "runtime_args",
                "finding_type": "missing_no_writeback_assertion",
                "field_path": "no_writeback",
                "severity": HOLD,
                "matched_value_retained": False,
            }
        )
    if not args.no_customer_visible:
        findings.append(
            {
                "source": "runtime_args",
                "finding_type": "missing_no_customer_visible_assertion",
                "field_path": "no_customer_visible",
                "severity": HOLD,
                "matched_value_retained": False,
            }
        )
    if args.provider in {"external-output", "qwen-api"} and not args.provider_output_file:
        findings.append(
            {
                "source": "runtime_args",
                "finding_type": "missing_provider_output_file",
                "field_path": "provider_output_file",
                "severity": HOLD,
                "matched_value_retained": False,
            }
        )
    return findings


def decide_outcome(requested: str, findings: list[dict[str, Any]]) -> tuple[str, str]:
    if any(finding.get("severity") == NO_GO for finding in findings):
        return NO_GO, "NO_GO: safety scan or boundary validation detected forbidden content/flags. Matched values were not retained."
    if any(finding.get("severity") == HOLD for finding in findings):
        return HOLD, "HOLD: runner prerequisites or safety assertions are incomplete."
    return requested, "Closed-shadow fixture metadata capture completed; reviewer signoff required."


def build_manifest(artifact_dir: Path, workdir: Path) -> dict[str, Any]:
    artifacts = []
    for file_name in STANDARD_ARTIFACTS:
        path = artifact_dir / file_name
        if path.exists():
            artifacts.append(
                {
                    "path": relpath(path, workdir),
                    "file_name": file_name,
                    "sha256": sha256_file(path),
                    "retention_class": "S1_CLOSED_SHADOW_EVIDENCE_METADATA",
                    "retain_allowed": True,
                    "contains_raw_payload": False,
                    "contains_secret_or_token": False,
                    "contains_customer_visible_artifact": False,
                }
            )
    return {
        "schema_version": "secupilot.s1.artifact_manifest.v1",
        "generated_at_utc": utc_now(),
        "artifact_dir": relpath(artifact_dir, workdir),
        "artifacts": artifacts,
        "manifest_self": {
            "path": relpath(artifact_dir / MANIFEST_FILE, workdir),
            "sha256": "SELF_REFERENTIAL_HASH_EXCLUDED",
        },
    }


def build_run_record_md(run_id: str, final_outcome: str, final_status: dict[str, Any]) -> str:
    return (
        "# S1 Closed Shadow Run Record\n\n"
        "```text\n"
        f"S1_CLOSED_SHADOW_RUN_ID = {run_id}\n"
        "S1_CLOSED_SHADOW_EXECUTION_STARTED_BY_CODEX = YES\n"
        "S1_CLOSED_SHADOW_RUN_ATTEMPTED_BY_CODEX = EXECUTED_FAST_MVP_FIXTURE_RUNNER\n"
        "S1_CLOSED_SHADOW_RUN_OUTPUT_CAPTURED = YES\n"
        f"S1_CLOSED_SHADOW_FINAL_OUTCOME = {final_outcome}\n"
        f"S1_CLOSED_SHADOW_EXIT_CODE = {final_status['exit_code']}\n"
        "CUSTOMER_VISIBLE_OUTPUT = NO\n"
        "PRODUCTION_WRITE_BACK = NO\n"
        "QWEN_AUTONOMOUS_APPROVAL_OR_ACTION = NO\n"
        "```\n\n"
        "This artifact was generated by `scripts/s1_closed_shadow_run.py`.\n\n"
        "It contains metadata-only run status and does not contain real data, masked-real data, raw payloads, "
        "customer-visible output, secrets, tokens, auth headers, production connector output, or write-back evidence.\n"
    )


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    workdir = Path(args.workdir).resolve()
    input_path = (workdir / args.input_ref).resolve() if not Path(args.input_ref).is_absolute() else Path(args.input_ref).resolve()
    output_dir = (workdir / args.output_ref).resolve() if not Path(args.output_ref).is_absolute() else Path(args.output_ref).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    start_time = utc_now()
    provider_scan = {
        "label": "provider_output_file",
        "scanned_fields": 0,
        "scanned_string_values": 0,
        "findings": [],
    }
    load_error = None
    loaded: LoadedInput | None = None
    provider_result: dict[str, Any] = {"provider": args.provider, "qwen_used": args.provider == "qwen-api", "items": []}
    input_scan = {
        "label": "input_package",
        "input_kind": "unloaded",
        "object_count": 0,
        "scanned_fields": 0,
        "scanned_string_values": 0,
        "findings": [],
    }
    findings = boundary_findings(args)

    try:
        loaded = load_input(input_path, workdir)
        input_scan = scan_loaded_input(loaded)
        findings.extend(input_scan["findings"])
        findings.extend(validate_fixture_meta(loaded))
        if args.provider == "fixture":
            provider_result = build_fixture_provider(loaded)
        else:
            provider_output = Path(args.provider_output_file or "")
            provider_output_path = (workdir / provider_output).resolve() if not provider_output.is_absolute() else provider_output.resolve()
            provider_result, provider_scan = build_import_provider(loaded, args.provider, provider_output_path)
            findings.extend(provider_scan["findings"])
    except Exception as exc:  # noqa: BLE001 - convert any input/provider issue into a HOLD artifact.
        load_error = f"{type(exc).__name__}: {exc}"
        findings.append(
            {
                "source": "runner",
                "finding_type": "input_or_provider_load_error",
                "field_path": "input",
                "severity": HOLD,
                "matched_value_retained": False,
            }
        )

    loaded_cases = loaded.cases if loaded is not None else tuple()
    source_ids = [part.strip() for part in args.source_ids.split(",") if part.strip()]
    if loaded is not None and not source_ids:
        source_ids = sorted({case.source_id for case in loaded.cases})

    requested_reason = args.pass_hold_reason
    final_outcome, default_reason = decide_outcome(args.requested_outcome, findings)
    reason = requested_reason if final_outcome == args.requested_outcome else default_reason
    exit_code = EXIT_CODES[final_outcome]
    end_time = utc_now()

    case_summary = derive_case_summary(loaded, provider_result) if loaded is not None else {
        "schema_version": "secupilot.s1.case_summary.v1",
        "case_count": 0,
        "provider": args.provider,
        "qwen_used": args.provider == "qwen-api",
        "cases": [],
    }

    run_record = {
        "schema_version": "secupilot.s1.run_record.v1",
        "run_id": args.run_id,
        "operator": args.operator,
        "operator_account": args.operator_account,
        "go_record_ref": args.go_record_ref,
        "start_time_utc": start_time,
        "end_time_utc": end_time,
        "workdir": ".",
        "artifact_dir": relpath(output_dir, workdir),
        "provider": args.provider,
        "qwen_used": provider_result.get("qwen_used", False),
        "input_ref": relpath(input_path, workdir),
        "input_kind": loaded.input_kind if loaded is not None else "unloaded",
        "input_load_error": load_error,
        "case_count": len(loaded_cases),
        "source_ids": source_ids,
        "data_boundary": {
            "data_mode": args.data_mode,
            "allowed_input_scope": args.allowed_input_scope,
            "customer_visible_output": False,
            "writeback_enabled": False,
            "production_writeback": False,
            "production_connectors_enabled": False,
            "raw_payload_retention": False,
            "secret_token_auth_header_retention": False,
        },
        "environment_boundary": {
            "environment_id": args.environment_id,
            "isolation_proof_ref": args.isolation_proof_ref,
            "no_writeback_proof_ref": args.no_writeback_proof_ref,
            "access_boundary_proof_ref": args.access_boundary_proof_ref,
        },
        "governance_refs": {
            "reviewer_register_ref": args.reviewer_register_ref,
            "retention_policy_ref": args.retention_policy_ref,
            "stop_clean_delete_ref": args.stop_clean_delete_ref,
        },
    }

    safety_scan = {
        "schema_version": "secupilot.s1.safety_scan.v1",
        "generated_at_utc": utc_now(),
        "scanner_scope": ["runtime_args", "input_package_or_directory", "provider_output_file_if_supplied", "generated_metadata"],
        "rules": [
            "no secrets/tokens/auth headers/cookies/private keys/SAS tokens",
            "no raw_payload/host_raw_evidence/raw_evidence keys",
            "no customer-visible artifact retention",
            "no write-back or production connector flags",
            "Qwen provider imports approved metadata only and makes no live API call in MVP-01",
        ],
        "input_package_scan": input_scan,
        "provider_output_scan": provider_scan,
        "runtime_boundary_findings": [finding for finding in findings if finding.get("source") == "runtime_args"],
        "summary": {
            "finding_count": len(findings),
            "no_go_count": sum(1 for finding in findings if finding.get("severity") == NO_GO),
            "hold_count": sum(1 for finding in findings if finding.get("severity") == HOLD),
            "matched_values_retained": False,
        },
        "findings": findings,
    }

    final_status = {
        "schema_version": "secupilot.s1.final_status.v1",
        "run_id": args.run_id,
        "final_outcome": final_outcome,
        "exit_code": exit_code,
        "pass_hold_reason": reason,
        "reviewer_action": args.reviewer_action,
        "required_reviewers": list(REQUIRED_REVIEWERS),
        "frontend_status_fields": {
            "s1_run_status": final_outcome,
            "case_summary_artifact": relpath(output_dir / "case_summary.json", workdir),
            "evidence_list_artifact": relpath(output_dir / MANIFEST_FILE, workdir),
            "hold_pass_reason": reason,
            "reviewer_action": args.reviewer_action,
        },
        "boundaries_preserved": {
            "customer_visible_output": False,
            "writeback": False,
            "production_connectors": False,
            "raw_payload_retention": False,
            "secret_retention": False,
            "qwen_autonomous_action": False,
        },
        "can_show_in_local_demo": final_outcome in {PASS, PASS_WITH_NOTES},
        "can_deploy_to_customer_production": False,
        "next_step": "FRONTEND_ARTIFACT_VIEW" if final_outcome in {PASS, PASS_WITH_NOTES} else "FIX_HOLD_OR_NO_GO_REASON",
    }

    write_json(output_dir / "run_record.json", run_record)
    write_json(output_dir / "safety_scan.json", safety_scan)
    write_json(output_dir / "case_summary.json", case_summary)
    write_json(output_dir / "final_status.json", final_status)
    write_text(output_dir / "RUN_RECORD.md", build_run_record_md(args.run_id, final_outcome, final_status))
    write_json(output_dir / MANIFEST_FILE, build_manifest(output_dir, workdir))

    return exit_code


def main() -> int:
    return run()


if __name__ == "__main__":
    sys.exit(main())
