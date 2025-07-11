# -*- coding: utf-8 -*-
from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.blog_tags.repositories.blog_tag_repository import BlogTagRepository
from app.blogs.models.blog_model import BlogModel
from app.blogs.repositories.blog_repository import BlogRepository
from app.utils.enums.operations import Operations
from app.utils.errors.exception_handlers import (handle_read_exceptions,
                                                 handle_service_transaction)
from app.utils.errors.exceptions import \
    NotFoundException as BlogNotFoundException, \
    ForbiddenException as BlogForbiddenException

_MODEL_NAME = "Blog"


class BlogService:
    def __init__(self, blog_repository: BlogRepository, blog_tag_repository: BlogTagRepository, db_session: Session) -> None:
        self._blog_repository: BlogRepository = blog_repository
        self._blog_tag_repository: BlogTagRepository = blog_tag_repository
        self._db_session: Session = db_session

    def _get_and_authorize_blog(self, blog_id: int, user_id: int) -> BlogModel:
        """
        Retrieves a blog by ID and verifies that the user is the owner.
        Returns the blog object if successful, otherwise raises an exception.
        """
        blog: Optional[BlogModel] = self._blog_repository.get_blog_by_id(
            blog_id=blog_id)
        if not blog:
            raise BlogNotFoundException(
                identifier=blog_id, resource_type=_MODEL_NAME)
        if str(blog.user_id) != str(user_id):
            raise BlogForbiddenException(
                details=f"User {user_id} lacks permission for blog {blog_id}.")
        return blog

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH
    )
    def get_all_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        return self._blog_repository.get_all_blogs(limit=limit, offset=offset)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH_BY
    )
    def get_blog_by_id(self, blog_id: int) -> Optional[BlogModel]:
        return self._blog_repository.get_blog_by_id(blog_id=blog_id)

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.CREATE
    )
    def create_blog(self, blog: dict[str, Any], user_id: int) -> BlogModel:
        tags: Optional[List[int]] = blog.pop("tags", [])
        blog_model = BlogModel(**blog, user_id=user_id)
        created_blog: BlogModel = self._blog_repository.create_blog(
            blog=blog_model)
        if tags:
            self._blog_tag_repository.link_blog_tags(
                blog_id=int(str(created_blog.id)), tag_ids=tags)
        self._db_session.refresh(created_blog)

        return created_blog

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.UPDATE
    )
    def update_blog(self, blog: dict[str, Any], blog_id: int, user_id: int) -> BlogModel:
        tags: Optional[List[int]] = blog.pop("tags", [])
        authorized_blog: BlogModel = self._get_and_authorize_blog(
            blog_id=blog_id, user_id=user_id)
        updated_blog: BlogModel = self._blog_repository.update_blog(
            blog=authorized_blog, blog_data=blog)
        if tags is not None:
            current_tag_ids: set[Any] = {tag.id for tag in updated_blog.tags}  # type: ignore
            new_tag_ids: set[int] = set(tags)

            tags_to_add: List[int] = list(new_tag_ids - current_tag_ids)
            tags_to_remove: List[int] = list(current_tag_ids - new_tag_ids)

            if tags_to_add:
                self._blog_tag_repository.link_blog_tags(blog_id, tags_to_add)
            if tags_to_remove:
                self._blog_tag_repository.unlink_blog_tags_by_blog_id(blog_id, tags_to_remove)
        return authorized_blog

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.DELETE
    )
    def delete_blog_for_user(self, blog_id: int, user_id: int) -> None:
        blog_to_delete: BlogModel = self._get_and_authorize_blog(
            blog_id=blog_id, user_id=user_id)
        self._blog_repository.delete_blog(
            blog=blog_to_delete)

    def delete_blog_for_admin(self, blog_id: int) -> None:
        """
        Deletes a blog entry from the database by an admin.
        Args:
            blog_id (int): The unique identifier of the blog to delete.
        """
        blog_to_delete: Optional[BlogModel] = self._blog_repository.get_blog_by_id(
            blog_id=blog_id)
        if not blog_to_delete:
            raise BlogNotFoundException(
                identifier=blog_id, resource_type=_MODEL_NAME)
        self._blog_repository.delete_blog(blog=blog_to_delete)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH
    )
    def get_public_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        return self._blog_repository.get_public_blogs(limit=limit, offset=offset)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH_BY
    )
    def get_blogs_by_user(self, user_id: int, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        return self._blog_repository.get_blogs_by_user(user_id=user_id, limit=limit, offset=offset)
