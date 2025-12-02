from abc import ABC, abstractmethod
from typing import List

from src.core.models import LLModelDTO


class LLMClient(ABC):
    """
    Abstract base class for LLM clients.
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

    @abstractmethod
    async def generate(self, prompt: str):
        pass
