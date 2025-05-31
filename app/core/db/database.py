from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from core.config.config import Config

database_url: str = Config().db_url

engine: Engine = create_engine(url="postgresql+psycopg2://postgres:postgres@db/postgres")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency that provides a database session.
    This function should be used in FastAPI routes to get a database session.
    
    Yields:
        Session: A database session that can be used to interact with the database.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize the database by creating all tables.
    This function should be called at the start of the application.
    """
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
