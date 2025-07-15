"""
Application configuration settings.

This module loads environment variables and provides application-wide configuration constants
for versioning, debug mode, host/port, database, Redis, and JWT authentication.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Application configuration settings
APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
APP_NAME: str = os.getenv("APP_NAME", "FastAPI Application")
# Debug mode
DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
# Host and port configuration
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: str = os.getenv("PORT", "8000")
# Database configuration
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# Redis configuration
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
# JWT configuration
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
if JWT_SECRET_KEY == "":
    raise ValueError("JWT_SECRET_KEY environment variable is not set.")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_OAUTH_SCHEME = "api/v1/auth/login"
# Access token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
# Cloud Storage Configuration
CLOUD_STORAGE_CONNECTION_STRING: str = os.getenv(
    "CLOUD_STORAGE_CONNECTION_STRING", "")
if CLOUD_STORAGE_CONNECTION_STRING == "":
    raise ValueError(
        "CLOUD_STORAGE_CONNECTION_STRING environment variable is not set.")
CLOUD_STORAGE_CONTAINER_NAME: str = os.getenv("CLOUD_STORAGE_CONTAINER_NAME", "")
if CLOUD_STORAGE_CONTAINER_NAME == "":
    raise ValueError(
        "CLOUD_STORAGE_CONTAINER_NAME environment variable is not set.")
