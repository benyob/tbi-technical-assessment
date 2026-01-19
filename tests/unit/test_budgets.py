from app.core.budgets import MAX_OUTPUT_TOKENS


def test_output_token_budget_reasonable():
    assert MAX_OUTPUT_TOKENS <= 500
