# -*- coding: utf-8 -*-

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
@cache(expire=60)  # Cache for 60 seconds
async def get_all_blogs(
    request: Request,
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=100),
    offset: int = Query(default=DEFAULT_OFFSET, ge=0),
) -> List[BlogModel]:

    return blog_service.get_all_blogs(limit=limit, offset=offset)


@blog_router.get(path="/public", response_model=List[BlogResponseFull], tags=["blogs"], description="Get public blogs", status_code=status.HTTP_200_OK)
async def get_public_blogs(
    blog_service: BlogServiceDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    """
    Fetch public blogs with pagination.
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
This endpoint allows users to create a new blog post by providing the necessary details in the request body.
"""
    return blog_service.create_blog(blog=blog.model_dump(exclude_unset=True), user_id=user_id)


@blog_router.delete(path="/{blog_id}", tags=["blogs"], description="Delete a blog", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: int,
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
):
    blog_service.delete_blog(blog_id=blog_id, user_id=user_id)


@blog_router.patch(path="/{blog_id}", response_model=BlogResponseFull, tags=["blogs"], description="Patch blog", status_code=status.HTTP_200_OK)
async def patch_blog(
    blog: BlogPatchRequest,
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
    blog_id: int = Path(..., description="The ID of the blog to update", gt=0),
) -> BlogModel:
    return blog_service.patch_blog(blog=blog.model_dump(exclude_unset=True), blog_id=blog_id, user_id=user_id)


@blog_router.get(path="/user/{user_id}", response_model=List[BlogResponseFull], tags=["blogs"], description="Get blogs by user", status_code=status.HTTP_200_OK)
async def get_blogs_by_user(
    user_id: int,
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    return blog_service.get_blogs_by_user(user_id=user_id, limit=limit, offset=offset)


@blog_router.get(path="/users/me", response_model=List[BlogResponseFull], tags=["blogs"], description="Get blogs by current user", status_code=status.HTTP_200_OK)
async def get_blogs_by_current_user(
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    return blog_service.get_blogs_by_user(user_id=user_id, limit=limit, offset=offset)


@blog_router.patch(path="/{blog_id}", response_model=BlogResponseFull, tags=["blogs"], description="Patch blog", status_code=status.HTTP_200_OK)
async def update_blog_content(
    blog: BlogPatchRequest,
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
    blog_id: int = Path(..., description="The ID of the blog to update", gt=0),
) -> BlogModel:
    return blog_service.update_blog(blog=blog.model_dump(exclude_unset=True), blog_id=blog_id, user_id=user_id)


@blog_router.get(path="/{blog_id}", response_model=Optional[BlogResponseFull], tags=["blogs"], description="Get blog by ID")
@cache(expire=.6)  # Cache for 60 seconds
async def get_blog_by_id(
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
    blog_id: int = Path(
        default=..., description="The ID of the blog to retrieve", ge=1),
) -> Optional[BlogModel]:
    return blog_service.get_blog_by_id(blog_id=blog_id)