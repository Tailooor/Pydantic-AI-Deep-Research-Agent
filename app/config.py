from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"


def load_env_file(env_file: Path = ENV_FILE) -> None:
    """Load a tiny .env file without adding another dependency."""
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


@dataclass(slots=True)
class Settings:
    openrouter_api_key: str
    openrouter_model: str = "openrouter/free"
    app_host: str = "127.0.0.1"
    app_port: int = 7860
    app_title: str = "Deep Research Agent"
    discovery_result_count: int = 5
    angle_result_count: int = 4


def get_settings() -> Settings:
    load_env_file()

    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is missing. Add it to the .env file before starting the app."
        )

    model = os.getenv("OPENROUTER_MODEL", "openrouter/free").strip() or "openrouter/free"
    host = os.getenv("APP_HOST", "127.0.0.1").strip() or "127.0.0.1"
    port = int(os.getenv("APP_PORT", "7860"))
    title = os.getenv("APP_TITLE", "Deep Research Agent").strip() or "Deep Research Agent"
    discovery_result_count = int(os.getenv("DISCOVERY_RESULT_COUNT", "5"))
    angle_result_count = int(os.getenv("ANGLE_RESULT_COUNT", "4"))

    return Settings(
        openrouter_api_key=api_key,
        openrouter_model=model,
        app_host=host,
        app_port=port,
        app_title=title,
        discovery_result_count=discovery_result_count,
        angle_result_count=angle_result_count,
    )
