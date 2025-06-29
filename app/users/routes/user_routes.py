from typing import List
from fastapi import APIRouter, HTTPException
from starlette import status

from app.utils.enumns.user_roles import UserRole
from app.users.schemas.user_response import UserResponse
from app.users.schemas.user_request import UserRequest
from app.core.dependencies import UserServiceDependency, AccessTokenDependency
from app.core.security.authentication_decorators import authentication_required, role_required
from app.users.excepctions.user_exceptions import UserNotFoundException, UserAlreadyExistsException, UserOperationException

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@user_router.get(path="/me", response_model=UserResponse, summary="Get current user", tags=["users"])
@authentication_required()
async def get_current_user(service: UserServiceDependency, jwt_payload: AccessTokenDependency):
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
        user_id: int | None = jwt_payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found in JWT payload")
        return service.get_user_by_id(user_id=user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_router.get(path="/{user_id}", response_model=UserResponse, summary="Get user by ID", tags=["users"])
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
@authentication_required()
async def get_users(service: UserServiceDependency, jwt_payload: AccessTokenDependency):
    """
    Endpoint to retrieve a list of users.

    Returns:
        List of users.
    """
    return service.get_all_users()


@user_router.post(path="", response_model=UserResponse, summary="Insert a new user", tags=["users"])
async def insert_user(service: UserServiceDependency, user: UserRequest):
    """
    Endpoint to insert a new user.

    Args:
        repo (UserRepositoryDependency): The user repository dependency.
        user (UserRequest): The user data to insert.

    Returns:
        The inserted user.
    """
    try:
        user_orm = user.to_orm()
        return service.create_user(user_data=user_orm)
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except UserOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
