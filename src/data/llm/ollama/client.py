from http import HTTPStatus

from fastapi.responses import JSONResponse
from httpx import AsyncClient, HTTPStatusError, RequestError
from pydantic import TypeAdapter, ValidationError as PydanticError
from typing import List, Dict

from src.constants import HTTPMethod, ChatRole
from src.config import settings
from src.core.models import LLModelDTO

from src.data.llm.client import LLMClient
from src.data.llm.ollama.models import OllamaModelData
from src.data.llm.ollama.constants import (
    LIST_ALL_MODELS_URL, LIST_ACTIVE_MODELS_URL,
    PULL_MODEL_URL, DELETE_MODEL_URL, MODEL_CHAT_URL
)
import src.dependencies as dependencies
from src.utils import report_error


class OllamaClient(LLMClient):
    """
    LLM client implementation for ollama inference engine.
    """

    def __init__(self):
        """"
        Ollama client initialization routine
        """

        self.active_storage = dependencies.get_active_data_storage()
        self.knowledge_base_loader = dependencies.get_knowledge_base_loader()

    async def list_models(self, active: bool = False) -> list[LLModelDTO]:
        # Define necessary inference engine endpoint
        url = LIST_ACTIVE_MODELS_URL if active else LIST_ALL_MODELS_URL

        # Getting models list from inference engine
        try:
            async with AsyncClient() as client:
                response = await client.get(
                    url
                )
        except HTTPStatusError as e:
            report_error(str(e))
        except RequestError as e:
            report_error(str(e))
        except Exception as e:
            report_error(str(e))

        # Validate received data
        try:
            ollama_list = TypeAdapter(list[OllamaModelData]).validate_python(
                response.json().get("models")
            )
        except PydanticError as e:
            report_error(str(e))

        # Return result
        return [
            LLModelDTO.model_validate(
                {
                    "name": model.name,
                    "size": model.size,
                    "format": model.details.format,
                    "parameters": model.details.parameter_size,
                    "quantization_level": model.details.quantization_level
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
        try:
            async with AsyncClient() as client:
                response = await client.post(
                    PULL_MODEL_URL,
                    timeout=10.0,
                    json={
                        "model": "{}:{}".format(model_name, model_version)
                    },
                )
                response.raise_for_status()
            return JSONResponse(
                content={
                    "model_name": model_name,
                    "model_version": model_version
                }, status_code=HTTPStatus.ACCEPTED
            )
        except Exception as e:
            report_error(str(e))

    async def delete_model(self, model_name: str, model_version: str):
        """
        Initiate model deletion by name and version.
        :param model_name:
        :param model_version:
        :return:
        """
        try:
            async with AsyncClient() as client:
                response = await client.request(
                    HTTPMethod.DELETE,
                    DELETE_MODEL_URL,
                    timeout=10.0,
                    json={
                        "model": "{}:{}".format(model_name, model_version)
                    },
                )
                response.raise_for_status()
            return JSONResponse(
                content={
                    "model_name": model_name,
                    "model_version": model_version
                }, status_code=HTTPStatus.ACCEPTED
            )
        except Exception as e:
            report_error(str(e))

    async def _get_knowledge_base(self) -> str:
        """
        Reads knowledge base from file
        :return:
        """

        return self.knowledge_base_loader.load_knowledge_base()

    async def _get_system_prompt(self) -> dict:
        """
        Reads system prompt from file
        :return:
        """

        knowledge_base = await self._get_knowledge_base()
        system_prompt = "Knowledge base: {}".format(
            knowledge_base
            ) if knowledge_base else ""

        # Obtain system prompt
        try:
            with open(settings.SYSTEM_PROMPT_FILE, "r") as file:
                system_prompt += file.read()
                return {
                    "role": ChatRole.SYSTEM.value,
                    "content": system_prompt
                }
        except FileNotFoundError:
            report_error("System prompt file not found.")
            return {}

    async def _build_chat_history(self, session_id: str) -> List[Dict]:
        """
        Recreate chat history both from memory and persistent storage.
        :param session_id:
        :return:
        """

        if session_id:
            saved_messages = (
                await self.active_storage.get_messages(
                    session_id
                )
            )
            return [
                {
                    "role": message.role,
                    "content": message.content
                }
                for message in saved_messages
            ]
        else:
            return []

    async def generate(self, session_id: str, prompt: str) -> str:
        """
        Generate text for specified prompt using LLM.
        :param session_id:
        :param prompt:
        :return:
        """
        chat_history = list()
        chat_history.append(await self._get_system_prompt())
        chat_history.extend(await self._build_chat_history(session_id))

        # Getting models list from inference engine
        try:
            async with AsyncClient() as client:
                response = await client.post(
                    MODEL_CHAT_URL,
                    # timeout is big enough to load LLM into memory
                    timeout=100.0,
                    json={
                        "model": "{}:{}".format(
                            settings.GENERATING_MODEL_NAME,
                            settings.GENERATING_MODEL_VERSION
                        ),
                        "temperature": settings.GENERATING_MODEL_TEMPERATURE,
                        "messages": chat_history,
                        "stream": False
                    }
                )
        except HTTPStatusError as e:
            report_error(str(e))
        except RequestError as e:
            report_error(str(e))
        except Exception as e:
            report_error(str(e))

        # Return result
        return response.json().get("message").get("content")
