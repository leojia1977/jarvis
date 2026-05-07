#!/usr/bin/env python3
"""Pick the next executable SecuPilot MVP Goal candidate."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20
OPEN_STATUSES = {"OPEN", "BACKLOG_OPEN"}
PRIORITY_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

QUEUE_ITEMS = (
    {
        "queue_key": "GOAL-MVP-NEXT_MANIFEST_SELF_HASH",
        "suffix": "MANIFEST_SELF_HASH",
        "match": "MANIFEST_SELF_HASH",
        "goal_type": "package",
        "profile": "PACKAGE",
    },
    {
        "queue_key": "GOAL-MVP-NEXT_RESULT_PAGE_FIELD_DOWNSHIFT",
        "suffix": "RESULT_PAGE_FIELD_DOWNSHIFT",
        "match": "RESULT_PAGE_FIELD_DOWNSHIFT",
        "goal_type": "page",
        "profile": "UI_PAGE",
    },
    {
        "queue_key": "GOAL-MVP-NEXT_CASE_TITLE_CLEANUP",
        "suffix": "CASE_TITLE_CLEANUP",
        "match": "CASE_TITLE_CLEANUP",
        "goal_type": "package",
        "profile": "PACKAGE",
    },
    {
        "queue_key": "GOAL-MVP-NEXT_GOAL_PICKER",
        "suffix": "NEXT_GOAL_PICKER",
        "match": "NEXT_GOAL_PICKER",
        "goal_type": "script",
        "profile": "SCRIPT_GOAL_PICKER",
    },
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_latest_backlog(repo_root: Path) -> Path | None:
    candidates = sorted(
        repo_root.glob("artifacts/product_backlog/**/reviewer_backlog.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def list_goal_cards(repo_root: Path) -> list[Path]:
    return sorted(repo_root.glob("docs/goals/GOAL-MVP-*.md"))


def next_goal_index(goal_cards: list[Path]) -> int:
    max_index = 0
    pattern = re.compile(r"GOAL-MVP-(\d+)_")
    for path in goal_cards:
        match = pattern.search(path.stem.upper())
        if match:
            max_index = max(max_index, int(match.group(1)))
    return max_index + 1 if max_index else 1


def choose_open_item(items: list[dict[str, Any]]) -> dict[str, Any] | None:
    open_items = []
    for item in items:
        status = str(item.get("status", "")).upper()
        if status in OPEN_STATUSES:
            open_items.append(item)
    if not open_items:
        return None

    def sort_key(item: dict[str, Any]) -> tuple[int, str]:
        priority = str(item.get("priority", "P3")).upper()
        return (PRIORITY_RANK.get(priority, 99), str(item.get("id", "")))

    open_items.sort(key=sort_key)
    return open_items[0]


def infer_profile(item: dict[str, Any]) -> str:
    text = f"{item.get('title', '')} {item.get('description', '')}".lower()
    if any(token in text for token in ("/s1-run", "result", "first-screen", "首屏", "文案", "tooltip")):
        return "UI_PAGE"
    if any(
        token in text
        for token in ("manifest", "candidate", "source", "package", "zip", "截图", "screenshot", "case title")
    ):
        return "PACKAGE"
    return "SCRIPT_GENERIC"


def profile_contract(
    profile: str,
    goal_id: str,
    date_tag: str,
    backlog_path: str | None,
) -> dict[str, Any]:
    goal_card = f"docs/goals/{goal_id}.md"
    closeout = f"docs/S6_FAST_MVP_{goal_id}_{date_tag}.md"
    if profile == "UI_PAGE":
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/s1/S1ArtifactView.tsx",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/s1-artifact-viewer.spec.ts",
                "frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "target UI field remains unchanged after patch",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "PACKAGE":
        return {
            "goal_type": "package",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_local_offline_trial_rc.py",
                "backend/tests/test_build_local_offline_trial_rc.py",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_local_offline_trial_rc",
                "py -3 scripts/build_local_offline_trial_rc.py --help",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "package builder behavior changes outside selected backlog scope",
                "unit test fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "SCRIPT_GOAL_PICKER":
        return {
            "goal_type": "script",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/pick_next_mvp_goal.py",
                "backend/tests/test_pick_next_mvp_goal.py",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_pick_next_mvp_goal",
                "py -3 scripts/pick_next_mvp_goal.py --repo-root . --output-json artifacts/product_acceleration/next_goal_candidate.json --output-md artifacts/product_acceleration/next_goal_candidate.md",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "latest backlog cannot be parsed as JSON",
                "script output misses exact_files or acceptance_commands",
                "unit test fails twice in the same way",
            ],
        }
    return {
        "goal_type": "script",
        "goal_card_path": goal_card,
        "closeout_path": closeout,
        "exact_files": [goal_card, "scripts/close_reviewer_backlog_items.py", closeout],
        "acceptance_commands": [
            f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
            "py -3 scripts/close_reviewer_backlog_items.py --help",
            "git -c core.quotepath=false diff --check",
        ],
        "hold_conditions": [
            "backlog item cannot map to a bounded execution profile",
            "script command fails",
            "scope expands beyond listed files",
        ],
    }


def backlog_candidate(
    repo_root: Path,
    goal_index: int,
    backlog_path: Path,
    item: dict[str, Any],
) -> dict[str, Any]:
    item_id = str(item.get("id", "UNKNOWN")).replace("-", "_")
    goal_id = f"GOAL-MVP-{goal_index:02d}_BACKLOG_ITEM_{item_id}"
    date_tag = datetime.now().strftime("%Y_%m_%d")
    profile = infer_profile(item)
    contract = profile_contract(profile, goal_id, date_tag, backlog_path.as_posix())
    return {
        "selection_mode": "BACKLOG_OPEN_ITEM",
        "source_backlog_json": backlog_path.as_posix(),
        "selected_backlog_item": {
            "id": item.get("id"),
            "title": item.get("title"),
            "status": item.get("status"),
            "priority": item.get("priority"),
            "category": item.get("category"),
        },
        "candidate_goal": {
            "queue_key": "REVIEWER_BACKLOG_OPEN_ITEM",
            "goal_id": goal_id,
            "goal_type": contract["goal_type"],
            "statement": str(item.get("title", "")).strip(),
            "exact_files": contract["exact_files"],
            "acceptance_commands": contract["acceptance_commands"],
            "hold_conditions": contract["hold_conditions"],
            "followup_note": "If implementation commit lands, run one follow-up backlog closeout Goal for this exact item.",
        },
    }


def queue_candidate(repo_root: Path, goal_index: int, goal_cards: list[Path]) -> dict[str, Any]:
    existing_names = [path.stem.upper() for path in goal_cards]
    date_tag = datetime.now().strftime("%Y_%m_%d")
    for item in QUEUE_ITEMS:
        if any(item["match"] in name for name in existing_names):
            continue
        goal_id = f"GOAL-MVP-{goal_index:02d}_{item['suffix']}"
        contract = profile_contract(item["profile"], goal_id, date_tag, None)
        return {
            "selection_mode": "QUEUE_FALLBACK",
            "candidate_goal": {
                "queue_key": item["queue_key"],
                "goal_id": goal_id,
                "goal_type": contract["goal_type"],
                "statement": f"Execute {item['queue_key']} as the next bounded product-acceleration Goal.",
                "exact_files": contract["exact_files"],
                "acceptance_commands": contract["acceptance_commands"],
                "hold_conditions": contract["hold_conditions"],
            },
        }

    goal_id = f"GOAL-MVP-{goal_index:02d}_QUEUE_EXHAUSTED"
    contract = profile_contract("SCRIPT_GENERIC", goal_id, date_tag, None)
    return {
        "selection_mode": "CONCRETE_BLOCKER",
        "candidate_goal": {
            "queue_key": "QUEUE_EXHAUSTED_REQUIRE_NEW_PRODUCT_GOAL",
            "goal_id": goal_id,
            "goal_type": contract["goal_type"],
            "statement": "All predefined queue goals appear completed; require one new explicit product-acceleration goal definition.",
            "exact_files": contract["exact_files"],
            "acceptance_commands": contract["acceptance_commands"],
            "hold_conditions": contract["hold_conditions"],
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    candidate = payload["candidate_goal"]
    selected = payload.get("selected_backlog_item")
    selected_block = ""
    if selected:
        selected_block = (
            "## Selected Backlog Item\n\n"
            f"- id: {selected.get('id')}\n"
            f"- priority: {selected.get('priority')}\n"
            f"- status: {selected.get('status')}\n"
            f"- title: {selected.get('title')}\n\n"
        )
    commands = "\n".join(f"- {line}" for line in candidate["acceptance_commands"])
    hold_conditions = "\n".join(f"- {line}" for line in candidate["hold_conditions"])
    files = "\n".join(f"- {path}" for path in candidate["exact_files"])
    return (
        "# SecuPilot Next MVP Goal Candidate\n\n"
        f"Generated at: {payload['generated_at_local']}\n\n"
        f"Selection mode: {payload['selection_mode']}\n\n"
        f"{selected_block}"
        "## Candidate Goal\n\n"
        f"- queue_key: {candidate['queue_key']}\n"
        f"- goal_id: {candidate['goal_id']}\n"
        f"- goal_type: {candidate['goal_type']}\n"
        f"- statement: {candidate['statement']}\n\n"
        "## Exact Files\n\n"
        f"{files}\n\n"
        "## Acceptance Commands\n\n"
        f"{commands}\n\n"
        "## HOLD Conditions\n\n"
        f"{hold_conditions}\n"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    output_json = (repo_root / args.output_json).resolve()
    output_md = (repo_root / args.output_md).resolve()

    goal_cards = list_goal_cards(repo_root)
    goal_index = next_goal_index(goal_cards)

    latest_backlog = find_latest_backlog(repo_root)
    payload_base = {
        "schema_version": "secupilot.next_mvp_goal_candidate.v1",
        "generated_at_local": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "latest_backlog_json": latest_backlog.as_posix() if latest_backlog else None,
    }

    try:
        if latest_backlog:
            backlog_payload = read_json(latest_backlog)
            if not isinstance(backlog_payload, dict):
                raise ValueError(f"backlog is not a JSON object: {latest_backlog.as_posix()}")
            items = backlog_payload.get("items", [])
            if not isinstance(items, list):
                raise ValueError(f"backlog items is not a list: {latest_backlog.as_posix()}")
            selected = choose_open_item(items)
            if selected:
                picked = backlog_candidate(repo_root, goal_index, latest_backlog, selected)
            else:
                picked = queue_candidate(repo_root, goal_index, goal_cards)
        else:
            picked = queue_candidate(repo_root, goal_index, goal_cards)
    except Exception as exc:
        error_payload = {
            "status": "HOLD",
            "error": str(exc),
            **payload_base,
        }
        print(json.dumps(error_payload, ensure_ascii=False, indent=2))
        return HOLD

    payload = {"status": "PASS", **payload_base, **picked}
    write_json(output_json, payload)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(payload), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
