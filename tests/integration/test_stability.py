from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_stability_multiple_requests():
    for _ in range(20):  # conservative, fast
        response = client.post(
            "/analyze",
            json={
                "document_text": "This document discusses neural networks.",
                "query": "What is this about?"
            }
        )
        assert response.status_code == 200
