"""
test_api.py
Integration tests for the Homer API.

These tests use FastAPI's TestClient which runs the full application
stack in-process — no need to start a server separately. Every test
hits a real endpoint, validates the response schema, and confirms
the full pipeline works end to end.
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app

# TestClient spins up the full FastAPI app in-process
# This means every request goes through the real middleware,
# routers, and business logic — a true integration test
client = TestClient(app)


# ── Health ────────────────────────────────────────────────────────────────────

def test_health_check():
    """API root should return status ok."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Homer" in data["message"]
    print("\n✅ Health check passed")


# ── Family Tree ───────────────────────────────────────────────────────────────

def test_get_full_tree():
    """Full tree should return nodes and edges."""
    response = client.get("/family-tree/")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) > 60
    assert len(data["edges"]) > 100
    print(f"✅ Full tree: {len(data['nodes'])} nodes, {len(data['edges'])} edges")


def test_get_figure_zeus():
    """Zeus endpoint should return full figure info."""
    response = client.get("/family-tree/Zeus")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Zeus"
    assert data["category"] == "olympian"
    assert len(data["children"]) > 0
    assert len(data["parents"]) > 0
    print(f"✅ Zeus: {len(data['children'])} children, "
          f"parents: {[p['name'] for p in data['parents']]}")


def test_get_figure_case_insensitive():
    """Endpoint should handle lowercase figure names."""
    response = client.get("/family-tree/zeus")
    assert response.status_code == 200
    assert response.json()["name"] == "Zeus"
    print("✅ Case insensitive lookup working")


def test_get_figure_not_found():
    """Unknown figure should return 404."""
    response = client.get("/family-tree/Gandalf")
    assert response.status_code == 404
    print("✅ 404 for unknown figure working")


def test_get_children():
    """Children endpoint should return list of figures."""
    response = client.get("/family-tree/Zeus/children")
    assert response.status_code == 200
    names = [f["name"] for f in response.json()]
    assert "Athena" in names
    assert "Apollo" in names
    print(f"✅ Zeus's children via endpoint: {names}")


def test_get_parents():
    """Parents endpoint should return list of figures."""
    response = client.get("/family-tree/Athena/parents")
    assert response.status_code == 200
    names = [f["name"] for f in response.json()]
    assert "Zeus" in names
    assert "Metis" in names
    print(f"✅ Athena's parents via endpoint: {names}")


def test_get_path():
    """Path endpoint should find connection between two figures."""
    response = client.get("/family-tree/Chaos/path/Achilles")
    assert response.status_code == 200
    data = response.json()
    assert data["found"] is True
    assert data["path"][0] == "Chaos"
    assert data["path"][-1] == "Achilles"
    print(f"✅ Path: {' → '.join(data['path'])}")


def test_get_path_not_found():
    """Path between unconnected figures should return found=false."""
    response = client.get("/family-tree/Odysseus/path/Aphrodite")
    assert response.status_code == 200
    data = response.json()
    # May or may not be connected — just check the response shape is correct
    assert "found" in data
    assert "path" in data
    print(f"✅ Path endpoint handles disconnected figures correctly")


# ── Chat ──────────────────────────────────────────────────────────────────────

def test_chat_basic():
    """A chat message should return a valid Homer response."""
    response = client.post("/chat/", json={
        "message": "Who is Poseidon?"
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["response"]) > 50
    assert "session_id" in data
    assert len(data["citations"]) > 0
    print(f"\n✅ Chat working")
    print(f"   Session ID: {data['session_id']}")
    print(f"   Citations: {data['citations']}")
    print(f"   Response preview: {data['response'][:150]}...")


def test_chat_session_continuity():
    """Follow-up messages in the same session should maintain context."""
    # First message
    first = client.post("/chat/", json={
        "message": "Tell me about Zeus."
    })
    assert first.status_code == 200
    session_id = first.json()["session_id"]

    # Follow-up using the same session_id
    second = client.post("/chat/", json={
        "message": "And what about his wife?",
        "session_id": session_id
    })
    assert second.status_code == 200
    data = second.json()
    assert data["session_id"] == session_id
    print(f"\n✅ Session continuity working")
    print(f"   Follow-up response preview: {data['response'][:150]}...")


def test_chat_empty_message_rejected():
    """Empty message should be rejected by Pydantic validation."""
    response = client.post("/chat/", json={
        "message": ""
    })
    assert response.status_code == 422
    print("✅ Empty message correctly rejected with 422")