from sqlalchemy import Column, Integer, ForeignKey, Table

from app.core.db.database import Base

blog_tags = Table(
    "blogs_tags",
    Base.metadata,
    Column("blog_id", Integer, ForeignKey("blogs.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

