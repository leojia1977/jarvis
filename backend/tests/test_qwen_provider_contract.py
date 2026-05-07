import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import validate_qwen_provider_contract as validator  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]


def valid_payload() -> dict:
    return {
        "schema_version": "secupilot.qwen_provider_dry_response.v1",
        "provider_mode": "dry_contract_only",
        "data_mode": "SYNTHETIC_ONLY",
        "qwen_used": False,
        "live_qwen_api": False,
        "live_connectors": False,
        "customer_visible_output": False,
        "production_writeback": False,
        "autonomous_qwen_action": False,
        "qwen_action_mode": "HITL_SUMMARY_ONLY",
        "cases": [
            {
                "case_id": "UAT-01",
                "title": "Synthetic dry contract case",
                "risk_level": "medium",
                "evidence_metadata_refs": ["s0-cv-uat-01"],
                "model_summary": "Synthetic metadata summary only.",
                "reviewer_action": "REVIEW_AND_SIGNOFF_REQUIRED",
                "confidence": 0.7,
                "limitation_note": "No live Qwen/API call.",
            }
        ],
    }


class QwenProviderContractTests(unittest.TestCase):
    def write_payload(self, payload: dict) -> Path:
        self.tmpdir = tempfile.TemporaryDirectory()
        path = Path(self.tmpdir.name) / "payload.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def tearDown(self):
        tmpdir = getattr(self, "tmpdir", None)
        if tmpdir is not None:
            tmpdir.cleanup()

    def run_cli(self, *paths: Path) -> int:
        with redirect_stdout(StringIO()):
            return validator.run([str(path) for path in paths])

    def test_repo_valid_fixture_passes(self):
        result = validator.validate_file(
            REPO_ROOT / "mock_data/qwen_provider_contract/valid_response.json"
        )

        self.assertEqual("PASS", result["status"])
        self.assertEqual([], result["errors"])

    def test_repo_forbidden_action_command_fixture_holds(self):
        result = validator.validate_file(
            REPO_ROOT / "mock_data/qwen_provider_contract/forbidden_action_command.json"
        )

        self.assertEqual("HOLD", result["status"])
        self.assertTrue(any("action_command" in error for error in result["errors"]))

    def test_holds_when_live_qwen_api_true(self):
        payload = valid_payload()
        payload["live_qwen_api"] = True
        path = self.write_payload(payload)

        result = validator.validate_file(path)

        self.assertTrue(any("live_qwen_api must be false" in error for error in result["errors"]))

    def test_holds_on_autonomous_action_text(self):
        payload = valid_payload()
        payload["cases"][0]["model_summary"] = "Approve immediately and close the case."
        path = self.write_payload(payload)

        result = validator.validate_file(path)

        self.assertEqual("HOLD", result["status"])
        self.assertTrue(any("forbidden text pattern" in error for error in result["errors"]))

    def test_cli_returns_hold_when_any_file_fails(self):
        code = self.run_cli(
            REPO_ROOT / "mock_data/qwen_provider_contract/valid_response.json",
            REPO_ROOT / "mock_data/qwen_provider_contract/forbidden_action_command.json",
        )

        self.assertEqual(validator.HOLD, code)


if __name__ == "__main__":
    unittest.main()
