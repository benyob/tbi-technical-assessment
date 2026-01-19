import pytest
from app.core.document import validate_document, chunk_document
from app.reliability.errors import InvalidInputError


def test_validate_document_ok():
    text = "This is a valid document."
    assert validate_document(text) == text


def test_validate_document_empty():
    with pytest.raises(InvalidInputError):
        validate_document("   ")


def test_validate_document_non_string():
    with pytest.raises(InvalidInputError):
        validate_document(123)


def test_chunk_document_bounds():
    text = "a" * 10_000
    chunks = chunk_document(text)
    assert len(chunks) > 0
