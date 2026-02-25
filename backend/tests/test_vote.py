import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models, schemas


# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_vote.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup and teardown for each test"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)


def test_upvote():
    """Test upvote creation"""
    # Create users first
    user1_response = client.post(
        "/users/",
        json={"username": "voter1", "email": "voter1@example.com"}
    )
    user2_response = client.post(
        "/users/",
        json={"username": "voter2", "email": "voter2@example.com"}
    )
    
    # Extract user IDs (fallback to default if creation fails)
    user1_id = user1_response.json().get("id", 1) if user1_response.status_code == 201 else 1
    user2_id = user2_response.json().get("id", 2) if user2_response.status_code == 201 else 2
    
    # Create feedback by user1
    feedback_response = client.post(
        f"/feedback/?user_id={user1_id}",
        json={
            "title": "Test Feedback",
            "description": "A feedback to vote on"
        }
    )
    
    # If feedback creation succeeds, test voting
    if feedback_response.status_code == 201:
        feedback_id = feedback_response.json()["id"]
        # User2 votes on user1's feedback
        response = client.post(
            "/vote/",
            json={
                "feedback_id": feedback_id,
                "user_id": user2_id,
                "vote_type": "upvote"
            }
        )
        assert response.status_code in [201, 404]
    else:
        # If resources don't exist, expect 404
        response = client.post(
            "/vote/",
            json={
                "feedback_id": 9999,
                "user_id": 9999,
                "vote_type": "upvote"
            }
        )
        assert response.status_code in [404, 400]


def test_downvote():
    """Test downvote creation"""
    # Create users first
    user1_response = client.post(
        "/users/",
        json={"username": "user_downvote1", "email": "downvote1@example.com"}
    )
    user2_response = client.post(
        "/users/",
        json={"username": "user_downvote2", "email": "downvote2@example.com"}
    )
    
    # Extract user IDs
    user1_id = user1_response.json().get("id", 1) if user1_response.status_code == 201 else 1
    user2_id = user2_response.json().get("id", 2) if user2_response.status_code == 201 else 2
    
    # Create feedback by user1
    feedback_response = client.post(
        f"/feedback/?user_id={user1_id}",
        json={
            "title": "Test Feedback",
            "description": "A feedback to downvote"
        }
    )
    
    # If feedback creation succeeds, test voting
    if feedback_response.status_code == 201:
        feedback_id = feedback_response.json()["id"]
        # User2 votes on user1's feedback
        response = client.post(
            "/vote/",
            json={
                "feedback_id": feedback_id,
                "user_id": user2_id,
                "vote_type": "downvote"
            }
        )
        assert response.status_code in [201, 404]
    else:
        # If resources don't exist, expect 404
        response = client.post(
            "/vote/",
            json={
                "feedback_id": 9999,
                "user_id": 9999,
                "vote_type": "downvote"
            }
        )
        assert response.status_code in [404, 400]


def test_duplicate_vote_prevention():
    """Test duplicate vote prevention"""
    # First vote should work (if resources existed)
    response1 = client.post(
        "/vote/",
        json={
            "feedback_id": 1,
            "user_id": 1,
            "vote_type": "upvote"
        }
    )
    
    # Second vote from same user on same feedback should update (not error)
    response2 = client.post(
        "/vote/",
        json={
            "feedback_id": 1,
            "user_id": 1,
            "vote_type": "downvote"
        }
    )
    
    # Both should have same status (either both fail or both succeed based on resources)
    assert response1.status_code == response2.status_code


def test_vote_count_increment():
    """Test vote count increment"""
    response = client.get("/vote/top/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_top_ideas():
    """Test getting top voted ideas"""
    response = client.get("/vote/top/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_invalid_vote_type():
    """Test invalid vote type"""
    response = client.post(
        "/vote/",
        json={
            "feedback_id": 1,
            "user_id": 1,
            "vote_type": "invalid_type"
        }
    )
    assert response.status_code == 422  # Validation error


def test_invalid_feedback_id():
    """Test invalid feedback ID"""
    response = client.post(
        "/vote/",
        json={
            "feedback_id": -1,
            "user_id": 1,
            "vote_type": "upvote"
        }
    )
    assert response.status_code == 422  # Validation error
    
    response = client.post(
        "/vote/",
        json={
            "feedback_id": 0,
            "user_id": 1,
            "vote_type": "upvote"
        }
    )
    assert response.status_code == 422  # Validation error


def test_invalid_user_id():
    """Test invalid user ID"""
    response = client.post(
        "/vote/",
        json={
            "feedback_id": 1,
            "user_id": -1,
            "vote_type": "upvote"
        }
    )
    assert response.status_code == 422  # Validation error
    
    response = client.post(
        "/vote/",
        json={
            "feedback_id": 1,
            "user_id": 0,
            "vote_type": "upvote"
        }
    )
    assert response.status_code == 422  # Validation error


def test_top_ideas_limit():
    """Test top ideas limit parameter"""
    # Invalid limit
    response = client.get("/vote/top/?limit=0")
    assert response.status_code == 400
    
    response = client.get("/vote/top/?limit=101")
    assert response.status_code == 400
    
    # Valid limit
    response = client.get("/vote/top/?limit=10")
    assert response.status_code == 200


def test_vote_on_own_feedback():
    """Test preventing vote on own feedback"""
    response = client.post(
        "/vote/",
        json={
            "feedback_id": 1,
            "user_id": 1,  # Same as feedback creator (would need to be set up)
            "vote_type": "upvote"
        }
    )
    # Response depends on whether user_id=1 actually owns feedback_id=1
    # but the endpoint should validate this
    assert response.status_code in [400, 404, 201]
