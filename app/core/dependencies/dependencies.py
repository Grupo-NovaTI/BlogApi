from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config.application_config import JWT_OAUTH_SCHEME
from app.users.services.user_service import UserService
from app.tags.services.tag_service import TagService
from app.auth.services.auth_service import AuthService
from app.blogs.services.blog_service import BlogService
from app.comments.services.comment_service import CommentService
from app.core.security.jwt_handler import JwtHandler
from app.core.security.password_hasher import PasswordHasher
from app.core.db.database import get_db
from app.users.repositories.user_repository import UserRepository
from app.tags.repositories.tag_repository import TagRepository
from app.blogs.repositories.blog_repository import BlogRepository
from app.comments.repositories.comment_repository import CommentRepository
from app.utils.errors.error_messages import validation_error_message
from app.utils.errors.exceptions import InvalidUserCredentialsException
from app.blog_tags.repositories.blog_tag_repository import BlogTagRepository

# Security Dependencies

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=JWT_OAUTH_SCHEME)

_jwt_handler_instance = JwtHandler()

def provides_jwt_handler() -> JwtHandler:
    return _jwt_handler_instance

JWTHandlerDependency = Annotated[JwtHandler, Depends(dependency=provides_jwt_handler)]

def provides_pass_hasher() -> PasswordHasher:
    return PasswordHasher()

_PasswordHasherDependency = Annotated[PasswordHasher, Depends(dependency=provides_pass_hasher)]

# Reusable dependency for getting the raw token string from the request
TokenDependency = Annotated[str, Depends(oauth2_scheme)]

async def provide_token_payload(
    jwt_handler: JWTHandlerDependency,
    token: TokenDependency,
) -> dict:
    """Dependency to decode the JWT and return its payload."""
    return jwt_handler.decode_access_token(token=token)

async def provide_user_id_from_token(
    payload: Annotated[dict, Depends(provide_token_payload)]
) -> int:
    """Dependency to extract the user ID from the token payload."""
    user_id = payload.get("user_id")
    if user_id is None:
        raise InvalidUserCredentialsException(
            validation_error_message(field="user_id", message="User ID not found in token payload.")
        )
    return int(user_id)

AccessTokenPayloadDependency = Annotated[dict, Depends(dependency=provide_token_payload)]
UserIDFromTokenDependency = Annotated[int, Depends(dependency=provide_user_id_from_token)]

# Database Dependencies
_DatabaseSession = Annotated[Session, Depends(dependency=get_db)]

# Repository Dependencies
def _provide_user_repository(db: _DatabaseSession) -> UserRepository:
    return UserRepository(db_session=db)

def _provide_comment_repository(db: _DatabaseSession) -> CommentRepository:
    return CommentRepository(db_session=db)

def _provide_tag_repository(db: _DatabaseSession) -> TagRepository:
    # Standardized to use 'db_session' for consistency
    return TagRepository(db_session=db)

def _provide_blog_repository(db: _DatabaseSession) -> BlogRepository:
    # Standardized to use 'db_session' for consistency
    return BlogRepository(db_session=db)

def _provide_blog_tag_repository(db: _DatabaseSession) -> BlogTagRepository:
    # Standardized to use 'db_session' for consistency
    return BlogTagRepository(db_session=db)

_UserRepositoryDependency = Annotated[UserRepository, Depends(dependency=_provide_user_repository)]
_TagRepositoryDependency = Annotated[TagRepository, Depends(dependency=_provide_tag_repository)]
_BlogRepositoryDependency = Annotated[BlogRepository, Depends(dependency=_provide_blog_repository)]
_CommentRepositoryDependency = Annotated[CommentRepository, Depends(dependency=_provide_comment_repository)]
_BlogTagRepositoryDepedency = Annotated[BlogTagRepository, Depends(dependency=_provide_blog_tag_repository)]

# Service Dependencies
def _provide_user_services(user_repository: _UserRepositoryDependency) -> UserService:
    return UserService(user_repository=user_repository)

def _provide_comment_service(comment_repository: _CommentRepositoryDependency) -> CommentService:
    return CommentService(comment_repository=comment_repository)

def _provide_auth_service(
    user_repository: _UserRepositoryDependency, 
    jwt_handler: JWTHandlerDependency, 
    password_service: _PasswordHasherDependency
) -> AuthService:
    return AuthService(user_repository=user_repository, jwt_handler=jwt_handler, password_service=password_service)

def _provide_tag_service(tag_repository: _TagRepositoryDependency) -> TagService:
    return TagService(tag_repository=tag_repository)

def _provide_blog_service(blog_repository: _BlogRepositoryDependency, blog_tag_repository : _BlogTagRepositoryDepedency, db : _DatabaseSession) -> BlogService:
    return BlogService(blog_repository=blog_repository, blog_tag_repository=blog_tag_repository, db_session=db)

# Final annotated dependencies for easy use in route handlers
CommentServiceDependency = Annotated[CommentService, Depends(dependency=_provide_comment_service)]
UserServiceDependency = Annotated[UserService, Depends(dependency=_provide_user_services)]
AuthServiceDependency = Annotated[AuthService, Depends(dependency=_provide_auth_service)]
TagServiceDependency = Annotated[TagService, Depends(dependency=_provide_tag_service)]
BlogServiceDependency = Annotated[BlogService, Depends(dependency=_provide_blog_service)]