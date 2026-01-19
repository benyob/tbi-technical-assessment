"""
Structured logging utilities.

Designed for:
- Auditability
- Request correlation
- Post-mortem analysis
"""

import logging
import sys


def setup_logging():
    """
    Configure root logger for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | "
            "request_id=%(request_id)s | %(message)s"
        ),
        stream=sys.stdout,
    )


class RequestLoggerAdapter(logging.LoggerAdapter):
    """
    Inject request_id into all log messages.
    """

    def process(self, msg, kwargs):
        return msg, {
            "extra": {
                "request_id": self.extra.get("request_id", "unknown")
            }
        }
