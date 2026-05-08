import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import validate_qwen_live_synthetic_go_precheck as precheck  # noqa: E402


class ValidateQwenLiveSyntheticGoPrecheckTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.request_path = self.root / "artifacts" / "qwen_live_go_precheck" / "go_request.json"
        self.output_dir = self.root / "artifacts" / "qwen_live_go_precheck"
        self.request_path.parent.mkdir(parents=True)
        self.write_request(self.valid_request())

    def tearDown(self):
        self.tmpdir.cleanup()

    def valid_request(self):
        return {
            "schema_version": precheck.SCHEMA_VERSION,
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
            "runtime_controls": {
                "provider_flag_default": False,
                "secret_source": "human_runtime_or_secret_manager_only",
                "secret_value_present": False,
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

    def write_request(self, payload):
        self.request_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def run_cli(self):
        with redirect_stdout(StringIO()):
            return precheck.run(
                [
                    "--request",
                    str(self.request_path),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

    def test_valid_request_generates_ready_report_without_execution(self):
        code = self.run_cli()

        self.assertEqual(precheck.PASS, code)
        report = json.loads((self.output_dir / precheck.DEFAULT_JSON_NAME).read_text(encoding="utf-8"))
        self.assertEqual("READY_FOR_QWEN_LIVE_SYNTHETIC_GO_REVIEW_NOT_EXECUTION", report["overall_status"])
        self.assertEqual("NOT_EXECUTED", report["execution_status"])
        self.assertFalse(report["network_call"])
        self.assertFalse(report["live_qwen_api_call"])
        self.assertTrue((self.output_dir / precheck.DEFAULT_MD_NAME).exists())

    def test_holds_if_live_call_authorized_in_precheck(self):
        payload = self.valid_request()
        payload["authorization"]["live_call_authorized"] = True
        self.write_request(payload)

        self.assertEqual(precheck.HOLD, self.run_cli())

    def test_holds_if_data_mode_is_not_synthetic(self):
        payload = self.valid_request()
        payload["data_mode"] = "MASKED_REAL_DATA"
        self.write_request(payload)

        self.assertEqual(precheck.HOLD, self.run_cli())

    def test_holds_if_secret_value_present(self):
        payload = self.valid_request()
        payload["runtime_controls"]["secret_value_present"] = True
        self.write_request(payload)

        self.assertEqual(precheck.HOLD, self.run_cli())

    def test_holds_if_timeout_unbounded(self):
        payload = self.valid_request()
        payload["runtime_controls"]["timeout_seconds"] = 120
        self.write_request(payload)

        self.assertEqual(precheck.HOLD, self.run_cli())

    def test_holds_if_stop_conditions_missing(self):
        payload = self.valid_request()
        payload["stop_conditions"] = ["too short"]
        self.write_request(payload)

        self.assertEqual(precheck.HOLD, self.run_cli())

    def test_holds_if_forbidden_key_present(self):
        payload = self.valid_request()
        payload["raw_payload"] = "should never be accepted"
        self.write_request(payload)

        self.assertEqual(precheck.HOLD, self.run_cli())

    def test_holds_if_request_outside_repo(self):
        outside = self.root.parent / "outside-qwen-go.json"
        outside.write_text(json.dumps(self.valid_request()), encoding="utf-8")
        try:
            with redirect_stdout(StringIO()):
                code = precheck.run(
                    [
                        "--request",
                        str(outside),
                        "--output-dir",
                        str(self.output_dir),
                        "--repo-root",
                        str(self.root),
                    ]
                )
            self.assertEqual(precheck.HOLD, code)
        finally:
            outside.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
