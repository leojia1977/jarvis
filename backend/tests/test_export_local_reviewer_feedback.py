import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import export_local_reviewer_feedback as exporter  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def decision_doc_text(decision: str = "PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL") -> str:
    return f"""# S6 RC-099 Decision

## 1. Decision

```text
RC_009_CN_LOCAL_OFFLINE_REVIEW = {decision}
CANDIDATE = LOCAL_OFFLINE_TRIAL_RC_099_CN
SOURCE_CANDIDATE = LOCAL_OFFLINE_TRIAL_RC_098_CN
CUSTOMER_VISIBLE_OR_DEPLOY_GO = NOT_AUTHORIZED
```

## 2. Reviewer

```text
Reviewer: Jarvis / TL / Product-governance reviewer
Decision: {decision}
Timestamp: 2026-05-07
Review scope: LOCAL_OFFLINE_REVIEW_ONLY
Package: artifacts/local_demo_packages/local-offline-trial-rc-099-cn-review
Zip: local-offline-trial-rc-099-cn-review-package.zip
Zip SHA256: abc123
```

## 3. Passed Checks

```text
中文页面能看懂 = YES
/s1-run 已像产品结果页，不再像证据台 = YES
candidate/source/package/zip 口径一致 = YES
未看到越界内容 = YES
```

## 4. Non-Blocking Observation

```text
可清理 source candidate 引用。
```

## 5. Reviewer Next-Round Suggestions

```text
1. 清理 /s1-trial 第 02 步说明文字中的 source candidate 引用。
2. 在 /s1-run 顶部增加本轮试用范围。
```

## 6. Non-Authorization

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
```
"""


class ExportLocalReviewerFeedbackTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "local_demo_packages" / "local-offline-trial-rc-099-cn-review"
        self.decision_doc = self.root / "docs" / "decision.md"
        self.output_json = self.package_dir / "reviewer_feedback.json"
        self.output_md = self.package_dir / "reviewer_feedback.md"
        self.write_package()
        self.decision_doc.parent.mkdir(parents=True, exist_ok=True)
        self.decision_doc.write_text(decision_doc_text(), encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_package(self, finding_count: int = 0):
        write_json(
            self.package_dir / "package_manifest.json",
            {
                "candidate": "LOCAL_OFFLINE_TRIAL_RC_099_CN",
                "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_098_CN",
            },
        )
        write_json(
            self.package_dir / "evidence" / "final_status.json",
            {
                "boundaries_preserved": {
                    "customer_visible_output": False,
                    "production_connectors": False,
                    "qwen_autonomous_action": False,
                    "raw_payload_retention": False,
                    "secret_retention": False,
                    "writeback": False,
                }
            },
        )
        write_json(
            self.package_dir / "evidence" / "safety_scan.json",
            {"summary": {"finding_count": finding_count}},
        )

    def run_exporter(self) -> int:
        with redirect_stdout(StringIO()):
            return exporter.run(
                [
                    "--decision-doc",
                    str(self.decision_doc),
                    "--package-dir",
                    str(self.package_dir),
                    "--output-json",
                    str(self.output_json),
                    "--output-md",
                    str(self.output_md),
                    "--repo-root",
                    str(self.root),
                ]
            )

    def test_exports_structured_json_and_markdown(self):
        code = self.run_exporter()

        self.assertEqual(exporter.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("secupilot.local_reviewer_feedback.v1", payload["schema_version"])
        self.assertEqual("LOCAL_OFFLINE_TRIAL_RC_099_CN", payload["candidate"])
        self.assertEqual("PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL", payload["decision"])
        self.assertEqual(False, payload["boundaries"]["customer_visible_output"])
        self.assertIn("产品结果页", self.output_md.read_text(encoding="utf-8"))

    def test_holds_when_safety_scan_has_findings(self):
        self.write_package(finding_count=1)

        code = self.run_exporter()

        self.assertEqual(exporter.HOLD, code)


if __name__ == "__main__":
    unittest.main()
