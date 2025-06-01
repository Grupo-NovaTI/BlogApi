from typing import Annotated, Type
from sqlalchemy.orm import Session
from fastapi import Depends

from auth.repositories.auth_repository import AuthRepository
from core.db.database import get_db
from users.repositories.user_repository import UserRepository
from utils.repositories.base_repository import BaseRepository
from core.security.jwt_handler import JwtHandler, oauth_scheme

# Database session type definition
_DatabaseSession = Annotated[Session, Depends(get_db)]

# Dependency to get an instance of JWTHandler (could be singleton)
_jwt_handler_instance = JwtHandler()


def _get_jwt_handler() -> JwtHandler:
    return _jwt_handler_instance  # Or new JWTHandler() if preferred


JWTHandlerDependency = Annotated[JwtHandler, Depends(_get_jwt_handler)]


class DependencyProvider:
    """
    Dependency provider class that centralizes dependency management.
    Facilitates dependency injection and testing.
    """
    @staticmethod
    def get_repository(repository_class: Type[BaseRepository], db: _DatabaseSession, **kwargs) -> BaseRepository:
        """
        Generic method to obtain any repository.

        Args:
            repository_class: Repository class to be instantiated
            db (Session): Database session

        Returns:
            BaseRepository: Instance of the requested repository
        """
        return repository_class(db_session=db, **kwargs)


def get_user_repository(db: _DatabaseSession) -> BaseRepository:
    """
    Dependency that provides a UserRepository instance.

    Args:
        db (Session): The database session dependency.

    Returns:
        UserRepository: Instance of the user repository

    Example:
        ```python
        @router.get("/users")
        async def get_users(repo: Annotated[UserRepository, Depends(get_user_repository)]):
            return await repo.get_all()
        ```
    """
    return DependencyProvider.get_repository(repository_class=UserRepository, db=db)


def get_auth_repository(db: _DatabaseSession, jwt_handler: JWTHandlerDependency) -> BaseRepository:
    """
    Dependency that provides an AuthRepository instance.

    Args:
        db (Session): The database session dependency.

    Returns:
        AuthRepository: Instance of the auth repository
    """
    return DependencyProvider.get_repository(repository_class=AuthRepository, db=db, jwt_handler=jwt_handler)


async def get_token_payload(
    token: Annotated[str, Depends(_jwt_handler_instance.oauth_scheme)],
    jwt_handler: JWTHandlerDependency
) -> dict:
    return jwt_handler.decode_access_token(token)


# Typed dependencies for use in endpoints
UserRepositoryDependency = Annotated[UserRepository, Depends(
    get_user_repository)]
AuthRepositoryDependency = Annotated[AuthRepository, Depends(
    get_auth_repository)]
JwtAccessTokenDependency = Annotated[dict, Depends(get_token_payload)]
