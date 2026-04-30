import json
import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts.synthetic_safety_tooling import (  # noqa: E402
    HOLD_REJECT_SECRET_BEARING_INPUT,
    mask_synthetic_value,
    scan_text_for_hard_stops,
    validate_qwen_fact_bundle,
    validate_qwen_fact_bundle_file,
)


ROOT = Path(__file__).resolve().parents[2]


class MaskingValidatorTests(unittest.TestCase):
    def test_required_synthetic_masking_examples_are_deterministic(self):
        self.assertEqual(mask_synthetic_value("192.168.1.42").value, "192.168.1.x")
        self.assertRegex(mask_synthetic_value("jsmith@corp.example").value, r"^user_[0-9a-f]{4}$")
        self.assertEqual(mask_synthetic_value("ws-finance-042").value, "host_finance_ws_042")
        self.assertEqual(mask_synthetic_value("-token abc123").value, "-token [REDACTED]")
        self.assertEqual(mask_synthetic_value("Authorization: Bearer abc123").value, "[REDACTED_AUTHORIZATION_HEADER]")

    def test_private_key_like_input_is_hold_rejected(self):
        decision = mask_synthetic_value("-----BEGIN PRIVATE KEY-----")
        self.assertEqual(decision.status, "HOLD")
        self.assertEqual(decision.value, HOLD_REJECT_SECRET_BEARING_INPUT)


class RedactionHardStopScannerTests(unittest.TestCase):
    def test_required_hard_stop_patterns_trigger_hold(self):
        samples = [
            "password=hunter2",
            "passwd=secret",
            "Authorization: Bearer abc123",
            "Bearer abc123",
            "api_key=abc123",
            "secret: abc123",
            "token=abc123",
            "private key",
            "session cookie",
            "-----BEGIN",
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                result = scan_text_for_hard_stops(sample)
                self.assertTrue(result.hold)
                self.assertGreaterEqual(len(result.findings), 1)

    def test_documentation_safe_list_still_detects_without_hold(self):
        result = scan_text_for_hard_stops("SAFE_DOC_EXAMPLE: `password=` is forbidden.", allow_doc_examples=True)
        self.assertFalse(result.hold)
        self.assertEqual(len(result.findings), 1)
        self.assertTrue(result.findings[0].safe_listed)


class QwenFactBundleSyntheticBuilderCheckTests(unittest.TestCase):
    def test_existing_s0_qwen_fact_bundles_validate_as_synthetic_only(self):
        bundle_dir = ROOT / "mock_data" / "s0_synthetic" / "qwen_fact_bundle"
        bundle_paths = sorted(bundle_dir.glob("*.json"))
        self.assertEqual(len(bundle_paths), 20)
        for path in bundle_paths:
            with self.subTest(path=path.name):
                result = validate_qwen_fact_bundle_file(path)
                self.assertTrue(result.valid, result.errors)

    def test_rejects_raw_or_secret_bearing_bundle(self):
        bad_bundle = {
            "fact_bundle_id": "bad",
            "facts": [{"text": "raw user email jsmith@corp.example and token=abc123", "synthetic": True}],
            "unsupported_claims": ["unsupported"],
            "forbidden_outputs": ["isolate host"],
            "raw_event_json": {"event": "should not enter Qwen"},
            "fixture_meta": {
                "synthetic_only": False,
                "real_data_derived": True,
                "masked_real_data": True,
                "secrets_present": True,
                "raw_layer0_payload_present": True,
            },
        }
        result = validate_qwen_fact_bundle(bad_bundle)
        self.assertFalse(result.valid)
        joined = "\n".join(result.errors)
        self.assertIn("fixture_meta.synthetic_only_not_true", joined)
        self.assertIn("forbidden_raw_key_present:$.raw_event_json", joined)
        self.assertIn("unmasked_email_present:$.facts[0].text", joined)
        self.assertIn("secret_pattern_present:$.facts[0].text", joined)

    def test_no_model_output_or_scoring_fields_are_allowed_in_qwen_input(self):
        good_path = ROOT / "mock_data" / "s0_synthetic" / "qwen_fact_bundle" / "uat-01_s0-qf-uat-01-ntlm-lateral.json"
        bundle = json.loads(good_path.read_text(encoding="utf-8"))
        bundle["model_output"] = "This is not an input field."
        result = validate_qwen_fact_bundle(bundle)
        self.assertFalse(result.valid)
        self.assertIn("model_output_field_present:$.model_output", result.errors)


if __name__ == "__main__":
    unittest.main()
