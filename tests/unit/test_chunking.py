from app.core.document import chunk_document
from app.core.budgets import CHUNK_SIZE_CHARS, MAX_CHUNKS


def test_chunk_size_never_exceeds_limit():
    text = "a" * (CHUNK_SIZE_CHARS * 2)
    chunks = chunk_document(text)

    for chunk in chunks:
        assert len(chunk) <= CHUNK_SIZE_CHARS


def test_chunk_count_is_bounded():
    text = "b" * (CHUNK_SIZE_CHARS * (MAX_CHUNKS + 5))
    chunks = chunk_document(text)

    assert len(chunks) == MAX_CHUNKS


def test_chunking_is_deterministic():
    text = "deterministic text " * 100
    chunks_1 = chunk_document(text)
    chunks_2 = chunk_document(text)

    assert chunks_1 == chunks_2
