from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    SQLITE_URL: str = "sqlite:///data/api.db"
    PROJECT_NAME: str = "py-service-template"
    DEFAULT_API_USER: str = "default"
    DEFAULT_API_KEY: str = "py-service-tempate-df5de656-15d8-4b1d-8660-d158eb736e07"
    DEFAULT_API_DESCRIPTION: str = "default"


settings = Settings()
