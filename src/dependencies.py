from src.config import get_settings
from src.constants import LLMProviderType, StorageType, KnowledgeBaseType

from src.data.llm.client import LLMClient
from src.data.llm.ollama.client import OllamaClient
from src.data.llm.openai.client import OpenAIClient

from src.data.storage.dialogs.base import Storage
from src.data.storage.dialogs.json import JSONStorage
from src.data.storage.dialogs.memory import MemoryStorage

from src.data.storage.knowledge.base import KnowledgeBaseLoader
from src.data.storage.knowledge.raw_text import RawTextLoader

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
        case StorageType.MEMORY:
            return MemoryStorage()
        case StorageType.JSON:
            return JSONStorage(
                settings.DATA_PATH
            )


def get_persistent_data_storage() -> Storage:
    """
    Get the LLM client according to the settings
    :return:
    """
    match settings.PERSISTENT_STORAGE_TYPE:
        case StorageType.JSON:
            return JSONStorage(
                settings.DATA_PATH
            )


def get_knowledge_base_loader() -> KnowledgeBaseLoader:
    """
    Get the knowledge base loader according to the settings
    :return:
    """
    match settings.KNOWLEDGE_BASE_TYPE:
        case KnowledgeBaseType.RAW_TEXT:
            return RawTextLoader(
                settings.DATA_PATH
            )
