"""
Lightweight relevance selection.
This is intentionally simple and explainable.
"""

from typing import List


def select_relevant_chunks(
    chunks: List[str],
    query: str,
    top_k: int = 5,
) -> List[str]:
    query_terms = set(query.lower().split())

    scored = []
    for chunk in chunks:
        score = sum(
            1 for word in chunk.lower().split()
            if word in query_terms
        )
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]
