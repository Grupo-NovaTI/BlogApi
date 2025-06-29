from fastapi import APIRouter, Depends, HTTPException

from app.tags.schemas.tag_response import TagResponse
from app.tags.schemas.tag_request import TagRequest
from app.tags.exceptions.tag_exceptions import TagOperationException, TagNotFoundException, TagAlreadyExistsException
from app.core.dependencies import TagServiceDependency, AccessTokenDependency

tag_router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)


@tag_router.get(path="", response_model=list[TagResponse], summary="Get all tags", tags=["tags"])
async def get_tags(tag_service: TagServiceDependency, token: AccessTokenDependency):
    """
    Retrieve all tags.

    Raises:
        HTTPException: If there is an error during retrieval.
    """
    try:
        return tag_service.get_tags()

    except TagOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred.")


@tag_router.get(path="/{tag_id}", response_model=TagResponse, summary="Get tag by ID", tags=["tags"])
async def get_tag_by_id(tag_id: int, token: AccessTokenDependency, tag_service: TagServiceDependency):
    """
    Retrieve a tag by its ID.

    Args:
        tag_id (int): The unique identifier of the tag to retrieve.

    Returns:
        TagResponse: The tag data if found.

    Raises:
        HTTPException: If the tag is not found or if there is an error during retrieval.
    """
    try:
        return tag_service.get_tag_by_id(tag_id=tag_id)
    except TagNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TagOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))


@tag_router.post(path="", response_model=TagResponse, summary="Create a new tag", tags=["tags"])
async def create_tag(tag_data: TagRequest, token: AccessTokenDependency, tag_service: TagServiceDependency):
    """
    Create a new tag.

    Args:
        tag_data (TagRequest): The data for the new tag.

    Returns:
        TagResponse: The created tag.

    Raises:
        HTTPException: If a tag with the same name already exists or if there is an error during creation.
    """
    try:
        return tag_service.create_tag(tag_data=tag_data.to_model())
    except TagAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TagOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))


@tag_router.put(path="/{tag_id}", response_model=TagResponse, summary="Update an existing tag", tags=["tags"])
async def update_tag(tag_id: int, tag_data: TagRequest, token: AccessTokenDependency, tag_service: TagServiceDependency):
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
    try:
        return tag_service.update_tag(tag_data=tag_data.to_model(), tag_id=tag_id)
    except TagNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TagOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))


@tag_router.delete(path="/{tag_id}", response_model=TagResponse, summary="Delete a tag", tags=["tags"])
async def delete_tag(tag_id: int, token: AccessTokenDependency, tag_service: TagServiceDependency):
    """
    Delete a tag by its ID.

    Args:
        tag_id (int): The unique identifier of the tag to delete.

    Returns:
        TagResponse: The deleted tag data.

    Raises:
        HTTPException: If the tag is not found or if there is an error during deletion.
    """
    try:
        return tag_service.delete_tag(tag_id=tag_id)
    except TagNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TagOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
