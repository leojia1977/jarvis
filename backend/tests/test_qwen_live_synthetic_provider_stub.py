import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import qwen_live_synthetic_provider_stub as stub  # noqa: E402
from scripts import validate_qwen_provider_contract as contract_validator  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]


class QwenLiveSyntheticProviderStubTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.bundle_dir = self.root / "mock_data" / "s0_synthetic" / "qwen_fact_bundle"
        self.output_dir = self.root / "artifacts" / "provider_stub"
        self.runtime_report = self.output_dir / "runtime_config_report.json"
        self.bundle_dir.mkdir(parents=True)
        self.output_dir.mkdir(parents=True)
        self.write_bundle(self.valid_bundle())
        self.write_runtime_report(self.valid_runtime_report())

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_json(self, path, payload):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def write_bundle(self, payload):
        self.write_json(self.bundle_dir / "uat-01.json", payload)

    def write_runtime_report(self, payload):
        self.write_json(self.runtime_report, payload)

    def valid_bundle(self):
        return {
            "fact_bundle_id": "s0-qf-uat-01",
            "uat_id": "UAT-01",
            "source_payload_id": "s0-cv-uat-01",
            "scenario_title": "Synthetic lateral movement review",
            "facts": [{"fact_id": "F-01", "text": "Synthetic metadata fact.", "synthetic": True}],
            "unsupported_claims": ["Confirmed credential theft"],
            "fixture_meta": {
                "synthetic_only": True,
                "real_data_derived": False,
                "masked_real_data": False,
                "secrets_present": False,
                "raw_layer0_payload_present": False,
            },
        }

    def valid_runtime_report(self):
        return {
            "overall_status": "RUNTIME_CONFIG_POLICY_READY_PROCESS_ENV_NOT_CHECKED",
            "network_call": False,
            "live_qwen_api_call": False,
            "secret_values_read": False,
            "secret_values_retained": False,
        }

    def run_cli(self):
        with redirect_stdout(StringIO()):
            return stub.run(
                [
                    "--bundle-dir",
                    str(self.bundle_dir),
                    "--runtime-config-report",
                    str(self.runtime_report),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

    def test_generates_contract_compatible_stub_output(self):
        code = self.run_cli()

        self.assertEqual(stub.PASS, code)
        output_path = self.output_dir / stub.DEFAULT_OUTPUT_NAME
        report_path = self.output_dir / stub.DEFAULT_REPORT_NAME
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        report = json.loads(report_path.read_text(encoding="utf-8"))

        self.assertEqual("dry_contract_only", payload["provider_mode"])
        self.assertEqual(stub.PROVIDER_STUB_MODE, payload["provider_stub_mode"])
        self.assertEqual("SYNTHETIC_ONLY", payload["data_mode"])
        self.assertFalse(payload["live_qwen_api"])
        self.assertFalse(payload["network_call"])
        self.assertFalse(payload["secret_values_read"])
        self.assertEqual(1, len(payload["cases"]))
        self.assertEqual("QWEN_SYNTHETIC_PROVIDER_STUB_READY_NO_NETWORK", report["overall_status"])
        self.assertEqual("PASS", contract_validator.validate_file(output_path)["status"])

    def test_repo_bundle_generates_twenty_case_stub(self):
        repo_bundle_copy = self.root / "mock_data" / "repo_bundle_copy"
        shutil.copytree(REPO_ROOT / "mock_data/s0_synthetic/qwen_fact_bundle", repo_bundle_copy)
        report = stub.build_provider_stub(
            bundle_dir=repo_bundle_copy,
            runtime_config_report=self.runtime_report,
            output_dir=self.output_dir,
            repo_root=self.root,
        )

        output = json.loads((self.output_dir / stub.DEFAULT_OUTPUT_NAME).read_text(encoding="utf-8"))
        self.assertEqual(20, report["case_count"])
        self.assertEqual(20, len(output["cases"]))
        self.assertEqual("PASS", contract_validator.validate_file(self.output_dir / stub.DEFAULT_OUTPUT_NAME)["status"])

    def test_holds_if_runtime_report_not_ready(self):
        payload = self.valid_runtime_report()
        payload["overall_status"] = "HOLD"
        self.write_runtime_report(payload)

        self.assertEqual(stub.HOLD, self.run_cli())

    def test_holds_if_bundle_is_not_synthetic_only(self):
        payload = self.valid_bundle()
        payload["fixture_meta"]["synthetic_only"] = False
        self.write_bundle(payload)

        self.assertEqual(stub.HOLD, self.run_cli())

    def test_holds_if_forbidden_action_text_would_be_emitted(self):
        payload = self.valid_bundle()
        payload["scenario_title"] = "isolate host immediately"
        self.write_bundle(payload)

        self.assertEqual(stub.HOLD, self.run_cli())


if __name__ == "__main__":
    unittest.main()
