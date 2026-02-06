from json import JSONDecodeError

from httpx import AsyncClient, HTTPStatusError, RequestError
from pydantic import ValidationError as PydanticError
from typing import List, Dict

from src.constants import ChatRole
from src.config import settings
import src.dependencies as dependencies

from src.data.llm.client import LLMClient
from src.data.llm.openai.constants import MODEL_CHAT_URL
from src.data.llm.openai.models import OpenAIAPIResponse
from src.utils import report_error


class OpenAIClient(LLMClient):
    """
    LLM client implementation for OpenAI API-compatible inference engines.
    """

    def __init__(self):
        """"
        Ollama client initialization routine
        """

        self.active_storage = dependencies.get_active_data_storage()
        self.knowledge_base_loader = dependencies.get_knowledge_base_loader()

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

        # Building chat history to include all the conversation messages
        chat_history = list()
        chat_history.append(await self._get_system_prompt())
        chat_history.extend(await self._build_chat_history(session_id))

        try:
            async with AsyncClient() as client:
                # Sending request with all the data
                # (authorization, messages, etc.)
                response = await client.post(
                    MODEL_CHAT_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {}".format(
                            settings.LLM_PROVIDER_KEY.get_secret_value()
                        )
                    },
                    json={
                        "model": settings.GENERATING_MODEL_NAME,
                        "messages": chat_history,
                    },
                    timeout=20.0
                )
        # Try to fail gracefully in case of any errors
        except HTTPStatusError as e:
            report_error(str(e))
        except RequestError as e:
            report_error(str(e))
        except Exception as e:
            report_error(str(e))

        # Try to parse the response
        # (it may be JSON or text)
        try:
            response.json()
        except JSONDecodeError as e:
            report_error(str(e))
            print(response.text)
            return "Model response is not valid JSON."

        # Validate received data
        try:
            answer = OpenAIAPIResponse.model_validate(
                response.json()
            )
            return answer.choices[0].message.content
        except PydanticError as e:
            print(
                "Model response is not valid OpenAI API response: {}".format(
                    response.json()
                )
            )
            report_error(str(e))
