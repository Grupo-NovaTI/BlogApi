from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    GUEST = "guest"
    USER = "user"

