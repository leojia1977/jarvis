import json
import unittest

from _project_bootstrap import bootstrap

bootstrap()

from scripts import s0_qwen_synthetic_run as runner  # noqa: E402


class S0QwenSyntheticRunPromptBudgetTests(unittest.TestCase):
    def _minimal_bundle(self):
        return {
            "uat_id": "UAT-TEST",
            "fact_bundle_id": "s0-qf-test",
            "scenario_title": "Prompt budget test",
            "facts": [{"id": "fact-1", "text": "synthetic fact only"}],
            "unsupported_claims": ["unsupported test claim"],
            "evaluation_profile": {"prompt_injection_required": False},
            "fixture_meta": {"synthetic_only": True, "real_data_derived": False},
        }

    def test_policy_header_is_compact(self):
        self.assertLess(len(runner.COMPACT_POLICY_HEADER), 400)
        self.assertIn("Return JSON only", runner.COMPACT_POLICY_HEADER)
        self.assertNotIn("PRD", runner.COMPACT_POLICY_HEADER)

    def test_build_messages_uses_compact_json_payload(self):
        messages = runner._build_messages(self._minimal_bundle())
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], runner.COMPACT_POLICY_HEADER)
        user_content = messages[1]["content"]
        self.assertEqual(user_content, json.dumps(json.loads(user_content), ensure_ascii=False, separators=(",", ":")))
        self.assertNotIn("\n  ", user_content)

    def test_prompt_budget_accepts_current_synthetic_shape(self):
        messages = runner._build_messages(self._minimal_bundle())
        runner._validate_prompt_budget(messages, max_input_chars=runner.DEFAULT_MAX_INPUT_CHARS, max_input_tokens_estimate=runner.DEFAULT_MAX_INPUT_TOKENS_ESTIMATE)

    def test_prompt_budget_rejects_oversized_prompt_before_model_call(self):
        large_bundle = self._minimal_bundle()
        large_bundle["facts"] = [{"id": "fact-large", "text": "x" * (runner.DEFAULT_MAX_INPUT_CHARS + 1)}]
        messages = runner._build_messages(large_bundle)
        with self.assertRaisesRegex(ValueError, "HOLD_PROMPT_TOO_LARGE"):
            runner._validate_prompt_budget(messages, max_input_chars=runner.DEFAULT_MAX_INPUT_CHARS, max_input_tokens_estimate=runner.DEFAULT_MAX_INPUT_TOKENS_ESTIMATE)


if __name__ == "__main__":
    unittest.main()
