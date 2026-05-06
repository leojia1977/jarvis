#!/usr/bin/env python3
"""Refresh the Fast MVP S1 golden synthetic snapshot artifact."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import s1_closed_shadow_run


PASS = 0
HOLD = 20
ALLOWED_RUNNER_EXIT_CODES = {0, 10}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh local synthetic S1 snapshot artifacts.")
    parser.add_argument("--input", required=True, help="Synthetic qwen_fact_bundle directory.")
    parser.add_argument("--output", required=True, help="Snapshot artifact output directory.")
    parser.add_argument("--provider", choices=("fixture",), default="fixture")
    parser.add_argument("--run-id", default="S1-CLOSED-SHADOW-2026-04-30-001-SNAPSHOT")
    parser.add_argument("--no-writeback", action="store_true")
    parser.add_argument("--no-customer-visible", action="store_true")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"HOLD: snapshot input not found: {input_path}")
        return HOLD
    if not args.no_writeback:
        print("HOLD: --no-writeback assertion is required")
        return HOLD
    if not args.no_customer_visible:
        print("HOLD: --no-customer-visible assertion is required")
        return HOLD

    runner_exit = s1_closed_shadow_run.run(
        [
            "--run-id",
            args.run_id,
            "--input",
            args.input,
            "--output",
            args.output,
            "--provider",
            args.provider,
            "--no-writeback",
            "--no-customer-visible",
        ]
    )
    if runner_exit not in ALLOWED_RUNNER_EXIT_CODES:
        print(f"HOLD: snapshot runner exited with {runner_exit}")
        return HOLD

    print(f"PASS: synthetic S1 snapshot refreshed at {Path(args.output).resolve()}")
    return PASS


def main(argv: list[str] | None = None) -> int:
    return run(argv)


if __name__ == "__main__":
    sys.exit(main())
