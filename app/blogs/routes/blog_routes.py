import time
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from app.blogs.exceptions.blog_exceptions import BlogNotFoundException, BlogOperationException
from app.core.dependencies import BlogServiceDependency,AccessTokenDependency
from app.blogs.schemas.blog_request import BlogRequest
from app.blogs.schemas.blog_response import BlogResponse, BlogResponseFull
from app.blogs.models.blog_model import BlogModel
from app.utils.consts.consts import DEFAULT_PAGE_SIZE, DEFAULT_OFFSET
from app.core.security.authentication_decorators import authentication_required
from fastapi_cache.decorator import cache

blog_router = APIRouter(
    prefix="/blogs",
    tags=["blogs"],
    responses={404: {"description": "Not found"}},
)


@blog_router.get(path="", response_model=List[BlogResponseFull], tags=["blogs"], description="Get all blogs")
@cache(expire=60)  # Cache for 60 seconds
async def get_blogs(
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    try:
        time.sleep(2)  # Simulate a delay for demonstration purposes
        return blog_service.get_all_blogs(limit=limit, offset=offset)
    except BlogOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@blog_router.get(path="/{id}", response_model=Optional[BlogResponseFull], tags=["blogs"], description="Get blog by ID")
async def get_blog_by_id(
    id: int,
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
) -> Optional[BlogModel]:
    try:
        return blog_service.get_blog_by_id(id=id)
    except BlogNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BlogOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@blog_router.post(path="", response_model=BlogResponseFull, tags=["blogs"], description="Create a new blog")
async def create_blog(
    blog: BlogRequest,
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
) -> BlogModel:
    """
Create a new blog post.
This endpoint allows users to create a new blog post by providing the necessary details in the request body.
"""
    try:
        return blog_service.create_blog(blog=BlogModel(**blog.model_dump()))
    except BlogOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")


@blog_router.put(path="/{id}", response_model=BlogResponseFull, tags=["blogs"], description="Update a blog")
async def update_blog(
    id: int,
    blog: BlogRequest,
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
) -> BlogModel:
    try:
        return blog_service.update_blog(blog=blog.model_dump(), id=id)
    except BlogNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BlogOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@blog_router.delete(path="/{id}", response_model=BlogResponse, tags=["blogs"], description="Delete a blog")
async def delete_blog(
    id: int,
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
) -> BlogModel:
    try:
        return blog_service.delete_blog(blog_id=id)
    except BlogNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BlogOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@blog_router.patch(path="/{id}/visibility", response_model=BlogResponseFull, tags=["blogs"], description="Update blog visibility")
async def update_blog_visibility(
    id: int,
    visibility: bool,
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
) -> Optional[BlogModel]:
    try:
        return blog_service.update_blog_visibility(id=id, visibility=visibility)
    except BlogNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BlogOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@blog_router.get(path="/public", response_model=List[BlogResponseFull], tags=["blogs"], description="Get public blogs")
async def get_public_blogs(
    blog_service: BlogServiceDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    try:
        return blog_service.get_public_blogs(limit=limit, offset=offset)
    except BlogOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@blog_router.get(path="/user/{user_id}", response_model=List[BlogResponseFull], tags=["blogs"], description="Get blogs by user")
async def get_blogs_by_user(
    user_id: int,

    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    try:
        return blog_service.get_blogs_by_user(user_id=user_id, limit=limit, offset=offset)
    except BlogOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error {str(e)}")


@blog_router.get(path="/users/me", response_model=List[BlogResponseFull], tags=["blogs"], description="Get blogs by current user")
@authentication_required()
async def get_blogs_by_current_user(
    blog_service: BlogServiceDependency,
    jwt_payload: AccessTokenDependency,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = DEFAULT_OFFSET,
) -> List[BlogModel]:
    try:
        user_id = jwt_payload.get("user_id", None)
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Unauthorized: User ID not found in access token")
        return blog_service.get_blogs_by_user(user_id=user_id, limit=limit, offset=offset)
    except BlogOperationException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error {str(e)}")
