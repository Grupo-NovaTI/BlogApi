from typing import Annotated, Type
from sqlalchemy.orm import Session
from fastapi import Depends

from core.db.database import get_db
from users.repositories.user_repository import UserRepository
from utils.repositories.base_repository import BaseRepository

# Database session type definition
_DatabaseSession = Annotated[Session, Depends(get_db)]

class DependencyProvider:
    """
    Dependency provider class that centralizes dependency management.
    Facilitates dependency injection and testing.
    """
    @staticmethod
    def get_repository(repository_class: Type[BaseRepository], db: _DatabaseSession) -> BaseRepository:
        """
        Generic method to obtain any repository.
        
        Args:
            repository_class: Repository class to be instantiated
            db (Session): Database session
            
        Returns:
            BaseRepository: Instance of the requested repository
        """
        return repository_class(db_session=db)

def get_user_repository(db: _DatabaseSession) -> UserRepository:
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
    return DependencyProvider.get_repository(repository_class=UserRepository, db=db)  # type: ignore[return-value]

# Typed dependencies for use in endpoints
UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]