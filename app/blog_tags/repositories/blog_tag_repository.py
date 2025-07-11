# -*- coding: utf-8 -*-
from typing import Any, List

from sqlalchemy import CursorResult, Delete
from sqlalchemy.orm import Session

from app.blog_tags.models.blog_tags import blog_tags


class BlogTagRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session: Session = db_session

    def link_blog_tags(self, blog_id: int, tag_ids: list[int]) -> int:
        """Links blog with tags by inserting entries into the blog_tags association table.

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
        query: Delete = blog_tags.delete().where(blog_tags.c.blog_id == blog_id)
        if tag_ids_to_unlink:
            query = query.where(blog_tags.c.tag_id.in_(tag_ids_to_unlink))
        result: CursorResult[Any] = self._db_session.execute(query)
        return result.rowcount
