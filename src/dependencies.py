from src.config import get_settings
from src.constants import (
    LLMProviderType, KnowledgeBaseType,
    ActiveStorageType, PersistentStorageType
)
from src.core.services.llm import LLMService
from src.data.llm.client import LLMClient
from src.data.llm.ollama.client import OllamaClient
from src.data.llm.openai.client import OpenAIClient

from src.data.storage.database.postgres import AsyncLocalSession
from src.data.storage.dialogs.base import ActiveStorage, PersistentStorage
from src.data.storage.dialogs.active.redis import RedisStorage
from src.data.storage.dialogs.persistent.json import JSONStorage

from src.data.storage.knowledge.base import KnowledgeBaseLoader
from src.data.storage.knowledge.raw_text import RawTextLoader

settings = get_settings()


def get_llm_service() -> LLMService:
    return LLMService()


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


def get_active_data_storage() -> ActiveStorage | None:
    """
    Get the LLM client according to the settings
    :return:
    """
    match settings.ACTIVE_STORAGE_TYPE:
        case ActiveStorageType.APP_STATE:
            # TODO: Implement this case
            return None
        case ActiveStorageType.REDIS:
            return RedisStorage()


def get_persistent_data_storage() -> PersistentStorage:
    """
    Get the LLM client according to the settings
    :return:
    """
    match settings.PERSISTENT_STORAGE_TYPE:
        case PersistentStorageType.JSON:
            return JSONStorage(
                settings.DATA_PATH
            )


async def get_db_session() -> AsyncLocalSession:
    """
    Returns live database session object
    :return:
    """

    async with AsyncLocalSession() as session:
        yield session


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
