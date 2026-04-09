"""
SecuPilot EDR Adapter Contract

Sprint 4 B-1 目标：
- 冻结生产侧 EDR 进程事件接入契约
- 让 B-2 只围绕 canonical process-event schema 做实现
- 保持 T3 仍然消费冻结后的 runtime payload，而不是 vendor 原始字段
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol

from app.tools.siem_adapter import AdapterResult, TimeRangeSpec
from app.tools.static_data_sources import HostIdentityRecord


EDRSourceMode = Literal["local_files", "api", "replay", "bundle", "hybrid"]
CanonicalProcessEventType = Literal[
    "process_create",
    "network_connect",
    "dns_query",
    "registry_set",
    "file_write",
]


@dataclass(frozen=True)
class EDRSourceMetadata:
    source_name: str
    source_mode: EDRSourceMode
    vendor: str
    ownership: str
    collected_at_utc: str | None = None
    record_count: int = 0


@dataclass(frozen=True)
class CanonicalProcessEvent:
    event_type: CanonicalProcessEventType
    host_id: str
    timestamp: str
    pid: int
    ppid: int = 0
    process_name: str = ""
    exe_path: str = ""
    command_line: str = ""
    user: str = ""
    src_ip: str = ""
    dst_ip: str = ""
    dst_port: int = 0
    protocol: str = ""
    query_domain: str = ""
    query_type: str = ""
    key_path: str = ""
    value_name: str = ""
    value_data: str = ""
    file_path: str = ""
    file_hash_sha256: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProcessEventBatch:
    metadata: EDRSourceMetadata
    host_identity: HostIdentityRecord
    time_range: TimeRangeSpec
    events: list[CanonicalProcessEvent]


class EDRAdapterProtocol(Protocol):
    async def query_process_events(
        self,
        host_identity: HostIdentityRecord,
        time_range: TimeRangeSpec,
    ) -> AdapterResult[ProcessEventBatch]:
        ...

    def get_runtime_stats(self) -> dict[str, int]:
        ...


def process_event_record_to_runtime_payload(
    event: CanonicalProcessEvent,
    *,
    default_host_id: str = "",
) -> dict[str, Any]:
    """
    Convert one canonical process-event record into the frozen T3 runtime payload.

    This keeps T3 unchanged in S4-B-1/S4-B-2 while the adapter layer absorbs
    vendor- and transport-specific differences.
    """

    payload: dict[str, Any] = {
        "event_type": event.event_type,
        "host_id": event.host_id or default_host_id,
        "timestamp": event.timestamp,
        "pid": event.pid,
        "ppid": event.ppid,
        "process_name": event.process_name,
        "exe_path": event.exe_path,
        "command_line": event.command_line,
        "user": event.user,
    }

    optional_fields = {
        "src_ip": event.src_ip,
        "dst_ip": event.dst_ip,
        "dst_port": event.dst_port,
        "protocol": event.protocol,
        "query_domain": event.query_domain,
        "query_type": event.query_type,
        "key_path": event.key_path,
        "value_name": event.value_name,
        "value_data": event.value_data,
        "file_path": event.file_path,
        "file_hash_sha256": event.file_hash_sha256,
    }
    for key, value in optional_fields.items():
        if value not in ("", 0, None):
            payload[key] = value

    if event.extra:
        payload["extra"] = deepcopy(event.extra)
    return payload


def process_event_batch_to_runtime_payload(batch: ProcessEventBatch) -> list[dict[str, Any]]:
    default_host_id = batch.host_identity.canonical_asset_id
    return [
        process_event_record_to_runtime_payload(event, default_host_id=default_host_id)
        for event in batch.events
    ]
