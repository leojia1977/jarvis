#!/usr/bin/env python3
"""
SecuPilot Phase 0: Mock Data Generator
生成全部 POC 所需的 Mock 数据集
"""

import json
import random
import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT_DIR / "mock_data"
DEFAULT_SEED = 20260407
UTC = timezone.utc

# ============================================================
# 1. 资产字典 (20 个资产)
# ============================================================

ASSETS = [
    # 高权重 (3个)
    {"asset_id": "FINANCE-DB-01", "ip_address": "10.1.5.10", "criticality_weight": 10,
     "business_unit": "Finance", "hostname": "fin-db-prod-01",
     "known_behaviors": ["nightly_db_backup", "quarterly_audit_scan", "high_volume_transactions"],
     "last_compromised_date": None, "owner": "DBA组-王工", "network_segment": "VLAN-Finance-01",
     "os": "Oracle Linux 8", "role": "Core Financial Database"},
    {"asset_id": "AD-CTRL-01", "ip_address": "10.1.1.5", "criticality_weight": 9,
     "business_unit": "IT-Infra", "hostname": "ad-dc-primary",
     "known_behaviors": ["ldap_auth_bursts", "group_policy_sync", "dns_resolution"],
     "last_compromised_date": None, "owner": "基础架构-李工", "network_segment": "VLAN-Core-01",
     "os": "Windows Server 2022", "role": "Primary Domain Controller"},
    {"asset_id": "CEO-WS-01", "ip_address": "10.1.10.2", "criticality_weight": 8,
     "business_unit": "Executive", "hostname": "ceo-laptop-01",
     "known_behaviors": ["vpn_remote_access", "cloud_storage_sync", "video_conferencing"],
     "last_compromised_date": None, "owner": "行政办-CEO", "network_segment": "VLAN-Exec-01",
     "os": "Windows 11 Pro", "role": "CEO Workstation"},
    # 中权重 (7个)
    {"asset_id": "MAIL-GW-01", "ip_address": "10.1.2.10", "criticality_weight": 7,
     "business_unit": "IT-Infra", "hostname": "mail-gateway-01",
     "known_behaviors": ["spam_filter_scan", "attachment_sandbox", "tls_handshake"],
     "last_compromised_date": None, "owner": "运维组-张工", "network_segment": "VLAN-DMZ-01",
     "os": "Ubuntu 22.04", "role": "Email Security Gateway"},
    {"asset_id": "VPN-SRV-01", "ip_address": "10.1.2.20", "criticality_weight": 6,
     "business_unit": "IT-Infra", "hostname": "vpn-concentrator-01",
     "known_behaviors": ["ssl_vpn_reconnect", "mfa_challenge", "split_tunnel"],
     "last_compromised_date": None, "owner": "运维组-张工", "network_segment": "VLAN-DMZ-01",
     "os": "FortiOS 7.4", "role": "VPN Concentrator"},
    {"asset_id": "HR-PORTAL-01", "ip_address": "10.1.6.10", "criticality_weight": 5,
     "business_unit": "HR", "hostname": "hr-webapp-01",
     "known_behaviors": ["monthly_payroll_batch", "annual_review_peak", "onboarding_bulk"],
     "last_compromised_date": None, "owner": "人力资源-赵工", "network_segment": "VLAN-HR-01",
     "os": "RHEL 9", "role": "HR Management System"},
    {"asset_id": "WEB-SRV-01", "ip_address": "10.1.3.10", "criticality_weight": 6,
     "business_unit": "Product", "hostname": "web-frontend-01",
     "known_behaviors": ["cdn_origin_pull", "health_check_ping", "ssl_cert_renewal"],
     "last_compromised_date": None, "owner": "研发-钱工", "network_segment": "VLAN-DMZ-02",
     "os": "Ubuntu 22.04", "role": "Public Web Server"},
    {"asset_id": "CI-CD-01", "ip_address": "10.1.8.10", "criticality_weight": 5,
     "business_unit": "Engineering", "hostname": "jenkins-master-01",
     "known_behaviors": ["pipeline_scan", "artifact_push", "container_build"],
     "last_compromised_date": None, "owner": "DevOps-孙工", "network_segment": "VLAN-Dev-01",
     "os": "Ubuntu 22.04", "role": "CI/CD Pipeline Server"},
    {"asset_id": "BACKUP-SRV-01", "ip_address": "10.1.9.10", "criticality_weight": 5,
     "business_unit": "IT-Infra", "hostname": "backup-server-01",
     "known_behaviors": ["nightly_full_backup", "weekly_offsite_sync", "retention_cleanup"],
     "last_compromised_date": None, "owner": "运维组-张工", "network_segment": "VLAN-Infra-01",
     "os": "Windows Server 2022", "role": "Backup Server"},
    {"asset_id": "SIEM-SRV-01", "ip_address": "10.1.9.20", "criticality_weight": 7,
     "business_unit": "Security", "hostname": "splunk-indexer-01",
     "known_behaviors": ["log_ingestion_burst", "search_head_query", "forwarder_heartbeat"],
     "last_compromised_date": None, "owner": "安全组-周工", "network_segment": "VLAN-Infra-01",
     "os": "RHEL 9", "role": "SIEM Indexer (Splunk)"},
    # 低权重 (10个)
    {"asset_id": "TEST-LNX-01", "ip_address": "10.1.2.4", "criticality_weight": 2,
     "business_unit": "QA", "hostname": "test-ubuntu-01",
     "known_behaviors": ["automated_scan", "pentest_traffic"],
     "last_compromised_date": "2025-11-12T00:00:00Z", "owner": "QA-无人管理", "network_segment": "VLAN-Test-01",
     "os": "Ubuntu 20.04", "role": "Unmanaged Test Server"},
    {"asset_id": "TEST-LNX-02", "ip_address": "10.1.2.5", "criticality_weight": 2,
     "business_unit": "QA", "hostname": "test-centos-01",
     "known_behaviors": ["automated_scan"],
     "last_compromised_date": None, "owner": "QA-无人管理", "network_segment": "VLAN-Test-01",
     "os": "CentOS 7", "role": "Legacy Test Server"},
    {"asset_id": "DEV-WS-01", "ip_address": "10.1.8.50", "criticality_weight": 3,
     "business_unit": "Engineering", "hostname": "dev-workstation-01",
     "known_behaviors": ["npm_install_burst", "docker_pull", "git_clone"],
     "last_compromised_date": None, "owner": "研发-小刘", "network_segment": "VLAN-Dev-01",
     "os": "macOS 14", "role": "Developer Workstation"},
    {"asset_id": "DEV-WS-02", "ip_address": "10.1.8.51", "criticality_weight": 3,
     "business_unit": "Engineering", "hostname": "dev-workstation-02",
     "known_behaviors": ["npm_install_burst", "docker_pull"],
     "last_compromised_date": None, "owner": "研发-小陈", "network_segment": "VLAN-Dev-01",
     "os": "Ubuntu 22.04", "role": "Developer Workstation"},
    {"asset_id": "PRINTER-01", "ip_address": "10.1.7.100", "criticality_weight": 1,
     "business_unit": "Admin", "hostname": "floor3-printer",
     "known_behaviors": ["snmp_poll", "print_job_queue"],
     "last_compromised_date": None, "owner": "行政-无指定", "network_segment": "VLAN-Office-01",
     "os": "Embedded", "role": "Network Printer"},
    {"asset_id": "GUEST-AP-01", "ip_address": "10.1.99.1", "criticality_weight": 1,
     "business_unit": "IT-Infra", "hostname": "guest-wifi-ap-01",
     "known_behaviors": ["dhcp_lease", "captive_portal_redirect"],
     "last_compromised_date": None, "owner": "运维组-张工", "network_segment": "VLAN-Guest-01",
     "os": "Aruba OS", "role": "Guest WiFi Access Point"},
    {"asset_id": "CONF-RM-01", "ip_address": "10.1.7.110", "criticality_weight": 1,
     "business_unit": "Admin", "hostname": "conf-room-display",
     "known_behaviors": ["calendar_sync", "screen_cast"],
     "last_compromised_date": None, "owner": "行政-无指定", "network_segment": "VLAN-Office-01",
     "os": "Android 13", "role": "Conference Room Display"},
    {"asset_id": "IOT-SENSOR-01", "ip_address": "10.1.99.50", "criticality_weight": 1,
     "business_unit": "Facilities", "hostname": "env-sensor-floor3",
     "known_behaviors": ["mqtt_telemetry", "firmware_check"],
     "last_compromised_date": None, "owner": "物业-无指定", "network_segment": "VLAN-IoT-01",
     "os": "Embedded Linux", "role": "Environmental Sensor"},
    {"asset_id": "WKST-047", "ip_address": "10.1.5.22", "criticality_weight": 3,
     "business_unit": "Finance", "hostname": "fin-analyst-ws-01",
     "known_behaviors": ["high_volume_printing", "nightly_db_backup"],
     "last_compromised_date": "2025-11-12T00:00:00Z", "owner": "财务-林分析师", "network_segment": "VLAN-Finance-01",
     "os": "Windows 11 Pro", "role": "Financial Analyst Workstation"},
    {"asset_id": "KIOSK-01", "ip_address": "10.1.7.200", "criticality_weight": 1,
     "business_unit": "Admin", "hostname": "lobby-kiosk",
     "known_behaviors": ["visitor_checkin", "badge_print"],
     "last_compromised_date": None, "owner": "行政-前台", "network_segment": "VLAN-Office-01",
     "os": "Windows 10 IoT", "role": "Visitor Check-in Kiosk"},
]

