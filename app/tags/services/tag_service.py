from typing import List
from app.tags.models.tag_model import TagModel
from app.tags.repositories.tag_repository import TagRepository
from app.tags.exceptions.tag_exceptions import TagNotFoundException, TagAlreadyExistsException


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

    def get_tag_by_id(self, tag_id: int) -> TagModel | None:
        """Retrieve a tag by its ID.
        Args:
            tag_id (int): The unique identifier of the tag to retrieve.
        Returns:
            TagModel: The tag object if found.
        Raises:
            TagNotFoundException: If the tag with the given ID does not exist.
        """
        tag: TagModel | None = self._repository.get_tag_by_id(tag_id=tag_id)
        if not tag:
            raise TagNotFoundException(f"Tag with ID {tag_id} not found.")
        return tag

    def create_tag(self, tag_data: TagModel) -> TagModel:
        """
        Create a new tag in the repository.
        Args:
            tag_data: Data for the new tag.
        Returns:
            The created tag.
        Raises:
            TagAlreadyExistsException: If a tag with the same name already exists.
        """
        check_tag_exists: TagModel | None = self._repository.get_tag_by_name(
            tag_name=str(tag_data.name))
        if check_tag_exists:
            raise TagAlreadyExistsException(
                f"Tag with name {tag_data.name} already exists.")
        return self._repository.create_tag(tag=tag_data)

    def update_tag(self, tag_data: dict, tag_id: int) -> TagModel:
        """
        Update an existing tag in the repository.
        Args:
            tag_data: Updated data for the tag.
        Returns:
            TagModel: The updated tag.
        """
        existing_tag: TagModel | None = self._repository.get_tag_by_id(
            tag_id=tag_id)
        if not existing_tag:
            raise TagNotFoundException(f"Tag with ID {tag_id} not found.")
        tag_name = tag_data.get("name")
        check_tag_exists_by_name: TagModel | None = self._repository.get_tag_by_name(
            tag_name=str(tag_name))
        if check_tag_exists_by_name:
            raise TagAlreadyExistsException(
                f"Tag with name {tag_name} already exists.")
        return self._repository.update_tag(tag_data=tag_data, tag_id=tag_id)

    def delete_tag(self, tag_id: int) -> TagModel | None:
        """
        Delete a tag from the repository.
        Args:
            tag_id (int): The unique identifier of the tag to delete.
        Returns:
            TagModel: The deleted tag.
        """
        tag: TagModel | None = self._repository.get_tag_by_id(tag_id=tag_id)
        if not tag:
            raise TagNotFoundException(f"Tag with ID {tag_id} not found.")
        return self._repository.delete_tag(tag_id=tag_id)
