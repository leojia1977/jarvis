from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
BACKEND_ROOT = ROOT / "backend"


def bootstrap() -> tuple[Path, Path]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    if str(BACKEND_ROOT) not in sys.path:
        sys.path.insert(0, str(BACKEND_ROOT))
    return ROOT, BACKEND_ROOT
