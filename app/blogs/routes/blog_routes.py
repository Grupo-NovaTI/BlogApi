# -*- coding: utf-8 -*-

from typing import List, Optional
from starlette import status
from fastapi import APIRouter, Request, Path, Query
from fastapi_cache.decorator import cache
from app.core.dependencies import BlogServiceDependency, AccessTokenDependency, UserIDFromTokenDependency
from app.blogs.schemas.blog_request import BlogRequest, BlogPatchRequest
from app.blogs.schemas.blog_response import BlogResponse, BlogResponseFull
from app.blogs.models.blog_model import BlogModel
from app.utils.constants.constants import DEFAULT_PAGE_SIZE, DEFAULT_OFFSET

blog_router = APIRouter(
    prefix="/blogs",
    tags=["blogs"],
)


@blog_router.get(path="", response_model=List[BlogResponseFull], tags=["blogs"], description="Get all blogs", status_code=status.HTTP_200_OK)
@cache(expire=60)  # Cache for 60 seconds
async def get_blogs(
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
    return blog_service.create_blog(blog=blog.model_dump(exclude_unset=True), author_id=user_id)


@blog_router.put(path="/{id}", response_model=BlogResponseFull, tags=["blogs"], description="Update a blog", status_code=status.HTTP_200_OK)
async def update_blog(
    id: int,
    blog: BlogRequest,
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
) -> BlogModel:
    return blog_service.update_blog(blog=blog.model_dump(exclude_unset=True), id=id, author_id=user_id)


@blog_router.delete(path="/{id}", response_model=BlogResponse, tags=["blogs"], description="Delete a blog", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    id: int,
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
):
    blog_service.delete_blog(blog_id=id, user_id=user_id)


@blog_router.patch(path="/{id}/visibility", response_model=BlogResponseFull, tags=["blogs"], description="Update blog visibility", status_code=status.HTTP_200_OK)
async def update_blog_visibility(
    id: int,
    visibility: bool,
    blog_service: BlogServiceDependency,
    user_id: UserIDFromTokenDependency,
) -> Optional[BlogModel]:
    return blog_service.update_blog_visibility(id=id, visibility=visibility, user_id=user_id)


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
    user_id_payload: UserIDFromTokenDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    return blog_service.get_blogs_by_user(user_id=user_id_payload, limit=limit, offset=offset)


@blog_router.patch(path="/{id}", response_model=BlogResponseFull, tags=["blogs"], description="Patch blog", status_code=status.HTTP_200_OK)
async def update_blog_content(
    blog: BlogPatchRequest,
    blog_service: BlogServiceDependency,
    author_id: UserIDFromTokenDependency,
    id: int = Path(..., description="The ID of the blog to update", gt=0),
) -> BlogModel:
    return blog_service.update_blog(blog=blog.model_dump(exclude_unset=True), id=id, author_id=author_id)


@blog_router.get(path="/{id}", response_model=Optional[BlogResponseFull], tags=["blogs"], description="Get blog by ID")
@cache(expire=60)  # Cache for 60 seconds
async def get_blog_by_id(
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
    id: int = Path(
        default=..., description="The ID of the blog to retrieve", ge=1),
) -> Optional[BlogModel]:
    return blog_service.get_blog_by_id(id=id)
