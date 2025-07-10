from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.database import Base
from app.blog_tags.models.blog_tags import blog_tags

class BlogModel(Base):
    __tablename__ = "blogs"
    """BlogModel represents a blog post in the system.

    Attributes:
        id (int): Unique identifier for the blog post.
        title (str): Title of the blog post.
        content (str): Content of the blog post.
        user_id (int): Foreign key referencing the user who authored the blog post.
        is_published (bool): Indicates whether the blog post is published or not.
        created_at (datetime): Timestamp when the blog post was created.
        updated_at (datetime): Timestamp when the blog post was last updated.   
    """
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, nullable=False, server_default="False", default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(
    ), default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), default=datetime.now(tz=timezone.utc))
    user = relationship("UserModel", back_populates="blogs")
    tags = relationship("TagModel", secondary=blog_tags, back_populates="blogs")
    comments = relationship("CommentModel", back_populates="blog", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Blog(id={self.id}, title={self.title}, user_id={self.user_id})>"

    def __str__(self):
        return f"Blog(id={self.id}, title={self.title}, user_id={self.user_id})"
