from typing import Annotated, Type

from fastapi import Depends
from users.repositories.user_repository import UserRepository
from core.dependencies.db_depends import DatabaseSession



def get_user_repository(db: DatabaseSession) -> UserRepository:
    """
    Dependency that provides a UserRepository instance.

    Args:
        db (Session): The database session dependency.

    Returns:
        UserRepository: Instance of the user repository
    """
    return UserRepository(db_session=db)

UserRepositoryDependency = Annotated[UserRepository, Depends(
    dependency=get_user_repository)]
