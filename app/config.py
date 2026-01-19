"""
Centralized application configuration.

This module defines explicit operational parameters.
All defaults are chosen to satisfy task constraints.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """
    Immutable runtime configuration.
    """

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    # --- Model ---
    LOCAL_MODEL_NAME: str = "google/flan-t5-small"
    MODEL_TIMEOUT_S: float = 2.5
    MAX_OUTPUT_TOKENS: int = 300

    # --- Streaming ---
    ENABLE_STREAMING: bool = True

    # --- Stability ---
    MAX_REQUESTS_PER_PROCESS: int = 100  # for stress tests


# Single config instance used across the app
CONFIG = AppConfig()
