"""
User routes for the FastAPI application.

This module defines the API endpoints for user-related operations, including retrieving the current user,
fetching users by ID, listing all users, deleting the current user, and activating or deactivating user accounts.
It uses dependency injection for service and authentication logic.
"""

from typing import List, Optional
from starlette import status

from fastapi import APIRouter, Path, Query

from app.utils.enums.user_roles import UserRole
from app.users.schemas.user_response import UserResponse
from app.core.dependencies import UserServiceDependency, UserIDFromTokenDependency, AccessTokenDependency
from app.core.security.authentication_decorators import role_required
from app.utils.constants.constants import DEFAULT_OFFSET, DEFAULT_PAGE_SIZE

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@user_router.get(path="/me", response_model=UserResponse, summary="Get current user", tags=["users"])
async def get_current_user(user_service: UserServiceDependency, current_user_id : UserIDFromTokenDependency):
    """
    Retrieve the current authenticated user's information.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        current_user_id (UserIDFromTokenDependency): The ID of the current user from the token.

    Returns:
        UserResponse: The current user's data.
    """
    return user_service.get_user_by_id(user_id=current_user_id )


@user_router.get(path="/{user_id}", response_model=Optional[UserResponse], summary="Get user by ID", tags=["users"])
@role_required(required_role=[UserRole.ADMIN, UserRole.USER])
async def get_user_by_id(user_service: UserServiceDependency, token: AccessTokenDependency, user_id: int = Path(
        ..., description="The unique identifier of the user to retrieve", ge=1, le=1000000)):
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


@user_router.get(path="", response_model=List[UserResponse], summary="Get all users", tags=["users"])
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


@user_router.delete(path="/me", summary="Delete user by ID", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(user_service: UserServiceDependency, current_user_id: UserIDFromTokenDependency):
    """
    Delete the current authenticated user.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        current_user_id (UserIDFromTokenDependency): The ID of the current user from the token.

    Returns:
        None
    """
    user_service.delete_user_by_id(user_id=current_user_id )


@user_router.patch(path="/reactivate", summary="Reactivate user account", tags=["users"], status_code=status.HTTP_200_OK)
async def reactivate_user_account(user_service: UserServiceDependency, current_user_id : UserIDFromTokenDependency):
    """
    Reactivate the current user's account.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        current_user_id (UserIDFromTokenDependency): The ID of the current user from the token.

    Returns:
        UserResponse: The reactivated user.
    """
    return user_service.update_user_active_status(user_id=current_user_id , is_active=True)


@user_router.patch("/deactivate", summary="Deactivate user account", tags=["users"], status_code=status.HTTP_200_OK)
async def set_user_inactive(user_service: UserServiceDependency, current_user_id : UserIDFromTokenDependency):
    """
    Deactivate the current user's account.

    Args:
        user_service (UserServiceDependency): The user service dependency.
        current_user_id (UserIDFromTokenDependency): The ID of the current user from the token.

    Returns:
        UserResponse: The deactivated user.
    """
    return user_service.update_user_active_status(user_id=current_user_id , is_active=False)
