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
    ForbiddenException as BlogForbiddenException
from app.utils.errors.exceptions import \
    NotFoundException as BlogNotFoundException

_MODEL_NAME = "Blog"


class BlogService:
    """BlogService provides business logic for managing blog posts and their associated tags.

    This service acts as an intermediary between the API layer and the data repositories,
    handling authorization, transactional operations, and exception management for blog-related actions.

    Attributes:
        _blog_repository (BlogRepository): Handles CRUD operations for blog data.
        _blog_tag_repository (BlogTagRepository): Manages associations between blogs and tags.
        _db_session (Session): SQLAlchemy session for database transactions.

    Methods:
        get_all_blogs(limit: int = 10, offset: int = 0) -> List[BlogModel]:
            Retrieve a paginated list of all blogs.

        get_blog_by_id(blog_id: int) -> Optional[BlogModel]:
            Retrieve a single blog by its unique identifier.

        create_blog(blog_data: dict[str, Any], user_id: int) -> BlogModel:
            Create a new blog post and associate it with tags.

        update_blog(blog_data: dict[str, Any], blog_id: int, user_id: int) -> BlogModel:
            Update an existing blog post and manage its tag associations, ensuring user authorization.

        delete_blog_for_user(blog_id: int, user_id: int) -> None:
            Delete a blog post if the requesting user is authorized.

        delete_blog_for_admin(blog_id: int) -> None:
            Delete a blog post as an admin, bypassing user authorization.

        get_public_blogs(limit: int = 10, offset: int = 0) -> List[BlogModel]:
            Retrieve a paginated list of publicly visible blogs.

        get_blogs_by_user(user_id: int, limit: int = 10, offset: int = 0) -> List[BlogModel]:
            Retrieve a paginated list of blogs authored by a specific user.

    Private Methods:
        _get_and_authorize_blog(blog_id: int, user_id: int) -> BlogModel:
            Retrieve a blog and verify that the user is authorized to access or modify it.
        """
    def __init__(self, blog_repository: BlogRepository, blog_tag_repository: BlogTagRepository, db_session: Session) -> None:
        """
        Initializes the BlogService with the given repositories and database session.

        Args:
            blog_repository (BlogRepository): Repository for blog data access and operations.
            blog_tag_repository (BlogTagRepository): Repository for blog tag data access and operations.
            db_session (Session): SQLAlchemy database session for database transactions.
        """
        self._blog_repository: BlogRepository = blog_repository
        self._blog_tag_repository: BlogTagRepository = blog_tag_repository
        self._db_session: Session = db_session

    def _get_and_authorize_blog(self, blog_id: int, user_id: int) -> BlogModel:
        """
        Retrieve a blog by its ID and verify that the specified user is authorized to access it.

        Args:
            blog_id (int): The unique identifier of the blog to retrieve.
            user_id (int): The unique identifier of the user requesting access.

        Returns:
            BlogModel: The blog instance if found and authorized.

        Raises:
            BlogNotFoundException: If no blog with the given ID exists.
            BlogForbiddenException: If the user does not have permission to access the blog.
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
        """
        Retrieve a list of blog entries with pagination support.

        Args:
            limit (int, optional): The maximum number of blog entries to return. Defaults to 10.
            offset (int, optional): The number of blog entries to skip before starting to collect the result set. Defaults to 0.

        Returns:
            List[BlogModel]: A list of blog entries retrieved from the repository.
        """
        return self._blog_repository.get_all_blogs(limit=limit, offset=offset)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH_BY
    )
    def get_blog_by_id(self, blog_id: int) -> Optional[BlogModel]:
        """
        Retrieve a blog entry by its unique identifier.

        Args:
            blog_id (int): The unique identifier of the blog to retrieve.

        Returns:
            Optional[BlogModel]: The blog entry if found, otherwise None.
        """
        return self._blog_repository.get_blog_by_id(blog_id=blog_id)

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.CREATE
    )
    def create_blog(self, blog_data: dict[str, Any], user_id: int) -> BlogModel:
        """
        Creates a new blog entry and associates it with the specified user and optional tags.

        Args:
            blog_data (dict[str, Any]): A dictionary containing the blog data. May include a "tags" key with a list of tag IDs.
            user_id (int): The ID of the user creating the blog.

        Returns:
            BlogModel: The created BlogModel instance with the blog data.

        Side Effects:
            - Persists the new blog entry to the database.
            - Links the blog to the specified tags if provided.
            - Refreshes the created_blog instance from the database.
        """
        tags: Optional[List[int]] = blog_data.pop("tags", [])
        blog_model = BlogModel(**blog_data, user_id=user_id)
        created_blog: BlogModel = self._blog_repository.create_blog(
            blog=blog_model)
        if tags:
            self._blog_tag_repository.link_blog_tags(
                blog_id=created_blog.id, tag_ids=tags) # type: ignore
        self._db_session.refresh(created_blog)

        return created_blog

    @handle_service_transaction(
        model=_MODEL_NAME,
        operation=Operations.UPDATE
    )
    def update_blog(self, blog_data: dict[str, Any], blog_id: int, user_id: int) -> BlogModel:
        """
        Updates a blog post with the provided data and manages its associated tags.

        Args:
            blog_data (dict[str, Any]): A dictionary containing the updated blog data. May include a "tags" key with a list of tag IDs.
            blog_id (int): The ID of the blog post to update.
            user_id (int): The ID of the user attempting the update, used for authorization.

        Returns:
            BlogModel: The authorized blog instance before the update.

        Raises:
            AuthorizationError: If the user is not authorized to update the blog.
            BlogNotFoundError: If the blog with the given ID does not exist.

        Side Effects:
            - Updates the blog post in the repository.
            - Adds or removes tag associations as needed.
        """
        tags: Optional[List[int]] = blog_data.pop("tags", [])
        authorized_blog: BlogModel = self._get_and_authorize_blog(
            blog_id=blog_id, user_id=user_id)
        updated_blog: BlogModel = self._blog_repository.update_blog(
            blog=authorized_blog, blog_data=blog_data)
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
        """
        Deletes a blog post for a specific user.

        Args:
            blog_id (int): The ID of the blog post to delete.
            user_id (int): The ID of the user requesting the deletion.

        Raises:
            BlogNotFoundException: If the blog with the given ID does not exist.
            UnauthorizedException: If the user is not authorized to delete the blog.

        Returns:
            None
        """
        blog_to_delete: BlogModel = self._get_and_authorize_blog(
            blog_id=blog_id, user_id=user_id)
        self._blog_repository.delete_blog(
            blog=blog_to_delete)

    def delete_blog_for_admin(self, blog_id: int) -> None:
        """Deletes a blog entry from the database as an admin user.

        Args:
            blog_id (int): The ID of the blog post to delete.

        Raises:
            BlogNotFoundException: If no blog with the specified ID exists.
        
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
        """
        Retrieve a list of public blogs with pagination support.

        Args:
            limit (int, optional): The maximum number of blogs to return. Defaults to 10.
            offset (int, optional): The number of blogs to skip before starting to collect the result set. Defaults to 0.

        Returns:
            List[BlogModel]: A list of public blog entries.
        """
        return self._blog_repository.get_public_blogs(limit=limit, offset=offset)

    @handle_read_exceptions(
        model=_MODEL_NAME,
        operation=Operations.FETCH_BY
    )
    def get_blogs_by_user(self, user_id: int, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        """
        Retrieve a list of blogs authored by a specific user.

        Args:
            user_id (int): The ID of the user whose blogs are to be retrieved.
            limit (int, optional): The maximum number of blogs to return. Defaults to 10.
            offset (int, optional): The number of blogs to skip before starting to collect the result set. Defaults to 0.

        Returns:
            List[BlogModel]: A list of BlogModel instances authored by the specified user.
        """
        return self._blog_repository.get_blogs_by_user(user_id=user_id, limit=limit, offset=offset)
