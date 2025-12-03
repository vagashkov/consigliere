from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import final

from pydantic_settings import BaseSettings

from src.constants import LLMProviderType


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

    APP_VERSION: str = "1.0"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    LLM_PROVIDER_TYPE: LLMProviderType = "ollama"
    LLM_PROVIDER_SCHEMA: str = "http"
    LLM_PROVIDER_HOST: str = "localhost"
    LLM_PROVIDER_PORT: int = 11434

    EMBEDDING_MODEL_NAME: str = "nomic-embed-text"
    EMBEDDING_MODEL_VERSION: str = "latest"
    GENERATING_MODEL_NAME: str = "gemma3"
    GENERATING_MODEL_VERSION: str = "270m"
    GENERATING_MODEL_TEMPERATURE: float = 0.7

    STORAGE_TYPE: str = "json"
    DATA_PATH: str = ""

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = ENV_FILE_ENCODING
        case_sensitive = True
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.DATA_PATH:
            self.DATA_PATH = BASE_DIR.parent / "data"


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
                "Failed to read .env file"
            ) from e
        else:
            raise RuntimeError(
                ".env file doesn't exist"
            ) from e


settings = get_settings()
