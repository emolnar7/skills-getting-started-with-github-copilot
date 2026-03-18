import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: Test GET /activities

def test_get_activities():
    # Arrange: nothing to setup
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Arrange-Act-Assert: Test POST /activities/{activity_name}/signup

def test_signup_for_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_signup_for_activity_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_for_activity_not_found():
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# Arrange-Act-Assert: Test DELETE /activities/{activity_name}/unregister

def test_unregister_from_activity_success():
    # Arrange
    activity = "Programming Class"
    email = "tempstudent@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

def test_unregister_from_activity_not_registered():
    # Arrange
    activity = "Programming Class"
    email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

def test_unregister_from_activity_not_found():
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
