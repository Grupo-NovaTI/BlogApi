"""
User routes for the FastAPI application.

This module defines the API endpoints for user-related operations, including retrieving the current user,
fetching users by ID, listing all users, deleting the current user, and activating or deactivating user accounts.
It uses dependency injection for service and authentication logic.
"""

from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, Path, Query, UploadFile
from starlette import status

from app.core.dependencies import (AccessTokenDependency,
                                   FileStorageServiceDependency,
                                   UserIDFromTokenDependency,
                                   UserServiceDependency)
from app.core.security.authentication_decorators import role_required
from app.users.schemas.user_request import UserUpdateRequest
from app.users.schemas.user_response import UserResponse
from app.utils.constants.constants import DEFAULT_OFFSET, DEFAULT_PAGE_SIZE
from app.utils.enums.user_roles import UserRole

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@user_router.get(path="/me", response_model=UserResponse, summary="Get current user")
async def get_current_user(user_service: UserServiceDependency, current_user_id: UserIDFromTokenDependency):
    """
    Retrieve the current authenticated user's information.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        current_user_id (UserIDFromTokenDependency): The ID of the current user from the token.

    Returns:
        UserResponse: The current user's data.
    """
    return user_service.get_user_by_id(user_id=current_user_id)


@user_router.get(path="/{user_id}", response_model=Optional[UserResponse], summary="Get user by ID")
@role_required(required_role=[UserRole.ADMIN, UserRole.USER])
async def get_user_by_id(user_service: UserServiceDependency, token: AccessTokenDependency, user_id: int = Path(
        default=..., description="The unique identifier of the user to retrieve", ge=1, le=1000000)):
    """
    Retrieve a user by their unique ID.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        token (AccessTokenDependency): The JWT payload dependency.
        user_id (int): The unique identifier of the user to retrieve.

    Returns:
        UserResponse: The user data if found, otherwise None.
    """
    return user_service.get_user_by_id(user_id=user_id)


@user_router.get(path="", response_model=List[UserResponse], summary="Get all users")
async def get_users(user_service: UserServiceDependency, limit: int = Query(DEFAULT_PAGE_SIZE, ge=1), offset: int = Query(DEFAULT_OFFSET, ge=0)):
    """
    Retrieve a list of users with pagination.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        limit (int): The maximum number of users to return.
        offset (int): The number of users to skip before starting to return results.

    Returns:
        List[UserResponse]: A list of user data.
    """
    return user_service.get_all_users()


@user_router.delete(path="/me", summary="Delete user by ID", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(user_service: UserServiceDependency, current_user_id: UserIDFromTokenDependency):
    """
    Delete the current authenticated user.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        current_user_id (UserIDFromTokenDependency): The ID of the current user from the token.

    Returns:
        None
    """
    user_service.delete_user_by_id(user_id=current_user_id)


@user_router.patch(path="/status", summary="Reactivate user account", status_code=status.HTTP_200_OK)
async def reactivate_user_account(user_service: UserServiceDependency, current_user_id: UserIDFromTokenDependency, is_active: bool = Path(default=..., description="Set to True to reactivate the account or False to deactivate it", example=True)):
    """
    Reactivate the current user's account.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        current_user_id (UserIDFromTokenDependency): The ID of the current user from the token.
        is_active (bool): Whether to reactivate the account (True) or deactivate it (False).
    Returns:
        UserResponse: The updated user.
    """
    return user_service.update_user_active_status(user_id=current_user_id, is_active=is_active)


@user_router.patch(path="/me", summary="Update user profile", status_code=status.HTTP_200_OK)
async def update_user_profile(user_service: UserServiceDependency, current_user_id: UserIDFromTokenDependency, user_data: UserUpdateRequest):
    """
    Update the current user's profile.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        current_user_id (UserIDFromTokenDependency): The ID of the current user from the token.
        user_data (UserProfileUpdate): The new user profile data.

    Returns:
        UserResponse: The updated user profile.
    """
    return user_service.update_user(user_id=current_user_id, user_data=user_data.model_dump(exclude_unset=True))


@user_router.post(path="/profile-picture", summary="Upload user profile picture", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def upload_user_profile_picture(user_service: UserServiceDependency, current_user_id: UserIDFromTokenDependency, file_service: FileStorageServiceDependency, file: UploadFile = File(default=..., description="The profile picture file to upload")):
    """
    Upload a profile picture for the current user.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        current_user_id (UserIDFromTokenDependency): The ID of the current user from the token.
        file (bytes): The profile picture file to upload.

    Returns:
        UserResponse: The updated user profile with the new profile picture.

    Raises:
        HTTPException: If the file type is invalid or exceeds the size limit.
    """
    file_content: bytes = await _validate_profile_picture(file=file)

    if file.content_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content type is required."
        )

    if file.content_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content type is required."
        )

    file_url: str = await file_service.upload_file(
        file_content=file_content,
        content_type=file.content_type,
        user_id=current_user_id,
        prefix="profile-pictures"
    )

    return user_service.update_profile_picture(user_id=current_user_id, picture_url=file_url)


async def _validate_profile_picture(file: UploadFile) -> bytes:
    """
    Validates an uploaded profile picture for type and size.

    Args:
        file: The uploaded file from FastAPI.

    Returns:
        The file content as bytes if validation is successful.

    Raises:
        HTTPException: If the file type or size is invalid.
    """

    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
    ALLOWED_MIME_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types are: {', '.join(ALLOWED_MIME_TYPES)}"
        )

    file_content: bytes = await file.read()

    if len(file_content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the limit of {MAX_FILE_SIZE_BYTES / (1024*1024):.0f}MB."
        )

    return file_content
