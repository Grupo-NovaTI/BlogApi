from typing import List
from app.core.db.database import Base
from app.core.config.application_config import DATABASE_URL
__all__: List[str] = [
    "Base",
    "DATABASE_URL",
]