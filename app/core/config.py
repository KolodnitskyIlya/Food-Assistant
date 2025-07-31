from typing import List, Optional
from pydantic import BaseModel, AnyHttpUrl, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseModel):
    title: str
    description: str
    version: str
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_url: Optional[AnyHttpUrl] = None


class DatabaseSettings(BaseModel):
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


class SecuritySettings(BaseModel):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30


class CorsSettings(BaseModel):
    origins: List[AnyHttpUrl] = []


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
    )

    api: ApiSettings
    database: DatabaseSettings
    security: SecuritySettings
    cors: CorsSettings


settings = Settings()

api_config = settings.api
database_config = settings.database
security_config = settings.security
cors_config = settings.cors