NOISE_TEMPLATES = [
    {"activity_name": "PORT_SCAN", "severity": "LOW"},
    {"activity_name": "DNS_QUERY_NORMAL", "severity": "INFO"},
    {"activity_name": "FIREWALL_BLOCK", "severity": "LOW"},
    {"activity_name": "VULNERABILITY_SCAN", "severity": "LOW"},
    {"activity_name": "HEALTH_CHECK", "severity": "INFO"},
    {"activity_name": "SSL_CERT_RENEWAL", "severity": "INFO"},
    {"activity_name": "BACKUP_JOB", "severity": "INFO"},
    {"activity_name": "LDAP_AUTH", "severity": "INFO"},
    {"activity_name": "ANTIVIRUS_UPDATE", "severity": "INFO"},
    {"activity_name": "NTP_SYNC", "severity": "INFO"},
    {"activity_name": "SNMP_POLL", "severity": "INFO"},
    {"activity_name": "VPN_RECONNECT", "severity": "LOW"},
    {"activity_name": "CDN_ORIGIN_PULL", "severity": "INFO"},
]

EXTERNAL_IPS = [
    "45.33.32.156", "104.236.198.48", "198.51.100.23", "203.0.113.45",
    "93.184.216.34", "151.101.1.140", "172.217.14.206", "20.190.190.1",
]


