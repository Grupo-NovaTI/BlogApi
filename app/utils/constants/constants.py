"""
Constants used throughout the application for validation and pagination.

This module defines regular expression patterns and default values for pagination
that are used in various parts of the application to ensure consistency.
"""

from typing import List


EMAIL_PATTERN: str = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PASSWORD_PATTERN: str = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*+.]).{8,}$"
DEFAULT_PAGE_SIZE: int = 10
DEFAULT_OFFSET: int = 0
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_MIME_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]