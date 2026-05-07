#!/usr/bin/env python3
"""Export a local/offline reviewer decision doc into structured feedback artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20

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

REQUIRED_FALSE_BOUNDARIES = (
    "real data",
    "masked-real data",
    "live qwen/api",
    "live connectors",
    "production write-back",
    "customer-visible",
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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def portable_path(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def text_between(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+(?:\d+\.\s+)?{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+(?:\d+\.\s+)?|\Z)",
        re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def code_block_lines(section: str) -> list[str]:
    match = re.search(r"```text\s*([\s\S]*?)```", section)
    if not match:
        return []
    return [line.strip() for line in match.group(1).splitlines() if line.strip()]


def key_value_lines(section: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in code_block_lines(section):
        if "=" in line:
            key, value = line.split("=", 1)
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            continue
        values[key.strip()] = value.strip()
    return values


def document_fields(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("`")
    return values


def first_decision_value(values: dict[str, str]) -> str:
    for value in values.values():
        if value:
            return value
    return ""


def numbered_lines(section: str) -> list[str]:
    lines = []
    for line in code_block_lines(section):
        cleaned = re.sub(r"^\d+\.\s*", "", line).strip()
        if cleaned:
            lines.append(cleaned)
    return lines


def bullet_lines(section: str) -> list[str]:
    lines = []
    for raw_line in section.splitlines():
        cleaned = raw_line.strip()
        if cleaned.startswith("- "):
            lines.append(cleaned[2:].strip())
    return lines


def scan_text(text: str, label: str) -> None:
    for pattern in FORBIDDEN_TEXT_PATTERNS:
        if pattern.search(text):
            raise ValueError(f"{label}: forbidden text pattern {pattern.pattern}")


def parse_decision_doc(decision_doc: Path, reviewer_override: str | None = None) -> dict[str, Any]:
    text = decision_doc.read_text(encoding="utf-8")
    scan_text(text, decision_doc.name)

    top_fields = document_fields(text)
    decision = key_value_lines(text_between(text, "Decision"))
    reviewer = key_value_lines(text_between(text, "Reviewer"))
    passed_checks = key_value_lines(text_between(text, "Passed Checks")) or key_value_lines(
        text_between(text, "Reviewer Checks")
    )
    passed_findings = bullet_lines(text_between(text, "Passed Findings"))
    observations = (
        code_block_lines(text_between(text, "Non-Blocking Observation"))
        or code_block_lines(text_between(text, "Non-Blocking Notes"))
        or bullet_lines(text_between(text, "Non-Blocking Notes"))
    )
    suggestions = numbered_lines(text_between(text, "Reviewer Next-Round Suggestions"))
    if not suggestions:
        suggestions = [
            line
            for line in observations
            if "后续" in line or "建议" in line or "弱化" in line or "tooltip" in line.lower()
        ]
    non_authorization = "\n".join(
        code_block_lines(text_between(text, "Non-Authorization"))
        or code_block_lines(text_between(text, "Boundary Confirmation"))
    ).lower()

    candidate = decision.get("CANDIDATE") or top_fields.get("Candidate")
    source_candidate = decision.get("SOURCE_CANDIDATE") or top_fields.get("Source candidate")
    reviewer_name = reviewer.get("Reviewer") or top_fields.get("Reviewer") or reviewer_override
    reviewer_decision = reviewer.get("Decision") or top_fields.get("Reviewer decision") or first_decision_value(decision)
    timestamp = reviewer.get("Timestamp") or top_fields.get("Date")
    package = reviewer.get("Package") or top_fields.get("Package")
    zip_path = reviewer.get("Zip") or top_fields.get("Zip")
    zip_sha = reviewer.get("Zip SHA256") or top_fields.get("Zip SHA256")

    required = {
        "Decision": reviewer_decision,
        "CANDIDATE": candidate,
        "SOURCE_CANDIDATE": source_candidate,
        "Reviewer": reviewer_name,
        "Timestamp": timestamp,
        "Package": package,
        "Zip": zip_path,
        "Zip SHA256": zip_sha,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise ValueError(f"decision doc missing required fields: {', '.join(missing)}")

    for boundary in REQUIRED_FALSE_BOUNDARIES:
        if boundary not in non_authorization:
            raise ValueError(f"non-authorization missing boundary: {boundary}")

    return {
        "decision": {
            "DECISION": reviewer_decision,
            "CANDIDATE": candidate,
            "SOURCE_CANDIDATE": source_candidate,
            "CUSTOMER_VISIBLE_OR_DEPLOY_GO": decision.get(
                "CUSTOMER_VISIBLE_OR_DEPLOY_GO", "NOT_AUTHORIZED"
            ),
        },
        "reviewer": {
            "Reviewer": reviewer_name,
            "Decision": reviewer_decision,
            "Timestamp": timestamp,
            "Review scope": reviewer.get("Review scope", "LOCAL_OFFLINE_REVIEW_ONLY"),
            "Package": package,
            "Zip": zip_path,
            "Zip SHA256": zip_sha,
        },
        "passed_checks": passed_checks,
        "passed_findings": passed_findings,
        "non_blocking_observations": observations,
        "next_round_suggestions": suggestions,
    }


def validate_package(package_dir: Path, parsed: dict[str, Any]) -> dict[str, Any]:
    manifest_path = package_dir / "package_manifest.json"
    final_status_path = package_dir / "evidence" / "final_status.json"
    safety_scan_path = package_dir / "evidence" / "safety_scan.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing package manifest: {manifest_path}")

    manifest = read_json(manifest_path)
    final_status = read_json(final_status_path)
    safety_scan = read_json(safety_scan_path)

    candidate = parsed["decision"]["CANDIDATE"]
    source_candidate = parsed["decision"]["SOURCE_CANDIDATE"]
    if manifest.get("candidate") != candidate:
        raise ValueError("package manifest candidate does not match decision doc")
    if manifest.get("source_candidate") != source_candidate:
        raise ValueError("package manifest source_candidate does not match decision doc")

    summary = safety_scan.get("summary", {})
    if summary.get("finding_count") != 0:
        raise ValueError("safety scan finding_count must be 0")

    boundaries = final_status.get("boundaries_preserved", {})
    for key in (
        "customer_visible_output",
        "production_connectors",
        "qwen_autonomous_action",
        "raw_payload_retention",
        "secret_retention",
        "writeback",
    ):
        if boundaries.get(key) is not False:
            raise ValueError(f"final_status boundary must be false: {key}")

    return {
        "package_manifest_sha256": file_sha256(manifest_path),
        "final_status_sha256": file_sha256(final_status_path),
        "safety_scan_sha256": file_sha256(safety_scan_path),
    }


def build_feedback_payload(
    decision_doc: Path, package_dir: Path, parsed: dict[str, Any], package_evidence: dict[str, Any], repo_root: Path
) -> dict[str, Any]:
    decision = parsed["decision"]
    reviewer = parsed["reviewer"]
    return {
        "schema_version": "secupilot.local_reviewer_feedback.v1",
        "generated_at_utc": utc_now(),
        "source_decision_doc": portable_path(decision_doc, repo_root),
        "package_dir": portable_path(package_dir, repo_root),
        "candidate": decision["CANDIDATE"],
        "source_candidate": decision["SOURCE_CANDIDATE"],
        "reviewer": reviewer["Reviewer"],
        "decision": reviewer["Decision"],
        "timestamp": reviewer["Timestamp"],
        "review_scope": reviewer.get("Review scope", "LOCAL_OFFLINE_REVIEW_ONLY"),
        "zip": reviewer["Zip"],
        "zip_sha256": reviewer["Zip SHA256"],
        "passed_checks": parsed["passed_checks"],
        "passed_findings": parsed["passed_findings"],
        "non_blocking_observations": parsed["non_blocking_observations"],
        "next_round_suggestions": parsed["next_round_suggestions"],
        "package_evidence": package_evidence,
        "boundaries": {
            "real_data": False,
            "masked_real_data": False,
            "live_qwen_api": False,
            "live_connectors": False,
            "production_writeback": False,
            "customer_visible_output": False,
            "push": False,
        },
        "state_mutation": "none",
        "artifact_write": "local_feedback_export_only",
        "customer_visible_or_deploy_go": False,
    }


def feedback_markdown(payload: dict[str, Any]) -> str:
    checks = "\n".join(f"- {key}: {value}" for key, value in payload["passed_checks"].items())
    findings = "\n".join(f"- {item}" for item in payload.get("passed_findings", []))
    observations = "\n".join(f"- {item}" for item in payload["non_blocking_observations"])
    suggestions = "\n".join(f"- {item}" for item in payload["next_round_suggestions"])
    return f"""# {payload["candidate"]} Local Reviewer Feedback

