from typing import List, Optional

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

    def get_comment_by_id(self, id: int) -> Optional[CommentModel]:
        """Get a comment by its ID."""
        return self._db_session.get(entity=CommentModel, ident=id)

    def update_comment_content(self, comment_id: int, user_id: int, content: str) -> Optional[CommentModel]:
        """Update a comment's content by its ID."""
        rows_updated: int = self._db_session.query(CommentModel).filter(
            and_(CommentModel.id == comment_id,
                 CommentModel.user_id == user_id)
        ).update(values={"content": content})
        if rows_updated == 0:
            return None
        return self.get_comment_by_id(id=comment_id)

    def delete_comment(self, comment_id: int) -> bool:
        """Delete a comment by its ID."""
        comment: Optional[CommentModel] = self.get_comment_by_id(comment_id)
        if comment:
            self._db_session.delete(instance=comment)
            return True
        return False

    def delete_comment_by_user(self, user_id: int, comment_id: int) -> bool:
        """Delete a comment by its ID and user ID."""
        comment: Optional[CommentModel] = self._db_session.query(CommentModel).filter(
            and_(CommentModel.id == comment_id,
                 CommentModel.user_id == user_id)
        ).first()
        if comment:
            self._db_session.delete(instance=comment)
            return True
        return False
