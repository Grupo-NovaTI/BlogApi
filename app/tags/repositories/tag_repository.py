from typing import List
from sqlalchemy.orm.session import Session
from tags.exceptions.tag_exceptions import TagOperationException
from tags.models.tag_model import TagModel


class TagRepository:
    def __init__(self, db: Session) -> None:
        self._db_session: Session = db

    def get_all_tags(self, limit: int = 10, offset: int = 0) -> List[TagModel]:
        try:
            return self._db_session.query(TagModel).limit(limit=limit).offset(offset=offset).all()
        except Exception as e:
            raise TagOperationException(
                f"Error on retrieving all tags: {str(e)}"
            )

    def get_tag_by_id(self, tag_id: int) -> TagModel | None:
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

        except Exception as e:
            raise TagOperationException(
                f"Error on retrieving tag by ID: {str(e)}"
            )

    def get_tag_by_name(self, tag_name: str) -> TagModel | None:
        """
        Retrieve a tag by its name from the database.

        Args:
            tag_name (str): The name of the tag to retrieve.

        Returns:
            TagModel: The tag object if found.

        Raises:
            TagOperationException: If there is a database error during retrieval.
        """
        try:
            return self._db_session.query(
                TagModel).filter(TagModel.name == tag_name).first()

        except Exception as e:
            raise TagOperationException(
                f"Error on retrieving tag by name: {str(e)}"
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
            return tag
        except Exception as e:
            raise TagOperationException(
                f"Error on creating tag: {str(e)}"
            )
    def update_tag(self, tag: TagModel) -> TagModel:
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
            self._db_session.merge(tag)
            self._db_session.commit()
            return tag
        except Exception as e:
            raise TagOperationException(
                f"Error on updating tag: {str(e)}"
            )
        
    def delete_tag(self, tag_id: int) -> TagModel | None:
        """
        Delete a tag by its ID from the database.

        Args:
            tag_id (int): The unique identifier of the tag to delete.

        Raises:
            TagOperationException: If there is a database error during deletion.
        """
        try:
            tag: TagModel | None = self.get_tag_by_id(tag_id)
            if tag:
                self._db_session.delete(tag)
                self._db_session.commit()
                return tag
            else:
                raise TagOperationException("Tag not found")
        except Exception as e:
            raise TagOperationException(
                f"Error on deleting tag: {str(e)}"
            )