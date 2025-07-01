from typing import List, Optional
from starlette import status

from fastapi import APIRouter, HTTPException, Path

from app.utils.enumns.user_roles import UserRole
from app.users.schemas.user_response import UserResponse
from app.core.dependencies import UserServiceDependency, UserIDFromTokenDependency, AccessTokenDependency
from app.core.security.authentication_decorators import authentication_required, role_required, current_user_only
from app.users.excepctions.user_exceptions import UserNotFoundException, UserOperationException
from app.auth.exceptions.auth_exceptions import OperationNotAllowedException

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@user_router.get(path="/me", response_model=UserResponse, summary="Get current user", tags=["users"])
async def get_current_user(service: UserServiceDependency, user_id_payload: UserIDFromTokenDependency):
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
    try:
        if not user_id_payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found in JWT payload")
        return service.get_user_by_id(user_id=user_id_payload)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_router.get(path="/{user_id}", response_model=Optional[UserResponse], summary="Get user by ID", tags=["users"])
@role_required(required_role=[UserRole.ADMIN, UserRole.USER])
async def get_user_by_id(user_id: int, service: UserServiceDependency, jwt_payload: AccessTokenDependency):
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
    try:
        return service.get_user_by_id(user_id=user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_router.get(path="", response_model=List[UserResponse], summary="Get all users", tags=["users"])
async def get_users(service: UserServiceDependency):
    """
    Endpoint to retrieve a list of users.

    Returns:
        List of users.
    """
    return service.get_all_users()


@user_router.delete(path="/me", summary="Delete user by ID", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(service: UserServiceDependency, user_id_payload: UserIDFromTokenDependency):
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
    try: 
         service.delete_user(user_id=user_id_payload)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user_router.patch(path="/reactivate", summary="Reactivate user account", tags=["users"], status_code=status.HTTP_200_OK)
async def reactivate_user_account(service: UserServiceDependency, user_id_payload: UserIDFromTokenDependency):
    """
    Endpoint to activate a user account.

    Args:
        user_id (int): The unique identifier of the user to activate.
        service (UserServicesDependency): The user services dependency.

    Returns:
        UserResponse: The activated user.
    """
    try:

        return service.reactivate_user_account(user_id=user_id_payload)
    except OperationNotAllowedException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user_router.patch("/deactivate", summary="Deactivate user account", tags=["users"], status_code=status.HTTP_200_OK)
async def set_user_inactive(service: UserServiceDependency, user_id_payload: UserIDFromTokenDependency):
    """
    Endpoint to deactivate a user account.

    Args:
        user_id (int): The unique identifier of the user to deactivate.
        service (UserServicesDependency): The user services dependency.

    Returns:
        UserResponse: The deactivated user.
    """
    try:
        return service.set_user_inactive(user_id=user_id_payload)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
