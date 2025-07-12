"""
Defines the UserRole enumeration for user access levels in the application.

This module provides a standardized set of user roles to be used for access control, authorization,
and role-based logic throughout the codebase.
"""

from enum import Enum

class UserRole(str, Enum):
    """
    Enumeration of user roles for access control and permissions.

    Attributes:
        ADMIN (str): Administrator with full access.
        GUEST (str): Guest user with limited access.
        USER (str): Regular user with standard access.
    """
    ADMIN = "admin"
    GUEST = "guest"
    USER = "user"

