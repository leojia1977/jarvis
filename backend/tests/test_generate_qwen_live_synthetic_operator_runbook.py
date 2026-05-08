import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import generate_qwen_live_synthetic_operator_runbook as runbook  # noqa: E402


class GenerateQwenLiveSyntheticOperatorRunbookTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.output_dir = self.root / "artifacts" / "qwen_live_go_precheck" / "run"
        self.request_path = self.output_dir / "qwen_live_synthetic_go_request.json"
        self.precheck_path = self.output_dir / "qwen_live_synthetic_go_precheck_report.json"
        self.output_dir.mkdir(parents=True)
        self.write_json(self.request_path, self.valid_request())
        self.write_json(self.precheck_path, self.valid_precheck())

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_json(self, path, payload):
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def valid_request(self):
        return {
            "schema_version": "secupilot.qwen_live_synthetic_go_request.v1",
            "request_id": "QWEN-LIVE-SYNTHETIC-GO-2026-05-08-001",
            "status": "PREPARED_NOT_EXECUTED",
            "authorization": {
                "live_call_authorized": False,
                "requires_separate_go": True,
            },
            "data_mode": "SYNTHETIC_ONLY",
            "run_id": "QWEN-LIVE-SYNTHETIC-2026-05-08-001",
            "operator": {
                "type": "human_runtime_operator",
                "alias": "SecuPilot-QWEN-RUNNER-01",
                "confirmation_required": True,
            },
            "artifact_root": "artifacts/qwen_live_synthetic_runs/2026-05-08-001",
            "input_package": "mock_data/s0_synthetic/qwen_fact_bundle",
            "runtime_controls": {
                "provider_flag_default": False,
                "secret_source": "human_runtime_or_secret_manager_only",
                "secret_value_present": False,
                "secret_env_var_names_allowed": ["SECUPILOT_QWEN_API_KEY"],
                "timeout_seconds": 30,
                "max_retries": 1,
                "cost_or_token_budget": {
                    "max_requests": 20,
                    "max_tokens_per_case": 1200,
                    "stop_on_budget_exceeded": True,
                },
            },
            "data_boundary": {
                "real_data": False,
                "masked_real_data": False,
                "raw_payload_allowed": False,
                "raw_log_allowed": False,
                "customer_visible_output": False,
                "production_writeback": False,
                "live_connectors": False,
                "autonomous_qwen_action": False,
            },
            "stop_conditions": [
                "runtime secret appears in repo, command, log, artifact, or chat",
                "input package is not synthetic-only",
                "provider flag is enabled by default",
                "timeout, retry, or budget guard is missing",
                "response contains forbidden fields",
                "adapter attempts connector action or write-back",
            ],
            "rollback_plan": [
                "disable provider flag",
                "delete incomplete run artifact directory",
                "preserve precheck report and failure reason",
            ],
        }

    def valid_precheck(self):
        return {
            "overall_status": "READY_FOR_QWEN_LIVE_SYNTHETIC_GO_REVIEW_NOT_EXECUTION",
            "execution_status": "NOT_EXECUTED",
            "network_call": False,
            "live_qwen_api_call": False,
        }

    def run_cli(self):
        with redirect_stdout(StringIO()):
            return runbook.run(
                [
                    "--request",
                    str(self.request_path),
                    "--precheck-report",
                    str(self.precheck_path),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

    def test_generates_runbook_manifest_and_dry_command(self):
        code = self.run_cli()

        self.assertEqual(runbook.PASS, code)
        manifest = json.loads((self.output_dir / runbook.MANIFEST_NAME).read_text(encoding="utf-8"))
        dry_command = (self.output_dir / runbook.DRY_COMMAND_NAME).read_text(encoding="utf-8")
        runbook_text = (self.output_dir / runbook.RUNBOOK_NAME).read_text(encoding="utf-8")

        self.assertEqual("OPERATOR_RUNBOOK_READY_DRY_COMMAND_ONLY", manifest["status"])
        self.assertEqual("NOT_EXECUTED", manifest["execution_status"])
        self.assertFalse(manifest["network_call"])
        self.assertFalse(manifest["live_qwen_api_call"])
        self.assertIn("DRY_COMMAND_ONLY_NO_LIVE_CALL", dry_command)
        self.assertIn("QWEN-LIVE-SYNTHETIC-2026-05-08-001", dry_command)
        self.assertIn("runtime secret", dry_command)
        self.assertNotIn("Invoke-RestMethod", dry_command)
        self.assertNotIn("curl", dry_command.lower())
        self.assertIn("Runtime Secret", runbook_text)

    def test_holds_if_precheck_not_ready(self):
        payload = self.valid_precheck()
        payload["overall_status"] = "HOLD"
        self.write_json(self.precheck_path, payload)

        self.assertEqual(runbook.HOLD, self.run_cli())

    def test_holds_if_request_authorizes_live_call(self):
        payload = self.valid_request()
        payload["authorization"]["live_call_authorized"] = True
        self.write_json(self.request_path, payload)

        self.assertEqual(runbook.HOLD, self.run_cli())

    def test_holds_if_secret_value_present(self):
        payload = self.valid_request()
        payload["runtime_controls"]["secret_value_present"] = True
        self.write_json(self.request_path, payload)

        self.assertEqual(runbook.HOLD, self.run_cli())

    def test_holds_if_output_dir_outside_repo(self):
        outside = self.root.parent / "outside-runbook"
        try:
            with redirect_stdout(StringIO()):
                code = runbook.run(
                    [
                        "--request",
                        str(self.request_path),
                        "--precheck-report",
                        str(self.precheck_path),
                        "--output-dir",
                        str(outside),
                        "--repo-root",
                        str(self.root),
                    ]
                )
            self.assertEqual(runbook.HOLD, code)
        finally:
            if outside.exists():
                for path in sorted(outside.rglob("*"), reverse=True):
                    if path.is_file():
                        path.unlink()
                outside.rmdir()


if __name__ == "__main__":
    unittest.main()
