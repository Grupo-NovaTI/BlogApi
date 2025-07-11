from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db.database import Base
from app.blog_tags.models.blog_tags import blog_tags

class TagModel(Base):
    """
    Represents a tag entity for categorizing blog posts.

    Attributes:
        id (int): Primary key, unique identifier for the tag.
        name (str): Unique name of the tag.
        description (str, optional): Optional description of the tag.
        blogs (List[BlogModel]): List of associated BlogModel instances via a many-to-many relationship.

    Methods:
        __repr__(): Returns a string representation for debugging.
        __str__(): Returns a human-readable string representation.
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(
        String, default=datetime.now(timezone.utc).isoformat(), nullable=False)
    updated_at = Column(
        String, default=datetime.now(timezone.utc).isoformat(), onupdate=datetime.now(timezone.utc).isoformat(), nullable=False)
    blogs = relationship("BlogModel", secondary=blog_tags, back_populates="tags")
    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"

    def __str__(self):
        return f"Tag(id={self.id}, name={self.name})"