def to_utc_iso(ts: datetime) -> str:
    """统一输出标准 UTC 时间戳，避免 naive datetime + Z 的伪 UTC 问题。"""
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=UTC)
    return ts.astimezone(UTC).isoformat().replace("+00:00", "Z")


def generate_noise_alerts(count, base_time):
    alerts = []
    for i in range(count):
        t = NOISE_TEMPLATES[i % len(NOISE_TEMPLATES)]
        a = ASSETS[i % len(ASSETS)]
        offset = timedelta(seconds=random.randint(0, 43200))
        alerts.append({
            "event_id": f"NOISE-{i:06d}",
            "event_time": to_utc_iso(base_time - offset),
            "source_ip": random.choice(EXTERNAL_IPS) if random.random() > 0.3 else a["ip_address"],
            "destination_asset_id": a["asset_id"],
            "activity_name": t["activity_name"],
            "severity": t["severity"],
            "enrichment": {"threat_intel_flag": False, "is_historical_fp": random.random() > 0.7},
            "triage_result": "AUTO_ARCHIVED"
        })
    return alerts


def generate_scenario_alerts(scenario):
    alerts = []
    for idx, raw in enumerate(scenario["alerts"]):
        dest = next((a for a in ASSETS if a["asset_id"] == raw.get("dest_asset")), None)
        alerts.append({
            "event_id": f"{scenario['scenario_id']}-{idx:03d}",
            "event_time": raw["event_time"],
            "source_ip": raw["source_ip"],
            "destination_asset_id": raw.get("dest_asset", "EXTERNAL"),
            "destination_ip": dest["ip_address"] if dest else raw.get("extra", {}).get("dest_ip", "0.0.0.0"),
            "activity_name": raw["activity_name"],
            "severity": raw["severity"],
            "count": raw.get("count", 1),
            "process_name": raw.get("process_name"),
            "parent_process": raw.get("parent_process"),
            "enrichment": {
                "threat_intel_flag": raw["severity"] in ("HIGH", "CRITICAL"),
                "is_historical_fp": False,
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["name"],
                "kill_chain": scenario.get("kill_chain", ""),
            },
            "extra": raw.get("extra", {})
        })
    return alerts


def generate_fp_baseline():
    patterns = []
    categories = [
        ("financial_batch", ["每日对账批处理", "ATM心跳", "交易系统高频连接", "反洗钱扫描", "风控规则更新"]),
        ("it_operations", ["Nessus漏扫", "Windows Update", "SNMP轮询", "健康检查", "AD组策略同步", "DHCP续期", "NTP同步", "RADIUS认证"]),
        ("security_tools", ["渗透测试流量", "EDR全盘扫描", "邮件沙箱", "DLP检查"]),
        ("devops", ["CI/CD构建", "Docker拉取", "K8s探针", "Prometheus采集"]),
    ]
    idx = 0
    for cat, descs in categories:
        for desc in descs:
            for _ in range(random.randint(25, 55)):
                patterns.append({
                    "baseline_id": f"FP-{idx:04d}", "category": cat,
                    "pattern_description": desc,
                    "confidence": round(random.uniform(0.85, 0.99), 2)
                })
                idx += 1
                if idx >= 1000:
                    return patterns
    return patterns[:1000]


