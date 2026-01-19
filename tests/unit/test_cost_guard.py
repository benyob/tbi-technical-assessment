from app.core.budgets import MAX_API_COST_USD


def test_max_api_cost_is_capped():
    assert MAX_API_COST_USD <= 0.01
