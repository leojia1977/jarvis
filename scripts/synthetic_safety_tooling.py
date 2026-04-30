#!/usr/bin/env python3
"""Offline synthetic safety helpers for pre-shadow mapping checks.

This module is intentionally independent from runtime services, connectors,
Qwen execution, fixtures, and frontend code. It only validates synthetic strings
and synthetic QwenFactBundle-shaped dictionaries before any future S1 gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


HOLD_REJECT_SECRET_BEARING_INPUT = "HOLD_REJECT_SECRET_BEARING_INPUT"

_IPV4_RE = re.compile(r"^(?P<a>\d{1,3})\.(?P<b>\d{1,3})\.(?P<c>\d{1,3})\.(?P<d>\d{1,3})$")
_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
_WS_HOST_RE = re.compile(r"^ws-(?P<unit>[a-z0-9]+)-(?P<num>\d+)$", re.IGNORECASE)
_TOKEN_ARG_RE = re.compile(r"(?i)(?P<prefix>(?:^|\s)-token\s+)(?P<value>\S+)")
_AUTH_HEADER_RE = re.compile(r"(?i)^\s*authorization\s*:\s*bearer\s+\S+")
_PRIVATE_KEY_RE = re.compile(r"(?i)-----BEGIN\s+(?:RSA\s+|EC\s+|OPENSSH\s+)?PRIVATE\s+KEY-----")

_UNMASKED_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


@dataclass(frozen=True)
class MaskDecision:
    status: str
    kind: str
    value: str


@dataclass(frozen=True)
class ScanFinding:
    label: str
    pattern: str
    safe_listed: bool = False


@dataclass(frozen=True)
class ScanResult:
    hold: bool
    findings: tuple[ScanFinding, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class BundleValidationResult:
    valid: bool
    errors: tuple[str, ...] = field(default_factory=tuple)


HARD_STOP_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("password", re.compile(r"(?i)\bpassword\s*=")),
    ("passwd", re.compile(r"(?i)\bpasswd\s*=")),
    ("authorization_header", re.compile(r"(?i)\bauthorization\s*:")),
    ("bearer_token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]+")),
    ("api_key", re.compile(r"(?i)\bapi[_-]?key\s*=")),
    ("secret_assignment", re.compile(r"(?i)(?:^|[\s_-])secret\s*[:=]")),
    ("token_assignment", re.compile(r"(?i)\btoken\s*=")),
    ("private_key", re.compile(r"(?i)private\s+key")),
    ("session_cookie", re.compile(r"(?i)session\s+cookie")),
    ("pem_block", re.compile(r"(?i)-----BEGIN")),
)

MODEL_OUTPUT_KEYS = {
    "assistant_response",
    "gpu_metrics",
    "model_output",
    "qwen_output",
    "runtime_metrics",
    "scoring",
}

FORBIDDEN_BUNDLE_KEYS = {
    "authorization",
    "connector_payload",
    "host_raw_evidence",
    "private_key",
    "raw_command_line",
    "raw_event",
    "raw_event_json",
    "raw_layer0_payload",
    "session_cookie",
    "token",
}


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.lower().strip().encode("utf-8")).hexdigest()[:4]


def mask_synthetic_value(value: str) -> MaskDecision:
    """Return a deterministic synthetic-safe masking decision for one value."""
    text = value.strip()
    if _PRIVATE_KEY_RE.search(text):
        return MaskDecision("HOLD", "private_key", HOLD_REJECT_SECRET_BEARING_INPUT)

    if _AUTH_HEADER_RE.search(text):
        return MaskDecision("MASKED", "authorization_header", "[REDACTED_AUTHORIZATION_HEADER]")

    token_match = _TOKEN_ARG_RE.search(text)
    if token_match:
        masked = _TOKEN_ARG_RE.sub(r"\g<prefix>[REDACTED]", text)
        return MaskDecision("MASKED", "token_arg", masked)

    ip_match = _IPV4_RE.match(text)
    if ip_match:
        octets = [int(ip_match.group(name)) for name in ("a", "b", "c", "d")]
        if all(0 <= octet <= 255 for octet in octets):
            return MaskDecision("MASKED", "ipv4", f"{octets[0]}.{octets[1]}.{octets[2]}.x")

    if _EMAIL_RE.match(text):
        return MaskDecision("MASKED", "email", f"user_{_short_hash(text)}")

    host_match = _WS_HOST_RE.match(text)
    if host_match:
        unit = host_match.group("unit").lower()
        num = host_match.group("num")
        return MaskDecision("MASKED", "workstation_host", f"host_{unit}_ws_{num}")

    return MaskDecision("UNCHANGED", "unclassified", text)


def _is_safe_doc_example(line: str) -> bool:
    lowered = line.lower()
    return "safe_doc_example" in lowered or "documentation example" in lowered


def scan_text_for_hard_stops(text: str, *, allow_doc_examples: bool = False) -> ScanResult:
    """Detect secret-bearing patterns without preserving matched values."""
    findings: list[ScanFinding] = []
    for line in text.splitlines() or [text]:
        safe_listed_line = allow_doc_examples and _is_safe_doc_example(line)
        for label, pattern in HARD_STOP_PATTERNS:
            if pattern.search(line):
                findings.append(ScanFinding(label=label, pattern=pattern.pattern, safe_listed=safe_listed_line))
    hold = any(not finding.safe_listed for finding in findings)
    return ScanResult(hold=hold, findings=tuple(findings))


def _walk_json(value: Any, path: str = "$") -> Iterable[tuple[str, Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk_json(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_json(child, f"{path}[{index}]")


def validate_qwen_fact_bundle(bundle: dict[str, Any]) -> BundleValidationResult:
    """Validate a synthetic QwenFactBundle without invoking Qwen."""
    errors: list[str] = []
    fixture_meta = bundle.get("fixture_meta")
    if not isinstance(fixture_meta, dict):
        errors.append("fixture_meta_missing")
    else:
        if fixture_meta.get("synthetic_only") is not True:
            errors.append("fixture_meta.synthetic_only_not_true")
        if fixture_meta.get("real_data_derived") is not False:
            errors.append("fixture_meta.real_data_derived_not_false")
        if fixture_meta.get("masked_real_data") is True:
            errors.append("fixture_meta.masked_real_data_true")
        if fixture_meta.get("secrets_present") is True:
            errors.append("fixture_meta.secrets_present_true")
        if fixture_meta.get("raw_layer0_payload_present") is True:
            errors.append("fixture_meta.raw_layer0_payload_present_true")

    facts = bundle.get("facts")
    if not isinstance(facts, list) or not facts:
        errors.append("facts_missing_or_empty")
    if not bundle.get("unsupported_claims"):
        errors.append("unsupported_claims_missing")
    if not bundle.get("forbidden_outputs"):
        errors.append("forbidden_outputs_missing")
    if not (bundle.get("source_limitations") or bundle.get("required_model_behavior") or bundle.get("evaluation_profile")):
        errors.append("source_limitations_or_behavior_missing")

    for path, value in _walk_json(bundle):
        if path.split(".")[-1].lower() in MODEL_OUTPUT_KEYS:
            errors.append(f"model_output_field_present:{path}")
        if path.split(".")[-1].lower() in FORBIDDEN_BUNDLE_KEYS:
            errors.append(f"forbidden_raw_key_present:{path}")
        if isinstance(value, str):
            if _UNMASKED_EMAIL_RE.search(value):
                errors.append(f"unmasked_email_present:{path}")
            scan = scan_text_for_hard_stops(value)
            if scan.hold:
                labels = ",".join(sorted({finding.label for finding in scan.findings if not finding.safe_listed}))
                errors.append(f"secret_pattern_present:{path}:{labels}")

    return BundleValidationResult(valid=not errors, errors=tuple(errors))


def validate_qwen_fact_bundle_file(path: Path) -> BundleValidationResult:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        return BundleValidationResult(False, ("bundle_root_not_object",))
    return validate_qwen_fact_bundle(data)


def _main() -> int:
    parser = argparse.ArgumentParser(description="Offline synthetic safety tooling")
    subparsers = parser.add_subparsers(dest="command", required=True)

    mask_parser = subparsers.add_parser("mask")
    mask_parser.add_argument("value")

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("text")
    scan_parser.add_argument("--allow-doc-examples", action="store_true")

    bundle_parser = subparsers.add_parser("validate-qwen-bundle")
    bundle_parser.add_argument("path", type=Path)

    args = parser.parse_args()

    if args.command == "mask":
        print(json.dumps(mask_synthetic_value(args.value).__dict__, ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "scan":
        result = scan_text_for_hard_stops(args.text, allow_doc_examples=args.allow_doc_examples)
        print(json.dumps({"hold": result.hold, "findings": [finding.__dict__ for finding in result.findings]}, ensure_ascii=False, sort_keys=True))
        return 1 if result.hold else 0
    if args.command == "validate-qwen-bundle":
        result = validate_qwen_fact_bundle_file(args.path)
        print(json.dumps({"valid": result.valid, "errors": list(result.errors)}, ensure_ascii=False, sort_keys=True))
        return 0 if result.valid else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(_main())