def generate_ioc_db():
    return {
        "malicious_ips": [
            {"ip": "45.33.49.12", "threat_type": "C2", "actor": "APT-BEAR", "confidence": 0.95, "country": "RU"},
            {"ip": "185.220.101.45", "threat_type": "C2", "actor": "RANSOMWARE-X", "confidence": 0.98, "country": "NL"},
            {"ip": "91.215.85.100", "threat_type": "Scanner", "actor": "Unknown", "confidence": 0.60, "country": "UA"},
        ] + [{"ip": f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
              "threat_type": random.choice(["Scanner", "Botnet", "Spam"]), "actor": "Unknown",
              "confidence": round(random.uniform(0.4, 0.7), 2), "country": random.choice(["US", "CN", "RU", "BR"])}
             for _ in range(17)],
        "malicious_domains": [
            {"domain": "data.evil-c2.example.com", "threat_type": "C2", "confidence": 0.95},
            {"domain": "update.legit-looking.xyz", "threat_type": "Malware", "confidence": 0.90},
        ] + [{"domain": f"{uuid.uuid4().hex[:8]}.{random.choice(['xyz','tk','cc'])}",
              "threat_type": "Phishing", "confidence": round(random.uniform(0.5, 0.85), 2)} for _ in range(13)],
        "malicious_hashes": [
            {"hash": hashlib.sha256(f"malware_{i}".encode()).hexdigest(),
             "family": random.choice(["Cobalt Strike", "Mimikatz", "Rubeus", "LockBit", "BlackCat"]),
             "confidence": round(random.uniform(0.7, 0.99), 2)} for i in range(10)],
        "c2_signatures": [
            {"pattern": "beacon_interval=60s,jitter=10%", "family": "Cobalt Strike", "confidence": 0.97},
            {"pattern": "dns_txt_exfil,base64", "family": "DNSCat2", "confidence": 0.90},
            {"pattern": "http_post,/api/v1/report", "family": "Metasploit", "confidence": 0.85},
        ]
    }


def generate_knowledge_graph():
    users = [
        {"user_id": "user_ceo", "name": "CEO", "role": "Executive"},
        {"user_id": "user_lin", "name": "林分析师", "role": "L1_Analyst"},
        {"user_id": "user_zhou", "name": "周工", "role": "L2_Analyst"},
        {"user_id": "user_zhang", "name": "张工", "role": "SysAdmin"},
        {"user_id": "user_wang", "name": "王工", "role": "DBA"},
        {"user_id": "user_qian", "name": "钱工", "role": "Developer"},
        {"user_id": "user_sun", "name": "孙工", "role": "DevOps"},
        {"user_id": "user_zhao", "name": "赵工", "role": "HR_Admin"},
        {"user_id": "user_liu", "name": "小刘", "role": "Developer"},
        {"user_id": "user_chen", "name": "小陈", "role": "Developer"},
        {"user_id": "user_li", "name": "李工", "role": "SysAdmin"},
        {"user_id": "user_intern", "name": "实习生A", "role": "Intern"},
    ]
    segments = [
        {"id": "VLAN-Finance-01", "zone": "High"}, {"id": "VLAN-Core-01", "zone": "Critical"},
        {"id": "VLAN-Exec-01", "zone": "High"}, {"id": "VLAN-DMZ-01", "zone": "Medium"},
        {"id": "VLAN-DMZ-02", "zone": "Medium"}, {"id": "VLAN-HR-01", "zone": "Medium"},
        {"id": "VLAN-Dev-01", "zone": "Low"}, {"id": "VLAN-Test-01", "zone": "Low"},
        {"id": "VLAN-Infra-01", "zone": "High"}, {"id": "VLAN-Office-01", "zone": "Low"},
        {"id": "VLAN-Guest-01", "zone": "Untrusted"}, {"id": "VLAN-IoT-01", "zone": "Untrusted"},
    ]
    rels = []
    access_map = {"user_ceo": ["CEO-WS-01"], "user_wang": ["FINANCE-DB-01"], "user_li": ["AD-CTRL-01"],
                  "user_zhang": ["VPN-SRV-01", "MAIL-GW-01"], "user_liu": ["DEV-WS-01", "CI-CD-01"],
                  "user_chen": ["DEV-WS-02"], "user_zhao": ["HR-PORTAL-01"], "user_sun": ["CI-CD-01"]}
    for uid, aids in access_map.items():
        for aid in aids:
            rels.append({"from": uid, "to": aid, "type": "accesses"})
    for a in ASSETS:
        rels.append({"from": a["asset_id"], "to": a["network_segment"], "type": "belongs_to"})

    # 关键业务依赖，供 T5 真实级联影响分析使用
    rels.extend([
        {"from": "FINANCE-DB-01", "to": "AD-CTRL-01", "type": "depends_on"},
        {"from": "HR-PORTAL-01", "to": "AD-CTRL-01", "type": "depends_on"},
        {"from": "MAIL-GW-01", "to": "AD-CTRL-01", "type": "depends_on"},
        {"from": "VPN-SRV-01", "to": "AD-CTRL-01", "type": "depends_on"},
        {"from": "CI-CD-01", "to": "AD-CTRL-01", "type": "depends_on"},
        {"from": "WKST-047", "to": "FINANCE-DB-01", "type": "connects_to"},
        {"from": "DEV-WS-01", "to": "WKST-047", "type": "connects_to"},
        {"from": "DEV-WS-01", "to": "CI-CD-01", "type": "depends_on"},
        {"from": "DEV-WS-02", "to": "CI-CD-01", "type": "depends_on"},
        {"from": "CEO-WS-01", "to": "VPN-SRV-01", "type": "connects_to"},
        {"from": "HR-PORTAL-01", "to": "BACKUP-SRV-01", "type": "critical_service"},
        {"from": "BACKUP-SRV-01", "to": "FINANCE-DB-01", "type": "critical_service"},
        {"from": "SIEM-SRV-01", "to": "FINANCE-DB-01", "type": "connects_to"},
        {"from": "SIEM-SRV-01", "to": "AD-CTRL-01", "type": "connects_to"},
        {"from": "WEB-SRV-01", "to": "MAIL-GW-01", "type": "connects_to"},
    ])
    return {"nodes": {"assets": ASSETS, "users": users, "segments": segments}, "relationships": rels}


