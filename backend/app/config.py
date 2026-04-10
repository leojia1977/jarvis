"""SecuPilot 配置管理"""

from pathlib import Path

try:
    from pydantic_settings import BaseSettings
except ImportError:
    class BaseSettings:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


class Settings(BaseSettings):
    project_root: str = str(Path(__file__).resolve().parents[2])

    # LLM
    llm_api_base: str = "https://api.anthropic.com/v1"
    llm_api_key: str = ""
    llm_model: str = "claude-sonnet-4-20250514"
    llm_temperature: float = 0.2
    llm_timeout_seconds: int = 15
    llm_max_retries: int = 2

    # Redis
    redis_url: str = "redis://localhost:6379"
    session_ttl_hours: int = 24
    max_suspended_tasks: int = 3

    # Risk thresholds
    high_risk_threshold: float = 8.5
    serious_tone_threshold: float = 8.0

    # Expert mode
    expert_mode_failure_threshold: int = 3

    # Mock data
    mock_data_path: str = "./mock_data"
    static_data_mode: str = "local_files"
    static_data_path: str = ""
    static_data_refresh_seconds: int = 300
    asset_source_mode: str = "local_files"
    baseline_source_mode: str = "local_files"
    intel_seed_source_mode: str = "local_files"
    topology_source_mode: str = "local_files"
    runtime_mode: str = "mock"
    business_timezone: str = "Asia/Shanghai"
    siem_vendor: str = "generic_http"
    siem_base_url: str = ""
    siem_auth_token: str = ""
    siem_request_timeout_seconds: float = 5.0
    edr_source_mode: str = "local_files"
    edr_vendor: str = "generic_http"
    edr_base_url: str = ""
    edr_auth_token: str = ""
    edr_request_timeout_seconds: float = 5.0
    case_store_backend: str = "sqlite_local"
    case_store_path: str = "./data/secupilot_case_store.sqlite3"
    case_store_retention_days: int = 90

    # Server
    service_name: str = "secupilot-runtime"
    service_version: str = "3.2.0-s3a"
    server_host: str = "127.0.0.1"
    server_port: int = 8080
    cors_origins: str = "http://localhost:3000"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

    def get_project_root(self) -> Path:
        return Path(self.project_root).resolve()

    def get_static_data_dir(self) -> Path:
        configured = self.static_data_path or self.mock_data_path
        path = Path(configured)
        if not path.is_absolute():
            path = self.get_project_root() / path
        return path.resolve()

    def get_mock_data_dir(self) -> Path:
        # Legacy alias kept for Sprint 4 transition. New work should prefer
        # get_static_data_dir() and the static-data source contract.
        return self.get_static_data_dir()

    def get_case_store_path(self) -> Path:
        path = Path(self.case_store_path)
        if not path.is_absolute():
            path = self.get_project_root() / path
        return path.resolve()


settings = Settings()
