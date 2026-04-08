#!/usr/bin/env python3
"""
SecuPilot Sprint 2: 行为事件生成器
生成符合冻结协议的 ProcessEvent 数据，供 T3 证据编译器消费

5 种事件类型：process_create / network_connect / dns_query / registry_set / file_write
每个攻击场景生成完整的行为事件序列（不只是告警，是底层原始行为日志）
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "mock_data" / "process_events"
LEGACY_OUTPUT_DIR = ROOT_DIR / "process_events"


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# ============================================================
# 场景 S-02：横向移动 + 权限提升（完整行为事件链）
# 攻击路径：DEV-WS-01 → WKST-047 → AD-CTRL-01 → FINANCE-DB-01
# ============================================================

S02_DEV_WS_01_EVENTS = [
    # 正常进程基线（explorer 启动 cmd 是日常操作的一部分，但后续链条异常）
    {"event_type": "process_create", "pid": 4200, "ppid": 1, "process_name": "services.exe",
     "exe_path": "C:\\Windows\\System32\\services.exe", "command_line": "services.exe",
     "user": "SYSTEM", "timestamp": "2026-04-01T00:00:00Z", "host_id": "DEV-WS-01"},
    {"event_type": "process_create", "pid": 4400, "ppid": 4200, "process_name": "svchost.exe",
     "exe_path": "C:\\Windows\\System32\\svchost.exe", "command_line": "svchost.exe -k netsvcs",
     "user": "SYSTEM", "timestamp": "2026-04-01T00:00:01Z", "host_id": "DEV-WS-01"},
    {"event_type": "process_create", "pid": 4872, "ppid": 1, "process_name": "explorer.exe",
     "exe_path": "C:\\Windows\\explorer.exe", "command_line": "explorer.exe",
     "user": "CORP\\dev-liu", "timestamp": "2026-04-01T01:25:00Z", "host_id": "DEV-WS-01"},

    # ---- 攻击开始 ----
    # Step 1: explorer → cmd.exe（用户启动命令行——可能是社工后执行）
    {"event_type": "process_create", "pid": 5201, "ppid": 4872, "process_name": "cmd.exe",
     "exe_path": "C:\\Windows\\System32\\cmd.exe",
     "command_line": "cmd.exe /c \"net use \\\\10.1.5.22\\admin$ /user:CORP\\admin Pa$$w0rd\"",
     "user": "CORP\\dev-liu", "timestamp": "2026-04-01T01:29:30Z", "host_id": "DEV-WS-01"},

    # Step 1.5: 网络连接到 WKST-047 的 SMB 端口
    {"event_type": "network_connect", "pid": 5201, "ppid": 4872, "process_name": "cmd.exe",
     "exe_path": "C:\\Windows\\System32\\cmd.exe", "command_line": "",
     "user": "CORP\\dev-liu", "timestamp": "2026-04-01T01:29:45Z", "host_id": "DEV-WS-01",
     "src_ip": "10.1.8.50", "dst_ip": "10.1.5.22", "dst_port": 445, "protocol": "TCP"},

    # Step 2: cmd → psexec.exe（横向移动工具）
    {"event_type": "process_create", "pid": 5344, "ppid": 5201, "process_name": "psexec.exe",
     "exe_path": "C:\\Users\\dev-liu\\Downloads\\PsExec64.exe",
     "command_line": "psexec.exe \\\\10.1.5.22 -u CORP\\admin -p Pa$$w0rd -s cmd.exe",
     "user": "CORP\\dev-liu", "timestamp": "2026-04-01T01:30:00Z", "host_id": "DEV-WS-01"},

    # Step 2.5: PsExec 网络连接
    {"event_type": "network_connect", "pid": 5344, "ppid": 5201, "process_name": "psexec.exe",
     "exe_path": "C:\\Users\\dev-liu\\Downloads\\PsExec64.exe", "command_line": "",
     "user": "CORP\\dev-liu", "timestamp": "2026-04-01T01:30:05Z", "host_id": "DEV-WS-01",
     "src_ip": "10.1.8.50", "dst_ip": "10.1.5.22", "dst_port": 445, "protocol": "TCP"},

    # Step 3: 正常 DNS 查询（噪声背景）
    {"event_type": "dns_query", "pid": 4400, "ppid": 4200, "process_name": "svchost.exe",
     "exe_path": "C:\\Windows\\System32\\svchost.exe", "command_line": "",
     "user": "SYSTEM", "timestamp": "2026-04-01T01:30:10Z", "host_id": "DEV-WS-01",
     "query_domain": "ad-dc-primary.corp.local", "query_type": "A"},
]

S02_WKST_047_EVENTS = [
    # WKST-047 上被 PsExec 推送的远程服务
    {"event_type": "process_create", "pid": 3100, "ppid": 1, "process_name": "services.exe",
     "exe_path": "C:\\Windows\\System32\\services.exe", "command_line": "services.exe",
     "user": "SYSTEM", "timestamp": "2026-04-01T00:00:00Z", "host_id": "WKST-047"},

    # PsExec 远程服务安装
    {"event_type": "process_create", "pid": 3800, "ppid": 3100, "process_name": "PSEXESVC.exe",
     "exe_path": "C:\\Windows\\PSEXESVC.exe",
     "command_line": "C:\\Windows\\PSEXESVC.exe",
     "user": "SYSTEM", "timestamp": "2026-04-01T01:32:15Z", "host_id": "WKST-047"},

    # 注册表：PsExec 服务注册
    {"event_type": "registry_set", "pid": 3100, "ppid": 1, "process_name": "services.exe",
     "exe_path": "C:\\Windows\\System32\\services.exe", "command_line": "",
     "user": "SYSTEM", "timestamp": "2026-04-01T01:32:16Z", "host_id": "WKST-047",
     "key_path": "HKLM\\SYSTEM\\CurrentControlSet\\Services\\PSEXESVC",
     "value_name": "ImagePath", "value_data": "C:\\Windows\\PSEXESVC.exe"},

    # PSEXESVC → cmd.exe
    {"event_type": "process_create", "pid": 3900, "ppid": 3800, "process_name": "cmd.exe",
     "exe_path": "C:\\Windows\\System32\\cmd.exe",
     "command_line": "cmd.exe /c whoami && hostname",
     "user": "SYSTEM", "timestamp": "2026-04-01T01:32:30Z", "host_id": "WKST-047"},

    # cmd → rubeus.exe（Kerberoasting 工具）
    {"event_type": "process_create", "pid": 4010, "ppid": 3900, "process_name": "rubeus.exe",
     "exe_path": "C:\\Users\\Public\\rubeus.exe",
     "command_line": "rubeus.exe kerberoast /outfile:hashes.txt",
     "user": "SYSTEM", "timestamp": "2026-04-01T01:35:00Z", "host_id": "WKST-047"},

    # rubeus 写文件
    {"event_type": "file_write", "pid": 4010, "ppid": 3900, "process_name": "rubeus.exe",
     "exe_path": "C:\\Users\\Public\\rubeus.exe", "command_line": "",
     "user": "SYSTEM", "timestamp": "2026-04-01T01:35:30Z", "host_id": "WKST-047",
     "file_path": "C:\\Users\\Public\\hashes.txt",
     "file_hash_sha256": _hash("kerberoast_hashes_content")},

    # Kerberoasting 网络活动
    {"event_type": "network_connect", "pid": 4010, "ppid": 3900, "process_name": "rubeus.exe",
     "exe_path": "C:\\Users\\Public\\rubeus.exe", "command_line": "",
     "user": "SYSTEM", "timestamp": "2026-04-01T01:35:05Z", "host_id": "WKST-047",
     "src_ip": "10.1.5.22", "dst_ip": "10.1.1.5", "dst_port": 88, "protocol": "TCP"},

    # cmd → mimikatz.exe（凭证窃取）
    {"event_type": "process_create", "pid": 4100, "ppid": 3900, "process_name": "mimikatz.exe",
     "exe_path": "C:\\Users\\Public\\mimikatz.exe",
     "command_line": "mimikatz.exe \"lsadump::dcsync /domain:corp.local /user:krbtgt\" exit",
     "user": "SYSTEM", "timestamp": "2026-04-01T01:38:22Z", "host_id": "WKST-047"},

    # DCSync 网络活动
    {"event_type": "network_connect", "pid": 4100, "ppid": 3900, "process_name": "mimikatz.exe",
     "exe_path": "C:\\Users\\Public\\mimikatz.exe", "command_line": "",
     "user": "SYSTEM", "timestamp": "2026-04-01T01:38:25Z", "host_id": "WKST-047",
     "src_ip": "10.1.5.22", "dst_ip": "10.1.1.5", "dst_port": 389, "protocol": "TCP"},

    # mimikatz 写 Hash 文件
    {"event_type": "file_write", "pid": 4100, "ppid": 3900, "process_name": "mimikatz.exe",
     "exe_path": "C:\\Users\\Public\\mimikatz.exe", "command_line": "",
     "user": "SYSTEM", "timestamp": "2026-04-01T01:38:40Z", "host_id": "WKST-047",
     "file_path": "C:\\Users\\Public\\krbtgt_hash.bin",
     "file_hash_sha256": _hash("dcsync_krbtgt_hash")},
]

# ============================================================
# 场景 S-04：勒索软件前兆（HR-PORTAL-01）
# ============================================================

S04_HR_PORTAL_EVENTS = [
    {"event_type": "process_create", "pid": 800, "ppid": 1, "process_name": "services.exe",
     "exe_path": "C:\\Windows\\System32\\services.exe", "command_line": "services.exe",
     "user": "SYSTEM", "timestamp": "2026-04-01T02:50:00Z", "host_id": "HR-PORTAL-01"},
    {"event_type": "process_create", "pid": 1200, "ppid": 800, "process_name": "svchost.exe",
     "exe_path": "C:\\Windows\\System32\\svchost.exe", "command_line": "svchost.exe -k netsvcs",
     "user": "SYSTEM", "timestamp": "2026-04-01T02:50:01Z", "host_id": "HR-PORTAL-01"},

    # C2 信标：svchost 伪装的恶意进程发起外连
    {"event_type": "network_connect", "pid": 1200, "ppid": 800, "process_name": "svchost.exe",
     "exe_path": "C:\\Windows\\System32\\svchost.exe", "command_line": "",
     "user": "SYSTEM", "timestamp": "2026-04-01T03:00:00Z", "host_id": "HR-PORTAL-01",
     "src_ip": "10.1.6.10", "dst_ip": "185.220.101.45", "dst_port": 443, "protocol": "TCP"},

    # DNS 查询可疑域名
    {"event_type": "dns_query", "pid": 1200, "ppid": 800, "process_name": "svchost.exe",
     "exe_path": "C:\\Windows\\System32\\svchost.exe", "command_line": "",
     "user": "SYSTEM", "timestamp": "2026-04-01T03:00:05Z", "host_id": "HR-PORTAL-01",
     "query_domain": "update.legit-looking.xyz", "query_type": "A"},

    # svchost → explorer.exe 异常（枚举文件）
    {"event_type": "process_create", "pid": 1500, "ppid": 1200, "process_name": "explorer.exe",
     "exe_path": "C:\\Windows\\explorer.exe",
     "command_line": "explorer.exe /e,C:\\",
     "user": "SYSTEM", "timestamp": "2026-04-01T03:10:00Z", "host_id": "HR-PORTAL-01"},

    # svchost → cmd → vssadmin（删除卷影副本）
    {"event_type": "process_create", "pid": 1600, "ppid": 1200, "process_name": "cmd.exe",
     "exe_path": "C:\\Windows\\System32\\cmd.exe",
     "command_line": "cmd.exe /c vssadmin delete shadows /all /quiet",
     "user": "SYSTEM", "timestamp": "2026-04-01T03:15:00Z", "host_id": "HR-PORTAL-01"},
    {"event_type": "process_create", "pid": 1700, "ppid": 1600, "process_name": "vssadmin.exe",
     "exe_path": "C:\\Windows\\System32\\vssadmin.exe",
     "command_line": "vssadmin delete shadows /all /quiet",
     "user": "SYSTEM", "timestamp": "2026-04-01T03:15:01Z", "host_id": "HR-PORTAL-01"},

    # 注册表持久化
    {"event_type": "registry_set", "pid": 1200, "ppid": 800, "process_name": "svchost.exe",
     "exe_path": "C:\\Windows\\System32\\svchost.exe", "command_line": "",
     "user": "SYSTEM", "timestamp": "2026-04-01T03:05:00Z", "host_id": "HR-PORTAL-01",
     "key_path": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
     "value_name": "SystemHealthMonitor",
     "value_data": "C:\\ProgramData\\healthmon.exe"},
]

# ============================================================
# 噪声进程事件（正常工作站行为）
# ============================================================

NOISE_PROCESS_EVENTS = [
    {"event_type": "process_create", "pid": 100, "ppid": 1, "process_name": "explorer.exe",
     "exe_path": "C:\\Windows\\explorer.exe", "command_line": "explorer.exe",
     "user": "CORP\\analyst-lin", "timestamp": "2026-04-01T08:30:00Z", "host_id": "SIEM-SRV-01"},
    {"event_type": "process_create", "pid": 200, "ppid": 100, "process_name": "chrome.exe",
     "exe_path": "C:\\Program Files\\Google\\Chrome\\chrome.exe", "command_line": "chrome.exe",
     "user": "CORP\\analyst-lin", "timestamp": "2026-04-01T08:31:00Z", "host_id": "SIEM-SRV-01"},
    {"event_type": "dns_query", "pid": 200, "ppid": 100, "process_name": "chrome.exe",
     "exe_path": "C:\\Program Files\\Google\\Chrome\\chrome.exe", "command_line": "",
     "user": "CORP\\analyst-lin", "timestamp": "2026-04-01T08:31:05Z", "host_id": "SIEM-SRV-01",
     "query_domain": "www.google.com", "query_type": "A"},
    {"event_type": "process_create", "pid": 300, "ppid": 100, "process_name": "notepad.exe",
     "exe_path": "C:\\Windows\\notepad.exe", "command_line": "notepad.exe report.txt",
     "user": "CORP\\analyst-lin", "timestamp": "2026-04-01T09:00:00Z", "host_id": "SIEM-SRV-01"},
    {"event_type": "network_connect", "pid": 200, "ppid": 100, "process_name": "chrome.exe",
     "exe_path": "C:\\Program Files\\Google\\Chrome\\chrome.exe", "command_line": "",
     "user": "CORP\\analyst-lin", "timestamp": "2026-04-01T08:31:10Z", "host_id": "SIEM-SRV-01",
     "src_ip": "10.1.9.20", "dst_ip": "172.217.14.206", "dst_port": 443, "protocol": "TCP"},
]

# ============================================================
# 输出
# ============================================================

ALL_HOST_EVENTS = {
    "DEV-WS-01": S02_DEV_WS_01_EVENTS,
    "WKST-047": S02_WKST_047_EVENTS,
    "HR-PORTAL-01": S04_HR_PORTAL_EVENTS,
    "SIEM-SRV-01": NOISE_PROCESS_EVENTS,
}


def _write_dataset(output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    for host_id, events in ALL_HOST_EVENTS.items():
        filename = f"process_events_{host_id.lower().replace('-', '_')}.json"
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            json.dump({
                "host_id": host_id,
                "event_count": len(events),
                "events": events,
            }, f, ensure_ascii=False, indent=2)
        total += len(events)
        print(f"  ✅ {host_id}: {len(events)} events -> {output_dir}")

    # 汇总索引
    with open(output_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump({
            "hosts": list(ALL_HOST_EVENTS.keys()),
            "total_events": total,
            "scenarios_covered": ["S-02", "S-04", "noise"],
        }, f, ensure_ascii=False, indent=2)

    return total


def main():
    total = _write_dataset(OUTPUT_DIR)
    _write_dataset(LEGACY_OUTPUT_DIR)
    print(f"\n  Total: {total} process events across {len(ALL_HOST_EVENTS)} hosts")


if __name__ == "__main__":
    main()
