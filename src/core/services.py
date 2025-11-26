from abc import ABC, abstractmethod
from typing import List

from src.data.llm.ollama.client import OllamaClient
from src.core.models import LLModelDTO


class LLMService(ABC):
    """
    Abstract base class for LLM services.
    """

    @abstractmethod
    async def list_models(self, active: bool = False) -> List[LLModelDTO]:
        pass


class OllamaLLMService(LLMService):
    """
    LLM service implementation for ollama inference engine.
    """

    def __init__(self):
        self.client = OllamaClient()

    async def list_models(self, active: bool = False) -> List[LLModelDTO]:
        """
        List all available models.
        :param active:
        :return:
        """
        return await self.client.list_models(active)
