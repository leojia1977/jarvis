import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import close_reviewer_backlog_items as closer  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class CloseReviewerBacklogItemsTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.backlog_json = self.root / "backlog.json"
        self.output_json = self.root / "out" / "reviewer_backlog.json"
        self.output_md = self.root / "out" / "reviewer_backlog.md"
        self.closeout_json = self.root / "out" / "reviewer_backlog_closeout.json"
        self.closeout_md = self.root / "out" / "reviewer_backlog_closeout.md"
        self.write_backlog()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_backlog(self, **overrides):
        payload = {
            "schema_version": "secupilot.reviewer_feedback_product_backlog.v1",
            "generated_at_utc": "2026-05-07T00:00:00Z",
            "candidate": "LOCAL_OFFLINE_TRIAL_RC_011_CN",
            "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_010_CN",
            "reviewer_decision": "PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL",
            "reviewer": "Jarvis",
            "items": [
                {
                    "id": "RFB-RC011-001",
                    "source_type": "next_round_suggestion",
                    "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_011_CN",
                    "source_decision": "PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL",
                    "title": "后续可继续增加中文 tooltip",
                    "description": "后续可继续增加中文 tooltip。",
                    "category": "REVIEWER_EXPERIENCE",
                    "priority": "P2",
                    "status": "BACKLOG_OPEN",
                    "owner": "SecuPilot product engineering",
                    "acceptance": ["local/offline only"],
                    "non_authorization": {
                        "customer_visible_or_deploy_go": False,
                        "live_qwen_api": False,
                        "production_writeback": False,
                    },
                },
                {
                    "id": "RFB-RC011-002",
                    "source_type": "next_round_suggestion",
                    "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_011_CN",
                    "source_decision": "PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL",
                    "title": "后续可继续弱化英文技术码的首屏存在感",
                    "description": "后续可继续弱化英文技术码的首屏存在感。",
                    "category": "REVIEWER_EXPERIENCE",
                    "priority": "P2",
                    "status": "BACKLOG_OPEN",
                    "owner": "SecuPilot product engineering",
                    "acceptance": ["local/offline only"],
                    "non_authorization": {
                        "customer_visible_or_deploy_go": False,
                        "live_qwen_api": False,
                        "production_writeback": False,
                    },
                },
            ],
            "boundaries": {
                "real_data": False,
                "masked_real_data": False,
                "live_qwen_api": False,
                "live_connectors": False,
                "production_writeback": False,
                "customer_visible_output": False,
                "push": False,
            },
            "customer_visible_or_deploy_go": False,
            "external_tracker_write": False,
        }
        payload.update(overrides)
        write_json(self.backlog_json, payload)

    def run_closer(self, *item_ids: str) -> int:
        args = [
            "--backlog-json",
            str(self.backlog_json),
            "--output-json",
            str(self.output_json),
            "--output-md",
            str(self.output_md),
            "--closeout-json",
            str(self.closeout_json),
            "--closeout-md",
            str(self.closeout_md),
            "--closed-by-goal",
            "GOAL-MVP-36_RESULT_TECH_CODE_DISCLOSURE",
            "--closed-by-commit",
            "02fa889",
            "--resolution",
            "MVP-36 added Chinese tooltips and moved raw technical codes into technical reconciliation.",
            "--repo-root",
            str(self.root),
        ]
        for item_id in item_ids:
            args.extend(["--item-id", item_id])
        with redirect_stdout(StringIO()):
            return closer.run(args)

    def test_closes_selected_items_and_writes_closeout(self):
        code = self.run_closer("RFB-RC011-001", "RFB-RC011-002")

        self.assertEqual(closer.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual(2, payload["closed_item_count"])
        self.assertTrue(all(item["status"] == "BACKLOG_CLOSED" for item in payload["items"]))
        closeout = json.loads(self.closeout_json.read_text(encoding="utf-8"))
        self.assertEqual("GOAL-MVP-36_RESULT_TECH_CODE_DISCLOSURE", closeout["closed_by_goal"])
        self.assertTrue(self.output_md.exists())

    def test_holds_when_item_id_is_missing(self):
        code = self.run_closer("RFB-RC011-999")

        self.assertEqual(closer.HOLD, code)
        self.assertFalse(self.output_json.exists())

    def test_holds_when_backlog_grants_deploy(self):
        self.write_backlog(customer_visible_or_deploy_go=True)

        code = self.run_closer("RFB-RC011-001")

        self.assertEqual(closer.HOLD, code)


if __name__ == "__main__":
    unittest.main()
