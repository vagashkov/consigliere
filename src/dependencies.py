from src.config import get_settings
from src.constants import LLMProviderType
from src.data.llm.client import LLMClient
from src.data.llm.ollama.client import OllamaClient
from src.data.llm.openai.client import OpenAIClient


class LLMClientDependency:
    @staticmethod
    def get_llm_client() -> LLMClient:
        """
        Get the LLM client according to the settings
        :return:
        """
        match get_settings().LLM_PROVIDER_TYPE:
            case LLMProviderType.OLLAMA:
                return OllamaClient()
            case LLMProviderType.OPENAI:
                return OpenAIClient()
