
import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from test import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine: Engine = create_engine(url=SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Fixtures ---

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture de Pytest que crea una nueva base de datos y sesión para cada función de prueba.
    Garantiza que las pruebas estén aisladas entre sí.
    """
    Base.metadata.create_all(bind=engine)
    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
