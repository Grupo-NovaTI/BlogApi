from datetime import datetime, timezone
from test import Base
from typing import Any, Generator
from unittest.mock import AsyncMock, Mock, MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.core.dependencies.dependencies import (_provide_file_storage_service,
                                                _provide_user_services,
                                                provide_token_payload,
                                                provide_user_id_from_token, _provide_blog_service)
from app.main import app
from app.users.models.user_model import UserModel
from app.blogs.models.blog_model import BlogModel

@pytest.fixture
def mock_db_session() -> MagicMock:
    """
    Fixture that creates a mock SQLAlchemy session.
    """
    return MagicMock()
# --- Mock Service Fixtures ---
@pytest.fixture(scope="function")
def mock_user_service() -> Mock:
    """Provides a fresh mock of the user service for each test function."""
    return Mock()

@pytest.fixture(scope="function")
def mock_file_service() -> AsyncMock:
    """Provides a fresh mock of the file storage service for each test function."""
    return AsyncMock()

@pytest.fixture(scope="function")
def mock_blog_service() -> Mock:
    """Provides a fresh mock of the blog service for each test function."""
    return Mock()

# --- Data Fixtures ---
@pytest.fixture(scope="session")
def sample_user_data() -> dict[str, Any]:
    """Provides sample user data that can be used across tests."""
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "name": "Test",
        "last_name": "User",
        "is_active": True,
        "role": "user",
        "profile_picture": "https://example.com/default.png",
        "created_at": datetime.now(tz=timezone.utc),
        "updated_at": datetime.now(tz=timezone.utc),
        "hashed_password": "fake_hash",
    }

@pytest.fixture
def sample_blog() -> BlogModel:
    """
    Fixture that provides a sample BlogModel for testing.
    """
    return BlogModel(
        id=1,
        title="Test Blog",
        content="Test content",
        user_id=1,
        is_published=True,
        created_at=datetime.now(tz=timezone.utc),
        updated_at=datetime.now(tz=timezone.utc),
    )


@pytest.fixture
def sample_blog_data() -> dict[str, Any]:
    """
    Fixture that provides sample blog data for creation/update operations.
    """
    return {
        "title": "New Blog",
        "content": "New blog content",
        "is_published": True,
                "image_url": "https://example.com/image.png",
        "created_at": datetime.now(tz=timezone.utc),
        "updated_at": datetime.now(tz=timezone.utc)
    }


@pytest.fixture(scope="function")
def auth_client(
    mock_user_service: Mock, mock_file_service: AsyncMock, mock_blog_service: Mock
) -> Generator[TestClient, Any, None]:
    """
    Creates a TestClient with dependency overrides for an authenticated user.

    This client simulates a request from a user with ID=1 and role='user'.
    It automatically injects mock services into the FastAPI application.
    The `yield` statement ensures that dependency overrides are cleaned up
    after each test.
    """
    app.dependency_overrides[_provide_user_services] = lambda: mock_user_service
    app.dependency_overrides[_provide_file_storage_service] = lambda: mock_file_service
    app.dependency_overrides[_provide_blog_service] = lambda: mock_blog_service

    app.dependency_overrides[provide_user_id_from_token] = lambda: 1
    app.dependency_overrides[provide_token_payload] = lambda: {"user_id": 1, "role": "user"}

    with TestClient(app, base_url="http://testserver/api/v1") as client:
        yield client

    app.dependency_overrides.clear()
    
    
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine: Engine = create_engine(url=SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Database Fixtures ---
@pytest.fixture(scope="function")
def db_session() -> Generator[Session, Any, None]:
    """
    Fixture for database session.
    """
    Base.metadata.create_all(bind=engine)
    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
