from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Application
    app_name: str = "RIAM Learning Management System"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./riam_lms.db"
    
    # JWT Settings
    jwt_secret_key: str = "riam-lms-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 24  # 24 hours
    
    # AWS Settings
    aws_region: str = "us-west-2"  # Bedrock region
    aws_profile: str = ""  # AWS profile for local development (empty = use IAM role)
    s3_bucket_name: str = "riam-lms-recordings"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    
    # RIAM Framework Categories
    riam_categories: list[str] = [
        "Technical Skill and Competence",
        "Compositional and Musicianship Knowledge",
        "Repertoire and Cultural Knowledge",
        "Performing Artistry"
    ]
    
    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