def generate_siem_responses():
    return {
        "adapter_type": "mock_splunk", "api_version": "1.0",
        "queries": {
            "summarize_recent_12h": {
                "response": {
                    "total_events": 50247, "noise_archived": 50227, "alerts_for_review": 20,
                    "critical_count": 3, "high_count": 8, "medium_count": 9,
                    "top_targeted_assets": [
                        {"asset_id": "FINANCE-DB-01", "count": 8},
                        {"asset_id": "AD-CTRL-01", "count": 5},
                        {"asset_id": "HR-PORTAL-01", "count": 4}
                    ],
                    "silent_watch_status": "YELLOW",
                    "silent_watch_summary": "有 1 件紧急事件需要你过目。"
                }
            },
            "query_asset_alerts": {"input": {"asset_id": "str", "time_range": "str"}, "response_ref": "scenario_by_asset"},
            "query_ip_history": {"input": {"ip": "str", "time_range": "str"}, "response": {
                "ip": "10.1.2.4", "asset_id": "TEST-LNX-01", "total_events_7d": 1250,
                "protocols": ["SSH", "LDAP", "HTTP"], "summary": "该IP主要进行SSH连接尝试和LDAP查询"
            }}
        }
    }


# 攻击场景（完整定义）
SCENARIOS = [
    {"scenario_id": "S-01", "name": "SSH Brute Force", "risk_score": 7.5, "confidence": 0.95,
     "kill_chain": "Initial Access → Credential Access",
     "alerts": [
         {"event_time": "2026-04-01T02:15:33Z", "source_ip": "10.1.2.4", "dest_asset": "FINANCE-DB-01",
          "activity_name": "SSH_LOGIN_FAILURE", "activity_id": 1, "count": 200,
          "process_name": "hydra", "parent_process": "/bin/bash", "severity": "HIGH"},
         {"event_time": "2026-04-01T02:18:45Z", "source_ip": "10.1.2.4", "dest_asset": "FINANCE-DB-01",
          "activity_name": "SSH_LOGIN_FAILURE", "activity_id": 1, "count": 150,
          "process_name": "hydra", "parent_process": "/bin/bash", "severity": "HIGH"},
         {"event_time": "2026-04-01T02:22:10Z", "source_ip": "10.1.2.4", "dest_asset": "AD-CTRL-01",
          "activity_name": "LDAP_QUERY_BURST", "activity_id": 6, "count": 50,
          "process_name": "ldapsearch", "parent_process": "/bin/bash", "severity": "MEDIUM"},
         {"event_time": "2026-04-01T02:25:00Z", "source_ip": "10.1.2.4", "dest_asset": "FINANCE-DB-01",
          "activity_name": "SSH_LOGIN_FAILURE", "activity_id": 1, "count": 150,
          "process_name": "hydra", "parent_process": "/bin/bash", "severity": "HIGH"},
     ],
     "narrative_arc": {
         "timeline": [
             {"ts": "02:15", "event": "首次SSH爆破（200次）", "significance": "起点"},
             {"ts": "02:18", "event": "持续爆破", "significance": "升级"},
             {"ts": "02:22", "event": "LDAP枚举", "significance": "侦察"},
             {"ts": "02:25", "event": "新字典攻击", "significance": "持续"}
         ],
         "motive": "利用无人管理测试机跳板攻击财务DB",
         "kill_chain_stage": "Credential Access → Discovery"
     },
     "action": {"type": "NETWORK_ISOLATE", "target": "TEST-LNX-01",
                "blast_radius": "测试网段2台机器断网，不影响生产"}},
    {"scenario_id": "S-02", "name": "Lateral Movement + Privilege Escalation", "risk_score": 9.2, "confidence": 0.92,
     "kill_chain": "Lateral Movement → Privilege Escalation → Collection",
     "alerts": [
         {"event_time": "2026-04-01T01:30:00Z", "source_ip": "10.1.8.50", "dest_asset": "WKST-047",
          "activity_name": "SMB_ADMIN_SHARE", "activity_id": 3, "count": 1,
          "process_name": "smbclient", "parent_process": "powershell.exe", "severity": "HIGH"},
         {"event_time": "2026-04-01T01:32:15Z", "source_ip": "10.1.8.50", "dest_asset": "WKST-047",
          "activity_name": "REMOTE_SERVICE_INSTALL", "activity_id": 4, "count": 1,
          "process_name": "psexec.exe", "parent_process": "cmd.exe", "severity": "CRITICAL"},
         {"event_time": "2026-04-01T01:35:00Z", "source_ip": "10.1.5.22", "dest_asset": "AD-CTRL-01",
          "activity_name": "KERBEROASTING", "activity_id": 6, "count": 15,
          "process_name": "rubeus.exe", "parent_process": "svchost.exe", "severity": "CRITICAL"},
         {"event_time": "2026-04-01T01:38:22Z", "source_ip": "10.1.5.22", "dest_asset": "AD-CTRL-01",
          "activity_name": "DCSYNC_ATTEMPT", "activity_id": 7, "count": 1,
          "process_name": "mimikatz.exe", "parent_process": "cmd.exe", "severity": "CRITICAL"},
         {"event_time": "2026-04-01T01:40:00Z", "source_ip": "10.1.5.22", "dest_asset": "FINANCE-DB-01",
          "activity_name": "DB_PRIVILEGE_ESCALATION", "activity_id": 5, "count": 1,
          "process_name": "sqlplus", "parent_process": "cmd.exe", "severity": "CRITICAL"},
     ],
     "narrative_arc": {
         "timeline": [
             {"ts": "01:30", "event": "SMB横向移动至财务工作站", "significance": "起点"},
             {"ts": "01:32", "event": "PsExec提权", "significance": "权限提升"},
             {"ts": "01:35", "event": "Kerberoasting攻击AD", "significance": "凭证窃取"},
             {"ts": "01:38", "event": "DCSync复制域控Hash", "significance": "关键转折"},
             {"ts": "01:40", "event": "登录财务数据库", "significance": "目标达成"}
         ],
         "motive": "APT从开发环境渗透至核心财务系统",
         "kill_chain_stage": "Lateral Movement → Privilege Escalation → Collection"
     },
     "action": {"type": "EMERGENCY_ISOLATE_MULTI", "targets": ["DEV-WS-01", "WKST-047"],
                "blast_radius": "隔离1台开发机+1台财务工作站，建议重置AD管理员密码"}},
    {"scenario_id": "S-03", "name": "Data Exfiltration", "risk_score": 8.8, "confidence": 0.88,
     "kill_chain": "Collection → Exfiltration",
     "alerts": [
         {"event_time": "2026-03-31T23:45:00Z", "source_ip": "10.1.5.22", "dest_asset": "EXTERNAL",
          "activity_name": "LARGE_OUTBOUND_TRANSFER", "activity_id": 9, "count": 1,
          "process_name": "curl", "parent_process": "bash", "severity": "HIGH",
          "extra": {"dest_ip": "45.33.49.12", "bytes_out": 524288000}},
         {"event_time": "2026-03-31T23:52:00Z", "source_ip": "10.1.5.22", "dest_asset": "EXTERNAL",
          "activity_name": "DNS_TXT_ANOMALY", "activity_id": 10, "count": 150,
          "process_name": "nslookup", "parent_process": "bash", "severity": "MEDIUM",
          "extra": {"query_domain": "data.evil-c2.example.com"}},
         {"event_time": "2026-04-01T00:05:00Z", "source_ip": "10.1.5.22", "dest_asset": "EXTERNAL",
          "activity_name": "LARGE_OUTBOUND_TRANSFER", "activity_id": 9, "count": 1,
          "process_name": "curl", "parent_process": "bash", "severity": "HIGH",
          "extra": {"dest_ip": "45.33.49.12", "bytes_out": 314572800}},
     ],
     "narrative_arc": {
         "timeline": [
             {"ts": "23:45", "event": "深夜传输500MB加密数据", "significance": "起点"},
             {"ts": "23:52", "event": "DNS隧道通信", "significance": "隐蔽通道"},
             {"ts": "00:05", "event": "第二批300MB数据传输", "significance": "持续外泄"}
         ],
         "motive": "利用深夜窗口批量外泄财务数据",
         "kill_chain_stage": "Collection → Exfiltration"
     },
     "action": {"type": "ISOLATE_AND_BLOCK", "target": "WKST-047",
                "blast_radius": "隔离财务工作站+封锁外泄目标IP"}},
    {"scenario_id": "S-04", "name": "Ransomware Precursor", "risk_score": 9.5, "confidence": 0.97,
     "kill_chain": "C2 → Impact (Pre-stage)",
     "alerts": [
         {"event_time": "2026-04-01T03:00:00Z", "source_ip": "10.1.6.10", "dest_asset": "EXTERNAL",
          "activity_name": "C2_BEACON", "activity_id": 11, "count": 30,
          "process_name": "svchost.exe", "parent_process": "services.exe", "severity": "CRITICAL",
          "extra": {"dest_ip": "185.220.101.45", "beacon_interval": "60s"}},
         {"event_time": "2026-04-01T03:10:00Z", "source_ip": "10.1.6.10", "dest_asset": "HR-PORTAL-01",
          "activity_name": "MASS_FILE_ENUM", "activity_id": 12, "count": 15000,
          "process_name": "explorer.exe", "parent_process": "svchost.exe", "severity": "HIGH"},
         {"event_time": "2026-04-01T03:15:00Z", "source_ip": "10.1.6.10", "dest_asset": "HR-PORTAL-01",
          "activity_name": "VSSADMIN_DELETE", "activity_id": 13, "count": 1,
          "process_name": "vssadmin.exe", "parent_process": "cmd.exe", "severity": "CRITICAL"},
     ],
     "narrative_arc": {
         "timeline": [
             {"ts": "03:00", "event": "C2信标通信", "significance": "起点"},
             {"ts": "03:10", "event": "枚举15000文件", "significance": "加密预备"},
             {"ts": "03:15", "event": "删除卷影副本", "significance": "关键转折"}
         ],
         "motive": "HR系统已被植入勒索软件，正在执行加密前准备",
         "kill_chain_stage": "C2 → Actions on Objectives"
     },
     "action": {"type": "EMERGENCY_ISOLATE", "target": "HR-PORTAL-01", "priority": "IMMEDIATE",
                "blast_radius": "HR门户不可用（影响800人请假/报销），但阻止勒索扩散"}},
    {"scenario_id": "S-05", "name": "Insider Threat", "risk_score": 6.5, "confidence": 0.72,
     "kill_chain": "Collection (Insider)",
     "alerts": [
         {"event_time": "2026-03-31T22:30:00Z", "source_ip": "10.1.10.2", "dest_asset": "FINANCE-DB-01",
          "activity_name": "DB_LOGIN_OFF_HOURS", "activity_id": 14, "count": 1,
          "process_name": "ssms.exe", "parent_process": "explorer.exe", "severity": "MEDIUM",
          "extra": {"username": "ceo_account"}},
         {"event_time": "2026-03-31T22:35:00Z", "source_ip": "10.1.10.2", "dest_asset": "FINANCE-DB-01",
          "activity_name": "SENSITIVE_TABLE_ACCESS", "activity_id": 15, "count": 5,
          "process_name": "ssms.exe", "parent_process": "explorer.exe", "severity": "MEDIUM",
          "extra": {"tables": ["salary_records", "bonus_allocation", "stock_options"]}},
         {"event_time": "2026-03-31T22:45:00Z", "source_ip": "10.1.10.2", "dest_asset": "FINANCE-DB-01",
          "activity_name": "DATA_EXPORT_CSV", "activity_id": 16, "count": 3,
          "process_name": "ssms.exe", "parent_process": "explorer.exe", "severity": "MEDIUM",
          "extra": {"rows": 2500}},
     ],
     "narrative_arc": {
         "timeline": [
             {"ts": "22:30", "event": "CEO工作站非工作时间登录财务DB", "significance": "起点"},
             {"ts": "22:35", "event": "访问薪资/奖金/期权表", "significance": "敏感数据"},
             {"ts": "22:45", "event": "导出2500行CSV", "significance": "数据导出"}
         ],
         "motive": "可能CEO本人查询或账号被盗用，需人工确认",
         "kill_chain_stage": "Collection (Insider - Unconfirmed)"
     },
     "action": {"type": "ALERT_AND_CONFIRM", "target": "CEO-WS-01",
                "blast_radius": "不建议直接隔离CEO工作站，建议联系本人确认"}},
]


