from typing import Annotated, Type

from fastapi import Depends
from users.repositories.user_repository import UserRepository
from tags.repositories.tag_repository import TagRepository
from core.dependencies.db_depends import DatabaseSession



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

UserRepositoryDependency = Annotated[UserRepository, Depends(
    dependency=_get_user_repository)]
TagRepositoryDependency = Annotated[TagRepository, Depends(
    dependency=_get_tag_repository)]
