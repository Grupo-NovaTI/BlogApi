from typing import Optional
from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status
from app.tags.schemas.tag_response import TagResponse
from app.tags.schemas.tag_request import TagRequest
from app.tags.exceptions.tag_exceptions import TagOperationException, TagNotFoundException, TagAlreadyExistsException
from app.core.dependencies import TagServiceDependency, AccessTokenDependency
from app.utils.consts.consts import DEFAULT_OFFSET, DEFAULT_PAGE_SIZE

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
    try:
        return tag_service.get_tags(limit=limit, offset=offset)

    except TagOperationException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


@tag_router.get(path="/{tag_name}", response_model=Optional[TagResponse], summary="Get a tag by Name", tags=["tags"], status_code=status.HTTP_200_OK)
async def get_tag_by_name(jwt_payload: AccessTokenDependency, tag_service: TagServiceDependency, tag_name: str = Path(..., description="The name of the tag to retrieve", min_length=1, max_length=100)):
    """
    Get a tag by its name.

    Args:
        tag_name (str): The name of the tag to retrieve.

    Returns:
        int: The total count of tags.

    Raises:
        HTTPException: If there is an error during counting.
    """
    try:
        return tag_service.get_tag_by_name(tag_name=tag_name)
    except TagOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred.")


@tag_router.get(path="/{tag_id}", response_model=TagResponse, summary="Get tag by ID", tags=["tags"], status_code=status.HTTP_200_OK)
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
    try:
        return tag_service.get_tag_by_id(tag_id=tag_id)
    except TagNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TagOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


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
    try:
        return tag_service.create_tag(tag=tag.to_orm())
    except TagAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TagOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


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
    try:
        return tag_service.update_tag(tag_data=tag_data.to_orm(), tag_id=tag_id)
    except TagNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TagOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@tag_router.delete(path="/{tag_id}", response_model=TagResponse, summary="Delete a tag", tags=["tags"], status_code=status.HTTP_200_OK)
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
    try:
        return tag_service.delete_tag(tag_id=tag_id)
    except TagNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TagOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
