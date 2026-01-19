"""
Document ingestion and preprocessing.
"""

from typing import List

from app.core.budgets import (
    MAX_DOCUMENT_CHARS,
    CHUNK_SIZE_CHARS,
    MAX_CHUNKS,
)
from app.reliability.errors import InvalidInputError


def validate_document(text: str) -> str:
    """
    Validate incoming document text.
    """
    if not isinstance(text, str):
        raise InvalidInputError("Document must be a UTF-8 string.")

    if not text.strip():
        raise InvalidInputError("Document is empty.")

    if len(text) > MAX_DOCUMENT_CHARS:
        raise InvalidInputError(
            f"Document exceeds {MAX_DOCUMENT_CHARS} character limit."
        )

    return text


def chunk_document(text: str) -> List[str]:
    """
    Deterministically split text into bounded chunks.
    """
    chunks = [
        text[i : i + CHUNK_SIZE_CHARS]
        for i in range(0, len(text), CHUNK_SIZE_CHARS)
    ]

    return chunks[:MAX_CHUNKS]
