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
    runtime_mode: str = "mock"
    business_timezone: str = "Asia/Shanghai"

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

    def get_mock_data_dir(self) -> Path:
        path = Path(self.mock_data_path)
        if not path.is_absolute():
            path = self.get_project_root() / path
        return path.resolve()


settings = Settings()
