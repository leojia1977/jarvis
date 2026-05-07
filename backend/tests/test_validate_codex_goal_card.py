import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import validate_codex_goal_card as validator  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]


def valid_goal_text(goal_id: str = "GOAL-MVP-99_VALID_TEST") -> str:
    return f"""# {goal_id}

## Goal ID

```text
{goal_id}
```

## Goal type

```text
validator
```

## Goal statement

```text
Validate a bounded executable Goal contract for local SecuPilot work.
```

## Primary executable object

```text
validator=scripts/example_validator.py
test=backend/tests/test_example_validator.py
```

## Inputs

```text
docs/goals/example.md
```

## Output paths

```text
scripts/example_validator.py
backend/tests/test_example_validator.py
```

## Allowed files

```text
scripts/example_validator.py
backend/tests/test_example_validator.py
```

## Allowed scope

```text
local/offline only
local validator script
local test output
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
secrets/tokens/auth headers/raw customer logs
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/example_validator.py docs/goals/example.md
py -3 -m unittest backend.tests.test_example_validator
```

## HOLD conditions

```text
tests fail twice in the same way
safety sentinel is observed
```

## Rollback

```text
revert scripts/example_validator.py
revert backend/tests/test_example_validator.py
preserve failure evidence
```

## Evidence contract

```text
command transcript or test output
closeout note with exact commands
```

## Safety sentinels

```text
no Authorization: / Bearer / refresh_token in artifacts
no writeback_enabled=true
no customer_visible_output=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-100_NEXT_VALID_TEST.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-99 valid test
do not push unless separately authorized
```
"""


class ValidateCodexGoalCardTests(unittest.TestCase):
    def write_goal(self, text: str, name: str = "GOAL-MVP-99_VALID_TEST.md") -> Path:
        self.tmpdir = tempfile.TemporaryDirectory()
        path = Path(self.tmpdir.name) / name
        path.write_text(text, encoding="utf-8")
        return path

    def tearDown(self):
        tmpdir = getattr(self, "tmpdir", None)
        if tmpdir is not None:
            tmpdir.cleanup()

    def run_cli(self, paths: list[str]) -> int:
        with redirect_stdout(StringIO()):
            return validator.run(paths)

    def test_repo_goal_cards_pass(self):
        for relative in (
            "docs/goals/GOAL-SYS-01_CODEX_GOAL_CONTRACT_LINTER.md",
            "docs/goals/GOAL-MVP-22_RESULT_PAGE.md",
        ):
            with self.subTest(relative=relative):
                errors = validator.validate_goal_card(REPO_ROOT / relative)
                self.assertEqual([], errors)

    def test_valid_goal_passes(self):
        path = self.write_goal(valid_goal_text())

        self.assertEqual([], validator.validate_goal_card(path))

    def test_missing_executable_object_holds(self):
        text = valid_goal_text().replace(
            "validator=scripts/example_validator.py\n"
            "test=backend/tests/test_example_validator.py",
            "bounded local validation work",
        )
        path = self.write_goal(text)

        errors = validator.validate_goal_card(path)

        self.assertTrue(any("executable marker" in error for error in errors))

    def test_missing_acceptance_command_holds(self):
        text = valid_goal_text().replace(
            "py -3 scripts/example_validator.py docs/goals/example.md\n"
            "py -3 -m unittest backend.tests.test_example_validator",
            "Run the validator manually.",
        )
        path = self.write_goal(text)

        errors = validator.validate_goal_card(path)

        self.assertTrue(any("acceptance commands" in error for error in errors))

    def test_broad_planning_goal_holds(self):
        text = valid_goal_text().replace(
            "Validate a bounded executable Goal contract for local SecuPilot work.",
            "继续完善 SecuPilot.",
        )
        path = self.write_goal(text)

        errors = validator.validate_goal_card(path)

        self.assertTrue(any("planning-only" in error for error in errors))

    def test_missing_safety_sentinels_holds(self):
        text = valid_goal_text().replace(
            "no Authorization: / Bearer / refresh_token in artifacts\n"
            "no writeback_enabled=true\n"
            "no customer_visible_output=true",
            "Safety will be considered during review.",
        )
        path = self.write_goal(text)

        errors = validator.validate_goal_card(path)

        self.assertTrue(any("safety sentinels" in error for error in errors))

    def test_missing_forbidden_boundary_holds(self):
        text = valid_goal_text().replace("live Qwen/API calls\n", "")
        path = self.write_goal(text)

        errors = validator.validate_goal_card(path)

        self.assertTrue(any("live qwen" in error for error in errors))

    def test_cli_returns_pass_for_repo_cards(self):
        code = self.run_cli(
            [
                str(REPO_ROOT / "docs/goals/GOAL-SYS-01_CODEX_GOAL_CONTRACT_LINTER.md"),
                str(REPO_ROOT / "docs/goals/GOAL-MVP-22_RESULT_PAGE.md"),
            ]
        )

        self.assertEqual(validator.PASS, code)

    def test_cli_returns_hold_for_invalid_card(self):
        path = self.write_goal(valid_goal_text().replace("Do not push.", "Push when useful."))

        code = self.run_cli([str(path)])

        self.assertEqual(validator.HOLD, code)


if __name__ == "__main__":
    unittest.main()
