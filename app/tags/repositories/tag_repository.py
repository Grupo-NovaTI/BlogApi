"""
Repository layer for tag management.

This module defines the TagRepository class, which provides CRUD operations and queries
for tag entities in the database.
"""
from typing import List, Optional
from sqlalchemy.orm.session import Session
from app.tags.models.tag_model import TagModel
from sqlalchemy import or_

class TagRepository:
    """
    Repository class for managing tag entities in the database.

    Provides methods for creating, retrieving, updating, and deleting tags.
    """
    def __init__(self, db_session: Session) -> None:
        """
        Initialize the TagRepository with a database session.

        Args:
            db_session (Session): SQLAlchemy session for database operations.
        """
        self._db_session: Session = db_session

    def get_all_tags(self, limit: int = 10, offset: int = 0) -> List[TagModel]:
        """
        Retrieve all tags from the database with pagination.

        Args:
            limit (int): Maximum number of tags to retrieve. Defaults to 10.
            offset (int): Number of tags to skip. Defaults to 0.

        Returns:
            List[TagModel]: List of tag objects.
        """
        return self._db_session.query(TagModel).limit(limit=limit).offset(offset=offset).all()

    def get_tag_by_id(self, tag_id: int) -> Optional[TagModel]:
        """
        Retrieve a tag by its ID from the database.

        Args:
            tag_id (int): The unique identifier of the tag to retrieve.

        Returns:
            Optional[TagModel]: The tag object if found, otherwise None.
        """
        return self._db_session.query(TagModel).filter(TagModel.id == tag_id).first()

    def get_tag_by_name(self, tag_name: str) -> Optional[TagModel]:
        """
        Retrieve a tag by its name from the database.

        Args:
            tag_name (str): The name of the tag to retrieve.

        Returns:
            Optional[TagModel]: The tag object if found, otherwise None.
        """
        return self._db_session.query(TagModel).filter(TagModel.name == tag_name).first()

    def create_tag(self, tag: TagModel) -> TagModel:
        """
        Create a new tag in the database.

        Args:
            tag (TagModel): The tag object to create.

        Returns:
            TagModel: The created tag object.
        """
        self._db_session.add(tag)
        self._db_session.flush()
        return tag

    def update_tag(self, tag: TagModel, tag_data: dict) -> Optional[TagModel]:
        """
        Update an existing tag in the database.

        Args:
            tag (TagModel): The tag object with updated information.
            tag_data (dict): Dictionary of fields to update.

        Returns:
            TagModel: The updated tag object.
        """
        for key, value in tag_data.items():
            setattr(tag, key, value)
        return tag

    def delete_tag(self, tag: TagModel) -> None:
        """
        Delete a tag by its ID from the database.

        Args:
            tag (TagModel): The tag object to delete.
        """
        self._db_session.delete(instance=tag)

    def get_tag_by_id_or_name(self, tag_id: int, tag_name: str) -> Optional[TagModel]:
        """
        Retrieve a tag by its ID or name from the database.

        Args:
            tag_id (int): The unique identifier of the tag.
            tag_name (str): The name of the tag.

        Returns:
            Optional[TagModel]: The tag object if found, otherwise None.
        """
        return self._db_session.query(TagModel).filter(or_(TagModel.id == tag_id, TagModel.name == tag_name)).first()