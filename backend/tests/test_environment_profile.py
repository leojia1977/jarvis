import shutil
import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings
from backend.app.runtime_service import SecuPilotRuntimeService


REPO_ROOT = Path(__file__).resolve().parents[2]
TMP_ROOT = REPO_ROOT / ".tmp_testdata"
TMP_ROOT.mkdir(exist_ok=True)


def _fresh_temp_root(name: str) -> Path:
    target = TMP_ROOT / name
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)
    return target


class EnvironmentProfileTests(unittest.TestCase):
    def test_mock_profile_marks_vendor_secrets_optional(self):
        configured = Settings(
            project_root=str(REPO_ROOT),
            runtime_mode="mock",
            mock_data_path="./mock_data",
        )

        contract = configured.get_environment_contract()

        self.assertEqual(contract["environment_profile"], "mock_local")
        self.assertIn("mock_data_path", contract["required_environment_fields"])
        self.assertEqual(contract["required_secret_names"], [])
        self.assertIn("siem_auth_token", contract["optional_secret_names"])
        self.assertIn("edr_auth_token", contract["optional_secret_names"])
        self.assertTrue(contract["profile_contract_ready"])

    def test_pilot_profile_requires_explicit_static_path_and_siem_secret(self):
        configured = Settings(
            project_root=str(REPO_ROOT),
            runtime_mode="production",
            mock_data_path="./mock_data",
            siem_base_url="https://siem.example.local",
        )

        contract = configured.get_environment_contract()

        self.assertEqual(contract["environment_profile"], "pilot_local")
        self.assertIn("static_data_path", contract["required_environment_fields"])
        self.assertIn("siem_auth_token", contract["required_secret_names"])
        self.assertFalse(contract["profile_contract_ready"])
        self.assertIn("static_data_path", contract["profile_contract_missing"])
        self.assertIn("siem_auth_token", contract["profile_contract_missing"])
        self.assertIn("siem_vendor(splunk_like_or_elastic_like)", contract["profile_contract_missing"])

    def test_pilot_api_edr_profile_requires_edr_secret(self):
        configured = Settings(
            project_root=str(REPO_ROOT),
            runtime_mode="production",
            static_data_path="./mock_data",
            siem_vendor="splunk_like",
            siem_base_url="https://siem.example.local",
            siem_auth_token="secret-token",
            edr_source_mode="api",
            edr_base_url="https://edr.example.local",
        )

        contract = configured.get_environment_contract()

        self.assertEqual(contract["environment_profile"], "pilot_local")
        self.assertIn("edr_auth_token", contract["required_secret_names"])
        self.assertIn("edr_auth_token", contract["profile_contract_missing"])

    def test_complete_pilot_profile_is_ready_but_emits_loopback_warning(self):
        configured = Settings(
            project_root=str(REPO_ROOT),
            runtime_mode="production",
            static_data_path="./mock_data",
            siem_vendor="splunk_like",
            siem_base_url="https://siem.example.local",
            siem_auth_token="secret-token",
            case_store_path="./data/secupilot_case_store.sqlite3",
        )

        contract = configured.get_environment_contract()

        self.assertTrue(contract["profile_contract_ready"])
        self.assertEqual(contract["profile_contract_missing"], [])
        self.assertEqual(contract["environment_profile"], "pilot_local")
        self.assertIn(
            "server_host_loopback_limits_remote_pilot_access",
            contract["profile_contract_warnings"],
        )
        self.assertNotIn("mock_data_path", contract["optional_environment_fields"])

    def test_readiness_exposes_environment_profile_contract(self):
        temp_dir = _fresh_temp_root("environment_profile_runtime")
        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="production",
                static_data_path="./mock_data",
                siem_vendor="splunk_like",
                siem_base_url="https://siem.example.local",
                siem_auth_token="secret-token",
                case_store_path=str(temp_dir / "cases.sqlite3"),
            )
        )

        readiness = service.readiness()

        self.assertEqual(readiness["environment_profile"], "pilot_local")
        self.assertTrue(readiness["profile_contract_ready"])
        self.assertEqual(readiness["profile_contract_missing"], [])
        self.assertIn("siem_auth_token", readiness["required_secret_names"])
        self.assertIn("case_store_path", readiness["required_environment_fields"])
        self.assertIn(
            "server_host_loopback_limits_remote_pilot_access",
            readiness["profile_contract_warnings"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
