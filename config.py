from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # Application
    app_name:str = "Nexus Task Manager"
    app_version:str = "1.0.0"
    environment:Literal["development","staging","production"] = "development"
    debug:bool = False
    
    # API
    ap1_v1_prefix:str = "/api/v1"
    api_title:str = "Nexus Task Manager API"
    api_description:str = "Enterprise-grade Task & Resource Management System"
    
    # Database
    database_url: str ="postgresql+asyncpg://postgres:root@localhost:5432/nexus_db"
    database_echo:bool = False
    database_pool_size:int = 20
    database_max_overflow:int = 10
    
    # Security
    secret_key:str = "your-super-key-change-in-prodcution"
    algorithm: str = "HS256"
    access_token_expire_minutes:int = 30
    refresh_token_expire_days:int = 7
    
    
    # CORS
    cors_origins:list = ["http://localhost:3000", "http://localhost:8000"] 
    cors_credentials:bool = True
    cors_methods: list = ["*"] 
    cors_headers:list = ["*"]
    
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
        
def get_settings() -> Settings:
    return Settings() 