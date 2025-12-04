from json import loads, JSONDecodeError

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
    PULL_MODEL_URL, DELETE_MODEL_URL, MODEL_GENERATE_URL
)
from src.data.storage.json import JSONStorage
from src.utils import report_error


class OllamaClient(LLMClient):
    """
    LLM client implementation for ollama inference engine.
    """

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
                    # timeout is big enough to load LLM into memory
                    timeout=10.0,
                    json={
                        "model": "{}:{}".format(model_name, model_version)
                    },
                )
                response.raise_for_status()
            return JSONResponse(
                content={}, status_code=201
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
                    # timeout is big enough to load LLM into memory
                    timeout=10.0,
                    json={
                        "model": "{}:{}".format(model_name, model_version)
                    },
                )
                response.raise_for_status()
            return JSONResponse(
                content={}, status_code=201
            )
        except Exception as e:
            report_error(str(e))

    async def _get_system_prompt(self) -> str:
        """
        Reads system prompt from file
        :return:
        """

        # Obtain system prompt
        try:
            with open(settings.SYSTEM_PROMPT_FILE, "r") as file:
                return file.read()
        except FileNotFoundError:
            report_error("System prompt file not found.")
            return ""

    async def _build_chat_history(self, session_id: str) -> List[Dict]:
        if session_id:
            saved_messages = await JSONStorage(
                settings.DATA_PATH
            ).get_messages(session_id)
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
        chat_history.extend(await self._build_chat_history(session_id))

        # Getting models list from inference engine
        try:
            async with AsyncClient() as client:
                response = await client.post(
                    MODEL_GENERATE_URL,
                    # timeout is big enough to load LLM into memory
                    timeout=100.0,
                    json={
                        "model": "{}:{}".format(
                            settings.GENERATING_MODEL_NAME,
                            settings.GENERATING_MODEL_VERSION
                        ),
                        "temperature": settings.GENERATING_MODEL_TEMPERATURE,
                        "prompt": prompt,
                        ChatRole.SYSTEM.value: await self._get_system_prompt(),
                        "stream": True
                    }
                )

                full_text = ""

                # Split the response text into lines and process each one
                for line in response.text.split("\n"):
                    # Empty line
                    if not line.strip():
                        continue

                    # Got some answer chunk - let's analyze it
                    try:
                        # Concise answer part
                        data = loads(line)
                        if "response" in data:
                            full_text += data["response"]
                    except JSONDecodeError:
                        # Some gibberish - skip it
                        continue
        except HTTPStatusError as e:
            report_error(str(e))
        except RequestError as e:
            report_error(str(e))
        except Exception as e:
            report_error(str(e))

        # Return result
        return full_text
