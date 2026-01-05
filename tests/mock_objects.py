from http import HTTPStatus
from fastapi.responses import JSONResponse

from src.core.models import LLModelDTO
from src.core.services.llm import LLMService
from src.data.llm.client import LLMClient

ALL_LLM_MODELS = [
    {
        "name": "smallLLM",
        "size": 380000000,
        "format": "GGUF",
        "parameters": "380M",
        "quantization_level": "16F"
    },
    {
        "name": "mediumLLM",
        "size": 3000000000000,
        "format": "GGUF",
        "parameters": "3b",
        "quantization_level": "8F"
    },
    {
        "name": "largeLLM",
        "size": 200000000000000,
        "format": "GGUF",
        "parameters": "200B",
        "quantization_level": "16F"
    }
]

ACTIVE_LLM_MODELS = ALL_LLM_MODELS[:2]


class MockLLMClient(LLMClient):
    """
    LLM client implementation for ollama inference engine.
    """

    async def list_models(self, active: bool = False) -> list[LLModelDTO]:
        # Define necessary inference engine endpoint
        ollama_list = ACTIVE_LLM_MODELS if active else ALL_LLM_MODELS

        # Return result
        return [
            LLModelDTO.model_validate(
                {
                    "name": model["name"],
                    "size": model["size"],
                    "format": model["format"],
                    "parameters": model["parameters"],
                    "quantization_level": model["quantization_level"]
                }
            ) for model in ollama_list
        ]

    async def pull_model(self, model_name: str, model_version: str):
        """
        Initiate model pulling by name and version.
        :param model_name:
        :param model_version:
        :return:
        """

        return JSONResponse(
            content={
                "model_name": model_name,
                "model_version": model_version
            }, status_code=HTTPStatus.ACCEPTED
        )

    async def delete_model(self, model_name: str, model_version: str):
        """
        Initiate model deletion by name and version.
        :param model_name:
        :param model_version:
        :return:
        """

        return JSONResponse(
            content={
                "model_name": model_name,
                "model_version": model_version
            }, status_code=HTTPStatus.ACCEPTED
        )

    async def generate(self, session_id: str, prompt: str) -> str:
        """
        Generate text for specified prompt using LLM.
        :param session_id:
        :param prompt:
        :return:
        """

        # Return result
        return "Generation result"


class MockLLMService(LLMService):
    """
    LLM service implementation
    """

    def __init__(self):
        super().__init__()
        self.client = MockLLMClient()


def get_mock_llm_service() -> LLMService:
    return MockLLMService()
