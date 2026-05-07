import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import pick_next_mvp_goal as picker  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class PickNextMvpGoalTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.output_json = self.root / "artifacts" / "next_goal_candidate.json"
        self.output_md = self.root / "artifacts" / "next_goal_candidate.md"
        (self.root / "docs" / "goals").mkdir(parents=True, exist_ok=True)
        (self.root / "docs" / "goals" / "GOAL-MVP-55_MANIFEST_SELF_HASH.md").write_text(
            "# placeholder\n", encoding="utf-8"
        )
        (self.root / "docs" / "goals" / "GOAL-MVP-47_RESULT_PAGE_FIELD_DOWNSHIFT.md").write_text(
            "# placeholder\n", encoding="utf-8"
        )
        (self.root / "docs" / "goals" / "GOAL-MVP-49_CASE_TITLE_CLEANUP.md").write_text(
            "# placeholder\n", encoding="utf-8"
        )
        self.backlog_json = (
            self.root
            / "artifacts"
            / "product_backlog"
            / "local-offline-trial-rc-999-cn-review"
            / "reviewer_backlog.json"
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def run_picker(self) -> int:
        with redirect_stdout(StringIO()):
            return picker.run(
                [
                    "--repo-root",
                    str(self.root),
                    "--output-json",
                    str(self.output_json.relative_to(self.root)),
                    "--output-md",
                    str(self.output_md.relative_to(self.root)),
                ]
            )

    def test_prefers_latest_open_backlog_item(self):
        write_json(
            self.backlog_json,
            {
                "items": [
                    {
                        "id": "RFB-RC999-002",
                        "title": "Later open item",
                        "description": "fallback",
                        "status": "BACKLOG_OPEN",
                        "priority": "P3",
                        "category": "REVIEWER_EXPERIENCE",
                    },
                    {
                        "id": "RFB-RC999-001",
                        "title": "Move /s1-run fields into technical summary",
                        "description": "result page refinement",
                        "status": "BACKLOG_OPEN",
                        "priority": "P1",
                        "category": "RESULT_PAGE_UX",
                    },
                ]
            },
        )

        code = self.run_picker()

        self.assertEqual(picker.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("BACKLOG_OPEN_ITEM", payload["selection_mode"])
        self.assertEqual("RFB-RC999-001", payload["selected_backlog_item"]["id"])
        self.assertIn("frontend/src/secupilot/s1/S1ArtifactView.tsx", payload["candidate_goal"]["exact_files"])

    def test_falls_back_to_queue_when_no_open_items(self):
        write_json(
            self.backlog_json,
            {
                "items": [
                    {
                        "id": "RFB-RC999-001",
                        "title": "already done",
                        "description": "closed item",
                        "status": "BACKLOG_CLOSED",
                        "priority": "P2",
                    }
                ]
            },
        )

        code = self.run_picker()

        self.assertEqual(picker.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("QUEUE_FALLBACK", payload["selection_mode"])
        self.assertEqual("GOAL-MVP-NEXT_GOAL_PICKER", payload["candidate_goal"]["queue_key"])
        self.assertIn("scripts/pick_next_mvp_goal.py", payload["candidate_goal"]["exact_files"])

    def test_holds_when_backlog_items_is_not_list(self):
        write_json(self.backlog_json, {"items": {"bad": "shape"}})

        code = self.run_picker()

        self.assertEqual(picker.HOLD, code)
        self.assertFalse(self.output_json.exists())


if __name__ == "__main__":
    unittest.main()
