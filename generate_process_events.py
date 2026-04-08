from _project_bootstrap import bootstrap

bootstrap()

from scripts.generate_process_events import *  # noqa: F401,F403


if __name__ == "__main__":
    raise SystemExit(main())
