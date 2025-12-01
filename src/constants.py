from enum import Enum


class HTTPMethod(str, Enum):
    # Supported HTTP methods
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


class LLMProviderType(str, Enum):
    """
    LLM provider selection class
    """

    OLLAMA = "ollama"
    OPENAI = "OpenAI"
