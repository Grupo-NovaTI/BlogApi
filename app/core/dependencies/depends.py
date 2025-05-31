from typing import Annotated, Type
from sqlalchemy.orm import Session
from fastapi import Depends

from core.db.database import get_db
from users.repositories.user_repository import UserRepository
from utils.repositories.base_repository import BaseRepository

# Definición del tipo para la sesión de base de datos
DatabaseSession = Annotated[Session, Depends(get_db)]

class DependencyProvider:
    """
    Clase proveedora de dependencias que centraliza la gestión de dependencias.
    Facilita la inyección de dependencias y el testing.
    """
    @staticmethod
    def get_repository(repository_class: Type[BaseRepository], db: DatabaseSession) -> BaseRepository:
        """
        Método genérico para obtener cualquier repositorio.
        
        Args:
            repository_class: Clase del repositorio que se desea instanciar
            db (Session): Sesión de base de datos
            
        Returns:
            BaseRepository: Instancia del repositorio solicitado
        """
        return repository_class(db_session=db)

def get_user_repository(db: DatabaseSession) -> UserRepository:
    """
    Dependencia que proporciona una instancia de UserRepository.
    
    Args:
        db (Session): The database session dependency.
    
    Returns:
        UserRepository: Instancia del repositorio de usuarios
    
    Example:
        ```python
        @router.get("/users")
        async def get_users(repo: Annotated[UserRepository, Depends(get_user_repository)]):
            return await repo.get_all()
        ```
    """
    return DependencyProvider.get_repository(repository_class=UserRepository, db=db)  # type: ignore[return-value]

# Dependencias tipadas para uso en los endpoints
UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]