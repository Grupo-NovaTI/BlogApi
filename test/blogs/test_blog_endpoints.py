from typing import Any, List
from httpx import Response
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from unittest.mock import Mock, patch
from test.utils.conftest import auth_client, mock_blog_service, sample_blog_data, sample_user_data, mock_user_service, mock_file_service
from app.utils.errors.exceptions import NotFoundException
from datetime import datetime, timezone

class TestBlogEndpoints:
    """Unit tests for blog-related API endpoints."""
    pass

@pytest.mark.asyncio
class TestGetBlogs:
    """Tests for the GET /blogs endpoint."""

    async def test_get_blogs_success(self, auth_client: TestClient, mock_blog_service: Mock, sample_blog_data: dict[str, Any], sample_user_data: dict[str, Any]):
        """Test retrieving a list of blogs successfully."""
        # Arrange - Create response data as plain dictionaries (not SQLAlchemy models)
        user_response = {
            "id": 1,
            "username": sample_user_data["username"],
            "email": sample_user_data["email"],
            "name": sample_user_data["name"],
            "is_active": sample_user_data.get("is_active", True),
            "role": sample_user_data.get("role", "user"),
            "last_name": sample_user_data["last_name"],
            "created_at": sample_user_data["created_at"].isoformat(),
            "updated_at": sample_user_data["created_at"].isoformat()
        }
        
        blog_response_data = {
            "id": 1,
            "title": sample_blog_data["title"],
            "content": sample_blog_data["content"],
            "is_published": sample_blog_data["is_published"],
            "image_url": sample_blog_data["image_url"],
            "user_id": 1,
            "user": user_response,
            "tags": [],
            "comments": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Mock the service to return plain dictionaries or response schemas
        mock_blog_service.get_all_blogs.return_value = [blog_response_data]
        
        # Act
        response: Response = auth_client.get("/blogs")
        
        # Debug output
        if response.status_code != 200:
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert len(response_data) == 1
        assert response_data[0]["title"] == sample_blog_data["title"]
        mock_blog_service.get_all_blogs.assert_called_once_with(offset=0, limit=10)

    async def test_get_blogs_empty(self, auth_client: TestClient, mock_blog_service: Mock):
        """Test retrieving an empty list of blogs."""
        # Arrange
        mock_blog_service.get_all_blogs.return_value = []

        # Act
        response: Response = auth_client.get("/blogs")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
        mock_blog_service.get_all_blogs.assert_called_once_with(offset=0, limit=10)

@pytest.mark.asyncio
class TestGetBlogById:
    """Tests for the GET /blogs/{blog_id} endpoint."""

    async def test_get_blog_by_id_success(self, auth_client: TestClient, mock_blog_service: Mock, sample_blog_data: dict[str, Any], sample_user_data: dict[str, Any]):
        """Test retrieving a specific blog by ID successfully."""
        # Arrange
        blog_id = 1
        
        user_response = {
            "id": 1,
            "username": sample_user_data["username"],
            "email": sample_user_data["email"],
            "name": sample_user_data["name"],
            "is_active": sample_user_data.get("is_active", True),
            "role": sample_user_data.get("role", "user"),
            "last_name": sample_user_data["last_name"],
            "created_at": sample_user_data["created_at"].isoformat(),
            "updated_at": sample_user_data["created_at"].isoformat()
        }
        
        blog_response = {
            "id": blog_id,
            "title": sample_blog_data["title"],
            "content": sample_blog_data["content"],
            "is_published": sample_blog_data["is_published"],
            "image_url": sample_blog_data["image_url"],
            "user_id": 1,
            "user": user_response,
            "tags": [],
            "comments": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        mock_blog_service.get_blog_by_id.return_value = blog_response

        # Act
        response: Response = auth_client.get(f"/blogs/{blog_id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == blog_id
        assert response_data["title"] == sample_blog_data["title"]
        mock_blog_service.get_blog_by_id.assert_called_once_with(blog_id=blog_id)

    async def test_get_blog_by_id_not_found(self, auth_client: TestClient, mock_blog_service: Mock):
        """Test retrieving a non-existent blog returns 404."""
        # Arrange
        blog_id = 999
        mock_blog_service.get_blog_by_id.side_effect = NotFoundException(
            identifier=blog_id, 
            resource_type="Blog"
        )

        # Act
        response: Response = auth_client.get(f"/blogs/{blog_id}")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        mock_blog_service.get_blog_by_id.assert_called_once_with(blog_id=blog_id)

@pytest.mark.asyncio
class TestCreateBlog:
    """Tests for the POST /blogs endpoint."""

    async def test_create_blog_success(self, auth_client: TestClient, mock_blog_service: Mock, sample_blog_data: dict[str, Any], sample_user_data: dict[str, Any]):
        """Test creating a new blog successfully."""
        # Arrange
        blog_data = {k: v for k, v in sample_blog_data.items() if k not in ['created_at', 'updated_at']}
        
        user_response = {
            "id": 1,
            "username": sample_user_data["username"],
            "email": sample_user_data["email"],
            "name": sample_user_data["name"],
            "is_active": sample_user_data.get("is_active", True),
            "role": sample_user_data.get("role", "user"),
            "last_name": sample_user_data["last_name"],
            "created_at": sample_user_data["created_at"].isoformat(),
            "updated_at": sample_user_data["created_at"].isoformat()
        }
        
        created_blog_response = {
            "id": 1,
            "user_id": 1,
            "user": user_response,
            "tags": [],
            "comments": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            **blog_data
        }
        
        mock_blog_service.create_blog.return_value = created_blog_response

        # Act
        response: Response = auth_client.post("/blogs", json=blog_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["title"] == blog_data["title"]
        assert response_data["content"] == blog_data["content"]
        mock_blog_service.create_blog.assert_called_once()

    async def test_create_blog_validation_error(self, auth_client: TestClient, mock_blog_service: Mock):
        """Test creating a blog with invalid data returns 422."""
        # Arrange - Invalid data (missing required fields)
        invalid_data = {"title": ""}  # Empty title

        # Act
        response: Response = auth_client.post("/blogs", json=invalid_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        mock_blog_service.create_blog.assert_not_called()

@pytest.mark.asyncio
class TestUpdateBlog:
    """Tests for the PATCH /blogs/{blog_id} endpoint."""

    async def test_update_blog_success(self, auth_client: TestClient, mock_blog_service: Mock, sample_blog_data: dict[str, Any], sample_user_data: dict[str, Any]):
        """Test updating a blog successfully."""
        # Arrange
        blog_id = 1
        update_data = {"title": "Updated Title", "content": "Updated Content"}
        
        user_response = {
            "id": 1,
            "username": sample_user_data["username"],
            "email": sample_user_data["email"],
            "name": sample_user_data["name"],
            "is_active": sample_user_data.get("is_active", True),
            "role": sample_user_data.get("role", "user"),
            "last_name": sample_user_data["last_name"],
            "created_at": sample_user_data["created_at"].isoformat(),
            "updated_at": sample_user_data["created_at"].isoformat()
        }
        
        blog_data = {k: v for k, v in sample_blog_data.items() if k not in ['created_at', 'updated_at']}
        updated_blog_response = {
            "id": blog_id,
            "user_id": 1,
            "user": user_response,
            "tags": [],
            "comments": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            **{**blog_data, **update_data}
        }
        
        mock_blog_service.update_blog.return_value = updated_blog_response

        # Act
        response: Response = auth_client.patch(f"/blogs/{blog_id}", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["title"] == update_data["title"]
        assert response_data["content"] == update_data["content"]
        mock_blog_service.update_blog.assert_called_once()

    async def test_update_blog_not_found(self, auth_client: TestClient, mock_blog_service: Mock):
        """Test updating a non-existent blog returns 404."""
        # Arrange
        blog_id = 999
        update_data = {"title": "Updated Title"}
        mock_blog_service.update_blog.side_effect = NotFoundException(
            identifier=blog_id,
            resource_type="Blog"
        )

        # Act
        response: Response = auth_client.patch(f"/blogs/{blog_id}", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        mock_blog_service.update_blog.assert_called_once()

@pytest.mark.asyncio
class TestDeleteBlog:
    """Tests for the DELETE /blogs/{blog_id} endpoint."""

    async def test_delete_blog_success(self, auth_client: TestClient, mock_blog_service: Mock):
        """Test deleting a blog successfully."""
        # Arrange
        blog_id = 1
        mock_blog_service.delete_blog_for_user.return_value = None

        # Act
        response: Response = auth_client.delete(f"/blogs/{blog_id}")

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_blog_service.delete_blog_for_user.assert_called_once()

    async def test_delete_blog_not_found(self, auth_client: TestClient, mock_blog_service: Mock):
        """Test deleting a non-existent blog returns 404."""
        # Arrange
        blog_id = 999
        mock_blog_service.delete_blog_for_user.side_effect = NotFoundException(
            identifier=blog_id,
            resource_type="Blog"
        )

        # Act
        response: Response = auth_client.delete(f"/blogs/{blog_id}")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        mock_blog_service.delete_blog_for_user.assert_called_once()