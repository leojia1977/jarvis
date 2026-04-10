from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Any, Optional, Protocol

from app.config import Settings, settings
from app.tools.persistent_case import (
    PersistentCaseRecord,
    persistent_case_record_from_dict,
    persistent_case_record_to_dict,
)


class CaseStoreRuntimeError(RuntimeError):
    def __init__(self, *, reason: str, operator_message: str, detail: str = "") -> None:
        super().__init__(detail or reason)
        self.reason = reason
        self.operator_message = operator_message
        self.detail = detail


class CaseStoreProtocol(Protocol):
    def save_case(self, record: PersistentCaseRecord) -> PersistentCaseRecord:
        ...

    def get_case(self, case_id: str) -> Optional[PersistentCaseRecord]:
        ...

    def get_runtime_stats(self) -> dict[str, Any]:
        ...


def load_current_snapshot_id(runtime_settings: Settings = settings) -> str:
    manifest_path = runtime_settings.get_project_root() / "releases" / "release_manifest.json"
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except OSError:
        return "UNKNOWN-SNAPSHOT"
    except json.JSONDecodeError:
        return "UNKNOWN-SNAPSHOT"

    snapshot_id = payload.get("snapshot", {}).get("id")
    return str(snapshot_id or "UNKNOWN-SNAPSHOT")


class SQLitePersistentCaseStore:
    def __init__(self, runtime_settings: Settings) -> None:
        self.settings = runtime_settings
        self.backend = "sqlite_local"
        self.store_path = runtime_settings.get_case_store_path()
        self.retention_days = int(runtime_settings.case_store_retention_days or 0)
        self._write_lock = threading.Lock()

    def _ensure_parent_dir(self) -> None:
        try:
            self.store_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise CaseStoreRuntimeError(
                reason="case_store_parent_init_failed",
                operator_message=(
                    f"Case store parent directory could not be created at {self.store_path.parent}."
                ),
                detail=str(exc),
            ) from exc

    def _connect(self) -> sqlite3.Connection:
        self._ensure_parent_dir()
        try:
            connection = sqlite3.connect(
                str(self.store_path),
                timeout=5.0,
                isolation_level=None,
                check_same_thread=False,
            )
        except sqlite3.Error as exc:
            raise CaseStoreRuntimeError(
                reason="case_store_connect_failed",
                operator_message=f"SQLite case store could not open {self.store_path}.",
                detail=str(exc),
            ) from exc

        connection.row_factory = sqlite3.Row
        try:
            connection.execute("PRAGMA journal_mode=WAL;")
            connection.execute("PRAGMA synchronous=NORMAL;")
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS cases (
                    case_id TEXT PRIMARY KEY,
                    lifecycle_status TEXT NOT NULL,
                    created_at_utc TEXT NOT NULL,
                    updated_at_utc TEXT NOT NULL,
                    source_snapshot_id TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )
        except sqlite3.Error as exc:
            connection.close()
            raise CaseStoreRuntimeError(
                reason="case_store_schema_init_failed",
                operator_message=f"SQLite case store schema could not be initialized at {self.store_path}.",
                detail=str(exc),
            ) from exc
        return connection

    def save_case(self, record: PersistentCaseRecord) -> PersistentCaseRecord:
        payload = persistent_case_record_to_dict(record)
        payload_json = json.dumps(payload, ensure_ascii=False, sort_keys=True)

        with self._write_lock:
            connection = self._connect()
            try:
                connection.execute("BEGIN IMMEDIATE")
                connection.execute(
                    """
                    INSERT INTO cases (
                        case_id,
                        lifecycle_status,
                        created_at_utc,
                        updated_at_utc,
                        source_snapshot_id,
                        schema_version,
                        payload_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(case_id) DO UPDATE SET
                        lifecycle_status = excluded.lifecycle_status,
                        created_at_utc = excluded.created_at_utc,
                        updated_at_utc = excluded.updated_at_utc,
                        source_snapshot_id = excluded.source_snapshot_id,
                        schema_version = excluded.schema_version,
                        payload_json = excluded.payload_json
                    """,
                    (
                        record.case_id,
                        record.lifecycle_status,
                        record.created_at_utc,
                        record.updated_at_utc,
                        record.source_snapshot_id,
                        record.schema_version,
                        payload_json,
                    ),
                )
                connection.commit()
            except sqlite3.Error as exc:
                connection.rollback()
                raise CaseStoreRuntimeError(
                    reason="case_store_write_failed",
                    operator_message=f"SQLite case store failed while saving case {record.case_id}.",
                    detail=str(exc),
                ) from exc
            finally:
                connection.close()

        return persistent_case_record_from_dict(payload)

    def get_case(self, case_id: str) -> Optional[PersistentCaseRecord]:
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT payload_json FROM cases WHERE case_id = ?",
                (case_id,),
            ).fetchone()
        except sqlite3.Error as exc:
            raise CaseStoreRuntimeError(
                reason="case_store_read_failed",
                operator_message=f"SQLite case store failed while reading case {case_id}.",
                detail=str(exc),
            ) from exc
        finally:
            connection.close()

        if not row:
            return None

        try:
            payload = json.loads(str(row["payload_json"]))
        except json.JSONDecodeError as exc:
            raise CaseStoreRuntimeError(
                reason="case_store_payload_invalid",
                operator_message=f"Stored case payload for {case_id} is not valid JSON.",
                detail=str(exc),
            ) from exc

        return persistent_case_record_from_dict(payload)

    def get_runtime_stats(self) -> dict[str, Any]:
        stored_cases = 0
        connection: Optional[sqlite3.Connection] = None
        if self.store_path.exists():
            try:
                connection = self._connect()
                row = connection.execute("SELECT COUNT(*) AS total FROM cases").fetchone()
                stored_cases = int(row["total"] if row else 0)
            except CaseStoreRuntimeError:
                stored_cases = 0
            finally:
                try:
                    if connection is not None:
                        connection.close()
                except Exception:
                    pass

        return {
            "backend": self.backend,
            "store_path": str(self.store_path),
            "retention_days": self.retention_days,
            "stored_cases": stored_cases,
        }


def build_case_store(runtime_settings: Settings = settings) -> CaseStoreProtocol:
    backend = str(runtime_settings.case_store_backend or "sqlite_local").strip().lower()
    if backend != "sqlite_local":
        raise CaseStoreRuntimeError(
            reason="case_store_backend_not_supported",
            operator_message=(
                f"Case store backend '{runtime_settings.case_store_backend}' is not supported in Sprint 4."
            ),
            detail=f"unsupported_case_store_backend:{runtime_settings.case_store_backend}",
        )
    return SQLitePersistentCaseStore(runtime_settings)
