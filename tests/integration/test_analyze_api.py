from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analyze_endpoint_success():
    response = client.post(
        "/analyze",
        json={
            "document_text": "Dropout is a regularization technique in deep learning.",
            "query": "What is dropout?"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "chunks_used" in data
