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
    Endpoint to retrieve the current authenticated user.

    Args:
        service (UserServicesDependency): The user services dependency.
        jwt_payload (JwtAccessTokenDependency): The JWT payload dependency.

    Returns:
        UserResponse: The current user's data.

    Raises:
        HTTPException: If the user is not found or if there is an error during retrieval.
    """
    return user_service.get_user_by_id(user_id=current_user_id )


@user_router.get(path="/{user_id}", response_model=Optional[UserResponse], summary="Get user by ID", tags=["users"])
@role_required(required_role=[UserRole.ADMIN, UserRole.USER])
async def get_user_by_id(user_service: UserServiceDependency, jwt_payload: AccessTokenDependency, user_id: int = Path(
        ..., description="The unique identifier of the user to retrieve", ge=1, le=1000000)):
    """
    Endpoint to retrieve a user by their ID.

    Args:
        user_id (int): The unique identifier of the user to retrieve.
        service (UserServicesDependency): The user services dependency.
        jwt_payload (JwtAccessTokenDependency): The JWT payload dependency.

    Returns:
        UserResponse: The user data if found.

    Raises:
        HTTPException: If the user is not found or if there is an error during retrieval.
    """
    return user_service.get_user_by_id(user_id=user_id)


@user_router.get(path="", response_model=List[UserResponse], summary="Get all users", tags=["users"])
async def get_users(user_service: UserServiceDependency, limit: int = Query(DEFAULT_PAGE_SIZE, ge=1), offset: int = Query(DEFAULT_OFFSET, ge=0)):
    """
    Endpoint to retrieve a list of users.

    Returns:
        List of users.
    """
    return user_service.get_all_users()


@user_router.delete(path="/me", summary="Delete user by ID", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(user_service: UserServiceDependency, current_user_id: UserIDFromTokenDependency):
    """
    Endpoint to delete a user by their ID.

    Args:
        user_id (int): The unique identifier of the user to delete.
        service (UserServicesDependency): The user services dependency.

    Returns:
        None

    Raises:
        HTTPException: If the user is not found or if there is an error during deletion.
    """
    user_service.delete_user_by_id(user_id=current_user_id )


@user_router.patch(path="/reactivate", summary="Reactivate user account", tags=["users"], status_code=status.HTTP_200_OK)
async def reactivate_user_account(service: UserServiceDependency, current_user_id : UserIDFromTokenDependency):
    """
    Endpoint to activate a user account.

    Args:
        user_id (int): The unique identifier of the user to activate.
        service (UserServicesDependency): The user services dependency.

    Returns:
        UserResponse: The activated user.
    """

    return service.update_user_active_status(user_id=current_user_id , is_active=True)


@user_router.patch("/deactivate", summary="Deactivate user account", tags=["users"], status_code=status.HTTP_200_OK)
async def set_user_inactive(user_service: UserServiceDependency, current_user_id : UserIDFromTokenDependency):
    """
    Endpoint to deactivate a user account.

    Args:
        user_id (int): The unique identifier of the user to deactivate.
        service (UserServicesDependency): The user services dependency.

    Returns:
        UserResponse: The deactivated user.
    """
    return user_service.update_user_active_status(user_id=current_user_id , is_active=False)
