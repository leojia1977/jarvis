import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import validate_qwen_live_synthetic_runtime_config as config_validator  # noqa: E402


class ValidateQwenLiveSyntheticRuntimeConfigTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.output_dir = self.root / "artifacts" / "runtime"
        self.request_path = self.output_dir / "qwen_live_synthetic_go_request.json"
        self.output_dir.mkdir(parents=True)
        self.write_request(self.valid_request())

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_request(self, payload):
        self.request_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def valid_request(self):
        return {
            "status": "PREPARED_NOT_EXECUTED",
            "authorization": {
                "live_call_authorized": False,
                "requires_separate_go": True,
            },
            "data_mode": "SYNTHETIC_ONLY",
            "runtime_controls": {
                "provider_flag_default": False,
                "secret_source": "human_runtime_or_secret_manager_only",
                "secret_value_present": False,
                "secret_env_var_names_allowed": ["SECUPILOT_QWEN_API_KEY"],
                "timeout_seconds": 30,
                "max_retries": 1,
            },
        }

    def valid_env(self):
        return {
            "SECUPILOT_QWEN_PROVIDER_ENABLED": "true",
            "SECUPILOT_QWEN_SYNTHETIC_ONLY": "true",
            "SECUPILOT_QWEN_API_BASE": "https://model-runtime.example.invalid/compatible-mode/v1",
            "SECUPILOT_QWEN_MODEL": "model-preview",
            "SECUPILOT_QWEN_TIMEOUT_SECONDS": "30",
            "SECUPILOT_QWEN_MAX_RETRIES": "1",
            "SECUPILOT_QWEN_API_KEY": "runtime-value-sentinel-not-retained",
        }

    def run_cli(self, mode="policy", env=None):
        with redirect_stdout(StringIO()):
            return config_validator.run(
                [
                    "--request",
                    str(self.request_path),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                    "--mode",
                    mode,
                ],
                env={} if env is None else env,
            )

    def test_policy_mode_passes_without_process_env(self):
        code = self.run_cli(mode="policy", env={})

        self.assertEqual(config_validator.PASS, code)
        report = json.loads((self.output_dir / config_validator.DEFAULT_JSON_NAME).read_text(encoding="utf-8"))
        self.assertEqual("RUNTIME_CONFIG_POLICY_READY_PROCESS_ENV_NOT_CHECKED", report["overall_status"])
        self.assertFalse(report["process_env_checked"])
        self.assertFalse(report["env_values_retained"])
        self.assertFalse(report["secret_values_read"])

    def test_process_mode_passes_and_does_not_retain_secret_or_env_values(self):
        code = self.run_cli(mode="process", env=self.valid_env())

        self.assertEqual(config_validator.PASS, code)
        report_text = (self.output_dir / config_validator.DEFAULT_JSON_NAME).read_text(encoding="utf-8")
        report = json.loads(report_text)
        self.assertEqual("RUNTIME_CONFIG_READY_FOR_SYNTHETIC_LIVE_GO_REVIEW_NOT_EXECUTION", report["overall_status"])
        self.assertTrue(report["process_env_checked"])
        self.assertFalse(report["env_values_retained"])
        self.assertFalse(report["secret_values_read"])
        self.assertNotIn("runtime-value-sentinel-not-retained", report_text)
        self.assertNotIn("model-runtime.example.invalid", report_text)
        self.assertNotIn("model-preview", report_text)

    def test_process_mode_holds_when_secret_env_missing(self):
        env = self.valid_env()
        del env["SECUPILOT_QWEN_API_KEY"]

        self.assertEqual(config_validator.HOLD, self.run_cli(mode="process", env=env))

    def test_process_mode_holds_when_api_base_not_https(self):
        env = self.valid_env()
        env["SECUPILOT_QWEN_API_BASE"] = "http://example.invalid"

        self.assertEqual(config_validator.HOLD, self.run_cli(mode="process", env=env))

    def test_process_mode_holds_when_provider_flag_not_true(self):
        env = self.valid_env()
        env["SECUPILOT_QWEN_PROVIDER_ENABLED"] = "false"

        self.assertEqual(config_validator.HOLD, self.run_cli(mode="process", env=env))

    def test_process_mode_holds_when_retry_exceeds_request_bound(self):
        env = self.valid_env()
        env["SECUPILOT_QWEN_MAX_RETRIES"] = "2"

        self.assertEqual(config_validator.HOLD, self.run_cli(mode="process", env=env))

    def test_holds_if_request_authorizes_live_call(self):
        payload = self.valid_request()
        payload["authorization"]["live_call_authorized"] = True
        self.write_request(payload)

        self.assertEqual(config_validator.HOLD, self.run_cli(mode="policy", env={}))

    def test_holds_if_request_contains_secret_value(self):
        payload = self.valid_request()
        payload["runtime_controls"]["secret_value_present"] = True
        self.write_request(payload)

        self.assertEqual(config_validator.HOLD, self.run_cli(mode="policy", env={}))


if __name__ == "__main__":
    unittest.main()
