from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from app.tags.exceptions.tag_exceptions import TagOperationException
from app.tags.models.tag_model import TagModel
from app.utils.logger.application_logger import ApplicationLogger
from app.utils.errors.error_messages import database_error_message, unknown_error_message

_logger = ApplicationLogger(__name__)

class TagRepository:
    def __init__(self, db: Session) -> None:
        self._db_session: Session = db

    def get_all_tags(self, limit: int = 10, offset: int = 0) -> List[TagModel]:
        try:
            return self._db_session.query(TagModel).limit(limit=limit).offset(offset=offset).all()
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(operation="retrieving", instance="all tags", exception=e))
            raise TagOperationException(
                database_error_message(operation="retrieving", instance="all tags", exception=e)
            )
        except Exception as e:
            _logger.log_error(message=unknown_error_message(operation="retrieving", instance="all tags", exception=e))
            raise TagOperationException(
                unknown_error_message(operation="retrieving", instance="all tags")
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
        try:
            return self._db_session.query(
                TagModel).filter(TagModel.id == tag_id).first()
        except SQLAlchemyError as e:
            _logger.log_error(message=database_error_message(operation="retrieving", instance="tag", exception=e))
            raise TagOperationException(
                database_error_message(operation="retrieving", instance="tag", exception=e)
            )
        except Exception as e:
            _logger.log_error(message=unknown_error_message(operation="retrieving", instance="tag", exception=e))
            raise TagOperationException(
                unknown_error_message(operation="retrieving", instance="tag", exception=e)
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
        try:
            return self._db_session.query(
                TagModel).filter(TagModel.name == tag_name).first()

        except SQLAlchemyError as e:
            _logger.log_error(message=database_error_message(operation="retrieving", instance="tag by name", exception=e))
            raise TagOperationException(
                database_error_message(operation="retrieving", instance="tag by name", exception=e)
            )
        except Exception as e:
            _logger.log_error(message=unknown_error_message(operation="retrieving", instance="tag by name", exception=e))
            raise TagOperationException(
                unknown_error_message(operation="retrieving", instance="tag by name", exception=e)
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
        try:
            self._db_session.add(tag)
            self._db_session.commit()
            self._db_session.refresh(tag)
            return tag
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(operation="creating", instance="tag", exception=e))
            raise TagOperationException(
                database_error_message(operation="creating", instance="tag", exception=e)
            )
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(message=unknown_error_message(operation="creating", instance="tag", exception=e))
            raise TagOperationException(
                unknown_error_message(operation="creating", instance="tag", exception=e)
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
        try:
            rows_affected : int = self._db_session.query(TagModel).filter(
                TagModel.id == tag_id
            ).update(tag_data)
            if rows_affected == 0:
                return None 
            self._db_session.commit()
            return self.get_tag_by_id(tag_id)
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(operation="updating", instance="tag", exception=e))
            raise TagOperationException(
                database_error_message(operation="updating", instance="tag", exception=e)
            )
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(message=unknown_error_message(operation="updating", instance="tag", exception=e))
            raise TagOperationException(
                unknown_error_message(operation="updating", instance="tag", exception=e)
            )

    def delete_tag(self, tag_id: int) -> Optional[TagModel]:
        """
        Delete a tag by its ID from the database.

        Args:
            tag_id (int): The unique identifier of the tag to delete.

        Raises:
            TagOperationException: If there is a database error during deletion.
        """
        try:
            target_tag: Optional[TagModel] = self.get_tag_by_id(tag_id=tag_id)
            rows_affected :int = self._db_session.query(TagModel).filter(
                TagModel.id == tag_id
            ).delete()
            if rows_affected == 0 or not target_tag:
                return None 
            self._db_session.commit()
            return target_tag
        except SQLAlchemyError as e:
            self._db_session.rollback()
            _logger.log_error(message=database_error_message(operation="deleting", instance="tag", exception=e))
            raise TagOperationException(
                database_error_message(operation="deleting", instance="tag", exception=e)
            )
        except Exception as e:
            self._db_session.rollback()
            _logger.log_error(message=unknown_error_message(operation="deleting", instance="tag", exception=e))
            raise TagOperationException(
                unknown_error_message(operation="deleting", instance="tag", exception=e)
            )

    