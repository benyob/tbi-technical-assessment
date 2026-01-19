"""
Retry logic with bounded backoff.

Used for:
- Model loading
- External APIs (future)
"""

import time
from typing import Callable, Type

from app.reliability.errors import AppError


def retry(
    func: Callable,
    retries: int = 2,
    delay_s: float = 0.5,
    allowed_errors: Type[Exception] = AppError,
):
    """
    Retry a function on allowed errors.

    Args:
        func: Callable with no arguments
        retries: Number of retries
        delay_s: Backoff delay
        allowed_errors: Error types to retry on
    """
    last_exc = None

    for _ in range(retries + 1):
        try:
            return func()
        except allowed_errors as exc:
            last_exc = exc
            time.sleep(delay_s)

    raise last_exc
