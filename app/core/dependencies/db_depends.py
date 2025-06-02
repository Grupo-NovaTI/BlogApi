from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from core.db.database import get_db

DatabaseSession = Annotated[Session, Depends(get_db)]