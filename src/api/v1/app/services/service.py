from abc import ABC, abstractmethod

from httpx import AsyncClient
from pydantic import ValidationError as PydanticError

from src.api.v1.app.constants import (
    LIST_ALL_MODELS_URL, LIST_ACTIVE_MODELS_URL
)
from src.api.v1.app.models.service import LLModelsList
from src.api.v1.app.utils import report_error


class LLMService(ABC):
    """
    Abstract base class for LLM services.
    """

    @abstractmethod
    async def list_models(self, active: bool = False) -> LLModelsList:
        pass


class OllamaLLMService(LLMService):
    """
    LLM service implementation for ollama inference engine.
    """

    async def list_models(self, active: bool = False) -> LLModelsList:
        # Define necessary inference engine endpoint
        url = LIST_ACTIVE_MODELS_URL if active else LIST_ALL_MODELS_URL

        # Getting models list from inference engine
        try:
            async with AsyncClient() as client:
                response = await client.get(
                    url
                )
        except Exception as e:
            report_error(str(e))

        models_list = response.json()

        # Validate received data
        try:
            LLModelsList.model_validate(
                models_list
            )
        except PydanticError as e:
            report_error(str(e))

        # Return result
        return LLModelsList(**models_list)
