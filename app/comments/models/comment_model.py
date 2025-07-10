from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.database import Base


class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blog_id = Column(Integer, ForeignKey("blogs.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(
    ), default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), default=datetime.now(tz=timezone.utc))

    user = relationship("UserModel", back_populates="comments")
    blog = relationship("BlogModel", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, content={self.content}, user_id={self.user_id}, blog_id={self.blog_id})>"

    def __str__(self):
        return f"Comment(id={self.id}, content={self.content}, user_id={self.user_id}, blog_id={self.blog_id})"
