"""
Dependency injection utilities for FastAPI services, repositories, and security.

This module provides reusable dependency definitions for injecting services, repositories,
database sessions, and security utilities into FastAPI route handlers.
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.services.auth_service import AuthService
from app.blog_tags.repositories.blog_tag_repository import BlogTagRepository
from app.blogs.repositories.blog_repository import BlogRepository
from app.blogs.services.blog_service import BlogService
from app.comments.repositories.comment_repository import CommentRepository
from app.comments.services.comment_service import CommentService
from app.core.config.application_config import JWT_OAUTH_SCHEME
from app.core.data.database import get_db
from app.core.security.jwt_handler import JwtHandler
from app.core.security.password_hasher import PasswordHasher
from app.tags.repositories.tag_repository import TagRepository
from app.tags.services.tag_service import TagService
from app.users.repositories.user_repository import UserRepository
from app.users.services.user_service import UserService
from app.utils.errors.exceptions import UnauthorizedException
from app.core.data.file_storage_interface import FileStorageInterface
from app.core.data.azure_file_storage_service import AzureFileStorageService
# Security Dependencies

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=JWT_OAUTH_SCHEME)

_jwt_handler_instance = JwtHandler()

def provides_jwt_handler() -> JwtHandler:
    """
    Provides a singleton JwtHandler instance for dependency injection.

    Returns:
        JwtHandler: The JWT handler instance.
    """
    return _jwt_handler_instance

JWTHandlerDependency = Annotated[JwtHandler, Depends(dependency=provides_jwt_handler)]

def provides_pass_hasher() -> PasswordHasher:
    """
    Provides a PasswordHasher instance for dependency injection.

    Returns:
        PasswordHasher: The password hasher instance.
    """
    return PasswordHasher()

_PasswordHasherDependency = Annotated[PasswordHasher, Depends(dependency=provides_pass_hasher)]

# Reusable dependency for getting the raw token string from the request
TokenDependency = Annotated[str, Depends(oauth2_scheme)]

async def provide_token_payload(
    jwt_handler: JWTHandlerDependency,
    token: TokenDependency,
) -> dict:
    """
    Dependency to decode the JWT and return its payload.

    Args:
        jwt_handler (JwtHandler): The JWT handler dependency.
        token (str): The JWT access token.

    Returns:
        dict: The decoded JWT payload.
    """
    return jwt_handler.decode_access_token(token=token)

async def provide_user_id_from_token(
    payload: Annotated[dict, Depends(provide_token_payload)]
) -> int:
    """
    Dependency to extract the user ID from the token payload.

    Args:
        payload (dict): The decoded JWT payload.

    Returns:
        int: The user ID extracted from the payload.

    Raises:
        UnauthorizedException: If user_id is not found in the payload.
    """
    user_id = payload.get("user_id")
    if user_id is None:
        raise UnauthorizedException(
            details="Invalid token: user_id not found in payload."
        )
    return int(user_id)

AccessTokenPayloadDependency = Annotated[dict, Depends(dependency=provide_token_payload)]
UserIDFromTokenDependency = Annotated[int, Depends(dependency=provide_user_id_from_token)]

# Data Dependencies
_DatabaseSession = Annotated[Session, Depends(dependency=get_db)]

# File Storage Dependency
@lru_cache
def _provide_file_storage_service() -> FileStorageInterface:
    """
    Provides a FileStorageService instance for dependency injection.

    Returns:
        FileStorageInterface: The file storage service instance.
    """
    return AzureFileStorageService()

FileStorageServiceDependency = Annotated[FileStorageInterface, Depends(dependency=_provide_file_storage_service)]

# Repository Dependencies
def _provide_user_repository(db_session: _DatabaseSession) -> UserRepository:
    """
    Provides a UserRepository instance for dependency injection.

    Args:
        db_session (Session): The database session dependency.

    Returns:
        UserRepository: The user repository instance.
    """
    return UserRepository(db_session=db_session)

def _provide_comment_repository(db_session: _DatabaseSession) -> CommentRepository:
    """
    Provides a CommentRepository instance for dependency injection.

    Args:
        db_session (Session): The database session dependency.

    Returns:
        CommentRepository: The comment repository instance.
    """
    return CommentRepository(db_session=db_session)

def _provide_tag_repository(db_session: _DatabaseSession) -> TagRepository:
    """
    Provides a TagRepository instance for dependency injection.

    Args:
        db_session (Session): The database session dependency.

    Returns:
        TagRepository: The tag repository instance.
    """
    return TagRepository(db_session=db_session)

def _provide_blog_repository(db_session: _DatabaseSession) -> BlogRepository:
    """
    Provides a BlogRepository instance for dependency injection.

    Args:
        db_session (Session): The database session dependency.

    Returns:
        BlogRepository: The blog repository instance.
    """
    return BlogRepository(db_session=db_session)

def _provide_blog_tag_repository(db_session: _DatabaseSession) -> BlogTagRepository:
    """
    Provides a BlogTagRepository instance for dependency injection.

    Args:
        db_session (Session): The database session dependency.

    Returns:
        BlogTagRepository: The blog-tag repository instance.
    """
    return BlogTagRepository(db_session=db_session)

_UserRepositoryDependency = Annotated[UserRepository, Depends(dependency=_provide_user_repository)]
_TagRepositoryDependency = Annotated[TagRepository, Depends(dependency=_provide_tag_repository)]
_BlogRepositoryDependency = Annotated[BlogRepository, Depends(dependency=_provide_blog_repository)]
_CommentRepositoryDependency = Annotated[CommentRepository, Depends(dependency=_provide_comment_repository)]
_BlogTagRepositoryDepedency = Annotated[BlogTagRepository, Depends(dependency=_provide_blog_tag_repository)]

# Service Dependencies
def _provide_user_services(user_repository: _UserRepositoryDependency, db_session : _DatabaseSession) -> UserService:
    """
    Provides a UserService instance for dependency injection.

    Args:
        user_repository (UserRepository): The user repository dependency.
        db_session (Session): The database session dependency.

    Returns:
        UserService: The user service instance.
    """
    return UserService(user_repository=user_repository, db_session=db_session)

def _provide_comment_service(comment_repository: _CommentRepositoryDependency, db_session: _DatabaseSession) -> CommentService:
    """
    Provides a CommentService instance for dependency injection.

    Args:
        comment_repository (CommentRepository): The comment repository dependency.
        db_session (Session): The database session dependency.

    Returns:
        CommentService: The comment service instance.
    """
    return CommentService(comment_repository=comment_repository, db_session=db_session)

def _provide_auth_service(
    user_repository: _UserRepositoryDependency, 
    jwt_handler: JWTHandlerDependency, 
    password_service: _PasswordHasherDependency,
    db_session: _DatabaseSession
) -> AuthService:
    """
    Provides an AuthService instance for dependency injection.

    Args:
        user_repository (UserRepository): The user repository dependency.
        jwt_handler (JwtHandler): The JWT handler dependency.
        password_service (PasswordHasher): The password hasher dependency.
        db_session (Session): The database session dependency.

    Returns:
        AuthService: The authentication service instance.
    """
    return AuthService(user_repository=user_repository, jwt_handler=jwt_handler, password_service=password_service, db_session=db_session)

def _provide_tag_service(tag_repository: _TagRepositoryDependency, db_session: _DatabaseSession) -> TagService:
    """
    Provides a TagService instance for dependency injection.

    Args:
        tag_repository (TagRepository): The tag repository dependency.
        db_session (Session): The database session dependency.

    Returns:
        TagService: The tag service instance.
    """
    return TagService(tag_repository=tag_repository, db_session=db_session)

def _provide_blog_service(blog_repository: _BlogRepositoryDependency, blog_tag_repository : _BlogTagRepositoryDepedency, db_session : _DatabaseSession) -> BlogService:
    """
    Provides a BlogService instance for dependency injection.

    Args:
        blog_repository (BlogRepository): The blog repository dependency.
        blog_tag_repository (BlogTagRepository): The blog-tag repository dependency.
        db_session (Session): The database session dependency.

    Returns:
        BlogService: The blog service instance.
    """
    return BlogService(blog_repository=blog_repository, blog_tag_repository=blog_tag_repository, db_session=db_session)

# Final annotated dependencies for easy use in route handlers
CommentServiceDependency = Annotated[CommentService, Depends(dependency=_provide_comment_service)]
UserServiceDependency = Annotated[UserService, Depends(dependency=_provide_user_services)]
AuthServiceDependency = Annotated[AuthService, Depends(dependency=_provide_auth_service)]
TagServiceDependency = Annotated[TagService, Depends(dependency=_provide_tag_service)]
BlogServiceDependency = Annotated[BlogService, Depends(dependency=_provide_blog_service)]