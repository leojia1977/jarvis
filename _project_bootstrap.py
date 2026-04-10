import asyncio
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
BACKEND_ROOT = ROOT / "backend"


def bootstrap() -> tuple[Path, Path]:
    # The Windows proactor loop can exhaust socketpair buffers when the
    # governed gate repeatedly spins up many short-lived asyncio event loops
    # across subprocess-backed test runs. The selector policy is stable for
    # SecuPilot's current test/runtime patterns and keeps verification
    # deterministic on Windows.
    if sys.platform == "win32":
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except AttributeError:
            pass
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    if str(BACKEND_ROOT) not in sys.path:
        sys.path.insert(0, str(BACKEND_ROOT))
    return ROOT, BACKEND_ROOT
