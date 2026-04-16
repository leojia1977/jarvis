import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from app.tools.siem_adapter import TimeRangeSpec  # noqa: E402
from app.tools.siem_alert_file_adapter import (  # noqa: E402
    GOVERNED_HEADERS,
    SIEMAlertFileAdapter,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
TMP_ROOT = REPO_ROOT / ".tmp_testdata" / "siem_alert_file_adapter"


def _time_range() -> TimeRangeSpec:
    return TimeRangeSpec(
        start_utc=datetime(2026, 4, 16, 0, 0, 0, tzinfo=timezone.utc),
        end_utc=datetime(2026, 4, 16, 23, 59, 59, tzinfo=timezone.utc),
        tz_label="UTC",
    )


def _base_row(**overrides):
    row = {
        "采集时间": "2026-04-16 10:00:00",
        "威胁名称": "Synthetic Alert",
        "威胁类型": "Synthetic Category",
        "威胁等级": "高危",
        "受影响主机": "SYNTH-ASSET-001",
        "协议": "TCP",
        "源Ip": "192.0.2.10",
        "源端口": "443",
        "目标Ip": "198.51.100.20",
        "目标端口": "8443",
        "受影响主机ip": "203.0.113.30",
        "状态": "攻击失败",
        "数据来源": "Synthetic Engine",
        "CVE": "SYNTH-CVE-0001",
    }
    row.update(overrides)
    return [row[header] for header in GOVERNED_HEADERS]


class SIEMAlertFileAdapterTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        TMP_ROOT.mkdir(parents=True, exist_ok=True)
        self._tmp = tempfile.TemporaryDirectory(dir=TMP_ROOT, ignore_cleanup_errors=True)
        self.tmp_path = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _write_workbook(self, rows, *, headers=None, title_rows=None) -> Path:
        from openpyxl import Workbook

        workbook = Workbook()
        worksheet = workbook.active
        for title_row in title_rows or []:
            worksheet.append(title_row)
        worksheet.append(list(headers or GOVERNED_HEADERS))
        for row in rows:
            worksheet.append(row)
        path = self.tmp_path / "synthetic.xlsx"
        workbook.save(path)
        workbook.close()
        return path

    async def test_happy_path_with_all_14_governed_headers(self):
        path = self._write_workbook([_base_row()])
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "ok")
        self.assertIsNone(result.gap_reason)
        self.assertEqual(len(result.data), 1)
        alert = result.data[0]
        self.assertEqual(set(alert), {"event_id", "event_time", "severity", "activity_name", "source_ip", "destination_ip", "destination_asset_id", "extra"})
        self.assertEqual(alert["event_id"], "ordiv_l1a_row_2")
        self.assertEqual(alert["event_time"], "2026-04-16T10:00:00Z")
        self.assertEqual(alert["severity"], "HIGH")
        self.assertEqual(alert["activity_name"], "Synthetic Alert")
        self.assertEqual(alert["source_ip"], "192.0.2.10")
        self.assertEqual(alert["destination_ip"], "198.51.100.20")
        self.assertEqual(alert["destination_asset_id"], "SYNTH-ASSET-001")
        self.assertEqual(alert["extra"]["alert_name"], "Synthetic Alert")
        self.assertEqual(alert["extra"]["source_port"], "443")
        self.assertEqual(alert["extra"]["destination_port"], "8443")
        self.assertEqual(alert["extra"]["outcome"], "blocked")

    async def test_title_row_is_skipped_before_exact_headers(self):
        path = self._write_workbook([_base_row()], title_rows=[["Synthetic workbook title"]])
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "ok")
        self.assertEqual(result.data[0]["event_id"], "ordiv_l1a_row_3")

    async def test_missing_required_headers_returns_partial_without_raw_leakage(self):
        headers = list(GOVERNED_HEADERS[:-1])
        path = self._write_workbook([_base_row()], headers=headers)
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.data, [])
        self.assertEqual(result.gap_reason, "MISSING_REQUIRED_HEADER")
        self.assert_no_gap_leakage(result.gap_reason)

    async def test_duplicate_header_returns_partial_without_raw_leakage(self):
        headers = list(GOVERNED_HEADERS)
        headers[-1] = "源Ip"
        path = self._write_workbook([_base_row()], headers=headers)
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.data, [])
        self.assertEqual(result.gap_reason, "DUPLICATE_HEADER")
        self.assert_no_gap_leakage(result.gap_reason)

    async def test_partial_row_returns_partial_without_raw_leakage(self):
        rows = [
            _base_row(威胁名称=""),
            _base_row(威胁名称="Second Synthetic Alert", 源Ip="192.0.2.11"),
        ]
        path = self._write_workbook(rows)
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.gap_reason, "PARTIAL_ROW:row_2")
        self.assertEqual(len(result.data), 1)
        self.assert_no_gap_leakage(result.gap_reason)

    async def test_invalid_timestamp_returns_partial_with_safe_row_index(self):
        path = self._write_workbook([_base_row(采集时间="not-a-timestamp")])
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.data, [])
        self.assertEqual(result.gap_reason, "INVALID_TIMESTAMP:row_2")
        self.assertNotIn("not-a-timestamp", result.gap_reason)
        self.assert_no_gap_leakage(result.gap_reason)

    async def test_invalid_ip_like_value_returns_partial_with_safe_row_index(self):
        path = self._write_workbook([_base_row(源Ip="999.999.999.999")])
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.data, [])
        self.assertEqual(result.gap_reason, "INVALID_IP_LIKE_VALUE:row_2")
        self.assertNotIn("999.999.999.999", result.gap_reason)
        self.assert_no_gap_leakage(result.gap_reason)

    async def test_invalid_port_returns_partial_and_omits_raw_port(self):
        path = self._write_workbook([_base_row(源端口="not-a-port")])
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.gap_reason, "INVALID_PORT:row_2")
        self.assertEqual(len(result.data), 1)
        self.assertNotIn("source_port", result.data[0]["extra"])
        self.assertNotIn("not-a-port", str(result.data[0]))
        self.assert_no_gap_leakage(result.gap_reason)

    async def test_severity_mapping_for_chinese_and_english_values(self):
        rows = [
            _base_row(威胁等级="高危", 源Ip="192.0.2.1"),
            _base_row(威胁等级="HIGH", 源Ip="192.0.2.2"),
            _base_row(威胁等级="中危", 源Ip="192.0.2.3"),
            _base_row(威胁等级="MEDIUM", 源Ip="192.0.2.4"),
            _base_row(威胁等级="低危", 源Ip="192.0.2.5"),
            _base_row(威胁等级="LOW", 源Ip="192.0.2.6"),
        ]
        path = self._write_workbook(rows)
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "ok")
        self.assertEqual(
            [alert["severity"] for alert in result.data],
            ["HIGH", "HIGH", "MEDIUM", "MEDIUM", "LOW", "LOW"],
        )

    async def test_unknown_severity_uses_closed_partial_row_gap(self):
        path = self._write_workbook([_base_row(威胁等级="unsupported-severity")])
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.gap_reason, "PARTIAL_ROW:row_2")
        self.assertNotIn("unsupported-severity", result.gap_reason)

    async def test_outcome_mapping_for_known_and_unknown_values(self):
        rows = [
            _base_row(状态="攻击失败", 源Ip="192.0.2.21"),
            _base_row(状态="疑似成功", 源Ip="192.0.2.22"),
            _base_row(状态="Synthetic Unknown Outcome", 源Ip="192.0.2.23"),
        ]
        path = self._write_workbook(rows)
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "ok")
        self.assertEqual(
            [alert["extra"]["outcome"] for alert in result.data],
            ["blocked", "suspected", "unknown"],
        )

    async def test_event_id_is_row_index_derived_and_unique_within_single_call(self):
        rows = [
            _base_row(源Ip="192.0.2.31"),
            _base_row(源Ip="192.0.2.32"),
        ]
        path = self._write_workbook(rows)
        result = await SIEMAlertFileAdapter(path).query_intent_alerts("any", "ignored", _time_range())

        event_ids = [alert["event_id"] for alert in result.data]
        self.assertEqual(event_ids, ["ordiv_l1a_row_2", "ordiv_l1a_row_3"])
        self.assertEqual(len(event_ids), len(set(event_ids)))
        for event_id in event_ids:
            self.assertNotIn(str(path), event_id)
            self.assertNotIn("192.0.2.", event_id)

    async def test_query_asset_alerts_filters_destination_asset_source_and_destination_ip(self):
        rows = [
            _base_row(受影响主机="SYNTH-ASSET-001", 源Ip="192.0.2.41", 目标Ip="198.51.100.41"),
            _base_row(受影响主机="SYNTH-ASSET-002", 源Ip="192.0.2.42", 目标Ip="198.51.100.42"),
            _base_row(受影响主机="SYNTH-ASSET-003", 源Ip="192.0.2.43", 目标Ip="198.51.100.43"),
        ]
        path = self._write_workbook(rows)
        adapter = SIEMAlertFileAdapter(path)

        by_asset = await adapter.query_asset_alerts("SYNTH-ASSET-002", _time_range())
        by_source = await adapter.query_asset_alerts("192.0.2.43", _time_range())
        by_destination = await adapter.query_asset_alerts("198.51.100.41", _time_range())

        self.assertEqual([alert["destination_asset_id"] for alert in by_asset.data], ["SYNTH-ASSET-002"])
        self.assertEqual([alert["source_ip"] for alert in by_source.data], ["192.0.2.43"])
        self.assertEqual([alert["destination_ip"] for alert in by_destination.data], ["198.51.100.41"])

    async def test_query_recent_summary_returns_sanitized_counts(self):
        rows = [
            _base_row(威胁等级="高危", 源Ip="192.0.2.51"),
            _base_row(威胁等级="中危", 源Ip="192.0.2.52"),
            _base_row(威胁等级="低危", 源Ip="192.0.2.53"),
        ]
        path = self._write_workbook(rows)
        result = await SIEMAlertFileAdapter(path).query_recent_summary(_time_range())

        self.assertEqual(result.status, "ok")
        self.assertEqual(result.data["total_alerts"], 3)
        self.assertEqual(result.data["severity_counts"], {"HIGH": 1, "MEDIUM": 1, "LOW": 1})
        self.assertNotIn(str(path), str(result.data))

    async def test_metadata_methods_return_ok_none(self):
        path = self._write_workbook([_base_row()])
        adapter = SIEMAlertFileAdapter(path)

        scenario = await adapter.get_scenario_metadata("SYNTH-SCENARIO")
        asset = await adapter.get_asset_context("SYNTH-ASSET-001")

        self.assertEqual(scenario.status, "ok")
        self.assertIsNone(scenario.data)
        self.assertEqual(asset.status, "ok")
        self.assertIsNone(asset.data)

    async def test_unavailable_workbook_returns_closed_gap_reason(self):
        missing_path = self.tmp_path / "missing.xlsx"
        result = await SIEMAlertFileAdapter(missing_path).query_intent_alerts("any", "ignored", _time_range())

        self.assertEqual(result.status, "unavailable")
        self.assertEqual(result.gap_reason, "WORKBOOK_UNAVAILABLE")
        self.assertNotIn(str(missing_path), result.gap_reason)

    def test_no_committed_workbook_fixtures_or_dependency_install_hooks(self):
        fixture_root = Path(__file__).parent / "fixtures"
        workbook_fixtures = list(fixture_root.rglob("*.xlsx")) if fixture_root.exists() else []
        self.assertEqual(workbook_fixtures, [])

        adapter_source = (Path(__file__).resolve().parents[1] / "app" / "tools" / "siem_alert_file_adapter.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("pip install", adapter_source)
        self.assertNotIn("subprocess", adapter_source)
        self.assertNotIn("requirements.txt", adapter_source)

    def assert_no_gap_leakage(self, gap_reason):
        self.assertIsNotNone(gap_reason)
        forbidden_tokens = [
            "synthetic.xlsx",
            str(self.tmp_path),
            "Synthetic Alert",
            "SYNTH-ASSET",
            "192.0.2.",
            "198.51.100.",
            "203.0.113.",
            "not-a-port",
            "not-a-timestamp",
        ]
        for token in forbidden_tokens:
            self.assertNotIn(token, gap_reason)
