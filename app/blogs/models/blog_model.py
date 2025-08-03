"""
SQLAlchemy ORM model for blogs.

This module defines the BlogModel class, representing blog posts in the database.
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.blog_tags.models.blog_tags import blog_tags
from app.core.data.db.database import Base


class BlogModel(Base):
    """BlogModel represents a blog post in the system.

    Attributes:
        id (int): Unique identifier for the blog post.
        title (str): Title of the blog post.
        content (str): Content of the blog post.
        user_id (int): Foreign key referencing the user who authored the blog post.
        is_published (bool): Indicates whether the blog post is published or not.
        created_at (datetime): Timestamp when the blog post was created.
        updated_at (datetime): Timestamp when the blog post was last updated.
        user: Relationship to the UserModel.
        tags: Relationship to TagModel (many-to-many).
        comments: Relationship to CommentModel (one-to-many).
    """
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, nullable=False, server_default="False", default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), default=datetime.now(tz=timezone.utc))
    image_url = Column(String, nullable=True, comment="URL of the blog image")
    user = relationship("UserModel", back_populates="blogs")
    tags = relationship("TagModel", secondary=blog_tags, back_populates="blogs")
    comments = relationship("CommentModel", back_populates="blog", cascade="all, delete-orphan")

    def __repr__(self):
        """
        Returns a string representation for debugging.

        Returns:
            str: Debug string for the blog instance.
        """
        return f"<Blog(id={self.id}, title={self.title}, user_id={self.user_id})>"

    def __str__(self):
        """
        Returns a human-readable string representation.

        Returns:
            str: Readable string for the blog instance.
        """
        return f"Blog(id={self.id}, title={self.title}, user_id={self.user_id})"
