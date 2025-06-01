from fastapi import APIRouter, HTTPException
from utils.enumns.user_roles import UserRole
from users.schemas.user_response import UserResponse
from users.schemas.user_request import UserRequest
from core.dependencies.depends import UserRepositoryDependency, JwtAccessTokenDependency
from core.security.authentication_decorators import role_required, admin_only
from starlette import status
user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@user_router.get("", response_model=list[UserResponse], summary="Get all users", tags=["users"])
@admin_only()
async def get_users(repo: UserRepositoryDependency, jwt_payload: JwtAccessTokenDependency):
    """
    Endpoint to retrieve a list of users.
    
    Returns:
        List of users.
    """
    return repo.get_all_users()

@user_router.post("", response_model=UserResponse, summary="Insert a new user", tags=["users"])
async def insert_user( repo: UserRepositoryDependency, user: UserRequest):
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
       return repo.create_user(user=user_orm)
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))