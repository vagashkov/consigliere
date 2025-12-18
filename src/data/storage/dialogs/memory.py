from datetime import datetime
import json
from redis.commands.json.path import Path as RedisPath
from typing import List

from src.api.v1 import main
from src.data.storage.dialogs.base import Storage
from src.config import get_settings
from src.core.models import ChatMessageDTO
import src.dependencies as dependencies

settings = get_settings()


class MemoryStorage(Storage):
    """
    Memory-based storage
    """

    # def __init__(self):
    #     """
    #     Storage initialization:
    #     """
    #
    #     self.redis = Redis(
    #         host=settings.REDIS_HOST,
    #         port=settings.REDIS_PORT,
    #         db=settings.REDIS_DB
    #     )

    async def save_message(self, message: ChatMessageDTO) -> None:
        """
        Save single message into session-related JSON file
        """

        session_data = main.app.state.redis.json().get(message.session_id)
        if session_data:
            main.app.state.redis.json().arrappend(
                message.session_id,
                RedisPath.root_path(),
                message.model_dump_json()
            )
        else:
            main.app.state.redis.json().set(
                message.session_id,
                RedisPath.root_path(),
                [
                    message.model_dump_json()
                ]
            )

    async def get_messages(
            self,
            session_id: str,
            limit: int = 50
    ) -> List[ChatMessageDTO]:
        """
        Get messages for a session with specified id
        """
        session_data = main.app.state.redis.json().get(session_id)
        if not session_data:
            return []

        message_strings = (
                              main.app.state.redis.json().get(session_id)
                          )[-limit:]
        messages = [
            json.loads(message) for message in message_strings
        ]
        # Convert to Message objects
        return [
            ChatMessageDTO(
                session_id=message.get("session_id"),
                role=message.get("role"),
                content=message.get("content"),
                timestamp=datetime.fromisoformat(
                    message.get("timestamp")
                )
            )
            for message
            in messages
        ]

    async def save_session(self, session_id: str) -> None:
        """
        Save messages from current session
        :param session_id:
        :return:
        """

        session_data = main.app.state.redis.json().get(session_id)
        if not session_data:
            return

        await (
            dependencies.get_persistent_data_storage().save_session(session_id)
        )

    async def delete_session(self, session_id: str) -> None:
        """
        Delete all messages for a session = delete specified file
        """
        main.app.state.redis.json().delete(
            session_id,
            RedisPath.root_path()
        )

    async def get_all_sessions(self) -> List[str]:
        """
        Get all session IDs
        """

        return [
            key for key in main.app.state.redis.keys()
        ]

    async def save_all_sessions(self) -> None:
        """
        Save all sessions to persistent storage
        :return:
        """
        all_sessions = await self.get_all_sessions()

        for session in all_sessions:
            await self.save_session(session)
