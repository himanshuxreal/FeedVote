"""
Shared pytest configuration and fixtures for FeedVote tests.

This conftest.py file provides:
- Centralized test database setup/teardown
- Shared fixtures for client, database, and user creation
- Consistent test configuration across all test files
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db


# Test database configuration
# Using in-memory SQLite for fast, isolated tests without file system dependency
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine with StaticPool to persist in-memory database across connections
# This is required for in-memory SQLite databases
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Create test session factory
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =====================
# Fixtures
# =====================

@pytest.fixture(scope="function")
def db_session():
    """
    Create a clean database session for each test.
    
    Automatically creates and drops all tables for test isolation.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    # Override dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield session
    
    # Cleanup: drop all tables after test
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client with database session override.
    
    Use this fixture to test API endpoints without real database.
    """
    return TestClient(app)


@pytest.fixture(scope="function")
def test_user(client):
    """
    Create a test user for use in tests.
    
    Returns: Dictionary with user data (id, username, email)
    """
    user_response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com"
        }
    )
    
    if user_response.status_code == 201:
        return user_response.json()
    
    # Fallback for tests that don't rely on real user creation
    return {"id": 1, "username": "testuser", "email": "test@example.com"}


@pytest.fixture(scope="function")
def test_feedback(client, test_user):
    """
    Create test feedback for use in tests.
    
    Returns: Dictionary with feedback data (id, title, description, user_id)
    """
    feedback_response = client.post(
        f"/feedback/?user_id={test_user['id']}",
        json={
            "title": "Test Feedback",
            "description": "This is test feedback for testing"
        }
    )
    
    if feedback_response.status_code == 201:
        return feedback_response.json()
    
    # Fallback for tests that don't rely on real feedback creation
    return {
        "id": 1,
        "title": "Test Feedback",
        "description": "This is test feedback for testing",
        "user_id": test_user['id']
    }


@pytest.fixture(scope="function")
def another_user(client):
    """
    Create another test user for testing multi-user scenarios.
    
    Returns: Dictionary with user data (id, username, email)
    """
    user_response = client.post(
        "/users/",
        json={
            "username": "testuser2",
            "email": "test2@example.com"
        }
    )
    
    if user_response.status_code == 201:
        return user_response.json()
    
    # Fallback
    return {"id": 2, "username": "testuser2", "email": "test2@example.com"}


# =====================
# Pytest Configuration
# =====================

def pytest_configure(config):
    """
    Configure pytest with custom markers.
    
    Allows organizing tests by type:
    - @pytest.mark.unit: Unit tests
    - @pytest.mark.integration: Integration tests
    - @pytest.mark.slow: Slow running tests
    """
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# =====================
# Session-wide setup/teardown
# =====================

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Setup and teardown for entire test session.
    
    Runs once per test session (not per test).
    """
    # Create all tables at session start
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Cleanup after all tests
    Base.metadata.drop_all(bind=engine)
