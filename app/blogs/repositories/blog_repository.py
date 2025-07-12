"""
Repository layer for blog management.

This module defines the BlogRepository class, which provides CRUD operations and queries
for blog entities in the database.
"""

from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm.session import Session

from app.blogs.models.blog_model import BlogModel


class BlogRepository:
    """
    Repository for managing blogs.
    """

    def __init__(self, db_session: Session) -> None:
        """
        Initialize the BlogRepository with a database session.

        Args:
            db_session (Session): SQLAlchemy session for database operations.
        """
        self._db_session: Session = db_session

    def get_all_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        """
        Fetches all blogs with pagination support.

        Args:
            limit (int): Maximum number of blogs to retrieve. Defaults to 10.
            offset (int): Number of blogs to skip. Defaults to 0.

        Returns:
            List[BlogModel]: List of blog models.
        """
        return self._db_session.query(BlogModel).filter(and_(BlogModel.is_published == True)).limit(limit=limit).offset(offset=offset).all()

    def get_blog_by_id(self, blog_id: int) -> Optional[BlogModel]:
        """
        Fetch a blog by its ID.

        Args:
            blog_id (int): The unique identifier of the blog.

        Returns:
            Optional[BlogModel]: The blog model if found, otherwise None.
        """
        return self._db_session.query(BlogModel).filter(BlogModel.id == blog_id).first()

    def create_blog(self, blog: BlogModel) -> BlogModel:
        """
        Creates a new blog entry in the database.

        Args:
            blog (BlogModel): The blog model to create.

        Returns:
            BlogModel: The created blog model.
        """
        self._db_session.add(blog)
        self._db_session.flush()
        return blog

    def update_blog(self, blog: BlogModel, blog_data: dict) -> Optional[BlogModel]:
        """
        Updates a blog entry in the database.

        Args:
            blog (BlogModel): The blog model to update.
            blog_data (dict): Dictionary of fields to update.

        Returns:
            Optional[BlogModel]: The updated blog model.
        """
        for key, value in blog_data.items():
            setattr(blog, key, value)
        return blog

    def delete_blog(self, blog: BlogModel) -> None:
        """
        Deletes a blog entry from the database.

        Args:
            blog (BlogModel): The blog model to delete.
        """
        self._db_session.delete(instance=blog)

    def get_public_blogs(self, limit: int = 10, offset: int = 0) -> List[BlogModel]:
        """
        Fetches all public blogs with pagination support.

        Args:
            limit (int): Maximum number of blogs to retrieve. Defaults to 10.
            offset (int): Number of blogs to skip. Defaults to 0.

        Returns:
            List[BlogModel]: List of public blog models.
        """
        return self._db_session.query(BlogModel).filter(BlogModel.is_published == True).limit(limit=limit).offset(offset=offset).all()

    def get_blogs_by_user(self, user_id: int, limit: int, offset: int) -> List[BlogModel]:
        """
        Fetches all blogs by a specific user with pagination support.

        Args:
            user_id (int): The ID of the user whose blogs to retrieve.
            limit (int): Maximum number of blogs to retrieve.
            offset (int): Number of blogs to skip.

        Returns:
            List[BlogModel]: List of blog models by the user.
        """
        return self._db_session.query(BlogModel).filter(and_(BlogModel.user_id == user_id, BlogModel.is_published == True)).limit(limit=limit).offset(offset=offset).all()

    def count_blogs_by_user(self, user_id: int) -> int:
        """
        Counts the number of blogs by a specific user.

        Args:
            user_id (int): The ID of the user whose blogs to count.

        Returns:
            int: The number of blogs by the user.
        """
        return self._db_session.query(BlogModel).filter(BlogModel.user_id == user_id).count()

    def count_public_blogs(self) -> int:
        """
        Counts the number of public blogs.

        Returns:
            int: The number of public blogs.
        """
        return self._db_session.query(BlogModel).filter(BlogModel.is_published == True).count()