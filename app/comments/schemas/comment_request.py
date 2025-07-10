from pydantic import BaseModel, Field
from typing import Optional
from app.comments.models.comment_model import CommentModel

class InsertCommentRequest(BaseModel):
    """
    Schema for inserting a new comment.
    """
    blog_id: int = Field(..., description="ID of the blog post to which the comment belongs")
    content: str = Field(..., min_length=1, max_length=500, description="Content of the comment")

    class Config:
        json_schema_extra = {
            "example": {
                "blog_id": 1,
                "content": "This is a sample comment."
            }
        }
class UpdateCommentRequest(BaseModel):
    """
    Schema for updating an existing comment.
    """
    content: str = Field(
        ..., min_length=1, max_length=500, description="Updated content of the comment"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "content": "This is the updated content of the comment."
            }
        }

    def to_orm(self) -> CommentModel:
        """
        Convert the UpdateCommentRequest schema to a CommentModel instance.

        Returns:
            CommentModel: An instance of CommentModel with the data from the request.
        """
        return CommentModel(
            content=self.content
        )