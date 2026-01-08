from http import HTTPStatus
from fastapi.responses import JSONResponse
from typing import List

from src.constants import SESSION_LENGTH
from src.core.models import LLModelDTO, ChatMessageDTO
from src.core.services.llm import LLMService
from src.data.llm.client import LLMClient
from src.data.storage.dialogs.base import ActiveStorage, PersistentStorage

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

MOCK_ANSWER = "Mock answer"


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
        return MOCK_ANSWER


class MockLLMService(LLMService):
    """
    LLM service implementation
    """

    def __init__(self):
        super().__init__()
        self.client = MockLLMClient()


class MockActiveStorage(ActiveStorage):
    """
    Memory-based session storage
    """

    def __init__(self):
        self.sessions: dict[str, list[ChatMessageDTO]] = dict()

    async def get_sessions_list(self) -> List[str]:
        """
        Get all session IDs
        """

        return [
            key for key in self.sessions
        ]

    async def save_message(self, message: ChatMessageDTO) -> bool:
        """
        Save single message into memory storage
        :param message:
        """
        # First check if it is a first session message
        session_data = self.sessions.get(message.session_id)

        if session_data:
            session_data.append(message)
        else:
            self.sessions[message.session_id] = [message]

        return True

    async def load_session(self, session_id: str) -> int:
        """
        Load session with designated ID from a persistent storage
        and uploads it into cache for further use
        :param session_id:
        :return:
        """

        # Get messages from persistent storage
        messages = list()

        for message in messages:
            await self.save_message(message)

        return len(messages)

    async def get_messages(
            self,
            session_id: str,
            limit: int = SESSION_LENGTH
    ) -> List[ChatMessageDTO]:
        """
        Get messages for a session with specified id
        """
        return self.sessions.get(session_id, [])

    async def delete_session(self, session_id: str) -> bool:
        """
        Delete all messages for a session
        """

        self.sessions.pop(session_id, None)

        return True

    async def save_session(
            self,
            session_id: str,
            persistent_storage: PersistentStorage
    ) -> bool:
        """
        Save messages from current session
        :param session_id:
        :param persistent_storage:
        :return:
        """

        return True

    async def save_all_sessions(
            self,
            persistent_storage: PersistentStorage
    ) -> bool:
        """
        Save all sessions to persistent storage
        :return:
        """

        return True


def get_mock_llm_service() -> LLMService:
    return MockLLMService()


def get_mock_active_storage() -> ActiveStorage:
    return MockActiveStorage()

