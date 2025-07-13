"""
User model definition for the application's database.

This module defines the UserModel class, which represents a user entity in the system.
It includes fields for authentication, personal information, role, and relationships to blogs and comments.
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.database import Base


class UserModel(Base):
    """
    SQLAlchemy ORM model for the 'users' table.

    Represents a user in the system, including authentication details, personal information,
    role, timestamps, and relationships to blogs and comments.
    """
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
    profile_picture = Column(String, nullable=True, default="https://imgs.search.brave.com/JqLkOW5ls518f8t5iH3rCS376Any3y5s4Jko9jGBHgg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/a2luZHBuZy5jb20v/cGljYy9tLzI0LTI0/ODI1M191c2VyLXBy/b2ZpbGUtZGVmYXVs/dC1pbWFnZS1wbmct/Y2xpcGFydC1wbmct/ZG93bmxvYWQucG5n")
    blogs  = relationship("BlogModel", back_populates="user", cascade="all, delete-orphan")
    comments  = relationship("CommentModel", back_populates="user", cascade="all, delete-orphan")


    def __repr__(self):
        """
        Return a string representation of the UserModel instance for debugging.

        Returns:
            str: A string with the user's id, username, and email.
        """
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def __str__(self):
        """
        Return a human-readable string representation of the UserModel instance.

        Returns:
            str: A string with the user's id, username, and email.
        """
        return f"User(id={self.id}, username={self.username}, email={self.email})"
