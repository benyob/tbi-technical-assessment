from app.core.retrieval import select_relevant_chunks


def test_retrieval_selects_relevant_chunks():
    chunks = [
        "This chunk talks about dropout in neural networks.",
        "This is about reinforcement learning.",
        "Dropout is used for regularization."
    ]
    query = "dropout"
    selected = select_relevant_chunks(chunks, query)
    assert len(selected) > 0
    assert "dropout" in selected[0].lower()
