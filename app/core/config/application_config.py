import os

from dotenv import load_dotenv

load_dotenv()


class ApplicationConfig:
    def __init__(self):
        self._app_name = os.getenv(
            key="APP_NAME", default="FastAPI Application")
        self._app_version = os.getenv(key="APP_VERSION", default="1.0.0")
        self._debug = os.getenv(
            key="DEBUG", default="False").lower() in ("true", "1", "yes")
        self._port = os.getenv(key="PORT", default="8000")
        self._host = os.getenv(key="HOST", default="0.0.0.0")
        self._db_url = os.getenv(
            key="DATABASE_URL", default="sqlite:///./test.db")
        self._access_token_expire_minutes = int(
            os.getenv(key="ACCESS_TOKEN_EXPIRE_MINUTES", default=30))
        self._jwt_secret_key = os.getenv(
            key="JWT_SECRET_KEY", default="your_jwt_secret_key")
        self._jwt_algorithm = os.getenv(key="JWT_ALGORITHM", default="HS256")
        self._redis_url = os.getenv(
            key="REDIS_URL", default="redis://localhost:6379/0")

    @property
    def app_name(self) -> str:
        """Get application name."""
        return self._app_name

    @property
    def app_version(self) -> str:
        """Get application version."""
        return self._app_version

    @property
    def debug(self) -> bool:
        """Get debug mode status."""
        return self._debug

    @property
    def port(self) -> str:
        """Get application port."""
        return self._port

    @property
    def host(self) -> str:
        """Get application host."""
        return self._host

    @property
    def redis_url(self) -> str:
        """Get Redis URL."""
        return self._redis_url
    
    @property
    def db_url(self) -> str:
        """Get database URL."""
        return self._db_url

    @property
    def access_token_expire_minutes(self) -> int:
        """Get access token expiration time in minutes."""
        return self._access_token_expire_minutes

    @property
    def jwt_secret_key(self) -> str:
        """Get JWT secret key."""
        return self._jwt_secret_key

    @property
    def jwt_algorithm(self) -> str:
        """Get JWT algorithm."""
        return self._jwt_algorithm
