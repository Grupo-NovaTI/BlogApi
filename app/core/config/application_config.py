import os

from dotenv import load_dotenv

load_dotenv()

class ApplicationConfig:    
    def __init__(self):
        self._app_name = os.getenv(key="APP_NAME", default="FastAPI Application")
        self._app_version = os.getenv(key="APP_VERSION", default="1.0.0")
        self._debug = os.getenv(key="DEBUG", default="False").lower() in ("true", "1", "yes")
        self._port = os.getenv(key="PORT",default= "8000")
        self._host = os.getenv(key="HOST", default="0.0.0.0")
        self._db_url = os.getenv(key="DATABASE_URL", default="sqlite:///./test.db")
        
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
    def db_url(self) -> str:
        """Get database URL."""
        return self._db_url

