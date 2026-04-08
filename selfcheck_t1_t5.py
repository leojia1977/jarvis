from datetime import timezone, timedelta

from blast_radius import RealBlastRadiusEngine
from triage_engine import RealTriageEngine


def check_t1_timezone() -> None:
    engine = RealTriageEngine(
        asset_db={"srv1": {"asset_id": "srv1", "criticality_weight": 8}},
        baseline_db=[],
        business_timezone="Asia/Shanghai",
    )
    result = engine.score_alert(
        {
            "event_id": "tz-1",
            "severity": "HIGH",
            "destination_asset_id": "srv1",
            "source_ip": "1.1.1.1",
            "activity_name": "lateral movement",
            "event_time": "2026-04-03T02:00:00Z",
        }
    )
    assert result.factors["business_hour"] == 10, result.factors
    assert result.factors["time_anomaly"] == 1.0, result.factors


def check_t1_priority_separation() -> None:
    engine = RealTriageEngine(
        asset_db={"srv1": {"asset_id": "srv1", "criticality_weight": 10}},
        baseline_db=[],
        business_timezone=timezone(timedelta(hours=8)),
    )

    alerts = [
        {
            "event_id": f"burst-{idx}",
            "severity": "CRITICAL",
            "destination_asset_id": "srv1",
            "source_ip": "8.8.8.8",
            "activity_name": "credential dump",
            "event_time": f"2026-04-03T00:{idx:02d}:00+08:00",
        }
        for idx in range(25)
    ]

    first = engine.score_alert(alerts[0])
    for alert in alerts[1:-1]:
        engine.score_alert(alert)
    last = engine.score_alert(alerts[-1])
    assert first.risk_score <= 10.0
    assert last.risk_score <= 10.0
    assert last.priority_score > first.priority_score, (first, last)


def check_t1_freq_cache_prune() -> None:
    engine = RealTriageEngine(
        asset_db={"srv1": {"asset_id": "srv1", "criticality_weight": 5}},
        baseline_db=[],
        business_timezone="UTC",
        window_minutes=60,
    )

    old_alert = {
        "event_id": "old-1",
        "severity": "LOW",
        "destination_asset_id": "srv1",
        "source_ip": "203.0.113.10",
        "activity_name": "port scan",
        "event_time": "2026-04-01T00:00:00Z",
    }
    new_alert = {
        "event_id": "new-1",
        "severity": "LOW",
        "destination_asset_id": "srv1",
        "source_ip": "198.51.100.20",
        "activity_name": "port scan",
        "event_time": "2026-04-03T12:00:00Z",
    }

    engine.triage_batch([old_alert])
    old_key = ("203.0.113.10", "srv1", "port scan")
    assert old_key in engine._freq_cache, engine._freq_cache

    engine.triage_batch([new_alert])
    assert old_key not in engine._freq_cache, engine._freq_cache


def check_t5_bidirectional_propagation() -> None:
    engine = RealBlastRadiusEngine(
        {
            "nodes": {
                "assets": [
                    {"asset_id": "gw1", "criticality_weight": 9, "role": "gateway"},
                    {"asset_id": "app1", "criticality_weight": 7, "role": "app"},
                    {"asset_id": "db1", "criticality_weight": 8, "role": "db"},
                ],
                "users": [],
                "segments": [],
            },
            "relationships": [
                {"from": "gw1", "to": "app1", "type": "connects_to"},
                {"from": "app1", "to": "db1", "type": "connects_to"},
            ],
        }
    )
    report = engine.calculate("BLOCK_IP", "gw1")
    assert "app1" in report.cascade_assets, report
    assert "db1" in report.cascade_assets, report


def check_t5_cycle_safe() -> None:
    engine = RealBlastRadiusEngine(
        {
            "nodes": {
                "assets": [
                    {"asset_id": "a1", "criticality_weight": 5, "role": "app"},
                    {"asset_id": "a2", "criticality_weight": 5, "role": "app"},
                    {"asset_id": "a3", "criticality_weight": 5, "role": "db"},
                ],
                "users": [],
                "segments": [],
            },
            "relationships": [
                {"from": "a1", "to": "a2", "type": "connects_to"},
                {"from": "a2", "to": "a1", "type": "connects_to"},
                {"from": "a3", "to": "a2", "type": "depends_on"},
            ],
        }
    )
    report = engine.calculate("BLOCK_IP", "a1")
    assert "a2" in report.cascade_assets, report
    assert "a3" in report.cascade_assets, report


if __name__ == "__main__":
    check_t1_timezone()
    check_t1_priority_separation()
    check_t1_freq_cache_prune()
    check_t5_bidirectional_propagation()
    check_t5_cycle_safe()
    print("SELF-CHECK PASSED")
