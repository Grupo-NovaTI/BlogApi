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
"""

from typing import Annotated
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from unittest.mock import Mock, AsyncMock, patch
from io import BytesIO
from datetime import datetime, timezone

# Assuming you have a main FastAPI app instance
from app.main import app
from app.users.models.user_model import UserModel

# Import the actual dependency provider function
from app.core.dependencies.dependencies import _provide_user_services, provide_user_id_from_token, provide_token_payload, _provide_file_storage_service # Adjust import if needed


class TestUserEndpoints:
    """Test class for user endpoints."""
    
    @pytest.fixture
    def mock_user_service(self):
        """Mock user service dependency using a standard Mock."""
        return Mock()
    
    @pytest.fixture
    def mock_file_service(self):
        """Mock file storage service dependency."""
        return AsyncMock()
    
    @pytest.fixture
    def mock_user_repository(self):
        """Mock user repository dependency."""
        return Mock()
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return {
            "id": 1, "username": "testuser", "email": "test@example.com",
            "name": "Test", "last_name": "User", "is_active": True, "role": "user",
            "profile_picture": "https://example.com/default.png",
            "created_at": datetime.now(tz=timezone.utc),
            "updated_at": datetime.now(tz=timezone.utc), "hashed_password": "fake_hash"
        }

    @pytest.fixture(scope="function")
    def client(self, mock_user_service, mock_file_service):
        """Create a test client with dependency overrides."""
        
        # Override the dependency provider function with our mock
        app.dependency_overrides[_provide_user_services] = lambda: mock_user_service
        
        # Override other dependencies needed for the tests
        app.dependency_overrides[_provide_file_storage_service] = lambda: mock_file_service
        app.dependency_overrides[provide_user_id_from_token] = lambda: 1  # Mock current user ID
        app.dependency_overrides[provide_token_payload] = lambda: {"user_id": 1, "role": "user"}
        
        yield TestClient(app, base_url="http://testserver/api/v1")  # Use a test server base URL
        
        # Clean up overrides after tests are done
        app.dependency_overrides.clear()

@pytest.mark.asyncio
class TestGetCurrentUser(TestUserEndpoints):
    """Tests for GET /users/me endpoint."""
    
    # The @pytest.mark.asyncio decorator is not needed if you set `asyncio_mode = anyio`
    
    async def test_get_current_user_success(self, client, mock_user_service, sample_user_data):
        """Test successful retrieval of current user."""
        # Arrange
        user_model = UserModel(**sample_user_data)
        mock_user_service.reset_mock()
        mock_user_service.get_user_by_id.return_value = user_model

        # Act
        response = client.get("/users/me")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert response_data["username"] == "testuser"
        assert response_data["email"] == "test@example.com"
        
        mock_user_service.get_user_by_id.assert_called_once_with(user_id=1)
    
    
    async def test_get_current_user_not_found(self, client, mock_user_service):
        """Test current user not found."""
        # Arrange
        from app.utils.errors.exceptions import NotFoundException
        mock_user_service.get_user_by_id.side_effect = NotFoundException(
            identifier=1, resource_type="Users"
        )
        
        # Act
        response = client.get("/users/me")
        print(f"client base URL: {client.base_url}")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetUserById(TestUserEndpoints):
    """Tests for GET /users/{user_id} endpoint."""
    
    def test_get_user_by_id_success(self, client, mock_user_service, mock_user_repository, sample_user_data):
        """Test successful retrieval of user by ID."""
        # Arrange
        user_model = UserModel(**sample_user_data)
        mock_user_service.get_user_by_id.return_value = user_model
        
        # Act
        response = client.get("/users/1")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == 1
        assert response_data["username"] == "testuser"
        mock_user_service.get_user_by_id.assert_called_with(user_id=1)
    
    def test_get_user_by_id_not_found(self, client, mock_user_service):
        """Test user not found by ID."""
        # Arrange
        from app.utils.errors.exceptions import NotFoundException
        mock_user_service.get_user_by_id.side_effect = NotFoundException(
            identifier=999, resource_type="Users"
        )
        
        # Act
        response = client.get("/users/999")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_user_by_id_invalid_path_param(self, client):
        """Test invalid user ID path parameter."""
        # Act
        response = client.get("/users/0")  # Invalid: below minimum value
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_user_by_id_path_param_too_large(self, client):
        """Test user ID path parameter exceeds maximum."""
        # Act
        response = client.get("/users/1000001")  # Invalid: above maximum value
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetAllUsers(TestUserEndpoints):
    """Tests for GET /users endpoint."""
    
    def test_get_all_users_success(self, client, mock_user_service, sample_user_data):
        """Test successful retrieval of all users."""
        # Arrange
        user1 = UserModel(**sample_user_data)
        user2_data = {**sample_user_data, "id": 2, "username": "user2", "email": "user2@example.com"}
        user2 = UserModel(**user2_data)
        users_list = [user1, user2]
        mock_user_service.get_all_users.return_value = users_list
        
        # Act
        response = client.get("/users")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data) == 2
        assert response_data[0]["username"] == "testuser"
        assert response_data[1]["username"] == "user2"
        mock_user_service.get_all_users.assert_called_once_with(offset=0, limit=10)
    
    def test_get_all_users_with_pagination(self, client, mock_user_service, sample_user_data):
        """Test users retrieval with pagination parameters."""
        # Arrange
        user1 = UserModel(**sample_user_data)
        users_list = [user1]
        mock_user_service.get_all_users.return_value = users_list
        
        # Act
        response = client.get("/users?limit=5&offset=10")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        mock_user_service.get_all_users.assert_called_once_with(offset=10, limit=5)
    
    def test_get_all_users_invalid_limit(self, client):
        """Test invalid limit parameter."""
        # Act
        response = client.get("/users?limit=0")  # Invalid: below minimum
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_all_users_invalid_offset(self, client):
        """Test invalid offset parameter."""
        # Act
        response = client.get("/users?offset=-1")  # Invalid: below minimum
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteCurrentUser(TestUserEndpoints):
    """Tests for DELETE /users/me endpoint."""
    
    def test_delete_current_user_success(self, client, mock_user_service):
        """Test successful deletion of current user."""
        # Arrange
        mock_user_service.delete_user_by_id.return_value = None
        
        # Act
        response = client.delete("/users/me")
        
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_user_service.delete_user_by_id.assert_called_once_with(user_id=1)
    
    def test_delete_current_user_not_found(self, client, mock_user_service):
        """Test deletion of non-existent current user."""
        # Arrange
        from app.utils.errors.exceptions import NotFoundException
        mock_user_service.delete_user_by_id.side_effect = NotFoundException(
            identifier=1, resource_type="Users"
        )
        
        # Act
        response = client.delete("/users/me")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestReactivateUserAccount(TestUserEndpoints):
    """Tests for PATCH /users/me/status endpoint."""
    
    def test_reactivate_user_account_success(self, client, mock_user_service, sample_user_data):
        """Test successful user account reactivation."""
        # Arrange
        updated_user_data = {**sample_user_data, "is_active": True}
        updated_user = UserModel(**updated_user_data)
        mock_user_service.update_user_active_status.return_value = updated_user
        
        # Act
        response = client.patch("/users/me/status?is_active=true")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["is_active"] is True
        mock_user_service.update_user_active_status.assert_called_once_with(
            user_id=1, is_active=True
        )
    
    def test_deactivate_user_account_success(self, client, mock_user_service, sample_user_data):
        """Test successful user account deactivation."""
        # Arrange
        updated_user_data = {**sample_user_data, "is_active": False}
        updated_user = UserModel(**updated_user_data)
        mock_user_service.update_user_active_status.return_value = updated_user
        
        # Act
        response = client.patch("/users/me/status?is_active=false")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["is_active"] is False
        mock_user_service.update_user_active_status.assert_called_once_with(
            user_id=1, is_active=False
        )
    
    def test_reactivate_user_missing_query_param(self, client):
        """Test missing is_active query parameter."""
        # Act
        response = client.patch("/users/me/status")
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
class TestUpdateUserProfile(TestUserEndpoints):
    """Tests for PATCH /users/me endpoint."""
    
    async def test_update_user_profile_success(self, client, mock_user_service, sample_user_data):
        """Test successful user profile update."""
        # Arrange
        update_data = {"name": "Updated Name", "last_name": "Updated Lastname"}
        updated_user_data = {**sample_user_data, **update_data}
        updated_user = UserModel(**updated_user_data)
        mock_user_service.update_user.return_value = updated_user
        
        # Act
        response = client.patch("/users/me", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["name"] == "Updated Name"
        assert response_data["last_name"] == "Updated Lastname"
        mock_user_service.update_user.assert_called_once_with(
            user_id=1, user_data=update_data
        )
    
    def test_update_user_profile_partial_update(self, client, mock_user_service, sample_user_data):
        """Test partial user profile update."""
        # Arrange
        update_data = {"name": "Only Name Updated"}
        updated_user_data = {**sample_user_data, **update_data}
        updated_user = UserModel(**updated_user_data)
        mock_user_service.update_user.return_value = updated_user
        
        # Act
        response = client.patch("/users/me", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["name"] == "Only Name Updated"
        assert response_data["last_name"] == "User"  # Should remain unchanged
        mock_user_service.update_user.assert_called_once_with(
            user_id=1, user_data=update_data
        )
    
    def test_update_user_profile_user_not_found(self, client, mock_user_service):
        """Test user profile update when user not found."""
        # Arrange
        from app.utils.errors.exceptions import NotFoundException
        update_data = {"name": "Updated Name"}
        mock_user_service.update_user.side_effect = NotFoundException(
            identifier=1, resource_type="Users"
        )
        
        # Act
        response = client.patch("/users/me", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    
    def test_update_user_profile_invalid_data(self, client):
        """Test user profile update with invalid data."""
        # Arrange
        invalid_data = {"email": "invalid-email"}  # Assuming email validation exists
        
        # Act
        response = client.patch("/users/me", json=invalid_data)
        
        # Assert might be 422 for validation error or 400 for bad request
        assert response.status_code in [status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_400_BAD_REQUEST]

@pytest.mark.asyncio
class TestUploadProfilePicture(TestUserEndpoints):
    """Tests for POST /users/me/profile-picture endpoint."""
    
    # CORRECTION:
    # - Removed redundant @patch decorators for dependencies.
    # - Kept the @patch for `validate_uploaded_image` as it's a regular function, not a dependency.
    # - Changed the function signature to use the mocks from the fixture (mock_user_service, mock_file_service).
    # - Updated the test logic to use these fixture mocks.
    @patch('app.users.routes.user_routes.validate_uploaded_image')
    async def test_upload_profile_picture_success(self, mock_validator, client, mock_user_service,
                                          mock_file_service, sample_user_data):
        """Test successful profile picture upload."""
        # Arrange
        file_content = b"fake image content"
        file_url = "https://example.com/profile-pictures/profile-picture.jpg"
        
        # This is the model that the service layer returns
        updated_user_model = UserModel(**{**sample_user_data, "profile_picture": file_url})
        
        # Configure the mocks provided by the fixture
        mock_validator.return_value = None # The validator just needs to not raise an exception
        mock_file_service.upload_file.return_value = file_url
        mock_user_service.update_profile_picture.return_value = updated_user_model
        
        # Act
        with BytesIO(file_content) as file_data:
            response = client.post(
                "/users/me/profile-picture",
                files={"file": ("test.jpg", file_data, "image/jpeg")}
            )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["profile_picture"] == file_url
        
        # Assert that the correct mocks were called
        mock_validator.assert_called_once()
        mock_file_service.upload_file.assert_called_once()
        mock_user_service.update_profile_picture.assert_called_once_with(
            user_id=1, picture_url=file_url
        )
    
    # CORRECTION: Same logic applied here.
    @patch('app.users.routes.user_routes.validate_uploaded_image')
    async def test_upload_profile_picture_validation_error(self, mock_validator, client):
        """Test profile picture upload with validation error."""
        # Arrange
        from fastapi import HTTPException
        # The validator is not a dependency, so patching it directly is correct.
        mock_validator.side_effect = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type"
        )
        
        # Act
        file_content = b"invalid file content"
        with BytesIO(file_content) as file_data:
            response = client.post(
                "/users/me/profile-picture",
                files={"file": ("test.txt", file_data, "text/plain")}
            )
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid file type" in response.json()["detail"]

    async def test_upload_profile_picture_no_file(self, client):
        """Test profile picture upload without file."""
        # Act
        response = client.post("/users/me/profile-picture")
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch('app.users.routes.user_routes.validate_uploaded_image')
    async def test_upload_profile_picture_no_content_type(self, mock_validator, client):
        """
        Test that uploading a profile picture without a content type
        results in a 400 Bad Request error.
        """
        # Arrange:
        expected_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content type is required"
        )
        mock_validator.side_effect = expected_exception


        with BytesIO(b"fake image content") as file_data:
            # Act
            response = client.post(
                "/users/me/profile-picture",
                files={"file": ("test.jpg", file_data, None)}
                )
            print("Response content:", response.content)
            

        # Assert
        mock_validator.assert_called_once()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "File content type is required" in response.json()["detail"]
    
# Integration test class for testing multiple endpoints together
class TestUserEndpointsIntegration(TestUserEndpoints):
    """Integration tests for user endpoints."""
    
    # CORRECTION: Removed redundant @patch decorators and using fixture mocks instead.
    def test_user_lifecycle_operations(self, client, mock_user_service, sample_user_data):
        """Test a complete user lifecycle: get -> update -> deactivate -> reactivate."""
        # Arrange
        # We need to return UserModel or a compatible object from the service layer
        original_user = UserModel(**sample_user_data)
        updated_user = UserModel(**{**sample_user_data, "name": "Updated Name"})
        deactivated_user = UserModel(**{**sample_user_data, "name": "Updated Name", "is_active": False})
        reactivated_user = UserModel(**{**sample_user_data, "name": "Updated Name", "is_active": True})

        # Configure the mock service for the sequence of calls
        mock_user_service.get_user_by_id.return_value = original_user
        mock_user_service.update_user.return_value = updated_user
        mock_user_service.update_user_active_status.side_effect = [
            deactivated_user, reactivated_user
        ]
        
        # Act & Assert - Get current user
        response = client.get("/users/me")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Test"
        
        # Act & Assert - Update user profile
        response = client.patch("/users/me", json={"name": "Updated Name"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Updated Name"
        
        # Act & Assert - Deactivate user
        response = client.patch("/users/me/status?is_active=false")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["is_active"] is False
        
        # Act & Assert - Reactivate user
        response = client.patch("/users/me/status?is_active=true")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["is_active"] is True


# Performance test class (basic examples)
class TestUserEndpointsPerformance(TestUserEndpoints):
    """Performance tests for user endpoints."""
    
    # CORRECTION: Removed redundant @patch decorator
    def test_get_all_users_large_dataset(self, client, mock_user_service, sample_user_data):
        """Test performance with large dataset."""
        # Arrange - Create large user list
        # The service layer returns model objects
        large_user_list = [
            UserModel(**{**sample_user_data, "id": i, "username": f"user{i}"})
            for i in range(1000)
        ]
        mock_user_service.get_all_users.return_value = large_user_list
        
        # Act
        import time
        start_time = time.time()
        response = client.get("/users?limit=1000")
        end_time = time.time()
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1000
        # Basic performance assertion - adjust threshold as needed
        assert (end_time - start_time) < 5.0  # Should complete within 5 seconds


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])