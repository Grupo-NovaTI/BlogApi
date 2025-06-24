from datetime import datetime, timezone

from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped
from typing import List
from app.core.db.database import Base



class UserModel(Base):
    __tablename__: str = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False, default="user", server_default="user")
    created_at = Column(DateTime(timezone=True), nullable=True,
                        server_default=func.now(), default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True, server_default=func.now(
    ), onupdate=func.now(), default=datetime.now(tz=timezone.utc))
    blogs  = relationship("BlogModel", back_populates="author", cascade="all, delete-orphan")
    comments  = relationship("CommentModel", back_populates="author", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
