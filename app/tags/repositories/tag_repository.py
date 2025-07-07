from typing import List, Optional
from sqlalchemy.orm.session import Session
from app.utils.errors.exception_handlers import handle_database_exception
from app.tags.models.tag_model import TagModel
from app.utils.logger.application_logger import ApplicationLogger
from app.utils.enums.operations import Operations
from sqlalchemy import or_
_logger = ApplicationLogger(__name__)

_MODEL = "Tag"
class TagRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session: Session = db_session

    @handle_database_exception(
        model = _MODEL,
        operation=Operations.FETCH
    )
    def get_all_tags(self, limit: int = 10, offset: int = 0) -> List[TagModel]:
        return self._db_session.query(TagModel).limit(limit=limit).offset(offset=offset).all()

    @handle_database_exception(
        model = _MODEL,
        operation=Operations.FETCH_BY
    )
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
        
    @handle_database_exception(
         model = _MODEL,
        operation=Operations.FETCH
    )
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
    
    @handle_database_exception(
         model = _MODEL,
        operation=Operations.CREATE
    )
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
        self._db_session.commit()
        self._db_session.refresh(tag)
        return tag
    @handle_database_exception(
         model = _MODEL,
        operation=Operations.UPDATE
    )
    def update_tag(self, tag_id : int, tag_data: dict) -> Optional[TagModel]:
        """
        Update an existing tag in the database.

        Args:
            tag (TagModel): The tag object with updated information.

        Returns:
            TagModel: The updated tag object.

        Raises:
            TagOperationException: If there is a database error during update.
        """
        rows_affected : int = self._db_session.query(TagModel).filter(
            TagModel.id == tag_id
        ).update(tag_data)
        if rows_affected == 0:
            return None 
        self._db_session.commit()
        return self.get_tag_by_id(tag_id)

    @handle_database_exception(
         model = _MODEL,
        operation=Operations.DELETE
    )
    def delete_tag(self, tag_id: int) -> Optional[TagModel]:
        """
        Delete a tag by its ID from the database.

        Args:
            tag_id (int): The unique identifier of the tag to delete.

        Raises:
            TagOperationException: If there is a database error during deletion.
        """
        target_tag: Optional[TagModel] = self.get_tag_by_id(tag_id=tag_id)
        if not target_tag:
            return None
        self._db_session.delete(instance=target_tag)
        self._db_session.commit()
        return target_tag
    @handle_database_exception(
         model = _MODEL,
        operation=Operations.FETCH
    )
    def get_tag_by_id_or_name(self, tag_id: int, tag_name: str) -> Optional[TagModel]:
            return self._db_session.query(TagModel).filter(or_(TagModel.id == tag_id, TagModel.name == tag_name)).first()