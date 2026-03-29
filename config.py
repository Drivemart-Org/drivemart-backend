from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "DriveMart API"
    version: str = "1.0.0"
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/drivemart"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
