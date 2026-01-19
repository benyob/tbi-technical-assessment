"""
Timeout enforcement utilities.
"""

import signal
from contextlib import contextmanager

from app.reliability.errors import TimeoutError


@contextmanager
def time_limit(seconds: int):
    """
    Enforce a hard wall-clock timeout.

    Raises:
        TimeoutError
    """

    def _handle_timeout(signum, frame):
        raise TimeoutError()

    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)
