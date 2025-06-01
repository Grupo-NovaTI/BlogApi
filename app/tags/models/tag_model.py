from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.db.database import Base
from tags.models.blog_tags import blog_tags

class TagModel(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    blogs = relationship("BlogModel", secondary=blog_tags, back_populates="tags")
    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"

    def __str__(self):
        return f"Tag(id={self.id}, name={self.name})"
