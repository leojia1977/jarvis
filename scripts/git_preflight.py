from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

FAST_COMMANDS = [
    ["py", "-3", "test_t3_hunt.py"],
    ["py", "-3", "test_secupilot_drafts.py"],
    [
        "py",
        "-3",
        "-m",
        "unittest",
        "-q",
        "backend.tests.test_t3_hunt",
        "backend.tests.test_secupilot_drafts",
        "backend.tests.test_runtime_service",
        "backend.tests.test_case_view",
        "backend.tests.test_siem_adapter_contract",
        "backend.tests.test_vendor_replay",
        "backend.tests.test_static_data_contracts",
        "backend.tests.test_static_data_adapters",
        "backend.tests.test_host_identity_resolver",
        "backend.tests.test_edr_adapter_contract",
    ],
    ["py", "-3", "selfcheck_t1_t5.py"],
]

RELEASE_COMMANDS = [
    ["py", "-3", "scripts/build_claude_review_pack.py"],
    ["py", "-3", "scripts/package_release.py"],
    ["py", "-3", "scripts/verify_release.py"],
]


def run_commands(commands: list[list[str]]) -> int:
    for argv in commands:
        print(f"[RUN] {' '.join(argv)}")
        proc = subprocess.run(argv, cwd=ROOT, shell=False)
        if proc.returncode != 0:
            print(f"[FAIL] {' '.join(argv)}")
            return proc.returncode
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["fast", "release", "all"], default="fast")
    args = parser.parse_args()

    if args.mode == "fast":
        return run_commands(FAST_COMMANDS)
    if args.mode == "release":
        return run_commands(RELEASE_COMMANDS)
    return run_commands(FAST_COMMANDS + RELEASE_COMMANDS)


if __name__ == "__main__":
    raise SystemExit(main())
