from dataclasses import dataclass
import os

@dataclass
class Config:
    app_name: str
    app_version: str
    debug: bool
    
    @staticmethod
    def from_env():
        return Config(
            app_name=os.getenv("APP_NAME", "MyApp"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
            debug=os.getenv("DEBUG", "true").lower() == "true"
        )
        
        
