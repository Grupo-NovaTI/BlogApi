from test import (ConflictException, NotFoundException, UserModel,
                  UserRepository, UserService)
from unittest.mock import MagicMock, patch

import pytest

# --- Pytest Fixtures ---

@pytest.fixture
def mock_user_repo() -> MagicMock:
    """
    Fixture that creates a mock (simulator) of UserRepository.
    We can control what its methods return in each test.
    """
    return MagicMock(spec=UserRepository)

@pytest.fixture
def mock_db_session() -> MagicMock:
    """
    Fixture that creates a mock of the SQLAlchemy session.
    For the service layer, we often don't need a real session,
    just an object that can be passed to the constructor.
    """
    return MagicMock()

@pytest.fixture
def user_service(mock_user_repo: MagicMock, mock_db_session: MagicMock):
    """
    Fixture that creates an instance of UserService with the mocks.
    """
    # We disable the decorators to test the internal logic of the method in isolation.
    # The 'patch' temporarily replaces the decorator with a function that simply
    # executes the original function without any additional transaction or error handling logic.
    with patch('app.users.services.user_service.handle_service_transaction', lambda **kwargs: lambda f: f), \
         patch('app.users.services.user_service.handle_read_exceptions', lambda **kwargs: lambda f: f):
        yield UserService(user_repository=mock_user_repo, db_session=mock_db_session)


# --- Test Class for UserService ---

class TestUserService:
    """Test group for UserService."""

    def test_create_user_success(self, user_service, mock_user_repo):
        """
        Test successful creation of a user when it does not already exist.
        """
        # 1. Arrange 
        user_data: dict[str, str] = {"username": "newuser", "email": "new@example.com"}
        
        # Configure the mock: when get_user_by_email_or_username is called, it should return None (does not exist).
        mock_user_repo.get_user_by_email_or_username.return_value = None
        
        # Configure the mock: the create_user method should return a simulated user.
        created_user_mock = UserModel(id=1, **user_data)
        mock_user_repo.create_user.return_value = created_user_mock

        # 2. Act
        result = user_service.create_user(user_data)

        # 3. Assert
        # Verify that the repository was called to check if the user existed.
        mock_user_repo.get_user_by_email_or_username.assert_called_once_with(
            email="new@example.com", username="newuser"
        )
        # Verify that the repository was called to create the user.
        mock_user_repo.create_user.assert_called_once()
        # Verify that the result is what the repository returned.
        assert result.id == 1
        assert result.username == "newuser"

    def test_create_user_already_exists(self, user_service: UserService, mock_user_repo: MagicMock) -> None:
        """
        Test that ConflictException is raised if the user already exists.
        """
        # 1. Arrange
        user_data: dict[str, str] = {"username": "existinguser", "email": "existing@example.com"}
        existing_user_mock = UserModel(id=1, **user_data)

        # Configure the mock: simulate that the user already exists.
        mock_user_repo.get_user_by_email_or_username.return_value = existing_user_mock

        # 2. Act & 3. Assert
        # Check that ConflictException is raised when trying to create a user that already exists.
        with pytest.raises(expected_exception=ConflictException) as excinfo:
            user_service.create_user(user_data=user_data)
        
        # Optional: check the exception message.
        assert "user with this email or username already exists" in str(excinfo.value.details).lower()
        # Verify that the create_user method was NEVER called.
        mock_user_repo.create_user.assert_not_called()

    def test_get_user_by_id_success(self, user_service: UserService, mock_user_repo: MagicMock) -> None:
        """
        Test getting a user by ID when it exists.
        """
        # 1. Arrange
        user_id = 1
        expected_user = UserModel(id=user_id, username="test", email="test@test.com")
        mock_user_repo.get_user_by_id.return_value = expected_user

        # 2. Act
        result = user_service.get_user_by_id(user_id)

        # 3. Assert
        mock_user_repo.get_user_by_id.assert_called_once_with(user_id=user_id)
        assert result == expected_user

    def test_get_user_by_id_not_found(self, user_service: UserService, mock_user_repo: MagicMock) -> None:
        """
        Test that NotFoundException is raised when the user is not found.
        """
        # 1. Arrange
        user_id = 999
        # Simulate that the repository finds nothing.
        mock_user_repo.get_user_by_id.return_value = None

        # 2. Act & 3. Assert
        with pytest.raises(expected_exception=NotFoundException):
            user_service.get_user_by_id(user_id=user_id)
            
        mock_user_repo.get_user_by_id.assert_called_once_with(user_id=user_id)

    def test_update_user_success(self, user_service: UserService, mock_user_repo: MagicMock) -> None:
        """
        Test successful update of a user.
        """
        # 1. Arrange
        user_id = 1
        update_data: dict[str, str] = {"username": "updated_name"}
        
        # Simulate the user that exists in the DB
        original_user = UserModel(id=user_id, username="original_name", email="test@test.com")
        mock_user_repo.get_user_by_id.return_value = original_user
        
        # Simulate the already updated user returned by the repo
        updated_user_mock = UserModel(id=user_id, username="updated_name", email="test@test.com")
        mock_user_repo.update_user.return_value = updated_user_mock
        
        # 2. Act
        result = user_service.update_user(user_id, update_data)

        # 3. Assert
        # First, the user was searched for
        mock_user_repo.get_user_by_id.assert_called_once_with(user_id=user_id)
        # Then it was called to update with the correct data
        mock_user_repo.update_user.assert_called_once_with(user=original_user, user_data=update_data)
        # The result is as expected
        assert result.username == "updated_name" # type: ignore
        
    def test_delete_user_success(self, user_service: UserService, mock_user_repo: MagicMock) -> None:
        """
        Test successful deletion of a user.
        """
        # 1. Arrange
        user_id = 1
        user_to_delete = UserModel(id=user_id, username="delete_me", email="delete@me.com")
        mock_user_repo.get_user_by_id.return_value = user_to_delete

        # 2. Act
        user_service.delete_user_by_id(user_id)

        # 3. Assert
        mock_user_repo.get_user_by_id.assert_called_once_with(user_id=user_id)
        mock_user_repo.delete_user.assert_called_once_with(user=user_to_delete)

    def test_delete_user_not_found(self, user_service: UserService, mock_user_repo: MagicMock) -> None:
        """
        Test that NotFoundException is raised when trying to delete a non-existent user.
        """
        # 1. Arrange
        user_id = 999
        mock_user_repo.get_user_by_id.return_value = None

        # 2. Act & 3. Assert
        with pytest.raises(NotFoundException):
            user_service.delete_user_by_id(user_id)
            
        # The delete method should never be called if the user is not found
        mock_user_repo.delete_user.assert_not_called()