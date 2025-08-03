"""
Comprehensive test suite for user endpoints.

This module contains tests for all user-related API endpoints including:
- GET /users/me (get current user)
- GET /users/{user_id} (get user by ID)
- GET /users (get all users)
- DELETE /users/me (delete current user)
- PATCH /users/me/status (activate/deactivate user)
- PATCH /users/me (update user profile)
- POST /users/me/profile-picture (upload profile picture)

NOTE: This test file relies on shared fixtures defined in `tests/utils/conftest.py`
      (e.g., auth_client, mock_user_service, mock_file_service, sample_user_data).
"""

from typing import Any, List
from httpx import Response
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from unittest.mock import Mock, patch
from io import BytesIO
from test.utils.conftest import auth_client, mock_user_service, mock_file_service, sample_user_data
from app.users.models.user_model import UserModel
from app.utils.errors.exceptions import NotFoundException


class TestUserEndpoints:
    """Base class for grouping user endpoint tests."""
    pass


@pytest.mark.asyncio
class TestGetCurrentUser(TestUserEndpoints):
    """Tests for GET /users/me endpoint."""

    async def test_get_current_user_success(self, auth_client: TestClient, mock_user_service: Mock, sample_user_data: dict[str, Any]):
        """Test successful retrieval of current user."""
        # Arrange
        user_model = UserModel(**sample_user_data)
        mock_user_service.get_user_by_id.return_value = user_model

        # Act
        response: Response = auth_client.get("/users/me")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["username"] == "testuser"
        assert response_data["email"] == "test@example.com"
        mock_user_service.get_user_by_id.assert_called_once_with(user_id=1)

    async def test_get_current_user_not_found(self, auth_client: TestClient, mock_user_service: Mock):
        """Test current user not found."""
        # Arrange
        mock_user_service.get_user_by_id.side_effect = NotFoundException(identifier=1, resource_type="Users")

        # Act
        response: Response = auth_client.get("/users/me")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetUserById(TestUserEndpoints):
    """Tests for GET /users/{user_id} endpoint."""

    def test_get_user_by_id_success(self, auth_client: TestClient, mock_user_service: Mock, sample_user_data: dict):
        """Test successful retrieval of user by ID."""
        # Arrange
        user_model = UserModel(**sample_user_data)
        mock_user_service.get_user_by_id.return_value = user_model

        # Act
        response: Response = auth_client.get("/users/1")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == 1
        assert response_data["username"] == "testuser"
        mock_user_service.get_user_by_id.assert_called_with(user_id=1)

    def test_get_user_by_id_not_found(self, auth_client: TestClient, mock_user_service: Mock):
        """Test user not found by ID."""
        # Arrange
        mock_user_service.get_user_by_id.side_effect = NotFoundException(identifier=999, resource_type="Users")

        # Act
        response: Response = auth_client.get("/users/999")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_user_by_id_invalid_path_param(self, auth_client: TestClient):
        """Test invalid user ID path parameter."""
        # Act
        response: Response = auth_client.get("/users/0")

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_user_by_id_path_param_too_large(self, auth_client: TestClient):
        """Test user ID path parameter exceeds maximum."""
        # Act
        response: Response = auth_client.get("/users/1000001") 

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetAllUsers(TestUserEndpoints):
    """Tests for GET /users endpoint."""

    def test_get_all_users_success(self, auth_client: TestClient, mock_user_service: Mock, sample_user_data: dict):
        """Test successful retrieval of all users."""
        # Arrange
        user1 = UserModel(**sample_user_data)
        user2_data = {**sample_user_data, "id": 2, "username": "user2", "email": "user2@example.com"}
        user2 = UserModel(**user2_data)
        users_list = [user1, user2]
        mock_user_service.get_all_users.return_value = users_list

        # Act
        response: Response = auth_client.get("/users")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data) == 2
        assert response_data[0]["username"] == "testuser"
        assert response_data[1]["username"] == "user2"
        mock_user_service.get_all_users.assert_called_once_with(offset=0, limit=10)

    def test_get_all_users_with_pagination(self, auth_client: TestClient, mock_user_service: Mock, sample_user_data: dict):
        """Test users retrieval with pagination parameters."""
        # Arrange
        user1 = UserModel(**sample_user_data)
        users_list: List[UserModel] = [user1]
        mock_user_service.get_all_users.return_value = users_list

        # Act
        response: Response = auth_client.get("/users?limit=5&offset=10")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        mock_user_service.get_all_users.assert_called_once_with(offset=10, limit=5)

    def test_get_all_users_invalid_limit(self, auth_client: TestClient):
        """Test invalid limit parameter."""
        # Act
        response: Response = auth_client.get("/users?limit=0")  # Invalid: below minimum

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_all_users_invalid_offset(self, auth_client: TestClient):
        """Test invalid offset parameter."""
        # Act
        response: Response = auth_client.get("/users?offset=-1")  # Invalid: below minimum

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteCurrentUser(TestUserEndpoints):
    """Tests for DELETE /users/me endpoint."""

    def test_delete_current_user_success(self, auth_client: TestClient, mock_user_service: Mock):
        """Test successful deletion of current user."""
        # Arrange
        mock_user_service.delete_user_by_id.return_value = None

        # Act
        response: Response = auth_client.delete("/users/me")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_user_service.delete_user_by_id.assert_called_once_with(user_id=1)

    def test_delete_current_user_not_found(self, auth_client: TestClient, mock_user_service: Mock):
        """Test deletion of non-existent current user."""
        # Arrange
        mock_user_service.delete_user_by_id.side_effect = NotFoundException(identifier=1, resource_type="Users")

        # Act
        response: Response = auth_client.delete("/users/me")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestReactivateUserAccount(TestUserEndpoints):
    """Tests for PATCH /users/me/status endpoint."""

    def test_reactivate_user_account_success(self, auth_client: TestClient, mock_user_service: Mock, sample_user_data: dict):
        """Test successful user account reactivation."""
        # Arrange
        updated_user = UserModel(**{**sample_user_data, "is_active": True})
        mock_user_service.update_user_active_status.return_value = updated_user

        # Act
        response: Response = auth_client.patch("/users/me/status?is_active=true")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["is_active"] is True
        mock_user_service.update_user_active_status.assert_called_once_with(user_id=1, is_active=True)

    def test_deactivate_user_account_success(self, auth_client: TestClient, mock_user_service: Mock, sample_user_data: dict):
        """Test successful user account deactivation."""
        # Arrange
        updated_user = UserModel(**{**sample_user_data, "is_active": False})
        mock_user_service.update_user_active_status.return_value = updated_user

        # Act
        response: Response = auth_client.patch("/users/me/status?is_active=false")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["is_active"] is False
        mock_user_service.update_user_active_status.assert_called_once_with(user_id=1, is_active=False)

    def test_reactivate_user_missing_query_param(self, auth_client: TestClient):
        """Test missing is_active query parameter."""
        # Act
        response: Response = auth_client.patch("/users/me/status")

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestUpdateUserProfile(TestUserEndpoints):
    """Tests for PATCH /users/me endpoint."""

    async def test_update_user_profile_success(self, auth_client: TestClient, mock_user_service: Mock, sample_user_data: dict):
        """Test successful user profile update."""
        # Arrange
        update_data: dict[str, str] = {"name": "Updated Name", "last_name": "Updated Lastname"}
        updated_user = UserModel(**{**sample_user_data, **update_data})
        mock_user_service.update_user.return_value = updated_user

        # Act
        response: Response = auth_client.patch("/users/me", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["name"] == "Updated Name"
        assert response_data["last_name"] == "Updated Lastname"
        mock_user_service.update_user.assert_called_once_with(user_id=1, user_data=update_data)

    def test_update_user_profile_partial_update(self, auth_client: TestClient, mock_user_service: Mock, sample_user_data: dict):
        """Test partial user profile update."""
        # Arrange
        update_data: dict[str, str] = {"name": "Only Name Updated"}
        updated_user = UserModel(**{**sample_user_data, **update_data})
        mock_user_service.update_user.return_value = updated_user

        # Act
        response: Response = auth_client.patch("/users/me", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data: dict = response.json()
        assert response_data["name"] == "Only Name Updated"
        assert response_data["last_name"] == "User"  # Should remain unchanged
        mock_user_service.update_user.assert_called_once_with(user_id=1, user_data=update_data)

    def test_update_user_profile_user_not_found(self, auth_client: TestClient, mock_user_service: Mock):
        """Test user profile update when user not found."""
        # Arrange
        update_data: dict[str, str] = {"name": "Updated Name"}
        mock_user_service.update_user.side_effect = NotFoundException(identifier=1, resource_type="Users")

        # Act
        response: Response = auth_client.patch("/users/me", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_user_profile_invalid_data(self, auth_client: TestClient):
        """Test user profile update with invalid data."""
        # Arrange
        invalid_data: dict[str, str] = {"email": "invalid-email"}  # Pydantic model should reject this

        # Act
        response: Response = auth_client.patch("/users/me", json=invalid_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestUploadProfilePicture(TestUserEndpoints):
    """Tests for POST /users/me/profile-picture endpoint."""

    @patch('app.users.routes.user_routes.validate_uploaded_image')
    async def test_upload_profile_picture_success(self, mock_validator, auth_client, mock_user_service, mock_file_service, sample_user_data):
        """Test successful profile picture upload."""
        # Arrange
        file_content = b"fake image content"
        file_url = "https://example.com/profile-pictures/profile-picture.jpg"
        updated_user_model = UserModel(**{**sample_user_data, "profile_picture": file_url})

        mock_validator.return_value = None
        mock_file_service.upload_file.return_value = file_url
        mock_user_service.update_profile_picture.return_value = updated_user_model

        # Act
        with BytesIO(file_content) as file_data:
            response = auth_client.post(
                "/users/me/profile-picture",
                files={"file": ("test.jpg", file_data, "image/jpeg")}
            )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["profile_picture"] == file_url
        mock_validator.assert_called_once()
        mock_file_service.upload_file.assert_called_once()
        mock_user_service.update_profile_picture.assert_called_once_with(user_id=1, picture_url=file_url)

    @patch('app.users.routes.user_routes.validate_uploaded_image')
    async def test_upload_profile_picture_validation_error(self, mock_validator, auth_client: TestClient):
        """Test profile picture upload with validation error."""
        # Arrange
        mock_validator.side_effect = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")

        # Act
        with BytesIO(b"invalid file content") as file_data:
            response = auth_client.post(
                "/users/me/profile-picture",
                files={"file": ("test.txt", file_data, "text/plain")}
            )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid file type" in response.json()["detail"]

    async def test_upload_profile_picture_no_file(self, auth_client: TestClient):
        """Test profile picture upload without file."""
        # Act
        response = auth_client.post("/users/me/profile-picture")

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch('app.users.routes.user_routes.validate_uploaded_image')
    async def test_upload_profile_picture_no_content_type(self, mock_validator, auth_client: TestClient):
        """Test that uploading a profile picture without a content type results in a 400 Bad Request error."""
        # Arrange
        mock_validator.side_effect = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File content type is required")

        # Act
        with BytesIO(b"fake image content") as file_data:
            response = auth_client.post(
                "/users/me/profile-picture",
                files={"file": ("test.jpg", file_data, None)}
            )

        # Assert
        mock_validator.assert_called_once()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "File content type is required" in response.json()["detail"]


class TestUserEndpointsIntegration(TestUserEndpoints):
    """Integration tests for user endpoints."""

    def test_user_lifecycle_operations(self, auth_client: TestClient, mock_user_service: Mock, sample_user_data: dict):
        """Test a complete user lifecycle: get -> update -> deactivate -> reactivate."""
        # Arrange
        original_user = UserModel(**sample_user_data)
        updated_user = UserModel(**{**sample_user_data, "name": "Updated Name"})
        deactivated_user = UserModel(**{**sample_user_data, "name": "Updated Name", "is_active": False})
        reactivated_user = UserModel(**{**sample_user_data, "name": "Updated Name", "is_active": True})

        mock_user_service.get_user_by_id.return_value = original_user
        mock_user_service.update_user.return_value = updated_user
        mock_user_service.update_user_active_status.side_effect = [deactivated_user, reactivated_user]

        # Act & Assert - 1. Get current user
        response = auth_client.get("/users/me")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Test"

        # Act & Assert - 2. Update user profile
        response = auth_client.patch("/users/me", json={"name": "Updated Name"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Updated Name"

        # Act & Assert - 3. Deactivate user
        response = auth_client.patch("/users/me/status?is_active=false")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["is_active"] is False

        # Act & Assert - 4. Reactivate user
        response = auth_client.patch("/users/me/status?is_active=true")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["is_active"] is True


class TestUserEndpointsPerformance(TestUserEndpoints):
    """Performance tests for user endpoints."""

    def test_get_all_users_large_dataset(self, auth_client: TestClient, mock_user_service: Mock, sample_user_data: dict):
        """Test performance with large dataset."""
        # Arrange
        large_user_list: List[UserModel] = [UserModel(**{**sample_user_data, "id": i, "username": f"user{i}"}) for i in range(1000)]
        mock_user_service.get_all_users.return_value = large_user_list

        # Act
        import time
        start_time: float = time.time()
        response: Response = auth_client.get("/users?limit=1000")
        end_time: float = time.time()

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1000
        assert (end_time - start_time) < 5.0, "Request took too long"