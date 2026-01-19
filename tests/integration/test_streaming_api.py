from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_streaming_endpoint_returns_events():
    response = client.post(
        "/analyze/stream",
        json={
            "document_text": "Dropout helps prevent overfitting.",
            "query": "Explain dropout"
        },
        stream=True,
    )

    chunks = []
    for chunk in response.iter_text():
        chunks.append(chunk)
        if len(chunks) > 2:
            break

    assert len(chunks) > 0
