from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.dependencies.services_depends import AuthServiceDependency as AuthService
from auth.schemas.token_response import TokenResponse
from users.schemas.user_request import UserRequest
from users.excepctions.user_exceptions import UserAlreadyExistsException, UserOperationException
from auth.exceptions.auth_exceptions import InvalidUserCredentialsException, OperationFailedException
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
    try:
        token: str = auth_service.login(
            username=form_data.username, password=form_data.password)
        return TokenResponse(access_token=token, token_type="bearer")
    except InvalidUserCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except UserOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except OperationFailedException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@auth_router.post(path="/register", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def register(auth_service: AuthService, user: UserRequest) -> TokenResponse:
    """
    Register a new user and return a JWT token.
    """
    try:
        token: str = auth_service.register(user=user.to_orm())
        return TokenResponse(access_token=token, token_type="bearer")
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InvalidUserCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except OperationFailedException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))