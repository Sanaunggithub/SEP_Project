from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    APP_NAME: str = "Student Management System"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads"
    ALLOWED_FILE_TYPES: list = ["pdf", "docx", "jpg", "jpeg", "png"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()