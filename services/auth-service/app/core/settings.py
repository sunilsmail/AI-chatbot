from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "postgresql+asyncpg://app:app@localhost:5432/ecommerce"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "secret"
    jwt_algorithm: str = "HS256"
    openai_api_key: str = ""

settings = Settings()
