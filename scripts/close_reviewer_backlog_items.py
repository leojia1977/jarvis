#!/usr/bin/env python3
"""Close repo-local reviewer backlog items with explicit Goal resolution evidence."""

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

REQUIRED_FALSE_BOUNDARIES = (
    "real_data",
    "masked_real_data",
    "live_qwen_api",
    "live_connectors",
    "production_writeback",
    "customer_visible_output",
    "push",
)

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


def validate_backlog(payload: dict[str, Any]) -> None:
    if payload.get("external_tracker_write") is not False:
        raise ValueError("backlog external_tracker_write must be false")
    if payload.get("customer_visible_or_deploy_go") is not False:
        raise ValueError("backlog must not grant customer-visible or deploy go")
    boundaries = payload.get("boundaries", {})
    for key in REQUIRED_FALSE_BOUNDARIES:
        if boundaries.get(key) is not False:
            raise ValueError(f"backlog boundary must be false: {key}")
    if not isinstance(payload.get("items"), list):
        raise ValueError("backlog items must be a list")
    scan_text(json.dumps(payload, ensure_ascii=False), "reviewer_backlog")


def render_backlog_markdown(payload: dict[str, Any]) -> str:
    item_blocks = []
    for item in payload["items"]:
        acceptance = "\n".join(f"  - {line}" for line in item.get("acceptance", []))
        closeout_lines = ""
        if item.get("status") == "BACKLOG_CLOSED":
            closeout_lines = f"""
Resolution:

```text
closed_by_goal = {item.get("closed_by_goal")}
closed_by_commit = {item.get("closed_by_commit")}
resolution = {item.get("resolution")}
closed_at_utc = {item.get("closed_at_utc")}
```
"""
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
{closeout_lines}
"""
        )
    return f"""# SecuPilot Reviewer Feedback Product Backlog

Generated at: {payload["generated_at_utc"]}

```text
candidate = {payload["candidate"]}
source_candidate = {payload["source_candidate"]}
reviewer_decision = {payload["reviewer_decision"]}
item_count = {len(payload["items"])}
closed_item_count = {payload.get("closed_item_count", 0)}
customer_visible_or_deploy_go = false
```

{"".join(item_blocks)}

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


def close_items(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    backlog_json = (repo_root / args.backlog_json).resolve()
    output_json = (repo_root / args.output_json).resolve()
    output_md = (repo_root / args.output_md).resolve()
    closeout_json = (repo_root / args.closeout_json).resolve()
    closeout_md = (repo_root / args.closeout_md).resolve()
    close_item_ids = set(args.item_id)
    evidence_refs = [value.replace("\\", "/") for value in args.evidence]

    payload = read_json(backlog_json)
    if not isinstance(payload, dict):
        raise ValueError("backlog must be a JSON object")
    validate_backlog(payload)

    known_ids = {item.get("id") for item in payload["items"] if isinstance(item, dict)}
    missing = sorted(close_item_ids - known_ids)
    if missing:
        raise ValueError(f"backlog item id not found: {', '.join(missing)}")

    closed_at = utc_now()
    closed_items = []
    for item in payload["items"]:
        if item.get("id") not in close_item_ids:
            continue
        item["status"] = "BACKLOG_CLOSED"
        item["closed_by_goal"] = args.closed_by_goal
        item["closed_by_commit"] = args.closed_by_commit
        item["closed_at_utc"] = closed_at
        item["resolution"] = args.resolution
        item.setdefault("closure_evidence", [])
        item["closure_evidence"] = list(dict.fromkeys([*item["closure_evidence"], *evidence_refs]))
        closed_items.append(item)

    payload["generated_at_utc"] = closed_at
    payload["closed_item_count"] = sum(
        1 for item in payload["items"] if item.get("status") == "BACKLOG_CLOSED"
    )
    payload["external_tracker_write"] = False
    payload["customer_visible_or_deploy_go"] = False
    validate_backlog(payload)

    write_json(output_json, payload)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_backlog_markdown(payload), encoding="utf-8")

    closeout = {
        "schema_version": "secupilot.reviewer_backlog_closeout.v1",
        "created_at_utc": closed_at,
        "source_backlog_json": portable_path(backlog_json, repo_root),
        "output_backlog_json": portable_path(output_json, repo_root),
        "output_backlog_md": portable_path(output_md, repo_root),
        "candidate": payload["candidate"],
        "source_candidate": payload["source_candidate"],
        "closed_by_goal": args.closed_by_goal,
        "closed_by_commit": args.closed_by_commit,
        "resolution": args.resolution,
        "closed_item_ids": sorted(close_item_ids),
        "closed_item_count": len(closed_items),
        "boundaries": {key: False for key in REQUIRED_FALSE_BOUNDARIES},
        "customer_visible_or_deploy_go": False,
        "external_tracker_write": False,
    }
    write_json(closeout_json, closeout)
    closeout_md.parent.mkdir(parents=True, exist_ok=True)
    closeout_md.write_text(
        f"""# Reviewer Backlog Closeout

```text
candidate = {payload["candidate"]}
closed_by_goal = {args.closed_by_goal}
closed_by_commit = {args.closed_by_commit}
closed_item_count = {len(closed_items)}
customer_visible_or_deploy_go = false
external_tracker_write = false
```

Closed items:

{chr(10).join(f"- {item['id']}: {item['title']}" for item in closed_items)}

Resolution:

```text
{args.resolution}
```
""",
        encoding="utf-8",
    )

    for path in (output_json, output_md, closeout_json, closeout_md):
        scan_text(path.read_text(encoding="utf-8"), path.name)

    return {
        "status": "PASS",
        "candidate": payload["candidate"],
        "closed_item_count": len(closed_items),
        "output_json": portable_path(output_json, repo_root),
        "output_md": portable_path(output_md, repo_root),
        "closeout_json": portable_path(closeout_json, repo_root),
        "closeout_md": portable_path(closeout_md, repo_root),
        "output_json_sha256": file_sha256(output_json),
        "closeout_json_sha256": file_sha256(closeout_json),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backlog-json", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--closeout-json", required=True)
    parser.add_argument("--closeout-md", required=True)
    parser.add_argument("--item-id", action="append", required=True)
    parser.add_argument("--closed-by-goal", required=True)
    parser.add_argument("--closed-by-commit", required=True)
    parser.add_argument("--resolution", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--repo-root", default=".")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = close_items(args)
    except Exception as exc:
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
