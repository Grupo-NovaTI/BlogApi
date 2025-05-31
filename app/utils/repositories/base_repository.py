class BaseRepository:
    
    """
    Clase base para repositorios que proporciona una interfaz común para operaciones CRUD.
    Esta clase debe ser extendida por repositorios específicos de entidades.
    """
    
    def __init__(self, db_session):
        self.db_session = db_session

