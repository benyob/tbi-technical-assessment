from app.core.prompt import build_summary_prompt
from app.core.budgets import MAX_INPUT_TOKENS_ESTIMATE


def test_prompt_includes_only_given_chunks():
    chunks = ["chunk one", "chunk two"]
    query = "test query"

    prompt = build_summary_prompt(chunks, query)

    assert "chunk one" in prompt
    assert "chunk two" in prompt
    assert "test query" in prompt


def test_prompt_size_is_reasonable():
    chunks = ["x" * 200] * 5
    query = "y" * 50

    prompt = build_summary_prompt(chunks, query)

    # Character-level proxy for token budget
    assert len(prompt) < MAX_INPUT_TOKENS_ESTIMATE * 4
