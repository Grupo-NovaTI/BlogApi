"""
Application configuration settings.

This module loads environment variables and provides application-wide configuration constants
for versioning, debug mode, host/port, database, Redis, and JWT authentication.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Application configuration settings
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_NAME = os.getenv("APP_NAME", "FastAPI Application")
# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
# Host and port configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", "8000")
# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
# JWT configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_OAUTH_SCHEME = "api/v1/auth/login"
# Access token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
