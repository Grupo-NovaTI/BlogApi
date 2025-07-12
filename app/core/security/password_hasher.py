"""
Password hashing and verification utility.

This module defines the PasswordHasher class, which provides methods for hashing and verifying
passwords using Passlib's CryptContext with configurable schemes.
"""
from typing import List, Optional

from passlib.context import CryptContext


class PasswordHasher:
    """
    A class for hashing and verifying passwords using Passlib.
    """
    def __init__(self, schemes: Optional[List[str]] = None, deprecated: str = "auto") -> None:
        """
        Initializes the PasswordHasher with specified hashing schemes.

        Args:
            schemes (Optional[List[str]]): List of hashing schemes to use (default is ['bcrypt', 'pbkdf2_sha256']).
            deprecated (str): Deprecated schemes handling (default is 'auto').
        """
        if schemes is None:
            schemes = ['bcrypt', 'pbkdf2_sha256']
        self.pwd_context = CryptContext(schemes=schemes, deprecated=deprecated)

    def hash_password(self, password: str) -> str:
        """
        Hashes a password using the configured hashing schemes.

        Args:
            password (str): The plain password to hash.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(secret=password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain password against a hashed password.

        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.pwd_context.verify(secret=plain_password, hash=hashed_password)

