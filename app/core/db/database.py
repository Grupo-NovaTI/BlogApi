from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.core.config import DATABASE_URL

from app.utils.logger.application_logger import ApplicationLogger

_logger: ApplicationLogger = ApplicationLogger(name=__name__, log_to_console=False)

_engine: Engine = create_engine(url=DATABASE_URL)

_SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

Base = declarative_base()

def get_db():
    """
    Yields a SQLAlchemy database session and ensures it is closed after use.

    This generator function provides a database session for use in dependency injection,
    such as with FastAPI endpoints. The session is automatically closed after the request
    is completed, ensuring proper resource management.

    Yields:
        Session: An active SQLAlchemy database session.
    """
    db: Session = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initializes the database by creating all tables defined in the SQLAlchemy Base metadata.

    Logs the start and completion of the database initialization process.
    """
    _logger.log_info("Initializing the database...")
    Base.metadata.create_all(bind=_engine)
    _logger.log_info("Database initialization complete.")
