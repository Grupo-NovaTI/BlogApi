from typing import List, Optional
from passlib.context import CryptContext




class PasswordHasher:
    """A class for hashing and verifying passwords using Passlib."""
    def __init__(self, schemes: Optional[List[str]] = None, deprecated: str = "auto"):
        """
        Initializes the PasswordHasher with specified hashing schemes.
        
        Args:
            schemes: List of hashing schemes to use (default is ['bcrypt', 'pbkdf2_sha256']).
            deprecated: Deprecated schemes handling (default is 'auto').
        """
        if schemes is None:
            schemes = ['bcrypt', 'pbkdf2_sha256']
        self.pwd_context = CryptContext(schemes=schemes, deprecated=deprecated)

    def hash_password(self, password: str) -> str:
        """Hashes a password using the configured hashing schemes."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain password against a hashed password."""
        return self.pwd_context.verify(plain_password, hashed_password)

