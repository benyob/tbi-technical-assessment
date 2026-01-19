"""
Prompt construction with explicit constraints.
"""

from typing import List


def build_summary_prompt(
    chunks: List[str],
    query: str,
) -> str:
    """
    Construct a bounded summarization prompt.
    """

    context = "\n\n".join(chunks)

    prompt = (
        "You are an assistant helping analyze a technical document.\n\n"
        "Task:\n"
        f"Answer the following question using only the provided context.\n\n"
        f"Question:\n{query}\n\n"
        "Context:\n"
        f"{context}\n\n"
        "Provide a concise, factual summary."
    )

    return prompt
