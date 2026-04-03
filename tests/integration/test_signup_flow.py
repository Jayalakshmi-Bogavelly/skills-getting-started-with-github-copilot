import pytest
from fastapi.testclient import TestClient

def test_complete_signup_flow(client: TestClient):
    """Test complete signup and unregister flow"""
    # Initial state: Basketball Team has no participants
    response = client.get("/activities")
    activities = response.json()
    assert activities["Basketball Team"]["participants"] == []

    # Sign up a student
    response = client.post("/activities/Basketball Team/signup?email=alice@mergington.edu")
    assert response.status_code == 200

    # Verify added
    response = client.get("/activities")
    activities = response.json()
    assert "alice@mergington.edu" in activities["Basketball Team"]["participants"]

    # Sign up another student
    response = client.post("/activities/Basketball Team/signup?email=bob@mergington.edu")
    assert response.status_code == 200

    # Verify both added
    response = client.get("/activities")
    activities = response.json()
    participants = activities["Basketball Team"]["participants"]
    assert "alice@mergington.edu" in participants
    assert "bob@mergington.edu" in participants
    assert len(participants) == 2

    # Unregister one
    response = client.delete("/activities/Basketball Team/signup?email=alice@mergington.edu")
    assert response.status_code == 200

    # Verify removed
    response = client.get("/activities")
    activities = response.json()
    participants = activities["Basketball Team"]["participants"]
    assert "alice@mergington.edu" not in participants
    assert "bob@mergington.edu" in participants
    assert len(participants) == 1

def test_signup_multiple_activities(client: TestClient):
    """Test signing up for multiple activities"""
    # Sign up for two different activities
    client.post("/activities/Basketball Team/signup?email=charlie@mergington.edu")
    client.post("/activities/Soccer Club/signup?email=charlie@mergington.edu")

    # Verify in both
    response = client.get("/activities")
    activities = response.json()
    assert "charlie@mergington.edu" in activities["Basketball Team"]["participants"]
    assert "charlie@mergington.edu" in activities["Soccer Club"]["participants"]

    # Unregister from one
    client.delete("/activities/Basketball Team/signup?email=charlie@mergington.edu")

    # Verify removed from one but not the other
    response = client.get("/activities")
    activities = response.json()
    assert "charlie@mergington.edu" not in activities["Basketball Team"]["participants"]
    assert "charlie@mergington.edu" in activities["Soccer Club"]["participants"]

def test_edge_case_empty_email(client: TestClient):
    """Test signup with empty email (edge case)"""
    # This should still work as FastAPI handles query params, but let's test
    response = client.post("/activities/Basketball Team/signup?email=")
    assert response.status_code == 200  # Assuming no validation

    # But perhaps we should add validation, but for now test as is
    response = client.get("/activities")
    activities = response.json()
    assert "" in activities["Basketball Team"]["participants"]