"""
Server-Sent Events utilities.
"""

from typing import Iterator
import json


def sse_event(data: dict) -> str:
    """
    Format a Server-Sent Event message.
    """
    return f"data: {json.dumps(data)}\n\n"


def stream_text_chunks(chunks: Iterator[str]) -> Iterator[str]:
    """
    Yield SSE-formatted text chunks.
    """
    for chunk in chunks:
        yield sse_event({
            "event": "token",
            "content": chunk
        })

    yield sse_event({
        "event": "complete"
    })
