from typing import List, Optional
from sqlalchemy.orm.session import Session
from app.tags.models.tag_model import TagModel
from sqlalchemy import or_

class TagRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session: Session = db_session

    def get_all_tags(self, limit: int = 10, offset: int = 0) -> List[TagModel]:
        return self._db_session.query(TagModel).limit(limit=limit).offset(offset=offset).all()

 
    def get_tag_by_id(self, tag_id: int) -> Optional[TagModel]:
        """
        Retrieve a tag by its ID from the database.

        Args:
            tag_id (int): The unique identifier of the tag to retrieve.

        Returns:
            TagModel: The tag object if found.

        Raises:
            TagOperationException: If there is a database error during retrieval.
        """
        return self._db_session.query(
                TagModel).filter(TagModel.id == tag_id).first()
        

    def get_tag_by_name(self, tag_name: str) -> Optional[TagModel]:
        """
        Retrieve a tag by its name from the database.

        Args:
            tag_name (str): The name of the tag to retrieve.

        Returns:
            Optional[TagModel]: The tag object if found, otherwise None.

        Raises:
            TagOperationException: If there is a database error during retrieval.
        """
        return self._db_session.query(
            TagModel).filter(TagModel.name == tag_name).first()
    
    def create_tag(self, tag: TagModel) -> TagModel:
        """
        Create a new tag in the database.

        Args:
            tag (TagModel): The tag object to create.

        Returns:
            TagModel: The created tag object.

        Raises:
            TagOperationException: If there is a database error during creation.
        """
        self._db_session.add(tag)
        self._db_session.flush()
        return tag
    
    
    def update_tag(self, tag: TagModel, tag_data: dict) -> Optional[TagModel]:
        """
        Update an existing tag in the database.

        Args:
            tag (TagModel): The tag object with updated information.

        Returns:
            TagModel: The updated tag object.

        Raises:
            TagOperationException: If there is a database error during update.
        """
        for key, value in tag_data.items():
            setattr(tag, key, value)
        return tag

    def delete_tag(self, tag: TagModel) -> None:
        """
        Delete a tag by its ID from the database.

        Args:
            tag (TagModel): The tag object to delete.

        Raises:
            TagOperationException: If there is a database error during deletion.
        """
        self._db_session.delete(instance=tag)

    def get_tag_by_id_or_name(self, tag_id: int, tag_name: str) -> Optional[TagModel]:
        return self._db_session.query(TagModel).filter(or_(TagModel.id == tag_id, TagModel.name == tag_name)).first()