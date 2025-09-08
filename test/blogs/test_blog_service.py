"""
Unit tests for BlogService class.

This module contains comprehensive unit tests for the BlogService class,
testing all public methods with various scenarios including success cases,
error cases, and edge cases.
"""

from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

import pytest

from app.blog_tags.repositories.blog_tag_repository import BlogTagRepository
from app.blogs.models.blog_model import BlogModel
from app.blogs.repositories.blog_repository import BlogRepository
from app.blogs.services.blog_service import BlogService
from app.utils.errors.exceptions import (ForbiddenException,
                                         NotFoundException)
from test.utils.conftest import mock_db_session, sample_blog_data, sample_blog

# --- Pytest Fixtures ---

@pytest.fixture
def mock_blog_repository() -> MagicMock:
    """
    Fixture that creates a mock BlogRepository.
    """
    return MagicMock(spec=BlogRepository)


@pytest.fixture
def mock_blog_tag_repository() -> MagicMock:
    """
    Fixture that creates a mock BlogTagRepository.
    """
    return MagicMock(spec=BlogTagRepository)



@pytest.fixture
def blog_service(mock_blog_repository: MagicMock, mock_blog_tag_repository: MagicMock, mock_db_session: MagicMock) :
    """
    Fixture that creates a BlogService instance with mocked dependencies.
    """
    # Disable decorators for unit testing
    with patch('app.blogs.services.blog_service.handle_service_transaction', lambda **kwargs: lambda f: f), \
         patch('app.blogs.services.blog_service.handle_read_exceptions', lambda **kwargs: lambda f: f):
        yield BlogService(
            blog_repository=mock_blog_repository,
            blog_tag_repository=mock_blog_tag_repository,
            db_session=mock_db_session
        )


# --- Test Class ---

