from typing import Any, Optional
from sqlalchemy.orm import Session
from app.comments.repositories.comment_repository import CommentRepository
from app.comments.models.comment_model import CommentModel
from app.utils.errors.exceptions import NotFoundException as CommentNotFoundException
from app.utils.errors.exception_handlers import handle_read_exceptions, handle_service_transaction
from app.utils.enums.operations import Operations
_MODEL_NAME = "Comments"


class CommentService:
    """Service for managing comments."""

    def __init__(self, comment_repository: CommentRepository, db_session: Session) -> None:
        self._repository: CommentRepository = comment_repository
        self._db_session: Session = db_session

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.CREATE
    )
    def create_comment(self, comment: dict[str, Any], user_id: int) -> CommentModel:
        comment_model = CommentModel(**comment, user_id=user_id)
        """Create a new comment in the repository."""
        return self._repository.create_comment(comment=comment_model)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH_BY
    )
    def get_comments_by_blog_id(self, blog_id: int) -> list[CommentModel]:
        """Retrieve all comments for a specific blog by its ID."""
        return self._repository.get_all_comments_by_blog(blog_id=blog_id)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH
    )
    def get_comments_by_user(self, user_id: int) -> list[CommentModel]:
        """Retrieve all comments made by a specific user by their ID."""
        return self._repository.get_all_comments_by_user(user_id=user_id)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH_BY
    )
    def get_comment_by_id(self, id: int) -> Optional[CommentModel]:
        """Retrieve a comment by its ID."""
        return self._repository.get_comment_by_id(id=id)

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.UPDATE
    )
    def update_comment_content(self, comment_id: int, content: str, user_id: int) -> CommentModel:
        """Update a comment's content by its ID."""
        updated_comment: Optional[CommentModel] = self._repository.update_comment_content(
            comment_id=comment_id, user_id=user_id, content=content)
        if not updated_comment:
            raise CommentNotFoundException(
                identifier=comment_id, resource_type="Comment")
        return updated_comment

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.DELETE
    )
    def delete_comment(self, comment_id: int) -> None:
        """Delete a comment by its ID."""
        was_deleted: bool = self._repository.delete_comment(comment_id=comment_id)
        if not was_deleted:
            raise CommentNotFoundException(
                identifier=comment_id, resource_type="Comment")

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.DELETE
    )
    def delete_comment_by_user(self, comment_id: int, user_id: int) -> None:
        """Delete a comment by its ID and author ID."""
        was_deleted: bool = self._repository.delete_comment_by_user(
            user_id=user_id, comment_id=comment_id)
        if not was_deleted:
            raise CommentNotFoundException(
                identifier=comment_id, resource_type="Comment")
