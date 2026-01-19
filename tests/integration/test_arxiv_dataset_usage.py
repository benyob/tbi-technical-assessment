import pytest
from app.data.arxiv_dataset import load_arxiv_sample


@pytest.mark.optional
def test_load_arxiv_sample():
    try:
        sample = load_arxiv_sample()
        assert "article" in sample
        assert "abstract" in sample
    except Exception:
        pytest.skip("Dataset download requires internet access.")
