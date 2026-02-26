from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import final

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import LLMProviderType, AuthMethod


# Build path inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = BASE_DIR.parent / ".env"
ENV_FILE_ENCODING = "utf-8"


class Environment(str, Enum):
    """
    Current environment selection class
    """

    # Application running modes
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"

    @property
    def is_developed(self) -> bool:
        return self in (self.DEVELOPMENT, )

    @property
    def is_deployed(self) -> bool:
        return self in (self.PRODUCTION, )


@final
class Settings(BaseSettings):
    """
    Project environment settings definition
    """

    BASE_URL: str = ""
    APP_TITLE: str = "AI Assistant"
    APP_VERSION: str = "1.0"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    DB_DIALECT: str = "postgresql"
    DB_DRIVER: str = "psycopg"
    DB_USERNAME: str = ""
    DB_PASSWORD: SecretStr = ""
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = ""
    DATABASE_URL: str = ""

    # LLM provider details
    LLM_PROVIDER_TYPE: LLMProviderType = "ollama"
    LLM_PROVIDER_SCHEMA: str = "http"
    LLM_PROVIDER_HOST: str = "localhost"
    LLM_PROVIDER_PORT: int = 11434
    LLM_PROVIDER_AUTH_METHOD: AuthMethod = AuthMethod.BEARER
    LLM_PROVIDER_KEY: SecretStr = ""

    # Embedding LLM details
    EMBEDDING_MODEL_NAME: str = "nomic-embed-text"
    EMBEDDING_MODEL_VERSION: str = "latest"

    # Generating LLM details
    GENERATING_MODEL_NAME: str = "gpt-3.5-turbo"
    GENERATING_MODEL_VERSION: str = "270m"
    GENERATING_MODEL_TEMPERATURE: float = 0.7

    # Active data storage type
    ACTIVE_STORAGE_TYPE: str = "app_state"

    # Cache settings
    REDIS_HOST: str = "redis://localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    DATA_PATH: Path = ""
    STATIC_PATH: Path = ""

    # Service data storage details
    PERSISTENT_STORAGE_TYPE: str = "json"

    # Knowledge base configuration
    KNOWLEDGE_BASE_TYPE: str = "raw_text"
    KNOWLEDGE_BASE_PATH: Path = ""
    SYSTEM_PROMPT_FILE: Path = ""

    # Client interaction channels configuration
    # Telegram
    USE_TELEGRAM: bool = False
    TELEGRAM_TOKEN: SecretStr
    TELEGRAM_WEBHOOK_URL: str = ""
    DISABLE_PENDING_MESSAGES: bool = True

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding=ENV_FILE_ENCODING,
        case_sensitive=True,
        extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATA_PATH = BASE_DIR.parent / "data"
        self.STATIC_PATH = BASE_DIR.parent / "static"
        self.SYSTEM_PROMPT_FILE = (
                self.DATA_PATH / "knowledge" / "system_prompt.txt"
        )
        self.KNOWLEDGE_BASE_PATH = (
                self.DATA_PATH / "knowledge" / "documents"
        )
        self.DATABASE_URL = "{}+{}://{}:{}@{}:{}/{}".format(
            self.DB_DIALECT,
            self.DB_DRIVER,
            self.DB_USERNAME,
            self.DB_PASSWORD.get_secret_value(),
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME
        )


@lru_cache()
def get_settings() -> Settings:
    """
    Global settings access point with caching support
    :return:
    """

    try:
        return Settings()
    except Exception as e:
        if ENV_FILE_PATH.exists():
            raise RuntimeError(
                "Failed to read .env file: {}".format(e)
            ) from e
        else:
            raise RuntimeError(
                ".env file doesn't exist"
            ) from e


settings = get_settings()
