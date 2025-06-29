from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.core.config.application_config import ApplicationConfig

from app.utils.logger.application_logger import ApplicationLogger

_logger: ApplicationLogger = ApplicationLogger(name=__name__, log_to_console=False)

_database_configuration = ApplicationConfig()

_engine: Engine = create_engine(url=_database_configuration.db_url)

_SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

Base = declarative_base()

def get_db():
    """
    Dependency that provides a database session.
    This function should be used in FastAPI routes to get a database session.
    
    Yields:
        Session: A database session that can be used to interact with the database.
    """
    db: Session = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize the database by creating all tables.
    This function should be called at the start of the application.
    """
    _logger.log_info("Initializing the database...")
    Base.metadata.create_all(bind=_engine)
    _logger.log_info("Database initialization complete.")