class TestBlogService:
    """Test suite for BlogService."""

    def test_get_all_blogs_success(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test successful retrieval of all blogs with pagination.
        """
        # Arrange
        expected_blogs: List[BlogModel] = [sample_blog]
        mock_blog_repository.get_all_blogs.return_value = expected_blogs

        # Act
        result: List[BlogModel] = blog_service.get_all_blogs(limit=10, offset=0)

        # Assert
        mock_blog_repository.get_all_blogs.assert_called_once_with(limit=10, offset=0)
        assert result == expected_blogs

    def test_get_blog_by_id_success(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test successful retrieval of a blog by ID.
        """
        # Arrange
        blog_id = 1
        mock_blog_repository.get_blog_by_id.return_value = sample_blog

        # Act
        result: Optional[BlogModel] = blog_service.get_blog_by_id(blog_id=blog_id)

        # Assert
        mock_blog_repository.get_blog_by_id.assert_called_once_with(blog_id=blog_id)
        assert result == sample_blog

    def test_get_blog_by_id_not_found(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock
    ) -> None:
        """
        Test that NotFoundException is raised when blog is not found.
        """
        # Arrange
        blog_id = 999
        mock_blog_repository.get_blog_by_id.return_value = None

        # Act & Assert
        with pytest.raises(expected_exception=NotFoundException):
            blog_service.get_blog_by_id(blog_id=blog_id)

        mock_blog_repository.get_blog_by_id.assert_called_once_with(blog_id=blog_id)

    def test_create_blog_success_with_tags(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        mock_blog_tag_repository: MagicMock,
        mock_db_session: MagicMock,
        sample_blog_data: Dict[str, Any]
    ) -> None:
        """
        Test successful blog creation with tags.
        """
        # Arrange
        user_id = 1
        created_blog = BlogModel(id=1, user_id=user_id, **{k: v for k, v in sample_blog_data.items() if k != 'tags'})
        mock_blog_repository.create_blog.return_value = created_blog

        # Act
        result: BlogModel = blog_service.create_blog(blog_data=sample_blog_data, user_id=user_id)

        # Assert
        mock_blog_repository.create_blog.assert_called_once()
        mock_blog_tag_repository.link_blog_tags.assert_called_once_with(
            blog_id=created_blog.id, tag_ids=[1, 2, 3]
        )
        mock_db_session.refresh.assert_called_once_with(created_blog)
        assert result == created_blog

    def test_create_blog_success_without_tags(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        mock_blog_tag_repository: MagicMock,
        mock_db_session: MagicMock
    ) -> None:
        """
        Test successful blog creation without tags.
        """
        # Arrange
        user_id = 1
        blog_data: Dict[str, str] = {"title": "Test Blog", "content": "Test content"}
        created_blog = BlogModel(id=1, user_id=user_id, **blog_data)
        mock_blog_repository.create_blog.return_value = created_blog

        # Act
        result: BlogModel = blog_service.create_blog(blog_data=blog_data, user_id=user_id)

        # Assert
        mock_blog_repository.create_blog.assert_called_once()
        mock_blog_tag_repository.link_blog_tags.assert_not_called()
        mock_db_session.refresh.assert_called_once_with(created_blog)
        assert result == created_blog

    def test_update_blog_success_with_tags(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        mock_blog_tag_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test successful blog update with tag management.
        """
        # Arrange
        blog_id = 1
        user_id = 1
        update_data: Dict[str, Any] = {"title": "Updated Title", "tags": [2, 3, 4]}

        # Mock existing blog with current tags
        sample_blog.tags = [MagicMock(id=1), MagicMock(id=2)]  # type: ignore
        mock_blog_repository.get_blog_by_id.return_value = sample_blog
        mock_blog_repository.update_blog.return_value = sample_blog

        # Act
        result: BlogModel = blog_service.update_blog(blog_data=update_data, blog_id=blog_id, user_id=user_id)

        # Assert
        mock_blog_repository.get_blog_by_id.assert_called_once_with(blog_id=blog_id)
        mock_blog_repository.update_blog.assert_called_once()
        
        # Check tag management: should add [3, 4] and remove [1]
        mock_blog_tag_repository.link_blog_tags.assert_called_once_with(blog_id, [3, 4])
        mock_blog_tag_repository.unlink_blog_tags_by_blog_id.assert_called_once_with(blog_id, [1])
        
        assert result == sample_blog

    def test_update_blog_unauthorized(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test that ForbiddenException is raised when user tries to update another user's blog.
        """
        # Arrange
        blog_id = 1
        user_id = 2  # Different user
        update_data = {"title": "Updated Title"}
        
        sample_blog.user_id = 1  # Blog belongs to user 1 # type: ignore
        mock_blog_repository.get_blog_by_id.return_value = sample_blog

        # Act & Assert
        with pytest.raises(expected_exception=ForbiddenException):
            blog_service.update_blog(blog_data=update_data, blog_id=blog_id, user_id=user_id)

    def test_delete_blog_for_user_success(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test successful blog deletion by authorized user.
        """
        # Arrange
        blog_id = 1
        user_id = 1
        sample_blog.user_id = user_id # type: ignore
        mock_blog_repository.get_blog_by_id.return_value = sample_blog

        # Act
        blog_service.delete_blog_for_user(blog_id=blog_id, user_id=user_id)

        # Assert
        mock_blog_repository.get_blog_by_id.assert_called_once_with(blog_id=blog_id)
        mock_blog_repository.delete_blog.assert_called_once_with(blog=sample_blog)

    def test_delete_blog_for_user_unauthorized(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test that ForbiddenException is raised when user tries to delete another user's blog.
        """
        # Arrange
        blog_id = 1
        user_id = 2  # Different user
        sample_blog.user_id = 1  # Blog belongs to user 1 # type: ignore
        mock_blog_repository.get_blog_by_id.return_value = sample_blog

        # Act & Assert
        with pytest.raises(expected_exception=ForbiddenException):
            blog_service.delete_blog_for_user(blog_id=blog_id, user_id=user_id)

        mock_blog_repository.delete_blog.assert_not_called()

    def test_delete_blog_for_admin_success(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test successful blog deletion by admin.
        """
        # Arrange
        blog_id = 1
        mock_blog_repository.get_blog_by_id.return_value = sample_blog

        # Act
        blog_service.delete_blog_for_admin(blog_id=blog_id)

        # Assert
        mock_blog_repository.get_blog_by_id.assert_called_once_with(blog_id=blog_id)
        mock_blog_repository.delete_blog.assert_called_once_with(blog=sample_blog)

    def test_delete_blog_for_admin_not_found(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock
    ) -> None:
        """
        Test that NotFoundException is raised when admin tries to delete non-existent blog.
        """
        # Arrange
        blog_id = 999
        mock_blog_repository.get_blog_by_id.return_value = None

        # Act & Assert
        with pytest.raises(expected_exception=NotFoundException):
            blog_service.delete_blog_for_admin(blog_id=blog_id)

        mock_blog_repository.delete_blog.assert_not_called()

    def test_get_public_blogs_success(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test successful retrieval of public blogs.
        """
        # Arrange
        expected_blogs: List[BlogModel] = [sample_blog]
        mock_blog_repository.get_public_blogs.return_value = expected_blogs

        # Act
        result: List[BlogModel] = blog_service.get_public_blogs(limit=5, offset=10)

        # Assert
        mock_blog_repository.get_public_blogs.assert_called_once_with(limit=5, offset=10)
        assert result == expected_blogs

    def test_get_blogs_by_user_success(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test successful retrieval of blogs by user.
        """
        # Arrange
        user_id = 1
        expected_blogs: List[BlogModel] = [sample_blog]
        mock_blog_repository.get_blogs_by_user.return_value = expected_blogs

        # Act
        result: List[BlogModel] = blog_service.get_blogs_by_user(user_id, limit=5, offset=10)

        # Assert
        mock_blog_repository.get_blogs_by_user.assert_called_once_with(
            user_id=user_id, limit=5, offset=10
        )
        assert result == expected_blogs

    def test_update_blog_image_success(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test successful blog image update.
        """
        # Arrange
        blog_id = 1
        user_id = 1
        image_url = "https://example.com/image.jpg"
        sample_blog.user_id = user_id # type: ignore
        mock_blog_repository.get_blog_by_id.return_value = sample_blog

        # Act
        result: BlogModel = blog_service.update_blog_image(blog_id, user_id, image_url)

        # Assert
        mock_blog_repository.get_blog_by_id.assert_called_once_with(blog_id=blog_id)
        mock_blog_repository.update_blog.assert_called_once_with(
            blog=sample_blog, blog_data={"image_url": image_url}
        )
        assert result == sample_blog

    def test_update_blog_image_unauthorized(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test that ForbiddenException is raised when user tries to update another user's blog image.
        """
        # Arrange
        blog_id = 1
        user_id = 2  # Different user
        image_url = "https://example.com/image.jpg"
        sample_blog.user_id = 1  # Blog belongs to user 1 # type: ignore
        mock_blog_repository.get_blog_by_id.return_value = sample_blog

        # Act & Assert
        with pytest.raises(expected_exception=ForbiddenException):
            blog_service.update_blog_image(blog_id=blog_id, user_id=user_id, blog_image_url=image_url)

        mock_blog_repository.update_blog.assert_not_called()

    def test_get_and_authorize_blog_not_found(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock
    ) -> None:
        """
        Test that NotFoundException is raised when blog is not found in authorization check.
        """
        # Arrange
        blog_id = 999
        user_id = 1
        mock_blog_repository.get_blog_by_id.return_value = None

        # Act & Assert
        with pytest.raises(expected_exception=NotFoundException):
            blog_service._get_and_authorize_blog(blog_id=blog_id, user_id=user_id)

    def test_get_and_authorize_blog_forbidden(
        self,
        blog_service: BlogService,
        mock_blog_repository: MagicMock,
        sample_blog: BlogModel
    ) -> None:
        """
        Test that ForbiddenException is raised when user is not authorized.
        """
        # Arrange
        blog_id = 1
        user_id = 2  # Different user
        sample_blog.user_id = 1  # Blog belongs to user 1 # type: ignore
        mock_blog_repository.get_blog_by_id.return_value = sample_blog

        # Act & Assert
        with pytest.raises(expected_exception=ForbiddenException):
            blog_service._get_and_authorize_blog(blog_id=blog_id, user_id=user_id)
