from typing import Annotated

from fastapi import Depends

from users.services.user_service import UserService
from tags.services.tag_service import TagService
from auth.services.auth_service import AuthService
from blogs.services.blog_service import BlogService
from core.dependencies.repo_depends import UserRepositoryDependency, TagRepositoryDependency, BlogRepositoryDependency
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

def get_tag_services(tag_repository: TagRepositoryDependency) -> TagService:
    """
    Dependency that provides a TagService instance.

    Args:
        tag_repository (TagRepositoryDependency): The tag repository dependency.

    Returns:
        TagService: Instance of the tag services
    """
    return TagService(tag_repository=tag_repository)

def get_blog_services(blog_repository: BlogRepositoryDependency) -> BlogService:
    """
    Dependency that provides a BlogService instance.

    Args:
        blog_repository (BlogRepositoryDependency): The blog repository dependency.

    Returns:
        BlogService: Instance of the blog services
    """
    return BlogService(blog_repository=blog_repository)

UserServiceDependency = Annotated[UserService, Depends(dependency=get_user_services)]
AuthServiceDependency = Annotated[AuthService, Depends(dependency=get_auth_services)]
TagServiceDependency = Annotated[TagService, Depends(dependency=get_tag_services)]
BlogServiceDependency = Annotated[BlogService, Depends(dependency=get_blog_services)]