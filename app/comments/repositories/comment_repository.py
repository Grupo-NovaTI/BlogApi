from typing import Any, List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.comments.models.comment_model import CommentModel


class CommentRepository:
    """Repository for managing comments."""

    def __init__(self, db_session: Session):
        self._db_session: Session = db_session

    def create_comment(self, comment: CommentModel) -> CommentModel:
        """Create a new comment."""
        self._db_session.add(instance=comment)
        self._db_session.flush()
        return comment

    def get_all_comments_by_blog(self, blog_id: int) -> List[CommentModel]:
        """Get all comments for a specific blog by its ID."""
        return self._db_session.query(CommentModel).filter(CommentModel.blog_id == blog_id).all()

    def get_all_comments_by_user(self, user_id: int) -> List[CommentModel]:
        """Get all comments made by a specific user by their ID."""
        return self._db_session.query(CommentModel).filter(CommentModel.user_id == user_id).all()

    def get_comment_by_id(self, comment_id: int) -> Optional[CommentModel]:
        """Get a comment by its ID."""
        return self._db_session.get(entity=CommentModel, ident=comment_id)

    def update_comment(self, comment : CommentModel, content: dict[str, Any]) -> Optional[CommentModel]:
        """Update a comment's content by its ID."""
        for key, value in content.items():
            setattr(comment, key, value)
        return comment


    def delete_comment(self, comment : CommentModel) -> None:
        """Delete a comment by its ID."""
        self._db_session.delete(instance=comment)
