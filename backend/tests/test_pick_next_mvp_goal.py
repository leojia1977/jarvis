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
        self.assertEqual("GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE", payload["candidate_goal"]["queue_key"])
        self.assertIn("frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts", payload["candidate_goal"]["exact_files"])
        self.assertTrue(
            any("LOCAL_OFFLINE_TRIAL_RC_016_CN" in command for command in payload["candidate_goal"]["acceptance_commands"])
        )

    def test_queue_advances_to_trial_report_after_prior_pool_items_exist(self):
        for name in (
            "GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE.md",
            "GOAL-MVP-62_ZIP_TAMPER_NEGATIVE_TEST.md",
            "GOAL-MVP-63_PRODUCT_ACCELERATION_POOL_PICKER.md",
            "GOAL-MVP-64_CLIENT_TRIAL_HOME_PRODUCTIZATION.md",
        ):
            (self.root / "docs" / "goals" / name).write_text("# placeholder\n", encoding="utf-8")
        write_json(self.backlog_json, {"items": []})

        code = self.run_picker()

        self.assertEqual(picker.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("QUEUE_FALLBACK", payload["selection_mode"])
        self.assertEqual("GOAL-MVP-65_LOCAL_OFFLINE_TRIAL_REPORT", payload["candidate_goal"]["queue_key"])
        self.assertIn("scripts/build_client_trial_readiness_report.py", payload["candidate_goal"]["exact_files"])

    def test_queue_advances_to_role_based_home_after_mvp61_to_66_exist(self):
        for name in (
            "GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE.md",
            "GOAL-MVP-62_ZIP_TAMPER_NEGATIVE_TEST.md",
            "GOAL-MVP-63_PRODUCT_ACCELERATION_POOL_PICKER.md",
            "GOAL-MVP-64_CLIENT_TRIAL_HOME_PRODUCTIZATION.md",
            "GOAL-MVP-65_LOCAL_OFFLINE_TRIAL_REPORT.md",
            "GOAL-MVP-66_RC_PACKAGE_SELF_REVIEW_REPORT.md",
        ):
            (self.root / "docs" / "goals" / name).write_text("# placeholder\n", encoding="utf-8")
        write_json(self.backlog_json, {"items": []})

        code = self.run_picker()

        self.assertEqual(picker.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("QUEUE_FALLBACK", payload["selection_mode"])
        self.assertEqual("GOAL-MVP-67_ROLE_BASED_TRIAL_HOME", payload["candidate_goal"]["queue_key"])
        self.assertIn("frontend/src/secupilot/s1/S1LocalTrialView.tsx", payload["candidate_goal"]["exact_files"])
        self.assertTrue(any("engineer" in condition for condition in payload["candidate_goal"]["hold_conditions"]))

    def test_queue_advances_to_internal_trial_kpi_after_product_experience_items_exist(self):
        for index, suffix in (
            (61, "RC016_SCREENSHOT_EXPECTED_CANDIDATE"),
            (62, "ZIP_TAMPER_NEGATIVE_TEST"),
            (63, "PRODUCT_ACCELERATION_POOL_PICKER"),
            (64, "CLIENT_TRIAL_HOME_PRODUCTIZATION"),
            (65, "LOCAL_OFFLINE_TRIAL_REPORT"),
            (66, "RC_PACKAGE_SELF_REVIEW_REPORT"),
            (67, "ROLE_BASED_TRIAL_HOME"),
            (68, "INCIDENT_DETAIL_PRODUCT_PAGE"),
            (69, "RECOMMENDED_ACTION_CARDS"),
            (70, "USER_FEEDBACK_LOOP"),
            (71, "QWEN_DRY_PROVIDER_UI"),
            (72, "QWEN_CLOUD_CONTRACT_MOCK"),
            (73, "PRIVATE_DEPLOY_PACKAGE_STRUCTURE"),
            (74, "CUSTOMER_TRIAL_README_AND_LAUNCHER"),
        ):
            (self.root / "docs" / "goals" / f"GOAL-MVP-{index}_{suffix}.md").write_text(
                "# placeholder\n", encoding="utf-8"
            )
        write_json(self.backlog_json, {"items": []})

        code = self.run_picker()

        self.assertEqual(picker.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("QUEUE_FALLBACK", payload["selection_mode"])
        self.assertEqual("GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT", payload["candidate_goal"]["queue_key"])
        self.assertIn("scripts/build_internal_trial_kpi_report.py", payload["candidate_goal"]["exact_files"])

    def test_private_preview_reset_skips_legacy_queue_items(self):
        (self.root / "docs" / "goals" / "GOAL-MVP-94_PRIVATE_PREVIEW_SHELL_ROUTE_MAP.md").write_text(
            "# placeholder\n", encoding="utf-8"
        )
        write_json(self.backlog_json, {"items": []})

        code = self.run_picker()

        self.assertEqual(picker.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("QUEUE_FALLBACK", payload["selection_mode"])
        self.assertEqual("GOAL-MVP-95_PRIVATE_PREVIEW_LAUNCH_SHELL", payload["candidate_goal"]["queue_key"])
        self.assertEqual("GOAL-MVP-95_PRIVATE_PREVIEW_LAUNCH_SHELL", payload["candidate_goal"]["goal_id"])
        self.assertIn("scripts/launch_s1_local_offline_trial.ps1", payload["candidate_goal"]["exact_files"])
        self.assertTrue(
            any("local-offline-trial-rc-019-cn-review" in command for command in payload["candidate_goal"]["acceptance_commands"])
        )

    def test_private_preview_lane_continues_after_rc_package_refresh(self):
        for name in (
            "GOAL-MVP-94_PRIVATE_PREVIEW_SHELL_ROUTE_MAP.md",
            "GOAL-MVP-95_PRIVATE_PREVIEW_LAUNCH_SHELL.md",
            "GOAL-MVP-96_PRIVATE_PREVIEW_ROUTE_MAP_INDEX.md",
            "GOAL-MVP-97_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW.md",
            "GOAL-MVP-98_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH.md",
        ):
            (self.root / "docs" / "goals" / name).write_text("# placeholder\n", encoding="utf-8")
        write_json(self.backlog_json, {"items": []})

        code = self.run_picker()

        self.assertEqual(picker.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("QUEUE_FALLBACK", payload["selection_mode"])
        self.assertEqual("GOAL-MVP-101_PRIVATE_PREVIEW_HEALTHCHECK", payload["candidate_goal"]["queue_key"])
        self.assertIn("scripts/check_private_preview_health.py", payload["candidate_goal"]["exact_files"])
        self.assertTrue(
            any("local-offline-trial-rc-020-cn-review" in command for command in payload["candidate_goal"]["acceptance_commands"])
        )

    def test_private_preview_lane_advances_to_product_path_smoke(self):
        for name in (
            "GOAL-MVP-94_PRIVATE_PREVIEW_SHELL_ROUTE_MAP.md",
            "GOAL-MVP-95_PRIVATE_PREVIEW_LAUNCH_SHELL.md",
            "GOAL-MVP-96_PRIVATE_PREVIEW_ROUTE_MAP_INDEX.md",
            "GOAL-MVP-97_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW.md",
            "GOAL-MVP-98_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH.md",
            "GOAL-MVP-99_PRIVATE_PREVIEW_HEALTHCHECK.md",
        ):
            (self.root / "docs" / "goals" / name).write_text("# placeholder\n", encoding="utf-8")
        write_json(self.backlog_json, {"items": []})

        code = self.run_picker()

        self.assertEqual(picker.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("GOAL-MVP-102_HOME_TO_INCIDENT_E2E_SMOKE", payload["candidate_goal"]["queue_key"])
        self.assertIn("frontend/tests/e2e/private-preview-product-path.spec.ts", payload["candidate_goal"]["exact_files"])
        self.assertTrue(any("playwright" in command for command in payload["candidate_goal"]["acceptance_commands"]))

    def test_private_preview_lane_exhausts_only_after_extended_pool(self):
        suffixes = (
            "PRIVATE_PREVIEW_SHELL_ROUTE_MAP",
            "PRIVATE_PREVIEW_LAUNCH_SHELL",
            "PRIVATE_PREVIEW_ROUTE_MAP_INDEX",
            "PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW",
            "PRIVATE_PREVIEW_RC_PACKAGE_REFRESH",
            "PRIVATE_PREVIEW_HEALTHCHECK",
            "HOME_TO_INCIDENT_E2E_SMOKE",
            "CUSTOMER_TASK_FLOW_REPORT",
            "FEEDBACK_TO_BACKLOG_SYNC",
            "PRIVATE_DEPLOY_PRECHECK_REPORT",
            "QWEN_DRY_ERROR_STATE_UI",
            "TRIAL_SCREENSHOT_PACKAGE_BUILDER",
            "PRODUCT_COPY_BOUNDARY_SCANNER",
            "RC_REVIEW_HANDOFF_AUTOBUILDER",
            "WINDOWS_START_STOP_SCRIPT_VALIDATOR",
            "CUSTOMER_README_PRODUCT_COPY_REFRESH",
            "PRODUCT_BACKLOG_PRIORITIZER",
            "CLOUD_MODEL_LATENCY_REPORT",
            "PRIVATE_PREVIEW_ROUTE_COVERAGE_REPORT",
            "INCIDENT_WORKBENCH_RC_PACKAGE",
        )
        for index, suffix in enumerate(suffixes, start=94):
            (self.root / "docs" / "goals" / f"GOAL-MVP-{index}_{suffix}.md").write_text(
                "# placeholder\n", encoding="utf-8"
            )
        write_json(self.backlog_json, {"items": []})

        code = self.run_picker()

        self.assertEqual(picker.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("CONCRETE_BLOCKER", payload["selection_mode"])
        self.assertEqual("QUEUE_EXHAUSTED_REQUIRE_NEW_PRODUCT_GOAL", payload["candidate_goal"]["queue_key"])

    def test_holds_when_backlog_items_is_not_list(self):
        write_json(self.backlog_json, {"items": {"bad": "shape"}})

        code = self.run_picker()

        self.assertEqual(picker.HOLD, code)
        self.assertFalse(self.output_json.exists())


if __name__ == "__main__":
    unittest.main()
