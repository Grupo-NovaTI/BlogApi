# -*- coding: utf-8 -*-
from typing import List
from app.blog_tags.models.blog_tags import blog_tags
from sqlalchemy.orm import Session
from sqlalchemy import  Delete
_MODEL = "BlogTags"


class BlogTagRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session: Session = db_session

    def link_blog_tags(self, blog_id: int, tag_ids: list[int]) -> None:
        """Links blog with tags by inserting entries into the blog_tags association table."""
        if tag_ids:
            links: List[dict[str, int]] = [{"blog_id": blog_id, "tag_id": tag_id} for tag_id in tag_ids]
            self._db_session.execute(blog_tags.insert(), links)

    def unlink_blog_tags_by_blog_id(self, blog_id: int, tag_ids_to_unlink: List[int]) -> None:
        query: Delete = blog_tags.delete().where(blog_tags.c.blog_id == blog_id)
        if tag_ids_to_unlink:
            query = query.where(blog_tags.c.tag_id.in_(tag_ids_to_unlink))
        self._db_session.execute(query)
