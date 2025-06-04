from typing import Annotated

from fastapi import Depends

from users.services.user_services import UserService
from auth.services.auth_service import AuthService
from core.dependencies.repo_depends import UserRepositoryDependency
from core.dependencies.security_depends import JWTHandlerDependency, PasswordHasherDependency

def get_user_services(user_repository: UserRepositoryDependency) -> UserService:
    """
    Dependency that provides a UserService instance.

    Args:
        user_repository (UserRepositoryDependency): The user repository dependency.

    Returns:
        UserService: Instance of the user services
    """
    return UserService(user_repository=user_repository)

def get_auth_services(user_repository: UserRepositoryDependency, jwt_handler: JWTHandlerDependency, password_service : PasswordHasherDependency) -> AuthService:
    """
    Dependency that provides an AuthService instance for authentication.

    Args:
        user_repository (UserRepositoryDependency): The user repository dependency.

    Returns:
        AuthService: Instance of the auth service for authentication
    """
    return AuthService(user_repository=user_repository, jwt_handler=jwt_handler, password_service= password_service)



UserServiceDependency = Annotated[UserService, Depends(dependency=get_user_services)]
AuthServiceDependency = Annotated[AuthService, Depends(dependency=get_auth_services)]