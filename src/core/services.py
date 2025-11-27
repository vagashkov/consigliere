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

    @abstractmethod
    async def pull_model(self, model_name: str, model_version: str):
        pass

    @abstractmethod
    async def delete_model(self, model_name: str, model_version: str):
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

    async def pull_model(self, model_name: str, model_version: str):
        """
        Initiate pulling of a model from ollama models.
        :param model_name:
        :param model_version:
        :return:
        """
        return await self.client.pull_model(model_name, model_version)

    async def delete_model(self, model_name: str, model_version: str):
        """
        Initiate model deletion by ollama engine
        :param model_name:
        :param model_version:
        :return:
        """
        return await self.client.delete_model(model_name, model_version)
