from enum import Enum


from src.config import settings

# Define LLM provider endpoints list
BASE_URL = "{}://{}:{}".format(
    settings.LLM_PROVIDER_SCHEMA,
    settings.LLM_PROVIDER_HOST,
    settings.LLM_PROVIDER_PORT
)
MODEL_CHAT_URL = "{}/api/v1/chat/completions".format(BASE_URL)


class FinishReason(str, Enum):
    # Supported token generation finish reasons
    STOP = "stop"
    LENGTH = "length"
    TOOL_CALLS = "tool_calls"
    CONTENT_FILTER = "content_filter"
