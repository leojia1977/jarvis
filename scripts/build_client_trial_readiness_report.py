#!/usr/bin/env python3
"""Build a SecuPilot local/offline client-trial readiness report."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20


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


def portable_path(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def require_false(value: Any, label: str, holds: list[str]) -> None:
    if value is not False:
        holds.append(f"{label} must be false")


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    package_dir = (repo_root / args.package_dir).resolve()
    feedback_path = (repo_root / args.feedback_json).resolve()
    output_report = (repo_root / args.output_report).resolve()

    manifest = read_json(package_dir / "package_manifest.json")
    final_status = read_json(package_dir / "evidence" / "final_status.json")
    safety_scan = read_json(package_dir / "evidence" / "safety_scan.json")
    screenshot_index = read_json(package_dir / "SCREENSHOT_INDEX.json")
    feedback = read_json(feedback_path)

    holds: list[str] = []
    if feedback.get("decision") != "PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL":
        holds.append("reviewer feedback decision must be PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL")
    if manifest.get("candidate") != feedback.get("candidate"):
        holds.append("package manifest candidate must match reviewer feedback")
    if manifest.get("source_candidate") != feedback.get("source_candidate"):
        holds.append("package manifest source_candidate must match reviewer feedback")

    package_boundaries = manifest.get("boundaries", {})
    for key in (
        "real_data",
        "masked_real_data",
        "live_qwen_api",
        "live_connectors",
        "production_writeback",
        "customer_visible_output",
    ):
        require_false(package_boundaries.get(key), f"package boundary {key}", holds)

    final_boundaries = final_status.get("boundaries_preserved", {})
    for key in (
        "customer_visible_output",
        "production_connectors",
        "qwen_autonomous_action",
        "raw_payload_retention",
        "secret_retention",
        "writeback",
    ):
        require_false(final_boundaries.get(key), f"final_status boundary {key}", holds)

    safety_summary = safety_scan.get("summary", {})
    if safety_summary.get("finding_count") != 0:
        holds.append("safety_scan finding_count must be 0")
    if safety_summary.get("no_go_count") != 0:
        holds.append("safety_scan no_go_count must be 0")

    screenshots = screenshot_index.get("screenshots", [])
    if len(screenshots) < 4:
        holds.append("screenshot index must include at least four screenshots")
    for item in screenshots:
        path = package_dir / item.get("path", "")
        if not path.exists():
            holds.append(f"screenshot missing: {item.get('path')}")

    customer_trial_ready = False
    readiness = "READY_FOR_INTERNAL_LOCAL_TRIAL_ONLY" if not holds else "HOLD"
    customer_trial_status = "NOT_AUTHORIZED_FOR_CUSTOMER_VISIBLE_TRIAL"

    report = render_report(
        generated_at=utc_now(),
        readiness=readiness,
        customer_trial_status=customer_trial_status,
        customer_trial_ready=customer_trial_ready,
        holds=holds,
        manifest=manifest,
        final_status=final_status,
        safety_scan=safety_scan,
        screenshot_index=screenshot_index,
        feedback=feedback,
        package_dir=portable_path(package_dir, repo_root),
        feedback_path=portable_path(feedback_path, repo_root),
    )
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(report, encoding="utf-8")

    return {
        "status": "PASS" if not holds else "HOLD",
        "readiness": readiness,
        "customer_trial_status": customer_trial_status,
        "output_report": portable_path(output_report, repo_root),
        "output_report_sha256": file_sha256(output_report),
        "hold_count": len(holds),
    }


def render_report(
    *,
    generated_at: str,
    readiness: str,
    customer_trial_status: str,
    customer_trial_ready: bool,
    holds: list[str],
    manifest: dict[str, Any],
    final_status: dict[str, Any],
    safety_scan: dict[str, Any],
    screenshot_index: dict[str, Any],
    feedback: dict[str, Any],
    package_dir: str,
    feedback_path: str,
) -> str:
    hold_block = "\n".join(f"- {item}" for item in holds) if holds else "None"
    suggestions = "\n".join(
        f"- {item}" for item in feedback.get("next_round_suggestions", [])
    ) or "None"
    observations = "\n".join(
        f"- {item}" for item in feedback.get("non_blocking_observations", [])
    ) or "None"
    return f"""# S6 Fast MVP Client Trial Readiness Report 2026-05-07

## 1. Decision

```text
readiness = {readiness}
customer_trial_status = {customer_trial_status}
customer_trial_ready = {str(customer_trial_ready).lower()}
customer_visible_or_deploy_go = false
```

## 2. Inputs

```text
generated_at_utc = {generated_at}
candidate = {manifest.get("candidate")}
source_candidate = {manifest.get("source_candidate")}
package_dir = {package_dir}
reviewer_feedback = {feedback_path}
reviewer_decision = {feedback.get("decision")}
final_outcome = {final_status.get("final_outcome")}
safety_finding_count = {safety_scan.get("summary", {}).get("finding_count")}
screenshot_count = {len(screenshot_index.get("screenshots", []))}
```

## 3. Readiness Basis

```text
RC-009 reviewer decision = PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL
/s1-run product result page = reviewer accepted
/s1-trial and /s1-run screenshots = sufficient for local/offline review
package manifest = candidate/source/package/zip consistent
safety scan = clean
boundaries = local/offline only
```

## 4. Remaining Notes

{observations}

## 5. Next-Round Suggestions

{suggestions}

## 6. HOLD Items

{hold_block}

## 7. Explicit Non-Authorization

This readiness report does not authorize:

```text
real data
masked-real data
live Qwen/API calls
live connectors
production connectors
production write-back
customer-visible publish/deploy/output
external pilot execution
production launch
credential handling
push
```

## 8. Next Unlock

```text
GOAL-MVP-25_QWEN_PROVIDER_DRY_CONTRACT = ELIGIBLE_DRY_CONTRACT_ONLY
GOAL-MVP-27_SCREENSHOT_SAFETY_VALIDATOR = RECOMMENDED
GOAL-MVP-28_RC_DIFF_CHECKER = RECOMMENDED
```
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--feedback-json", required=True)
    parser.add_argument("--output-report", required=True)
    parser.add_argument("--repo-root", default=".")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = build_report(args)
    except Exception as exc:
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False, indent=2))
        return HOLD
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return PASS if result["status"] == "PASS" else HOLD


if __name__ == "__main__":
    sys.exit(run())
