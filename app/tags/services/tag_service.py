from typing import List, Optional
from app.tags.models.tag_model import TagModel
from app.tags.repositories.tag_repository import TagRepository
from app.tags.exceptions.tag_exceptions import TagNotFoundException, TagAlreadyExistsException
from app.utils.errors.error_messages import not_found_message, already_exists_message


class TagService:
    def __init__(self, tag_repository: TagRepository) -> None:
        self._repository: TagRepository = tag_repository

    def get_tags(self) -> List[TagModel]:
        """Retrieve all tags from the repository.
        Returns:
            List[TagModel]: A list of all tags.
        Raises:
            TagOperationException: If there is an error retrieving tags from the repository.
        """
        return self._repository.get_all_tags()

    def get_tag_by_id(self, tag_id: int) -> Optional[TagModel]:
        """Retrieve a tag by its ID.
        Args:
            tag_id (int): The unique identifier of the tag to retrieve.
        Returns:
            TagModel: The tag object if found.
        Raises:
            TagNotFoundException: If the tag with the given ID does not exist.
        """
        return self._repository.get_tag_by_id(tag_id=tag_id)

    def create_tag(self, tag: TagModel) -> TagModel:
        """
        Create a new tag in the repository.
        Args:
            tag_data: Data for the new tag.
        Returns:
            The created tag.
        Raises:
            TagAlreadyExistsException: If a tag with the same name already exists.
        """
        check_tag_exists: Optional[TagModel] = self._repository.get_tag_by_name(
            tag_name=str(tag.name))
        if check_tag_exists:
            raise TagAlreadyExistsException(already_exists_message(
                instance="tag",
                identifier=str(tag.name)))

        return self._repository.create_tag(tag=tag)

    def update_tag(self, tag_data: dict, tag_id: int) -> TagModel:
        """
        Update an existing tag in the repository.
        Args:
            tag_data: Updated data for the tag.
        Returns:
            TagModel: The updated tag.
        """
        tag_name: Optional[str] = tag_data.get("name")
        check_tag_exists_by_name: Optional[TagModel] = self._repository.get_tag_by_name(
            tag_name=str(tag_name))
        if check_tag_exists_by_name:
            raise TagAlreadyExistsException(
                already_exists_message(
                    instance="tag",
                    identifier=str(tag_name)
                )
            )
        updated_tag: Optional[TagModel] = self._repository.update_tag(
            tag_data=tag_data, tag_id=tag_id)
        if not updated_tag:
            raise TagNotFoundException(not_found_message(
                instance="tag",
                identifier=tag_id
            ))
        return updated_tag

    def delete_tag(self, tag_id: int) -> TagModel:
        """
        Delete a tag from the repository.
        Args:
            tag_id (int): The unique identifier of the tag to delete.
        Returns:
            TagModel: The deleted tag.
        """
        
        tag_result: Optional[TagModel] = self._repository.delete_tag(tag_id=tag_id)
        if not tag_result:
            raise TagNotFoundException(not_found_message(
                instance="tag",
                identifier=tag_id
            ))
        return tag_result

    def get_tag_by_name(self, tag_name: str) -> Optional[TagModel]:
        """
        Retrieve a tag by its name.
        Args:
            tag_name (str): The name of the tag to retrieve.
        Returns:
            TagModel: The tag object if found.
        Raises:
            TagNotFoundException: If the tag with the given name does not exist.
        """
        return self._repository.get_tag_by_name(tag_name=tag_name)