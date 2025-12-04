from typing import List

from src.dependencies import get_llm_client
from src.core.models import LLModelDTO


class LLMService:
    """
    LLM service implementation
    """

    def __init__(self):
        super().__init__()
        self.client = get_llm_client()

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

    async def generate(self, session_id: str, prompt: str) -> str:
        """
        Prompt the model with user input.
        :param session_id:
        :param prompt:
        :return:
        """

        return await self.client.generate(session_id, prompt)
