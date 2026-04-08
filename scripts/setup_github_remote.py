from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=ROOT, check=True, shell=False, text=True, capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="GitHub remote URL")
    parser.add_argument("--remote", default="origin", help="Remote name, default: origin")
    args = parser.parse_args()

    current = subprocess.run(
        ["git", "remote", "get-url", args.remote],
        cwd=ROOT,
        shell=False,
        text=True,
        capture_output=True,
    )

    if current.returncode == 0:
        run(["git", "remote", "set-url", args.remote, args.url])
        print(f"[OK] Updated remote '{args.remote}' -> {args.url}")
    else:
        run(["git", "remote", "add", args.remote, args.url])
        print(f"[OK] Added remote '{args.remote}' -> {args.url}")

    print("[NEXT] Push with: git push -u origin main")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
