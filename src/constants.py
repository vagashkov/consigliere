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


class KnowledgeBaseType(str, Enum):
    """
    Knowledge base type selection class
    """

    RAW_TEXT = "raw_text"


class Language(str, Enum):
    """
    Language selection class
    """
    RU = "ru"
    EN = "en"


MAX_PROMPT_LENGTH = 2000
MAX_REQUESTS_PER_MINUTE = 10
MAX_REQUESTS_PER_HOUR = 100
MAX_REQUESTS_PER_DAY = 1000
