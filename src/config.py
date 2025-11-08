"""Configuration helpers for the MCP story evaluation server."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _get_float(name: str, default: float) -> float:
    """Fetch a floating point value from the environment."""

    raw_value = os.getenv(name)
    if raw_value is None:
        return float(default)
    try:
        return float(raw_value)
    except ValueError as exc:  # pragma: no cover - defensive guard
        raise ValueError(f"Environment variable {name} must be a float.") from exc


def _get_int(name: str, default: int) -> int:
    """Fetch an integer value from the environment."""

    raw_value = os.getenv(name)
    if raw_value is None:
        return int(default)
    try:
        return int(raw_value)
    except ValueError as exc:  # pragma: no cover - defensive guard
        raise ValueError(f"Environment variable {name} must be an integer.") from exc


@dataclass(frozen=True)
class WolverineSettings:
    """Runtime configuration for the Wolverine OpenAI-compatible endpoint."""

    base_url: str
    api_key: str
    model: str
    temperature: float
    top_p: float
    max_new_tokens: int
    request_timeout: float

    @classmethod
    def from_env(cls) -> "WolverineSettings":
        """Load settings from process environment variables."""

        return cls(
            base_url=os.getenv("WOLVERINE_BASE_URL", "http://127.0.0.1:11434/v1"),
            api_key=os.getenv("WOLVERINE_API_KEY", "not-required"),
            model=os.getenv("WOLVERINE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2"),
            temperature=_get_float("WOLVERINE_TEMPERATURE", 0.7),
            top_p=_get_float("WOLVERINE_TOP_P", 0.95),
            max_new_tokens=_get_int("WOLVERINE_MAX_NEW_TOKENS", 256),
            request_timeout=_get_float("WOLVERINE_REQUEST_TIMEOUT", 120.0),
        )


# Single shared settings instance used across the application.
WOLVERINE_SETTINGS = WolverineSettings.from_env()

