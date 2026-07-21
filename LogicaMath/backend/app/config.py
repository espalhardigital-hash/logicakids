from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    DATABASE_URL: Optional[str] = Field(None, description="Database connection URL")
    GOOGLE_API_KEY: Optional[str] = Field(None, description="Google Gemini API Key")
    SECRET_KEY: Optional[str] = Field(None, description="JWT Secret Key")
    JWT_ALGORITHM: str = Field("HS256", description="JWT Algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(10080, description="Access Token Expire Minutes")
    
    # S3 / MinIO Configuration
    S3_ACCESS_KEY: Optional[str] = Field(None, description="S3 Access Key")
    S3_SECRET_KEY: Optional[str] = Field(None, description="S3 Secret Key")
    S3_ENDPOINT_URL: Optional[str] = Field(None, description="S3 Endpoint URL")
    S3_PUBLIC_URL: Optional[str] = Field(None, description="S3 Public URL for Frontend")
    MINIO_EXTERNAL_ENDPOINT: Optional[str] = Field(None, description="MinIO External Endpoint URL")
    S3_BUCKET_NAME: Optional[str] = Field(None, description="S3 Bucket Name")
    S3_REGION: str = Field("us-east-1", description="S3 Region")
    
    # Security/CORS
    ENABLE_SECURITY_HEADERS: bool = Field(True, description="Enable Security Headers")
    ALLOWED_ORIGINS: str = Field("*", description="Allowed CORS Origins")
    REDIS_URL: str = Field("redis://redis:6379/0", description="Redis connection string")
    
    # Session / Cookie Mode
    SESSION_MODE: str = Field("token", description="Session mode: 'cookie' or 'token'")
    COOKIE_SECURE: bool = Field(False, description="Cookie Secure flag")
    COOKIE_SAMESITE: str = Field("lax", description="Cookie SameSite attribute")
    
    # Infrastructure & Admin Security
    ENABLE_SYSTEM_CONFIG_ENDPOINT: bool = Field(False, description="Enable /admin/system-config endpoint")
    ENVIRONMENT: str = Field("production", description="Environment: 'development' or 'production'")
    SQL_ECHO: bool = Field(False, description="SQLAlchemy Echo SQL queries")

settings = Settings()
