from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "DriveMart API"
    version: str = "1.0.0"
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/drivemart"

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7 # 7 days
    
    # Cloudinary Config
    cloudinary_cloud_name: str | None = None
    cloudinary_api_key: str | None = None
    cloudinary_api_secret: str | None = None

    # Razorpay Config
    razorpay_key_id: str | None = None
    razorpay_key_secret: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
