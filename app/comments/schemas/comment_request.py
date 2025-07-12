"""
Pydantic schemas for comment creation and update requests.

This module defines schemas for validating and serializing comment input data for creation and update operations.
"""

from pydantic import BaseModel, Field

from app.comments.models.comment_model import CommentModel


class InsertCommentRequest(BaseModel):
    """
    Schema for inserting a new comment.

    Attributes:
        blog_id (int): ID of the blog post to which the comment belongs.
        content (str): Content of the comment.
    """
    blog_id: int = Field(
        ...,
        description="ID of the blog post to which the comment belongs"
    )
    content: str = Field(
        ..., min_length=1, max_length=500,
        description="Content of the comment"
    )

    class Config:
        """
        Pydantic configuration for InsertCommentRequest schema.
        """
        json_schema_extra = {
            "example": {
                "blog_id": 1,
                "content": "This is a sample comment."
            }
        }


class UpdateCommentRequest(BaseModel):
    """
    Schema for updating an existing comment.

    Attributes:
        content (str): Updated content of the comment.
    """
    content: str = Field(
        ..., min_length=1, max_length=500, description="Updated content of the comment"
    )

    class Config:
        """
        Pydantic configuration for UpdateCommentRequest schema.
        """
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
