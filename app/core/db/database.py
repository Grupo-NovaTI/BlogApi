from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from utils.logger.file_logger import FileLogger
from core.config.application_config import ApplicationConfig

_database_configuration = ApplicationConfig()

_engine: Engine = create_engine(url=_database_configuration.db_url)

_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

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
    logger = FileLogger(__name__, show_log_file=True)
    Base.metadata.create_all(bind=_engine)
    logger.log_debug("Database initialized successfully.")
