from typing import Annotated

from fastapi import Depends
from app.users.repositories.user_repository import UserRepository
from app.tags.repositories.tag_repository import TagRepository
from app.blogs.repositories.blog_repository import BlogRepository
from app.core.dependencies.db_depends import DatabaseSession



def _get_user_repository(db: DatabaseSession) -> UserRepository:
    """
    Dependency that provides a UserRepository instance.

    Args:
        db (Session): The database session dependency.

    Returns:
        UserRepository: Instance of the user repository
    """
    return UserRepository(db_session=db)

def _get_tag_repository(db: DatabaseSession) -> TagRepository:
    """
    Dependency that provides a TagRepository instance.

    Args:
        db (Session): The database session dependency.

    Returns:
        TagRepository: Instance of the tag repository
    """
    return TagRepository(db=db)

def _get_blog_repository(db: DatabaseSession) -> BlogRepository:
    """
    Dependency that provides a BlogRepository instance.

    Args:
        db (Session): The database session dependency.

    Returns:
        BlogRepository: Instance of the blog repository
    """
    return BlogRepository(db=db)

UserRepositoryDependency = Annotated[UserRepository, Depends(
    dependency=_get_user_repository)]
TagRepositoryDependency = Annotated[TagRepository, Depends(
    dependency=_get_tag_repository)]
BlogRepositoryDependency = Annotated[BlogRepository, Depends(
    dependency=_get_blog_repository)]
