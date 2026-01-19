"""
Canonical error definitions and normalization.

All user-facing errors should map to one of these types.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppError(Exception):
    """
    Base application error.
    """
    code: str
    message: str
    user_message: str


class TimeoutError(AppError):
    def __init__(self):
        super().__init__(
            code="TIMEOUT",
            message="Operation exceeded time limit",
            user_message="The request took too long and was aborted."
        )


class ExternalServiceError(AppError):
    def __init__(self):
        super().__init__(
            code="EXTERNAL_SERVICE_ERROR",
            message="External dependency failed",
            user_message="A required external service is unavailable."
        )


class InvalidInputError(AppError):
    def __init__(self, message: str):
        super().__init__(
            code="INVALID_INPUT",
            message=message,
            user_message=message
        )
