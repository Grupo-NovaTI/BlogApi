from typing import Optional
from starlette import status
from fastapi import APIRouter, Path
from app.comments.schemas.comment_request import InsertCommentRequest, UpdateCommentRequest
from app.comments.schemas.comment_response import CommentResponse
from app.core.dependencies import CommentServiceDependency, AccessTokenDependency, UserIDFromTokenDependency

comment_router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)

@comment_router.post(
    path="",
    response_model=CommentResponse,
    summary="Insert a new comment",
    tags=["comments"],
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    comment_request: InsertCommentRequest,
    comment_service: CommentServiceDependency,
    user_id: UserIDFromTokenDependency,
) -> CommentResponse:
    """
    Create a new comment for a blog post.

    Args:
        comment_request (InsertCommentRequest): The request body containing the comment details.
        comment_service (CommentServiceDependency): The service dependency for managing comments.
        user_id (int): The ID of the user making the comment.

    Returns:
        CommentResponse: The created comment.
    """
    return comment_service.create_comment(comment=comment_request.model_dump(exclude_unset=True), user_id=user_id)

@comment_router.get(
    path="/blogs/{blog_id}",
    response_model=list[CommentResponse],
    summary="Get all comments for a blog",
    tags=["comments"],
)
async def get_comments_by_blog_id(
    jwt_payload: AccessTokenDependency,
    comment_service: CommentServiceDependency,
    blog_id: int = Path(..., description="The ID of the blog to retrieve comments for", ge=1, le=1000000)
):
    """
    Retrieve all comments for a specific blog by its ID.

    Args:
        blog_id (int): The ID of the blog to retrieve comments for.
        jwt_payload (dict): The JWT payload containing user information.
        comment_service (CommentServiceDependency): The service dependency for managing comments.

    Returns:
        list[CommentResponse]: A list of comments for the specified blog.
    """
    return comment_service.get_comments_by_blog_id(blog_id=blog_id)

@comment_router.get(
    path="/user/me",
    response_model=list[CommentResponse],
    summary="Get all comments by the current user",
    tags=["comments"],
)
async def get_comments_by_user(
    user_id: UserIDFromTokenDependency,
    comment_service: CommentServiceDependency,
):
    """
    Retrieve all comments made by the current user.

    Args:
        jwt_payload (dict): The JWT payload containing user information.
        comment_service (CommentServiceDependency): The service dependency for managing comments.

    Returns:
        list[CommentResponse]: A list of comments made by the current author.
    """
    return comment_service.get_comments_by_user(user_id=user_id)

@comment_router.get(
    path="/{comment_id}",
    response_model=Optional[CommentResponse],
    summary="Get a comment by ID",
    tags=["comments"],
)
async def get_comment_by_id(
    jwt_payload: AccessTokenDependency,
    comment_service: CommentServiceDependency,
    comment_id: int = Path(..., description="The ID of the comment to retrieve", ge=1, le=1000000)
):
    """
    Retrieve a comment by its ID.

    Args:
        comment_id (int): The ID of the comment to retrieve.
        jwt_payload (dict): The JWT payload containing user information.
        comment_service (CommentServiceDependency): The service dependency for managing comments.

    Returns:
        CommentResponse: The requested comment.
    """
    return comment_service.get_comment_by_id(comment_id=comment_id)
  

@comment_router.patch(
    path="/{comment_id}",
    response_model=CommentResponse,
    summary="Update a comment",
    tags=["comments"],
)
async def update_comment(
    comment_request: UpdateCommentRequest,
    user_id: UserIDFromTokenDependency,
    comment_service: CommentServiceDependency,
    comment_id: int = Path(..., description="The ID of the comment to update", ge=1, le=1000000)
):
    """
    Update an existing comment.

    Args:
        comment_id (int): The ID of the comment to update.
        comment_request (UpdateCommentRequest): The request body containing the updated comment details.
        user_id (int): The ID of the user making the request.
        comment_service (CommentServiceDependency): The service dependency for managing comments.

    Returns:
        CommentResponse: The updated comment.
    """

    return comment_service.update_comment(
        comment_id=comment_id,
        content=comment_request.content,
        user_id=user_id
    )
    
    
@comment_router.delete(
    path="/{comment_id}",
    summary="Delete a comment",
    tags=["comments"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    user_id: UserIDFromTokenDependency,
    comment_service: CommentServiceDependency,
    comment_id: int = Path(..., description="The ID of the comment to delete", ge=1, le=1000000)
):
    """
    Delete a comment by its ID.

    Args:
        comment_id (int): The ID of the comment to delete.
        jwt_payload (dict): The JWT payload containing user information.
        comment_service (CommentServiceDependency): The service dependency for managing comments.

    Returns:
        None: If the deletion is successful.
    """
    comment_service.delete_comment_for_user(comment_id=comment_id, user_id=user_id)
