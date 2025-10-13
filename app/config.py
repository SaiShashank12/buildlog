from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Appwrite Configuration
    appwrite_endpoint: str = "https://cloud.appwrite.io/v1"
    appwrite_project_id: str
    appwrite_api_key: str

    # Database Configuration
    appwrite_database_id: str = "buildlog_db"
    appwrite_projects_collection_id: str = "projects"
    appwrite_build_logs_collection_id: str = "build_logs"

    # Storage Configuration
    appwrite_storage_bucket_id: str = "buildlog_files"

    # Application Settings
    secret_key: str
    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
