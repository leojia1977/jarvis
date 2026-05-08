import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_private_deployment_package as package_builder  # noqa: E402
from scripts import capture_customer_trial_feedback_sample as feedback_sample  # noqa: E402
from scripts import generate_private_deployment_prereq_sizing_draft as draft_builder  # noqa: E402


class GeneratePrivateDeploymentPrereqSizingDraftTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "private" / "secupilot-private"
        self.feedback_path = self.package_dir / "trial_output" / feedback_sample.DEFAULT_OUTPUT_NAME
        self.output_dir = self.package_dir / "trial_output"
        package_builder.build_package(
            package_id="secupilot-private-test",
            output_dir=self.package_dir,
            repo_root=self.root,
        )
        self.write_trial_status()
        feedback_sample.build_feedback_sample(
            package_dir=self.package_dir,
            output_path=self.feedback_path,
            repo_root=self.root,
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_trial_status(self, *, boundary_overrides=None):
        manifest = json.loads((self.package_dir / "package_manifest.json").read_text(encoding="utf-8"))
        boundaries = dict(manifest["boundaries"])
        if boundary_overrides:
            boundaries.update(boundary_overrides)
        payload = {
            "schema_version": "secupilot.local_trial_start_result.v1",
            "generated_at_utc": "2026-05-08T00:00:00Z",
            "package_id": manifest["package_id"],
            "package_type": manifest["package_type"],
            "status": "LOCAL_TRIAL_ENTRY_READY",
            "mode": "local_offline_dry_run",
            "entry_document": "CUSTOMER_TRIAL_START_HERE_中文.md",
            "entry_script": "START_SECUPILOT_LOCAL_TRIAL.cmd",
            "boundaries": boundaries,
            "boundary_check": {"status": "PASS", "output": ["BOUNDARY_CHECK_PASS"]},
        }
        status_path = self.package_dir / "trial_output" / "customer_trial_status.json"
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_generates_prereq_sizing_and_model_path_draft(self):
        draft = draft_builder.build_draft(
            package_dir=self.package_dir,
            feedback_json=self.feedback_path,
            output_dir=self.output_dir,
            repo_root=self.root,
        )

        self.assertEqual(draft_builder.SCHEMA_VERSION, draft["schema_version"])
        self.assertEqual("DRAFT_READY_FOR_INTERNAL_PRODUCT_REVIEW", draft["status"])
        self.assertEqual("GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT", draft["next_unlock"])
        self.assertEqual(3, draft["source_feedback"]["feedback_count"])
        self.assertEqual(2, len(draft["source_feedback"]["missing_information_items"]))
        self.assertIn("FB-SAMPLE-002", draft["windows_prerequisites"]["source_feedback_ids"])
        self.assertIn("FB-SAMPLE-003", draft["resource_sizing"]["source_feedback_ids"])
        self.assertIn("FB-SAMPLE-003", draft["model_provider_path"]["source_feedback_ids"])
        self.assertEqual(4, len(draft["windows_prerequisites"]["checks_to_turn_into_precheck_script"]))
        self.assertEqual(3, len(draft["resource_sizing"]["profiles"]))
        self.assertEqual(4, len(draft["model_provider_path"]["stages"]))
        self.assertTrue((self.output_dir / draft_builder.DEFAULT_JSON_NAME).exists())
        self.assertTrue((self.output_dir / draft_builder.DEFAULT_MD_NAME).exists())

    def test_cli_returns_pass_for_valid_feedback_sample(self):
        with redirect_stdout(StringIO()):
            code = draft_builder.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--feedback-json",
                    str(self.feedback_path),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(draft_builder.PASS, code)

    def test_holds_when_package_id_mismatch(self):
        payload = json.loads(self.feedback_path.read_text(encoding="utf-8"))
        payload["package_id"] = "different-package"
        self.feedback_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = draft_builder.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--feedback-json",
                    str(self.feedback_path),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(draft_builder.HOLD, code)

    def test_holds_when_boundary_is_true(self):
        self.write_trial_status(boundary_overrides={"network_request": True})

        with redirect_stdout(StringIO()):
            code = draft_builder.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--feedback-json",
                    str(self.feedback_path),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(draft_builder.HOLD, code)

    def test_holds_when_feedback_contains_forbidden_literal(self):
        payload = json.loads(self.feedback_path.read_text(encoding="utf-8"))
        payload["feedback"][0]["notes"] = "Authorization: should never appear"
        self.feedback_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = draft_builder.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--feedback-json",
                    str(self.feedback_path),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(draft_builder.HOLD, code)

    def test_blocker_feedback_creates_hold_draft(self):
        payload = json.loads(self.feedback_path.read_text(encoding="utf-8"))
        payload["feedback"][0]["blocker"] = "Need install precheck before sharing package."
        self.feedback_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        draft = draft_builder.build_draft(
            package_dir=self.package_dir,
            feedback_json=self.feedback_path,
            output_dir=self.output_dir,
            repo_root=self.root,
        )

        self.assertEqual("HOLD_FOR_BLOCKER_REVIEW", draft["status"])
        self.assertIsNone(draft["next_unlock"])
        self.assertEqual(1, len(draft["blockers"]))


if __name__ == "__main__":
    unittest.main()
