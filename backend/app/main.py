from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import unquote

from app.config import settings
from app.runtime_service import SecuPilotRuntimeService


SERVICE = SecuPilotRuntimeService()


class SecuPilotHandler(BaseHTTPRequestHandler):
    server_version = "SecuPilotRuntime/3.2"

    def _write_json(self, status_code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def _internal_error(self, exc: Exception) -> None:
        self._write_json(500, {"status": "error", "error": "internal_error", "detail": str(exc)})

    def _parse_action_request_route(self) -> tuple[str, str, str] | None:
        prefix = "/api/v1/cases/"
        if not self.path.startswith(prefix) or "/action-requests/" not in self.path:
            return None

        suffix = self.path[len(prefix) :]
        case_part, remainder = suffix.split("/action-requests/", 1)
        if "/" not in remainder:
            return None
        action_request_part, operation = remainder.rsplit("/", 1)
        return unquote(case_part).strip(), unquote(action_request_part).strip(), operation.strip()

    def do_GET(self) -> None:  # noqa: N802
        try:
            if self.path == "/health":
                self._write_json(200, SERVICE.health())
                return
            if self.path == "/ready":
                readiness = SERVICE.readiness()
                self._write_json(200 if readiness["ready"] else 503, readiness)
                return
            if self.path.startswith("/api/v1/cases/"):
                case_id = unquote(self.path.split("/api/v1/cases/", 1)[1]).strip()
                status_code, payload = SERVICE.get_case_sync(case_id)
                self._write_json(status_code, payload)
                return
            self._write_json(404, {"status": "error", "error": "not_found", "path": self.path})
        except Exception as exc:
            self._internal_error(exc)

    def do_POST(self) -> None:  # noqa: N802
        try:
            payload = self._read_json()
        except Exception as exc:
            self._write_json(400, {"status": "error", "error": "invalid_json", "detail": str(exc)})
            return

        try:
            if self.path == "/api/v1/cases":
                status_code, response = SERVICE.create_case_sync(payload)
                self._write_json(status_code, response)
                return
            if self.path == "/api/v1/pilot-smoke":
                status_code, response = SERVICE.pilot_smoke_sync(payload)
                self._write_json(status_code, response)
                return
            if self.path == "/api/v1/investigate":
                status_code, response = SERVICE.investigate_sync(payload)
                self._write_json(status_code, response)
                return
            if self.path.startswith("/api/v1/cases/") and self.path.endswith("/action-requests"):
                case_id = unquote(
                    self.path.split("/api/v1/cases/", 1)[1].rsplit("/action-requests", 1)[0]
                ).strip()
                status_code, response = SERVICE.create_action_request_sync(case_id, payload)
                self._write_json(status_code, response)
                return

            action_request_route = self._parse_action_request_route()
            if action_request_route:
                case_id, action_request_id, operation = action_request_route
                if operation == "submit":
                    status_code, response = SERVICE.submit_action_request_sync(case_id, action_request_id, payload)
                elif operation == "approve":
                    status_code, response = SERVICE.approve_action_request_sync(case_id, action_request_id, payload)
                elif operation == "reject":
                    status_code, response = SERVICE.reject_action_request_sync(case_id, action_request_id, payload)
                elif operation == "cancel":
                    status_code, response = SERVICE.cancel_action_request_sync(case_id, action_request_id, payload)
                else:
                    self._write_json(404, {"status": "error", "error": "not_found", "path": self.path})
                    return
                self._write_json(status_code, response)
                return

            self._write_json(404, {"status": "error", "error": "not_found", "path": self.path})
        except Exception as exc:
            self._internal_error(exc)

    def log_message(self, format: str, *args: Any) -> None:
        return


def run_server(host: str | None = None, port: int | None = None) -> int:
    listen_host = host or settings.server_host
    listen_port = port or settings.server_port
    server = ThreadingHTTPServer((listen_host, listen_port), SecuPilotHandler)
    print(f"[SecuPilot] Runtime listening on http://{listen_host}:{listen_port}")
    print(
        "[SecuPilot] Endpoints: GET /health, GET /ready, "
        "POST /api/v1/investigate, POST /api/v1/pilot-smoke, "
        "POST /api/v1/cases, GET /api/v1/cases/{case_id}, "
        "POST /api/v1/cases/{case_id}/action-requests, "
        "POST /api/v1/cases/{case_id}/action-requests/{action_request_id}/{submit|approve|reject|cancel}"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def main() -> int:
    return run_server()


if __name__ == "__main__":
    raise SystemExit(main())
