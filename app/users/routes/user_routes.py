from fastapi import APIRouter
from users.models.user_model import UserModel
from users.schemas.user_response import UserResponse
from users.schemas.user_request import UserRequest
from core.dependencies.depends import UserRepositoryDependency
user_router = APIRouter()


@user_router.get("/users", response_model=list[UserResponse], summary="Get all users", tags=["users"])
async def get_users(repo: UserRepositoryDependency):
    """
    Endpoint to retrieve a list of users.
    
    Returns:
        List of users.
    """
    return repo.get_all_users()

@user_router.post("/users", response_model=UserResponse, summary="Insert a new user", tags=["users"])
async def insert_user(repo: UserRepositoryDependency, user: UserRequest):
    """
    Endpoint to insert a new user.
    
    Args:
        repo (UserRepositoryDependency): The user repository dependency.
        user (UserRequest): The user data to insert.

    Returns:
        The inserted user.
    """
    new_user = UserModel(**user.model_dump())
    return repo.create_user(user=new_user)