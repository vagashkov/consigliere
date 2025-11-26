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
