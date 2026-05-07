#!/usr/bin/env python3
"""Convert local/offline reviewer feedback into a product backlog/action list."""

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
    "real_data",
    "masked_real_data",
    "live_qwen_api",
    "live_connectors",
    "production_writeback",
    "customer_visible_output",
    "push",
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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def portable_path(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def scan_text(text: str, label: str) -> None:
    for pattern in FORBIDDEN_TEXT_PATTERNS:
        if pattern.search(text):
            raise ValueError(f"{label}: forbidden text pattern {pattern.pattern}")


def validate_feedback(payload: dict[str, Any]) -> None:
    required = ("candidate", "source_candidate", "decision", "reviewer", "timestamp")
    missing = [key for key in required if not payload.get(key)]
    if missing:
        raise ValueError(f"feedback missing required fields: {', '.join(missing)}")
    boundaries = payload.get("boundaries", {})
    for key in REQUIRED_FALSE_BOUNDARIES:
        if boundaries.get(key) is not False:
            raise ValueError(f"feedback boundary must be false: {key}")
    if payload.get("customer_visible_or_deploy_go") is not False:
        raise ValueError("feedback must not grant customer-visible or deploy go")
    scan_text(json.dumps(payload, ensure_ascii=False), "reviewer_feedback")


def classify_category(text: str) -> str:
    lowered = text.lower()
    if "截图" in text or "screenshot" in lowered:
        return "REVIEW_SCREENSHOT"
    if "路径" in text or "package" in lowered or "candidate" in lowered:
        return "PACKAGE_CONSISTENCY"
    if "说明" in text or "文案" in text or "试用范围" in text:
        return "PRODUCT_COPY"
    if "结果页" in text or "/s1-run" in lowered:
        return "RESULT_PAGE_UX"
    return "REVIEWER_EXPERIENCE"


def priority_for(text: str, source_type: str) -> str:
    if source_type == "next_round_suggestion":
        if any(token in text for token in ("清理", "路径", "截图", "candidate", "source")):
            return "P1"
        return "P2"
    return "P3"


def acceptance_for(text: str) -> list[str]:
    checks = [
        "local/offline only",
        "no real or masked-real data",
        "no live Qwen/API/connectors",
        "no production write-back",
        "no customer-visible publish/deploy/output",
    ]
    if "截图" in text:
        checks.append("Playwright screenshot and screenshot safety validator PASS")
    if "路径" in text or "candidate" in text or "source" in text:
        checks.append("RC consistency validator PASS")
    if "结果页" in text or "/s1-run" in text:
        checks.append("/s1-run App and Playwright smoke PASS")
    return checks


def item_id(candidate: str, index: int) -> str:
    match = re.search(r"RC_(\d{3})", candidate)
    rc = match.group(1) if match else "000"
    return f"RFB-RC{rc}-{index:03d}"


def build_items(feedback: dict[str, Any]) -> list[dict[str, Any]]:
    raw_items: list[tuple[str, str]] = []
    raw_items.extend(("non_blocking_observation", item) for item in feedback.get("non_blocking_observations", []))
    raw_items.extend(("next_round_suggestion", item) for item in feedback.get("next_round_suggestions", []))
    deduped: dict[str, tuple[str, str]] = {}
    for source_type, text in raw_items:
        normalized = text.strip().rstrip(".。")
        if not normalized:
            continue
        previous = deduped.get(normalized)
        if previous and previous[0] == "next_round_suggestion":
            continue
        deduped[normalized] = (source_type, text)
    items: list[dict[str, Any]] = []
    for index, (source_type, text) in enumerate(deduped.values(), start=1):
        category = classify_category(text)
        items.append(
            {
                "id": item_id(feedback["candidate"], index),
                "source_type": source_type,
                "source_candidate": feedback["candidate"],
                "source_decision": feedback["decision"],
                "title": text.rstrip(".。"),
                "description": text,
                "category": category,
                "priority": priority_for(text, source_type),
                "status": "BACKLOG_OPEN",
                "owner": "SecuPilot product engineering",
                "acceptance": acceptance_for(text),
                "non_authorization": {
                    "customer_visible_or_deploy_go": False,
                    "live_qwen_api": False,
                    "production_writeback": False,
                },
            }
        )
    return items


def backlog_markdown(payload: dict[str, Any]) -> str:
    item_blocks = []
    for item in payload["items"]:
        acceptance = "\n".join(f"  - {line}" for line in item["acceptance"])
        item_blocks.append(
            f"""## {item["id"]}: {item["title"]}

```text
category = {item["category"]}
priority = {item["priority"]}
status = {item["status"]}
source_type = {item["source_type"]}
```

Acceptance:

{acceptance}
"""
        )
    items_text = "\n".join(item_blocks) if item_blocks else "No reviewer backlog items."
    return f"""# SecuPilot Reviewer Feedback Product Backlog

Generated at: {payload["generated_at_utc"]}

```text
candidate = {payload["candidate"]}
source_candidate = {payload["source_candidate"]}
reviewer_decision = {payload["reviewer_decision"]}
item_count = {len(payload["items"])}
customer_visible_or_deploy_go = false
```

{items_text}

## Non-Authorization

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


def export_backlog(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    feedback_path = (repo_root / args.feedback_json).resolve()
    output_json = (repo_root / args.output_json).resolve()
    output_md = (repo_root / args.output_md).resolve()
    feedback = read_json(feedback_path)
    if not isinstance(feedback, dict):
        raise ValueError("reviewer feedback must be a JSON object")
    validate_feedback(feedback)

    items = build_items(feedback)
    payload = {
        "schema_version": "secupilot.reviewer_feedback_product_backlog.v1",
        "generated_at_utc": utc_now(),
        "source_feedback_json": portable_path(feedback_path, repo_root),
        "candidate": feedback["candidate"],
        "source_candidate": feedback["source_candidate"],
        "reviewer_decision": feedback["decision"],
        "reviewer": feedback["reviewer"],
        "items": items,
        "boundaries": {key: False for key in REQUIRED_FALSE_BOUNDARIES},
        "customer_visible_or_deploy_go": False,
        "external_tracker_write": False,
    }

    write_json(output_json, payload)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(backlog_markdown(payload), encoding="utf-8")
    scan_text(output_json.read_text(encoding="utf-8"), output_json.name)
    scan_text(output_md.read_text(encoding="utf-8"), output_md.name)

    return {
        "status": "PASS",
        "candidate": payload["candidate"],
        "item_count": len(items),
        "output_json": portable_path(output_json, repo_root),
        "output_md": portable_path(output_md, repo_root),
        "output_json_sha256": file_sha256(output_json),
        "output_md_sha256": file_sha256(output_md),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feedback-json", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--repo-root", default=".")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = export_backlog(args)
    except Exception as exc:
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
