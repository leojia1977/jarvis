"""
SecuPilot EDR Adapter Contract

Sprint 4 B-1 目标：
- 冻结生产侧 EDR 进程事件接入契约
- 让 B-2 只围绕 canonical process-event schema 做实现
- 保持 T3 仍然消费冻结后的 runtime payload，而不是 vendor 原始字段
"""

from __future__ import annotations

import asyncio
import json
import time
import urllib.error
import urllib.request
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Optional, Protocol

from app.config import settings
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

_EXTRA_EXCLUDED_KEYS = {
    "event_type",
    "event",
    "type",
    "host_id",
    "host",
    "asset_id",
    "device",
    "endpoint",
    "timestamp",
    "@timestamp",
    "event_time",
    "pid",
    "ppid",
    "process_name",
    "exe_path",
    "command_line",
    "user",
    "src_ip",
    "dst_ip",
    "dst_port",
    "protocol",
    "query_domain",
    "query_type",
    "key_path",
    "value_name",
    "value_data",
    "file_path",
    "file_hash_sha256",
    # Exclude common ECS-style vendor containers so raw nested trees do not
    # quietly ride into the T3 runtime payload through extra{}.
    "process",
    "source",
    "destination",
    "dns",
    "registry",
    "file",
    "network",
}


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


class EDRTransportProtocol(Protocol):
    async def post_json(
        self,
        endpoint: str,
        payload: dict[str, Any],
        *,
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        ...


def _parse_iso_utc(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def _path_get(payload: Any, path: str) -> Any:
    current = payload
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current.get(part)
    return current


def _first_present(payload: Any, *paths: str) -> Any:
    for path in paths:
        value = _path_get(payload, path)
        if value is not None:
            return value
    return None


def _read_json_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _normalize_process_event_type(value: Any) -> str:
    token = str(value or "").strip().lower()
    if token in {
        "process_create",
        "network_connect",
        "dns_query",
        "registry_set",
        "file_write",
    }:
        return token
    return "process_create"


def _normalize_runtime_host_key(value: str) -> str:
    return str(value or "").strip().upper()


def _process_event_file_stem(value: str) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(".", "_")


def _filter_events_by_time(events: list[CanonicalProcessEvent], time_range: TimeRangeSpec) -> list[CanonicalProcessEvent]:
    filtered: list[CanonicalProcessEvent] = []
    for event in events:
        parsed = _parse_iso_utc(event.timestamp)
        if time_range.contains(parsed):
            filtered.append(event)
    return filtered


def _compat_local_events(events: list[CanonicalProcessEvent]) -> list[CanonicalProcessEvent]:
    """
    Preserve the historical mock/replay semantics for local process-event data.

    Local-file and in-memory process-event fixtures are static investigation
    replays. They should remain available to T3 even when their timestamps fall
    outside a relative request window, otherwise Sprint 2/3 mock behavior would
    regress as the calendar moves forward.
    """
    return list(events)


def _normalize_process_event(raw: dict[str, Any], *, default_host_id: str) -> CanonicalProcessEvent:
    return CanonicalProcessEvent(
        event_type=_normalize_process_event_type(
            _first_present(raw, "event_type", "event.type", "type")
        ),
        host_id=str(
            _first_present(raw, "host_id", "host.id", "asset_id", "device.id", "endpoint.id")
            or default_host_id
        ),
        timestamp=str(
            _first_present(raw, "timestamp", "@timestamp", "event.created", "event_time")
            or ""
        ),
        pid=int(_first_present(raw, "pid", "process.pid") or 0),
        ppid=int(_first_present(raw, "ppid", "process.parent.pid") or 0),
        process_name=str(
            _first_present(raw, "process_name", "process.name", "event.process_name") or ""
        ),
        exe_path=str(
            _first_present(raw, "exe_path", "process.executable", "process.path") or ""
        ),
        command_line=str(
            _first_present(raw, "command_line", "process.command_line", "process.cmdline") or ""
        ),
        user=str(_first_present(raw, "user.name", "actor.user", "user") or ""),
        src_ip=str(_first_present(raw, "src_ip", "source.ip", "network.src_ip") or ""),
        dst_ip=str(_first_present(raw, "dst_ip", "destination.ip", "network.dst_ip") or ""),
        dst_port=int(_first_present(raw, "dst_port", "destination.port", "network.dst_port") or 0),
        protocol=str(_first_present(raw, "protocol", "network.transport", "network.protocol") or ""),
        query_domain=str(_first_present(raw, "query_domain", "dns.question.name", "dns.query") or ""),
        query_type=str(_first_present(raw, "query_type", "dns.question.type") or ""),
        key_path=str(_first_present(raw, "key_path", "registry.path") or ""),
        value_name=str(_first_present(raw, "value_name", "registry.value_name") or ""),
        value_data=str(_first_present(raw, "value_data", "registry.value_data") or ""),
        file_path=str(_first_present(raw, "file_path", "file.path") or ""),
        file_hash_sha256=str(
            _first_present(raw, "file_hash_sha256", "file.hash.sha256", "hash.sha256") or ""
        ),
        extra={
            key: value
            for key, value in raw.items()
            if key not in _EXTRA_EXCLUDED_KEYS
        },
    )


class UrllibEDRTransport:
    async def post_json(
        self,
        endpoint: str,
        payload: dict[str, Any],
        *,
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        return await asyncio.to_thread(
            self._post_json_sync,
            endpoint,
            payload,
            headers,
            timeout_seconds,
        )

    @staticmethod
    def _post_json_sync(
        endpoint: str,
        payload: dict[str, Any],
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json", **headers},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
        return json.loads(body or "{}")


class InMemoryEDRAdapter:
    def __init__(
        self,
        process_events_by_host: dict[str, list[dict[str, Any]]],
        *,
        source_mode: EDRSourceMode = "local_files",
        source_name: str = "in_memory_process_events",
        vendor: str = "mock",
    ) -> None:
        self._source_mode = source_mode
        self._source_name = source_name
        self._vendor = vendor
        self._events_by_host = {
            _normalize_runtime_host_key(host_id): [deepcopy(event) for event in events]
            for host_id, events in (process_events_by_host or {}).items()
        }

    def _candidate_keys(self, host_identity: HostIdentityRecord) -> list[str]:
        values = [
            host_identity.canonical_asset_id,
            host_identity.hostname,
            host_identity.fqdn,
            *host_identity.aliases,
        ]
        ordered: list[str] = []
        seen: set[str] = set()
        for value in values:
            key = _normalize_runtime_host_key(value)
            if not key or key in seen:
                continue
            seen.add(key)
            ordered.append(key)
        return ordered

    async def query_process_events(
        self,
        host_identity: HostIdentityRecord,
        time_range: TimeRangeSpec,
    ) -> AdapterResult[ProcessEventBatch]:
        started = time.monotonic()
        raw_events: list[dict[str, Any]] = []
        for key in self._candidate_keys(host_identity):
            raw_events = self._events_by_host.get(key, [])
            if raw_events:
                break

        events = _compat_local_events(
            [
                _normalize_process_event(
                    event,
                    default_host_id=host_identity.canonical_asset_id,
                )
                for event in raw_events
            ]
        )
        batch = ProcessEventBatch(
            metadata=EDRSourceMetadata(
                source_name=self._source_name,
                source_mode=self._source_mode,
                vendor=self._vendor,
                ownership="T3 process-event ingestion",
                record_count=len(events),
            ),
            host_identity=host_identity,
            time_range=time_range,
            events=events,
        )
        return AdapterResult.ok(
            batch,
            latency_ms=(time.monotonic() - started) * 1000,
            metadata={"candidate_keys": self._candidate_keys(host_identity)},
        )

    def get_runtime_stats(self) -> dict[str, int]:
        return {
            "process_event_hosts": len(self._events_by_host),
            "process_event_total": sum(len(events) for events in self._events_by_host.values()),
        }


class LocalFileEDRAdapter:
    def __init__(
        self,
        root: Path,
        *,
        source_mode: EDRSourceMode = "local_files",
        vendor: str = "local_files",
    ) -> None:
        self.root = Path(root).resolve()
        self.source_mode = source_mode
        self.vendor = vendor
        self.index_path = self.root / "index.json"
        self._index = self._load_index()

    def _load_index(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return {"hosts": [], "total_events": 0}
        try:
            with self.index_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, json.JSONDecodeError):
            return {"hosts": [], "total_events": 0}

    def _candidate_files(self, host_identity: HostIdentityRecord) -> list[Path]:
        candidates = [
            host_identity.canonical_asset_id,
            host_identity.hostname,
            host_identity.fqdn.split(".")[0] if host_identity.fqdn else "",
            *host_identity.aliases,
        ]
        ordered: list[Path] = []
        seen: set[str] = set()
        for candidate in candidates:
            stem = _process_event_file_stem(candidate)
            if not stem or stem in seen:
                continue
            seen.add(stem)
            ordered.append(self.root / f"process_events_{stem}.json")
        return ordered

    async def query_process_events(
        self,
        host_identity: HostIdentityRecord,
        time_range: TimeRangeSpec,
    ) -> AdapterResult[ProcessEventBatch]:
        started = time.monotonic()
        selected_path: Optional[Path] = None
        payload: dict[str, Any] = {}

        for candidate in self._candidate_files(host_identity):
            if candidate.exists():
                selected_path = candidate
                break

        if selected_path:
            try:
                payload = await asyncio.to_thread(_read_json_file, selected_path)
            except json.JSONDecodeError as exc:
                return AdapterResult.unavailable(
                    ProcessEventBatch(
                        metadata=EDRSourceMetadata(
                            source_name=str(selected_path.relative_to(self.root)).replace("\\", "/"),
                            source_mode=self.source_mode,
                            vendor=self.vendor,
                            ownership="T3 process-event ingestion",
                            record_count=0,
                        ),
                        host_identity=host_identity,
                        time_range=time_range,
                        events=[],
                    ),
                    latency_ms=(time.monotonic() - started) * 1000,
                    gap_reason=f"edr_source_invalid_json:{exc}",
                    metadata={"path": str(selected_path)},
                )
            except OSError as exc:
                return AdapterResult.unavailable(
                    ProcessEventBatch(
                        metadata=EDRSourceMetadata(
                            source_name=str(selected_path.relative_to(self.root)).replace("\\", "/"),
                            source_mode=self.source_mode,
                            vendor=self.vendor,
                            ownership="T3 process-event ingestion",
                            record_count=0,
                        ),
                        host_identity=host_identity,
                        time_range=time_range,
                        events=[],
                    ),
                    latency_ms=(time.monotonic() - started) * 1000,
                    gap_reason=f"edr_source_read_failed:{exc}",
                    metadata={"path": str(selected_path)},
                )

        raw_events = payload.get("events", []) if payload else []
        events = _compat_local_events(
            [
                _normalize_process_event(
                    event,
                    default_host_id=host_identity.canonical_asset_id,
                )
                for event in raw_events
            ]
        )
        source_name = (
            str(selected_path.relative_to(self.root)).replace("\\", "/")
            if selected_path
            else "process_events:missing"
        )
        batch = ProcessEventBatch(
            metadata=EDRSourceMetadata(
                source_name=source_name,
                source_mode=self.source_mode,
                vendor=self.vendor,
                ownership="T3 process-event ingestion",
                collected_at_utc=payload.get("collected_at_utc"),
                record_count=len(events),
            ),
            host_identity=host_identity,
            time_range=time_range,
            events=events,
        )
        return AdapterResult.ok(
            batch,
            latency_ms=(time.monotonic() - started) * 1000,
            metadata={"path": str(selected_path) if selected_path else "", "candidate_files": [str(path) for path in self._candidate_files(host_identity)]},
        )

    def get_runtime_stats(self) -> dict[str, int]:
        return {
            "process_event_hosts": len(self._index.get("hosts", []) or []),
            "process_event_total": int(self._index.get("total_events", 0) or 0),
        }


class ProductionEDRAdapter:
    def __init__(
        self,
        runtime_settings=settings,
        *,
        transport: Optional[EDRTransportProtocol] = None,
    ) -> None:
        self.settings = runtime_settings
        self.transport = transport or UrllibEDRTransport()
        self.base_url = (getattr(runtime_settings, "edr_base_url", "") or "").rstrip("/")
        self.auth_token = getattr(runtime_settings, "edr_auth_token", "") or ""
        self.vendor = getattr(runtime_settings, "edr_vendor", "generic_http") or "generic_http"
        self.source_mode = str(getattr(runtime_settings, "edr_source_mode", "api") or "api")
        self.timeout_seconds = float(getattr(runtime_settings, "edr_request_timeout_seconds", 5.0))
        self._endpoint = "/api/v1/process-events/query"

    def is_configured(self) -> bool:
        return bool(self.base_url and self.auth_token)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "X-SecuPilot-EDR-Vendor": self.vendor,
        }

    async def query_process_events(
        self,
        host_identity: HostIdentityRecord,
        time_range: TimeRangeSpec,
    ) -> AdapterResult[ProcessEventBatch]:
        if not self.is_configured():
            return AdapterResult.unavailable(
                ProcessEventBatch(
                    metadata=EDRSourceMetadata(
                        source_name="production_edr",
                        source_mode=self.source_mode,  # type: ignore[arg-type]
                        vendor=self.vendor,
                        ownership="T3 production process-event ingestion",
                        record_count=0,
                    ),
                    host_identity=host_identity,
                    time_range=time_range,
                    events=[],
                ),
                gap_reason="production_edr_not_configured",
            )

        payload = {
            "canonical_asset_id": host_identity.canonical_asset_id,
            "hostname": host_identity.hostname,
            "fqdn": host_identity.fqdn,
            "ip_addresses": list(host_identity.ip_addresses),
            "aliases": list(host_identity.aliases),
            "time_range": {
                "start_utc": time_range.start_utc.isoformat(),
                "end_utc": time_range.end_utc.isoformat(),
                "tz_label": time_range.tz_label,
            },
        }

        started = time.monotonic()
        try:
            raw = await self.transport.post_json(
                f"{self.base_url}{self._endpoint}",
                payload,
                headers=self._headers(),
                timeout_seconds=self.timeout_seconds,
            )
        except TimeoutError:
            return AdapterResult.timeout(
                ProcessEventBatch(
                    metadata=EDRSourceMetadata(
                        source_name="production_edr",
                        source_mode=self.source_mode,  # type: ignore[arg-type]
                        vendor=self.vendor,
                        ownership="T3 production process-event ingestion",
                        record_count=0,
                    ),
                    host_identity=host_identity,
                    time_range=time_range,
                    events=[],
                ),
                gap_reason="production_edr_timeout",
            )
        except (json.JSONDecodeError, ValueError) as exc:
            return AdapterResult.unavailable(
                ProcessEventBatch(
                    metadata=EDRSourceMetadata(
                        source_name="production_edr",
                        source_mode=self.source_mode,  # type: ignore[arg-type]
                        vendor=self.vendor,
                        ownership="T3 production process-event ingestion",
                        record_count=0,
                    ),
                    host_identity=host_identity,
                    time_range=time_range,
                    events=[],
                ),
                gap_reason=f"production_edr_bad_response:{exc}",
            )
        except urllib.error.URLError as exc:
            return AdapterResult.unavailable(
                ProcessEventBatch(
                    metadata=EDRSourceMetadata(
                        source_name="production_edr",
                        source_mode=self.source_mode,  # type: ignore[arg-type]
                        vendor=self.vendor,
                        ownership="T3 production process-event ingestion",
                        record_count=0,
                    ),
                    host_identity=host_identity,
                    time_range=time_range,
                    events=[],
                ),
                gap_reason=f"production_edr_unavailable:{exc.reason}",
            )

        status = str(raw.get("status", "ok")).lower()
        if status not in {"ok", "partial", "timeout", "unavailable"}:
            status = "unavailable"
        rows = raw.get("events")
        if rows is None:
            rows = _path_get(raw, "data.events")
        if rows is None:
            rows = raw.get("data", [])
        events = _filter_events_by_time(
            [_normalize_process_event(row, default_host_id=host_identity.canonical_asset_id) for row in list(rows or [])],
            time_range,
        )
        batch = ProcessEventBatch(
            metadata=EDRSourceMetadata(
                source_name=str(raw.get("source_name") or "production_edr"),
                source_mode=self.source_mode,  # type: ignore[arg-type]
                vendor=self.vendor,
                ownership="T3 production process-event ingestion",
                collected_at_utc=raw.get("collected_at_utc"),
                record_count=len(events),
            ),
            host_identity=host_identity,
            time_range=time_range,
            events=events,
        )
        latency_ms = (time.monotonic() - started) * 1000
        gap_reason = raw.get("gap_reason")
        if status == "partial":
            return AdapterResult.partial(batch, latency_ms=latency_ms, gap_reason=gap_reason or "production_edr_partial")
        if status == "timeout":
            return AdapterResult.timeout(batch, latency_ms=latency_ms, gap_reason=gap_reason or "production_edr_timeout")
        if status == "unavailable":
            return AdapterResult.unavailable(batch, latency_ms=latency_ms, gap_reason=gap_reason or "production_edr_unavailable")
        return AdapterResult.ok(batch, latency_ms=latency_ms, metadata=raw.get("metadata") or {})

    def get_runtime_stats(self) -> dict[str, int]:
        return {
            "process_event_hosts": 0,
            "process_event_total": 0,
        }


def build_edr_adapter(
    runtime_settings=settings,
    *,
    process_events_cache: Optional[dict[str, list[dict[str, Any]]]] = None,
) -> EDRAdapterProtocol:
    if process_events_cache is not None:
        return InMemoryEDRAdapter(process_events_cache)

    mode = str(getattr(runtime_settings, "edr_source_mode", "local_files") or "local_files").strip().lower()
    if mode in {"local_files", "bundle"}:
        return LocalFileEDRAdapter(
            runtime_settings.get_static_data_dir() / "process_events",
            source_mode=mode,  # type: ignore[arg-type]
            vendor="local_files",
        )
    return ProductionEDRAdapter(runtime_settings)


def process_event_record_to_runtime_payload(
    event: CanonicalProcessEvent,
    *,
    default_host_id: str = "",
) -> dict[str, Any]:
    """
    Convert one canonical process-event record into the frozen T3 runtime payload.

    This keeps T3 unchanged in S4-B-1/S4-B-2 while the adapter layer absorbs
    vendor- and transport-specific differences. If present, extra{} may be
    forwarded for audit/debug continuity, but T3 must never rely on it for
    analysis and it must not leak into T3 output or case contracts.
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
