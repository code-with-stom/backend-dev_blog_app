from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "Encore Hub"
    PROJECT_V1_STR: str = "/api/v1"
    PROJECT_VERSION: str = "1.0.0"
    
    # Security Settings
    DATABASE_URL: str = getenv("DATABASE_URL")
    JWT_SECRET: str = getenv("JWT_SECRET")
    JWT_ALGORITHM: str = getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_TIMEDELTA: int = 20
    
    # GitHub Settings
    CLIENT_ID: str = getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET: str = getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI: str = getenv("GOOGLE_REDIRECT_URI")
    
settings = Settings()