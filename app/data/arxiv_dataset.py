"""
Utilities for loading samples from the arXiv summarization dataset.

This module is used for tests and examples, not production inference.
"""

from datasets import load_dataset


def load_arxiv_sample(split: str = "test", index: int = 0) -> dict:
    """
    Load a single arXiv paper sample.

    Returns:
        dict with keys:
        - article: full document text
        - abstract: reference summary
    """
    dataset = load_dataset("ccdv/arxiv-summarization", split=split)
    sample = dataset[index]

    return {
        "article": sample["article"],
        "abstract": sample["abstract"],
    }
