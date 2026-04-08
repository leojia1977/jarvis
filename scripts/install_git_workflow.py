from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(argv: list[str]) -> None:
    subprocess.run(argv, cwd=ROOT, check=True, shell=False)


def main() -> int:
    git_dir = ROOT / ".git"
    if not git_dir.exists():
        run(["git", "init", "-b", "main"])

    run(["git", "config", "core.hooksPath", ".githooks"])
    run(["git", "config", "commit.template", ".gitmessage.txt"])

    print(f"[OK] Git repository ready at: {ROOT}")
    print("[OK] core.hooksPath = .githooks")
    print("[OK] commit.template = .gitmessage.txt")
    print("[NEXT] Set or confirm user.name and user.email before your first commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
