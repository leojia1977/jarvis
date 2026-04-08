from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

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

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._write_json(200, SERVICE.health())
            return
        if self.path == "/ready":
            readiness = SERVICE.readiness()
            self._write_json(200 if readiness["ready"] else 503, readiness)
            return
        self._write_json(404, {"status": "error", "error": "not_found", "path": self.path})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/v1/investigate":
            self._write_json(404, {"status": "error", "error": "not_found", "path": self.path})
            return
        try:
            payload = self._read_json()
        except Exception as exc:
            self._write_json(400, {"status": "error", "error": "invalid_json", "detail": str(exc)})
            return

        status_code, response = SERVICE.investigate_sync(payload)
        self._write_json(status_code, response)

    def log_message(self, format: str, *args: Any) -> None:
        return


def run_server(host: str | None = None, port: int | None = None) -> int:
    listen_host = host or settings.server_host
    listen_port = port or settings.server_port
    server = ThreadingHTTPServer((listen_host, listen_port), SecuPilotHandler)
    print(f"[SecuPilot] Runtime listening on http://{listen_host}:{listen_port}")
    print("[SecuPilot] Endpoints: GET /health, GET /ready, POST /api/v1/investigate")
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
