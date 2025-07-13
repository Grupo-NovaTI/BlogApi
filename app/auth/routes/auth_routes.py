"""
Authentication API routes for user login and registration.

This module defines FastAPI routes for user authentication, including login and registration endpoints.
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.auth.schemas.update_password_request import UpdatePasswordRequest
from app.auth.schemas.token_response import TokenResponse
from app.core.dependencies import AuthServiceDependency as AuthService, UserIDFromTokenDependency
from app.users.schemas.user_request import UserRequest

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post(path="/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(auth_service: AuthService, form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    """
    Authenticate user with username and password.

    Args:
        auth_service (AuthService): The authentication service dependency.
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.

    Returns:
        TokenResponse: JWT token if authentication is successful.
    """
    token: str = auth_service.login(
        username=form_data.username, password=form_data.password)
    return TokenResponse(access_token=token, token_type="bearer")

@auth_router.post(path="/register", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def register(auth_service: AuthService, user: UserRequest) -> TokenResponse:
    """
    Register a new user and return a JWT token.

    Args:
        auth_service (AuthService): The authentication service dependency.
        user (UserRequest): The user registration data.

    Returns:
        TokenResponse: JWT token for the newly registered user.
    """
    token: str = auth_service.register(user_data=user.model_dump(exclude_unset=True))
    return TokenResponse(access_token=token, token_type="bearer")

@auth_router.patch(path="/update-password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(auth_service: AuthService, user_id : UserIDFromTokenDependency, password_request: UpdatePasswordRequest) -> None:
    """
    Update the user's password.

    Args:
        auth_service (AuthService): The authentication service dependency.
        user_id (int): The ID of the user whose password is being updated.
        current_password (str): The user's current password.
        new_password (str): The new password to set for the user.

    Returns:
        None
    """
    auth_service.update_password(user_id=user_id, current_password=password_request.current_password, new_password=password_request.new_password)