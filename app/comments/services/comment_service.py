"""
Service layer for comment management.

This module defines the CommentService class, which provides business logic for comment operations
such as creation, retrieval, update, and deletion, using the CommentRepository.
"""

from typing import Any, Optional

from sqlalchemy.orm import Session

from app.comments.models.comment_model import CommentModel
from app.comments.repositories.comment_repository import CommentRepository
from app.utils.enums.operations import Operations
from app.utils.errors.exception_handlers import (handle_read_exceptions,
                                                 handle_service_transaction)
from app.utils.errors.exceptions import ForbiddenException, NotFoundException
from app.utils.errors.exceptions import \
    NotFoundException as CommentNotFoundException

_MODEL_NAME = "Comment"


class CommentService:
    """
    Service for managing comments.
    """

    def __init__(self, comment_repository: CommentRepository, db_session: Session) -> None:
        """
        Initialize the CommentService with a comment repository and database session.

        Args:
            comment_repository (CommentRepository): The comment repository instance.
            db_session (Session): SQLAlchemy session for database operations.
        """
        self._repository: CommentRepository = comment_repository
        self._db_session: Session = db_session

    def _get_and_authorize_comment(self, comment_id: int, user_id: int) -> CommentModel:
        """
        Retrieves a comment by ID and verifies that the user is the owner.

        Args:
            comment_id (int): The unique identifier of the comment.
            user_id (int): The unique identifier of the user.

        Returns:
            CommentModel: The comment object if found and authorized.

        Raises:
            CommentNotFoundException: If the comment does not exist.
            ForbiddenException: If the user is not the owner of the comment.
        """
        comment: Optional[CommentModel] = self._repository.get_comment_by_id(
            comment_id=comment_id)
        if not comment:
            raise CommentNotFoundException(
                identifier=comment_id, resource_type=_MODEL_NAME)
        if comment.user_id != user_id:  # type: ignore
            raise ForbiddenException(
                details=f"User {user_id} lacks permission for comment {comment_id}.")
        return comment

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.CREATE
    )
    def create_comment(self, comment_data: dict[str, Any], user_id: int) -> CommentModel:
        """
        Create a new comment in the repository.

        Args:
            comment (dict[str, Any]): Data for the new comment.
            user_id (int): The unique identifier of the user creating the comment.

        Returns:
            CommentModel: The created comment.
        """
        comment_model = CommentModel(**comment_data, user_id=user_id)
        return self._repository.create_comment(comment=comment_model)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH_BY
    )
    def get_comments_by_blog_id(self, blog_id: int) -> list[CommentModel]:
        """
        Retrieve all comments for a specific blog by its ID.

        Args:
            blog_id (int): The unique identifier of the blog.

        Returns:
            list[CommentModel]: List of comments for the blog.
        """
        return self._repository.get_all_comments_by_blog(blog_id=blog_id)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH
    )
    def get_comments_by_user(self, user_id: int) -> list[CommentModel]:
        """
        Retrieve all comments made by a specific user by their ID.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            list[CommentModel]: List of comments made by the user.
        """
        return self._repository.get_all_comments_by_user(user_id=user_id)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH_BY
    )
    def get_comment_by_id(self, comment_id: int) -> CommentModel:
        """
        Retrieve a comment by its ID.

        Args:
            comment_id (int): The unique identifier of the comment.

        Returns:
            Optional[CommentModel]: The comment object if found, otherwise None.
        """
        comment: Optional[CommentModel] = self._repository.get_comment_by_id(
            comment_id=comment_id)
        if comment is None:
            raise NotFoundException(
                resource_type=_MODEL_NAME,
                identifier=comment_id
            )
        return comment

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.UPDATE
    )
    def update_comment(self, comment_id: int, content: str, user_id: int) -> CommentModel:
        """
        Update a comment's content by its ID.

        Args:
            comment_id (int): The unique identifier of the comment to update.
            content (str): The new content for the comment.
            user_id (int): The unique identifier of the user updating the comment.

        Returns:
            CommentModel: The updated comment.
        """
        comment_to_update: CommentModel = self._get_and_authorize_comment(
            comment_id=comment_id, user_id=user_id)
        updated_comment: Optional[CommentModel] = self._repository.update_comment(
            comment=comment_to_update, content={"content": content})

        return updated_comment

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.DELETE
    )
    def delete_comment_for_admin(self, comment_id: int) -> None:
        """
        Delete a comment by its ID (admin only).

        Args:
            comment_id (int): The unique identifier of the comment to delete.
        """
        comment_to_delete: Optional[CommentModel] = self._repository.get_comment_by_id(
            comment_id=comment_id)
        if not comment_to_delete:
            raise CommentNotFoundException(
                identifier=comment_id, resource_type=_MODEL_NAME)
        self._repository.delete_comment(comment=comment_to_delete)

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.DELETE
    )
    def delete_comment_for_user(self, comment_id: int, user_id: int) -> None:
        """
        Delete a comment by its ID and author ID (user only).

        Args:
            comment_id (int): The unique identifier of the comment to delete.
            user_id (int): The unique identifier of the user deleting the comment.
        """
        comment_to_delete: CommentModel = self._get_and_authorize_comment(
            comment_id=comment_id, user_id=user_id)
        self._repository.delete_comment(
            comment=comment_to_delete)
