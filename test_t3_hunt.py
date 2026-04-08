from _project_bootstrap import bootstrap

bootstrap()

from backend.tests.test_t3_hunt import *  # noqa: F401,F403


if __name__ == "__main__":
    import unittest

    unittest.main(module="backend.tests.test_t3_hunt", verbosity=2)
