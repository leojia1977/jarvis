from _project_bootstrap import bootstrap

bootstrap()

from backend.tests.test_secupilot_drafts import *  # noqa: F401,F403


if __name__ == "__main__":
    import unittest

    unittest.main(module="backend.tests.test_secupilot_drafts")
