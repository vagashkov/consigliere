from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Abstract base class for LLM clients.
    """

    @abstractmethod
    async def generate(self, session_id: str, prompt: str):
        pass
