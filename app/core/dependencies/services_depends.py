from typing import Annotated

from fastapi import Depends

from users.services.user_services import UserServices
from auth.services.auth_service import AuthService
from core.dependencies.repo_depends import UserRepositoryDependency
from core.dependencies.depends import JWTHandlerDependency

def get_user_services(user_repository: UserRepositoryDependency) -> UserServices:
    """
    Dependency that provides a UserServices instance.

    Args:
        user_repository (UserRepositoryDependency): The user repository dependency.

    Returns:
        UserServices: Instance of the user services
    """
    return UserServices(user_repository=user_repository)

def get_auth_services(user_repository: UserRepositoryDependency, jwt_handler: JWTHandlerDependency) -> AuthService:
    """
    Dependency that provides an AuthService instance for authentication.

    Args:
        user_repository (UserRepositoryDependency): The user repository dependency.

    Returns:
        AuthService: Instance of the auth service for authentication
    """
    return AuthService(user_repository=user_repository, jwt_handler=jwt_handler)



UserServicesDependency = Annotated[UserServices, Depends(dependency=get_user_services)]
AuthServiceDependency = Annotated[AuthService, Depends(dependency=get_auth_services)]