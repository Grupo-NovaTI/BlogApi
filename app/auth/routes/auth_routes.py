from starlette import status
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import AuthServiceDependency as AuthService
from app.auth.schemas.token_response import TokenResponse
from app.users.schemas.user_request import UserRequest
auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post(path="/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(auth_service: AuthService, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user with username and password.
    Returns a JWT token if authentication is successful.
    """
    token: str = auth_service.login(
        username=form_data.username, password=form_data.password)
    return TokenResponse(access_token=token, token_type="bearer")


@auth_router.post(path="/register", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def register(auth_service: AuthService, user: UserRequest) -> TokenResponse:
    """
    Register a new user and return a JWT token.
    """
    token: str = auth_service.register(user=user.to_orm())
    return TokenResponse(access_token=token, token_type="bearer")
