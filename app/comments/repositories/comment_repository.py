"""
Repository layer for comment management.

This module defines the CommentRepository class, which provides CRUD operations and queries
for comment entities in the database.
"""
from typing import Any, List, Optional
from sqlalchemy.orm import Session

from app.comments.models.comment_model import CommentModel


class CommentRepository:
    """
    Repository for managing comments.
    """

    def __init__(self, db_session: Session) -> None:
        """
        Initialize the CommentRepository with a database session.

        Args:
            db_session (Session): SQLAlchemy session for database operations.
        """
        self._db_session: Session = db_session

    def create_comment(self, comment: CommentModel) -> CommentModel:
        """
        Create a new comment.

        Args:
            comment (CommentModel): The comment object to create.

        Returns:
            CommentModel: The created comment object.
        """
        self._db_session.add(instance=comment)
        self._db_session.flush()
        return comment

    def get_all_comments_by_blog(self, blog_id: int) -> List[CommentModel]:
        """
        Get all comments for a specific blog by its ID.

        Args:
            blog_id (int): The unique identifier of the blog.

        Returns:
            List[CommentModel]: List of comments for the blog.
        """
        return self._db_session.query(CommentModel).filter(CommentModel.blog_id == blog_id).all()

    def get_all_comments_by_user(self, user_id: int) -> List[CommentModel]:
        """
        Get all comments made by a specific user by their ID.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            List[CommentModel]: List of comments made by the user.
        """
        return self._db_session.query(CommentModel).filter(CommentModel.user_id == user_id).all()

    def get_comment_by_id(self, comment_id: int) -> Optional[CommentModel]:
        """
        Get a comment by its ID.

        Args:
            comment_id (int): The unique identifier of the comment.

        Returns:
            Optional[CommentModel]: The comment object if found, otherwise None.
        """
        return self._db_session.get(entity=CommentModel, ident=comment_id)

    def update_comment(self, comment: CommentModel, content: dict[str, Any]) -> Optional[CommentModel]:
        """
        Update a comment's content by its ID.

        Args:
            comment (CommentModel): The comment object to update.
            content (dict[str, Any]): Dictionary of fields to update.

        Returns:
            Optional[CommentModel]: The updated comment object.
        """
        for key, value in content.items():
            setattr(comment, key, value)
        return comment

    def delete_comment(self, comment: CommentModel) -> None:
        """
        Delete a comment by its ID.

        Args:
            comment (CommentModel): The comment object to delete.
        """
        self._db_session.delete(instance=comment)
