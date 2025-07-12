"""
Constants used throughout the application for validation and pagination.

This module defines regular expression patterns and default values for pagination
that are used in various parts of the application to ensure consistency.
"""

EMAIL_PATTERN: str = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

DEFAULT_PAGE_SIZE: int = 10
DEFAULT_OFFSET: int = 0
