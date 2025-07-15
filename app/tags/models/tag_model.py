"""
Tag model definition for blog post categorization.

This module defines the TagModel SQLAlchemy ORM class, representing tags that can be associated
with blog posts for categorization and filtering.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.data.database import Base
from app.blog_tags.models.blog_tags import blog_tags


class TagModel(Base):
    """
    Represents a tag entity for categorizing blog posts.

    Attributes:
        id (int): Primary key, unique identifier for the tag.
        name (str): Unique name of the tag.
        description (str, optional): Optional description of the tag.
        created_at (str): ISO timestamp of creation.
        updated_at (str): ISO timestamp of last update.
        blogs (List[BlogModel]): List of associated BlogModel instances via a many-to-many relationship.
    """

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(
        String, default=datetime.now(timezone.utc).isoformat(), nullable=False
    )
    updated_at = Column(
        String,
        default=datetime.now(timezone.utc).isoformat(),
        onupdate=datetime.now(timezone.utc).isoformat(),
        nullable=False,
    )
    blogs = relationship("BlogModel", secondary=blog_tags, back_populates="tags")

    def __repr__(self):
        """
        Returns a string representation for debugging.

        Returns:
            str: Debug string for the tag instance.
        """
        return f"<Tag(id={self.id}, name={self.name})>"

    def __str__(self):
        """
        Returns a human-readable string representation.

        Returns:
            str: Readable string for the tag instance.
        """
        return f"Tag(id={self.id}, name={self.name})"
