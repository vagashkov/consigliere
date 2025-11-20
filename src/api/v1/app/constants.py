from enum import Enum

from src.api.v1.app.config import settings


class HTTPMethod(str, Enum):
    # Supported HTTP methods
    GET = "GET"
    POST = "POST"


# Define LLM provider endpoints list
BASE_URL = "{}://{}:{}".format(
    settings.OLLAMA_SCHEMA,
    settings.OLLAMA_HOST,
    settings.OLLAMA_PORT
)
LIST_ALL_MODELS_URL = "{}/api/tags".format(BASE_URL)
LIST_ACTIVE_MODELS_URL = "{}/api/ps".format(BASE_URL)
