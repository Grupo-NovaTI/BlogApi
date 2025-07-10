from typing import Optional
from fastapi import APIRouter, Path, Query
from starlette import status
from app.tags.schemas.tag_response import TagResponse
from app.tags.schemas.tag_request import TagRequest
from app.core.dependencies import TagServiceDependency, AccessTokenDependency
from app.core.security.authentication_decorators import admin_only
from app.utils.constants.constants import DEFAULT_OFFSET, DEFAULT_PAGE_SIZE

tag_router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)


@tag_router.get(path="", response_model=list[TagResponse], summary="Get all tags", tags=["tags"], status_code=status.HTTP_200_OK)
async def get_tags(tag_service: TagServiceDependency, limit: int = Query(DEFAULT_PAGE_SIZE, ge=1), offset: int = Query(DEFAULT_OFFSET, ge=0)):
    """
    Retrieve all tags.

    Raises:
        HTTPException: If there is an error during retrieval.
    """
    return tag_service.get_tags(limit=limit, offset=offset)


@tag_router.get(path="/{tag_id}", response_model=Optional[TagResponse], summary="Get tag by ID", tags=["tags"], status_code=status.HTTP_200_OK)
async def get_tag_by_id(jwt_payload: AccessTokenDependency, tag_service: TagServiceDependency, tag_id: int = Path(..., description="The unique identifier of the tag to retrieve")):
    """
    Retrieve a tag by its ID.

    Args:
        tag_id (int): The unique identifier of the tag to retrieve.

    Returns:
        TagResponse: The tag data if found.

    Raises:
        HTTPException: If the tag is not found or if there is an error during retrieval.
    """
    return tag_service.get_tag_by_id(tag_id=tag_id)

@admin_only()
@tag_router.post(path="", response_model=TagResponse, summary="Create a new tag", tags=["tags"], status_code=status.HTTP_201_CREATED)
async def create_tag(tag: TagRequest, jwt_payload: AccessTokenDependency, tag_service: TagServiceDependency):
    """
    Create a new tag.

    Args:
        tag_data (TagRequest): The data for the new tag.

    Returns:
        TagResponse: The created tag.

    Raises:
        HTTPException: If a tag with the same name already exists or if there is an error during creation.
    """
    return tag_service.create_tag(tag=tag.model_dump(exclude_unset=True))

@admin_only()
@tag_router.put(path="/{tag_id}", response_model=TagResponse, summary="Update an existing tag", tags=["tags"], status_code=status.HTTP_200_OK)
async def update_tag(tag_data: TagRequest, jwt_payload: AccessTokenDependency, tag_service: TagServiceDependency, tag_id: int = Path(..., description="The unique identifier of the tag to update")):
    """
    Update an existing tag.

    Args:
        tag_id (int): The unique identifier of the tag to update.
        tag_data (TagRequest): The updated data for the tag.

    Returns:
        TagResponse: The updated tag.

    Raises:
        HTTPException: If the tag is not found or if there is an error during update.
    """
    return tag_service.update_tag(tag_data=tag_data.model_dump(exclude_defaults=True), tag_id=tag_id)

@admin_only()
@tag_router.delete(path="/{tag_id}", summary="Delete a tag", tags=["tags"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(jwt_payload: AccessTokenDependency, tag_service: TagServiceDependency, tag_id: int = Path(..., description="The unique identifier of the tag to delete"),):
    """
    Delete a tag by its ID.

    Args:
        tag_id (int): The unique identifier of the tag to delete.

    Returns:
        TagResponse: The deleted tag data.

    Raises:
        HTTPException: If the tag is not found or if there is an error during deletion.
    """
    tag_service.delete_tag(tag_id=tag_id)
