import asyncio, json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True

def test_ingest_search_chat():
    r = client.post("/ingest", json={"text":"Weaviate stores vectors. Comet tracks runs."})
    assert r.status_code == 200
    r = client.get("/search", params={"q":"vector database","k":3})
    assert r.status_code == 200
    r = client.post("/chat", json={"message":"How are we tracking experiments?"})
    assert r.status_code == 200
    assert "reply" in r.json()
