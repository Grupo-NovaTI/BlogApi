from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.dependencies.depends import AuthRepositoryDependency
from auth.schemas.token_response import TokenResponse
auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(auth_repo: AuthRepositoryDependency, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user with username and password.
    Returns a JWT token if authentication is successful.
    """
    try:
        token = auth_repo.login(
            username=form_data.username, password=form_data.password)
        return TokenResponse(access_token=token, token_type="bearer")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
