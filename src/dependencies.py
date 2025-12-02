from src.config import get_settings
from src.constants import LLMProviderType, StorageType

from src.data.llm.client import LLMClient
from src.data.llm.ollama.client import OllamaClient
from src.data.llm.openai.client import OpenAIClient

from src.data.storage.base import Storage
from src.data.storage.json import JSONStorage

settings = get_settings()


def get_llm_client() -> LLMClient:
    """
    Get the LLM client according to the settings
    :return:
    """
    match settings.LLM_PROVIDER_TYPE:
        case LLMProviderType.OLLAMA:
            return OllamaClient()
        case LLMProviderType.OPENAI:
            return OpenAIClient()


def get_data_storage() -> Storage:
    """
    Get the LLM client according to the settings
    :return:
    """
    match settings.STORAGE_TYPE:
        case StorageType.JSON:
            return JSONStorage(
                settings.DATA_PATH
            )
