"""
Blog API routes for blog management endpoints.

This module defines FastAPI routes for creating, retrieving, updating, and deleting blogs.
It uses dependency injection for service and authentication, and supports caching for some endpoints.
"""

from typing import List, Optional

from fastapi import APIRouter, Path, Query, Request
from fastapi_cache.decorator import cache
from starlette import status

from app.blogs.models.blog_model import BlogModel
from app.blogs.schemas.blog_request import BlogPatchRequest, BlogRequest
from app.blogs.schemas.blog_response import BlogResponse, BlogResponseFull
from app.core.dependencies import (AccessTokenDependency,
                                   BlogServiceDependency,
                                   UserIDFromTokenDependency)
from app.utils.constants.constants import DEFAULT_OFFSET, DEFAULT_PAGE_SIZE

blog_router = APIRouter(
    prefix="/blogs",
    tags=["blogs"],
)


@blog_router.get(path="", response_model=List[BlogResponseFull], tags=["blogs"], description="Get all blogs", status_code=status.HTTP_200_OK)
@cache(expire=60)
async def get_all_blogs(
    request: Request,
    blog_service: BlogServiceDependency,
    token: AccessTokenDependency,
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=100),
    offset: int = Query(default=DEFAULT_OFFSET, ge=0),
) -> List[BlogModel]:
    """
    Retrieve all blogs with pagination.

    Args:
        request (Request): The FastAPI request object.
        blog_service (BlogServiceDependency): The blog service dependency.
        token (AccessTokenDependency): The JWT payload containing user information.
        limit (int): Maximum number of blogs to retrieve.
        offset (int): Number of blogs to skip.

    Returns:
        List[BlogModel]: List of blog models.
    """
    return blog_service.get_all_blogs(limit=limit, offset=offset)


@blog_router.get(path="/public", response_model=List[BlogResponseFull], tags=["blogs"], description="Get public blogs", status_code=status.HTTP_200_OK)
async def get_public_blogs(
    blog_service: BlogServiceDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    """
    Fetch public blogs with pagination.

    Args:
        blog_service (BlogServiceDependency): The blog service dependency.
        limit (int): Maximum number of blogs to retrieve.
        offset (int): Number of blogs to skip.

    Returns:
        List[BlogModel]: List of public blog models.
    """
    return blog_service.get_public_blogs(limit=limit, offset=offset)


@blog_router.post(path="", response_model=BlogResponseFull, tags=["blogs"], description="Create a new blog", status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: BlogRequest,
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
) -> BlogModel:
    """
    Create a new blog post.

    Args:
        blog (BlogRequest): The request body containing the blog details.
        blog_service (BlogServiceDependency): The blog service dependency.
        user_id (int): The ID of the user creating the blog.

    Returns:
        BlogModel: The created blog model.
    """
    return blog_service.create_blog(blog_data=blog.model_dump(exclude_unset=True), user_id=user_id)


@blog_router.delete(path="/{blog_id}", tags=["blogs"], description="Delete a blog", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: int,
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
):
    """
    Delete a blog by its ID.

    Args:
        blog_id (int): The ID of the blog to delete.
        blog_service (BlogServiceDependency): The blog service dependency.
        user_id (int): The ID of the user deleting the blog.
    """
    blog_service.delete_blog_for_user(blog_id=blog_id, user_id=user_id)


@blog_router.patch(path="/{blog_id}", response_model=BlogResponseFull, tags=["blogs"], description="Patch blog", status_code=status.HTTP_200_OK)
async def patch_blog(
    blog: BlogPatchRequest,
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
    blog_id: int = Path(..., description="The ID of the blog to update", gt=0),
) -> BlogModel:
    """
    Patch (partially update) a blog post.

    Args:
        blog (BlogPatchRequest): The request body containing the updated blog details.
        blog_service (BlogServiceDependency): The blog service dependency.
        user_id (int): The ID of the user updating the blog.
        blog_id (int): The ID of the blog to update.

    Returns:
        BlogModel: The updated blog model.
    """
    return blog_service.update_blog(blog_data=blog.model_dump(exclude_unset=True), blog_id=blog_id, user_id=user_id)


@blog_router.get(path="/user/{user_id}", response_model=List[BlogResponseFull], tags=["blogs"], description="Get blogs by user", status_code=status.HTTP_200_OK)
async def get_blogs_by_user(
    user_id: int,
    blog_service: BlogServiceDependency,
    token: AccessTokenDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    """
    Retrieve all blogs by a specific user.

    Args:
        user_id (int): The ID of the user whose blogs to retrieve.
        blog_service (BlogServiceDependency): The blog service dependency.
        token (AccessTokenDependency): The JWT payload containing user information.
        limit (int): Maximum number of blogs to retrieve.
        offset (int): Number of blogs to skip.

    Returns:
        List[BlogModel]: List of blog models by the user.
    """
    return blog_service.get_blogs_by_user(user_id=user_id, limit=limit, offset=offset)


@blog_router.get(path="/users/me", response_model=List[BlogResponseFull], tags=["blogs"], description="Get blogs by current user", status_code=status.HTTP_200_OK)
async def get_blogs_by_current_user(
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    """
    Retrieve all blogs by the current user.

    Args:
        blog_service (BlogServiceDependency): The blog service dependency.
        user_id (int): The ID of the current user.
        limit (int): Maximum number of blogs to retrieve.
        offset (int): Number of blogs to skip.

    Returns:
        List[BlogModel]: List of blog models by the current user.
    """
    return blog_service.get_blogs_by_user(user_id=user_id, limit=limit, offset=offset)


@blog_router.patch(path="/{blog_id}", response_model=BlogResponseFull, tags=["blogs"], description="Patch blog", status_code=status.HTTP_200_OK)
async def update_blog_content(
    blog: BlogPatchRequest,
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
    blog_id: int = Path(..., description="The ID of the blog to update", gt=0),
) -> BlogModel:
    """
    Update the content of a blog post.

    Args:
        blog (BlogPatchRequest): The request body containing the updated blog details.
        blog_service (BlogServiceDependency): The blog service dependency.
        user_id (int): The ID of the user updating the blog.
        blog_id (int): The ID of the blog to update.

    Returns:
        BlogModel: The updated blog model.
    """
    return blog_service.update_blog(blog_data=blog.model_dump(exclude_unset=True), blog_id=blog_id, user_id=user_id)


@blog_router.get(path="/{blog_id}", response_model=Optional[BlogResponseFull], tags=["blogs"], description="Get blog by ID")
@cache(expire=60)  # Cache for 60 seconds
async def get_blog_by_id(
    blog_service: BlogServiceDependency,
    token: AccessTokenDependency,
    blog_id: int = Path(
        default=..., description="The ID of the blog to retrieve", ge=1),
) -> Optional[BlogModel]:
    """
    Retrieve a blog by its ID.

    Args:
        blog_service (BlogServiceDependency): The blog service dependency.
        token (AccessTokenDependency): The JWT payload containing user information.
        blog_id (int): The ID of the blog to retrieve.

    Returns:
        Optional[BlogModel]: The requested blog model if found, otherwise None.
    """
    return blog_service.get_blog_by_id(blog_id=blog_id)