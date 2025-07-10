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
    NotFoundException as BlogNotFoundException

_MODEL_NAME = "Blogs"
class BlogService:
    def __init__(self, blog_repository: BlogRepository, blog_tag_repository: BlogTagRepository, db_session: Session) -> None:
        self._blog_repository: BlogRepository = blog_repository
        self._blog_tag_repository: BlogTagRepository = blog_tag_repository
        self._db_session: Session = db_session
        self.model_name = "Blogs"

    def get_all_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        return self._blog_repository.get_all_blogs(limit=limit, offset=offset)

    def get_blog_by_id(self, id: int) -> Optional[BlogModel]:
        return self._blog_repository.get_blog_by_id(id=id)

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
        updated_blog: Optional[BlogModel] = self._blog_repository.update_blog(
            blog_data=blog, blog_id=blog_id, user_id=user_id)
        if not updated_blog:
            raise BlogNotFoundException(identifier=blog_id, resource_type=self.model_name)
        if tags:
            self._blog_tag_repository.unlink_blog_tags_by_blog_id(
                blog_id=blog_id, tag_ids_to_unlink=tags)
            self._blog_tag_repository.link_blog_tags(
                blog_id=int(str(updated_blog.id)), tag_ids=tags)
        return updated_blog

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.DELETE
    )
    def delete_blog(self, blog_id: int, user_id: int) -> None:
        was_deleted: bool = self._blog_repository.delete_blog(
            blog_id=blog_id, user_id=user_id)
        if not was_deleted:
            raise BlogNotFoundException(
                identifier=blog_id, resource_type=self.model_name)

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.UPDATE
    )
    def update_blog_visibility(self, id: int, visibility: bool, user_id : int) -> BlogModel:
        updated_blog: Optional[BlogModel] = self._blog_repository.update_blog_visibility(
            blog_id=id, visibility=visibility, user_id=user_id)
        if not updated_blog:
            raise BlogNotFoundException(identifier=id, resource_type=self.model_name)
        return updated_blog

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
