#!/usr/bin/env python3
"""Validate SecuPilot Codex Goal cards as executable engineering contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PASS = 0
HOLD = 20

ALLOWED_GOAL_TYPES = {
    "page",
    "script",
    "interface",
    "interface/api",
    "package",
    "test-report",
    "run-artifact",
    "validator",
}

REQUIRED_SECTIONS = (
    "goal id",
    "goal type",
    "goal statement",
    "primary executable object",
    "inputs",
    "output paths",
    "allowed files",
    "allowed scope",
    "forbidden scope",
    "acceptance commands",
    "hold conditions",
    "rollback",
    "evidence contract",
    "safety sentinels",
    "merge rule",
    "next unlock",
    "commit posture",
)

EXECUTABLE_MARKERS = (
    "page=",
    "script=",
    "interface=",
    "api=",
    "package=",
    "test=",
    "artifact=",
    "validator=",
    "report=",
    "run-artifact=",
    "closeout=",
)

COMMAND_PREFIXES = (
    "py ",
    "python ",
    "npm ",
    "npx ",
    "node ",
    "powershell",
    "pwsh ",
    "git ",
)

FORBIDDEN_SCOPE_SENTINELS = (
    ("real data",),
    ("masked-real data", "masked real data"),
    ("live qwen",),
    ("connector",),
    ("production write-back", "production writeback"),
    ("customer-visible", "customer visible"),
    ("secret", "token", "auth header"),
)

EVIDENCE_MARKERS = (
    "command transcript",
    "test output",
    "artifact manifest",
    "package index",
    "screenshot",
    "closeout",
    "report",
    "sha256",
)

SAFETY_MARKERS = (
    "no ",
    "false",
    "!=",
    "forbidden",
    "customer_visible_output",
    "production_writeback",
    "writeback_enabled",
    "authorization",
    "bearer",
    "token",
)

INVALID_GOAL_PATTERNS = (
    "继续完善",
    "推进上线准备",
    "整理下一阶段规划",
    "补充治理材料",
    "优化体验",
    "做好上线准备",
    "continue improving",
    "improve secupilot",
    "prepare launch",
)

GOAL_ID_PATTERN = re.compile(r"^GOAL-[A-Z0-9]+-\d{2,}_[A-Z0-9_]+$")


def normalize_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def first_content_line(block: str) -> str:
    for line in block.splitlines():
        stripped = line.strip().strip("`").strip()
        if stripped and stripped != "text":
            return stripped
    return ""


def strip_markup(line: str) -> str:
    return line.strip().lstrip("-*0123456789. ").strip("`").strip()


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in text.splitlines():
        if raw_line.startswith("## "):
            current = normalize_heading(raw_line[3:])
            sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(raw_line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def has_command(block: str) -> bool:
    for raw_line in block.splitlines():
        line = strip_markup(raw_line).lower()
        if any(line.startswith(prefix) for prefix in COMMAND_PREFIXES):
            return True
    return False


def contains_any(block: str, markers: tuple[str, ...]) -> bool:
    lower = block.lower()
    return any(marker.lower() in lower for marker in markers)


def validate_goal_card(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"goal card not found: {path}"]

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return [f"{path}: goal card is empty"]

    sections = parse_sections(text)
    for section in REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(f"missing required section: {section}")
        elif not first_content_line(sections[section]):
            errors.append(f"empty required section: {section}")

    if errors:
        return errors

    goal_id = first_content_line(sections["goal id"])
    if not GOAL_ID_PATTERN.match(goal_id):
        errors.append(f"invalid Goal ID: {goal_id}")
    if path.name.startswith("GOAL-") and path.stem != goal_id:
        errors.append(f"Goal ID does not match filename: {goal_id} != {path.stem}")

    goal_type = first_content_line(sections["goal type"]).lower()
    if goal_type not in ALLOWED_GOAL_TYPES:
        errors.append(f"invalid Goal type: {goal_type}")

    statement = sections["goal statement"].lower()
    if any(pattern in statement for pattern in INVALID_GOAL_PATTERNS):
        errors.append("goal statement contains broad planning-only wording")

    executable = sections["primary executable object"]
    if not contains_any(executable, EXECUTABLE_MARKERS):
        errors.append("primary executable object must include an executable marker")

    allowed_files = sections["allowed files"]
    if not re.search(r"[/\\*]|\.[A-Za-z0-9]+", allowed_files):
        errors.append("allowed files must name exact files, directories, or globs")

    forbidden_scope = sections["forbidden scope"].lower()
    for alternatives in FORBIDDEN_SCOPE_SENTINELS:
        if not any(item in forbidden_scope for item in alternatives):
            errors.append(f"forbidden scope missing sentinel: {'/'.join(alternatives)}")

    acceptance = sections["acceptance commands"]
    if not has_command(acceptance):
        errors.append("acceptance commands must include at least one runnable command")

    evidence = sections["evidence contract"]
    if not contains_any(evidence, EVIDENCE_MARKERS):
        errors.append("evidence contract must name verifiable artifact or test evidence")

    safety = sections["safety sentinels"]
    if not contains_any(safety, SAFETY_MARKERS):
        errors.append("safety sentinels must include machine-checkable safety markers")

    merge_rule = sections["merge rule"].lower()
    if "do not push" not in merge_rule:
        errors.append("merge rule must include Do not push")
    if "pass" not in merge_rule:
        errors.append("merge rule must require passing acceptance commands")
    if "unrelated" not in merge_rule:
        errors.append("merge rule must reject unrelated changes")

    next_unlock = sections["next unlock"].lower()
    if "unlock" not in next_unlock or "hold" not in next_unlock:
        errors.append("next unlock must state PASS unlock and HOLD behavior")

    commit_posture = sections["commit posture"].lower()
    if "commit" not in commit_posture:
        errors.append("commit posture must include commit wording")
    if "do not push" not in commit_posture:
        errors.append("commit posture must include Do not push")

    return errors


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("goal_cards", nargs="+", type=Path)
    args = parser.parse_args(argv)

    results = []
    all_errors: list[str] = []
    for goal_card in args.goal_cards:
        errors = validate_goal_card(goal_card)
        results.append(
            {
                "path": goal_card.as_posix(),
                "status": "HOLD" if errors else "PASS",
                "errors": errors,
            }
        )
        all_errors.extend(f"{goal_card}: {error}" for error in errors)

    payload = {
        "schema_version": "secupilot.codex_goal_validator.v1",
        "status": "HOLD" if all_errors else "PASS",
        "checked": len(args.goal_cards),
        "results": results,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return HOLD if all_errors else PASS


if __name__ == "__main__":
    sys.exit(run())
