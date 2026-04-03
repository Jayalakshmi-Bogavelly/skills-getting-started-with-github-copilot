import pytest
from fastapi.testclient import TestClient

def test_get_activities(client: TestClient):
    """Test GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # We have 9 activities
    assert "Chess Club" in data
    assert "Programming Class" in data

    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_for_activity_success(client: TestClient):
    """Test successful signup for an activity"""
    response = client.post("/activities/Basketball Team/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up test@mergington.edu for Basketball Team" in data["message"]

    # Verify the participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "test@mergington.edu" in activities["Basketball Team"]["participants"]

def test_signup_for_nonexistent_activity(client: TestClient):
    """Test signup for activity that doesn't exist"""
    response = client.post("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_signup_duplicate(client: TestClient):
    """Test signing up for the same activity twice"""
    # First signup
    client.post("/activities/Basketball Team/signup?email=test@mergington.edu")

    # Second signup should fail
    response = client.post("/activities/Basketball Team/signup?email=test@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]

def test_unregister_from_activity_success(client: TestClient):
    """Test successful unregister from an activity"""
    # First signup
    client.post("/activities/Basketball Team/signup?email=test@mergington.edu")

    # Then unregister
    response = client.delete("/activities/Basketball Team/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered test@mergington.edu from Basketball Team" in data["message"]

    # Verify the participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert "test@mergington.edu" not in activities["Basketball Team"]["participants"]

def test_unregister_from_nonexistent_activity(client: TestClient):
    """Test unregister from activity that doesn't exist"""
    response = client.delete("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_unregister_not_signed_up(client: TestClient):
    """Test unregistering when not signed up"""
    response = client.delete("/activities/Basketball Team/signup?email=test@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student is not registered for this activity" in data["detail"]