## Decision

```text
candidate: {payload["candidate"]}
source_candidate: {payload["source_candidate"]}
reviewer: {payload["reviewer"]}
decision: {payload["decision"]}
timestamp: {payload["timestamp"]}
review_scope: {payload["review_scope"]}
```

## Passed Checks

{checks}

## Passed Findings

{findings}

## Non-Blocking Observations

{observations}

## Next-Round Suggestions

{suggestions}

## Boundaries

```text
real_data = false
masked_real_data = false
live_qwen_api = false
live_connectors = false
production_writeback = false
customer_visible_output = false
push = false
```
"""


def export_feedback(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    decision_doc = (repo_root / args.decision_doc).resolve()
    package_dir = (repo_root / args.package_dir).resolve()
    output_json = (repo_root / args.output_json).resolve()
    output_md = (repo_root / args.output_md).resolve()

    parsed = parse_decision_doc(decision_doc, args.reviewer)
    package_evidence = validate_package(package_dir, parsed)
    payload = build_feedback_payload(decision_doc, package_dir, parsed, package_evidence, repo_root)

    output_json.parent.mkdir(parents=True, exist_ok=True)
    write_json(output_json, payload)
    output_md.write_text(feedback_markdown(payload), encoding="utf-8")
    scan_text(output_json.read_text(encoding="utf-8"), output_json.name)
    scan_text(output_md.read_text(encoding="utf-8"), output_md.name)

    return {
        "status": "PASS",
        "candidate": payload["candidate"],
        "decision": payload["decision"],
        "output_json": portable_path(output_json, repo_root),
        "output_md": portable_path(output_md, repo_root),
        "output_json_sha256": file_sha256(output_json),
        "output_md_sha256": file_sha256(output_md),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision-doc", required=True)
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--reviewer")
    parser.add_argument("--repo-root", default=".")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = export_feedback(args)
    except Exception as exc:
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
