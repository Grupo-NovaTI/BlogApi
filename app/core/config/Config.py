import os

from dotenv import load_dotenv

load_dotenv()

class Config:    
    def __init__(self):
        self.app_name = os.getenv(key="APP_NAME", default="FastAPI Application")
        self.app_version = os.getenv(key="APP_VERSION", default="1.0.0")
        self.debug = os.getenv(key="DEBUG", default="False").lower() in ("true", "1", "yes")
        self.port = os.getenv(key="PORT",default= "8000")
        self.host = os.getenv(key="HOST", default="0.0.0.0")
        self.db_url = os.getenv(key="DATABASE_URL", default="sqlite:///./test.db")

