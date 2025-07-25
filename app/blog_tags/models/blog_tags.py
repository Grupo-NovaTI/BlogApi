"""
Association table for many-to-many relationship between blogs and tags.

This module defines the SQLAlchemy Table object for linking blogs and tags.
"""

from sqlalchemy import Column, ForeignKey, Integer, Table

from app.core.data.database import Base

blog_tags = Table(
    "blogs_tags",
    Base.metadata,
    Column("blog_id", Integer, ForeignKey("blogs.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

