from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.comments.models.comment_model import CommentModel
from app.comments.exceptions.comment_exceptions import CommentOperationException
from app.utils.errors.error_messages import database_error_message, integrity_error_message, unknown_error_message
from app.utils.logger.application_logger import ApplicationLogger
_logger = ApplicationLogger(__name__)
class CommentRepository:
    """Repository for managing comments."""

    def __init__(self, db_session: Session):
        self._db_session: Session = db_session

    def create_comment(self, comment: CommentModel) -> CommentModel:
        """Create a new comment."""
        try:
            self._db_session.add(instance=comment)
            self._db_session.commit()
            self._db_session.refresh(instance=comment)
            return comment
        except IntegrityError as e:
            self._db_session.rollback()
            _logger.log_error(message=integrity_error_message(operation="Comment", instance="create", exception=e))
            raise CommentOperationException(message=str(e), operation="Create")
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(operation="Comment", instance="create", exception=e))
            raise CommentOperationException(message=str(e), operation="Create")
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(message=unknown_error_message(operation="Comment", instance="create", exception=e))
            raise CommentOperationException(message=str(e), operation="Create")

    def get_all_comments_by_blog_id(self, blog_id: int) -> list[CommentModel]:
        """Get all comments for a specific blog by its ID."""
        try:
            return self._db_session.query(CommentModel).filter(CommentModel.blog_id == blog_id).all()
        except SQLAlchemyError as e:
            _logger.log_error(message=database_error_message(operation="Comment", instance="retrieve", exception=e))
            raise CommentOperationException(message=str(e), operation="Retrieve")
        except Exception as e:
            _logger.log_error(message=unknown_error_message(operation="Comment", instance="retrieve", exception=e))
            raise CommentOperationException(message=str(e), operation="Retrieve")

    def get_all_comments_by_author_id(self, author_id: int) -> list[CommentModel]:
        """Get all comments made by a specific author by their ID."""
        try:
            return self._db_session.query(CommentModel).filter(CommentModel.author_id == author_id).all()
        except SQLAlchemyError as e:
            _logger.log_error(message=database_error_message(operation="Comment", instance="retrieve", exception=e))
            raise CommentOperationException(message=str(e), operation="Retrieve")
        except Exception as e:
            _logger.log_error(message=unknown_error_message(operation="Comment", instance="retrieve", exception=e))
            raise CommentOperationException(message=str(e), operation="Retrieve")

    def get_comment_by_id(self, comment_id: int) -> Optional[CommentModel]:
        """Get a comment by its ID."""
        try:
            return self._db_session.get(entity=CommentModel, ident=comment_id)
        except SQLAlchemyError as e:
            _logger.log_error(message=database_error_message(operation="Comment", instance="retrieve", exception=e))
            raise CommentOperationException(message=str(e), operation="Retrieve")
        except Exception as e:
            _logger.log_error(message=unknown_error_message(operation="Comment", instance="retrieve", exception=e))
            raise CommentOperationException(message=str(e), operation="Retrieve")

    def update_comment_content(self, comment_id: int, user_id: int, content: str) -> Optional[CommentModel]:
        """Update a comment's content by its ID."""
        try:
            rows_updated: int = self._db_session.query(CommentModel).filter(
                and_(CommentModel.id == comment_id, CommentModel.author_id == user_id)
            ).update(values={"content": content})
            if rows_updated == 0:
                return None
            self._db_session.commit()
            return self.get_comment_by_id(comment_id=comment_id)
        except IntegrityError as e:
            self._db_session.rollback()
            _logger.log_error(message=integrity_error_message(operation="Comment", instance="update", exception=e))
            raise CommentOperationException(message=str(e), operation="Update")
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(operation="Comment", instance="update", exception=e))
            raise CommentOperationException(message=str(e), operation="Update")
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(message=unknown_error_message(operation="Comment", instance="update", exception=e))
            raise CommentOperationException(message=str(e), operation="Update")

    def delete_comment(self, comment_id: int) -> bool:
        """Delete a comment by its ID."""
        try:
            comment: Optional[CommentModel] = self.get_comment_by_id(comment_id)
            if comment:
                self._db_session.delete(instance=comment)
                self._db_session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(operation="Comment", instance="delete", exception=e))
            raise CommentOperationException(message=str(e), operation="Delete")
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(message=unknown_error_message(operation="Comment", instance="delete", exception=e))
            raise CommentOperationException(message=str(e), operation="Delete")

    def delete_comment_by_author(self, author_id: int, comment_id: int) -> bool:
        """Delete a comment by its ID and user ID."""
        try:
            comment: Optional[CommentModel] = self._db_session.query(CommentModel).filter(
                and_(CommentModel.id == comment_id, CommentModel.author_id == author_id)
            ).first()
            if comment:
                self._db_session.delete(instance=comment)
                self._db_session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(operation="Comment", instance="delete", exception=e))
            raise CommentOperationException(message=str(e), operation="Delete")
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(message=unknown_error_message(operation="Comment", instance="delete", exception=e))
            raise CommentOperationException(message=str(e), operation="Delete")