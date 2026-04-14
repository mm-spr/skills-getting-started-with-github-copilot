"""
Tests for the Mergington High School Activities API.

Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a known state before each test."""
    original_state = {
        name: {**data, "participants": list(data["participants"])}
        for name, data in activities.items()
    }
    yield
    activities.clear()
    activities.update(original_state)


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestGetActivities:
    def test_get_activities_returns_all_activities(self, client):
        # Arrange - no special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert "Chess Club" in data

    def test_get_activities_includes_description(self, client):
        # Arrange - no special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        for activity in response.json().values():
            assert "description" in activity
            assert "schedule" in activity
            assert "max_participants" in activity
            assert "participants" in activity

    def test_root_redirects_to_index(self, client):
        # Arrange - no special setup needed

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestSignupForActivity:
    def test_signup_adds_student_to_activity(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]

    def test_signup_returns_success_message(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "another@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert "message" in response.json()

    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404

    def test_signup_duplicate_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # already signed up

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_full_activity_returns_400(self, client):
        # Arrange
        activity_name = "Math Olympiad"  # max_participants: 10, currently 2
        existing_count = len(activities[activity_name]["participants"])
        for i in range(activities[activity_name]["max_participants"] - existing_count):
            activities[activity_name]["participants"].append(f"filler{i}@mergington.edu")

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email=overflow@mergington.edu")

        # Assert
        assert response.status_code == 400
        assert "full" in response.json()["detail"]

    def test_signup_decreases_available_spots(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        spots_before = activities[activity_name]["max_participants"] - len(activities[activity_name]["participants"])

        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        spots_after = activities[activity_name]["max_participants"] - len(activities[activity_name]["participants"])
        assert spots_after == spots_before - 1


class TestUnregisterFromActivity:
    def test_unregister_removes_student_from_activity(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # already signed up

        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404

    def test_unregister_student_not_signed_up_returns_404(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404

    def test_unregister_returns_success_message(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # already signed up

        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert "message" in response.json()

    def test_unregister_increases_available_spots(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # already signed up
        spots_before = activities[activity_name]["max_participants"] - len(activities[activity_name]["participants"])

        # Act
        client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        spots_after = activities[activity_name]["max_participants"] - len(activities[activity_name]["participants"])
        assert spots_after == spots_before + 1
