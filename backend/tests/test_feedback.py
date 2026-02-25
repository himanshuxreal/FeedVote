import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import crud, schemas


# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

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


def test_create_feedback():
    """Test feedback creation"""
    # First create a user
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com"}
    )
    # If user endpoint doesn't exist, we'll skip this test
    
    # For testing without users endpoint, we assume user_id = 1
    response = client.post(
        "/feedback/?user_id=1",
        json={
            "title": "Improve UI",
            "description": "Add dark mode"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Improve UI"
    assert data["description"] == "Add dark mode"


def test_get_all_feedback():
    """Test getting all feedback"""
    response = client.get("/feedback/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_feedback_by_id():
    """Test getting feedback by ID"""
    response = client.get("/feedback/1")
    # Should return 404 if feedback doesn't exist
    assert response.status_code == 404


def test_invalid_feedback_creation():
    """Test invalid input validation"""
    # Empty title
    response = client.post(
        "/feedback/?user_id=1",
        json={
            "title": "",
            "description": "Add dark mode"
        }
    )
    # Should fail validation
    assert response.status_code in [422, 400]
    
    # Empty description
    response = client.post(
        "/feedback/?user_id=1",
        json={
            "title": "Improve UI",
            "description": ""
        }
    )
    assert response.status_code in [422, 400]


def test_pagination():
    """Test pagination parameters"""
    # Invalid skip
    response = client.get("/feedback/?skip=-1")
    assert response.status_code == 400
    
    # Invalid limit
    response = client.get("/feedback/?limit=0")
    assert response.status_code == 400
    
    # Invalid limit (too large)
    response = client.get("/feedback/?limit=101")
    assert response.status_code == 400
    
    # Valid parameters
    response = client.get("/feedback/?skip=0&limit=10")
    assert response.status_code == 200


def test_feedback_not_found():
    """Test getting non-existent feedback"""
    response = client.get("/feedback/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_invalid_feedback_id():
    """Test invalid feedback ID"""
    response = client.get("/feedback/-1")
    assert response.status_code == 400
    
    response = client.get("/feedback/0")
    assert response.status_code == 400
