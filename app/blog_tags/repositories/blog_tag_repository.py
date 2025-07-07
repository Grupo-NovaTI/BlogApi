# -*- coding: utf-8 -*-
from app.blog_tags.models.blog_tags import blog_tags
from app.utils.errors.exception_handlers import handle_repository_exception
from app.utils.enums.operations import Operations
from sqlalchemy.orm import Session
from sqlalchemy import Insert, Delete
_MODEL = "BlogTags"


class BlogTagRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session: Session = db_session

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.CREATE
    )
    def link_blog_tag(self, blog_id: int, tag_id: int) -> None:
        """Links a blog with a tag in the many-to-many relationship."""
        link: Insert = blog_tags.insert().values(blog_id=blog_id, tag_id=tag_id)
        self._db_session.execute(link)
        self._db_session.commit()

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.DELETE
    )
    def unlink_blog_tag_by_tag_id(self, tag_id: int) -> None:
        """Unlinks a blog from a tag in the many-to-many relationship."""
        unlink: Delete = blog_tags.delete().where(
            blog_tags.c.tag_id == tag_id
        )
        self._db_session.execute(unlink)
        self._db_session.commit()

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.DELETE
    )
    def unlink_blog_tag_by_blog_id(self, blog_id: int) -> None:
        """Unlinks a tag from a blog in the many-to-many relationship."""
        unlink: Delete = blog_tags.delete().where(
            blog_tags.c.blog_id == blog_id
        )
        self._db_session.execute(unlink)
        self._db_session.commit()

    @handle_repository_exception(
        model=_MODEL,
        operation=Operations.CREATE
    )
    def link_multiple_blog_tags(self, blog_id: int, tag_ids: list[int]) -> None:
        if tag_ids:
            links: list[dict[str, int]] = [{"blog_id": blog_id, "tag_id": tag_id} for tag_id in tag_ids]
            self._db_session.execute(blog_tags.insert(), links)
            self._db_session.commit()
