from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.db.database import Base
from tags.models.blog_tags import blog_tags

class BlogModel(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, nullable=False, server_default="False", default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(
    ), default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), default=datetime.now(tz=timezone.utc))
    author = relationship("UserModel", back_populates="blogs")
    tags = relationship("TagModel", secondary=blog_tags, back_populates="blogs")
    comments = relationship("CommentModel", back_populates="blog", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Blog(id={self.id}, title={self.title}, author_id={self.author_id})>"

    def __str__(self):
        return f"Blog(id={self.id}, title={self.title}, author_id={self.author_id})"
