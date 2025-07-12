# -*- coding: utf-8 -*-
"""
Repository layer for managing blog-tag associations.

This module defines the BlogTagRepository class, which provides methods for linking and unlinking
blogs and tags using the association table.
"""

from typing import Any, List

from sqlalchemy import CursorResult, Delete
from sqlalchemy.orm import Session

from app.blog_tags.models.blog_tags import blog_tags


class BlogTagRepository:
    """
    Repository for managing blog-tag associations.
    """

    def __init__(self, db_session: Session) -> None:
        """
        Initialize the BlogTagRepository with a database session.

        Args:
            db_session (Session): SQLAlchemy session for database operations.
        """
        self._db_session: Session = db_session

    def link_blog_tags(self, blog_id: int, tag_ids: list[int]) -> int:
        """
        Links blog with tags by inserting entries into the blog_tags association table.

        Args:
            blog_id (int): The ID of the blog to link.
            tag_ids (list[int]): A list of tag IDs to link to the blog.

        Returns:
            int: The number of rows inserted or 0 if no tags were linked.
        """
        if tag_ids:
            links: List[dict[str, int]] = [{"blog_id": blog_id, "tag_id": tag_id} for tag_id in tag_ids]
            result: CursorResult[Any] = self._db_session.execute(blog_tags.insert(), links)
            return result.rowcount
        return 0

    def unlink_blog_tags_by_blog_id(self, blog_id: int, tag_ids_to_unlink: List[int]) -> int:
        """
        Unlinks tags from a blog by deleting entries from the blog_tags association table.

        Args:
            blog_id (int): The ID of the blog to unlink tags from.
            tag_ids_to_unlink (List[int]): A list of tag IDs to unlink from the blog.

        Returns:
            int: The number of rows deleted.
        """
        query: Delete = blog_tags.delete().where(blog_tags.c.blog_id == blog_id)
        if tag_ids_to_unlink:
            query = query.where(blog_tags.c.tag_id.in_(tag_ids_to_unlink))
        result: CursorResult[Any] = self._db_session.execute(query)
        return result.rowcount
