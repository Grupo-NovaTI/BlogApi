"""
Tag API routes for tag management endpoints.

This module defines FastAPI routes for creating, retrieving, updating, and deleting tags.
It uses dependency injection for service and authentication, and enforces admin-only access
for write operations.
"""

from typing import Optional

from fastapi import APIRouter, Path, Query, Request
from fastapi_cache.decorator import cache
from starlette import status

from app.core.dependencies import AccessTokenDependency, TagServiceDependency
from app.core.security.authentication_decorators import admin_only
from app.tags.schemas.tag_request import TagRequest
from app.tags.schemas.tag_response import TagResponse
from app.utils.constants.constants import DEFAULT_OFFSET, DEFAULT_PAGE_SIZE

tag_router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)


@tag_router.get(
    path="",
    response_model=list[TagResponse],
    summary="Get all tags",
    tags=["tags"],
    status_code=status.HTTP_200_OK
)
@cache(expire=60)
async def get_tags(
    request: Request,
    tag_service: TagServiceDependency,
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1),
    offset: int = Query(DEFAULT_OFFSET, ge=0)
):
    """
    Retrieve all tags.

    Args:
        tag_service (TagServiceDependency): The tag service dependency.
        limit (int): Maximum number of tags to retrieve.
        offset (int): Number of tags to skip.

    Returns:
        list[TagResponse]: List of tag data.

    Raises:
        HTTPException: If there is an error during retrieval.
    """
    return tag_service.get_tags(limit=limit, offset=offset)


@tag_router.get(
    path="/{tag_id}",
    response_model=Optional[TagResponse],
    summary="Get tag by ID",
    tags=["tags"],
    status_code=status.HTTP_200_OK
)
@cache(expire=60)
async def get_tag_by_id(
    request: Request,
    token: AccessTokenDependency,
    tag_service: TagServiceDependency,
    tag_id: int = Path(..., description="The unique identifier of the tag to retrieve")
):
    """
    Retrieve a tag by its ID.

    Args:
        token (AccessTokenDependency): The JWT payload dependency.
        tag_service (TagServiceDependency): The tag service dependency.
        tag_id (int): The unique identifier of the tag to retrieve.

    Returns:
        TagResponse: The tag data if found.

    Raises:
        HTTPException: If the tag is not found or if there is an error during retrieval.
    """
    return tag_service.get_tag_by_id(tag_id=tag_id)


@tag_router.post(
    path="",
    response_model=TagResponse,
    summary="Create a new tag",
    tags=["tags"],
    status_code=status.HTTP_201_CREATED
)
@admin_only()
async def create_tag(
    tag: TagRequest,
    token: AccessTokenDependency,
    tag_service: TagServiceDependency
):
    """
    Create a new tag.

    Args:
        tag (TagRequest): The data for the new tag.
        token (AccessTokenDependency): The JWT payload dependency.
        tag_service (TagServiceDependency): The tag service dependency.

    Returns:
        TagResponse: The created tag.

    Raises:
        HTTPException: If a tag with the same name already exists or if there is an error during creation.
    """
    return tag_service.create_tag(tag_data=tag.model_dump(exclude_unset=True))


@tag_router.put(
    path="/{tag_id}",
    response_model=TagResponse,
    summary="Update an existing tag",
    tags=["tags"],
    status_code=status.HTTP_200_OK
)
@admin_only()
async def update_tag(
    tag: TagRequest,
    token: AccessTokenDependency,
    tag_service: TagServiceDependency,
    tag_id: int = Path(..., description="The unique identifier of the tag to update")
):
    """
    Update an existing tag.

    Args:
        tag (TagRequest): The updated data for the tag.
        token (AccessTokenDependency): The JWT payload dependency.
        tag_service (TagServiceDependency): The tag service dependency.
        tag_id (int): The unique identifier of the tag to update.

    Returns:
        TagResponse: The updated tag.

    Raises:
        HTTPException: If the tag is not found or if there is an error during update.
    """
    return tag_service.update_tag(tag_data=tag.model_dump(exclude_defaults=True), tag_id=tag_id)


@tag_router.delete(
    path="/{tag_id}",
    summary="Delete a tag",
    tags=["tags"],
    status_code=status.HTTP_204_NO_CONTENT
)
@admin_only()
async def delete_tag(
    token: AccessTokenDependency,
    tag_service: TagServiceDependency,
    tag_id: int = Path(..., description="The unique identifier of the tag to delete")
):
    """
    Delete a tag by its ID.

    Args:
        token (AccessTokenDependency): The JWT payload dependency.
        tag_service (TagServiceDependency): The tag service dependency.
        tag_id (int): The unique identifier of the tag to delete.

    Returns:
        None

    Raises:
        HTTPException: If the tag is not found or if there is an error during deletion.
    """
    tag_service.delete_tag(tag_id=tag_id)
