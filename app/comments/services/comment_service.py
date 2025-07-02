from typing import Optional
from app.comments.repositories.comment_repository import CommentRepository
from app.comments.models.comment_model import CommentModel
from app.comments.exceptions.comment_exceptions import CommentNotFoundException
from app.utils.errors.error_messages import not_found_message
class CommentService:
    """Service for managing comments."""
    def __init__(self, comment_repository: CommentRepository) -> None:
        self._repository: CommentRepository = comment_repository

    def create_comment(self, comment: CommentModel) -> CommentModel:
        """Create a new comment in the repository."""
        return self._repository.create_comment(comment=comment)

    def get_comments_by_blog_id(self, blog_id: int) -> list[CommentModel]:
        """Retrieve all comments for a specific blog by its ID."""
        return self._repository.get_all_comments_by_blog_id(blog_id=blog_id)

    def get_comments_by_author_id(self, author_id: int) -> list[CommentModel]:
        """Retrieve all comments made by a specific author by their ID."""
        return self._repository.get_all_comments_by_author_id(author_id=author_id)

    def get_comment_by_id(self, comment_id: int) -> Optional[CommentModel]:
        """Retrieve a comment by its ID."""
        return self._repository.get_comment_by_id(comment_id=comment_id)

    def update_comment_content(self, comment_id: int, content: str, user_id: int) -> CommentModel:
        """Update a comment's content by its ID."""
        comment: Optional[CommentModel] = self._repository.update_comment_content(comment_id=comment_id, user_id=user_id, content=content)
        if not comment:
            raise CommentNotFoundException(identifier=comment_id, message=not_found_message(
                instance="comment",
                identifier=str(comment_id)
            ))
        return comment
    
    def delete_comment(self, comment_id: int) -> None:
        """Delete a comment by its ID."""
        deleted = self._repository.delete_comment(comment_id=comment_id)
        if not deleted:
            raise CommentNotFoundException(identifier=comment_id, message=not_found_message(
                instance="comment",
                identifier=str(comment_id)
            ))
            
    def delete_comment_by_author(self, comment_id: int, author_id: int) -> None:
        """Delete a comment by its ID and author ID."""
        deleted: bool = self._repository.delete_comment_by_author(author_id=author_id, comment_id=comment_id)
        if not deleted:
            raise CommentNotFoundException(identifier=comment_id, message=not_found_message(
                instance="comment",
                identifier=str(comment_id)
            ))
        