def main(seed: int = DEFAULT_SEED):
    print("=" * 60)
    print("SecuPilot Phase 0: Mock Data Generation")
    print("=" * 60)
    random.seed(seed)
    print(f"Seed: {seed}")

    for subdir in ["alerts", "assets", "baselines", "scenarios", "threat_intel", "siem_adapter", "knowledge_graph"]:
        (BASE_DIR / subdir).mkdir(parents=True, exist_ok=True)

    # 1. Assets
    print("\n[1/8] Assets...")
    with open(BASE_DIR / "assets" / "asset_dictionary.json", "w", encoding="utf-8") as f:
        json.dump({"assets": ASSETS, "total": 20}, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 20 assets")

    # 2. Scenario alerts
    print("\n[2/8] Attack scenarios...")
    all_scenario_alerts = []
    for s in SCENARIOS:
        alerts = generate_scenario_alerts(s)
        all_scenario_alerts.extend(alerts)
        with open(BASE_DIR / "alerts" / f"scenario_{s['scenario_id'].lower().replace('-','_')}.json", "w", encoding="utf-8") as f:
            json.dump({"scenario": s, "alerts": alerts}, f, ensure_ascii=False, indent=2)
        print(f"  ✅ {s['scenario_id']}: {s['name']} ({len(alerts)} alerts)")

    # 3. Noise
    noise_count = 50000 - len(all_scenario_alerts)
    print(f"\n[3/8] Noise alerts ({noise_count})...")
    noise = generate_noise_alerts(noise_count, datetime(2026, 4, 1, 8, 0, 0, tzinfo=UTC))
    with open(BASE_DIR / "alerts" / "noise_baseline.json", "w", encoding="utf-8") as f:
        json.dump({"total": len(noise), "sample": noise[:100]}, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {noise_count} noise (100 samples stored)")

    # 4. FP Baseline
    print("\n[4/8] False positive baseline...")
    fps = generate_fp_baseline()
    with open(BASE_DIR / "baselines" / "false_positive_baseline.json", "w", encoding="utf-8") as f:
        json.dump({"total": len(fps), "baselines": fps}, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {len(fps)} patterns")

    # 5. IOC
    print("\n[5/8] IOC database...")
    ioc = generate_ioc_db()
    with open(BASE_DIR / "threat_intel" / "mock_ioc_database.json", "w", encoding="utf-8") as f:
        json.dump(ioc, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {len(ioc['malicious_ips'])+len(ioc['malicious_domains'])+len(ioc['malicious_hashes'])} IOCs")

    # 6. Knowledge Graph
    print("\n[6/8] Knowledge Graph...")
    kg = generate_knowledge_graph()
    with open(BASE_DIR / "knowledge_graph" / "entity_relationships.json", "w", encoding="utf-8") as f:
        json.dump(kg, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {len(kg['relationships'])} relationships")

    # 7. SIEM Adapter
    print("\n[7/8] Mock SIEM Adapter...")
    siem = generate_siem_responses()
    with open(BASE_DIR / "siem_adapter" / "mock_splunk_responses.json", "w", encoding="utf-8") as f:
        json.dump(siem, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {len(siem['queries'])} queries")

    # 8. Demo Scenarios
    print("\n[8/8] Demo scenarios...")
    demos = [
        {"id": "DEMO-01", "input": "最近还好吗？", "intent": "SUMMARIZE_RECENT", "scenario": None},
        {"id": "DEMO-02", "input": "昨晚财务服务器还好吗？", "intent": "ASSET_QUERY", "scenario": "S-01"},
        {"id": "DEMO-03", "input": "帮我查一下内网有没有横向移动", "intent": "THREAT_HUNT", "scenario": "S-02"},
        {"id": "DEMO-04", "input": "有没有异常的外发流量？", "intent": "DATA_EXFIL_CHECK", "scenario": "S-03"},
        {"id": "DEMO-05", "input": "[SYSTEM] risk=9.5", "intent": "HIGH_RISK_INTERRUPT", "scenario": "S-04"},
    ]
    with open(BASE_DIR / "scenarios" / "demo_scenarios.json", "w", encoding="utf-8") as f:
        json.dump({"demos": demos}, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {len(demos)} demos")

    print("\n" + "=" * 60)
    print("✅ Phase 0 Mock Data Complete!")
    print(f"  Total: 50,000 alerts | 20 assets | {len(fps)} FP | 5 scenarios")
    print("=" * 60)


if __name__ == "__main__":
    main()
