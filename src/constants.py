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


class StorageType(str, Enum):
    """
    Data storage selection class
    """

    JSON = "json"
    SQLITE = "sqlite"
    POSTGRES = "postgres"


class ChatRole(str, Enum):
    """
    Chat role election class
    """

    USER = "user"
    SYSTEM = "system"
