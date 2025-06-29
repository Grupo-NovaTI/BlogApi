from typing import Annotated

from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config.application_config import ApplicationConfig
from app.users.services.user_service import UserService
from app.tags.services.tag_service import TagService
from app.auth.services.auth_service import AuthService
from app.blogs.services.blog_service import BlogService
from app.core.security.jwt_handler import JwtHandler
from app.core.security.password_hasher import PasswordHasher
from app.core.db.database import get_db
from app.users.repositories.user_repository import UserRepository
from app.tags.repositories.tag_repository import TagRepository
from app.blogs.repositories.blog_repository import BlogRepository


# Global Dependencies
# This section provides global dependencies that can be used across the application.



@lru_cache
def provide_application_config() -> ApplicationConfig:
    return ApplicationConfig()


# Security Dependencies
# This section provides dependencies for security-related services such as JWT handling and password hashing.
_jwt_handler_instance = JwtHandler(config=provide_application_config())

def provides_jwt_handler() -> JwtHandler:
    return _jwt_handler_instance


JWTHandlerDependency = Annotated[JwtHandler, Depends(dependency=provides_jwt_handler)]


def provides_pass_hasher() -> PasswordHasher:
    return PasswordHasher()

_PasswordHasherDependency = Annotated[PasswordHasher, Depends(dependency=provides_pass_hasher)]

async def provide_token_payload(
    jwt_handler: JWTHandlerDependency,
    token: Annotated[str, Depends(dependency=_jwt_handler_instance.oauth_scheme)],
) -> dict:
    return jwt_handler.decode_access_token(token=token)

AccessTokenDependency = Annotated[dict, Depends(dependency=provide_token_payload)]


# Database Dependencies
# This section provides dependencies for various repositories used in the application.
_DatabaseSession = Annotated[Session, Depends(dependency=get_db)]

# Repository Dependencies
# This section provides dependencies for repositories used in the application.


def _provide_user_repository(db: _DatabaseSession) -> UserRepository:
    """
    Dependency that provides a UserRepository instance.

    Args:
        db (Session): The database session dependency.

    Returns:
        UserRepository: Instance of the user repository
    """
    return UserRepository(db_session=db)


def _provide_tag_repository(db: _DatabaseSession) -> TagRepository:
    """
    Dependency that provides a TagRepository instance.

    Args:
        db (Session): The database session dependency.

    Returns:
        TagRepository: Instance of the tag repository
    """
    return TagRepository(db=db)


def _provide_blog_repository(db: _DatabaseSession) -> BlogRepository:
    """
    Dependency that provides a BlogRepository instance.

    Args:
        db (Session): The database session dependency.

    Returns:
        BlogRepository: Instance of the blog repository
    """
    return BlogRepository(db=db)


_UserRepositoryDependency = Annotated[UserRepository, Depends(
    dependency=_provide_user_repository)]
_TagRepositoryDependency = Annotated[TagRepository, Depends(
    dependency=_provide_tag_repository)]
_BlogRepositoryDependency = Annotated[BlogRepository, Depends(
    dependency=_provide_blog_repository)]

# Service Dependencies
# This section provides dependencies for various services such as user, tag, blog, and authentication services.


def _provide_user_services(user_repository: _UserRepositoryDependency) -> UserService:
    """
    Dependency that provides a UserService instance.

    Args:
        user_repository (UserRepositoryDependency): The user repository dependency.

    Returns:
        UserService: Instance of the user services
    """
    return UserService(user_repository=user_repository)


def __provide_auth_service(user_repository: _UserRepositoryDependency, jwt_handler: JWTHandlerDependency, password_service: _PasswordHasherDependency) -> AuthService:
    """
    Dependency that provides an AuthService instance for authentication.

    Args:
        user_repository (UserRepositoryDependency): The user repository dependency.

    Returns:
        AuthService: Instance of the auth service for authentication
    """
    return AuthService(user_repository=user_repository, jwt_handler=jwt_handler, password_service=password_service)


def __provide_tag_service(tag_repository: _TagRepositoryDependency) -> TagService:
    """
    Dependency that provides a TagService instance.

    Args:
        tag_repository (TagRepositoryDependency): The tag repository dependency.

    Returns:
        TagService: Instance of the tag services
    """
    return TagService(tag_repository=tag_repository)


def __provide_blog_service(blog_repository: _BlogRepositoryDependency) -> BlogService:
    """
    Dependency that provides a BlogService instance.

    Args:
        blog_repository (BlogRepositoryDependency): The blog repository dependency.

    Returns:
        BlogService: Instance of the blog services
    """
    return BlogService(blog_repository=blog_repository)


UserServiceDependency = Annotated[UserService,
                                  Depends(dependency=_provide_user_services)]
AuthServiceDependency = Annotated[AuthService,
                                  Depends(dependency=__provide_auth_service)]
TagServiceDependency = Annotated[TagService,
                                 Depends(dependency=__provide_tag_service)]
BlogServiceDependency = Annotated[BlogService,
                                  Depends(dependency=__provide_blog_service)]

