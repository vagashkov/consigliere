from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import final

from pydantic_settings import BaseSettings


# Build path inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = BASE_DIR / ".env"
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
    OLLAMA_SCHEMA: str = "http"
    OLLAMA_HOST: str = "localhost"
    OLLAMA_PORT: int = 11434

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = ENV_FILE_ENCODING
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
