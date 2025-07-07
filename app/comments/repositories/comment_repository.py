from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.comments.models.comment_model import CommentModel
from app.utils.errors.exception_handlers import handle_database_exception
from app.utils.logger.application_logger import ApplicationLogger
from app.utils.enums.operations import Operations
_logger = ApplicationLogger(__name__)

_MODEL = "Comments"


class CommentRepository:
    """Repository for managing comments."""

    def __init__(self, db_session: Session):
        self._db_session: Session = db_session

    @handle_database_exception(
        model=_MODEL,
        operation=Operations.CREATE
    )
    def create_comment(self, comment: CommentModel) -> CommentModel:
        """Create a new comment."""
        self._db_session.add(instance=comment)
        self._db_session.commit()
        self._db_session.refresh(instance=comment)
        return comment

    @handle_database_exception(
        model=_MODEL,
        operation=Operations.FETCH
    )
    def get_all_comments_by_blog_id(self, blog_id: int) -> list[CommentModel]:
        """Get all comments for a specific blog by its ID."""
        return self._db_session.query(CommentModel).filter(CommentModel.blog_id == blog_id).all()

    @handle_database_exception(
        model=_MODEL,
        operation=Operations.FETCH
    )
    def get_all_comments_by_author_id(self, author_id: int) -> list[CommentModel]:
        """Get all comments made by a specific author by their ID."""
        return self._db_session.query(CommentModel).filter(CommentModel.author_id == author_id).all()

    def get_comment_by_id(self, comment_id: int) -> Optional[CommentModel]:
        """Get a comment by its ID."""
        return self._db_session.get(entity=CommentModel, ident=comment_id)

    @handle_database_exception(
        model=_MODEL,
        operation=Operations.UPDATE
    )
    def update_comment_content(self, comment_id: int, user_id: int, content: str) -> Optional[CommentModel]:
        """Update a comment's content by its ID."""
        rows_updated: int = self._db_session.query(CommentModel).filter(
            and_(CommentModel.id == comment_id,
                 CommentModel.author_id == user_id)
        ).update(values={"content": content})
        if rows_updated == 0:
            return None
        self._db_session.commit()
        return self.get_comment_by_id(comment_id=comment_id)

    @handle_database_exception(
        model=_MODEL,
        operation=Operations.DELETE
    )
    def delete_comment(self, comment_id: int) -> bool:
        """Delete a comment by its ID."""
        comment: Optional[CommentModel] = self.get_comment_by_id(comment_id)
        if comment:
            self._db_session.delete(instance=comment)
            self._db_session.commit()
            return True
        return False

    @handle_database_exception(
        model=_MODEL,
        operation=Operations.DELETE
    )
    def delete_comment_by_author(self, author_id: int, comment_id: int) -> bool:
        """Delete a comment by its ID and user ID."""
        comment: Optional[CommentModel] = self._db_session.query(CommentModel).filter(
            and_(CommentModel.id == comment_id,
                 CommentModel.author_id == author_id)
        ).first()
        if comment:
            self._db_session.delete(instance=comment)
            self._db_session.commit()
            return True
        return False
