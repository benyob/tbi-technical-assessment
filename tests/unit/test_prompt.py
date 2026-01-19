from app.core.prompt import build_summary_prompt


def test_prompt_contains_query_and_context():
    chunks = ["Context chunk one.", "Context chunk two."]
    query = "What is dropout?"
    prompt = build_summary_prompt(chunks, query)

    assert query in prompt
    for chunk in chunks:
        assert chunk in prompt
